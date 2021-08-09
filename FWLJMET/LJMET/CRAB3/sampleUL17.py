import os,sys

datadict = { 
  "SingleElectronRun2017B": "/SingleElectron/Run2017B-UL2017_MiniAODv2-v1/MINIAOD",
  "SingleElectronRun2017C": "/SingleElectron/Run2017C-UL2017_MiniAODv2-v1/MINIAOD",
  "SingleElectronRun2017D": "/SingleElectron/Run2017D-UL2017_MiniAODv2-v1/MINIAOD",
  "SingleElectronRun2017E": "/SingleElectron/Run2017E-UL2017_MiniAODv2-v1/MINIAOD",
  "SingleElectronRun2017F": "/SingleElectron/Run2017F-UL2017_MiniAODv2-v1/MINIAOD",
  
  "SingleMuonRun2017B": "/SingleMuon/Run2017B-UL2017_MiniAODv2-v1/MINIAOD",
  "SingleMuonRun2017C": "/SingleMuon/Run2017C-UL2017_MiniAODv2-v1/MINIAOD",
  "SingleMuonRun2017D": "/SingleMuon/Run2017D-UL2017_MiniAODv2-v1/MINIAOD",
  "SingleMuonRun2017E": "/SingleMuon/Run2017E-UL2017_MiniAODv2-v1/MINIAOD",
  "SingleMuonRun2017F": "/SingleMuon/Run2017F-UL2017_MiniAODv2-v1/MINIAOD",
  
  "JetHTRun2017B": "/JetHT/Run2017B-UL2017_MiniAODv2-v1/MINIAOD",
  "JetHTRun2017C": "/JetHT/Run2017C-UL2017_MiniAODv2-v1/MINIAOD",
  "JetHTRun2017D": "/JetHT/Run2017D-UL2017_MiniAODv2-v1/MINIAOD",
  "JetHTRun2017E": "/JetHT/Run2017E-UL2017_MiniAODv2-v1/MINIAOD",
  "JetHTRun2017F": "/JetHT/Run2017F-UL2017_MiniAODv2-v1/MINIAOD",
}

# not sure where trigdictmc is referenced or how it is used 
trigdictmc = {
  "TTTo2L2Nu": "TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM"
}

signaldict = {
  "TTTW": "TTTW",
  "TTTJ": ""
}

bkgdict = {
  "TTW": "",
  "TTZM1to10": "",
  "TTZM10": "",
  "TTHbb": "",
  "TTHnonbb": "",
  "ST_tW_antitop": "",
  "ST_tW_top": "",
  "ST_t_antitop": "",
  "ST_t_top": "",
  "ST_s_top": "",
  "ST_s_antitop": ""
}

bkghtdict = {}

for DYM_HT in [ "200to400", "400to600", "600to800", "800to1200", "1200to2500", "2500toInf" ]:
  bkghtdict[ "DYM50HT" + DYM_HT ] = "/DYJetsToLL_M-50_HT-{}_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM".format( DYM_HT )
for WJets_HT in [ "200To400", "400To600", "600To800", "800To1200", "1200To2500", "2500ToInf" ]:  
  bkghtdict[ "WJetsHT" + WJets_HT ] = "/WJetsToLNu_HT-{}_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM".format( WJets_HT )
for QCD_HT in [ "200to300", "300to500", "700to1000", "1000to1500", "1500to2000", "2000toInf" ]:
  bkghtdict[ "QCDHT" + QCD_HT ] = "/QCD_HT{}_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM".format( QCD_HT )

ttbarbkgdict = {
  "TTTT": "",
  "TTWW": "",
  "TTZZ": "",
  "TTWH": "",
  "TTWZ": "",
  "TTZH": "",
  "TTHH": "",
  "TTToSemiLepton_HT500Njet9": ""
}

# need to look up whether erdON samples are included
for tt in [ "SemiLeptonic", "Hadronic", "2L2Nu" ]:
  for shift in [ "", "TuneCP5down", "TuneCP5up", "hdampUP_TuneCP5", "hdampDOWN_TuneCP5" ]:
    ttbarbkgdict[ tt + shift ] = "TTTo{}_{}_PSweights_13TeV-powheg-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM"












