import os
import numpy as np

data_path = os.path.join( os.getcwd(), "Data" )
results_path = os.path.join( os.getcwd(), "Results" )

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
  "MODEL": { # parameters for setting up the NAF model
    "NODES_COND": 16,
    "HIDDEN_COND": 3,
    "NODES_TRANS": 8,
    "LRATE": 1.0e-5,
    "DECAY": 1e-1,
    "GAP": 1000.,
    "DEPTH": 2,
    "REGULARIZER": "None",
    "ACTIVATION": "softplus",
    "BETA1": 0.90,
    "BETA2": 0.90,
    "MINIBATCH": 105,
    "RETRAIN": True,
    "SEED": 101 if use_randSeed.value else np.random.randint( 100000 ),
    "SAVEDIR": "./Results/",
    "VERBOSE": False   
  },
  "TRAIN": {
    "EPOCHS": 15000,
    "PATIENCE": 5000,
    "SPLIT": 0.25,
    "MONITOR": 1000,
    "SHOWLOSS": True,
    "SAVEHP": True
  },
  "PLOT": {
    "RATIO": [ 0.25, 2.0 ], # y limits for the ratio plot
    "YSCALES": [ "log" ],   # which y-scale plots to produce
    "NBINS": 20,            # histogram x-bins
    "ERRORBARS": True,      # include errorbars on hist
    "NORMED": True,         # normalize histogram counts/density
    "SAVE": False,          # save the plots as png
    "PLOT_KS": True,        # include the KS p-value in plots
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
