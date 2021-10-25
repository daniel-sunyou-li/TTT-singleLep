import os
import numpy as np
from skopt.space import Real, Integer, Categorical

data_path = os.path.join( os.getcw(), "Data" )

variables = {
  "AK4HT": {
    "CATEGORICAL": False,
    "TRANSFORM": True,
    "LIMIT": [0.,3000.],
    "LATEX": "H_T\ \mathrm{(GeV)}"
  },
  "DNN_5j_1to30_S2B5": {
    "CATEGORICAL": False,
    "TRANSFORM": True,
    "LIMIT": [0.,1.],
    "LATEX": "DNN_{1-30}"
  },
  "NJets_JetSubCalc": {
    "CATEGORICAL": True,
    "TRANSFORM": False,
    "LIMIT": [0,16],
    "LATEX": "N_j"
  },
  "NJetsCSV_MultiLepCalc": {
    "CATEGORICAL": True,
    "TRANSFORM": False,
    "LIMIT": [0,6],
    "LATEX": "N_b"
  }
}

selection = {
  "AK4HT": 350.,
  "NJets_JetSubCalc": 6
}

regions = {
  "X": {
    "VARIABLE": "NJets_JetSubCalc",
    "INCLUSIVE": True,
    "MIN": 6,
    "MAX": 8,
    "SIGNAL": 8
  },
  "Y": {
    "VARIABLE": "NJetsCSV_MultiLepCalc",
    "INCLUSIVE": True,
    "MIN": 2,
    "MAX": 3,
    "SIGNAL": 3
  }
}

params = {
  "EVENTS": {
    "SOURCE": os.path.join( data_path, "Semileptonic_HT0Njet0_2017_mc.root" ),
    "TARGET": os.path.join( data_path, "singleLep_2017_data.root" ),
    "MCWEIGHT": None
  },
  "MODEL": {
    "NDENSE": 64,
    "MINIBATCH": 64,
    "LR": 1.0e-5,
    "GAP": 1000,
    "NAFDIM": 30,
    "DEPTH": 3,
    "RETRAIN": True,
    "SEED": 101,
    "SAVEDIR": "./Results/"
  },
  "TRAIN": {
    "EPOCHS": 15000,
    "PATIENCE": 5000,
    "SPLIT": 0.25,
    "MONITOR": 1000,
    "SHOWLOSS": True,
    "SAVEHP": True
  }
}
        
hyper = {
  "OPTIMIZE": {
    "NODES_COND": ( [8,16,32,64,128], "CAT" ),
    "HIDDEN_COND": ( [1,4] ), "INT" ),
    "NODES_TRANS": ( [1,8,16,32,64,128], "CAT" ),
    "LRATE": ( [1e-5,1e-4,1e-3,1e-2,1e-1], "CAT" ),
    "DECAY": ( [1,1e-1,1e-2,1e-3], "CAT" ),
    "GAP": ( [100,500,1000,5000], "CAT" ),
    "DEPTH": ( [1,4], "INT" ),
    "REGULARIZER": ( ["L1","L2","L1+L2","None"], "CAT" ),
    "ACTIVATION": ( ["swish","relu","elu","softplus"], "CAT" ),
    "BETA1": ( [0.5,0.75,0.90,0.99,0.999], "CAT" ),
    "BETA2": ( [0.5,0.75,0.90,0.99,0.999], "CAT" )
  },
  "PARAMS": {
    "PATIENCE": 2000,
    "EPOCHS": 10000,
    "N_RANDOM": 20,
    "N_CALLS": 30,
    "MINIBATCH": 105,
    "VERBOSE": True
  }
}
       
space = []
if args.hpo:
  for hp in hyper[ "OPTIMIZE" ]:
    if hyper[ "OPTIMIZE" ][ hp ][ i ] == "CAT": 
      space.append( Categorical( hyper[ "OPTIMIZE" ][ hp ][0], name = str(hp) ) ) )
    elif config.hyper[ "OPTIMIZE" ][ hp ][ i ] == "INT":
      space.append( Integer( hyper[ "OPTIMIZE" ][ hp ][0][0], hyper[ "OPTIMIZE" ][0][1], name = str(hp) ) )
    elif config.hyper[ "OPTIMIZE" ][ hp ][ i ] == "REAL":
      space.append( Real( hyper[ "OPTIMIZE" ][ hp ][0][0], hyper[ "OPTIMIZE" ][0][1], name = str(hp) ) )
