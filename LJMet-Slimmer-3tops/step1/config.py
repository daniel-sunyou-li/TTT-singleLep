eosUserName = "dali"
postfix = "deepJetV1"  #"Winter2021"
years = [ "16", "17", "18" ]

ljmetDir = {
  year: {
    "LPC": "/eos/uscms/store/user/{}/FWLJMET106XUL_1lep20{}_3t_{}".format( eosUserName, year, postfix ),
    "BRUX": "/isilon/hadoop/store/user/{}/FWLJMET106XUL_1lep20{}_3t_{}".format( eosUserName, year, postfix )
  } for year in years
}

step1Dir = {
  year: {
    "LPC": "/eos/uscms/store/user/{}/FWLJMET106XUL_1lep20{}_3t_{}_step1".format( eosUserName, year, postfix ), 
    "BRUX": "/isilon/hadoop/store/user/{}/FWLJMET106XUL_1lep20{}_3t_{}_step1".format( eosUserName, year, postfix ) 
  } for year in years
}

haddDir = {
  year: {
    "LPC": "/eos/uscms/store/user/{}/FWLJMET106XUL_1lep20{}_3t_{}_step1hadds".format( eosUserName, year, postfix ),
    "BRUX": "/isilon/hadoop/store/user/{}/FWLJMET106XUL_1lep20{}_3t_{}_step1hadds".format( eosUserName, year, postfix )
  } for year in years
}

outputPath = "/store/user/{}/".format( eosUserName ),


samples = {
  "2016": {
    "TEST": [ "TTTW_TuneCUETP8M2T4_13TeV-madgraph-pythia8" ],
    "LPC": [
      "DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8",
      "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",
      "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",
      "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",
      "ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",
      "SingleElectron",
      "SingleMuon",
      "TTHH_TuneCUETP8M2T4_13TeV-madgraph-pythia8",
      "TTTJ_TuneCUETP8M2T4_13TeV-madgraph-pythia8",
      "TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_correctnPartonsInBorn",
      "TTTW_TuneCUETP8M2T4_13TeV-madgraph-pythia8",
      "TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8",
      "TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8",
      "TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8",
      "TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8",
      "TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8",
      "TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8",
      "TTToHadronic_TuneCP5down_PSweights_13TeV-powheg-pythia8",
      "TTToHadronic_TuneCP5up_PSweights_13TeV-powheg-pythia8",
      "TTToHadronic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8",
      "TTToHadronic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8",
      "TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8",
      "TTToSemiLepton_HT500Njet9_TuneCP5down_PSweights_13TeV-powheg-pythia8",
      "TTToSemiLepton_HT500Njet9_TuneCP5up_PSweights_13TeV-powheg-pythia8",
      "TTToSemiLepton_HT500Njet9_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8",
      "TTToSemiLepton_HT500Njet9_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8",
      "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8",
      "TTToSemiLeptonic_TuneCP5down_PSweights_13TeV-powheg-pythia8",
      "TTToSemiLeptonic_TuneCP5up_PSweights_13TeV-powheg-pythia8",
      "TTToSemiLeptonic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8",
      "TTToSemiLeptonic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8",
      "TTWH_TuneCUETP8M2T4_13TeV-madgraph-pythia8",
      "TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8",
      "TTWW_TuneCUETP8M2T4_13TeV-madgraph-pythia8",
      "TTWZ_TuneCUETP8M2T4_13TeV-madgraph-pythia8",
      "TTZH_TuneCUETP8M2T4_13TeV-madgraph-pythia8",
      "TTZToLLNuNu_M-10_TuneCP5_PSweights_13TeV-amcatnlo-pythia8",
      "TTZToLL_M-1to10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "TTZZ_TuneCUETP8M2T4_13TeV-madgraph-pythia8",
      "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
      "WW_TuneCUETP8M1_13TeV-pythia8",
      "WZ_TuneCUETP8M1_13TeV-pythia8",
      "ZZ_TuneCUETP8M1_13TeV-pythia8",
      "ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8",
      "ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8",
    ],
    "BRUX": [
    
    ]
  },
  "2017": {
    "TEST": [ "TTTW_TuneCP5_13TeV-madgraph-pythia8" ],
    "LPC": [
      #"DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8",
      #"DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8",
      #"DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8",
      #"DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8",
      #"DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8",
      #"DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8",
      #"QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraph-pythia8",
      #"QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8",
      #"QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraph-pythia8",
      #"QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraph-pythia8",
      #"QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraph-pythia8",
      #"QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8",
      #"QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraph-pythia8",
      #"ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8",
      #"ST_s-channel_top_leptonDecays_13TeV-PSweights_powheg-pythia",
      "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
      #"ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
      #"ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
      #"ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
      #"SingleElectron",
      #"SingleMuon",
      #"TTHH_TuneCP5_13TeV-madgraph-pythia8",
      #"TTTJ_TuneCP5_13TeV-madgraph-pythia8",
      #"TTTW_TuneCP5_13TeV-madgraph-pythia8",
      #"TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
      #"TTTo2L2Nu_TuneCP5down_13TeV-powheg-pythia8",
      #"TTTo2L2Nu_TuneCP5up_13TeV-powheg-pythia8",
      #"TTTo2L2Nu_hdampDOWN_TuneCP5_13TeV-powheg-pythia8",
      #"TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8",
      #"TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
      #"TTToHadronic_TuneCP5down_13TeV-powheg-pythia8",
      #"TTToHadronic_TuneCP5up_13TeV-powheg-pythia8",
      #"TTToHadronic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8",
      #"TTToHadronic_hdampUP_TuneCP5_13TeV-powheg-pythia8",
      #"TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8",
      #"TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
      "TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8",
      #"TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8",
      #"TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8",
      "TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8",
      "TTWH_TuneCP5_13TeV-madgraph-pythia8",
      #"TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
      "TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
      #"TTWW_TuneCP5_13TeV-madgraph-pythia8",
      #"TTWZ_TuneCP5_13TeV-madgraph-pythia8",
      #"TTZH_TuneCP5_13TeV-madgraph-pythia8",
      #"TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
      #"TTZZ_TuneCP5_13TeV-madgraph-pythia8",
      #"WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8",
      #"WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8",
      #"WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8",
      #"WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8",
      #"WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8",
      #"WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8",
      #"WW_TuneCP5_13TeV-pythia8",
      #"WZ_TuneCP5_13TeV-pythia8",
      #"ZZ_TuneCP5_13TeV-pythia8",
      #"ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8",
      #"ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8",
      "TTTT_TuneCP5_13TeV-amcatnlo-pythia8",
      #"TTToSemiLepton_HT500Njet9_TuneCP5down_PSweights_13TeV-powheg-pythia8",
      #"TTToSemiLepton_HT500Njet9_TuneCP5up_PSweights_13TeV-powheg-pythia8",
      #"TTToSemiLepton_HT500Njet9_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8",
      #"TTToSemiLepton_HT500Njet9_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8",
    ],
    "BRUX": [
      #"DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8",
      #"QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraph-pythia8",
      #"QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraph-pythia8",
      #"QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8",
      #"ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
      #"ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
      #"TTHH_TuneCP5_13TeV-madgraph-pythia8",
      "TTTT_TuneCP5_13TeV-amcatnlo-pythia8",
      #"TTTJ_TuneCP5_13TeV-madgraph-pythia8",
      #"TTTW_TuneCP5_13TeV-madgraph-pythia8",
      #"TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
      #"TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8",
      #"TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
      #"TTToHadronic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8",
      #"TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8",
      #"TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
      #"TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8",
      #"TTWH_TuneCP5_13TeV-madgraph-pythia8",
      #"TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
      #"TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
      #"TTWW_TuneCP5_13TeV-madgraph-pythia8",
      #"TTWZ_TuneCP5_13TeV-madgraph-pythia8",
      #"ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8"
    ]
  },
  "2018": {
    "TEST": [ "TTTW_TuneCP5_13TeV-madgraph-pythia8" ],
    "LPC": [
      "DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8",
      "DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8",
      "DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8",
      "DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8",
      "DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8",
      "DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8",
      "QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8",
      "QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8",
      "QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8",
      "QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8",
      "QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8",
      "QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8",
      "QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8",
      "ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8",
      "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
      "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
      "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
      "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
      "EGamma",
      "SingleMuon",
      "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
      "TTTo2L2Nu_TuneCP5down_13TeV-powheg-pythia8",
      "TTTo2L2Nu_hdampDOWN_TuneCP5_13TeV-powheg-pythia8",
      "TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8",
      "TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
      "TTToHadronic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8",
      "TTToHadronic_hdampUP_TuneCP5_13TeV-powheg-pythia8",
      "TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8",
      "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
      "TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8",
      "TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
      "TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
      "TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8",
      "WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8",
      "WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8",
      "WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8",
      "WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8",
      "WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8",
      "WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8",
      "WW_TuneCP5_PSweights_13TeV-pythia8",
      "WZ_TuneCP5_PSweights_13TeV-pythia8",
      "ZZ_TuneCP5_13TeV-pythia8",
      "ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8",
      "ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8",
      "TTTT_TuneCP5_13TeV-amcatnlo-pythia8",
      "TTToSemiLepton_HT500Njet9_TuneCP5down_13TeV-powheg-pythia8",
      "TTToSemiLepton_HT500Njet9_TuneCP5up_13TeV-powheg-pythia8",
      "TTToSemiLepton_HT500Njet9_hdampDOWN_TuneCP5_13TeV-powheg-pythia8",
      "TTToSemiLepton_HT500Njet9_hdampUP_TuneCP5_13TeV-powheg-pythia8",
    ],
    "BRUX": [
      "TTHH_TuneCP5_13TeV-madgraph-pythia8",
      "TTTJ_TuneCP5_13TeV-madgraph-pythia8",
      "TTTo2L2Nu_TuneCP5up_13TeV-powheg-pythia8",
      "TTToHadronic_TuneCP5down_13TeV-powheg-pythia8",
      "TTToHadronic_TuneCP5up_13TeV-powheg-pythia8",
      "TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8",
      "TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8",
      "TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8",
      "TTTT_TuneCP5_13TeV-amcatnlo-pythia8",
      "TTTW_TuneCP5_13TeV-madgraph-pythia8",
      "TTWH_TuneCP5_13TeV-madgraph-pythia8",
      "TTWW_TuneCP5_13TeV-madgraph-pythia8",
      "TTWZ_TuneCP5_13TeV-madgraph-pythia8",
      "TTZH_TuneCP5_13TeV-madgraph-pythia8",
      "TTZZ_TuneCP5_13TeV-madgraph-pythia8",
    ]
  }
}
