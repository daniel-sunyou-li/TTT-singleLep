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
    "EVENTS": 638000.0, 
    "XSEC": 0.0003974 
  },
  "TTTW": { 
    "EVENTS": 710000.0, 
    "XSEC": 0.0007314
  },
  
  "TTTT": { 
    "EVENTS": 7492690.0, 
    "XSEC": 0.01197
  },
  "TTWW": { 
    "EVENTS": 910000.0, 
    "XSEC": 0.00703
  },
  "TTWZ": { 
    "EVENTS": 498000.0, 
    "XSEC": 0.002453
  },
  "TTWH": { 
    "EVENTS": 497000.0, 
    "XSEC": 0.001141
  },
  "TTHH": { 
    "EVENTS": 500000.0, 
    "XSEC": 0.0006655
  },
  "TTZH": { 
    "EVENTS": 362000.0, 
    "XSEC": 0.00113
  },
  "TTZZ": { 
    "EVENTS": 498000.0, 
    "XSEC": 0.001385
  },
  "TTWl": { 
    "EVENTS": 9687000.0, 
    "XSEC": 0.2161
  },
  "TTWq": { 
    "EVENTS": 707273.0, 
    "XSEC": 0.4377
  },
  "TTZlM10": { 
    "EVENTS": 9651834.0, 
    "XSEC": 0.05324
  },
  "TTZlM1to10": { 
    "EVENTS": 550706.0, 
    "XSEC": 0.05324
  },
  "TTHB": { 
    "EVENTS": 9292938.0, 
    "XSEC": 0.5269
  },
  "TTHnoB": { 
    "EVENTS": 7088505.0, 
    "XSEC": 0.5638
  },
  "Ts": { 
    "EVENTS": 12607741.0, 
    "XSEC": 3.44
  },
  "Tt": { 
    "EVENTS": 167505220.0, 
    "XSEC": 136.02
  },
  "Tbt": { 
    "EVENTS": 90216506.0, 
    "XSEC": 80.95
  },
  "TtW": { 
    "EVENTS": 7955614.0, 
    "XSEC": 35.83
  },
  "TbtW": { 
    "EVENTS": 7748690.0, 
    "XSEC": 35.83
  },
  
  "QCD200": { 
    "EVENTS": 57336623.0, 
    "XSEC": 1712000
  },
  "QCD300": { 
    "EVENTS": 61705174.0, 
    "XSEC": 347700
  },
  "QCD500": { 
    "EVENTS": 49184771.0, 
    "XSEC": 32100
  },
  "QCD700": { 
    "EVENTS": 48506751.0, 
    "XSEC": 6831
  },
  "QCD1000": { 
    "EVENTS": 14527915.0, 
    "XSEC": 1207
  },
  "QCD1500": { 
    "EVENTS": 10871473.0, 
    "XSEC": 119.9
  },
  "QCD2000": { 
    "EVENTS": 5374711.0, 
    "XSEC": 25.24
  },
  
  "WW": { 
    "EVENTS": 15679000.0, 
    "XSEC": 118.7
  },
  "WZ": { 
    "EVENTS": 7940000.0, 
    "XSEC": 47.13
  },
  "ZZ": { 
    "EVENTS": 3526000.0, 
    "XSEC": 16.523
  },
  
  "DYM200": { 
    "EVENTS": 18455718.0, 
    "XSEC": 54.951
  },
  "DYM400": { 
    "EVENTS": 16650005.0, 
    "XSEC": 7.862
  },
  "DYM600": { 
    "EVENTS": 7694911.0, 
    "XSEC": 1.977
  },
  "DYM800": { 
    "EVENTS": 7670311.0, 
    "XSEC": 0.858
  },
  "DYM1200": { 
    "EVENTS": 6353162.0, 
    "XSEC": 0.191
  },
  "DYM2500": { 
    "EVENTS": 2845715.0, 
    "XSEC": 0.0045
  },
  
  "WJetsMG200": { 
    "EVENTS": 107357977.0, 
    "XSEC": 359.7 * k_factor[ "WJetsMG" ]
  },
  "WJetsMG400": { 
    "EVENTS": 9901804.0, 
    "XSEC": 48.91 * k_factor[ "WJetsMG" ]
  },
  "WJetsMG600": { 
    "EVENTS": 7718765.0, 
    "XSEC": 12.05 * k_factor[ "WJetsMG" ]
  },
  "WJetsMG800": { 
    "EVENTS": 7306187.0, 
    "XSEC": 5.501 * k_factor[ "WJetsMG" ]
  },
  "WJetsMG1200": { 
    "EVENTS": 6481518.0, 
    "XSEC": 1.329 * k_factor[ "WJetsMG" ]
  },
  "WJetsMG2500": { 
    "EVENTS": 2097648.0, 
    "XSEC": 0.03216 * k_factor[ "WJetsMG" ]
  },
  
  "TTToSemiLeptonic": { 
    "EVENTS": 547148148.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9" ] )
  },
  "TTToSemiLeptonicUEUP": { 
    "EVENTS": 547148148.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9UEUP" ] )
  },
  "TTToSemiLeptonicUEDN": { 
    "EVENTS": 547148148.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9UEDN" ] )
  },
  "TTToSemiLeptonicHDUP": { 
    "EVENTS": 547148148.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9HDUP" ] )
  },
  "TTToSemiLeptonicHDDN": { 
    "EVENTS": 547148148.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9HDDN" ] )
  },
  
  "TTToSemiLeptonicHT500": { 
    "EVENTS": 547148148.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9" ] 
  },
  "TTToSemiLeptonicHT500UEUP": { 
    "EVENTS": 547148148.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9UEUP" ]
  },
  "TTToSemiLeptonicHT500UEDN": { 
    "EVENTS": 547148148.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9UEDN" ]
  },
  "TTToSemiLeptonicHT500HDUP": { 
    "EVENTS": 547148148.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9HDUP" ]
  },
  "TTToSemiLeptonicHT500HDDN": { 
    "EVENTS": 547148148.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9HDDN" ]
  },
  "TTToSemiLeptonHT500": { 
    "EVENTS": 16122362.0, 
    "XSEC": 2.251
  },
  "TTToHadronic": { 
    "EVENTS": 322629460.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ] 
  },
  "TTToHadronicUEUP": { 
    "EVENTS": 322629460.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ]
  },
  "TTToHadronicUEDN": { 
    "EVENTS": 322629460.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ]
  },
  "TTToHadronicHDUP": { 
    "EVENTS": 322629460.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ]
  },
  "TTToHadronicHDDN": { 
    "EVENTS": 322629460.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ]
  },
  
  "TTTo2L2Nu": { 
    "EVENTS": 126685058.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  },
  "TTTo2L2NuUEUP": { 
    "EVENTS": 126685058.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  },
  "TTTo2L2NuUEDN": { 
    "EVENTS": 126685058.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  },
  "TTTo2L2NuHDUP":{ 
    "EVENTS": 126685058.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  },
  "TTTo2L2NuHDDN": { 
    "EVENTS": 126685058.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  }
}

weights = { key: config.lumi[ "18" ] * mc_stats[ key ][ "XSEC" ] / mc_stats[ key ][ "EVENTS" ] for key in mc_stats  }

weights[ "TTTT1" ] = weights[ "TTTT" ]
weights[ "TTTT2" ] = weights[ "TTTT" ]

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
