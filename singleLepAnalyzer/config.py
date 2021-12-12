import numpy as np


lumi = { # 1/pb
  "16": 35867., 
  "17": 41530.,
  "18": 59970.
}

# binning configuration

bins = {
  "templates": {
    "lepton": [ "E", "M" ],
    "nHOT": [ "0", "1", "2p" ],
    "nT": [ "0p" ],
    "nW": [ "0", "1p" ],
    "nB": [ "2", "3p" ],
    "nJ": [ "5", "6", "7", "8p" ]
  },
  "baseline": {
    "lepton": [ "E", "M" ],
    "nHOT": [ "0p" ],
    "nT": [ "0p" ],
    "nW": [ "0p" ],
    "nB": [ "2p" ],
    "nJ": [ "5p" ]
  }
}

event_cuts = {
  "pt_electron": 20,
  "pt_muon": 20,
  "pt_jet": 20,
  "met": 30,
  "mt": 0,
  "ht": 350
}

base_cut = "( isTraining == 1 || isTraining == 2 ) && ( DataPastTriggerX == 1 ) && ( MCPastTriggerX == 1 ) "
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
  "NBJETS": ( "NJetsCSV_MultiLepCalc", bins( 0, 10, 11 ), ";Medium DeepJet Multiplicity" ),
  "NWJETS": ( "NJetsWtagged", bins( 0, 6, 7 ), ";W-tagged Jet Multiplicity" ),
  "NTJETS": ( "NJetsTtagged", bins( 0, 4, 5 ), ";t-tagged Jet Multiplicity" ),
  "DNN_3t": ( "DNN_3t", bins( 0, 1, 101 ), ";DNN 3t" )
}

systematics = [
  "pileup", 
  "prefire", 
  "muRFcorrd", 
  "muR", 
  "muF", 
  "isr", 
  "fsr", 
  "tau32", 
  "jmst", 
  "jmrt", 
  "tau21",
  "jmsW",
  "jmrW",
  "tau21pt",
  "btag",
  "mistag",
  "jec",
  "jer",
  "hotstat",
  "hostcspur",
  "hotclosure",
  "njet",
  "njetsf",
  "lfstats",
  "hfstats"
]

pdf_range = 100
