import os
import numpy as np

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

if int( regions[ "X" ][ "MAX" ] - regions[ "X" ][ "MIN" ] + 1 ) * int( regions[ "Y" ][ "MAX" ] - regions[ "Y" ][ "MIN" ] + 1 ):
  print( "[WARN] The chosen control variable ranges does not result in 6 regions. Please choose new ranges for control variables X and Y. Edit `regions` in config.py"

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
    "MONITOR": 1000,
    "SHOWLOSS": True,
    "SAVEHP": True
  }
}






