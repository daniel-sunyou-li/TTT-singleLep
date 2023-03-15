import numpy as np

years = [ "16APV", "16", "17", "18" ]

postfix = "3t"
inputDir = { year: "/isilon/hadoop/store/user/dali/FWLJMET106XUL_singleLep20{}UL_RunIISummer20_{}_step3/".format( year, postfix ) for year in years }

# target lumis in 1/pb for each year
lumi = {
  "16APV": 19520., # from pdmv
  "16": np.around( 16810. * 0.995 ),    # from pdmv, missing a few LJMet files from Run2016F
  "17": 41480.,    # calculated using brilcalc on GoldenJSON 
  "18": 59832.     # calculated using brilcalc on GoldenJSON
}
lumiStr = { year: str( lumi[ year ] / 1000. ).replace( ".", "p" ) + "fb" for year in lumi }

# Branching ratios
BR = {
  "BW" : [0.0,0.50,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0],
  "TH" : [0.5,0.25,0.0,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0],
  "TZ" : [0.5,0.25,1.0,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]
}

# boolean options that need to be coordinated across template making
options = {
  "GENERAL": {
    "TEST": False,        # run on limited samples
    "HDAMP": False,       # hdamp systematics
    "UE": False,          # ue systematics
    "PDF": True,          # pdf systematics
    "SYSTEMATICS": True,  # include other systematics defined in systematics[ "MC" ]
    "ABCDNN": True,
    "FINAL ANALYSIS": False
  },
  "HISTS": {
    "RENORM PDF": True,        # renormalize the PDF weights
    "SUMMARY": False,          # produce summary templates
    "SCALE SIGNAL 1PB": False, # Scale the signal xsec to 1 PB for future studies
  },
  "MODIFY BINNING": {
    "BLIND": True,                 #  
    "PDF": True,                   # add PDF systematic uncertainty
    "CR SYST": False,              # add systematic uncertainty to control region
    "SHAPE SYST": True,            # add systematic shape uncertainty 
    "SHAPE STAT": True,            # add statistical uncertainty 
    "MURF SHAPES": True,           # include QCD renormalization and factorization systematics
    "PS WEIGHTS": True,            # include parton shower weighting systematics as well as evaluate systematic envelope (PSwgt)
    "NORM THEORY SIG SYST": True,  # normalize the theoretical systematics (MURF, PS WEIGHTS, PDF) for the signal
    "NORM THEORY BKG SYST": True,  # normalize the theoretical systematics (MURF, PS WEIGHTS, PDF) for the background
    "SYMM SMOOTHING": True,        # symmetrize the systematics per bin before smoothing
    "SYMM TOP PT": True,           # symmetrize top pt systematic
    "SYMM HOTCLOSURE": True,       # symmetrize hotclosure systematic
    "SYMM THEORY": True,
    "NORM ABCDNN": True,
    "SCALE SIGNAL XSEC": False,    
    "ADD SHAPE SYST YIELD": True,
    "SMOOTH": True,                # perform smoothing
    "UNCORRELATE YEARS": True,     # add year postfix to systematics for decorrelation in Higgs combine
    "TRIGGER EFFICIENCY": False,
  },
  "COMBINE": {
    "ABCDNN": True,    # use ABCDnn and extended ABCD corrected histograms
    "SMOOTH": True,    # use smoothed systematic histograms
    "GROUPS": False,    # evaluate significance and limits with combinations of systematic groups
    "IMPACTS": {
      "MASKED": False,  # include evaluations of impacts with channels masked
      "FREEZE": False,  # include evaluations of impacts with NP frozen
    }
  }
}
# non-boolean parameters used in creating templates
params = {
  "GENERAL": {
    "ZERO": 1e-12,      # default non-zero value for zero to prevent division by zero
    "REBIN": -1,        # rebin histogram binning, use -1 to keep original binning
    "PDF RANGE": 100,   # PDF range
  },
  "ABCDNN": {
    "TAG": "nJ7pnB3pnHOT1p",                      # ABCDnn transformed variable tag i.e. <varname>_<tag>
    "TF": {
      "16APV": 0.01707,       # nJ5pnB2p = 0.02610, nJ7pnB3p = 0.01489, nJ7pnB3pnHOT1p = 0.01707
      "16": 0.01289,          # nJ5pnB2p = 0.02805, nJ7pnB3p = 0.01522, nJ7pnB3pnHOT1p = 0.01289
      "17": 0.00672,          # nJ5pnB2p = 0.01210, nJ7pnB3p = 0.00724, nJ7pnB3pnHOT1p = 0.00672 
      "18": 0.01138,          # nJ5pnB2p = 0.02060, nJ7pnB3p = 0.01123, nJ7pnB3pnHOT1p = 0.01138 
    },                        
    "TF SCALE": {  # additional yield scaling factor for ext abcd if applying cut on fit variable
      "16APV": 0.99994,   # nJ7pnB3pnHOT1pDNN20 = 0.99994
      "16"   : 0.99993,   # nJ7pnB3pnHOT1pDNN20 = 0.99993
      "17"   : 0.99991,   # nJ7pnB3pnHOT1pDNN20 = 0.99991
      "18"   : 0.99995,   # nJ7pnB3pnHOT1pDNN20 = 0.99995
    },
    "CONTROL VARIABLES":  [ "NJ", "NB" ],       # X and Y control variables to define regions
    "TRANSFER VARIABLES": [ "HT", "DNN" ],  # transformed variables
    "GROUPS": [ "TTBB", "TTNOBB" ],         # MC samples used in ABCDnn training
    "MINOR BKG": [ "TTH", "TOP", "EWK" ],   # Minor backgrounds to include with ABCDnn in SR
    "SYSTEMATICS": [ "ABCDNNCLOSURE", "EXTABCDSYST", "EXTABCDSTAT", "EXTABCDCLOSURE" ],
  },
  "HISTS": {
    "LUMISCALE": 1,         # scale the luminosity multiplicatively in templates
    "REBIN": -1,            # rebin histograms to have this number of bins
    "TTHFSF": 4.7/3.9,      # from TOP-18-002 (v34), set to 1 if tt heavy flavor scaling not used
    "TTLFSF": -1.,          # if ttLFsf -1, compute automatically using ttHFsf, else set manually
    "MIN BKG YIELD": 0.015, # minimum yield threshold for a bkg group to be included in combine analysis ( default = 0.015 )
    "MAX BKG ERROR": 0.50   # maximum uncertainty threshold for a bkg group to be included in combine analysis ( default = 0.50 )
  },
  "MODIFY BINNING": {
    "STAT THRESHOLD": 1.0,      # the ratio of yield error to yield must be below this value per bin ( default = 0.3 )
    "MIN MERGE": 1,             # merge at least this number of bins
    "THRESHOLD BB": 0.05 ,      # total bkg statistical uncertainty threshold to assign bin-by-bin nuisances  ( default = 0.05 )
    "SMOOTHING ALGO": "lowess", # smoothing algorithm to use
    "LOWESS": 0.33,             # relative proportion of neighboring datapoints to consider during smoothing 
    "REMOVE SYST FROM YIELD": [ # list of systematics to exclude from yield calculation
      "HDAMP", "UE", 
      "NJET", "NJETSF", "PSWGT", "BTAG"
    ],
  },
  "COMBINE": {
    "BACKGROUNDS": [ "TTH", "EWK", "TTBB", "TOP", "QCD", "TTNOBB" ], 
    "DATA": [ "data_obs" ],
    "SIGNALS": [ "TTTW", "TTTJ" ],
    "FITS": { # arguments used with Combine -M MultiDimFit
      "ARGS": [
        "--cminDefaultMinimizerStrategy=1",
        "--setCrossingTolerance=0.001",   # default is 0.0001
        "--setRobustFitTolerance=1000",   # default is 0.1, setting higher to account for poor EDM initial state
        "--stepSize=0.01",                 # default is 0.2
        "--robustFit=1",
        "--rMin -33",
        "--rMax 33",
        #"--robustHesse=1",
        #"--freezeParameter TOPPTLOWESS",
        #"--freezeParameter ISRTOPLOWESS,JECFLAVORQCDLOWESS,MURFTTBARLOWESS,HOTCLOSURELOWESS16APV,", # 2016APV freeze
        #"--freezeParameter ISRTOPLOWESS,JECFLAVORQCDLOWESS,MURFTTBARLOWESS,FSRTTBARLOWESS,ISRTTBARLOWESS", # 2016 freeze
        "--expectSignal=1",
        "-t -1",
        "-m 125", # higgs mass, doesn't really matter for three top
      ]
    },
    "SIGNIFICANCE": { # arguments used with Combine -M Significance
      "ARGS": [
        "--cminDefaultMinimizerStrategy=1",
        "--expectSignal=1",
        "-t -1",
        "-m 125"
      ]
    },
    "LIMITS": { # arguments used with Combine -M AsymptoticLimits
      "ARGS": [
        "--cminDefaultMinimizerStrategy=0",
        "--run=blind",
      ]
    }
  }
}


# shape systematic uncertainty sources
systematics = {
  "MC": {  # Include, Symmetrize, Smooth
    "pileup": ( True, False, False ), 
    "prefire": ( True, False, False ),
    "pileupJetID": ( True, False, False ),
    "trigeff": ( False, False, False ),   
    "muRFcorrd": ( True, False, True ),
    "muR": ( True, False, True ),
    "muF": ( True, False, True ),
    "isr": ( True, False, True ),
    "fsr": ( True, False, True ),
    "hotstat": ( True, False, False ),
    "hotcspur": ( True, False, False ),
    "hotclosure": ( True, False, False ),
    "LF": ( True, False, False ),
    "lfstats1": ( True, False, False ),
    "lfstats2": ( True, False, False ),
    "HF": ( True, False, False ),
    "hfstats1": ( True, False, False ),
    "hfstats2": ( True, False, False ),
    "cferr1": ( True, False, False ),
    "cferr2": ( True, False, False ),
    "toppt": ( True, False, False ),
    "ABCDNNSAMPLE": ( False, False, False ),     
    "ABCDNNMODEL": ( False, False, False ),
    "ABCDNNCLOSURE": ( True, False, False ),
    "JER": ( True, False, True ),
    "JEC": ( True, False, True ), # calls from REDUCED JEC list
    "HD": ( False, False, False ), 
    "UE": ( False, False, False )
  },
  "REDUCED JEC": {
    "Total": False,             # use either Total or FlavorQCD, RelativeBal, RelativeSampel_Era, HF, HF_Era, BBEC1, BBEC1_Era, EC2, EC2_Era, Absolute, Absolute_Era
    "FlavorQCD": True,          # use either FlavorQCD or FlavorPureGluon/Quark/Charm/Bottom (breakdown)
    "FlavorPureGluon": False,
    "FlavorPureQuark": False,
    "FlavorPureCharm": False,
    "FlavorPureBottom": False,
    "RelativeBal": True,
    "RelativeSample_Era": True,
    "HF": True,
    "HF_Era": True,
    "BBEC1": True,
    "BBEC1_Era": True,
    "EC2": True,
    "EC2_Era": True,
    "Absolute": True,
    "Absolute_Era": True
  },
  "PS BREAKDOWN": {
    "isr": True,             # use either ISR or ISR breakdown into 8 components
    "fsr": True,             # use either FSR or FSR breakdown into 8 components
    "fsrG2GGmuR": False,
    "fsrG2QQmuR": False,
    "fsrQ2QGmuR": False,
    "fsrX2XGmuR": False,
    "fsrG2GGcNS": False,
    "fsrG2QQcNS": False,
    "fsrQ2QGcNS": False,
    "fsrX2XGcNS": False,
    "isrG2GGmuR": False,
    "isrG2QQmuR": False,
    "isrQ2QGmuR": False,
    "isrX2XGmuR": False,
    "isrG2GGcNS": False,
    "isrG2QQcNS": False,
    "isrQ2QGcNS": False,
    "isrX2XGcNS": False
  },
  "LUMI": { # uncorrelated
    "16APV": 1.007,
    "16": 1.007,
    "17": 1.020,
    "18": 1.015
  },
  "LUMI_RUN2": { # Full Run2 correlated
    "16APV": 1.004,
    "16": 1.004,
    "17": 1.009,
    "18": 1.020
  },
  "LUMI_17_18": { # 2017 and 2018 correlated
    "16APV": 1.00,
    "16": 1.00,
    "17": 1.006,
    "18": 1.002
  },
  "TRIG": {
    "E": { year: 1.03 for year in years }, 
    "M": { year: 1.02 for year in years },
  },
  "ID": {
    "E": { year: 1.015 for year in years },
    "M": { year: 1.010 for year in years }
  },
  "ISO": {
    "E": { year: 1.025 for year in years },
    "M": { year: 1.025 for year in years }
  },
  "XSEC": {
    "TTBAR": [ 0.91, 1.11 ], # hDamp uncertainty of +10/-7% added in quadrature with x-sec uncertainty of +4.8/-5.5%
    "TTH": 1.20,             # 15APR21 4tops meeting agreement
    "TOP": 1.04,             # aligning with 50% ttV, ttH and tt+xy uncertainties from OSDL and SSDL 4T analyses
    "EWK": 1.038             # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV scale and pdf added in quadrature 
  },
  # all of the Extended ABCD uncertainties calculated using specific analysis region (i.e. nJ = {4,5,6+} and nB = {2,3+} ), make sure using corresponding uncertainty value for given analysis regions
  "EXTABCDSYST": {
    "16APV": 1.084,  # nJ7pnB3p = 1.050, nJ5pnB2p = 1.015, nJ7pnB3pnHOT1p = 1.084
    "16": 1.081,     # nJ7pnB3p = 1.048, nJ5pnB2p = 1.014, nJ7pnB3pnHOT1p = 1.081
    "17": 1.054,     # nJ7pnB3p = 1.031, nJ5pnB2p = 1.010, nJ7pnB3pnHOT1p = 1.054
    "18": 1.044,     # nJ7pnB3p = 1.026, nJ5pnB2p = 1.008, nJ7pnB3pnHOT1p = 1.044
  },
  "EXTABCDSTAT": {
    "16APV": 1.041,  # nJ7pnB3p = 1.029, nJ5pnB2p = 1.005, nJ7pnB3pnHOT1p = 1.041
    "16": 1.042,     # nJ7pnB3p = 1.029, nJ5pnB2p = 1.004, nJ7pnB3pnHOT1p = 1.042
    "17": 1.029,     # nJ7pnB3p = 1.018, nJ5pnB2p = 1.003, nJ7pnB3pnHOT1p = 1.029
    "18": 1.023,     # nJ7pnB3p = 1.015, nJ5pnB2p = 1.002, nJ7pnB3pnHOT1p = 1.023
  },
  "EXTABCDCLOSURE": {
    "16APV": 1.016,  # nJ6nB2 = 1.070, nJ6nB1 = 1.040, nJ7nB2nHOT1p = 1.016
    "16": 1.061,     # nJ6nB2 = 1.009, nJ6nB1 = 1.060, nJ7nB2nHOT1p = 1.061
    "17": 1.009,     # nJ6nB2 = 1.025, nJ6nB1 = 1.042, nJ7nB2nHOT1p = 1.009
    "18": 1.047      # nJ6nB2 = 1.023, nJ6nB1 = 1.042, nJ7nB2nHOT1p = 1.047
  },
  "PILEUP": 1.046,
  "TTHF": { year: 1.04 for year in years },
  "HDAMP": 1.085,
  "MUR SF": { 
    "16APV": { "DN": 1.0781, "UP": 0.9218 }, 
    "16":    { "DN": 1.0740, "UP": 0.9253 },
    "17":    { "DN": 1.0736, "UP": 0.9255 },
    "18":    { "DN": 1.0755, "UP": 0.9237 }
  },
  "MUF SF": { 
    "16APV": { "DN": 1.0232, "UP": 0.9734 }, 
    "16":    { "DN": 1.0219, "UP": 0.9749 },
    "17":    { "DN": 1.0222, "UP": 0.9746 },
    "18":    { "DN": 1.0228, "UP": 0.9738 }
  },
  "MURFCORRD SF": { 
    "16APV": { "DN": 1.1034, "UP": 0.8989 }, 
    "16":    { "DN": 1.0979, "UP": 0.9036 },
    "17":    { "DN": 1.0976, "UP": 0.9035 },
    "18":    { "DN": 1.1003, "UP": 0.9010 }
  },
  "ISR SF": {
    "SIG": {
      "16APV": { "DN": 0.9995, "UP": 1.1649 },
      "16":    { "DN": 0.9925, "UP": 1.1100 },
      "17":    { "DN": 1.0018, "UP": 1.1502 },
      "18":    { "DN": 0.9989, "UP": 1.1318 }
    },
    "BKG": {
      "16APV": { "DN": 1.0230, "UP": 1.2265 },
      "16":    { "DN": 1.0179, "UP": 1.1868 },
      "17":    { "DN": 1.0142, "UP": 1.1876 },
      "18":    { "DN": 1.0189, "UP": 1.1999 }
    }
  },
  "FSR SF": {
    "SIG": {
      "16APV": { "DN": 0.9994, "UP": 0.9997 },
      "16":    { "DN": 1.0023, "UP": 1.0138 },
      "17":    { "DN": 0.9996, "UP": 1.0050 },
      "18":    { "DN": 0.9994, "UP": 1.0048 }
    },
    "BKG": {
      "16APV": { "DN": 0.9865, "UP": 0.9813 },
      "16":    { "DN": 0.9837, "UP": 0.9698 },
      "17":    { "DN": 0.9869, "UP": 0.9788 },
      "18":    { "DN": 0.9895, "UP": 0.9869 }
    }
  },
}

# binning configuration for the templates

region_prefix = {
  "SR": "templates_SR",
  "VR": "templates_VR",
  "TTCR": "ttbar",
  "WJCR": "wjets",
  "BASELINE": "baseline",
  "ABCDNN": "abcdnn"
}

hist_bins = {
  "SR": {
    "LEPTON": [ "E", "M" ],
    "NHOT": [ "0", "1p" ],
    "NT": [ "0p" ],
    "NW": [ "0p" ],
    "NB": [ "2", "3p" ],
    "NJ": [ "5", "6", "7p" ]
  },
  "EXCLUDE": { # these regions get excluded in Combine
    "LEPTON": [ "E", "M" ],
    "NHOT": [ "0" ],
    "NT": [ "0p" ],
    "NW": [ "0p" ],
    "NB": [ "2" ],
    "NJ": [ "4" ]
  },
  "VR": {
    "LEPTON": [ "E", "M" ],
    "NHOT": [ "0p" ],
    "NT": [ "0p" ],
    "NW": [ "0p" ],
    "NB": [ "0", "1" ],
    "NJ": [ "4", "5", "6" ]
  },
  "BASELINE": {
    "LEPTON": [ "E", "M" ],
    "NHOT": [ "0p" ],
    "NT": [ "0p" ],
    "NW": [ "0p" ],
    "NB": [ "2p" ],
    "NJ": [ "4p" ]
  },
  "ABCDNN": { # edit these based on ABCDnn training signal region
    "LEPTON": [ "E", "M" ],
    "NHOT": [ "1p" ],
    "NT": [ "0p" ],
    "NW": [ "0p" ],
    "NB": [ "3p" ],
    "NJ": [ "7p" ] 
  }
}

event_cuts = {
  "pt_electron": 20,  # BASELINE = 20,  S1/2 = 20
  "pt_muon": 20,      # BASELINE = 20,  S1/2 = 20
  "met": 20,          # BASELINE = 20,  S1/2 = 20 
  "mtW": 0,           # BASELINE = 0,   S1/2 = 0
  "met+mtW": 70.,     # BASELINE = 0,   S1 = 0, S2 = 70
  "ht": 390,          # BASELINE = 350, S1/2 = 390
  "mindr_lj": 0.2,    # BASELINE = 0,   S1/2 = 0.2
  "dnn": 0.2          # BASELINE = 0,   S1 = 0, S2 = 0.2
}

base_cut = "DataPastTriggerX == 1 && MCPastTriggerX == 1 "
base_cut += " && ( ( leptonPt_MultiLepCalc > {} && isElectron == 1 ) || ( leptonPt_MultiLepCalc > {} && isMuon == 1 ) )".format( event_cuts[ "pt_electron" ], event_cuts[ "pt_muon" ] )
base_cut += " && AK4HT > {} && corr_met_MultiLepCalc > {} && MT_lepMet > {} && minDR_lepJet > {}".format( event_cuts[ "ht" ], event_cuts[ "met" ], event_cuts[ "mtW" ], event_cuts[ "mindr_lj" ] )
base_cut += " && ( corr_met_MultiLepCalc + 0.667 * MT_lepMet ) > {}".format( event_cuts[ "met+mtW" ] ) # targetting QCD in MTW,MET phase space, values determined against tttW+tttj
base_cut += " && DNN_1to40_3t > {}".format( event_cuts[ "dnn" ] )
mc_weight = "triggerXSF * triggerSF * pileupWeight * pileupJetIDWeight * lepIdSF * EGammaGsfSF * isoSF * L1NonPrefiringProb_CommonCalc"
mc_weight += " * ( MCWeight_MultiLepCalc / abs( MCWeight_MultiLepCalc ) )"

# plotting configuration
def bins( min_, max_, nbins_ ):
  return np.linspace( min_, max_, nbins_ ).tolist()

plot_params = {
  "VARIABLES": {
    "LEPPT": ( "leptonPt_MultiLepCalc", bins( 0, 600, 31 ), "Lepton p_{T} [GeV]" ),
    "LEPETA": ( "leptonEta_MultiLepCalc", bins( -2.4, 2.4, 17 ), "Lepton #eta" ),
    "MINDR_LJ": ( "minDR_lepJet", bins( 0, 3, 16 ), "min #DeltaR(l,jet)" ),
    "JETPT": ( "theJetPt_JetSubCalc_PtOrdered", bins( 0, 900, 31 ), "AK4 Jet p_{T} [GeV]" ),
    "JETETA": ( "theJetEta_JetSubCalc_PtOrdered", bins( -2.4, 2.4, 17 ), "AK4 Jet #eta" ),
    "MET": ( "corr_met_MultiLepCalc", bins( 0, 600, 31 ), "E_{T}^{miss} [GeV]" ),
    "HT": ( "AK4HT", bins( 0, 2000, 41 ), "H_{T} [GeV]" ),
    "NJETS": ( "NJets_JetSubCalc", bins( 0, 13, 14 ), "AK4 Jet Multiplicity" ),
    "NPU": ( "NJetsPU_JetSubCalc", bins( 0, 6, 7 ), "Pileup (T) Jet Multiplicity" ),
    "NFWD": ( "NJetsForward_JetSubCalc", bins( 0, 3, 4 ), "Forward Jet Multiplicity" ),
    "NBJETS": ( "NJetsCSV_JetSubCalc", bins( 0, 6, 7 ), "Medium DeepJet Multiplicity" ),
    "NWJETS": ( "NJetsWtagged", bins( 0, 6, 7 ), "W-tagged Jet Multiplicity" ),
    "NTJETS": ( "NJetsTtagged", bins( 0, 4, 5 ), "t-tagged Jet Multiplicity" ),
    "DNN": ( "DNN_1to40_3t", bins( 0, 1, 41 ), "DNN" ),
    "DNN3": ( "DNN_1to3_3t", bins( 0, 1, 41 ), "DNN (1-3)" ),
    "DNN5": ( "DNN_1to5_3t", bins( 0, 1, 41 ), "DNN (1-5)" ),
    "DNN10": ( "DNN_1to10_3t", bins( 0, 1, 41 ), "DNN (1-10)" ),
    "DNN20": ( "DNN_1to20_3t", bins( 0, 1, 41 ), "DNN (1-20)" ),
    "DNN30": ( "DNN_1to30_3t", bins( 0, 1, 41 ), "DNN (1-30)" ),
    "DNN40": ( "DNN_1to40_3t", bins( 0, 1, 41 ), "DNN (1-40)" ),
    "ST": ( "AK4HTpMETpLepPt", bins( 0, 4000, 41 ), "S_T [GeV]"  ),
    "MINM_LB": ( "minMleppBjet", bins( 0, 1000, 41 ), "min[M(l,b)] [GeV]" ),
    "M_MINBBDR": ( "mass_minBBdr", bins( 0, 1400, 41 ), "M(b,b) with min(#DeltaR(b,b)) [GeV]" ),
    "DR_LB": ( "deltaR_lepBJet_maxpt", bins( 0, 6.0, 21 ), "#DeltaR(l,b) with max[p_{T}(l,b)]" ),
    "DR_LBB": ( "lepDR_minBBdr", bins( -1, 10, 21 ), "#DeltaR(l,bb) with min[#DeltaR(b,b)]" ),
    "CENTRALITY": ( "centrality", bins( 0, 1.0, 21 ), "Centrality" ),
    "DE_BB": ( "deltaEta_maxBB", bins( -6, 11, 21 ), "max[#Delta#eta(b,b)]" ),
    "PT_CSV": ( "aveCSVpt", bins( -0.3, 1.1, 41 ), "ave(p_{T} weighted CSVv2) [GeV]" ),
    "DR_BB": ( "aveBBdr", bins( 0, 6.0, 21 ), "ave[#DeltaR(b,b)]" ),
    "FW0": ( "FW_momentum_0", bins( 0, 1, 21 ), "0^{th} FW moment [GeV]" ),
    "FW1": ( "FW_momentum_1", bins( 0, 1, 21 ), "1^{st} FW moment [GeV]" ),
    "FW2": ( "FW_momentum_2", bins( 0, 1, 21 ), "2^{nd} FW moment [GeV]" ),
    "FW3": ( "FW_momentum_3", bins( 0, 1, 21 ), "3^{rd} FW moment [GeV]" ),
    "FW4": ( "FW_momentum_4", bins( 0, 1, 21 ), "4^{th} FW moment [GeV]" ),
    "FW5": ( "FW_momentum_5", bins( 0, 1, 21 ), "5^{th} FW moment [GeV]" ),
    "FW6": ( "FW_momentum_6", bins( 0, 1, 21 ), "6^{th} FW moment [GeV]" ),
    "M_JJJ": ( "mass_maxJJJpt", bins( 0, 3000, 41 ), "M(jjj) with max[p_{T}(jjj)] [GeV]" ),
    "PT_B1": ( "BJetLeadPt", bins( 0, 500, 51 ), "p_{T}{b_{1}) [GeV]" ),
    "MINDR_BB": ( "deltaR_minBB", bins( 0, 6, 21 ), "min[#DeltaR(b,b)]" ),
    "MINDR_LB": ( "minDR_lepBJet", bins( 0, 6, 21 ), "min[#DeltaR(l,b)]" ),
    "MT_LMET": ( "MT_lepMet", bins( 0, 250, 41 ), "M_{T}(l,#slash{E}_{T}) [GeV]" ),
    "HEMIOUT": ( "hemiout", bins( 0, 2000, 41 ), "Hemiout [GeV]" ),
    "M_LJ0": ( "mass_lepJets0", bins( 0, 2000, 41 ), "M(l,j_{1}) [GeV]" ),
    "M_LJ1": ( "mass_lepJets1", bins( 0, 2000, 41 ), "M(l,j_{2}) [GeV]" ),
    "M_LJ2": ( "mass_lepJets2", bins( 0, 2000, 41 ), "M(l,j_{3}) [GeV]" ),
    "MT2BB": ( "MT2bb", bins( 0, 400, 41 ), "MT2bb [GeV]" ),
    "M_LB0": ( "mass_lepBJet0", bins( 0, 1800, 41 ), "M(l,b_{1}) [GeV]" ),
    "M_MINDR_LB": ( "mass_lepBJet_mindr", bins( 0, 1000, 21 ), "M(l,b) with min[#DeltaR(l,b)] [GeV]" ),
    "PT_J1": ( "theJetLeadPt", bins( 0, 500, 51 ), "p_{T}(j_{1}) [GeV]" ),
    "PT_J2": ( "secondJetPt", bins( 0, 500, 51 ), "2^{nd} Jet p_{T} [GeV]" ),
    "PT_J5": ( "fifthJetPt", bins( 0, 300, 31 ), "5^{th} Jet p_{T} [GeV]" ),
    "PT_J6": ( "sixthJetPt", bins( 0, 200, 21 ), "6^{th} Jet p_{T} [GeV]" ),
    "J5PT": ( "PtFifthJet", bins( 0, 800, 41 ), "5^{th} Jet p_{T} [GeV]" ),
    "M_MINLLDR": ( "mass_minLLdr", bins( 0, 600, 41 ), "M(j,j) with min[#DeltaR(j,j)], j #neq b [GeV]" ),
    "M_MAXBB": ( "mass_maxBBmass", bins( 0, 2000, 41 ), "max[M(b,b)] [GeV]" ),
    "DR_MINLJ": ( "deltaR_lepJetInMinMljet", bins( 0, 4.5, 21 ), "#DeltaR(l,j) with min M(l, j)" ),
    "DP_MINLJ": ( "deltaPhi_lepJetInMinMljet", bins( -4, 4, 21 ), "#Delta #Phi(l,j) with min M(l, j)" ),
    "DR_MINLB": ( "deltaR_lepbJetInMinMlb", bins( 0, 4.5, 21 ), "#DeltaR(l,b) with min M(l, b)" ),
    "DP_MINLB": ( "deltaPhi_lepbJetInMinMlb", bins( -11, 5, 21 ), "#Delta #Phi(l,b) with min M(l, b)" ),
    "M_JW": ( "M_allJet_W", bins( 0, 7000, 41 ), "M(J_{all}, W_{lep}) [GeV]" ),
    "HT_B": ( "HT_bjets", bins( 0, 1800, 41 ), "HT(bjets) [GeV]" ),
    "RATIO_HT": ( "ratio_HTdHT4leadjets", bins( 1, 2.1, 21 ),  "HT/HT(4 leading jets)" ),
    "CSV_J3": ( "csvJet3", bins( 0, 1, 41 ), "DeepCSV(3rdPtJet)" ),
    "CSV_J4": ( "csvJet4", bins( 0, 1, 41 ), "DeepCSV(4thPtJet)" ),
    "CSVB_1": ( "firstcsvb_bb", bins( 0, 1, 41 ), "DeepJet (1st)" ),
    "CSVB_2": ( "secondcsvb_bb", bins( 0, 1, 41 ), "DeepJet (2nd)" ),
    "CSVB_3": ( "thirdcsvb_bb", bins( 0, 1, 41 ), "DeepJet (3rd)" ),
    "CSVB_4": ( "fourthcsvb_bb", bins( 0, 1, 41 ), "DeepJet (4th)" ),
    "HT_2M": ( "HT_2m", bins( 0, 3000, 41 ), "H_{T}(b_{1},b_{2}) [GeV]" ),
    "SPHERICITY": ( "Sphericity", bins( 0, 1.0, 21 ), "Sphericity" ),
    "APLANARITY": ( "Aplanarity", bins( 0, 0.5, 21 ), "Aplanarity" ),
    "BDT3J_1": ( "BDTtrijet1", bins( -1, 1, 41 ), "trijet1 discriminator" ),
    "BDT3J_2": ( "BDTtrijet2", bins( -1, 1, 41 ), "trijet2 discriminator" ),
    "BDT3J_3": ( "BDTtrijet3", bins( -1, 1, 41 ), "trijet3 discriminator" ),
    "BDT3J_4": ( "BDTtrijet4", bins( -1, 1, 41 ), "trijet4 discriminator" ),
    "NHOT": ( "NresolvedTops1pFake", bins( 0, 3, 4 ), "Resolved t-tagged jet multiplicity" ),
    "HOT1_MASS": ( "HOTGoodTrijet1_mass", bins( 0, 250, 41 ), "HOTGoodTrijet1_mass [GeV]" ),
    "HOT1_DJMASS": ( "HOTGoodTrijet1_dijetmass", bins( 0, 250, 41 ), "HOTGoodTrijet1_dijetmass [GeV]" ),
    "HOT1_PTRATIO": ( "HOTGoodTrijet1_pTratio", bins( 0, 1, 41 ), "HOTGoodTrijet1_pTratio" ),
    "HOT1_DRJJ": ( "HOTGoodTrijet1_dRtridijet", bins( 0, 4, 21 ), "HOTGoodTrijet1_dRtridijet" ),
    "HOT1_CSVNOJJ": ( "HOTGoodTrijet1_csvJetnotdijet", bins( -2.2, 1.2, 41 ), "HOTGoodTrijet1_csvJetnotdijet" ),
    "HOT1_DRNOJJ": ( "HOTGoodTrijet1_dRtrijetJetnotdijet", bins( 0, 4, 21 ), "HOTGoodTrijet1_dRtrijetJetnotdijet" ),
    "HOT2_MASS": ( "HOTGoodTrijet2_mass", bins( 0, 300, 41 ), "HOTGoodTrijet2_mass [GeV]" ),
    "HOT2_DJMASS": ( "HOTGoodTrijet2_dijetmass", bins( 0, 200, 41 ), "HOTGoodTrijet2_dijetmass [GeV]" ),
    "HOT2_PTRATIO": ( "HOTGoodTrijet2_pTratio", bins( 0, 1, 41 ), "HOTGoodTrijet2_pTratio" ),
    "HOT2_DRJJ": ( "HOTGoodTrijet2_dRtridijet", bins( 0, 4, 21 ), "HOTGoodTrijet2_dRtridijet" ),
    "HOT2_CSVNOJJ": ( "HOTGoodTrijet2_csvJetnotdijet", bins( 0, 1, 41 ), "HOTGoodTrijet2_csvJetnotdijet" ),
    "HOT2_DRNOJJ": ( "HOTGoodTrijet2_dRtrijetJetnotdijet", bins( 0, 4, 21 ), "HOTGoodTrijet2_dRtrijetJetnotdijet" ),
  }
}

