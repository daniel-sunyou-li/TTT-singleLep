# methods and classes used for constructing the ABCDnn module

import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
import tensorflow_probability as tfp
from tensorflow.keras.optimizers.schedules import LearningRateSchedule
import numpy as np

def invsigmoid( x ):
# inverse sigmoid function for transformer
  xclip = tf.clip_by_value( x, 1e-6, 1.0 - 1e-6 )
  return tf.math.log( xclip, / ( 1.0 - xclip ) )

def NAF( inputdim, conddim, activation, regularizer, nodes_cond, hidden_cond, nodes_trans, depth, permute ):
# neural autoregressive flow is a chain of MLP networks used for the conditioner and transformer parts of the flow
  activation_key = { # edit this if you add options to config.hyper dict with more activation functions
    "swish": tf.nn.swish,
    "softplus": tf.nn.softplus,
    "relu": tf.nn.relu,
    "elu": tf.nn.elu
  }
  regularizer_key = { 
    "L1": tf.keras.regularizers.L1,
    "L2": tf.keras.regluarizers.L2,
    "L1+L2": tf.keras.regularizers.L1L2,
    "None": None
  }
  
  xin = layers.Input( shape = ( inputdim + conddim, ), name = "INPUT_LAYER" )
  xcondin = xin[ :, inputdim: ]
  xfeatures = xin[ :, :inputdim ]
  nextfeature = xfeatures
  
  for idepth in range( depth ):
    if permute: # mix up the input order of the consecutive neural networks in the flow
      randperm = np.random.permutation( inputdim ).astype( "int32" )
      permutation = tf.constant( randperm )
    else:
      permutation = tf.range( inputdim, dtype = "int32" )
    permuter = tfp.bijectors.Permute( permutation = permutation )
    xfeatures_permuted = permuter.forward( nextfeature )
    outlist = []
    for i in range( inputdim ):
      x = tf.reshape( xfeatures_permuted[ :, i ], [ -1, 1 ] )
      
      # conditioner network
      net1 = x
      condnet = xcondin
      for _ in range( hidden_cond ):
        condnet = layers.Dense( nodes_cond, activation = activation_key[ activation ], kernel_regularizer = regularizer_key[ regularizer ], name = f"COND_DENSE_{idepth}_{iv}_{i}" )( condnet )
      w1 = layers.Dense( nodes_trans, activation = tf.nn.softplus, name = f"SIGMOID_WEIGHT_{idepth}_{iv}" )(condnet ) # has to be softplus for output to be >0
      b1 = layers.Dense( nodes_trans, activation = None, name = f"SIGMOID_BIAS_{idepth}_{iv}" )( condnet )
      del condnet
      # transforming layer
      net2 = tf.nn.sigmoid( w1 * net1 + b1,  name = f"TRANS_DENSE_{idepth}_{iv}" ) 
       
      # reverse conditioner network
      condnet = xcondin
      for _ in range( hidden_cond ):
        condnet = layers.Dense( nodes_cond, activation = activation_key[ activation ], kernel_regularizer = regularizer_key[ regularizer ], name = f"INV_COND_DENSE_{idepth}_{iv}_{i}" )( condnet )
      w2 = layers.Dense( nodes_trans, activation = tf.nn.softplus, name = f"INV_SIGMOID_WEIGHT_{idepth}_{iv}" )( condnet )
      w2 = w2 / ( 1.0e-6 + tf.reduce_sum( w2, axis = 1, keepdims = True ) ) # normalize the transformer output
      
      # inverse transformer network
      net3 = invsigmoid( tf.reduce_sum( net2 * w2, axis = 1, keepdims = True ) )
      
      outlist.append( net3 )
      xcondin = tf.concat( [ xcondin, x ], axis = 1 )
      
    outputlayer_permuted = tf.concat( outlist, axis = 1 )
    outputlayer = permuter.inverse( outputlayer_permuted )
    nextfeature = outputlayer
    
  return keras.Model( xin, outputlayer )
      
def mix_rbf_mmd2( X, Y, sigmas = ( 1, ), wts = None ):
  def mix_rbf_kernel( X, Y, sigmas, wts ):
    if wts is None: wts = [1] * len( sigmas )
    
    # matmul is matrix multiplication between X and Y where X is the target batch and Y is the generated batch
    XX = tf.matmul( X, X, transpose_b = True )
    XY = tf.matmul( X, Y, transpose_b = True )
    YY = tf.matmul( X, Y, transpose_b = True )
    
    X_sqnorms = tf.linalg.diag_part( XX )
    Y_sqnorms = tf.linalg.diag_part( YY )
    
    r = lambda x: tf.expand_dims( x, 0 )
    c = lambda x: tf.expand_dims( x, 1 )
    
    K_XX, K_XY, K_YY = 0, 0, 0
    
    for sigma, wt in zip( sigmas, wts ):
      gamma = 1 / ( 2 * sigma**2 )
      K_XX += wt * tf.exp( -gamma * ( -2 * XX + c(X_sqnorms) + r(X_sqnorms) ) )
      K_XY += wt * tf.exp( -gamma * ( -2 * XY + c(X_sqnorms) + r(Y_sqnorms) ) )
      K_YY += wt * tf.exp( -gamma * ( -2 * YY + c(Y_sqnorms) + r(Y_sqnorms) ) )
    
    # reduce_sum() computes sum of elements across dimensions of a tensor
    return K_XX, K_XY, K_YY, tf.reduce_sum( wts )
  
  K_XX, K_XY, K_YY, d = mix_rbf_kernel( X, Y, sigmas, wts )
  m = tf.cast( tf.shape( K_XX )[0], tf.float32 )
  n = tf.cast( tf.shape( K_YY )[0], tf.float32 )
  
  mmd2 = ( tf.reduce_sum( K_XX ) / ( m * m ) + tf.reduce_sum( K_YY ) / ( n * n ) - 2 * tf.reduce_sum( K_XY ) / ( m * n ) )
  return mmd2
  
# Onehot encoding class
class OneHotEncoder_int( object ):
  def __init__( self, categorical_features, lowerlimit = None, upperlimit = None ):
    self.iscategorical = categorical_features
    self.ncolumns = len(categorical_features)
    self.ncats = 0
    self.categories_per_feature = []

    self.ncatgroups = 0
    for b in categorical_features:
      if b:
        self.ncatgroups += 1
    self.lowerlimit = lowerlimit 
    self.upperlimit = upperlimit
    self.categories_fixed = False
    pass

  def applylimit( self, categoricalinputdata ):
    if self.lowerlimit is None:
      self.lowerlimit = np.min( categoricalinputdata, axis=0 )
    else:
      self.lowerlimit = np.maximum( self.lowerlimit, np.min( categoricalinputdata, axis = 0 ) )
    
    if self.upperlimit is None:
      self.upperlimit = np.max( categoricalinputdata, axis = 0 )
    else:
      self.upperlimit = np.minimum( self.upperlimit, np.max( categoricalinputdata, axis = 0 ) )

    lowerlimitapp = np.maximum( categoricalinputdata, self.lowerlimit )
    limitapp = np.minimum( lowerlimitapp, self.upperlimit )
    
    return limitapp

  def encode( self, inputdata ):
  # encoding done in prepdata()
    cat_limited = self.applylimit( inputdata ) - self.lowerlimit

    # one hot encoding information
    if not self.categories_fixed:
      for icol, iscat in zip( range( self.ncolumns ), self.iscategorical ):
        if iscat:
          ncats = int( self.upperlimit[icol] - self.lowerlimit[icol] + 1 )
          self.categories_per_feature.append( ncats )
          self.ncats += ncats 
        else:
          self.categories_per_feature.append( 0 )
      self.categories_fixed = True

    # the encoding part
    arraylist = []
    for icol, ncat_feat in zip( range( self.ncolumns ), self.categories_per_feature ):
      if ncat_feat > 0:
        res = np.eye( ncat_feat )[ cat_limited[ :,icol ].astype(int) ]
        arraylist.append( res )
      else:
        arraylist.append( inputdata[:,icol].reshape( ( inputdata.shape[0], 1 ) ) )
    encoded = np.concatenate( tuple( arraylist ), axis = 1 ).astype( np.float32 )
    return encoded

  def encodedcategories( self ):
    return self.ncats

  def transform( self, inputdata ):
    return self.encode( inputdata )

  def decode( self, onehotdata ):
    current_col = 0 # start from column 0
    arraylist = []
    for ifeat, ncats in zip( range( len( self.categories_per_feature ) ), self.categories_per_feature ):
      if ncats > 0:
        datatoconvert = onehotdata[ :, current_col:current_col+ncats ]
        converted = np.argmax( datatoconvert, axis = 1 ) + self.lowerlimit[ ifeat ]
        converted = np.reshape( converted, newshape = ( converted.shape[0], 1 ) )
        arraylist.append( converted )
        current_col += ncatgroups
      else:
        arraylist.append( onehotdata[:, current_col].reshape((onehotdata.shape[0], 1) ) )
        current_col += 1
    decoded = np.concatenate( tuple( arraylist ), axis = 1 )
    return decoded
  
class SawtoothSchedule( LearningRateSchedule ):
  def __init__(self, start_learning_rate = 1e-4, end_learning_rate = 1e-6, cycle_steps = 100, random_fluctuation = 0.0, name = None ):
    super( SawtoothSchedule, self ).__init__()
    self.start_learning_rate = start_learning_rate 
    self.end_learning_rate = end_learning_rate
    self.cycle_steps = cycle_steps
    self.random_fluctuation = random_fluctuation
    self.name = name
  pass

  def __call__( self, step ):
    phase = step % self.cycle_steps
    lr = self.start_learning_rate + ( self.end_learning_rate - self.start_learning_rate ) * ( phase / self.cycle_steps )
    if ( self.random_fluctuation > 0 ):
      lr *= np.random.normal( 1.0, self.random_fluctuation )
    return lr

  def get_config( self ):
    return {
        "start_learning_rate": self.start_learning_rate,
        "end_learning_rate": self.end_learning_rate,
        "cycle_step": self.cycle_steps,
        "random_fluctuation": self.random_fluctuation,
        "name": self.name
    }
  
def unweight(pddata):
# by default, this isn't used, need to use option prepdata( mc_weight = "unweight" )
  nrows = pddata.shape[0]
  minweight = pddata['xsecWeight'].min()
  maxweight = pddata['xsecWeight'].max()
  selrows = pddata['xsecWeight']>minweight # identify all entries above the minimum xsec weight

  datatoexpand = pddata[selrows].sort_values(by=['xsecWeight']) # sort selected entries by xsec weight
  nselected = datatoexpand.shape[0] 
  idx = 0
  print(nselected)
  while idx < nselected-1: # loop through all selected entries
    thisweight = datatoexpand.iloc[idx]['xsecWeight']
    multfactor = int(thisweight//minweight)
    selectrows = (datatoexpand['xsecWeight']==thisweight)
    matches = datatoexpand[selectrows]
    nmatches = matches.shape[0]
    pddata = pddata.append([matches]*multfactor)
    idx += nmatches
    print(idx)
  return pddata
  
def prepdata( rSource, rTarget, selection, variables, mc_weight = None ):
# mc_weight(str) = option for weighting MC by the xsec
# rSource (str) = source ROOT file
# rTarget (str) = target ROOT file
# selection (dict) = event selection with key: value
# variables (dict) = list of all variables considered and associated parameters

  # set up one-hot encoder
  vars = [ str( var ) for var in variables ]
  categorical = [ variables[ var ][ "categorical" ] for var in variables ]
  upperlimit  = [ variables[ var ][ "limit" ][1] for var in variables ]

  _onehotencoder = OneHotEncoder_int( categorical, upperlimit = upperlimit )

  # read MC and data
  mcf = uproot.open( rSource )
  dataf = uproot.open( rTarget )
  tree_mc = mcf[ 'Events' ]
  tree_data = dataf[ 'Events' ]
  mc_df = {}
  data_df = {}
  for var in selection:
    mc_df[ var ] = tree_mc.pandas.df( var ) 
    data_df[ var ] = tree_data.pandas.df( var )
  zero_key = list( selection.keys() )[0]
  mc_select = ( mc_df[ zero_key ][ zero_key ] >= selection[ zero_key ] )
  data_select = ( data_df[ zero_key ][ zero_key ] >= selection[ zero_key ] )
  for var in selection.keys():
    if var != zero_key:
      mc_select &= ( mc_df[ var ][ var ] >= selection[ var ] )
      data_select &= ( data_df[ var ][ var ] >= selection[ var ] )

  # do not consider cross section weight. The weight of the resut file is filled with 1.
  if mc_weight == None:
    inputrawmc = tree_mc.pandas.df( vars )[ mc_select ]
    inputrawmcweight = None

  # The weight of the resut file is filled with 'xsecWeight'
  if mc_weight == "weight":
    inputrawmc = tree_mc.pandas.df( vars )[ mc_select ]
    inputrawmcweight = tree_mc.pandas.df( [ 'xsecWeight' ] )[ mc_select ].to_numpy( dtype=np.float32 )
  
  # duplicate source samples according to the cross section. The weight of the resut file is filled with 1.
  # may take too long if input sample is the combined one with several samples that has different cross section.
  if mc_weight == "unweight":
    inputrawmc = unweight(tree_mc.pandas.df( vars + ['xsecWeight'])[ mc_select ]).drop( columns=['xsecWeight'] )
    inputrawmcweight = None
  
  inputsmc_enc = _onehotencoder.encode( inputrawmc.to_numpy( dtype=np.float32 ) )

  inputrawdata = tree_data.pandas.df( vars )[ data_select ]
  inputrawdata_np = inputrawdata.to_numpy( dtype=np.float32 )  
  inputrawdata_enc = _onehotencoder.encode( inputrawdata_np )

  inputsdata = _onehotencoder.encode( inputrawdata.to_numpy(dtype=np.float32))

  ncats = _onehotencoder.ncats
  ncat_per_feature = _onehotencoder.categories_per_feature

  meanslist = []
  sigmalist = []
  currentcolumn = 0

  # normalize data
  for ifeat, ncatfeat in zip( range( inputsdata.shape[1] ), ncat_per_feature ):
    if ncatfeat == 0: # for float features, get mean and sigma
      mean = np.mean( inputrawdata_np[:, currentcolumn], axis=0, dtype=np.float32 ).reshape( 1, 1 )
      meanslist.append( mean )
      sigma = np.std( inputrawdata_np[:, currentcolumn], axis=0, dtype=np.float32 ).reshape( 1, 1 )
      sigmalist.append( sigma )
      currentcolumn += 1
    else: # categorical features do not get changed
      mean = np.zeros( shape = ( 1, ncatfeat ), dtype=np.float32 ) 
      meanslist.append( mean )
      sigma = np.ones( shape = ( 1, ncatfeat ), dtype=np.float32 )
      sigmalist.append( sigma )
      currentcolumn += ncatfeat

  inputmeans = np.hstack( meanslist )
  inputsigma = np.hstack( sigmalist )

  normedinputs_data = ( inputrawdata_enc - inputmeans ) / inputsigma        # normed Data
  normedinputs_mc = ( inputsmc_enc - inputmeans ) / inputsigma              # normed MC

  return inputrawdata, inputrawmc, inputrawmcweight, normedinputs_data, normedinputs_mc, inputmeans, inputsigma, ncat_per_feature
  
  
# construct the ABCDnn model here
class ABCDnn(object):
  def __init__( self, inputdim_categorical_list, inputdim, nodes_cond, hidden_cond,
               nodes_trans, minibatch, activation, regularizer,
               depth, lr, gap, conddim, beta1, beta2, decay,
               retrain, savedir, savefile, 
               seed, permute, verbose ):
    self.inputdim_categorical_list = inputdim_categorical_list
    self.inputdim = inputdim
    self.inputdimcat = int( np.sum( inputdim_categorical_list ) )
    self.inputdimreal = inputdim - self.inputdimcat
    self.minibatch = minibatch
    self.nodes_cond = nodes_cond
    self.hidden_cond = hidden_cond
    self.nodes_trans = nodes_trans
    self.activation = activation
    self.regularizer = regularizer
    self.depth = depth
    self.lr = lr 
    self.decay = decay
    self.gap = gap
    self.conddim = conddim
    self.beta1 = beta1
    self.beta2 = beta2
    self.retrain = retrain
    self.savedir = savedir
    self.savefile = savefile
    self.global_step = tf.Variable( 0, name = "global_step" )
    self.monitor_record = []
    self.seed = seed 
    self.permute = permute
    self.verbose = verbose
    self.minloss = 0
    self.setup()

  def setup( self ):
    np.random.seed( self.seed )
    tf.random.set_seed( self.seed )
    self.createmodel()
    self.checkpoint = tf.train.Checkpoint( global_step = self.global_step, model = self.model, optimizer = self.optimizer )
    self.checkpointmgr = tf.train.CheckpointManager( self.checkpoint, directory = self.savedir, max_to_keep = 1 )
    if (not self.retrain) and os.path.exists(self.savedir):
      status = self.checkpoint.restore(self.checkpointmgr.latest_checkpoint)
      status.assert_existing_objects_matched()
      print( ">> Loaded model from checkpoint" )
      if os.path.exists(os.path.join(self.savedir, self.savefile)):
        print( ">> Reading monitor file" )
        self.load_training_monitor()
      print( ">> Resuming from step {}".format( self.global_step ) )
    elif not os.path.exists(self.savedir):
      os.mkdir(self.savedir)
    pass

  def createmodel( self ):
    self.model = NAF( 
      inputdim = self.inputdim,  
      conddim = self.conddim, 
      activation = self.activation,
      regularizer = self.regularizer,
      nodes_cond = self.nodes_cond, 
      hidden_cond = self.hidden_cond,
      nodes_trans = self.nodes_trans, 
      depth = self.depth, 
      permute = self.permute
    )
    if self.verbose: self.model.summary()
    self.optimizer = keras.optimizers.Adam(
      learning_rate = SawtoothSchedule( self.lr, self.lr * self.decay, self.gap, 0 ),  
      beta_1 = self.beta1, beta_2 = self.beta2, 
      epsilon = 1e-5, 
      name = 'nafopt'
    )
    pass

  def category_sorted(self, numpydata, verbose ):
    categoricals, categorical_cats, unique_counts = np.unique( numpydata[:, self.inputdimreal:], axis=0, return_inverse = True, return_counts = True)
    if verbose: 
      print( f"Data has {categoricals} unique  categorical features. The counts in categories are" )
      print( unique_counts )

    # store indices separately for easy access later
    categorical_indices_grouped = []
    for icat in range( len( categoricals ) ):
      cat_indices = np.where( categorical_cats == icat )[0]
      categorical_indices_grouped.append( cat_indices )
    
    return categoricals, categorical_indices_grouped

  def setrealdata( self, numpydata, verbose ):
    self.numpydata = numpydata
    self.ntotalevents = numpydata.shape[0]
    self.datacounter = 0
    self.randorder = np.random.permutation( self.numpydata.shape[0] )
    # following is dummy
    self.dataeventweight = np.ones((self.ntotalevents, 1), np.float32)
    # find unique occurrenes of categorical features in data
    self.categoricals_data, self.categorical_data_indices_grouped = self.category_sorted( self.numpydata, verbose )
    pass

  def setmcdata(self, numpydata, verbose, eventweight = None ):
    self.mcnumpydata = numpydata
    self.mcntotalevents = numpydata.shape[0]
    self.mcdatacounter = 0
    self.mcrandorder = np.random.permutation( self.mcnumpydata.shape[0] )
    if eventweight is not None:
      self.mceventweight = eventweight
    else:
      self.mceventweight = np.ones( ( self.mcntotalevents, 1 ) , np.float32 )
    self.categoricals_mc, self.categorical_mc_indices_grouped = self.category_sorted( self.mcnumpydata, verbose )
    pass

  def savehyperparameters(self):
    """Write hyper parameters into file
    """
    params = {
      "inputdim": self.inputdim, 
      "conddim": self.conddim, 
      "lr": self.lr,
      "decay": self.decay, 
      "gap": self.gap, 
      "nodes_cond": self.nodes_cond, 
      "hidden_cond": self.hidden_cond, 
      "nodes_trans": self.nodes_trans, 
      "beta1": self.beta1, 
      "beta2": self.beta2, 
      "minibatch": self.minibatch,
      "activation": self.activation,
      "regularizer": self.regularizer,
      "depth": self.depth  
    }
    pickle.dump( params, open( os.path.join( self.savedir, "hyperparams.pkl" ), "wb" ) )

  def monitor( self, step, glossv_trn, glossv_val, mmdloss_trn, mmdloss_val  ):
    self.monitor_record.append( [ 
      step, 
      glossv_trn, glossv_val, 
      mmdloss_trn, mmdloss_val 
      ]
    )

  def save_training_monitor(self):
    pickle.dump( self.monitor_record, open(os.path.join( self.savedir, self.savefile ), 'wb' ))
    pass

  def load_training_monitor(self):
    fullfile = os.path.join( self.savedir, self.savefile )
    if os.path.exists(fullfile):
      self.monitor_record = pickle.load(open(fullfile, 'rb'))
      self.epoch = self.monitor_record[-1][0] + 1
    pass

  def find_condmatch(self, conditional):
    
    """[Find data and MC batches matching conditional category]

    Args:
        conditional ([numpy]): [single conditional]
    """

    idx_cond = ( ( self.categoricals_data == conditional ).all( axis = 1 ).nonzero()[0])[0]
    # Data
    data_for_cond = self.categorical_data_indices_grouped[idx_cond]
    nextdatabatchidx = np.random.permutation(data_for_cond)[0:self.minibatch]
    target_b = self.numpydata[nextdatabatchidx]

    # MC
    idx_cond = ((self.categoricals_mc == conditional).all(axis=1).nonzero()[0])[0]
    mc_for_cond = self.categorical_mc_indices_grouped[idx_cond]
    mcnextbatchidx = np.random.permutation(mc_for_cond)[0:self.minibatch]
    source_b = self.mcnumpydata[mcnextbatchidx]
    weight_b = self.mceventweight[mcnextbatchidx]
    return target_b, source_b, weight_b
  
  def get_next_batch(self, split, size=None, cond=True):
    """Return minibatch from random ordered numpy data
    """
    if size is None:
      size = int( self.minibatch * ( split ** -1 ) )

    # reset counter if no more entries left for current batch
    if self.datacounter + size >= self.ntotalevents:
      self.datacounter = 0
      self.randorder = np.random.permutation( self.numpydata.shape[0] )

    if self.mcdatacounter + size >= self.mcntotalevents:
      self.mcdatacounter = 0
      self.mcrandorder = np.random.permutation( self.mcnumpydata.shape[0] )

    batchbegin = self.datacounter

    if not cond:
      batchend = batchbegin + size
      target = self.numpydata[ self.randorder[ batchbegin:batchend ], 0:: ]
    else:
      nextconditional = self.numpydata[ self.randorder[batchbegin], self.inputdim: ]
      target_b, source_b, weight_b = self.find_condmatch( nextconditional )

    self.datacounter += size
    self.this_source = source_b
    self.this_target = target_b
    self.this_weight = weight_b
    return source_b, target_b, weight_b

  # eqvuialent to train_step = tf.function( train_step )
  @tf.function
  def train_step(self, source, target, split, sourceweight=1. ):
    source_trn, source_val, target_trn, target_val = train_test_split(
      self.this_source, self.this_target, test_size = split
    )
    
    with tf.GradientTape() as gtape:
      # get the predicted values from the current trained model
      generated_trn = tf.concat( [
          self.model( source_trn, training = True ),
          target_trn[:, -self.conddim:]
        ],
        axis = -1
      )

      #mmdloss = mix_rbf_mmd2(targetbatch[:, :self.inputdim], generated[:, :self.inputdim], sigmas=(0.1, 0.2,)) # for 1-D or 2-D
      mmdloss_trn = mix_rbf_mmd2( target_trn[:, :self.inputdim], generated_trn[:, :self.inputdim], sigmas=(0.2, 0.5, 1.0, 2.0, 4.0) ) # not clear how these sigma values were chosen
    
    gradient = gtape.gradient( mmdloss_trn, self.model.trainable_variables )
    self.optimizer.apply_gradients( zip( 
        gradient, 
        self.model.trainable_variables 
      ) 
    )

    generated_val = tf.concat( [
        self.model( source_val, training = False ),
        target_val[ :, -self.conddim:]
      ],
      axis = -1
    )

    mmdloss_val = mix_rbf_mmd2( target_val[:, :self.inputdim], generated_val[:, :self.inputdim], sigmas=(0.2, 0.5, 1.0, 2.0, 4.0) )

    glossv_trn = tf.reduce_mean( mmdloss_trn )
    glossv_val = tf.reduce_mean( mmdloss_val )

    return glossv_trn, glossv_val, mmdloss_trn, mmdloss_val

  def train( self, steps = 10000, monitor = 1000, patience = 100, early_stopping = True, split = 0.25, hpo = False ):
    # need to update this to use a validation set
    print( "{:<5} / {:<14} / {:<14} / {:<14}".format( "Epoch", "MMD (Train)", "MMD (Val)", "Min MMD (Val)" ) ) 
    impatience = 0      # don't edit
    stop_train = False  # don't edit
    self.minepoch = 0
    for i in range( steps ):
      source, target, batchweight = self.get_next_batch( split = split )
      glossv_trn, glossv_val, mmdloss_trn, mmdloss_val  = self.train_step( source, target, split, batchweight )
      # currently not using glossv because mmdloss is a scalar and glossv is the mean of mmdloss
      # generator update
      if i == 0: self.minloss = mmdloss_val
      else: 
        if mmdloss_val.numpy() < self.minloss.numpy(): 
          self.minloss = mmdloss_val
          self.minepoch = i
          impatience = 0
          if not hpo: self.checkpointmgr.save()
        elif impatience > patience:
          print( ">> Early stopping after {} epochs without improvement in loss (min loss = {:.2e})".format( i, self.minloss ) )
          stop_train = True
        else:
          impatience += 1
      if i % monitor == 0:
        print( "{:<5}   {:<14.3e}   {:<14.3e}    {:<14.3e}".format( 
          self.checkpoint.global_step.numpy(),
          mmdloss_trn.numpy(),
          mmdloss_val.numpy(),
          self.minloss
         ) )
        self.monitor( 
          self.checkpoint.global_step.numpy(), 
          glossv_trn.numpy(), glossv_val.numpy(),
          mmdloss_trn, mmdloss_val
        )
      self.checkpoint.global_step.assign_add(1) # increment counter
      if stop_train: break
    print( ">> Minimum loss (validation) of {:.3e} on epoch {}".format( self.minloss, self.minepoch ) )
    self.save_training_monitor()

  def display_training(self):
    # Following section is for creating movie files from trainings

    fig, ax = plt.subplots(1,2, figsize=(6,6))
    monarray = np.array(self.monitor_record)
    x = monarray[0::, 0]
    ax[0].plot(x, monarray[0::, 1], color='r', label='MMD (Training)')
    ax[0].plot(x, monarray[0::, 2], color='b', label='MMD (Validation)')
    ax[0].set_ylabel( "MMD Loss", ha = "right", y = 1.0 )
    ax[0].set_yscale('linear')
    ax[0].legend()
    ax[1].plot(x, monarray[0::, 2], color='r', label='MMD')
    ax[0].set_ylabel( "MMD", ha = "right", y = 1.0 )
    ax[1].set_yscale('log')
    ax[1].legend()

    plt.draw()

    #fig.savefig(os.path.join(self.savedir, 'trainingperf.pdf'))
    pass  
