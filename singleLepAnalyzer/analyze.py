#!/usr/bin/python

from ROOT import TH1D, TH2D, TTree, TFile
from array import array
import config, samples

# rTree is an instance of ROOT.TFile().Get( "ljmet" )
# year is a str = 16/17/18
# process is a str key for the sample name
# variable is a str key for the variable being binned
# doSYST is a bool to process full list of systematics
# doPDF is a bool to use Parton Density Function systematics
# category is a dict with the jet multiplicity bin and lepton ID

def analyze( rTree, year, process, variable, doSYST, doPDF, category, verbose ):
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
  
  # modify weights
  weights = {
    "NOMINAL": "3" if process.startswith( "TTTo" ) else "1", # weights only applied to MC
    "PROCESS": samples.weights[ process ] # weight specific to physics process and adjusted to target luminosity
  }
  if "data" not in process.lower(): 
    weights[ "NOMINAL" ] += " * {} * {}".format( config.mc_weight, weights[ "PROCESS" ] )
	
  if "data" not in process.lower():
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
    # deep jet related systematics
    for syst in [ "LF", "lfstats1", "lfstats2", "HF", "hfstats1", "hfstats2", "cferr1", "cferr2", "jes" ]:
      for shift in [ "up", "dn" ]:
        weights[ syst.upper() ][ shift.upper() ] = weights[ "NOMINAL" ].replace( "btagDeepJetWeight", "btagDeepJetWeight_" + syst + shift ).replace( "btagDeepJet2DWeight_HTnj", "btagDeepJet2DWeight_HTnj_" + syst + shift )
  
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
  lumiStr = str( config.lumi[ year ] / 1000. ).replace(".","p") + "fb" # 1/fb  
  categoryTag = "is{}nJ{}nB{}nT{}nH{}nW{}".format( 
    category[ "LEPTON" ], category[ "NJ" ], category[ "NB" ],
    category[ "NT" ], category[ "NHOT" ], category[ "NW" ] 
  )
  histTag = "{}_{}_{}_{}".format( variable, lumiStr, categoryTag, process )
  hists[ histTag ] = TH1D( histTag, xLabel, len( histBins ) - 1, histBins )
  if doSYST:
    for syst in config.systematics:
      for shift in [ "UP", "DOWN" ]:
        histTag = "{}_{}_{}_{}_{}".format( variable, syst.upper() + shift, lumiStr, categoryTag, process )
        hists[ histTag ] = TH1D( histTag, xLabel, len( histBins ) - 1, histBins )
  if doPDF:
    for i in range( config.pdf_range ):
      histTag = "{}_PDF{}_{}_{}".format( variable, i, lumiStr, categoryTag, process )
      hists[ histTag ] = TH1D( histTag, xLabel, len( histBins ) - 1, histBins )
				
  # Sumw2() tells the hist to also store the sum of squares of weights
  for histTag in hists: hists[ histTag ].Sumw2()
		
  # draw histograms
  rTree[ process ].Draw( 
    "{} >> {}_{}_{}_{}".format( variableName, variable ,lumiStr, categoryTag, process ), 
    "{} * ( {} )".format( weights[ "NOMINAL" ], cuts[ "NOMINAL" ] ), 
    "GOFF" )
  if verbose: print("[OK ] Finished drawing nominal histogram" )

  if doSYST:
    for syst in config.systematics:
      for shift in [ "UP", "DOWN" ]:
        histTag = "{}_{}_{}_{}_{}".format( variable, syst.upper() + shift, lumiStr, categoryTag, process )
        if syst.upper() in [ "PILEUP", "PREFIRE", "MURFCORRD", "MUR", "MUF", "ISR", "FSR", "NJET", "NJETSF", "CSVSHAPELF", "CSVSHAPEHF" ]:
          rTree[ process ].Draw( 
            "{} >> {}".format( variableName, histTag ), 
            "{} * ({})".format( weights[ syst.upper() ][ shift ], cuts[ "NOMINAL" ] ), 
            "GOFF" )
        # hot-tagging plots
        if ( syst.upper() in [ "HOTSTAT", "HOTCSPUR", "HOTCLOSURE" ] ) and ( category[ "NHOT" ] != "0p" ):
          rTree[ process ].Draw( 
            "{} >> {}".format( variableName, histTag ), 
            "{} * ({})".format( weights[ "NOMINAL" ], cuts[ syst.upper() ][ shift ] ), 
            "GOFF" )
        # t-tagging plots
        if ( syst.upper() in [ "TAU32", "JMST", "JMRT" ] ) and ( category[ "NT" ] != "0p" ):
          if "ttagged" in variableName.lower() or "tjet" in variableName.lower():
            shift_indx = 2*np.argwhere( np.array([ "TAU32", "JMST", "JMRT" ]) == syst.upper() )[0,0] + np.argwhere( np.array([ "UP", "DOWN" ]) == shift )[0,0]
            rTree[ process ].Draw( 
              "{}_shifts[{}] >> {}".format( variableName, shift_indx, histTag ), 
              "{} * ({})".format( weights[ "NOMINAL" ], cuts[ syst.upper() ][ shift ] ), 
              "GOFF" )
          else: 
            rTree[ process ].Draw( 
              "{} >> {}".format( variableName, histTag ), 
              "{} * ({})".format( weights[ "NOMINAL" ], cuts[ syst.upper() ][ shift ] ), 
              "GOFF" )
        # W-tagging plots
        if ( syst in [ "TAU21", "JMSW", "JMRW", "TAU21PT" ] ) and ( category[ "NW" ] != "0p" ):
          if "wtagged" in variableName.lower() or "wjet" in variableName.lower():
            shift_indx = 2*np.argwhere( np.array([ "TAU21", "JMSW", "JMRW", "TAU21PT" ]) == syst.upper() )[0,0] + np.argwhere( np.array([ "UP", "DOWN" ]) == shift )[0,0]
            rTree[ process ].Draw( 
              "{}_shifts[{}] >> {}".format( variableName, shift_indx, histTag ), 
              "{} * ({})".format( weights[ "NOMINAL" ], cuts[ syst.upper() ][ shift ] ), 
              "GOFF" )
          else: rTree[ process ].Draw( 
            "{} >> {}".format( variableName, histTag ), 
            "{} * ({})".format( weights[ "NOMINAL" ], cuts[ syst.upper() ][ shift ] ), 
            "GOFF" )
        # b-tagging plots
        if ( syst.upper() in [ "BTAG", "MISTAG" ] ) and ( category[ "NB" ] != "0p" ):
          if "csvwithsf" in variableName.lower() or "htag" in variableName.lower() or "mleppb" in variableName.lower() or "bjetlead" in variableName.lower() or "minmlb" in variableName.lower():
            if syst.upper() == "BTAG": rTree[ process ].Draw( 
              "{}_bSF{} >> {}".format( variableName, shift.lower(), histTag ), 
              "{} * ({})".format( weights[ "NOMINAL" ], cut[ syst.upper() ][ shift ] ), 
              "GOFF" )
            if syst.upper() == "MISTAG": rTree[ process ].Draw( 
              "{}_lSF{} >> {}".format( variableName, shift.lower(), histTag ), 
              "{} * ({})".format( weights[ "NOMINAL" ], cut[ syst.upper() ][ shift ] ), 
              "GOFF" )
          else: rTree[ process ].Draw( 
            "{} >> {}".format( variableName, histTag ), 
            "{} * ({})".format( weights[ "NOMINAL" ], cuts[ syst.upper() ][ shift ] ), 
            "GOFF" )
        # process jec and jer
        if ( syst in [ "JEC", "JER" ] ) and rTree[ process + syst.upper() + shift.upper() ]: rTree.Draw( 
          "{} >> {}".format( variableName, histTag ), 
          "{} * ({})".format( weights[ "NOMINAL" ], cuts[ "NOMINAL" ] ), 
          "GOFF" )
  print( "[OK ] Finished drawing systematic histograms" )
	
  if doPDF:
    for i in range( config.pdf_range ):
      histTag = "{}pdf{}_{}_{}_{}".format( variable, i, lumiStr, categoryTag, process )
      rTree[ process ].Draw( 
        "{} >> {}".format(variableName, histTag ), 
        "pdfWeights[{}] * {} * ({})".format( i, weights[ "NOMINAL" ], cuts[ "NOMINAL" ] ), 
        "GOFF" )
    print( "[OK ] Finished drawing PDF histograms" )
							
  for key in hists: hists[ key ].SetDirectory(0)
  if verbose: print( "[OK ] Finished" )
  return hists
