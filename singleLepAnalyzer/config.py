import numpy as np

years = [ "16", "17", "18" ]

postfix = "deepJetV1"
inputDir = { year: "/isilon/hadoop/store/user/dali/FWLJMET106XUL_1lep20{}_3t_{}_step3/".format( year, postfix ) for year in years }

# target lumis in 1/pb for each year
lumi = {
  "16": 35867., 
  "17": 41530.,
  "18": 59970.
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
    "JET SHIFTS": False,  # JEC/JER shifts for shape 
    "HDAMP": False,       # hdamp systematics
    "UE": False,          # ue systematics
    "PDF": True,          # pdf systematics
    "SYSTEMATICS": True,  # include other systematics defined in systematics[ "MC" ]
    "FINAL ANALYSIS": False
  },
  "HISTS": {
    "RENORM PDF": True, # renormalize the PDF weights
    "SUMMARY": False, # produce summary templates
    "SCALE SIGNAL 1PB": False, # Scale the signal xsec to 1 PB for future studies
  },
  "MODIFY BINNING": {
    "BLIND": True,
    "PDF": True,                   # add PDF systematic uncertainty
    "CR SYST": False,              # add systematic uncertainty to control region
    "SHAPE SYST": True,            # add systematic uncertainty shapes
    "SHAPE STAT": True,            # add statistical uncertainty shapes
    "MURF SHAPES": True,
    "PS WEIGHTS": True,            # Construct Parton Shower weights
    "NORM THEORY SIG SYST": True,  # normalize the theoretical systematics (MURF, PS WEIGHTS, PDF) for the signal
    "NORM THEORY BKG SYST": False, # normalize the theoretical systematics (MURF, PS WEIGHTS, PDF) for the background
    "SYMM SMOOTHING": True,
    "SYMM TOP PT": True,
    "SYMM HOTCLOSURE": True,
    "SCALE SIGNAL XSEC": False,
    "ADD SHAPE SYST YIELD": True,
    "SMOOTH": True,
    "UNCORRELATE YEARS": True,
    "TRIGGER EFFICIENCY": True,
  }
}
# non-boolean parameters used in creating templates
params = {
  "GENERAL": {
    "ZERO": 1e-12,      # default non-zero value for zero to prevent division by zero
    "REBIN": -1,        # rebin histogram binning, use -1 to keep original binning
    "PDF RANGE": 100,   # PDF range
  },
  "HISTS": {
    "LUMISCALE": 1,         # scale the luminosity multiplicatively in templates
    "REBIN": -1,            # rebin histograms to have this number of bins
    "TTHFSF": 4.7/3.9,      # from TOP-18-002 (v34), set to 1 if tt heavy flavor scaling not used
    "TTLFSF": -1.,          # if ttLFsf -1, compute automatically using ttHFsf, else set manually
    "MIN BKG YIELD": 0.015, # minimum yield threshold for a bkg group to be included in combine analysis 
    "MAX BKG ERROR": 0.50   # maximum uncertainty threshold for a bkg group to be included in combine analysis
  },
  "MODIFY BINNING": {
    "STAT THRESHOLD": 0.3,      # the ratio of yield error to yield must be below this value per bin
    "MIN MERGE": 1,             # merge at least this number of bins
    "THRESHOLD BB": 0.05,       # stat shape uncertainty threshold for inclusion
    "SMOOTHING ALGO": "lowess", # smoothing algorithm to use
    "REMOVE SYST FROM YIELD": [ # list of systematics to exclude from yield calculation
      "HDAMP", "UE", 
      "NJET", "NJETSF", "PSWGT", "BTAG"
    ],
    "EXCLUDE SMOOTH": [
      "TOPPT", "HT" 
    ]
  },
  "COMBINE": {
    "BACKGROUNDS": [ "TTNOBB", "TTBB", "TOP", "EWK", "QCD" ], # TTH?
    "DATA NAME": "DAT",
    
  }
}

region_prefix = {
  "SR": "templates",
  "VR": "templates",
  "TTCR": "ttbar",
  "WJCR": "wjets",
  "BASELINE": "baseline"
}

# systematic uncertainty sources
systematics = {
  "MC": [ 
    "pileup", #"trigeff",
    "muRFcorrd", "muR", "muF", "isr", "fsr", 
    "hotstat", "hotcspur", "hotclosure", 
    "LF", "LFstat1", "LFstat2", "HF", "HFstat1", "HFstat2", 
    "CFerr1", "CFerr2",
    #"toppt", "ht",
    #"JER", "JEC"
  ],
  "LUMI": {
    "17": 0.023,
    "18": 0.025
  },
  "TRIG": {
    "E": 0.0, 
    "M": 0.0
  },
  "ID": {
    "E": 0.03,
    "M": 0.03
  },
  "ISO": {
    "E": 0.0,
    "M": 0.0
  },
  "XSEC": {
    "TTBAR": 0.0515,
    "TTH": 0.20,
    "TOP": 0.04,
    "EWK": 0.038
  },
  "TTHF": 0.13,
  "HDAMP": 0.085
}

# binning configuration for the templates
hist_bins = {
  "SR": {
    "LEPTON": [ "E", "M" ],
    "NHOT": [ "0", "1", "2p" ],
    "NT": [ "0p" ],
    "NW": [ "0", "1p" ],
    "NB": [ "2", "3p" ],
    "NJ": [ "5", "6", "7p" ]
  },
  "VR": {
    "LEPTON": [ "E", "M" ],
    "NHOT": [ "0p" ],
    "NT": [ "0p" ],
    "NW": [ "0p" ],
    "NB": [ "2", "3p" ],
    "NJ": [ "5", "6" ]
  },
  "BASELINE": {
    "LEPTON": [ "E", "M" ],
    "NHOT": [ "0p" ],
    "NT": [ "0p" ],
    "NW": [ "0p" ],
    "NB": [ "2p" ],
    "NJ": [ "5p" ]
  }
}

event_cuts = {
  "pt_electron": 20,
  "pt_muon": 20,
  "pt_jet": 20,
  "met": 20,
  "mt": 0,
  "ht": 350
}

base_cut = "DataPastTriggerX == 1 && MCPastTriggerX == 1 "
base_cut += " && ( ( leptonPt_MultiLepCalc > {} && isElectron == 1 ) || ( leptonPt_MultiLepCalc > {} && isMuon == 1 ) )".format( event_cuts[ "pt_electron" ], event_cuts[ "pt_muon" ] )
base_cut += " && AK4HT > {} && corr_met_MultiLepCalc > {} && MT_lepMet > {} && minDR_lepJet > 0.4".format( event_cuts[ "ht" ], event_cuts[ "met" ], event_cuts[ "mt" ] )
mc_weight = "triggerXSF * pileupWeight * lepIdSF * EGammaGsfSF * isoSF * L1NonPrefiringProb_CommonCalc"
mc_weight += " * ( MCWeight_MultiLepCalc / abs( MCWeight_MultiLepCalc ) )"
mc_weight += " * btagDeepJetWeight * btagDeepJet2DWeight_HTnj"

# plotting configuration
def bins( min_, max_, nbins_ ):
  return np.linspace( min_, max_, nbins_ ).tolist()

plot_params = {
  "PLOTTING": {
    "ONE BAND ERR": True, # combine the various uncertainty bands into one color
    "SMOOTHING": True,
    "CR SYST": False,
    "SCALE SIGNAL": 10, # scale the signal yield to be more visible, put -1 for auto-scaling
  },
  "VARIABLES": {
    "LEPPT": ( "leptonPt_MultiLepCalc", bins( 0, 600, 121 ), ";Lepton p_{T} [GeV]" ),
    "LEPETA": ( "leptonEta_MultiLepCalc", bins( -2.4, 2.4, 49 ), ";Lepton #eta" ),
    "JETPT": ( "theJetPt_JetSubCalc_PtOrdered", bins( 0, 1500, 51 ), ";AK4 Jet p_{T} [GeV]" ),
    "JETETA": ( "theJetEta_JetSubCalc_PtOrdered", bins( -2.4, 2.4, 49 ), ";AK4 Jet #eta" ),
    "MET": ( "corr_met_MultiLepCalc", bins( 0, 1000, 51 ), ";p_{T}^{miss} [GeV]" ),
    "HT": ( "AK4HT", bins( 0, 3000, 121 ), ";H_{T} [GeV]" ),
    "NJETS": ( "NJets_JetSubCalc", bins( 0, 15, 16 ), ";AK4 Jet Multiplicity" ),
    "NBJETS": ( "NJetsCSV_JetSubCalc", bins( 0, 10, 11 ), ";Medium DeepJet Multiplicity" ),
    "NWJETS": ( "NJetsWtagged", bins( 0, 6, 7 ), ";W-tagged Jet Multiplicity" ),
    "NTJETS": ( "NJetsTtagged", bins( 0, 4, 5 ), ";t-tagged Jet Multiplicity" ),
    "DNN_3t": ( "DNN_5j_1to50_S2B10", bins( 0, 1, 101 ), ";DNN_{1-50}" )
  }
}
