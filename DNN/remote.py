import sys
import os
from base64 import b64decode

os.environ['KERAS_BACKEND'] = 'tensorflow'


from keras.models import Sequential
from keras.layers.core import Dense, Dropout
from keras.layers import BatchNormalization
from keras.optimizers import Adam
from argparse import ArgumentParser

import config

# Parse the arguments
parser = ArgumentParser()
parser.add_argument( "-y",  "--year" )
parser.add_argument( "-s",  "--seedvars" )
parser.add_argument( "-nj", "--NJETS" )
parser.add_argument( "-nb", "--NBJETS" )
parser.add_argument( "-ht", "--AK4HT" )
parser.add_argument( "-met", "--MET" )
parser.add_argument( "-lpt", "--LEPPT" )
parser.add_argument( "-mt", "--MT" )
parser.add_argument( "-dr", "--MINDR" )
args = parser.parse_args()

sys.argv = []
import jobtracker as jt
from ROOT import TMVA, TCut, TFile

seed_vars = set(b64decode(args.seedvars).split(","))

print(">> TTT Condor Job using {} samples".format( config.step2Sample[ args.year ] ) )

# Initialize TMVA
TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()

inputDir = config.step2DirXRD[ args.year ] + "nominal/"
loader = TMVA.DataLoader( "tmva_data" )
factory = TMVA.Factory("VariableImportance",
                       "!V:!ROC:Silent:!Color:!DrawProgressBar:Transformations=I;:AnalysisType=Classification")

# Add variables from seed to loader
num_vars = 0
print( ">> Using the following variables: " )
for var_data in config.varList["DNN"]:
  if var_data[0] in seed_vars:
    num_vars += 1
    print( "    {:<4} {}".format( str(num_vars) + ".", var_data[0] ) )
    loader.AddVariable( var_data[0], var_data[1], "", "F" )
    
# Add signal and background trees to loader
print( ">> Loading trees" )
sFiles, bFiles = [], []
sTrees, bTrees = [], []
for sig in config.sig_training[ args.year ]:
  sFiles.append( TFile.Open( inputDir + sig ) )
  sTree = sFiles[-1].Get("ljmet")
  sTree.SetBranchStatus( "*", 0 )
  for vName in config.branches:
    sTree.SetBranchStatus( vName, 1 )
  sTrees.append( sTree )
  sTrees[-1].GetEntry(0)
  loader.AddSignalTree( sTrees[-1], 1 )


for bkg in config.bkg_training[ args.year ]:
  bFiles.append( TFile.Open( inputDir + bkg ) )
  bTree = bFiles[-1].Get( "ljmet" )
  bTree.SetBranchStatus( "*", 0 )
  for vName in config.branches:
    bTree.SetBranchStatus( vName, 1 )
  bTrees.append( bTree )
  bTrees[-1].GetEntry(0)
  if bTree.GetEntries() != 0:
    loader.AddBackgroundTree( bTrees[-1], 1 )


# Set weights and cuts
cutStr = config.base_cut
cutStr += " && ( isTraining == 2 || isTraining == 3 )"
cutStr += " && ( NJetsCSV_JetSubCalc >= {} ) && ( NJets_JetSubCalc >= {} )".format( args.NBJETS, args.NJETS ) 
cutStr += " && ( AK4HT > {} ) && ( corr_met_MultiLepCalc > {} ) && ( MT_lepMet > {} ) && ( minDR_lepJet > {} )".format( args.AK4HT, args.MET, args.MT, args.MINDR )
cutStr += " && ( leptonPt_MultiLepCalc > {})".format( args.LEPPT ) 

loader.SetSignalWeightExpression( "1" )
#loader.SetBackgroundWeightExpression( config.weightStr )
loader.SetBackgroundWeightExpression( "1" )

cut = TCut( cutStr )

# Prepare tree
loader.PrepareTrainingAndTestTree( 
    cut, cut, 
    "SplitMode=Random:NormMode=NumEvents:!V:nTrain_Signal=10000:nTrain_Background=10000"
)

# Build model
print( ">> Building Model" )
model_name = "TTT_TMVA_model.h5"
model = Sequential()
model.add( Dense( num_vars,
                input_dim = num_vars,
                activation = "relu") )
for _ in range( 2 ):
    model.add( Dropout( 0.5 ) )
    model.add( Dense( 32, activation = "relu" ) )
model.add( Dense( 2, activation="sigmoid" ) )

model.compile(
    loss = "categorical_crossentropy",
    optimizer = Adam(),
    metrics = [ "accuracy" ]
)

model.save( model_name )
model.summary()

factory.BookMethod(
    loader,
    TMVA.Types.kPyKeras,
    "PyKeras",
    "!H:!V:VarTransform=G:FilenameModel=" + model_name + ":NumEpochs=15:BatchSize=128:SaveBestOnly=true"
)

(TMVA.gConfig().GetIONames()).fWeightFileDir = "weights"

# Train
print( ">> Training model" )
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

# Get Results
ROC = factory.GetROCIntegral( loader, "PyKeras")
print( "ROC-integral: {}".format( ROC ) )

factory.DeleteAllMethods()
factory.fMethodsMap.clear()
