import os, sys
import tqdm
import numpy as np
from array import array
from pickle import load as pickle_load
from pickle import dump as pickle_dump

os.environ["KERAS_BACKEND"] = "tensorflow"

from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import initializers
from tensorflow.keras import activations
from tensorflow.keras import optimizers
from tensorflow.keras import callbacks
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.backend import clear_session

import ROOT
import uproot

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.model_selection import ShuffleSplit
from sklearn.utils import shuffle as shuffle_data

import config

# The parameters to apply to the cut.

CUT_VARIABLES = [
  "leptonPt_MultiLepCalc", "isElectron", "isMuon",
  "corr_met_MultiLepCalc", "MT_lepMet", "minDR_lepJet",
  "DataPastTriggerX", "MCPastTriggerX", "isTraining", 
  "AK4HT", "NJetsCSV_JetSubCalc", "NJets_JetSubCalc" 
]

WEIGHT_VARIABLES = [
  "triggerXSF", "pileupWeight", "lepIdSF", 
  "EGammaGsfSF", "isoSF", "L1NonPrefiringProb_CommonCalc",
  "MCWeight_MultiLepCalc", "xsecEff", "tthfWeight",
  "btagDeepJetWeight", "btagDeepJet2DWeight_HTnj"
]

ML_VARIABLES = [ x[0] for x in config.varList[ "DNN" ] ]
VARIABLES = list( sorted( list( set( ML_VARIABLES ).union( set( CUT_VARIABLES ) ).union( set( WEIGHT_VARIABLES ) ) ) ) )

config.params[ "KFCV" ][ "SAVE AUC POINTS" ] = 20

print("[INFO] mltools.py using {} variables.".format(len(VARIABLES)))

class MLTrainingInstance(object):
  def __init__(self, signal_paths, background_paths, variables, ratio, selection):
    self.signal_paths = signal_paths
    self.background_paths = background_paths
    self.samples = signal_paths + background_paths
    self.variables = variables
    self.ratio = ratio
    self.selection = selection

  def load_cut_events( self, path, weighted, override ):
    self.cut_events = {}
    if override:
      print( "[START] Overriding existing events" )
      self.apply_cut()
      self.save_cut_events( path, weighted )
      print( "[DONE] New cut events saved." )
    rFile = uproot.open( path )
    rTreeSig = rFile[ "signal" ]
    rTreeBkg = rFile[ "background" ]
    self.cut_events["TOTAL SIGNAL"] = rTreeSig.pandas.df( self.variables )
    self.cut_events["TOTAL BACKGROUND"] = rTreeBkg.pandas.df( self.variables )

  def apply_cut( self ): # applies cuts to events as well as computing the event weight from the cut events to set relative proportion of events
    print( "[START] Applying event selection..." )
    print( "[INFO] Event selection: {}".format( self.selection ) )
    self.cut_events = { "SIGNAL": {}, "TOTAL SIGNAL": {}, "BACKGROUND": {}, "TOTAL BACKGROUND": {} }
    ROOT.gInterpreter.Declare("""
    float compute_weight( float triggerXSF, float pileupWeight, float lepIdSF, float isoSF, float L1NonPrefiringProb_CommonCalc, float MCWeight_MultiLepCalc, float xsecEff, float tthfWeight, float btagDeepJetWeight, float btagDeepJet2DWeight_HTnj ){
      return triggerXSF * pileupWeight * lepIdSF * isoSF * L1NonPrefiringProb_CommonCalc * ( MCWeight_MultiLepCalc / abs( MCWeight_MultiLepCalc ) ) * xsecEff * tthfWeight * btagDeepJetWeight * btagDeepJet2DWeight_HTnj;
    }
    """)
    self.nPass = {} # store the number of events passing for each process
    self.nTotal = {} # store the total number of events for each process
    self.nWeight = {} # store the weighted number of events passing for each process
    self.nSigTot = 0
    self.nSigPass = 0
    self.nSigWeight = 0 
    for path in self.signal_paths:
      print( "  >> Applying cuts to {}...".format( path.split("/")[-1] ) )
      rDF = ROOT.RDataFrame( "ljmet", path )
      rDF_selection = rDF.Filter( self.selection ).Define( "weight", "compute_weight( triggerXSF, pileupWeight, lepIdSF, isoSF, L1NonPrefiringProb_CommonCalc, MCWeight_MultiLepCalc, xsecEff, tthfWeight, btagDeepJetWeight, btagDeepJet2DWeight_HTnj )" )
      nDF = rDF_selection.AsNumpy( columns = self.variables + [ "weight" ] )
      self.nTotal[path]  = float( rDF.Count().GetValue() )
      self.nPass[path]   = float( len( nDF[ "weight" ] ) )
      self.nWeight[path] = np.sum( nDF[ "weight" ] )
      self.nSigTot    += self.nTotal[path]
      self.nSigPass   += self.nPass[path]
      self.nSigWeight += self.nWeight[path]
      self.cut_events["SIGNAL"][path] = nDF
      print( "    + {}/{} events passed, event weight = {:.2f}".format( int( self.nPass[path] ), int( self.nTotal[path] ), self.nWeight[path] ) )

    self.nBkgTot = 0
    self.nBkgPass = 0
    self.nBkgWeight = 0
    for path in self.background_paths:
      print( "  >> Applying cuts to {}...".format( path.split("/")[-1] ) )
      rDF = ROOT.RDataFrame( "ljmet", path )
      rDF_selection = rDF.Filter( self.selection ).Define( "weight", "compute_weight( triggerXSF, pileupWeight, lepIdSF, isoSF, L1NonPrefiringProb_CommonCalc, MCWeight_MultiLepCalc, xsecEff, tthfWeight, btagDeepJetWeight, btagDeepJet2DWeight_HTnj )" )
      nDF = rDF_selection.AsNumpy( columns = self.variables + [ "weight" ] )
      self.nTotal[path]  = float( rDF.Count().GetValue() )
      self.nPass[path]   = float( len( nDF[ "weight" ] ) )
      self.nWeight[path] = np.sum( nDF[ "weight" ] )
      self.nBkgTot    += self.nTotal[path]
      self.nBkgPass   += self.nPass[path]
      self.nBkgWeight += self.nWeight[path]
      self.cut_events["BACKGROUND"][path] = nDF
      print( "    + {}/{} events passed, event weight = {:.2f}".format( int(self.nPass[path]), int(self.nTotal[path]), self.nWeight[path] ) )

    print( "[INFO] Event Selection:" )
    print( "  + Signal: {}/{}, Weighted: {:.1f}".format( int(self.nSigPass), int(self.nSigTot), self.nSigWeight ) )
    print( "  + Background: {}/{}, Weighted: {:.1f}".format( int(self.nBkgPass), int(self.nBkgTot), self.nBkgWeight ) )
    del rDF, rDF_selection

  def save_cut_events( self, folder, weighted = True ):
    self.rFile = ROOT.TFile.Open( folder, "RECREATE" )
    self.rTreeSig = ROOT.TTree( "signal", folder )
    self.rVariablesSig = {}
    for variable in self.variables:
      self.rVariablesSig[variable] = { "ARRAY": array( "f", [0] ), "STRING": "{}/F".format( variable ) }
      self.rTreeSig.Branch( variable, self.rVariablesSig[variable]["ARRAY"], self.rVariablesSig[variable]["STRING"] )
    print( "[START] Filling signal tree" )
    for path in self.cut_events["SIGNAL"]:
      print( "  + {}: {} events".format( path.split("/")[-1], self.nPass[path] ) )
      for i in tqdm.tqdm( range( int( self.nPass[path] ) ) ):
        for variable in self.variables:
          self.rVariablesSig[ variable ][ "ARRAY" ][0] = self.cut_events["SIGNAL"][path][variable][i]
        self.rTreeSig.Fill()
   
    print( "[START] Filling background tree" )
    self.rTreeBkg = ROOT.TTree( "background", folder )
    self.rVariablesBkg = {}
    for variable in self.variables:
      self.rVariablesBkg[variable] = { "ARRAY": array( "f", [0] ), "STRING": "{}/F".format( variable ) }
      self.rTreeBkg.Branch( variable, self.rVariablesBkg[variable]["ARRAY"], self.rVariablesBkg[variable]["STRING"] ) 
    
    scaleMax = 0 # placeholder for the minimum scaling of a background event
    for path in self.cut_events["BACKGROUND"]:
      scaleMax = np.max( [ scaleMax, ( self.nWeight[path] / self.nBkgWeight ) * self.nBkgPass / self.nPass[path] ] )
    for path in self.cut_events["BACKGROUND"]:
      nKeep = ( self.nWeight[path] / self.nBkgWeight ) * self.nBkgPass / scaleMax if weighted else self.nPass[path] # scale by cross section and keep only number of events available
      if self.ratio > 0:
        if weighted:
          nKeep = int( nKeep / ( ( self.nBkgPass / scaleMax ) / ( self.nSigPass * self.ratio ) ) ) # scale down to meet signal-to-background ratio
        else:
          nKeep = min( int( nKeep ), int( ( self.nSigPass * self.ratio ) / len( self.cut_events["BACKGROUND"].keys() ) ) ) # each background should equally contribute to meet signal-to-background ratio
      print( "  + {}: {} / {} events".format( path.split("/")[-1], nKeep, int( self.nPass[path] ) ) )
      for i in tqdm.tqdm( range( nKeep ) ):
        for variable in self.variables:
          self.rVariablesBkg[ variable ][ "ARRAY" ][0] = self.cut_events["BACKGROUND"][path][variable][i]
        self.rTreeBkg.Fill() 

    self.rFile.Write()
    self.rFile.Close()

  def build_model(self):
    # Override with the code that builds the Keras model.
    pass

  def train_model(self):
    # Train the model on the singal and background data formatted with pickle
    pass        
	
class HyperParameterModel(MLTrainingInstance):
  def __init__( self, parameters, signal_paths, background_paths, variables, ratio, selection, model_name=None):
    MLTrainingInstance.__init__( self, signal_paths, background_paths, variables, ratio, selection)
    self.parameters = parameters
    self.model_name = model_name
    self.variables = variables

  def select_ml_variables(self, sig_events, bkg_events, varlist):
    # Select which variables from ML_VARIABLES to use in training
    positions = { v: self.variables.index(v) for v in varlist }
    var_mask = [ positions[v] for v in sorted( positions.keys() ) ]
    return np.concatenate( ( np.array( sig_events )[:, var_mask], np.array( bkg_events )[:, var_mask] ) )

  def build_model(self):
    self.model = models.Sequential()
    self.model.add( layers.Dense(
      int( self.parameters[ "HIDDEN NODES" ] ),
      input_dim = len( self.parameters["VARIABLES"] ),
      kernel_initializer = self.parameters[ "KERNEL INITIALIZER" ],
      kernel_regularizer = None if self.parameters[ "KERNEL REGULARIZER" ] == "NONE" else self.parameters[ "KERNEL REGULARIZER" ], 
      kernel_constraint = None if self.parameters[ "KERNEL CONSTRAINT" ] == "NONE" else self.parameters[ "KERNEL CONSTRAINT" ],
      bias_regularizer = None if self.parameters[ "BIAS REGULARIZER" ] == "NONE" else self.parameters[ "BIAS REGULARIZER" ],
      activation = self.parameters[ "ACTIVATION FUNCTION" ],
      activity_regularizer = None if self.parameters[ "ACTIVATION REGULARIZER" ] == "NONE" else self.parameters[ "ACTIVATION REGULARIZER" ]
    ) )
    if self.parameters[ "TRAINING REGULATOR" ] in [ "DROPOUT", "BOTH" ]:
      self.model.add( layers.Dropout( config.params[ "DROPOUT" ] ) ) # 50% dropout per the original paper by Hinton et. al (2012), remaining weights scaled by 1 / ( 1 - RATE )
    if self.parameters[ "TRAINING REGULATOR" ] in [ "BATCH NORMALIZATION", "BOTH" ]:
      self.model.add( layers.BatchNormalization() ) # normalizes inputs relative to batch such that mean is 0 and stdev is 1
    for i in range( int( self.parameters[ "HIDDEN LAYERS" ] ) ):
      self.model.add( layers.Dense(
        int( self.parameters[ "HIDDEN NODES" ] ),
        kernel_initializer = self.parameters[ "KERNEL INITIALIZER" ],
        kernel_regularizer = None if self.parameters[ "KERNEL REGULARIZER" ] == "NONE" else self.parameters[ "KERNEL REGULARIZER" ],
        kernel_constraint = None if self.parameters[ "KERNEL CONSTRAINT" ] == "NONE" else self.parameters[ "KERNEL CONSTRAINT" ],
        bias_regularizer = None if self.parameters[ "BIAS REGULARIZER" ] == "NONE" else self.parameters[ "BIAS REGULARIZER" ],
        activation = self.parameters[ "ACTIVATION FUNCTION" ],
        activity_regularizer = None if self.parameters[ "ACTIVATION REGULARIZER" ] == "NONE" else self.parameters[ "ACTIVATION REGULARIZER" ] 
      ) )
      if self.parameters[ "TRAINING REGULATOR" ] in [ "DROPOUT", "BOTH" ]:
        self.model.add( layers.Dropout( config.params[ "DROPOUT" ] ) ) # 50% dropout per the original paper by Hinton et. al (2012), remaining weights scaled by 1 / ( 1 - RATE )
      if self.parameters[ "TRAINING REGULATOR" ] in [ "BATCH NORMALIZATION", "BOTH" ]:
        self.model.add( layers.BatchNormalization() )
    self.model.add( layers.Dense(
      1,
      activation = activations.sigmoid,                 # used for single binary classification node
      kernel_initializer = "glorot_uniform", # draws samples from uniform distribution with limits of sqrt( 6 / ( fan_in + fan_out ) ) where fan_in (out) is number of inputs (outputs) 
    ) )
    self.model.compile(
      optimizer = optimizers.Adam( lr = self.parameters["LEARNING RATE"] ),
      loss = "binary_crossentropy",
      metrics = [ "accuracy" ]
    )

    if self.model_name != None:
      self.model.save( self.model_name )

    self.model.summary()

  def train_model( self, variables_train ):
    # Join all signals and backgrounds
    signal_events = self.cut_events[ "TOTAL SIGNAL" ].to_numpy()
    background_events = self.cut_events[ "TOTAL BACKGROUND" ].to_numpy()

    signal_labels = np.full( len( signal_events ), [1] ).astype( "bool" )
    background_labels = np.full( len( background_events ), [0] ).astype( "bool" )

    all_x = self.select_ml_variables( signal_events, background_events, variables_train )
    all_y = np.concatenate( ( signal_labels, background_labels ) )
    del signal_events, background_events

    print( ">> Splitting data." )
    train_x, test_x, train_y, test_y = train_test_split(
      all_x, all_y,
      test_size = config.params[ "TRAIN TEST SPLIT" ]
    )
    del all_x, all_y

    model_checkpoint = ModelCheckpoint(
      self.model_name,
      verbose = 0,
      save_best_only = True,
      save_weights_only = False,
      mode = "auto",
      period = 1
    )

    early_stopping = EarlyStopping(
      monitor = "val_loss",
      patience = self.parameters[ "PATIENCE" ]
    )

    # Train
    print( ">> Training." )
    history = self.model.fit(
      np.array( train_x ), np.array( train_y ),
      epochs = self.parameters[ "EPOCHS" ],
      batch_size = 2**self.parameters[ "BATCH POWER" ],
      shuffle = True,
      verbose = 1,
      callbacks = [ early_stopping, model_checkpoint ],
      validation_split = config.params[ "VALIDATION SPLIT" ]
    )

    # Test
    print( ">> Testing." )
    model_ckp = models.load_model( self.model_name )
    self.loss, self.accuracy = model_ckp.evaluate( test_x, test_y, verbose = 1 )
      
    self.fpr_train, self.tpr_train, _ = roc_curve( train_y.astype(int), model_ckp.predict( train_x )[:,0] )
    self.fpr_test,  self.tpr_test,  _ = roc_curve( test_y.astype(int),  model_ckp.predict( test_x )[:,0] )

    self.auc_train = auc( self.fpr_train, self.tpr_train )
    self.auc_test  = auc( self.fpr_test,  self.tpr_test )
    
    clear_session()

    del train_x, test_x, train_y, test_y, history

class CrossValidationModel( HyperParameterModel ):
  def __init__( self, parameters, signal_paths, background_paths, variables, ratio, model_folder, selection, num_folds = 5, best_metric = "ACC" ):
    HyperParameterModel.__init__( self, parameters, signal_paths, background_paths, variables, ratio, selection, None )
        
    self.model_folder = model_folder
    self.num_folds = num_folds
    self.best_metric = best_metric

    if not os.path.exists( self.model_folder ):
      os.mkdir( self.model_folder )

  def train_model( self ):
    # Set up and store k-way cross validation events
    # Event inclusion masks
    print( ">> Splitting events into {} sets for cross-validation.".format( self.num_folds ) )
    fold_data = {
      "SIGNAL": {},
      "BACKGROUND": {}
    }
    input_data = {
      "TRAIN X": {},
      "TRAIN Y": {},
      "TEST X": {},
      "TEST Y": {}
    }

    signal_split = np.array_split( self.cut_events[ "TOTAL SIGNAL" ].to_numpy(), self.num_folds )
    background_split = np.array_split( self.cut_events[ "TOTAL BACKGROUND" ].to_numpy(), self.num_folds )
    for k in range( self.num_folds ):
      fold_data["SIGNAL"][k] = {
        "TEST":  signal_split[k],
        "TRAIN": np.concatenate( np.delete( signal_split, k, axis = 0 ), axis = 0 )
      }
      fold_data["BACKGROUND"][k] = {
        "TEST":  background_split[k],
        "TRAIN": np.concatenate( np.delete( background_split, k, axis = 0 ), axis = 0 )
      }

      input_data["TRAIN X"][k] = self.select_ml_variables( fold_data["SIGNAL"][k]["TRAIN"], fold_data["BACKGROUND"][k]["TRAIN"], sorted( self.parameters["VARIABLES"] ) )
      input_data["TEST X"][k]  = self.select_ml_variables( fold_data["SIGNAL"][k]["TEST"], fold_data["BACKGROUND"][k]["TEST"], sorted( self.parameters["VARIABLES"] ) )
      input_data["TRAIN Y"][k] = np.concatenate( ( 
          np.full( np.shape( fold_data["SIGNAL"][k]["TRAIN"] )[0], 1 ).astype( "bool" ),
          np.full( np.shape( fold_data["BACKGROUND"][k]["TRAIN"] )[0], 0 ).astype( "bool" )
        ) )
      input_data["TEST Y"][k] = np.concatenate( (
          np.full( np.shape( fold_data["SIGNAL"][k]["TEST"] )[0], 1 ).astype( "bool" ),
          np.full( np.shape( fold_data["BACKGROUND"][k]["TEST"] )[0], 0 ).astype( "bool" )
      ) )

    # Train each fold
    print( "[START] Training {} models".format( self.num_folds ) )
    self.model_paths = []
    self.mean_disc_res = []
    self.weights = []
    self.loss = []
    self.loss_train = {}
    self.loss_validation = {}
    self.accuracy = []
    self.fpr_train = []
    self.fpr_test = []
    self.tpr_train = []
    self.tpr_test = []
    self.auc_train = []
    self.auc_test = []
    self.best_fold = -1

    for k in range( self.num_folds ):
      print(">> Cross Validation Iteration {} of {}".format(k + 1, self.num_folds))  
      clear_session()

      model_name = os.path.join(self.model_folder, "fold_{}.tf".format(k+1))

      self.build_model()

      model_checkpoint = ModelCheckpoint(
        model_name,
        verbose=0,
        save_best_only=True,
        monitor="val_loss",
        save_weights_only=False,
        mode="auto",
        period=1
      )

      early_stopping = EarlyStopping(
        monitor = "val_loss",
        patience = self.parameters[ "PATIENCE" ]
      )

      shuffled_train_x, shuffled_train_y = shuffle_data( input_data["TRAIN X"][k], input_data["TRAIN Y"][k], random_state=0 )
      shuffled_test_x, shuffled_test_y = shuffle_data( input_data["TEST X"][k], input_data["TEST Y"][k], random_state=0 )

      history = self.model.fit(
        shuffled_train_x, shuffled_train_y,
        epochs = self.parameters[ "EPOCHS" ],
        batch_size = 2**self.parameters[ "BATCH POWER" ],
        shuffle = True,
        verbose = 1,
        callbacks = [ early_stopping, model_checkpoint ],
        validation_split = config.params[ "VALIDATION SPLIT" ]
      )

      self.loss_train[k] = history.history[ "loss" ]
      self.loss_validation[k] = history.history[ "val_loss" ] 
      model_ckp = models.load_model(model_name)
      loss, accuracy = model_ckp.evaluate(shuffled_test_x, shuffled_test_y, verbose=1)
         
      predict_train = model_ckp.predict(shuffled_train_x)[:,0]
      predict_test  = model_ckp.predict(shuffled_test_x)[:,0]

      fpr_train, tpr_train, _ = roc_curve( shuffled_train_y.astype(int), predict_train )
      fpr_test, tpr_test, _ = roc_curve( shuffled_test_y.astype(int), predict_test )

      auc_train = auc( fpr_train, tpr_train )
      auc_test  = auc( fpr_test, tpr_test )

      mean_disc_res = abs( np.mean( predict_test ) - 0.5 ) # want the mean to be as far from edges as possible

      print( "[INFO] Statistics from training (k={})".format(k+1) )
      print( "  + Discriminator: {:.3f} pm {:.3f}".format( np.mean( predict_test ), np.std( predict_test ) ) )
      print( "  + Accuracy: {:.3f}".format( accuracy ) )
      print( "  + Loss: {:.5f}".format( loss ) )
      print( "  + AUC: {:.3f}".format( auc_test ) )

      if self.best_metric == "ACC":
        if self.best_fold == -1 or accuracy > max( self.accuracy ):
          if len( self.accuracy ) > 0: print( "[INFO] New best accuracy (k = {} -> {}): {:.3f} {:.3f}".format( self.best_fold, k, max( self.accuracy ), accuracy ) )
          self.best_fold = k
      elif self.best_metric == "LOSS":
        if self.best_fold == -1 or loss < min( self.loss ):
          if len( self.loss ) > 0: print( "[INFO] New best loss (k = {} -> {}): {:.3f} -> {:.3f}".format( self.best_fold, k, min( self.loss ), loss ) )
          self.best_fold = k
      elif self.best_metric == "AUC":
        if self.best_fold == -1 or auc_test > max( self.auc_test ):
          if len( self.auc_test ) > 0: print( "[INFO] New best AUC (k = {} -> {}): {:.3f} -> {:.3f}".format( self.best_fold, k, max( self.auc_test ), auc_test ) )
          self.best_fold = k
      elif self.best_metric == "STABLE":
        if self.best_fold == -1 or mean_disc_res < min( self.mean_disc_res ):
          if len( self.mean_disc_res ) > 0: print( "[INFO] New best mean disc (k = {} -> {}): {:.3f} -> {:.3f}".format( self.best_fold, k, min( self.mean_disc_res ), mean_disc_res ) )          
          else: print( "[INFO] New best mean disc (k = {}): {:.3f}".format( k, mean_disc_res ) )
          self.best_fold = k
 
      if not os.path.exists( self.model_folder ): os.system( "mkdir -vp {}".format( self.model_folder ) )
      model_ckp.save( model_name )
      self.weights.append( model_ckp.get_weights() )

      self.model_paths.append( model_name )
      self.mean_disc_res.append( mean_disc_res )
      self.loss.append( loss )
      self.accuracy.append( accuracy )
      self.fpr_train.append( fpr_train[ 0::int( len(fpr_train) / config.params[ "KFCV" ][ "SAVE AUC POINTS" ] ) ] )
      self.tpr_train.append( tpr_train[ 0::int( len(tpr_train) / config.params[ "KFCV" ][ "SAVE AUC POINTS" ] ) ] )
      self.fpr_test.append( fpr_test[ 0::int( len(fpr_test) / config.params[ "KFCV" ][ "SAVE AUC POINTS" ] ) ] )
      self.tpr_test.append( tpr_test[ 0::int( len(tpr_test) / config.params[ "KFCV" ][ "SAVE AUC POINTS" ] ) ] )
      self.auc_train.append( auc_train )
      self.auc_test.append( auc_test )

    print( "[DONE]" )

  def ensemble_models(self,model_name):
    self.ensemble_weight = []
    for weights_ in zip(*self.weights):
      self.ensemble_weight.append(
        np.array( [ np.array( weight_ ).mean( axis = 0 ) for weight_ in zip(*weights_) ] )
      )
    self.build_model() 
    self.model.set_weights( self.ensemble_weight )
    self.model.save( model_name ) 
