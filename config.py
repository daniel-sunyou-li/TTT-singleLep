# updated 10/23/2021 by Daniel Li
# edit the parameters here before running train_abcdnn.py

import os

data_path = os.path.join( os.getcwd(), "/Data/" )
if not os.path.exists( data_path ): os.system( "mkdir {}".format( data_path ) )
  
variables = {
  "AK4HT": {
    "categorical": False,
    "transform": True,
    "limit": [0.,3000.],
    "latex": "H_T\ \mathrm{(GeV)}"
  },
  "DNN_5j_1to30_S2B5": {
    "categorical": False,
    "transform": True,
    "limit": [0.,1.],
    "latex": "DNN_{1-30}"
  },
  "NJets_JetSubCalc": {
    "categorical": True,
    "transform": False,
    "limit": [0,10],
    "latex": "N_j"
  },
  "NJetsCSV_MultiLepCalc": {
    "categorical": True,
    "transform": False,
    "limit": [0,3],
    "latex": "N_b"
  }
}

selection = {
  "AK4HT": 350.,
  "NJets_JetSubCalc": 5
}

regions = {
  "X": {
    "Variable": "NJets_JetSubCalc",
    "Inclusive": True,
    "Min": 6,
    "Max": 8,
    "Signal": 8
  },
  "Y": {
    "Variable": "NJetsCSV_MultiLepCalc",
    "Inclusive": True,
    "Min": 2,
    "Max": 3,
    "Signal": 3
  }
}

params = {
  "EVENTS": {
    "SOURCE": os.path.join( data_path, "Semileptonic_HT0Njet0_2017_mc.root" ),
    "TARGET": os.path.join( data_path, "singleLep_2017_data.root" ),
    "MCWEIGHT": None
  },
  "MODEL": {
    "NODES_COND": 16,
    "HIDDEN_COND": 3,
    "NODES_TRANS": 8,
    "LRATE": 1e-5,
    "DECAY": 1e-1,
    "GAP": 1000.,
    "DEPTH": 2,
    "REGULARIZER": "None",
    "ACTIVATION": "softplus",
    "BETA1": 0.90,
    "BETA2": 0.90,
    "MINIBATCH": 105,
    "RETRAIN": True,
    "SEED": np.random.randint( 100000 ),
    "SAVEDIR": "/Results/",
    "VERBOSE": False
  },
  "TRAIN": {
    "EPOCHS": 20000,
    "PATIENCE": 5000,
    "MONITOR": 1000,
    "SPLIT": 0.25,
    "SHOWLOSS": True,
    "SAVEHP": True
  }
}

hyper = {
  "OPTIMIZE": {
    "NODES_COND": ( [8,16,32,64,128], "CAT" ),
    "HIDDEN_COND": ( [1,4], "INT" ),
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








  
