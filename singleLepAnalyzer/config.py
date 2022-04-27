import numpy as np

years = [ "16APV", "16", "17", "18" ]

postfix = "3t_deepJetV1"
inputDir = { year: "/isilon/hadoop/store/user/dali/FWLJMET106XUL_1lep20{}_{}_step3/".format( year, postfix ) for year in years }

# target lumis in 1/pb for each year
lumi = {
  "16APV": 19520., # from pdmv
  "16": 16810.,    # from pdmv
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
    "JET SHIFTS": False,  # JEC/JER shifts for shape 
    "HDAMP": False,       # hdamp systematics
    "UE": False,          # ue systematics
    "PDF": True,          # pdf systematics
    "SYSTEMATICS": True,  # include other systematics defined in systematics[ "MC" ]
    "ABCDNN": True,
    "FINAL ANALYSIS": False
  },
  "HISTS": {
    "RENORM PDF": True, # renormalize the PDF weights
    "SUMMARY": False,   # produce summary templates
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
    "SYMM SMOOTHING": False,
    "SYMM TOP PT": True,
    "SYMM HOTCLOSURE": True,
    "SCALE SIGNAL XSEC": False,
    "ADD SHAPE SYST YIELD": True,
    "SMOOTH": True,
    "UNCORRELATE YEARS": True,
    "TRIGGER EFFICIENCY": True,
  },
  "COMBINE": {
    "TTHF SYST": True,
    "PDF": True,
    "ABCDNN": True,
    "SMOOTH": True
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
    "TAG": "SR",
    "CONTROL VARIABLES":  [ "NJ", "NB" ],
    "TRANSFER VARIABLES": [ "HT", "DNN_3t" ],
    "GROUPS": [ "TTBB", "TTNOBB" ],
    "SYSTEMATICS": [ "ABCDNN", "MUR", "MUF", "MURFCORRD", "FSR", "ISR", "PDF" ]
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
    "BACKGROUNDS": [ "TTNOBB", "TTBB", "TOP", "EWK", "QCD", "TTH" ], 
    "DATA": [ "data_obs" ],
    "SIGNALS": [ "TTTW", "TTTJ" ],
    "MURF NORM": { 
      "TTNOBB": 1.36,
      "TTBB": 1.36,
      "TOP": 1.47,
      "EWK": 1.31,
      "QCD": 1.38
    },
    "ISR NORM": {
      "TTNOBB": 1.17,
      "TTBB": 1.15,
      "TOP": 1.16,
      "EWK": 1.00,
      "QCD": 1.11
    },
    "FSR NORM": {
      "TTNOBB": 1.33,
      "TTBB": 1.68,
      "TOP": 1.24,
      "EWK": 1.00,
      "QCD": 1.21
    },
    "PDF NORM": {
      "TTNOBB": 1.00,
      "TTBB": 1.00,
      "TOP": 1.20,
      "EWK": 1.00,
      "QCD": 1.01
    }
  }  
}

region_prefix = {
  "SR": "templates_SR",
  "VR": "templates_VR",
  "TTCR": "ttbar",
  "WJCR": "wjets",
  "BASELINE": "baseline",
  "ABCDNN": "acbdnn"
}

# systematic uncertainty sources
systematics = {
  "MC": {
    "pileup": True, 
    "trigeff": False,
    "muRFcorrd": True, 
    "muR": True, 
    "muF": True, 
    "isr": True, 
    "fsr": True, 
    "hotstat": True, 
    "hotcspur": True, 
    "hotclosure": True,
    "njet": False,
    "njetsf": False,
    "LF": True, 
    "lfstats1": True, 
    "lfstats2": True, 
    "HF": True, 
    "hfstats1": True, 
    "hfstats2": True, 
    "cferr1": True, 
    "cferr2": True,
    "jes": False,
    "toppt": True, 
    "ht": False,
    "ABCDNN": True,
    "JER": False, 
    "JEC": False,
    "HD": False,
    "UE": False
  },
  "LUMI": {
    "16APV": 1.012,
    "16": 1.012,
    "17": 1.023,
    "18": 1.025
  },
  "TRIG": {
    "E": 1.03, 
    "M": 1.03,
  },
  "ID": {
    "E": 1.015,
    "M": 1.010
  },
  "ISO": {
    "E": 1.025,
    "M": 1.025
  },
  "XSEC": {
    "TTBAR": [ 0.945, 1.048 ],
    "TTH": 1.20,
    "TOP": 1.04,
    "EWK": 1.038
  },
  "TTHF": 1.13,
  "HDAMP": 1.085,
  "ABCDNN": 1.10,
}

# binning configuration for the templates
hist_bins = {
  "SR": {
    "LEPTON": [ "E", "M" ],
    "NHOT": [ "0p" ],
    "NT": [ "0p" ],
    "NW": [ "0p" ],
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
  },
  "ABCDNN": { # edit these based on ABCDnn training signal region
    "LEPTON": [ "E", "M" ],
    "NHOT": [ "0p" ],
    "NT": [ "0p" ],
    "NW": [ "0p" ],
    "NB": [ "3p" ],
    "NJ": [ "7p" ] 
  }
}

event_cuts = {
  "pt_electron": 20,
  "pt_muon": 20,
  "pt_jet": 30,
  "met": 20,
  "mt": 0,
  "ht": 350
}

base_cut = "DataPastTriggerX == 1 && MCPastTriggerX == 1 "
base_cut += " && ( ( leptonPt_MultiLepCalc > {} && isElectron == 1 ) || ( leptonPt_MultiLepCalc > {} && isMuon == 1 ) )".format( event_cuts[ "pt_electron" ], event_cuts[ "pt_muon" ] )
base_cut += " && AK4HT > {} && corr_met_MultiLepCalc > {} && MT_lepMet > {} && minDR_lepJet > 0.4".format( event_cuts[ "ht" ], event_cuts[ "met" ], event_cuts[ "mt" ] )
mc_weight = "triggerXSF * pileupWeight * lepIdSF * EGammaGsfSF * isoSF"
mc_weight += " * ( MCWeight_MultiLepCalc / abs( MCWeight_MultiLepCalc ) )"
mc_weight += " * btagDeepJetWeight * btagDeepJet2DWeight_HTnj"

# plotting configuration
def bins( min_, max_, nbins_ ):
  return np.linspace( min_, max_, nbins_ ).tolist()

plot_params = {
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
    "DNN_3t": ( "DNN_5j_1to50_S2B10", bins( 0, 1, 101 ), "DNN_{1-50}" ),
  }
}
