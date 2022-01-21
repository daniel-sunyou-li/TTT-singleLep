#!/usr/bin/python

import os, sys, time, math, datetime, pickle, itertools, getopt
import numpy as np
from array import array
from argparse import ArgumentParser

sys.path.append( os.path.dirname( "../" ) ) 

import utils
import config

parser = ArgumentParser()
parser.add_argument( "-v", "--variable", default = "HT" )
parser.add_argument( "-y", "--year", default = "17" )
parser.add_argument( "-l", "--lepton", default = "E" )
parser.add_argument( "-nh", "--nhot", default = "0p" )
parser.add_argument( "-nt", "--nt", default = "0p" )
parser.add_argument( "-nw", "--nw", default = "0p" )
parser.add_argument( "-nb", "--nb", default = "2p" )
parser.add_argument( "-nj", "--nj", default = "5p" )
parser.add_argument( "-sd", "--subDir" )
args = parser.parse_args()

if args.year == "16":
  import weightsUL16 as weights
  import samplesUL16 as samples
elif args.year == "17":
  import weightsUL17 as weights
  import samplesUL17 as samples
elif args.year == "18":
  import weightsUL18 as weights
  import samplesUL18 as samples
else:
  quit( "[ERR] Invalid -y (--year) option used. Quitting..." )

import ROOT

"""
Note: 
--Each process in step1 (or step2) directories should have the root files hadded! 
--The code will look for <step1Dir>/<process>_hadd.root for nominal trees.
The uncertainty shape shifted files will be taken from <step1Dir>/../<shape>/<process>_hadd.root,
where <shape> is for example "JECUp". hadder.py can be used to prepare input files this way! 
--Each process given in the lists below must have a definition in "samples.py"
--Check the set of cuts in "analyze.py"
"""

ROOT.gROOT.SetBatch(1)
start_time = time.time()

category = {
  "LEPTON": [ args.lepton ],
  "NHOT": [ args.nhot ],
  "NT": [ args.nt ],
  "NW": [ args.nw ],
  "NB": [ args.nb ],
  "NJ": [ args.nj ]
}

groups = {
  "DATA": [ str( process ) for process in samples.samples[ "DATA" ] ],
  "SIGNAL": [ str( process ) for process in samples.samples[ "SIGNAL" ] ],
  "BACKGROUND": [ str( process ) for process in samples.samples[ "BACKGROUND" ] if ( "UE" not in str( process ) and "HD" not in str( process ) ) ],
  "UE": [ str( process ) for process in samples.samples[ "BACKGROUND" ] if "UE" in str( process ) ],
  "HD": [ str( process ) for process in samples.samples[ "BACKGROUND" ] if "HD" in str( process ) ],
  "TEST": [ str( process ) for process in samples.samples[ "TEST" ] ]
}

backgrounds = list( samples.samples[ "BACKGROUND" ].keys() )
hdamp = list( samples.samples[ "HD" ].keys() )
ue = list( samples.samples[ "UE" ].keys() )
signals = list( samples.samples[ "SIGNAL" ].keys() )
data = list( samples.samples[ "DATA" ].keys() )
         		
def read_tree( samplePath ):
  if not os.path.exists( samplePath ):
    print("[ERR] {} does not exist.  Exiting program...".format( samplePath ) )
    sys.exit(1)
  rootFile = ROOT.TFile.Open( samplePath, "READ" )
  rootTree = rootFile.Get( "ljmet" )
  return rootFile, rootTree

def analyze( rTree, year, process, variable, doSYST, doPDF, category, verbose ):
  variableName = config.plot_params[ variable ][0]
  histBins = array( "d", config.plot_params[ variable ][1] )
  xLabel = config.plot_params[ variable ][2]

  print( ">> Processing {} for 20{} {}".format( variable, year, process ) )
  
  # modify weights
  mc_weights = { "NOMINAL": "3" if process.startswith( "TTTo" ) else "1" } # weights only applied to MC
  if process in weights.weights.keys():
    mc_weights[ "PROCESS" ] = "{:.10f}".format( weights.weights[ process ] ) 
  else:
    mc_weights[ "PROCESS" ] = "1"

  if process not in list( samples.samples[ "DATA" ].keys() ):
    mc_weights[ "NOMINAL" ] += "*{}*{}".format( config.mc_weight, mc_weights[ "PROCESS" ] )

  if process not in list( samples.samples[ "DATA" ].keys() ) and doSYST:
    #mc_weights[ "TRIGGER" ] = { "UP": weights[ "NOMINAL" ].replace( "triggerXSF", "(triggerXSF+triggerXSFUncert)" ),
    #                           "DN": weights[ "NOMINAL" ].replace( "triggerXSF", "(triggerXSF-triggerXSFUncert)" ) }
    mc_weights[ "PILEUP" ] = { "UP": mc_weights[ "NOMINAL" ].replace( "pileupWeight", "pileupWeightUp" ),
                               "DN": mc_weights[ "NOMINAL" ].replace( "pileupWeight", "pileupWeightDown" ) }
    mc_weights[ "PREFIRE" ] = { "UP": mc_weights[ "NOMINAL" ].replace("L1NonPrefiringProb_CommonCalc","L1NonPrefiringProbUp_CommonCalc"),
                                "DN": mc_weights[ "NOMINAL" ].replace("L1NonPrefiringProb_CommonCalc","L1NonPrefiringProbDn_CommonCalc") }
    mc_weights[ "MURFCORRD" ] = { "UP": "renormWeights[5] * {}".format( mc_weights[ "NOMINAL" ] ),
                                  "DN": "renormWeights[3] * {}".format( mc_weights[ "NOMINAL" ] ) }
    mc_weights[ "MUR" ] = { "UP": "renormWeights[4] * {}".format( mc_weights[ "NOMINAL" ] ),
                            "DN": "renormWeights[2] * {}".format( mc_weights[ "NOMINAL" ] ) }
    mc_weights[ "MUF" ] = { "UP": "renormWeights[1] * {}".format( mc_weights[ "NOMINAL" ] ),
                            "DN": "renormWeights[0] * {}".format( mc_weights[ "NOMINAL" ] ) }
    mc_weights[ "ISR" ] = { "UP": "renormPSWeights[0] * {}".format( mc_weights[ "NOMINAL" ] ),
                            "DN": "renormPSWeights[2] * {}".format( mc_weights[ "NOMINAL" ] ) }
    mc_weights[ "FSR" ] = { "UP": "renormPSWeights[1] * {}".format( mc_weights[ "NOMINAL" ] ),
                            "DN": "renormPSWeights[3] * {}".format( mc_weights[ "NOMINAL" ] ) }
    mc_weights[ "TOPPT" ] = { "UP": "({}) * {}".format( "topPtWeight13TeV" if "TTTo" in process else "1", mc_weights[ "NOMINAL" ] ),
                              "DN": "(1/{}) * {}".format( "topPtWeight13TeV" if "TTTo" in process else "1", mc_weights[ "NOMINAL" ] ) }
    mc_weights[ "NJET" ] = { "UP": mc_weights[ "NOMINAL" ],
                             "DN": mc_weights[ "NOMINAL" ] }
    mc_weights[ "NJETSF" ] = { "UP": mc_weights[ "NOMINAL" ],
                               "DN": mc_weights[ "NOMINAL" ] }
    # deep jet related systematics
    for syst in [ "LF", "lfstats1", "lfstats2", "HF", "hfstats1", "hfstats2", "cferr1", "cferr2", "jes" ]:
      mc_weights[ syst.upper() ] = {}
      for shift in [ "up", "dn" ]:
        mc_weights[ syst.upper() ][ shift.upper() ] = mc_weights[ "NOMINAL" ].replace( "btagDeepJetWeight", "btagDeepJetWeight_" + syst + shift ).replace( "btagDeepJet2DWeight_HTnj", "btagDeepJet2DWeight_HTnj_" + syst + shift )
  
  # modify cuts
  cuts = { "BASE": config.base_cut }
  if "TTToSemiLepton" in process and "HT500" in process: cuts[ "NOMINAL" ] = cuts[ "BASE" ] + " && isHTgt500Njetge9==1"
  elif "TTToSemiLepton" in process and "HT500" not in process: cuts[ "NOMINAL" ] = cuts[ "BASE" ] + " && isHTgt500Njetge9==0"
  else: cuts[ "NOMINAL" ] = cuts[ "BASE" ][:]

  cuts[ "LEPTON" ] = " && isElectron==1" if category[ "LEPTON" ][0] == "E" else " && isMuon==1"
  cuts[ "NHOT" ] = " && NresolvedTops1pFake {}= {}".format( ">" if "p" in category[ "NHOT" ][0] else "=", category[ "NHOT" ][0][:-1] if "p" in category[ "NHOT" ][0] else category[ "NHOT" ][0] )
  cuts[ "NT" ] = " && NJetsTtagged {}= {}".format( ">" if "p" in category[ "NT" ][0] else "=", category[ "NT" ][0][:-1] if "p" in category[ "NT" ][0] else category[ "NT" ][0] )
  cuts[ "NW" ] = " && NJetsWtagged {}= {}".format( ">" if "p" in category[ "NW" ][0] else "=", category[ "NW" ][0][:-1] if "p" in category[ "NW" ][0] else category[ "NW" ][0] )
  cuts[ "NB" ] = " && NJetsCSV_JetSubCalc {}= {}".format( ">" if "p" in category[ "NB" ][0] else "=", category[ "NB" ][0][:-1] if "p" in category[ "NB" ][0] else category[ "NB" ][0] )
  cuts[ "NJ" ] = " && NJets_JetSubCalc {}= {}".format( ">" if "p" in category[ "NJ" ][0] else "=", category[ "NJ" ][0][:-1] if "p" in category[ "NJ" ][0] else category[ "NJ" ][0] )
 
  cuts[ "NOMINAL" ] += cuts[ "LEPTON" ] + cuts[ "NHOT" ] + cuts[ "NT" ] + cuts[ "NW" ] + cuts[ "NB" ] + cuts[ "NJ" ]
    
  # modify the cuts for shifts
  cuts[ "BTAG" ] = { "UP": cuts[ "NOMINAL" ].replace( "NJetsCSV_JetSubCalc", "NJetsCSVwithSF_JetSubCalc_bSFup" ),
                     "DN": cuts[ "NOMINAL" ].replace( "NJetsCSV_JetSubCalc", "NJetsCSVwithSF_JetSubCalc_bSFdn" ) }
  cuts[ "MISTAG" ] = { "UP": cuts[ "NOMINAL" ].replace( "NJetsCSV_JetSubCalc", "NJetsCSVwithSF_JetSubCalc_lSFup" ),
                       "DN": cuts[ "NOMINAL" ].replace( "NJetsCSV_JetSubCalc", "NJetsCSVwithSF_JetSubCalc_lSFdn" ) }
  cuts[ "TAU21" ] = { "UP": cuts[ "NOMINAL" ].replace( "NJetsWtagged", "NJetsWtagged_shifts[0]" ),
                      "DN": cuts[ "NOMINAL" ].replace( "NJetsWtagged", "NJetsWtagged_shifts[1]" ) }
  cuts[ "JMSW" ] = { "UP": cuts[ "NOMINAL" ].replace( "NJetsWtagged", "NJetsWtagged_shifts[2]" ),
                     "DN": cuts[ "NOMINAL" ].replace( "NJetsWtagged", "NJetsWtagged_shifts[3]" ) }
  cuts[ "JMRW" ] = { "UP": cuts[ "NOMINAL" ].replace( "NJetsWtagged", "NJetsWtagged_shifts[4]" ),
                     "DN": cuts[ "NOMINAL" ].replace( "NJetsWtagged", "NJetsWtagged_shifts[5]" ) }
  cuts[ "TAU21PT" ] = { "UP": cuts[ "NOMINAL" ].replace( "NJetsWtagged", "NJetsWtagged_shifts[6]" ),
                        "DN": cuts[ "NOMINAL" ].replace( "NJetsWtagged", "NJetsWtagged_shifts[7]" ) }
  cuts[ "TAU32" ] = { "UP": cuts[ "NOMINAL" ].replace( "NJetsTtagged", "NJetsTtagged_shifts[0]" ),
                      "DN": cuts[ "NOMINAL" ].replace( "NJetsTtagged", "NJetsTtagged_shifts[1]" ) }
  cuts[ "JMST" ] = { "UP": cuts[ "NOMINAL" ].replace( "NJetsTtagged", "NJetsTtagged_shifts[2]" ),
                     "DN": cuts[ "NOMINAL" ].replace( "NJetsTtagged", "NJetsTtagged_shifts[3]" ) }
  cuts[ "JMRT" ] = { "UP": cuts[ "NOMINAL" ].replace( "NJetsTtagged", "NJetsTtagged_shifts[4]" ),
                     "DN": cuts[ "NOMINAL" ].replace( "NJetsTtagged", "NJetsTtagged_shifts[5]" ) }
  cuts[ "HOTSTAT" ] = { "UP": cuts[ "NOMINAL" ].replace( "NresolvedTops1pFake", "NresolvedTops1pFake_shifts[0]" ),
                        "DN": cuts[ "NOMINAL" ].replace( "NresolvedTops1pFake", "NresolvedTops1pFake_shifts[1]" ) }
  cuts[ "HOTCSPUR" ] = { "UP": cuts[ "NOMINAL" ].replace( "NresolvedTops1pFake", "NresolvedTops1pFake_shifts[2]" ),
                         "DN": cuts[ "NOMINAL" ].replace( "NresolvedTops1pFake", "NresolvedTops1pFake_shifts[3]" ) }
  cuts[ "HOTCLOSURE" ] = { "UP": cuts[ "NOMINAL" ].replace( "NresolvedTops1pFake", "NresolvedTops1pFake_shifts[4]" ),
                           "DN": cuts[ "NOMINAL" ].replace( "NresolvedTops1pFake", "NresolvedTops1pFake_shifts[5]" ) }
	
  if category[ "NB" ][0] == "0" and "minmlb" in variable.lower():
    originalLJMETName = plotTreeName[:]
    plotTreeName = "minMleppJet"
    
  # declare histograms
  hists = {}
  lumiStr = config.lumiStr[ year ] # 1/fb  
  categoryTag = "is{}nHOT{}nT{}nW{}nB{}nJ{}".format(
    category[ "LEPTON" ][0], category[ "NHOT" ][0], category[ "NT" ][0],
    category[ "NW" ][0], category[ "NB" ][0], category[ "NJ" ][0]
  )
  histTag = "{}_{}_{}_{}".format( variable, lumiStr, categoryTag, process )
  hists[ histTag ] = ROOT.TH1D( histTag, xLabel, len( histBins ) - 1, histBins )
  if doSYST:
    for syst in config.systematics[ "MC" ]:
      for shift in [ "UP", "DN" ]:
        histTag = "{}_{}_{}_{}_{}".format( variable, syst.upper() + shift, lumiStr, categoryTag, process )
        hists[ histTag ] = ROOT.TH1D( histTag, xLabel, len( histBins ) - 1, histBins )
  if doPDF:
    for i in range( config.params[ "GENERAL" ][ "PDF RANGE" ] ):
      histTag = "{}_PDF{}_{}_{}_{}".format( variable, i, lumiStr, categoryTag, process )
      hists[ histTag ] = ROOT.TH1D( histTag, xLabel, len( histBins ) - 1, histBins )
				
  # Sumw2() tells the hist to also store the sum of squares of weights
  for histTag in hists: hists[ histTag ].Sumw2()
		
  # draw histograms
  histTag = "{}_{}_{}_{}".format( variable, lumiStr, categoryTag, process )
  rTree[ process ].Draw( 
    "{} >> {}".format( variableName, histTag ), 
    "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ "NOMINAL" ] ), 
    "GOFF" )

  if verbose: print( "  + NOMINAL" )

  if process not in list( samples.samples[ "DATA" ].keys() ) and doSYST:
    for syst in config.systematics[ "MC" ]:
      for shift in [ "UP", "DN" ]:
        histTag = "{}_{}_{}_{}_{}".format( variable, syst.upper() + shift, lumiStr, categoryTag, process )
        if syst.upper() in [ "PILEUP", "PREFIRE", "MURFCORRD", "MUR", "MUF", "ISR", "FSR", "NJET", "NJETSF", "CSVSHAPELF", "CSVSHAPEHF" ]:
          rTree[ process ].Draw( 
            "{} >> {}".format( variableName, histTag ), 
            "{} * ({})".format( mc_weights[ syst.upper() ][ shift ], cuts[ "NOMINAL" ] ), 
            "GOFF" )
        # hot-tagging plots
        if ( syst.upper() in [ "HOTSTAT", "HOTCSPUR", "HOTCLOSURE" ] ) and ( category[ "NHOT" ][0] != "0p" ):
          rTree[ process ].Draw( 
            "{} >> {}".format( variableName, histTag ), 
            "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ syst.upper() ][ shift ] ), 
            "GOFF" )
        # t-tagging plots
        if ( syst.upper() in [ "TAU32", "JMST", "JMRT" ] ) and ( category[ "NT" ][0] != "0p" ):
          if "ttagged" in variableName.lower() or "tjet" in variableName.lower():
            shift_indx = 2*np.argwhere( np.array([ "TAU32", "JMST", "JMRT" ]) == syst.upper() )[0,0] + np.argwhere( np.array([ "UP", "DN" ]) == shift )[0,0]
            rTree[ process ].Draw( 
              "{}_shifts[{}] >> {}".format( variableName, shift_indx, histTag ), 
              "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ syst.upper() ][ shift ] ), 
              "GOFF" )
          else: 
            rTree[ process ].Draw( 
              "{} >> {}".format( variableName, histTag ), 
              "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ syst.upper() ][ shift ] ), 
              "GOFF" )
        # W-tagging plots
        if ( syst in [ "TAU21", "JMSW", "JMRW", "TAU21PT" ] ) and ( category[ "NW" ][0] != "0p" ):
          if "wtagged" in variableName.lower() or "wjet" in variableName.lower():
            shift_indx = 2*np.argwhere( np.array([ "TAU21", "JMSW", "JMRW", "TAU21PT" ]) == syst.upper() )[0,0] + np.argwhere( np.array([ "UP", "DN" ]) == shift )[0,0]
            rTree[ process ].Draw( 
              "{}_shifts[{}] >> {}".format( variableName, shift_indx, histTag ), 
              "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ syst.upper() ][ shift ] ), 
              "GOFF" )
          else: rTree[ process ].Draw( 
            "{} >> {}".format( variableName, histTag ), 
            "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ syst.upper() ][ shift ] ), 
            "GOFF" )
        # b-tagging plots
        if ( syst.upper() in [ "BTAG", "MISTAG" ] ) and ( category[ "NB" ][0] != "0p" ):
          if "csvwithsf" in variableName.lower() or "htag" in variableName.lower() or "mleppb" in variableName.lower() or "bjetlead" in variableName.lower() or "minmlb" in variableName.lower():
            if syst.upper() == "BTAG": rTree[ process ].Draw( 
              "{}_bSF{} >> {}".format( variableName, shift.lower(), histTag ), 
              "{} * ({})".format( mc_weights[ "NOMINAL" ], cut[ syst.upper() ][ shift ] ), 
              "GOFF" )
            if syst.upper() == "MISTAG": rTree[ process ].Draw( 
              "{}_lSF{} >> {}".format( variableName, shift.lower(), histTag ), 
              "{} * ({})".format( mc_weights[ "NOMINAL" ], cut[ syst.upper() ][ shift ] ), 
              "GOFF" )
          else: rTree[ process ].Draw( 
            "{} >> {}".format( variableName, histTag ), 
            "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ syst.upper() ][ shift ] ), 
            "GOFF" )
        # process jec and jer
        if ( syst in [ "JEC", "JER" ] ) and rTree[ process + syst.upper() + shift.upper() ]: rTree.Draw( 
          "{} >> {}".format( variableName, histTag ), 
          "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ "NOMINAL" ] ), 
          "GOFF" )
    if verbose: print( "  + SYSTEMATICS" ) 
	
  if doPDF:
    for i in range( config.params[ "GENERAL" ][ "PDF RANGE" ] ):
      histTag = "{}pdf{}_{}_{}_{}".format( variable, i, lumiStr, categoryTag, process )
      rTree[ process ].Draw( 
        "{} >> {}".format(variableName, histTag ), 
        "pdfWeights[{}] * {} * ({})".format( i, mc_weights[ "NOMINAL" ], cuts[ "NOMINAL" ] ), 
        "GOFF" )
    if verbose: print( "  + PDF" )
							
  for key in hists: hists[ key ].SetDirectory(0)
  return hists

def make_hists( groups, group, category ): 
  # only valid group arguments are DATA, SIGNAL, BACKGROUND, TEST
  doSys = config.options[ "GENERAL" ][ "SYSTEMATICS" ] if group in [ "SIGNAL", "BACKGROUND", "TEST" ] else False
  hists = {}
  for process in groups[ group ]:
    process_time = time.time()
    rFiles, rTrees = {}, {} 
    rFiles[ process ], rTrees[ process ] = read_tree( os.path.join( config.inputDir[ args.year ], "nominal/", samples.samples[ group ][ process ] + "_hadd.root" ) )
    if config.options[ "GENERAL" ][ "JET SHIFTS" ] and group in [ "SIGNAL", "BACKGROUND" ]:
      for syst in [ "JEC", "JER" ]:
        for shift in [ "up", "down" ]:
          rFile[ process + syst + shift ], rTrees[ process + syst + shift ] = read_tree( os.path.join( config.inputDir, sys + shift, samples.samples[ group ][ process ] ) )
    hists.update( analyze( rTrees, args.year, process, args.variable, doSys, config.options[ "GENERAL" ][ "PDF" ], category, True ) )
    print( "[OK] Added hists for {} in {:.2f} minutes".format( process, round( ( time.time() - process_time ) / 60,2 ) ) )
    del rFiles, rTrees
  if config.options[ "GENERAL" ][ "UE" ] and group in [ "BACKGROUND" ]:
    for process in groups[ "UE" ]:
      process_time = time.time()
      rTree = read_tree( os.path.join( config.inputDir[ args.year ], "nominal/", samples.samples[ "BACKGROUND" ][ process ] + "_hadd.root" ) )
      hists.update( analyze( rTree, args.year, process, args.variable, False, config.options[ "GENERAL" ][ "PDF" ], category, True ) )
      print( "[OK] Added hists for {} in {:.2f} minutes".format( process, round( ( time.time() - process_time ) / 60, 2 ) ) )
  if config.options[ "GENERAL" ][ "HDAMP" ] and group in [ "BACKGROUND" ]:
    for process in groups[ "HD" ]:
      process_time = time.time()
      rTree = read_tree( os.path.join( config.inputDir[ args.year ], "nominal/", samples.samples[ "BACKGROUND" ][ process ] + "_hadd.root" ) )
      hists.update( analyze( rTree, args.year, process, args.variable, False, config.options[ "GENERAL" ][ "PDF" ], category, True ) )
      print( "[OK] Added hists for {} in {:.2f} minutes".format( process, round( ( time.time() - process_time ) / 60, 2 ) ) )
  categoryDir = "is{}nHOT{}nT{}nW{}nB{}nJ{}".format( category[ "LEPTON" ][0], category[ "NHOT" ][0], category[ "NT" ][0], category[ "NW" ][0], category[ "NB" ][0], category[ "NJ" ][0] )
  pickle.dump( hists, open( "{}/{}/{}_{}.pkl".format( args.subDir, categoryDir, group, args.variable ), "wb" ) )
  
if not config.options[ "GENERAL" ][ "TEST" ]:
  for group in [ "DATA", "BACKGROUND", "SIGNAL" ]:
    group_time = time.time()
    print( ">> Processing hists for {}".format( group ) )
    for key in category: print( "  - {}: {}".format( key, category[ key ] ) )
    make_hists( groups, group, category )
    print( "[DONE] Finished processing hists for {} in {} minutes".format( group, round( ( time.time() - group_time ) / 60, 2 ) ) )
else:
  test_time = time.time() 
  print( ">> Processing TEST hists" )
  for key in category: print( "  - {}: {}".format( key, category[ key ] ) )
  make_hists( groups, "TEST", category )
  print( "[DONE] Finished processing hists for TEST in {} minutes".format( round( ( time.time() - test_time ) / 60, 2 ) ) )

print( "[DONE] Finished making hists in {}".format( round( ( time.time() - start_time ) / 60, 2 ) ) )
