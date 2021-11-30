# this is currently the sampleUL17.py --> update
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

MINIAODv1v2 = "RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM"
MINIAODv2v1 = "RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM"
MINIAODv2v2 = "RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM"

# not sure where trigdictmc is referenced or how it is used 
trigdictmc = {
  "TTTo2L2Nu": "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/" + MINIAODv2v1
}

signaldict = {
  "TTTW": "TTTW_TuneCP5_13TeV-madgraph-pythia8/" + MINIAODv2v2,
  "TTTJ": "TTTJ_TuneCP5_13TeV-madgraph-pythia8/" + MINIAODv2v2
}

bkgdict = {
  "TTWl": "/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/" + MINIAODv2v1,
  "TTWq": "/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/" + MINIAODv2v1,
  # "TTZM1to10": "/TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8/" + MINIAODv2, # unsubmitted
  "TTZM10": "/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/" + MINIAODv2v1,
  "TTHbb": "/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/" + MINIAODv2v2,
  "TTHnonbb": "/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/" + MINIAODv2v2, 
  "ST_tW_antitop": "/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/" + MINIAODv2v2, # in-progress 
  "ST_tW_top": "/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/" + MINIAODv2v2, # in-progress
  # "ST_t_antitop": "/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/" + MINIAODv1, # submitted
  # "ST_t_top": "/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/" + MINIAODv1, # submitted
  "ST_s_top": "/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/" + MINIAODv2v1,
  # "ST_s_antitop": "/ST_s-channel_antitop_leptonDecays_13TeV-PSweights_powheg-pythia8/" + MINIAODv2 # unsubmitted
}

bkghtdict = {}

for DYM_HT in [ "200to400", "400to600", "600to800", "800to1200", "1200to2500", "2500toInf" ]: 
  bkghtdict[ "DYM50HT" + DYM_HT ] = "/DYJetsToLL_M-50_HT-{}_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/{}".format( DYM_HT, MINIAODv2v1 )
for WJets_HT in [ "200To400", "400To600", "600To800", "1200To2500", "2500ToInf" ]: # "800To1200" in-progres 
  bkghtdict[ "WJetsHT" + WJets_HT ] = "/WJetsToLNu_HT-{}_13TeV-madgraphMLM-pythia8/{}".format( WJets_HT, MINIAODv2v1 )
for QCD_HT in [ "200to300", "300to500", "500to700", "700to1000", "1500to2000" ]: # "1000to1500", "2000toInf" in-progress
  bkghtdict[ "QCDHT" + QCD_HT ] = "/QCD_HT{}_TuneCP5_PSWeights_13TeV-madgraph-pythia8/{}".format( QCD_HT, MINIAODv2v1 )

ttbarbkgdict = {
  "TTTT": "/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/" + MINIAODv2v2,
  "TTWW": "/TTWW_TuneCP5_13TeV-madgraph-pythia8/" + MINIAODv2v1,
  "TTZZ": "/TTZZ_TuneCP5_13TeV-madgraph-pythia8/" + MINIAODv2v1,
  # "TTWH": "/TTWH_TuneCP5_13TeV-madgraph-pythia8/" + MINIAODv1, # in-progress
  "TTWZ": "/TTWZ_TuneCP5_13TeV-madgraph-pythia8/" + MINIAODv2,
  # "TTZH": "/TTZH_TuneCP5_13TeV-madgraph-pythia8/" + MINIAODv1, # submitted
  "TTHH": "/TTHH_TuneCP5_13TeV-madgraph-pythia8/" + MINIAODv2v2, 
  "TTToSemiLepton_HT500Njet9": "/TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8/" + MINIAODv2v2 
}

for tt in [ "SemiLeptonic", "Hadronic", "2L2Nu" ]:
  for shift in [ "", "TuneCP5down", "TuneCP5up", "hdampUP_TuneCP5", "hdampDOWN_TuneCP5" ]:
    ttbarbkgdict[ tt + shift ] = "TTTo{}_{}_PSweights_13TeV-powheg-pythia8/{}".format( tt, shift, MINIAODv2 )
    
# still need to add the TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT500Njet9 samples --> probably need to request