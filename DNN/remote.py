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
parser.add_argument( "-j0", "--JET0PT" )
parser.add_argument( "-j1", "--JET1PT" )
parser.add_argument( "-j2", "--JET2PT" )
args = parser.parse_args()

sys.argv = []
import jobtracker as jt
from ROOT import TMVA, TCut, TFile

seed_vars = set(b64decode(args.seedvars).split(","))

print(">> TTT Condor Job using {} samples".format( config.step2Sample[ args.year ] ) )

# Initialize TMVA
TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()

inputDir = config.step2DirEOS[ args.year ] + "nominal/"
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
signals = []
signal_trees = []
backgrounds = []
background_trees = []  
for sig in config.sig_training[ args.year ]:
  signals.append( TFile.Open( inputDir + sig ) )
  signal_trees.append( signals[-1].Get("ljmet") )
  signal_trees[-1].GetEntry(0)
  loader.AddSignalTree( signal_trees[-1], 1 )

for bkg in config.bkg_training[ args.year ]:
  backgrounds.append( TFile.Open( inputDir + bkg ) )
  background_trees.append( backgrounds[-1].Get( "ljmet" ) )
  background_trees[-1].GetEntry(0)
  if background_trees[-1].GetEntries() != 0:
    loader.AddBackgroundTree( background_trees[-1], 1 )

# Set weights and cuts
cutStr = config.base_cut
cutStr += " && ( NJetsCSV_MultiLepCalc >= {} )".format( args.NBJETS ) 
cutStr += " && ( NJets_JetSubCalc >= {} )".format( args.NJETS )
cutStr += " && ( AK4HT > {} ) && ( corr_met_MultiLepCalc > {} ) && ( MT_lepMet > {} ) && ( minDR_lepJet > {} )".format( args.AK4HT, args.MET, args.MT, args.MINDR ) 
cutStr += " && ( ( leptonPt_MultiLepCalc > {} && isElectron == 1 ) || ( leptonPt_MultiLepCalc > {} && isMuon == 1 ) )".format( args.LEPPT, args.LEPPT ) 
cutStr += " && ( theJetPt_JetSubCalc_PtOrdered[0] > {} ) && ( theJetPt_JetSubCalc_PtOrdered[1] > {} ) && ( theJetPt_JetSubCalc_PtOrdered[2] > {} )".format( args.JET0PT, args.JET1PT, args.JET2PT )

loader.SetSignalWeightExpression( config.weightStr )
loader.SetBackgroundWeightExpression( config.weightStr )

cut = TCut( cutStr )

# Prepare tree
loader.PrepareTrainingAndTestTree( 
    cut, cut, 
    "SplitMode=Random:NormMode=NumEvents:!V"
)

# Build model
model_name = "TTT_TMVA_model.h5"
model = Sequential()
model.add( Dense( num_vars,
                input_dim = num_vars,
                activation = "relu") )
for _ in range( 3 ):
    model.add( BatchNormalization() )
    model.add( Dropout( 0.3 ) )
    model.add( Dense( 50, activation = "relu" ) )
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
    "!H:!V:VarTransform=G:FilenameModel=" + model_name + ":NumEpochs=50:TriesEarlyStopping=10:BatchSize=512:SaveBestOnly=true"
)

(TMVA.gConfig().GetIONames()).fWeightFileDir = "weights"

# Train
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

# Get Results
ROC = factory.GetROCIntegral( loader, "PyKeras")
print( "ROC-integral: {}".format( ROC ) )

factory.DeleteAllMethods()
factory.fMethodsMap.clear()
