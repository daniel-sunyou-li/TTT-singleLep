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

from ROOT import TFile

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.model_selection import ShuffleSplit
from sklearn.utils import shuffle as shuffle_data

import config

# The parameters to apply to the cut.
CUT_VARIABLES = ["leptonPt_MultiLepCalc", "isElectron", "isMuon",
                 "corr_met_MultiLepCalc", "MT_lepMet", "minDR_lepJet",
                 "DataPastTriggerX", "MCPastTriggerX", "isTraining", "AK4HT",
                 "NJetsCSV_MultiLepCalc", "NJets_JetSubCalc"]

base_cut =  "( %(DataPastTriggerX)s == 1 and %(MCPastTriggerX)s == 1 ) and " + \
            "( %(isTraining)s == 1 or %(isTraining)s == 2 )"

ML_VARIABLES = [ x[0] for x in config.varList[ "DNN" ] ]
VARIABLES = list( sorted( list( set( ML_VARIABLES ).union( set( CUT_VARIABLES ) ) ) ) )
CUT_VARIABLES = [ ( v, VARIABLES.index(v) ) for v in CUT_VARIABLES ]

SAVE_FPR_TPR_POINTS = 20

print(">> mltools.py using {} variables.".format(len(VARIABLES)))

class MLTrainingInstance(object):
  def __init__(self, signal_paths, background_paths, njets, nbjets, ak4ht, lepPt, met, mt, minDR ):
    self.signal_paths = signal_paths
    self.background_paths = background_paths
    self.njets = njets
    self.nbjets = nbjets
    self.ak4ht = ak4ht
    self.met = met
    self.lepPt = lepPt
    self.mt = mt
    self.minDR = minDR
    self.cut = base_cut + \
               " ( (%(leptonPt_MultiLepCalc)s > {} and %(isElectron)s == 1 )".format( lepPt ) + \
               " ( (%(leptonPt_MultiLepCalc)s > {} and %(isMuon)s == 1 ) ) and ".format( lepPt ) + \
               " and ( %(NJetsCSV_MultiLepCalc)s >= {} ) ".format( nbjets ) + \
               " and ( %(NJets_JetSubCalc)s >= {} )".format( njets) + \
               " and ( %(AK4HT)s >= {} )".format( ak4ht ) + \
               " and ( %(corr_met_MultiLepCalc)s > {} )".format( met ) + \
               " and ( %(MT_lepMet)s > {} )".format( mt ) + \
               " and ( %(minDR_lepJet)s > {} )".format( minDR )

  def load_cut_events( self, paths ):
    cut_events_pkl = []
    override = False
    for path in paths:
      with open( path, "rb" ) as f:
        cut_event_pkl = pickle_load( f )
        if cut_event_pkl[ "condition" ] != self.cut:
          print( "[WARN] Event cut in {} is different from cut in varsList.py".format( path ) ) 
          print( ">> Cut events file will be overridden." )
          override = True
        cut_events_pkl.append( cut_event_pkl )

    if override:
      self.load_trees()
      self.apply_cut()
      self.save_cut_events_pkl( paths )
      print( "[OK] New cut events saved." )
    else:
      self.cut_events = {
        "condition": self.cut,
        "signal": cut_events_pkl[0]["signal"],
        "background": cut_events_pkl[0]["background"]
      }
      for cut_event in cut_events_pkl[1:]:
        for event_key in cut_event[ "signal" ].keys():
          self.cut_events[ "signal" ][ event_key ].extend( cut_event[ "signal" ][ event_key ] )
        for event_key in cut_event[ "background" ].keys():
          self.cut_events[ "background" ][ event_key ].extend( cut_event[ "background" ][ event_key ] )

  def save_cut_events( self, paths ):
    config.ratio = 10. # limit background to signal ratio to this
    for i, path in enumerate( paths ):
      event_partition = {
        "condition": self.cut,
        "signal": {},
        "background": {}
      }
      signal_size = 0
      for signal in self.cut_events[ "signal" ]:
        event_partition[ "signal" ][ signal ] = self.cut_events[ "signal" ][ signal ][ i::len( paths ) ] 
        signal_size += len( self.cut_events[ "signal" ][ signal ][ i::len( paths ) ] )

      background_size = 0
      for background in self.cut_events[ "background" ]:
        background_size += len( self.cut_events[ "background" ][ background ][ i::len( paths ) ] )

      sig_to_bkg = float( config.ratio ) * float( signal_size ) / float( background_size )
      for background in self.cut_events[ "background" ]:
        keep_size = int( sig_to_bkg * float( len( self.cut_events[ "background" ][ background ] ) ) )
        event_partition[ "background" ][ background ] = self.cut_events[ "background" ][ background ][:keep_size][ i::len( paths ) ]

      with open( path, "wb" ) as f:
        pickle_dump( event_partition, f )

  def save_cut_events_prq( self, paths ):
    for i, path in enumerate( paths ):
      print( ">> Saving parquet file: {}".format( path ) )
      self.cut_events_prq[i].to_parquet( path )
			
  def load_trees( self ):
    # Load signal files
    self.signal_files = {}
    self.signal_trees = {}
    for path in self.signal_paths:
      self.signal_files[ path ] = TFile.Open( path )
      self.signal_trees[ path ] = self.signal_files[path].Get( "ljmet" )
    # Load background files
    self.background_files = {}
    self.background_trees = {}
    for path in self.background_paths:
      self.background_files[ path ] = TFile.Open( path )
      self.background_trees[ path ] = self.background_files[ path ].Get( "ljmet" )
   
  def apply_cut( self ):
    # Apply cut parameters to the loaded signals and backgrounds
    # Load in events
    test_cut = lambda d: eval( self.cut % d )
    all_signals = {}
    for path, signal_tree in self.signal_trees.iteritems():
      print( "  >> Applying cuts to {}...".format( path.split("/")[-1] ) )
      sig_list = np.asarray( signal_tree.AsMatrix( VARIABLES ) )
      if path in all_signals:
        all_signals[path] = np.concatenate( ( all_signals[path], sig_list ) )
      else:
        all_signals[path] = sig_list
    print( "[OK] Signal cuts are complete" )
    all_backgrounds = {}
    for path, background_tree in self.background_trees.iteritems():
      print( "  >> Applying cuts to {}...".format( path.split("/")[-1] ) )
      bkg_list = np.asarray( background_tree.AsMatrix( VARIABLES ) )
      if path in all_backgrounds:
        all_backgrounds[ path ] = np.concatenate( ( all_backgrounds[path], bkg_list ) )
      else:
        all_backgrounds[ path ] = bkg_list
    print( "[OK] Background cuts are complete" )
    # Apply cuts
    self.cut_events = {
      "condition": self.cut,
      "signal": {},
      "background": {}
    }
    n_s = 0
    c_s = 0
    for path, events in all_signals.iteritems():
      self.cut_events[ "signal" ][ path ] = []
      n_s += len( events )
      for event in events:
        if test_cut( { var: event[i] for var, i in CUT_VARIABLES } ):
          self.cut_events[ "signal" ][ path ].append( event )
          c_s += 1
    n_b = 0
    c_b = 0
    for path, events in all_backgrounds.iteritems():
      self.cut_events[ "background" ][ path ] = []
      n_b += len( events )
      for event in events:
        if test_cut( { var: event[i] for var, i in CUT_VARIABLES } ):
          self.cut_events[ "background" ][ path ].append( event )
          c_b += 1

    print(">> Signal {}/{}, Background {}/{}".format(c_s, n_s, c_b, n_b))

  def apply_cut_prq( self, save_paths ):
    test_cut = lambda d: eval( self.cut % d )
    all_signals = {}
    for path, signal_tree in self.signal_trees.iteritems():
      print( ">> Converting {} from ROOT to Numpy Format".format( path ) )
      sig_list = np.asarray( signal_tree.AsMatrix( VARIABLES ) )
      if path in all_signals:
        all_signals[path] = np.concatenate( ( all_signals[path], sig_list ) )
      else:
        all_signals[path] = sig_list
    all_backgrounds = {}
    for path, background_tree in self.background_trees.iteritems():
      print( ">> Converting {} from ROOT to Numpy Format".format( path ) )
      bkg_list = np.asarray( background_tree.AsMatrix( VARIABLES ) )
      if path in all_backgrounds:
        all_backgrounds[ path ] = np.concatenate( ( all_backgrounds[path], bkg_list ) )
      else:
        all_backgrounds[ path ] = bkg_list
				
    all_events = []
    n_s = 0
    c_s = 0
    print( ">> Applying cuts to signal" )
    for path, events in all_signals.iteritems():
      print( "  o Cutting {}".format( path ) )
      n_s += len( events )
      for event in events:
        if test_cut( { var: event[i] for var, i in CUT_VARIABLES } ):
          all_events.append( np.append( event, 1 ) )
          c_s += 1
    n_b = 0
    c_b = 0
    print( ">> Applying cuts to background" )
    for path, events in all_backgrounds.iteritems():
      n_b += len( events )
      print( "  o Cutting {}".format( path ) )
      for event in events:
        if test_cut( { var: event[i] for var, i in CUT_VARIABLES } ):
          all_events.append( np.append( event, 0 ) )
          c_b += 1

    self.cut_events_prq = []
    for i, path in enumerate( save_paths ):
      print( ">> Transferring Numpy events to Pandas Dataframe ({} out of {})".format(i+1,len(save_paths)) )
      self.cut_events_prq.append( pd.DataFrame( all_events[i::len(save_paths)], columns = [ variable for variable in VARIABLES ] + [ "type" ] ) )
                
  def build_model(self):
    # Override with the code that builds the Keras model.
    pass

  def train_model_pkl(self):
    # Train the model on the singal and background data formatted with pickle
    pass        
	
  def train_model_prq(self):
    # train the model on the signal and background data formatted with parquet
    pass

class HyperParameterModel(MLTrainingInstance):
  def __init__(self, parameters, signal_paths, background_paths, njets, nbjets, ak4ht, model_name=None):
    MLTrainingInstance.__init__(self, signal_paths, background_paths, njets, nbjets, ak4ht)
    self.parameters = parameters
    self.model_name = model_name

  def select_ml_variables(self, sig_events, bkg_events, varlist):
    # Select which variables from ML_VARIABLES to use in training
    events = []
    positions = {v: VARIABLES.index(v) for v in varlist}
    for e in sig_events:
      events.append([e[positions[v]] for v in varlist])
    for e in bkg_events:
      events.append([e[positions[v]] for v in varlist])
    return events

  def build_model(self, input_size="auto"):
    self.model = Sequential()
    self.model.add( Dense(
      self.parameters[ "initial_nodes" ],
      input_dim=len(self.parameters["variables"]) if input_size == "auto" else input_size,
      kernel_initializer = "he_normal",
      activation=self.parameters[ "activation_function" ]
    ) )
    partition = int( self.parameters[ "initial_nodes" ] / self.parameters[ "hidden_layers" ] )
    for i in range( self.parameters[ "hidden_layers" ] ):
      self.model.add( BatchNormalization() )
      if self.parameters[ "regulator" ] in [ "dropout", "both" ]:
        self.model.add( Dropout( 0.2 ) )
      if self.parameters[ "node_pattern" ] == "dynamic":
        self.model.add( Dense(
          self.parameters[ "initial_nodes" ] - ( partition * i ),
          kernel_initializer = "he_normal",
          activation=self.parameters[ "activation_function" ]
        ) )
      elif self.parameters[ "node_pattern" ] == "static":
	self.model.add( Dense(
          self.parameters[ "initial_nodes" ],
          kernel_initializer = "he_normal",
          activation=self.parameters[ "activation_function" ]
        ) )
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
      #tf.keras.experimental.export_saved_model( self.model, self.model_name )
      self.model.save( self.model_name )

    self.model.summary()

  def train_model_pkl( self ):
    # Join all signals and backgrounds
    signal_events = []
    for events in self.cut_events[ "signal" ].values():
      for event in events:
        signal_events.append( event )
    background_events = []
    for events in self.cut_events[ "background" ].values():
      for event in events:
        background_events.append( event )
        
    signal_labels = np.full( len( signal_events ), [1] ).astype( "bool" )
    background_labels = np.full( len( background_events ), [0] ).astype( "bool" )

    all_x = np.array( self.select_ml_variables( signal_events, background_events, self.parameters[ "variables" ] ) )
    all_y = np.concatenate( ( signal_labels, background_labels ) )

    print( ">> Splitting data." )
    train_x, test_x, train_y, test_y = train_test_split(
      all_x, all_y,
      test_size = 0.2
    )

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

  def train_model_prq( self ):
    # Join all signals and backgrounds
    cut_events = pd.concat( [ cut_event for cut_event in self.cut_events_prq ] )
    signal_events = []
    background_events = []
    for i in range( len( cut_events.index ) ):
      if cut_events.iloc[i]["type"] == 1.0: signal_events.append( cut_events.iloc[i].values[:-1] )
      else: background_events.append( cut_events.iloc[i].values[:-1] )
        
    signal_labels = np.full( len( signal_events ), [1] ).astype( "bool" )
    background_labels = np.full( len( background_events ), [0] ).astype( "bool" )

    all_x = np.array( self.select_ml_variables( signal_events, background_events, self.parameters[ "variables" ] ) )
    all_y = np.concatenate( ( signal_labels, background_labels ) )

    print( ">> Splitting data." )
    train_x, test_x, train_y, test_y = train_test_split(
      all_x, all_y,
      test_size = 0.2
    )

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
    
class CrossValidationModel( HyperParameterModel ):
  def __init__( self, parameters, signal_paths, background_paths, model_folder, njets, nbjets, ak4ht, num_folds = 5 ):
    HyperParameterModel.__init__( self, parameters, signal_paths, background_paths, njets, nbjets, ak4ht, None )
        
    self.model_folder = model_folder
    self.num_folds = num_folds

    if not os.path.exists( self.model_folder ):
      os.mkdir( self.model_folder )

  def train_model_pkl( self ):
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
        self.cut_events["background"][path][fold_mask["background"][path][k]["train"]] for path in self.cut_events["background"]
      ])
      bkg_test_k = np.concatenate([
        self.cut_events["background"][path][fold_mask["background"][path][k]["test"]] for path in self.cut_events["background"]
      ])
            
      fold_data.append( {
        "train_x": np.array( self.select_ml_variables(
          sig_train_k, bkg_train_k, self.parameters[ "variables" ] ) ),
        "test_x": np.array( self.select_ml_variables(
          sig_test_k, bkg_test_k, self.parameters[ "variables" ] ) ),

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
	
  def train_model_prq( self ):
    shuffle = ShuffleSplit( n_splits = self.num_folds, test_size = float( 1.0 / self.num_folds ), random_state = 0 )

    # Set up and store k-way cross validation events
    # Event inclusion masks
    print( ">> Splitting events into {} sets for cross-validation.".format( self.num_folds ) )
    cut_events = pd.concat( [ cut_event for cut_event in self.cut_events_prq ] ) 

    signal_events = []
    background_events = []
    fold_mask = {
      "signal": {},
      "background": {}
    }
    n_events = len( cut_events.index ) 
    print( "Total number of events: {}".format( n_events ) )
    checkpoints = np.rint( np.linspace( 0, n_events, 21 ) )	
    for i in range( n_events ):
      if i in checkpoints: 
        print( ">> Event {}: {:.2f}% events loaded...".format( i, 100.*(float(i)/float(n_events)) ) )
      if cut_events.iloc[i]["type"] == 1.0: signal_events.append( cut_events.iloc[i].values[:-1] )
      else: background_events.append( cut_events.iloc[i].values[:-1] )
        
    print( "[OK ] Finished loading events from parquet, splitting into {} folds".format( self.num_folds ) )
    k = 0
    for train, test in shuffle.split(signal_events):
      fold_mask["signal"][k] = {
        "train": train,
        "test": test
      }
      k += 1
    
    print( "[OK ] Signal events split into {} folds.".format( self.num_folds ) )
    k = 0
    for train, test in shuffle.split(background_events):
      fold_mask["background"][k] = {
        "train": train,
        "test": test
      }
      k += 1
    print( "[OK ] Background events split into {} folds...".format( self.num_folds ) )

    print( ">> Formatting events into trainable format..." )
    # Event lists
    fold_data = []
    for k in range(self.num_folds):
      print( ">> Formatting fold {}...".format( k ) )
      sig_train_k = np.array( signal_events )[ fold_mask["signal"][k]["train"] ]
      sig_test_k  = np.array( signal_events )[ fold_mask["signal"][k]["test"]  ]
      bkg_train_k = np.array( background_events )[ fold_mask["background"][k]["train"] ]
      bkg_test_k  = np.array( background_events )[ fold_mask["background"][k]["test"] ]
            
      fold_data.append( {
        "train_x": np.array( self.select_ml_variables(
          sig_train_k, bkg_train_k, self.parameters[ "variables" ] ) ),
        "test_x": np.array( self.select_ml_variables(
          sig_test_k, bkg_test_k, self.parameters[ "variables" ] ) ),

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
