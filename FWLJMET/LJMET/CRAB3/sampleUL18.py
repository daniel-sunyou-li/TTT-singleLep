datadict = { 
  "SingleElectronRun2018A": "/EGamma/Run2018A-UL2018_MiniAODv2-v1/MINIAOD",
  "SingleElectronRun2018B": "/EGamma/Run2018B-UL2018_MiniAODv2-v1/MINIAOD",
  "SingleElectronRun2018C": "/EGamma/Run2018C-UL2018_MiniAODv2-v1/MINIAOD",
  "SingleElectronRun2018D": "/EGamma/Run2018D-UL2018_MiniAODv2-v2/MINIAOD",
  
  "SingleMuonRun2018A": "/SingleMuon/Run2018A-UL2018_MiniAODv2-v3/MINIAOD",
  "SingleMuonRun2018B": "/SingleMuon/Run2018B-UL2018_MiniAODv2-v2/MINIAOD",
  "SingleMuonRun2018C": "/SingleMuon/Run2018C-UL2018_MiniAODv2-v2/MINIAOD",
  "SingleMuonRun2018D": "/SingleMuon/Run2018D-UL2018_MiniAODv2-v3/MINIAOD",
  
  "JetHTRun2018A": "/JetHT/Run2018A-UL2018_MiniAODv2-v1/MINIAOD",
  "JetHTRun2018B": "/JetHT/Run2018B-UL2018_MiniAODv2-v1/MINIAOD",
  "JetHTRun2018C": "/JetHT/Run2018C-UL2018_MiniAODv2-v1/MINIAOD",
  "JetHTRun2018D": "/JetHT/Run2018D-UL2018_MiniAODv2-v1/MINIAOD"
}

MINIAODv1 = "RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM"
MINIAODv2v1 = "RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM"
MINIAODv2v2 = "RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM"

# not sure where trigdictmc is referenced or how it is used 
trigdictmc = {
  "TTTo2L2Nu": "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/" + MINIAODv2v1
}

signaldict = {
  # "TTTW": "TTTW_TuneCP5_13TeV-madgraph-pythia8/" + MINIAODv1 # in-progress
  # "TTTJ": "TTTJ_TuneCP5_13TeV-madgraph-pythia8/" + MINIAODv1 # in-progress
}

bkgdict = {
  "TTWl": "/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/" + MINIAODv2,
  "TTWq": "/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/" + MINIAODv2,
  # "TTZM1to10": "/TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8/" + MINIAODv2, # unsubmitted
  "TTZM10": "/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/" + MINIAODv1, # MINIAODv2 in-progress
  # "TTHbb": "/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/" + MINIAODv1, # in-progress
  # "TTHnonbb": "/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/" + MINIAODv1, # in-progress
  # "ST_tW_antitop": "/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/" + MINIAODv1, # in-progress 
  # "ST_tW_top": "/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/" + MINIAODv1, # in-progress
  # "ST_t_antitop": "/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/" + MINIAODv1, # submitted
  # "ST_t_top": "/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-madspin-pythia8/" + MINIAODv1, # submitted
  "ST_s_top": "/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/" + MINIAODv2,
  # "ST_s_antitop": "/ST_s-channel_antitop_leptonDecays_13TeV-PSweights_powheg-pythia8/" + MINIAODv2 # unsubmitted
}

bkghtdict = {}

for DYM_HT in [ "200to400", "400to600", "600to800", "800to1200", "1200to2500", ]: # "2500toInf" in-progress
  bkghtdict[ "DYM50HT" + DYM_HT ] = "/DYJetsToLL_M-50_HT-{}_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/{}".format( DYM_HT, MINIAODv2 )
for WJets_HT in [ "200To400", "400To600", "600To800", "800To1200" ]: # "1200To2500" "2500ToInf" in-progres 
  bkghtdict[ "WJetsHT" + WJets_HT ] = "/WJetsToLNu_HT-{}_TuneCP5_13TeV-madgraphMLM-pythia8/{}".format( WJets_HT, MINIAODv2 )
for QCD_HT in [ ]: #  "200to300", "300to500", "700to1000","1000to1500", "1500to2000", "2000toInf" in-progress
  bkghtdict[ "QCDHT" + QCD_HT ] = "/QCD_HT{}_TuneCP5_PSWeights_13TeV-madgraph-pythia8/{}".format( QCD_HT, MINIAODv1 )

ttbarbkgdict = {
  # "TTTT": "/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/" + MINIAODv1, # in-progress
  "TTWW": "/TTWW_TuneCP5_13TeV-madgraph-pythia8/" + MINIAODv2,
  "TTZZ": "/TTZZ_TuneCP5_13TeV-madgraph-pythia8/" + MINIAODv1, # MINIAODv2 in-progress
  # "TTWH": "/TTWH_TuneCP5_13TeV-madgraph-pythia8/" + MINIAODv1, # in-progress
  "TTWZ": "/TTWZ_TuneCP5_13TeV-madgraph-pythia8/" + MINIAODv2,
  # "TTZH": "/TTZH_TuneCP5_13TeV-madgraph-pythia8/" + MINIAODv1, # submitted
  # "TTHH": "/TTHH_TuneCP5_13TeV-madgraph-pythia8/" + MINIAODv1, # submitted
  "TTToSemiLepton_HT500Njet9": "/TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8/" + MINIAODv1 # MINIAODv2 in-progress
}

# need to look up whether erdON samples are included
for tt in [ "SemiLeptonic", "Hadronic", "2L2Nu" ]:
  for shift in [ "TuneCP5", "TuneCP5down", "TuneCP5up", "hdampUP_TuneCP5", "hdampDOWN_TuneCP5" ]:
    ttbarbkgdict[ tt + shift ] = "TTTo{}_{}_13TeV-powheg-pythia8/{}".format( tt, shift, MINIAODv2 )
