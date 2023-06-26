#!/usr/bin/python

import config

BR = { 
  "TT": {
    "SemiLeptonic": 0.438,
    "Hadronic": 0.457,
    "2L2Nu": 0.105
  }
}

filtEff_tt = {
  "Njet9": 0.00617938417682763,
  "Njet9HDDN": 0.005645170035947885,
  "Njet9HDUP": 0.006711348259851689,
  "Njet9UEDN": 0.006108623095875414,
  "Njet9UEUP": 0.0062286452403598055 
}

k_factor = {
  "WJetsMG": 1.21,
  "TTTJ": 1.75,    # NLO QCD 5FS https://github.com/gdurieux/triple-top-nlo
  "TTTW": 1.86     # NLO QCD 5FS https://github.com/gdurieux/triple-top-nlo
}

tt_xsec = 831.8

xsec = {
  "TTTJ": 0.0003974 * k_factor[ "TTTJ" ],
  "TTTW": 0.0007314 * k_factor[ "TTTW" ],
  "TTTT": 0.01197,
  "TTWW": 0.00703,
  "TTWZ": 0.002453,
  "TTWH": 0.001141,
  "TTHH": 0.0006655,
  "TTZH": 0.00113,
  "TTZZ": 0.001385,
  "TTWl": 0.2161,
  "TTWq": 0.4377,
  "TTZlM10": 0.2439,
  "TTZlM1to10": 0.05324,
  "TTHB": 0.291,
  "TTHnoB": 0.209,
  "Ts": 3.549,      # NLO https://cms-gen-dev.cern.ch/xsdb/?columns=67108863&currentPage=0&pageSize=10&searchQuery=process_name%3DST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8
  "Tt": 134.2,     # NNLO https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopNNLORef
  "Tbt": 80.0,     # NNLO https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopNNLORef
  "TtW": 39.65,    # NNLO https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopNNLORef
  "TbtW": 39.65,   # NNLO https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopNNLORef
  "QCD200": 1712000,
  "QCD300": 347700,
  "QCD500": 32100,
  "QCD700": 6831,
  "QCD1000": 1207,
  "QCD1500": 119.9,
  "QCD2000": 25.24,
  "WW": 118.7,
  "WZ": 47.13,
  "ZZ": 16.523,
  "DYM200": 54.951,
  "DYM400": 7.862,
  "DYM600": 1.977,
  "DYM800": 0.858,
  "DYM1200": 0.191,
  "DYM2500": 0.0045,
  "WJetsMG200": 359.7 * k_factor[ "WJetsMG" ],
  "WJetsMG400": 48.91 * k_factor[ "WJetsMG" ],
  "WJetsMG600": 12.05 * k_factor[ "WJetsMG" ],
  "WJetsMG800": 5.501 * k_factor[ "WJetsMG" ],
  "WJetsMG1200": 1.329 * k_factor[ "WJetsMG" ],
  "WJetsMG2500": 0.03216 * k_factor[ "WJetsMG" ],
  "TTToSemiLeptonic": tt_xsec * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9" ] ),
  "TTToSemiLeptonicUEUP": tt_xsec * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9UEUP" ] ),
  "TTToSemiLeptonicUEDN": tt_xsec * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9UEDN" ] ),
  "TTToSemiLeptonicHDUP": tt_xsec * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9HDUP" ] ),
  "TTToSemiLeptonicHDDN": tt_xsec * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9HDDN" ] ),
  "TTToSemiLeptonicHT500": tt_xsec * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9" ],
  "TTToSemiLeptonicHT500UEUP": tt_xsec * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9UEUP" ],
  "TTToSemiLeptonicHT500UEDN": tt_xsec * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9UEDN" ],
  "TTToSemiLeptonicHT500HDUP": tt_xsec * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9HDUP" ],
  "TTToSemiLeptonicHT500HDDN": tt_xsec * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9HDDN" ],
  "TTToSemiLeptonHT500": 2.251,
  "TTToHadronic": tt_xsec * BR[ "TT" ][ "Hadronic" ],
  "TTToHadronicUEUP": tt_xsec * BR[ "TT" ][ "Hadronic" ],
  "TTToHadronicUEDN": tt_xsec * BR[ "TT" ][ "Hadronic" ],
  "TTToHadronicHDUP": tt_xsec * BR[ "TT" ][ "Hadronic" ],
  "TTToHadronicHDDN": tt_xsec * BR[ "TT" ][ "Hadronic" ],
  "TTTo2L2Nu": tt_xsec * BR[ "TT" ][ "2L2Nu" ],
  "TTTo2L2NuUEUP": tt_xsec * BR[ "TT" ][ "2L2Nu" ],
  "TTTo2L2NuUEDN": tt_xsec * BR[ "TT" ][ "2L2Nu" ],
  "TTTo2L2NuHDUP": tt_xsec * BR[ "TT" ][ "2L2Nu" ],
  "TTTo2L2NuHDDN": tt_xsec * BR[ "TT" ][ "2L2Nu" ]
}

N = {
  "TTToSemiLeptonicttjj": range( 1, 11 ),
  "TTTT": range( 1, 4 )
}

for tt in [ "SemiLeptonic", "SemiLeptonicHT500", "SemiLeptonHT500", "Hadronic", "2L2Nu" ]:
  for fs in [ "jj", "cc", "bb", "1b", "2b" ]:
    if tt == "SemiLeptonic" and fs == "jj":
      for n in N["TTToSemiLeptonicttjj"]:
        xsec[ "TTTo{}tt{}{}".format( tt, fs, n ) ] = xsec[ "TTTo{}".format( tt ) ]
    else:
      xsec[ "TTTo{}tt{}".format( tt, fs ) ] = xsec[ "TTTo{}".format( tt ) ]
    if tt in [ "SemiLeptonic", "SemiLeptonicHT500", "Hadronic", "2L2Nu" ]:
      for syst in [ "UE", "HD" ]:
        for shift in [ "DN", "UP" ]:
          xsec[ "TTTo{}{}{}tt{}".format( tt, syst, shift, fs ) ] = xsec[ "TTTo{}{}{}".format( tt, syst, shift ) ]

for i in N["TTTT"]:
  xsec[ "TTTT{}".format(i) ] = xsec[ "TTTT" ]
