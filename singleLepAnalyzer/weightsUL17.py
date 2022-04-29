#!/usr/bin/python

import config

xsec = { "TT": 831.8 }

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
  "WJetsMG": 1.21
}

mc_stats = {
  "TTTJ": { 
    "EVENTS": 465000.0, 
    "XSEC": 0.0003974 
  },
  "TTTW": { 
    "EVENTS": 448000.0, 
    "XSEC": 0.0007314
  },
  
  "TTTT": { 
    "EVENTS": 5371110., 
    "XSEC": 0.01197
  },
  "TTWW": { 
    "EVENTS": 530000.0, 
    "XSEC": 0.00703
  },
  "TTWZ": { 
    "EVENTS": 698000.0, 
    "XSEC": 0.002453
  },
  "TTWH": { 
    "EVENTS": 523000.0, 
    "XSEC": 0.001141
  },
  "TTHH": { 
    "EVENTS": 442000.0, 
    "XSEC": 0.0006655
  },
  "TTZH": { 
    "EVENTS": 700000.0, 
    "XSEC": 0.00113
  },
  "TTZZ": { 
    "EVENTS": 621000., 
    "XSEC": 0.001385
  },
  "TTWl": { 
    "EVENTS": 4071914., 
    "XSEC": 0.2161
  },
  "TTWq": { 
    "EVENTS": 395611., 
    "XSEC": 0.4377
  },
  "TTZlM10": { 
    "EVENTS": 7555432., 
    "XSEC": 0.05324
  },
  "TTZlM1to10": { 
    "EVENTS": 781204., 
    "XSEC": 0.05324
  },
  "TTHB": { 
    "EVENTS": 13932018., 
    "XSEC": 0.5269
  },
  "TTHnoB": { 
    "EVENTS": 6124800., 
    "XSEC": 0.5638
  },
  "Ts": { 
    "EVENTS": 9037288., 
    "XSEC": 3.44
  },
  "Tt": { 
    "EVENTS": 63509348., 
    "XSEC": 136.02
  },
  "Tbt": { 
    "EVENTS": 63509348., 
    "XSEC": 80.95
  },
  "TtW": { 
    "EVENTS": 5648712., 
    "XSEC": 35.83
  },
  "TbtW": { 
    "EVENTS": 5644700., 
    "XSEC": 35.83
  },
  
  "QCD200": { 
    "EVENTS": 42714435., 
    "XSEC": 1712000
  },
  "QCD300": { 
    "EVENTS": 38938413., 
    "XSEC": 347700
  },
  "QCD500": { 
    "EVENTS": 36194860., 
    "XSEC": 32100
  },
  "QCD700": { 
    "EVENTS": 34051754., 
    "XSEC": 6831
  },
  "QCD1000": { 
    "EVENTS": 10256089., 
    "XSEC": 1207
  },
  "QCD1500": { 
    "EVENTS": 7701876., 
    "XSEC": 119.9
  },
  "QCD2000": { 
    "EVENTS": 4112573., 
    "XSEC": 25.24
  },
  
  "WW": { 
    "EVENTS": 15634000., 
    "XSEC": 118.7
  },
  "WZ": { 
    "EVENTS": 7889000., 
    "XSEC": 47.13
  },
  "ZZ": { 
    "EVENTS": 2706000., 
    "XSEC": 16.523
  },
  
  "DYM200": { 
    "EVENTS": 9704602., 
    "XSEC": 54.951
  },
  "DYM400": { 
    "EVENTS": 5408819., 
    "XSEC": 7.862
  },
  "DYM600": { 
    "EVENTS": 3535183., 
    "XSEC": 1.977
  },
  "DYM800": { 
    "EVENTS": 1025124., 
    "XSEC": 0.858
  },
  "DYM1200": { 
    "EVENTS": 4798360., 
    "XSEC": 0.191
  },
  "DYM2500": { 
    "EVENTS": 1395535., 
    "XSEC": 0.0045
  },
  
  "WJetsMG200": { 
    "EVENTS": 42602407., 
    "XSEC": 359.7 * k_factor[ "WJetsMG" ]
  },
  "WJetsMG400": { 
    "EVENTS": 5408819., 
    "XSEC": 48.91 * k_factor[ "WJetsMG" ]
  },
  "WJetsMG600": { 
    "EVENTS": 5292676., 
    "XSEC": 12.05 * k_factor[ "WJetsMG" ]
  },
  "WJetsMG800": { 
    "EVENTS": 4834185., 
    "XSEC": 5.501 * k_factor[ "WJetsMG" ]
  },
  "WJetsMG1200": { 
    "EVENTS": 3556525., 
    "XSEC": 1.329 * k_factor[ "WJetsMG" ]
  },
  "WJetsMG2500": { 
    "EVENTS": 1185699., 
    "XSEC": 0.03216 * k_factor[ "WJetsMG" ]
  },
  
  "TTToSemiLeptonic": { 
    "EVENTS": 331279322.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9" ] )
  },
  "TTToSemiLeptonicUEUP": { 
    "EVENTS": 137475034.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9UEUP" ] )
  },
  "TTToSemiLeptonicUEDN": { 
    "EVENTS": 131182302.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9UEDN" ] )
  },
  "TTToSemiLeptonicHDUP": { 
    "EVENTS": 132383014.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9HDUP" ] )
  },
  "TTToSemiLeptonicHDDN": { 
    "EVENTS": 132018269.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9HDDN" ] )
  },
  
  "TTToSemiLeptonicHT500": { 
    "EVENTS": 331279322., 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9" ] 
  },
  "TTToSemiLeptonicHT500UEUP": { 
    "EVENTS": 137475034.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9UEUP" ]
  },
  "TTToSemiLeptonicHT500UEDN": { 
    "EVENTS": 131182302.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9UEDN" ]
  },
  "TTToSemiLeptonicHT500HDUP": { 
    "EVENTS": 132383014.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9HDUP" ]
  },
  "TTToSemiLeptonicHT500HDDN": { 
    "EVENTS": 132018269.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9HDDN" ]
  },
  "TTToSemiLeptonHT500": { 
    "EVENTS": 7035304.0, 
    "XSEC": 2.251
  },
  "TTToHadronic": { 
    "EVENTS": 233815417.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ] 
  },
  "TTToHadronicUEUP": { 
    "EVENTS": 95498399.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ]
  },
  "TTToHadronicUEDN": { 
    "EVENTS": 94308036.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ]
  },
  "TTToHadronicHDUP": { 
    "EVENTS": 99030356.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ]
  },
  "TTToHadronicHDDN": { 
    "EVENTS": 93721302.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ]
  },
  
  "TTTo2L2Nu": { 
    "EVENTS": 105697364., 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  },
  "TTTo2L2NuUEUP": { 
    "EVENTS": 42495090.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  },
  "TTTo2L2NuUEDN": { 
    "EVENTS": 39078720.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  },
  "TTTo2L2NuHDUP":{ 
    "EVENTS": 40026124.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  },
  "TTTo2L2NuHDDN": { 
    "EVENTS": 39960772.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  }
}

weights = { key: config.lumi[ "17" ] * mc_stats[ key ][ "XSEC" ] / mc_stats[ key ][ "EVENTS" ] for key in mc_stats  }

for tt in [ "SemiLeptonic", "SemiLeptonicHT500", "SemiLeptonHT500", "Hadronic", "2L2Nu" ]:
  for fs in [ "jj", "cc", "bb", "1b", "2b" ]:
    if tt == "SemiLeptonic" and fs == "jj":
      for n in [ "1", "2", "3", "4" ]:
        weights[ "TTTo{}tt{}{}".format( tt, fs, n ) ] = weights[ "TTTo{}".format( tt ) ]
    else:
      weights[ "TTTo{}tt{}".format( tt, fs ) ] = weights[ "TTTo{}".format( tt ) ]
    if tt in [ "SemiLeptonic", "SemiLeptonicHT500", "Hadronic", "2L2Nu" ]:
      for syst in [ "UE", "HD" ]:
        for shift in [ "DN", "UP" ]:
          weights[ "TTTo{}{}{}tt{}".format( tt, syst, shift, fs ) ] = weights[ "TTTo{}{}{}".format( tt, syst, shift ) ]
