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
    "EVENTS": 302000.0, 
    "XSEC": 0.0003974 
  },
  "TTTW": { 
    "EVENTS": 340000.0, 
    "XSEC": 0.0007314
  },
  
  "TTTT": { 
    "EVENTS": 3458180.0, 
    "XSEC": 0.01197
  },
  "TTWW": { 
    "EVENTS": 245000.0, 
    "XSEC": 0.00703
  },
  "TTWZ": { 
    "EVENTS": 140000.0, 
    "XSEC": 0.002453
  },
  "TTWH": { 
    "EVENTS": 140000.0, 
    "XSEC": 0.001141
  },
  "TTHH": { 
    "EVENTS": 140000.0, 
    "XSEC": 0.0006655
  },
  "TTZH": { 
    "EVENTS": 140000.0, 
    "XSEC": 0.00113
  },
  "TTZZ": { 
    "EVENTS": 140000.0, 
    "XSEC": 0.001385
  },
  "TTWl": { 
    "EVENTS": 1543290.0, 
    "XSEC": 0.2161
  },
  "TTWq": { 
    "EVENTS": 148842.0, 
    "XSEC": 0.4377
  },
  "TTZlM10": { 
    "EVENTS": 177656.0, 
    "XSEC": 0.2439
  },
  "TTZlM1to10": { 
    "EVENTS": 140000.0, 
    "XSEC": 0.05324
  },
  "TTHB": { 
    "EVENTS": 4121294.0, 
    "XSEC": 0.291
  },
  "TTHnoB": { 
    "EVENTS": 1936276.0, 
    "XSEC": 0.209
  },
  "Ts": { 
    "EVENTS": 3478306.0, 
    "XSEC": 3.44
  },
  "Tt": { 
    "EVENTS": 52437432.0, 
    "XSEC": 136.02
  },
  "Tbt": { 
    "EVENTS": 29205918.0, 
    "XSEC": 80.95
  },
  "TtW": { 
    "EVENTS": 2299880.0, 
    "XSEC": 35.83
  },
  "TbtW": { 
    "EVENTS": 2299866.0, 
    "XSEC": 35.83
  },
  
  "QCD200": { 
    "EVENTS": 18273591.0, 
    "XSEC": 1712000
  },
  "QCD300": { 
    "EVENTS": 15226527.0, 
    "XSEC": 347700
  },
  "QCD500": { 
    "EVENTS": 15775001.0, 
    "XSEC": 32100
  },
  "QCD700": { 
    "EVENTS": 15808790.0, 
    "XSEC": 6831
  },
  "QCD1000": { 
    "EVENTS": 4773503.0, 
    "XSEC": 1207
  },
  "QCD1500": { 
    "EVENTS": 3503675.0, 
    "XSEC": 119.9
  },
  "QCD2000": { 
    "EVENTS": 1629000.0, 
    "XSEC": 25.24
  },
  
  "WW": { 
    "EVENTS": 15025000.0, 
    "XSEC": 118.7
  },
  "WZ": { 
    "EVENTS": 7934000.0, 
    "XSEC": 47.13
  },
  "ZZ": { 
    "EVENTS": 1282000.0, 
    "XSEC": 16.523
  },
  
  "DYM200": { 
    "EVENTS": 5862631.0, 
    "XSEC": 54.951
  },
  "DYM400": { 
    "EVENTS": 2716892.0, 
    "XSEC": 7.862
  },
  "DYM600": { 
    "EVENTS": 2617037.0, 
    "XSEC": 1.977
  },
  "DYM800": { 
    "EVENTS": 2411091.0, 
    "XSEC": 0.858
  },
  "DYM1200": { 
    "EVENTS": 2189664.0, 
    "XSEC": 0.191
  },
  "DYM2500": { 
    "EVENTS": 721404.0, 
    "XSEC": 0.0045
  },
  
  "WJetsMG200": { 
    "EVENTS": 17164198.0, 
    "XSEC": 359.7 * k_factor[ "WJetsMG" ]
  },
  "WJetsMG400": { 
    "EVENTS": 2302057.0, 
    "XSEC": 48.91 * k_factor[ "WJetsMG" ]
  },
  "WJetsMG600": { 
    "EVENTS": 1905536.0, 
    "XSEC": 12.05 * k_factor[ "WJetsMG" ]
  },
  "WJetsMG800": { 
    "EVENTS": 2350331.0, 
    "XSEC": 5.501 * k_factor[ "WJetsMG" ]
  },
  "WJetsMG1200": { 
    "EVENTS": 1754683.0, 
    "XSEC": 1.329 * k_factor[ "WJetsMG" ]
  },
  "WJetsMG2500": { 
    "EVENTS": 808649.0, 
    "XSEC": 0.03216 * k_factor[ "WJetsMG" ]
  },
  
  "TTToSemiLeptonic": { 
    "EVENTS": 133661764.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9" ] )
  },
  "TTToSemiLeptonicUEUP": { 
    "EVENTS": 1, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9UEUP" ] )
  },
  "TTToSemiLeptonicUEDN": { 
    "EVENTS": 1, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9UEDN" ] )
  },
  "TTToSemiLeptonicHDUP": { 
    "EVENTS": 1, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9HDUP" ] )
  },
  "TTToSemiLeptonicHDDN": { 
    "EVENTS": 1, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9HDDN" ] )
  },
  
  "TTToSemiLeptonicHT500": { 
    "EVENTS": 133661764.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9" ] 
  },
  "TTToSemiLeptonicHT500UEUP": { 
    "EVENTS": 1, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9UEUP" ]
  },
  "TTToSemiLeptonicHT500UEDN": { 
    "EVENTS": 1, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9UEDN" ]
  },
  "TTToSemiLeptonicHT500HDUP": { 
    "EVENTS": 1, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9HDUP" ]
  },
  "TTToSemiLeptonicHT500HDDN": { 
    "EVENTS": 1, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9HDDN" ]
  },
  "TTToSemiLeptonHT500": { 
    "EVENTS": 4443604.0, 
    "XSEC": 2.251
  },
  "TTToHadronic": { 
    "EVENTS": 93137016.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ] 
  },
  "TTToHadronicUEUP": { 
    "EVENTS": 1, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ]
  },
  "TTToHadronicUEDN": { 
    "EVENTS": 1, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ]
  },
  "TTToHadronicHDUP": { 
    "EVENTS": 1, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ]
  },
  "TTToHadronicHDDN": { 
    "EVENTS": 1, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ]
  },
  
  "TTTo2L2Nu": { 
    "EVENTS": 40819800.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  },
  "TTTo2L2NuUEUP": { 
    "EVENTS": 1, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  },
  "TTTo2L2NuUEDN": { 
    "EVENTS": 1, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  },
  "TTTo2L2NuHDUP":{ 
    "EVENTS": 1, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  },
  "TTTo2L2NuHDDN": { 
    "EVENTS": 1, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  }
}

weights = { key: config.lumi[ "16APV" ] * mc_stats[ key ][ "XSEC" ] / mc_stats[ key ][ "EVENTS" ] for key in mc_stats  }

for tt in [ "SemiLeptonic", "SemiLeptonicHT500", "SemiLeptonHT500", "Hadronic", "2L2Nu" ]:
  for fs in [ "jj", "cc", "bb", "1b", "2b" ]:
    if tt == "SemiLeptonic" and fs == "jj":
      for n in range(1,11):
        weights[ "TTTo{}tt{}{}".format( tt, fs, n ) ] = weights[ "TTTo{}".format( tt ) ]
    else:
      weights[ "TTTo{}tt{}".format( tt, fs ) ] = weights[ "TTTo{}".format( tt ) ]
    if tt in [ "SemiLeptonic", "SemiLeptonicHT500", "Hadronic", "2L2Nu" ]:
      for syst in [ "UE", "HD" ]:
        for shift in [ "DN", "UP" ]:
          weights[ "TTTo{}{}{}tt{}".format( tt, syst, shift, fs ) ] = weights[ "TTTo{}{}{}".format( tt, syst, shift ) ]
