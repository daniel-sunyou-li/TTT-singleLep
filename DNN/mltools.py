import os, sys
import numpy as np
from pickle import load as pickle_load
from pickle import dump as pickle_dump

os.environ["KERAS_BACKEND"] = "tensorflow"

from keras.models import Sequential
from keras.models import load_model
from keras.layers.core import Dense, Dropout
from keras.layers import BatchNormalization
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.backend import clear_session

import ROOT

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

base_cut =  "( %(DataPastTriggerX)s == 1 and %(MCPastTriggerX)s == 1 ) and " + \
            "( %(isTraining)s == 1 )"

ML_VARIABLES = [ x[0] for x in config.varList[ "DNN" ] ]
VARIABLES = list( sorted( list( set( ML_VARIABLES ).union( set( CUT_VARIABLES ) ).union( set( CUT_VARIABLES ) ) ) ) )
CUT_VARIABLES = [ ( v, VARIABLES.index(v) ) for v in CUT_VARIABLES ]

SAVE_FPR_TPR_POINTS = 20

print(">> mltools.py using {} variables.".format(len(VARIABLES)))

class MLTrainingInstance(object):
  def __init__(self, signal_paths, background_paths, ratio, njets, nbjets, ak4ht, lepPt, met, mt, minDR ):
    self.signal_paths = signal_paths
    self.background_paths = background_paths
    self.samples = signal_paths + background_paths
    self.ratio = ratio
    self.njets = njets
    self.nbjets = nbjets
    self.ak4ht = ak4ht
    self.met = met
    self.lepPt = lepPt
    self.mt = mt
    self.minDR = minDR
    self.cut = base_cut + \
               " and ( (%(leptonPt_MultiLepCalc)s > {} and %(isElectron)s == 1 )".format( lepPt ) + \
               " or (%(leptonPt_MultiLepCalc)s > {} and %(isMuon)s == 1 ) )".format( lepPt ) + \
               " and ( %(NJetsCSV_JetSubCalc)s >= {} ) ".format( nbjets ) + \
               " and ( %(NJets_JetSubCalc)s >= {} )".format( njets) + \
               " and ( %(AK4HT)s >= {} )".format( ak4ht ) + \
               " and ( %(corr_met_MultiLepCalc)s > {} )".format( met ) + \
               " and ( %(MT_lepMet)s > {} )".format( mt ) + \
               " and ( %(minDR_lepJet)s > {} )".format( minDR )

  def load_cut_events( self, paths ):
    cut_events_pkl = []
    override = False
    for path in paths:
      print( "  - {}".format( path ) )
      with open( path, "rb" ) as f:
        cut_event_pkl = pickle_load( f )
        if cut_event_pkl[ "condition" ] != self.cut:
          print( "[WARN] Event cut in {} is different from cut used existing pickle file...".format( path ) ) 
          print( ">> Cut events file will be overridden." )
          override = True
        if set( cut_event_pkl[ "samples" ] ) != set( self.samples ):
          print( "[WARN] Samples used in {} is different from samples used in existing pickle file...".format( path ) )
          print( ">> Cut events file will be overridden." )
          override = True
        if cut_event_pkl[ "ratio" ] != self.ratio:
          print( "[WARN] Ratio used in {} is different from ratio used in existing pickle file...".format( path ) )
          print( ">> Cut events file will be overridden." )
          override = True
        cut_events_pkl.append( cut_event_pkl )
        del cut_event_pkl

    if override:
      self.apply_cut()
      self.save_cut_events( paths )
      print( "[OK] New cut events saved." )
    else:
      self.cut_events = {
        "condition": self.cut,
        "ratio": self.ratio,
        "samples": self.samples,                                                                     
        "signal": cut_events_pkl[0]["signal"].copy(),
        "background": cut_events_pkl[0]["background"].copy()
      }
      c_s, c_b = 0, 0
      for event_key in self.cut_events["signal"].keys(): 
        #self.cut_events["signal"][event_key] = self.cut_events["signal"][event_key]
        c_s += len( self.cut_events["signal"][event_key] )
      for event_key in self.cut_events["background"].keys():
        self.cut_events["background"][event_key] = self.cut_events["background"][event_key]
        c_b += len( self.cut_events["background"][event_key] )

      del cut_events_pkl[0]
      while len( cut_events_pkl ) > 0:
        while len( cut_events_pkl[0][ "signal" ].keys() ) > 0:     
          event_key = cut_events_pkl[0][ "signal" ].keys()[0]
          self.cut_events[ "signal" ][ event_key  ].extend( cut_events_pkl[0][ "signal" ][ event_key ] )
          c_s += len( cut_events_pkl[0][ "signal" ][ event_key ] )
          del cut_events_pkl[0][ "signal" ][ event_key ]
        while len( cut_events_pkl[0][ "background" ].keys() ) > 0:
          event_key = cut_events_pkl[0][ "background" ].keys()[0]
          self.cut_events[ "background" ][ event_key ].extend( cut_events_pkl[0][ "background" ][ event_key ] )
          c_b += len( cut_events_pkl[0][ "background" ][ event_key ] )
          del cut_events_pkl[0][ "background" ][ event_key ]
        del cut_events_pkl[0]
      print( "[OK] Found {} signal events and {} background events...".format( c_s, c_b ) )

  def save_cut_events( self, paths ):
    for i, path in enumerate( paths ):
      event_partition = {
        "condition": self.cut,
        "ratio": self.ratio,
        "samples": self.samples,
        "signal": {},
        "background": {}
      }
    
      for signal in self.cut_events[ "signal" ]:
        event_partition[ "signal" ][ signal ] = self.cut_events[ "signal" ][ signal ][ i::len( paths ) ]
      for background in self.cut_events[ "background" ]:
        event_partition[ "background" ][ background ] = self.cut_events[ "background" ][ background ][ i::len( paths ) ]
      
      with open( path, "wb" ) as f: pickle_dump( event_partition, f )

  def apply_cut( self ): # applies cuts to events as well as computing the event weight from the cut events to set relative proportion of events
    ROOT.gInterpreter.Declare("""
    float compute_weight( float triggerXSF, float pileupWeight, float lepIdSF, float isoSF, float L1NonPrefiringProb_CommonCalc, float MCWeight_MultiLepCalc, float xsecEff, float tthfWeight, float btagDeepJetWeight, float btagDeepJet2DWeight_HTnj ){
      return triggerXSF * pileupWeight * lepIdSF * isoSF * L1NonPrefiringProb_CommonCalc * ( MCWeight_MultiLepCalc / abs( MCWeight_MultiLepCalc ) ) * xsecEff * tthfWeight * btagDeepJetWeight * btagDeepJet2DWeight_HTnj;
    }
    """)
    weights = {}
    factors = {}
    all_signals = {}
    n_s, c_s, w_s = 0, 0, 0
    for path in self.signal_paths:
      print( "   >> Applying cuts to {}...".format( path.split("/")[-1] ) )
      df = ROOT.RDataFrame( "ljmet", path )
      df_count = df.Count().GetValue()
      n_s += df_count
      df_1 = df.Filter( "isTraining == 1" ).Filter( "DataPastTriggerX == 1 && MCPastTriggerX == 1" ).Filter( "isElectron == 1 || isMuon == 1" )
      df_2 = df_1.Filter( "leptonPt_MultiLepCalc > {} && NJetsCSV_JetSubCalc >= {} && NJets_JetSubCalc >= {}".format( self.lepPt, self.nbjets, self.njets ) )
      df_3 = df_2.Filter( "AK4HT > {} && corr_met_MultiLepCalc > {} && MT_lepMet > {} && minDR_lepJet > {}".format( self.ak4ht, self.met, self.mt, self.minDR ) )
      df3_count = df_3.Count().GetValue()
      sig_dict = df_3.AsNumpy( columns = VARIABLES )
      df_weight = df_3.Define( "weight", "compute_weight( triggerXSF, pileupWeight, lepIdSF, isoSF, L1NonPrefiringProb_CommonCalc, MCWeight_MultiLepCalc, xsecEff, tthfWeight, btagDeepJetWeight, btagDeepJet2DWeight_HTnj )" )
      del df, df_1, df_2, df_3
      weights[ path ] = df_weight.Sum( "weight" ).GetValue()
      factors[ path ] = float( df3_count ) / weights[ path ] 
      sig_list = []
      for x, y in sig_dict.items(): sig_list.append(y)
      if path in all_signals:
        all_signals[path] = np.concatenate( ( all_signals[path], np.array( sig_list ).transpose() ) )
      else:
        all_signals[path] = np.array( sig_list ).transpose()
      print( "     - {}/{} events passed, event weight = {:.2f}".format( df3_count, df_count, weights[path] ) )
      c_s += df3_count
      w_s += weights[ path ]
      del df_weight, sig_list      

    all_backgrounds = {}
    n_b, c_b, w_b = 0, 0, 0
    min_factor = 1e10
    for path in self.background_paths:
      print( "   >> Applying cuts to {}...".format( path.split("/")[-1] ) )
      df = ROOT.RDataFrame( "ljmet", path )
      df_count = df.Count().GetValue()
      n_b += df_count
      df_1 = df.Filter( "isTraining == 1" ).Filter( "DataPastTriggerX == 1 && MCPastTriggerX == 1" ).Filter( "isElectron == 1 || isMuon == 1" )
      df_2 = df_1.Filter( "leptonPt_MultiLepCalc > {} && NJetsCSV_JetSubCalc >= {} && NJets_JetSubCalc >= {}".format( self.lepPt, self.nbjets, self.njets ) )
      df_3 = df_2.Filter( "AK4HT > {} && corr_met_MultiLepCalc > {} && MT_lepMet > {} && minDR_lepJet > {}".format( self.ak4ht, self.met, self.mt, self.minDR ) )
      df3_count = df_3.Count().GetValue()
      df_weight = df_3.Define( "weight", "compute_weight( triggerXSF, pileupWeight, lepIdSF, isoSF, L1NonPrefiringProb_CommonCalc, MCWeight_MultiLepCalc, xsecEff, tthfWeight, btagDeepJetWeight, btagDeepJet2DWeight_HTnj )" )
      weights[ path ] = df_weight.Sum( "weight" ).GetValue()
      factors[ path ] = df3_count / weights[ path ]
      if factors[ path ] < min_factor: min_factor = factors[ path ]
      bkg_dict = df_3.AsNumpy( columns = VARIABLES )
      del df, df_1, df_2, df_3
      bkg_list = []
      for x, y in bkg_dict.items(): bkg_list.append(y)
      if path in all_backgrounds:
        all_backgrounds[path] = np.concatenate( ( all_backgrounds[path], np.array( bkg_list ).tranpose() ) )
      else:
        all_backgrounds[path] = np.array( bkg_list ).transpose()
      print( "     - {}/{} events passed, event weight = {:.2f}".format( df3_count, df_count, weights[ path ] ) )
      c_b += df3_count
      w_b += weights[ path ]
      del df_weight, bkg_list

    self.cut_events = {
      "condition": self.cut,
      "ratio": self.ratio,
      "samples": self.samples,
      "signal": {},
      "background": {}
    }

    for path, events in all_signals.iteritems(): 
      self.cut_events[ "signal" ][ path ] = events.tolist()
      #self.cut_events[ "signal" ][ path ] = []
      #for event in events: self.cut_events[ "signal" ][ path ].append( np.append( event, 1 ) )
    del all_signals
    for path, events in all_backgrounds.iteritems():
      self.cut_events[ "background" ][ path ] = events
      #self.cut_events[ "background" ][ path ] = []
      #for event in events: self.cut_events[ "background" ][ path ].append( np.append( event, 0 ) )
    del all_backgrounds
   
    r_b = 0
    for path in self.cut_events[ "background" ]:
      max_path = self.ratio * float( c_s ) * ( weights[ path ] / float( w_b ) )
      rel_path = min_factor * weights[ path ]
      nEvents_bkg = max_path if self.ratio > 0 else rel_path
      bkg_incl = int( nEvents_bkg ) if nEvents_bkg <= len( self.cut_events[ "background" ][ path ] ) else len( self.cut_events[ "background" ][ path ] )
      bkg_excl = int( len( self.cut_events[ "background" ][ path ] ) - bkg_incl )
      mask = np.concatenate( ( np.full( bkg_incl, 1 ), np.full( bkg_excl, 0 ) ) )
      np.random.shuffle( mask )
      self.cut_events[ "background" ][ path ] = np.array( self.cut_events[ "background" ][ path ] )[ mask.astype(bool) ].tolist()
      r_b += bkg_incl

    print( ">> Signal: {}/{}, Weighted: {:.0f}".format( c_s, n_s, w_s ) )
    print( ">> Background: Passed = {}/{}, Weighted = {:.0f}, Training = {}".format( c_b, n_b, w_b, r_b ) )
    print( "  - Minimum Factor: {:.2f}".format( min_factor ) )

  def build_model(self):
    # Override with the code that builds the Keras model.
    pass

  def train_model(self):
    # Train the model on the singal and background data formatted with pickle
    pass        
	
class HyperParameterModel(MLTrainingInstance):
  def __init__(self, parameters, signal_paths, background_paths, ratio, njets, nbjets, ak4ht, lepPt, met, mt, minDR, model_name=None):
    MLTrainingInstance.__init__(self, signal_paths, background_paths, ratio, njets, nbjets, ak4ht, lepPt, met, mt, minDR)
    self.parameters = parameters
    self.model_name = model_name

  def select_ml_variables(self, sig_events, bkg_events, varlist):
    # Select which variables from ML_VARIABLES to use in training
    positions = { v: VARIABLES.index(v) for v in varlist }
    var_mask = [ positions[v] for v in positions ]
    return np.concatenate( ( np.array( sig_events )[:, var_mask], np.array( bkg_events )[:, var_mask] ) )

  def build_model(self, input_size="auto"):
    self.model = Sequential()
    self.model.add( Dense(
      self.parameters[ "initial_nodes" ],
      input_dim=len(self.parameters["variables"]) if input_size == "auto" else input_size,
      kernel_initializer = "he_normal",
      #kernel_initializer = "glorot_uniform",
      kernel_regularizer="l2",
      activation=self.parameters[ "activation_function" ]
    ) )
    self.model.add( BatchNormalization() )
    partition = int( self.parameters[ "initial_nodes" ] / self.parameters[ "hidden_layers" ] )
    for i in range( self.parameters[ "hidden_layers" ] ):
      if self.parameters[ "regulator" ] in [ "dropout", "both" ]:
        self.model.add( Dropout( 0.3 ) )
      if self.parameters[ "node_pattern" ] == "dynamic":
        self.model.add( Dense(
          self.parameters[ "initial_nodes" ] - ( partition * i ),
          kernel_initializer = "he_normal",
          #kernel_initializer = "glorot_uniform",
          kernel_regularizer = "l2",
          activation=self.parameters[ "activation_function" ]
        ) )
      elif self.parameters[ "node_pattern" ] == "static":
	self.model.add( Dense(
          self.parameters[ "initial_nodes" ],
          kernel_initializer = "he_normal",
          #kernel_initializer = "glorot_uniform",
          kernel_regularizer = "l2",
          activation=self.parameters[ "activation_function" ]
        ) )
      self.model.add( BatchNormalization() )
      # Final classification node
    self.model.add( Dense(
      1,
      activation = "sigmoid"
    ) )
    self.model.compile(
      optimizer = Adam( lr = self.parameters["learning_rate"] ),
      loss = "binary_crossentropy",
      metrics=[ "accuracy" ]
    )

    if self.model_name != None:
      self.model.save( self.model_name )

    self.model.summary()

  def train_model( self ):
    # Join all signals and backgrounds
    signal_events = []
    for path in self.cut_events[ "signal" ]:
      signal_events += self.cut_events[ "signal" ][ path ]
    
    background_events = []
    for path in self.cut_events[ "background" ]:
      background_events += self.cut_events[ "background" ][ path ]

    signal_labels = np.full( len( signal_events ), [1] ).astype( "bool" )
    background_labels = np.full( len( background_events ), [0] ).astype( "bool" )

    all_x = self.select_ml_variables( signal_events, background_events, self.parameters[ "variables" ] )
    del signal_events, background_events
    all_y = np.concatenate( ( signal_labels, background_labels ) )

    print( ">> Splitting data." )
    train_x, test_x, train_y, test_y = train_test_split(
      all_x, all_y,
      test_size = 0.2
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
      patience=self.parameters[ "patience" ]
    )

    # Train
    print( ">> Training." )
    history = self.model.fit(
      np.array( train_x ), np.array( train_y ),
      epochs = self.parameters[ "epochs" ],
      batch_size = 2**self.parameters[ "batch_power" ],
      shuffle = True,
      verbose = 1,
      callbacks = [ early_stopping, model_checkpoint ],
      validation_split = 0.25
    )

    # Test
    print( ">> Testing." )
    model_ckp = load_model( self.model_name )
    self.loss, self.accuracy = model_ckp.evaluate( test_x, test_y, verbose = 1 )
      
    self.fpr_train, self.tpr_train, _ = roc_curve( train_y.astype(int), model_ckp.predict( train_x )[:,0] )
    self.fpr_test,  self.tpr_test,  _ = roc_curve( test_y.astype(int),  model_ckp.predict( test_x )[:,0] )

    self.auc_train = auc( self.fpr_train, self.tpr_train )
    self.auc_test  = auc( self.fpr_test,  self.tpr_test )

    del train_x, test_x, train_y, test_y, history

class CrossValidationModel( HyperParameterModel ):
  def __init__( self, parameters, signal_paths, background_paths, ratio, model_folder, njets, nbjets, ak4ht, lepPt, met, mt, minDR, num_folds = 5 ):
    HyperParameterModel.__init__( self, parameters, signal_paths, background_paths, ratio, njets, nbjets, ak4ht, lepPt, met, mt, minDR, None )
        
    self.model_folder = model_folder
    self.num_folds = num_folds

    if not os.path.exists( self.model_folder ):
      os.mkdir( self.model_folder )

  def train_model( self ):
    shuffle = ShuffleSplit( n_splits = self.num_folds, test_size = float( 1.0 / self.num_folds ), random_state = 0 )

    # Set up and store k-way cross validation events
    # Event inclusion masks
    print( ">> Splitting events into {} sets for cross-validation.".format( self.num_folds ) )
    fold_mask = {
      "signal": {},
      "background": {}
    }

    for path, events in self.cut_events[ "signal" ].iteritems():
      self.cut_events[ "signal" ][path] = np.array(events)

    for path, events in self.cut_events["background"].iteritems():
      self.cut_events["background"][path] = np.array(events)
        
    for path, events in self.cut_events["signal"].iteritems():
      k = 0
      fold_mask["signal"][path] = {}
      for train, test in shuffle.split(events):
        fold_mask["signal"][path][k] = {
          "train": train,
          "test": test
         }
        k += 1

    for path, events in self.cut_events["background"].iteritems():
      k = 0
      fold_mask["background"][path] = {}
      for train, test in shuffle.split(events):
        fold_mask["background"][path][k] = {
          "train": train,
          "test": test
        }
        k += 1

    # Event lists
    fold_data = []
    for k in range(self.num_folds):
      sig_train_k = np.concatenate([
        self.cut_events["signal"][path][fold_mask["signal"][path][k]["train"]] for path in self.cut_events["signal"]
      ])
      sig_test_k = np.concatenate([
        self.cut_events["signal"][path][fold_mask["signal"][path][k]["test"]] for path in self.cut_events["signal"]
      ])
      bkg_train_k = np.concatenate([
        self.cut_events["background"][path][fold_mask["background"][path][k]["train"]] for path in self.cut_events["background"] if len( self.cut_events["background"][path][fold_mask["background"][path][k]["train"]] ) > self.num_folds
      ])
      bkg_test_k = np.concatenate([
        self.cut_events["background"][path][fold_mask["background"][path][k]["test"]] for path in self.cut_events["background"] if len( self.cut_events["background"][path][fold_mask["background"][path][k]["test"]] ) > self.num_folds
      ])
            
      fold_data.append( {
        "train_x": self.select_ml_variables(
          sig_train_k, bkg_train_k, self.parameters[ "variables" ] ),
        "test_x": self.select_ml_variables(
          sig_test_k, bkg_test_k, self.parameters[ "variables" ] ),

        "train_y": np.concatenate( (
          np.full( np.shape( sig_train_k )[0], 1 ).astype( "bool" ),
          np.full( np.shape( bkg_train_k )[0], 0 ).astype( "bool" ) ) ),
        "test_y": np.concatenate( (
          np.full( np.shape( sig_test_k )[0], 1 ).astype( "bool" ),
          np.full( np.shape( bkg_test_k )[0], 0 ).astype( "bool" ) ) ) 
      } )

    # Train each fold
    print( ">> Beginning Training and Evaluation." )
    self.model_paths = []
    self.loss = []
    self.accuracy = []
    self.fpr_train = []
    self.fpr_test = []
    self.tpr_train = []
    self.tpr_test = []
    self.auc_train = []
    self.auc_test = []
    self.best_fold = -1

    for k, events in enumerate(fold_data):
      print("CV Iteration {} of {}".format(k + 1, self.num_folds))  
      clear_session()

      model_name = os.path.join(self.model_folder, "fold_{}.tf".format(k))

      self.build_model(events["train_x"].shape[1])

      model_checkpoint = ModelCheckpoint(
        model_name,
        verbose=0,
        save_best_only=True,
        save_weights_only=False,
        mode="auto",
        period=1
      )

      early_stopping = EarlyStopping(
        monitor = "val_loss",
        patience=self.parameters[ "patience" ]
      )

      shuffled_x, shuffled_y = shuffle_data( events[ "train_x" ], events[ "train_y" ], random_state=0 )
      shuffled_test_x, shuffled_test_y = shuffle_data( events[ "test_x" ], events[ "test_y" ], random_state=0 )

      history = self.model.fit(
        shuffled_x, shuffled_y,
        epochs = self.parameters[ "epochs" ],
        batch_size = 2**self.parameters[ "batch_power" ],
        shuffle = True,
        verbose = 1,
        callbacks = [ early_stopping, model_checkpoint ],
        validation_split = 0.25
      )

      model_ckp = load_model(model_name)
      loss, accuracy = model_ckp.evaluate(shuffled_test_x, shuffled_test_y, verbose=1)
         
      fpr_train, tpr_train, _ = roc_curve( shuffled_y.astype(int), model_ckp.predict(shuffled_x)[:,0] )
      fpr_test, tpr_test, _ = roc_curve( shuffled_test_y.astype(int), model_ckp.predict(shuffled_test_x)[:,0] )

      auc_train = auc( fpr_train, tpr_train )
      auc_test  = auc( fpr_test, tpr_test )

      if self.best_fold == -1 or auc_test > max(self.auc_test):
        self.best_fold = k

      self.model_paths.append( model_name )
      self.loss.append( loss )
      self.accuracy.append( accuracy )
      self.fpr_train.append( fpr_train[ 0::int( len(fpr_train) / SAVE_FPR_TPR_POINTS ) ] )
      self.tpr_train.append( tpr_train[ 0::int( len(tpr_train) / SAVE_FPR_TPR_POINTS ) ] )
      self.fpr_test.append( fpr_test[ 0::int( len(fpr_test) / SAVE_FPR_TPR_POINTS ) ] )
      self.tpr_test.append( tpr_test[ 0::int( len(tpr_test) / SAVE_FPR_TPR_POINTS ) ] )
      self.auc_train.append( auc_train )
      self.auc_test.append( auc_test )

    print( "[OK ] Finished." )
