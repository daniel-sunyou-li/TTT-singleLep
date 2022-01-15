#!/usr/bin/python

xsec[ "TT" ] = 831.8

BR = { 
  "TT": {
    "SemiLeptonic": 0.438,
    "Hadronic": 0.457,
    "2L2Nu": 0.105
  }
}

filtEff_tt = {
  "Njet9": 0.00617938417682763,
  "Njet9_HDDN": 0.005645170035947885,
  "Njet9_HDUP": 0.006711348259851689,
  "Njet9_UEDN": 0.006108623095875414,
  "Njet9_UEUP": 0.0062286452403598055 
}

k_factor = {
  "WJets": 1.21
}

mc_stats = {
  "TTTJ": { 
    "EVENTS": 354000., 
    "XSEC": 0.0003974 
  },
  "TTTW": { 
    "EVENTS": 360000., 
    "XSEC": 0.0007314
  },
  
  "TTTT": { 
    "EVENTS": 4526556., 
    "XSEC": 0.01197
  },
  "TTWW": { 
    "EVENTS": 698000., 
    "XSEC": 0.00703
  },
  "TTWZ": { 
    "EVENTS": 350000., 
    "XSEC": 0.002453
  },
  "TTWH": { 
    "EVENTS": 360000., 
    "XSEC": 0.001141
  },
  "TTHH": { 
    "EVENTS": 360000., 
    "XSEC": 0.0006655
  },
  "TTZH": { 
    "EVENTS": 350000., 
    "XSEC": 0.00113
  },
  "TTZZ": { 
    "EVENTS": 327000., 
    "XSEC": 0.001385
  },
  "TTWl": { 
    "EVENTS": 6497731., 
    "XSEC": 0.2161
  },
  "TTWq": { 
    "EVENTS": 359006., 
    "XSEC": 0.4377
  },
  "TTZlM10": { 
    "EVENTS": 6990534., 
    "XSEC": 0.05324
  },
#  "TTZlM1to10": { 
#    "EVENTS": 0., 
#    "XSEC": 0.05324
#  },
  "TTHBB": { 
    "EVENTS": 7661779., 
    "XSEC": 0.5269
  },
  "TTHnoBB": { 
    "EVENTS": 4965389., 
    "XSEC": 0.5638
  },
  "Ts": { 
    "EVENTS": 8938338., 
    "XSEC": 3.44
  },
  "Tt": { 
    "EVENTS": 121728252.0, 
    "XSEC": 136.02
  },
  "Tbt": { 
    "EVENTS": 65821722., 
    "XSEC": 80.95
  },
  "TtW": { 
    "EVENTS": 5648712., 
    "XSEC": 35.83
  },
  "TbtW": { 
    "EVENTS": 5673700., 
    "XSEC": 35.83
  },
  
  "QCD200": { 
    "EVENTS": 42714435., 
    "XSEC": 1712000
  },
  "QCD300": { 
    "EVENTS": 43589739.0, 
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
    "EVENTS": 10256089.0, 
    "XSEC": 1207
  },
  "QCD1500": { 
    "EVENTS": 7701876., 
    "XSEC": 119.9
  },
  "QCD2000": { 
    "EVENTS": 4112573.0, 
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
    "EVENTS": 12513057., 
    "XSEC": 54.951
  },
  "DYM400": { 
    "EVENTS": 5543804., 
    "XSEC": 7.862
  },
  "DYM600": { 
    "EVENTS": 5278417., 
    "XSEC": 1.977
  },
  "DYM800": { 
    "EVENTS": 4506887., 
    "XSEC": 0.858
  },
  "DYM1200": { 
    "EVENTS": 4802716., 
    "XSEC": 0.191
  },
  "DYM2500": { 
    "EVENTS": 1480047., 
    "XSEC": 0.0045
  },
  
  "WJets200": { 
    "EVENTS": 42602407., 
    "XSEC": 359.7 * k_factor[ "WJets" ]
  },
  "WJets400": { 
    "EVENTS": 5437447., 
    "XSEC": 48.91 * k_factor[ "WJets" ]
  },
  "WJets600": { 
    "EVENTS": 5545298., 
    "XSEC": 12.05 * k_factor[ "WJets" ]
  },
  "WJets800": { 
    "EVENTS": 5088483.0, 
    "XSEC": 5.501 * k_factor[ "WJets" ]
  },
  "WJets1200": { 
    "EVENTS": 4942590., 
    "XSEC": 1.329 * k_factor[ "WJets" ]
  },
  "WJets2500": { 
    "EVENTS": 1185699.0, 
    "XSEC": 0.03216 * k_factor[ "WJets" ]
  },
  
  "TTToSemiLeptonic": { 
    "EVENTS": 352212660.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9" ] )
  },
  "TTToSemiLeptonic_UEUP": { 
    "EVENTS": 137475034.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9_UEUP" ] )
  },
  "TTToSemiLeptonic_UEDN": { 
    "EVENTS": 131182302.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9_UEDN" ] )
  },
  "TTToSemiLeptonic_HDUP": { 
    "EVENTS": 132383014.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9_HDUP" ] )
  },
  "TTToSemiLeptonic_HDDN": { 
    "EVENTS": 132018269.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * ( 1.0 - filtEff_tt[ "Njet9_HDDN" ] )
  },
  
  "TTToSemiLeptonicHT500": { 
    "EVENTS": 352212660, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9" ] 
  },
  "TTToSemiLeptonicHT500_UEUP": { 
    "EVENTS": 137475034.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9_UEUP" ]
  },
  "TTToSemiLeptonicHT500_UEDN": { 
    "EVENTS": 131182302.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9_UEDN" ]
  },
  "TTToSemiLeptonicHT500_HDUP": { 
    "EVENTS": 132383014.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9_HDUP" ]
  },
  "TTToSemiLeptonicHT500_HDDN": { 
    "EVENTS": 132018269.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "SemiLeptonic" ] * filtEff_tt[ "Njet9_HDDN" ]
  },
  
  "TTToSemiLeptonHT500": { 
    "EVENTS": 10179200, 
    "XSEC": 2.251
  },
  
  "TTToHadronic": { 
    "EVENTS": 233815417., 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ] 
  },
  "TTToHadronic_UEUP": { 
    "EVENTS": 95498399.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ]
  },
  "TTToHadronic_UEDN": { 
    "EVENTS": 94308036.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ]
  },
  "TTToHadronic_HDUP": { 
    "EVENTS": 99030356.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ]
  },
  "TTToHadronic_HDDN": { 
    "EVENTS": 93721302.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "Hadronic" ]
  },
  
  "TTTo2L2Nu": { 
    "EVENTS": 44580106. + 28515514. + 51439568. + 47012288. + 25495972., 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  },
  "TTTo2L2Nu_UEUP": { 
    "EVENTS": 42495090.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  },
  "TTTo2L2Nu_UEDN": { 
    "EVENTS": 39078720.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  },
  "TTTo2L2Nu_HDUP":{ 
    "EVENTS": 40026124.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  },
  "TTTo2L2Nu_HDDN": { 
    "EVENTS": 39960772.0, 
    "XSEC": xsec[ "TT" ] * BR[ "TT" ][ "2L2Nu" ]
  }
}

weights = { key: config.lumi[ "17" ] * mc_stats[ key ][ "XSEC" ] / mc_stats[ key ][ "EVENTS" ] for key in mc_stats  }

for tt in [ "SemiLeptonic", "SemiLeptonicHT500", "SemiLeptonHT500", "Hadronic", "2L2Nu" ]:
  for fs in [ "jj", "cc", "bb", "1b", "2b" ]:
    if tt == "SemiLeptonic":
      for n in [ "1", "2", "3", "4" ]:
        weight[ "{}_tt{}{}".format( tt, fs, n ) ] = weight[ tt ]
    else:
      weight[ "{}_tt{}".format( tt, fs ) ] = weight[ tt ]
    if tt in [ "SemiLeptonic", "SemiLeptonicHT500", "Hadronic", "2L2Nu" ]:
      for syst in [ "UE", "HD" ]:
        for shift in [ "DN", "UP" ]:
          weight[ "{}_tt{}_{}{}".format( tt, fs, syst, shift ) ] = weight[ "{}_{}{}".format( tt, syst, shift ) ]
xsec['TTTJ'] = 0.0004741 # from McM
xsec['TTTW'] = 0.0007330 # from McM
xsec['TTHH'] = 0.0007565 # from https://arxiv.org/pdf/1610.07922.pdf (NLO QCD)
xsec['TTWH'] = 0.001582 # from https://arxiv.org/pdf/1610.07922.pdf (NLO QCD)
xsec['TTZH'] = 0.001535 # from https://arxiv.org/pdf/1610.07922.pdf (NLO QCD)
xsec['TTWW'] = 0.011500 # from https://arxiv.org/pdf/1610.07922.pdf (NLO QCD 4f)
xsec['TTWZ'] = 0.003884 # from https://arxiv.org/pdf/1610.07922.pdf (NLO QCD)
xsec['TTZZ'] = 0.001982 # from https://arxiv.org/pdf/1610.07922.pdf (NLO QCD)

#4 Tops
xsec['tttt'] = 0.012 # from https://arxiv.org/pdf/1711.02116.pdf, in McM: 0.008213

xsec['X53LHM700'] = 0.455 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM700'] = 0.455 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM800'] = 0.196 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM800'] = 0.196 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM900'] = 0.0903 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM900'] = 0.0903 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM1000'] = 0.0440 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM1000'] = 0.0440 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM1100'] = 0.0224 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM1100'] = 0.0224 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM1200'] = 0.0118 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM1200'] = 0.0118 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM1300'] = 0.00639 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM1300'] = 0.00639 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM1400'] = 0.00354 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM1400'] = 0.00354 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM1500'] = 0.00200 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM1500'] = 0.00200 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM1600'] = 0.001148 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM1600'] = 0.001148 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM1700'] = 0.000666
xsec['X53RHM1700'] = 0.000666

# Calculate lumi normalization weights
weight = {}
for sample in sorted(nRun.keys()): 
	weight[sample] = (targetlumi*xsec[sample]) / (nRun[sample])

weight['WJetsMG12001'] = weight['WJetsMG1200']
weight['WJetsMG12002'] = weight['WJetsMG1200']
weight['WJetsMG12003'] = weight['WJetsMG1200']
weight['WJetsMG25001'] = weight['WJetsMG2500'] 
weight['WJetsMG25002'] = weight['WJetsMG2500'] 
weight['WJetsMG25003'] = weight['WJetsMG2500'] 
weight['WJetsMG25004'] = weight['WJetsMG2500']

for flv in ['jj','cc','bb','1b','2b']:
	weight['TTJets2L2nuTT'+flv] = weight['TTJets2L2nu']
	weight['TTJetsHadTT'+flv] = weight['TTJetsHad']
	weight['TTJetsSemiLepTT'+flv] = weight['TTJetsSemiLep']
	weight['TTJetsSemiLepNjet0TT'+flv] = weight['TTJetsSemiLepNjet0']
	weight['TTJetsSemiLepNjet9TT'+flv] = weight['TTJetsSemiLepNjet9']
	weight['TTJetsSemiLepNjet9binTT'+flv] = weight['TTJetsSemiLepNjet9bin']
	for syst in ['UEdn','UEup','HDAMPdn','HDAMPup']:
		weight['TTJets2L2nu'+syst+'TT'+flv] = weight['TTJets2L2nu'+syst]
		weight['TTJetsHad'+syst+'TT'+flv] = weight['TTJetsHad'+syst]
		weight['TTJetsSemiLep'+syst+'TT'+flv] = weight['TTJetsSemiLep'+syst]
		weight['TTJetsSemiLep'+syst+'Njet0TT'+flv] = weight['TTJetsSemiLep'+syst+'Njet0']
		weight['TTJetsSemiLep'+syst+'Njet9TT'+flv] = weight['TTJetsSemiLep'+syst+'Njet9']
		weight['TTJetsSemiLep'+syst+'Njet9binTT'+flv] = weight['TTJetsSemiLep'+syst+'Njet9bin']

weight['TTJetsSemiLepNjet0TTjj1'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet0TTjj2'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet0TTjj3'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet0TTjj4'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet0TTjj5'] = weight['TTJetsSemiLepNjet0']

for sample in weight.keys():
        if 'TTJetsSemiLep' in sample and ('Njet0TT' in sample or 'Njet9TT' in sample):
                weight[sample.replace('TTJetsSemiLep','TTJetsSemiLepInc')] = weight[sample[:sample.find('Njet')]]
