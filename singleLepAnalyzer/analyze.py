#!/usr/bin/python

from ROOT import TH1D, TH2D, TTree, TFile
from array import array
import config, samples

# rTree is an instance of ROOT.TFile().Get( "ljmet" )
# year is a str = 16/17/18
# process is a str key for the sample name
# variable is a str key for the variable being binned
# shifts is a bool to use JEC/JER
# ue is a bool to use samples with Underlying Event shifts
# hdamp is a bool to use samples with HDAMP shifts
# pdf is a bool to use Parton Density Function systematics
# category is a dict with the jet multiplicity bin and lepton ID

def analyze( rTree, year, process, variable, systematics, pdf, category, verbose ):
  variableName = config.plot_params[ variable ][0]
  histBins = array( "d", config.plot_params[ variable ][1] )
  xLabel = config.plot_params[ variable ][2]

  print( ">> Processing {} for {}, {}".format( variable, year, process ) )
  print( ">> Lepton: {}".format( category[ "LEPTON" ] ) )
  print( ">> # HOT jets: {}".format( category[ "NHOT" ] ) )
  print( ">> # t jets: {}".format( category[ "NT" ] ) )
  print( ">> # W jets: {}".format( category[ "NW" ] ) )
  print( ">> # b jets: {}".format( category[ "NB" ] ) )
  print( ">> # jets: {}".format( category[ "NJ" ] ) )
  
  lumiStr = str( config.lumi[ year ] / 1000. ).replace(".","p") + "fb" # 1/fb  
  
  # define the base cuts
  weights = {
    "NOMINAL": "3" if process.startswith( "TTTo" ) else "1",
    "PROCESS": samples.weights[ process ]
  }
  if "Data" not in process: weights[ "NOMINAL" ] += " * {} * {}".format( config.mc_weight, weights[ "PROCESS" ] )
  cuts = {
    "BASE": config.base_cut,
    "NOMINAL": config.base_cut
  }
	
  # modify weights for systematic shifts
	
  if "Data" not in process:
    weights[ "NOMINAL" ] += " * {} * {}".format( config.mc_weight, weights[ "PROCESS" ] )
    weights[ "TRIGGER" ] = { "UP":   weights[ "NOMINAL" ].replace( "triggerXSF", "(triggerXSF+triggerXSFUncert)" ),
                             "DOWN": weights[ "NOMINAL" ].replace( "triggerXSF", "(triggerXSF-triggerXSFUncert)" ) }
    weights[ "PILEUP" ] = { "UP":   weights[ "NOMINAL" ].replace( "pileupWeight", "pileupWeightUp" ),
                            "DOWN": weights[ "NOMINAL" ].replace( "pileupWeight", "pileupWeightDown" ) }
    weights[ "PREFIRE" ] = { "UP":   weights[ "NOMINAL" ].replace("L1NonPrefiringProb_CommonCalc","L1NonPrefiringProbUp_CommonCalc"),
                             "DOWN": weights[ "NOMINAL" ].replace("L1NonPrefiringProb_CommonCalc","L1NonPrefiringProbDn_CommonCalc") }
    weights[ "MURFCORRD" ] = { "UP":   "renormWeights[5] * {}".format( weights[ "NOMINAL" ] ),
                               "DOWN": "renormWeights[3] * {}".format( weights[ "NOMINAL" ] ) }
    weights[ "MUR" ] = { "UP":   "renormWeights[4] * {}".format( weights[ "NOMINAL" ] ),
                         "DOWN": "renormWeights[2] * {}".format( weights[ "NOMINAL" ] ) }
    weights[ "MUF" ] = { "UP":   "renormWeights[1] * {}".format( weights[ "NOMINAL" ] ),
                         "DOWN": "renormWeights[0] * {}".format( weights[ "NOMINAL" ] ) }
    weights[ "ISR" ] = { "UP":   "renormPSWeights[0] * {}".format( weights[ "NOMINAL" ] ),
                         "DOWN": "renormPSWeights[2] * {}".format( weights[ "NOMINAL" ] ) }
    weights[ "FSR" ] = { "UP":   "renormPSWeights[1] * {}".format( weights[ "NOMINAL" ] ),
                         "DOWN": "renormPSWeights[3] * {}".format( weights[ "NOMINAL" ] ) }
    weights[ "TOPPT" ] = { "UP": "({}) * {}".format( "topPtWeight13TeV" if "TTTo" in process else "1", weights[ "NOMINAL" ] ),
                           "DOWN": "(1/{}) * {}".format( "topPtWeight13TeV" if "TTTo" in process else "1", weights[ "NOMINAL" ] ) }
    weights[ "NJET" ] = { "UP":   weights[ "NOMINAL" ],
                          "DOWN": weights[ "NOMINAL" ] }
    weights[ "NJETSF" ] = { "UP":   weights[ "NOMINAL" ],
                            "DOWN": weights[ "NOMINAL" ] }
    weights[ "CSVSHAPELF" ] = { "UP":   weights[ "NOMINAL" ].replace( "btagCSVWeight", "btagCSVWeight_LFup" ),
                                "DOWN": weights[ "NOMINAL" ].replace( "btagCSVWeight", "btagCSVWeight_LFdn" ) }
    weights[ "CSVSHAPEHF" ] = { "UP":   weights[ "NOMINAL" ].replace( "btagCSVWeight", "btagCSVWeight_HFup" ),
                                "DOWN": weights[ "NOMINAL" ].replace( "btagCSVWeight", "btagCSVWeight_HFdn" ) }
		
  # modify cuts
  if "TTToSemiLepton" in process: cuts[ "NOMINAL" ] += " && isHTgt500Njetge9 == {}".format( "1" if "HT500" in process else "0" )
  if "TTTo" in process: cuts[ "Base" ] += " && isTraining == 3"
  
  cuts[ "LEPTON" ] = " && isElectron==1" if category[ "LEPTON" ] == "E" else " && isMuon==1"
  cuts[ "NHOT" ] = " && NresolvedTops1pFake{}={}".format( ">" if "p" in category[ "NHOT" ] else "=", category[ "NHOT" ][:-1] if "p" in category[ "NHOT" ] else category[ "NHOT" ] )
  cuts[ "NT" ] = " && NJetsTtagged{}={}".format( ">" if "p" in category[ "NT" ] else "=", category[ "NT" ][:-1] if "p" in category[ "NT" ] else category[ "NT" ] )
  cuts[ "NW" ] = " && NJetsWtagged{}={}".format( ">" if "p" in category[ "NW" ] else "=", category[ "NW" ][:-1] if "p" in category[ "NW" ] else category[ "NW" ] )
  cuts[ "NB" ] = " && NJetsCSV_JetSubCalc{}={}".format( ">" if "p" in category[ "NB" ] else "=", category[ "NB" ][:-1] if "p" in category[ "NB" ] else category[ "NB" ] )
  cuts[ "NJ" ] = " && NJets_JetSubCalc{}={}".format( ">" if "p" in category[ "NJ" ] else "=", category[ "NJ" ][:-1] if "p" in category[ "NJ" ] else category[ "NJ" ] )
 
  cuts[ "NOMINAL" ] += cuts[ "LEPTON" ] + cuts[ "NHOT" ] + cuts[ "NT" ] + cuts[ "NW" ] + cuts[ "NB" ] + cuts[ "NJ" ]
    
  # modify the cuts for shifts
  cuts[ "BTAG" ] = { "UP":   cuts[ "NOMINAL" ].replace( "NJetsCSVwithSF_MultiLepCalc", "NJetsCSVwithSF_MultiLepCalc_bSFup" ),
                     "DOWN": cuts[ "NOMINAL" ].replace( "NJetsCSVwithSF_MultiLepCalc", "NJetsCSVwithSF_MultiLepCalc_bSFdn" ) }
  cuts[ "MISTAG" ] = { "UP":   cuts[ "NOMINAL" ].replace( "NJetsCSVwithSF_MultiLepCalc", "NJetsCSVwithSF_MultiLepCalc_lSFup" ),
                       "DOWN": cuts[ "NOMINAL" ].replace( "NJetsCSVwithSF_MultiLepCalc", "NJetsCSVwithSF_MultiLepCalc_lSFdn" ) }
  cuts[ "TAU21" ] = { "UP":   cuts[ "NOMINAL" ].replace( "NJetsWtagged", "NJetsWtagged_shifts[0]" ),
                      "DOWN": cuts[ "NOMINAL" ].replace( "NJetsWtagged", "NJetsWtagged_shifts[1]" ) }
  cuts[ "JMSW" ] = { "UP":   cuts[ "NOMINAL" ].replace( "NJetsWtagged", "NJetsWtagged_shifts[2]" ),
                     "DOWN": cuts[ "NOMINAL" ].replace( "NJetsWtagged", "NJetsWtagged_shifts[3]" ) }
  cuts[ "JMRW" ] = { "UP":   cuts[ "NOMINAL" ].replace( "NJetsWtagged", "NJetsWtagged_shifts[4]" ),
                     "DOWN": cuts[ "NOMINAL" ].replace( "NJetsWtagged", "NJetsWtagged_shifts[5]" ) }
  cuts[ "TAU21PT" ] = { "UP":   cuts[ "NOMINAL" ].replace( "NJetsWtagged", "NJetsWtagged_shifts[6]" ),
                        "DOWN": cuts[ "NOMINAL" ].replace( "NJetsWtagged", "NJetsWtagged_shifts[7]" ) }
  cuts[ "TAU32" ] = { "UP":   cuts[ "NOMINAL" ].replace( "NJetsTtagged", "NJetsTtagged_shifts[0]" ),
                      "DOWN": cuts[ "NOMINAL" ].replace( "NJetsTtagged", "NJetsTtagged_shifts[1]" ) }
  cuts[ "JMST" ] = { "UP":   cuts[ "NOMINAL" ].replace( "NJetsTtagged", "NJetsTtagged_shifts[2]" ),
                     "DOWN": cuts[ "NOMINAL" ].replace( "NJetsTtagged", "NJetsTtagged_shifts[3]" ) }
  cuts[ "JMRT" ] = { "UP":   cuts[ "NOMINAL" ].replace( "NJetsTtagged", "NJetsTtagged_shifts[4]" ),
                     "DOWN": cuts[ "NOMINAL" ].replace( "NJetsTtagged", "NJetsTtagged_shifts[5]" ) }
  cuts[ "HOTSTAT" ] = { "UP":   cuts[ "NOMINAL" ].replace( "NresolvedTops1pFake", "NresolvedTops1pFake_shifts[0]" ),
                        "DOWN": cuts[ "NOMINAL" ].replace( "NresolvedTops1pFake", "NresolvedTops1pFake_shifts[1]" ) }
  cuts[ "HOTCSPUR" ] = { "UP":   cuts[ "NOMINAL" ].replace( "NresolvedTops1pFake", "NresolvedTops1pFake_shifts[2]" ),
                         "DOWN": cuts[ "NOMINAL" ].replace( "NresolvedTops1pFake", "NresolvedTops1pFake_shifts[3]" ) }
  cuts[ "HOTCLOSURE" ] = { "UP":   cuts[ "NOMINAL" ].replace( "NresolvedTops1pFake", "NresolvedTops1pFake_shifts[4]" ),
                           "DOWN": cuts[ "NOMINAL" ].replace( "NresolvedTops1pFake", "NresolvedTops1pFake_shifts[5]" ) }
	
  if nbtag == "0" and "minmlb" in iPlot.lower():
  originalLJMETName = plotTreeName
  plotTreeName = "minMleppJet"
    
  # declare histograms
  hists = {}
  with "{}_{}_{}_{}".format( variable, lumiStr, catStr, process ) as key:
    hists[ key ] = TH1D( key, xAxisLabel, len(xbins) - 1, xbinS )
  if doAllSys:
    for syst in systList:
      for dir in [ "Up","Down" ]:
        with "{}_{}_{}_{}".format( iPlot+syst+dir, lumiStr, catStr, process ) as key:
          hists[ key ] = TH1D( key, xAxisLabel, len(xbins) - 1, xbins )
  if doPDF:
    for i in range(100):
      with "{}pdf{}_{}_{}_{}".format( iPlot, i, lumiStr, catStr, process ) as key:
        hists[ key ] = TH1D( key, xAxisLabel, len(xbins) - 1, xbins )
				
  # Sumw2() tells the hist to also store the sum of squares of weights
  for key in hists: hists[ key ].Sumw2()
		
  # draw histograms
  rootTree[process].Draw( "{} >> {}_{}_{}_{}".format(plotTreeName,iPlot,lumiStr,catStr,process), "{} * ( {} )".format( weights[ "Nominal" ], cuts[ "Nominal" ] ), "GOFF" )
  if verbose: print("[OK ] Finished drawing nominal histogram" )

  if doAllSys:
    for syst in systList:
      for dir in [ "Up", "Down" ]:
        with "{}_{}_{}_{}".format( iPlot + syst + dir, lumiStr, catStr, process ) as key:
          if syst in [ "pileup", "prefire", "muRFcorrd", "muR", "muF", "isr", "fsr", "njet", "njetsf", "CSVshapelf", "CSVshapehf" ]:
            rootTree[ process ].Draw( "{} >> {}".format( plotTreeName, key ), "{} * ({})".format( weights[ syst ][ dir ], cuts[ "Nominal" ] ), "GOFF" )
          # hot-tagging plots
          if ( syst in [ "hotstat", "hotcspur", "hotclosure" ] ) and ( nhott != "0p" ):
            rootTree[ process ].Draw( "{} >> {}".format( plotTreeName, key ), "{} * ({})".format( weights[ "Nominal" ], cuts[ syst ][ dir ] ), "GOFF" )
          # t-tagging plots
          if ( syst in [ "tau32", "jmst", "jmrt" ] ) and ( nttag != "0p" ):
            if "ttagged" in plotTreeName.lower() or "tjet" in plotTreeName.lower():
              shift_indx = 2*np.argwhere( np.array([ "tau32", "jmst", "jmrt" ]) == syst )[0,0] + np.argwhere( np.array([ "Up", "Down" ]) == dir )[0,0]
              rootTree[ process ].Draw( "{}_shifts[{}] >> {}".format( plotTreeName, shift_indx, key ), "{} * ({})".format( weights[ "Nominal" ], cuts[ syst ][ dir ] ), "GOFF" )
            else: rootTree[ process ].Draw( "{} >> {}".format( plotTreeName, key ), "{} * ({})".format( weights[ "Nominal" ], cuts[ syst ][ dir ] ), "GOFF" )
          # W-tagging plots
          if ( syst in [ "tau21", "jmsW", "jmrW", "tau21pt" ] ) and ( nWtag != "0p" ):
            if "wtagged" in plotTreeName.lower() or "wjet" in plotTreeName.lower():
              shift_indx = 2*np.argwhere( np.array([ "tau21", "jmsW", "jmrW", "tau21pt" ]) == syst )[0,0] + np.argwhere( np.array([ "Up", "Down" ]) == dir )[0,0]
              rootTree[ process ].Draw( "{}_shifts[{}] >> {}".format( plotTreeName, shift_indx, key ), "{} * ({})".format( weights[ "Nominal" ], cuts[ syst ][ dir ] ), "GOFF" )
            else: rootTree[ process ].Draw( "{} >> {}".format( plotTreeName, key ), "{} * ({})".format( weights[ "Nominal" ], cuts[ syst ][ dir ] ), "GOFF" )
          # b-tagging plots
          if ( syst in [ "btag", "mistag" ] ) and ( nbtag != "0p" ):
            if "csvwithsf" in plotTreeName.lower() or "htag" in plotTreeName.lower() or "mleppb" in plotTreeName.lower() or "bjetlead" in plotTreeName.lower() or "minmlb" in plotTreeName.lower():
              if syst == "btag": rootTree[ process ].Draw( "{}_bSF{} >> {}".format( plotTreeName, dir.lower(), key ), "{} * ({})".format( weights[ "Nominal" ], cut[ syst ][ dir ] ), "GOFF" )
              if syst == "mistag": rootTree[ process ].Draw( "{}_lSF{} >> {}".format( plotTreeName, dir.lower(), key ), "{} * ({})".format( weights[ "Nominal" ], cut[ syst ][ dir ] ), "GOFF" )
            else: rootTree[ process ].Draw( "{} >> {}".format( plotTreeName, key ), "{} * ({})".format( weights[ "Nominal" ], cuts[ syst ][ dir ] ), "GOFF" )
          # process jec and jer
          if ( syst in [ "jec", "jer" ] ) and rootTree[ process + syst + dir ]: rootTree.Draw( "{} >> {}".format( plotTreeName, key ), "{} * ({})".format( weights[ "Nominal" ], cuts[ "Nominal" ] ), "GOFF" )
    print( "[OK ] Finished drawing systematic histograms" )
	
  if doPDF:
    for i in range(100):
      with "{}pdf{}_{}_{}_{}".format( iPlot, i, lumiStr, catStr, process ) as key:
        rootTree[ process ].Draw( "{} >> {}".format( plotTreeName, key ), "pdfWeights[{}] * {} * ({})".format( i, weights[ "Nominal" ], cuts[ "Nominal" ] ), "GOFF" )
    print( "[OK ] Finished drawing PDF histograms" )
							
  for key in hists: hists[ key ].SetDirectory(0)
  if verbose: print( "[OK ] Finished" )
  return hists
