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
  
  xin = layers.Input( shape = ( inputdim + conddim, ) )
  xcondin = xin[ :, inputdim: ]
  xfeatures = xin[ :, :inputdim ]
  nextfeature = xfeatures
  
  for idepth in range( depth ):
    if permute: # mix up the input order of the consecutive neural networks in the flow
      randperm = np.random.permutation( inputdim ).astype( "int32" )
      permutation = tf.constant( randperm, name = f"permutation{idepth}" )
    else:
      permutation = tf.range( inputdim, dtype = "int32", name = f"permutation{idepth}" )
    permuter = tfp.bijectors.Permute( permutation = permutation, name = f"permute{idepth}" )
    xfeatures_permuted = permuter.forward( nextfeature )
    outlist = []
    for i in range( inputdim ):
      x = tf.reshape( xfeatures_permuted[ :, i ], [ -1, 1 ] )
      
      # conditioner network
      net1 = x
      condnet = xcondin
      for _ in range( hidden_cond ):
        condnet = layers.Dense( nodes_cond, activation = activation_key[ activation ], kernel_regularizer = regularizer_key[ regularizer ] )( condnet )
      w1 = layers.Dense( nodes_trans, activation = tf.nn.softplus )( condnet ) # has to be softplus for output to be >0
      b1 = layers.Dense( nodes_trans, activation = None )( condnet )
      del condnet
      
      
      # transformer network
      net2 = tf.nn.sigmoid( w1 * net1 + b1 ) 
      condnet = xcondin
      for _ in range( hidden_cond ):
        condnet = layers.Dense( nodes_cond, activation = activation_key[ activation ], kernel_regularizer = regularizer_key[ regularizer ] )( condnet )
      w2 = layers.Dense( nodes_trans, activation = tf.nn.softplus )( condnet )
      w2 = w2 / ( 1.0e-6 + tf.reduce_sum( w2, axis = 1, keepdims = True ) ) # normalize the transformer output
      
      # inverse transformer network
      net3 = invsigmoid( tf.reduce_sum( net2 * w2, axis = 1, keepdims = True ) )
      
      outlist.append( net3 )
      xcondin = tf.concat( [ xcondin, x ], axis = 1 )
      
    outputlayer_permuted = tf.concat( outlist, axis = 1 )
    outputlayer = permuter.inverse( outputlayer_permuted )
    nextfeature = outputlayer
    
  return keras.Model( xin, outputlayer )
      
  
  
  
  
  
  
  
  
