# updated 10/25 by Daniel Li
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
from json import loads as load_json
from json import dumps as write_json
from argparse import ArgumentParser

# import custom methods
import config
import abcdnn

parser = ArgumentParser()
parser.add_argument( "-s", "--source", default = "", required = False )
parser.add_argument( "-t", "--target", default = "", required = False )
parser.add_argument( "-h", "--hpo", store_action = True )
parser.add_arugment( "-v", "--verbose", store_action = True )
args = parser.parse_args()

if args.source != "": config.params[ "EVENTS" ][ "SOURCE" ] = os.path.join( config.data_path, args.source )
if args.target != "": config.params[ "EVENTS" ][ "TARGET" ] = os.path.join( config.data_path, args.target )

nTrans = len( [ var for var in config.variables if config.variables[ var ][ "transform" ] == True ] )
    
hp = 
if args.hpo:
  print( ">> Running on optimized parameters" )
  with open( os.path.join( config.results_path, "opt_params.json" ), "r" ) as jsf:
    
  for i,
else:
               
abcdnn_ = abcdnn.ABCDnn_training()
abcdnn_.setup_events(
  rSource = config.params[ "EVENTS" ][ "SOURCE" ], 
  rTarget = config.params[ "EVENTS" ][ "TARGET" ],
  selection = config.selection,
  variables = config.variables,
  regions = config.regions,
  mc_weight = config.params[ "EVENTS" ][ "MCWEIGHT" ]
)

abcdnn_.setup_model(
  nodes_cond = hp[ "NODES_COND" ],
  hidden_cond = hp[ "HIDDEN_COND" ],
  nodes_trans = hp[ "NODES_TRANS" ],
  lr = hp[ "LRATE" ],
  decay = hp[ "DECAY" ],
  gap = hp[ "GAP" ],
  depth = hp[ "DECAY" ],
  regularizer = hp[ "REGULARIZER" ],
  activation = hp[ "ACTIVATION" ],
  beta1 = hp[ "BETA1" ],
  beta2 = hp[ "BETA2" ],
  minibatch = config.params[ "MODEL" ][ "MINIBATCH" ],
  savedir = config.params[ "MODEL" ][ "SAVEDIR" ],
  seed = config.params[ "MODEL" ][ "SEED" ],
  verbose = config.params[ "MODEL" ][ "VERBOSE" ],
  retrain = config.params[ "MODEL" ][ "RETRAIN" ]
)

abcdnn_.train(
  steps = config.params[ "TRAIN" ][ "EPOCHS" ],
  patience = config.params[ "TRAIN" ][ "PATIENCE" ],
  monitor = config.params[ "TRAIN" ][ "MONITOR" ],
  display_loss = config.params[ "TRAIN" ][ "SHOWLOSS" ],
  save_hp = config.params[ "TRAIN" ][ "SAVEHP" ]
)

abcdnn_.evaluate_regions()
abcdnn_.extended_ABCD()
