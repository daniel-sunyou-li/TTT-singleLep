#!/usr/bin/python

samples = {
  "TEST": {
    "TTTJ": "TTTJ_TuneCP5_13TeV-madgraph-pythia8",
    #"TTTW": "TTTW_TuneCP5_13TeV-madgraph-pythia8",
    #"DataE": "SingleElectron",
    "TTToSemiLeptonHT500": "TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8_ttbb"
  },
  "DATA": {
    "DataE": "SingleElectron",
    "DataM": "SingleMuon",
  },
  "SIGNAL": {
    "TTTJ": "TTTJ_TuneCP5_13TeV-madgraph-pythia8",
    "TTTW": "TTTW_TuneCP5_13TeV-madgraph-pythia8",
  },
  "BACKGROUND": {
    "WW": "WW_TuneCP5_13TeV-pythia8",
    "WZ": "WZ_TuneCP5_13TeV-pythia8",
    "ZZ": "ZZ_TuneCP5_13TeV-pythia8",

    "Ts": "ST_s-channel_4f_leptonDecays_13TeV_amcatnlo-pythia",
    "Tt": "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
    "Tbt": "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
    "TtW": "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
    "TbtW": "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",

    "TTTT": "TTTT_TuneCP5_13TeV-amcatnlo-pythia8",
    "TTHH": "TTHH_TuneCP5_13TeV-madgraph-pythia8",
    "TTWH": "TTWH_TuneCP5_13TeV-madgraph-pythia8",
    "TTWW": "TTWW_TuneCP5_13TeV-madgraph-pythia8",
    "TTWZ": "TTWZ_TuneCP5_13TeV-madgraph-pythia8",
    "TTZH": "TTZH_TuneCP5_13TeV-madgraph-pythia8",
    "TTZZ": "TTZZ_TuneCP5_13TeV-madgraph-pythia8",
    "TTWl": "TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
    "TTWq": "TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8", # MISSING IN OCT2019 PRODUCTION
    "TTZlM10": "TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
    #"TTZlM1to10": "TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8",
    "TTHB": "ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8",
    "TTHnoB": "ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8"
  },
  "HD": {},
  "UE": {}
}

for DYM_HT in [ "200to400", "400to600", "600to800", "800to1200", "1200to2500", "2500toInf" ]: 
  samples[ "BACKGROUND" ][ "DYM" + DYM_HT.split( "to" )[0] ] = "DYJetsToLL_M-50_HT-{}_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8".format( DYM_HT )

for WJets_HT in [ "200To400", "400To600", "600To800", "800To1200", "1200To2500", "2500ToInf" ]: 
  samples[ "BACKGROUND" ][ "WJetsMG" + WJets_HT.split( "To" )[0] ] = "WJetsToLNu_HT-{}_TuneCP5_13TeV-madgraphMLM-pythia8".format( WJets_HT )
  
for QCD_HT in [ "200to300", "300to500", "500to700", "700to1000", "1000to15000", "1500to2000", "2000toInf" ]: 
  samples[ "BACKGROUND" ][ "QCD" + QCD_HT.split( "to" )[0] ] = "QCD_HT{}_TuneCP5_PSWeights_13TeV-madgraph-pythia8".format( QCD_HT ) 
  
shifts = {
  "TuneCP5": "",
  "TuneCP5up": "_UEUP",
  "TuneCP5down": "_UEDN",
  "hdampUP_TuneCP5": "_HDUP",
  "hdampDOWN_TuneCP5": "_HDDN"
}
  
for tt in [ "SemiLepton", "SemiLeptonic", "Hadronic", "2L2Nu" ]:
  for shift in shifts:
    for fs in [ "1b", "2b", "bb", "cc", "jj" ]:
      if tt == "SemiLeptonic":
        samples[ "BACKGROUND" ][ "TTTo{}{}_tt{}".format( tt, shifts[ shift ], fs ) ] = "TTTo{}_{}_13TeV-powheg-pythia8_tt{}".format( tt, shift, fs )
        samples[ "BACKGROUND" ][ "TTTo{}HT500{}_tt{}".format( tt, shifts[ shift ], fs ) ] = "TTTo{}_{}_13TeV-powheg-pythia_HT500Njet9_tt{}".format( tt, shift, fs )
      elif tt == "SemiLepton":
        if shift != "TuneCP5": continue
        samples[ "BACKGROUND" ][ "TTTo{}HT500_tt{}".format( tt, fs ) ] = "TTTo{}_HT500Njet9_{}_13TeV-powheg-pythia8_tt{}".format( tt, shift, fs )
      else:
        samples[ "BACKGROUND" ][ "TTTo{}{}_tt{}".format( tt, shifts[ shift ], fs ) ] = "TTTo{}_{}_13TeV-powheg-pythia8_tt{}".format( tt, shift, fs )
