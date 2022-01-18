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

# Branching ratios
BR = {
  "BW" : [0.0,0.50,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0],
  "TH" : [0.5,0.25,0.0,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0],
  "TZ" : [0.5,0.25,1.0,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]
}

# boolean options that need to be coordinated across template making
options = {
  "TEST": True,
  "JET SHIFTS": False, # JEC/JER shifts for shape 
  "HDAMP": False, 
  "UE": False,
  "PDF": True,
  "SYSTEMATICS": True
}

# systematic uncertainty sources
systematics = {
  "MC": [ 
    "pileup", "muRFcorrd", "muR", "muF", "isr", "fsr", 
    "hotstat", "hotcspur", "hotclosure", 
    "LF", "LFstat1", "LFstat2", "HF", "HFstat1", "HFstat2", 
    "CFerr1", "CFerr2",
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
  "TEMPLATES": {
    "LEPTON": [ "E", "M" ],
    "NHOT": [ "0", "1", "2p" ],
    "NT": [ "0p" ],
    "NW": [ "0", "1p" ],
    "NB": [ "2", "3p" ],
    "NJ": [ "5", "6", "7", "8p" ]
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

# use isTraining == 3 when running final analysis
base_cut = "isTraining == 2 && DataPastTriggerX == 1 && MCPastTriggerX == 1 "
base_cut += " && ( ( leptonPt_MultiLepCalc > {} && isElectron == 1 ) || ( leptonPt_MultiLepCalc > {} && isMuon == 1 ) )".format( event_cuts[ "pt_electron" ], event_cuts[ "pt_muon" ] )
base_cut += " && AK4HT > {} && corr_met_MultiLepCalc > {} && MT_lepMet > {} && minDR_lepJet > 0.4".format( event_cuts[ "ht" ], event_cuts[ "met" ], event_cuts[ "mt" ] )
mc_weight = "triggerXSF * pileupWeight * lepIdSF * EGammaGsfSF * isoSF * L1NonPrefiringProb_CommonCalc"
mc_weight += " * ( MCWeight_MultiLepCalc / abs( MCWeight_MultiLepCalc ) )"
mc_weight += " * btagDeepJetWeight * btagDeepJet2DWeight_HTnj"

# plotting configuration
def bins( min_, max_, nbins_ ):
  return np.linspace( min_, max_, nbins_ ).tolist()

plot_params = {
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
  "DNN_3t": ( "DNN_5j_1to50_S2B10", bins( 0, 1, 101 ), ";DNN_{1-50} 3t" )
}

ttHFsf = 4.7/3.9 # from TOP-18-002 (v34), set to 1 if no ttHFsf used
ttLFsf = -1      # if ttLFsf -1, computed automatically using ttHFsf, else set manually

pdf_range = 100

ratio_threshold = 0.015 # ratio beneath which process / total background a process will be exccluded
uncertainty_threshold = 0.5 # threshold beneath which a statistical uncertainty is excluded

zero = 1e-12
