#!/usr/bin/python

import os, sys, time, math, datetime, pickle, itertools, getopt
import numpy as np
from array import array
from argparse import ArgumentParser

sys.path.append( os.path.dirname( "../" ) ) 

from utils import hist_tag
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

if args.year == "16APV":
  import weightsUL16APV as weights
  import samplesUL16APV as samples 
elif args.year == "16":
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
  "DAT": sorted( [ str( process ) for process in samples.samples[ "DAT" ] ] ),
  "SIG": sorted( [ str( process ) for process in samples.samples[ "SIG" ] ] ),
  "BKG": sorted( [ str( process ) for process in samples.samples[ "BKG" ] ] ),
  "UE": sorted( [ str( process ) for process in samples.samples[ "UE" ] ] ),
  "HD": sorted( [ str( process ) for process in samples.samples[ "HD" ] ] ),
  "TEST": [ str( process ) for process in samples.samples[ "TEST" ] ]
}

def read_tree( samplePath ):
  if not os.path.exists( samplePath ):
    print("[ERR] {} does not exist.  Exiting program...".format( samplePath ) )
    sys.exit(1)
  rootFile = ROOT.TFile.Open( samplePath, "READ" )
  rootTree = rootFile.Get( "ljmet" )
  return rootFile, rootTree

def analyze( rTree, year, process, variable, doSYST, doPDF, category, verbose ):
  variableName = config.plot_params[ "VARIABLES" ][ variable ][0]
  histBins = array( "d", config.plot_params[ "VARIABLES" ][ variable ][1] )
  xLabel = config.plot_params[ "VARIABLES" ][ variable ][2]

  print( ">> Processing {} for 20{} {}".format( variable, year, process ) )
  
  # modify weights
  # scale up MC samples used in DNN/ABCDnn training where dataset partitioned into 40/20/40 so scale isTraining==3 by 2.5 
  mc_weights = { "NOMINAL": "2.5" if ( ( process.startswith( "TTTo" ) or process.startswith( "TTTW" ) or process.startswith( "TTTJ" ) or process.startswith( "TTTT" ) ) and "DNN" in variable ) else "1" } # weights only applied to MC
  if process in weights.weights.keys():
    mc_weights[ "PROCESS" ] = "{:.10f}".format( weights.weights[ process ] ) 
  else:
    mc_weights[ "PROCESS" ] = "1"

  if process.startswith( "TTTo" ):
    mc_weights[ "NOMINAL" ] += " * topPtWeight13TeV"

<<<<<<< HEAD
  if process not in groups[ "DAT" ]:
    if config.options[ "GENERAL" ][ "ABCDNN" ] and process.startswith( "TTTo" ):
      mc_weights[ "NOMINAL" ] += "*transfer_{}*{}".format( config.params[ "GENERAL" ][ "ABCDNN TAG" ], mc_weights[ "PROCESS" ] ) 
    else:
      mc_weights[ "NOMINAL" ] += "*{}*{}".format( config.mc_weight, mc_weights[ "PROCESS" ] )
    
  if process not in groups[ "DAT" ] and doSYST:
    #mc_weights[ "TRIGGER" ] = { "UP": weights[ "NOMINAL" ].replace( "triggerXSF", "(triggerXSF+triggerXSFUncert)" ),
    #                           "DN": weights[ "NOMINAL" ].replace( "triggerXSF", "(triggerXSF-triggerXSFUncert)" ) }
    if config.systematics[ "MC" ][ "pileup" ]:
      mc_weights[ "PILEUP" ] = { "UP": mc_weights[ "NOMINAL" ].replace( "pileupWeight", "pileupWeightUp" ),
                                 "DN": mc_weights[ "NOMINAL" ].replace( "pileupWeight", "pileupWeightDown" ) }
    if year in [ "16APV", "16", "17" ]:
      mc_weights[ "PREFIRE" ] = { "UP": mc_weights[ "NOMINAL" ].replace("L1NonPrefiringProb_CommonCalc","L1NonPrefiringProbUp_CommonCalc"),
                                  "DN": mc_weights[ "NOMINAL" ].replace("L1NonPrefiringProb_CommonCalc","L1NonPrefiringProbDown_CommonCalc") }
    if config.systematics[ "MC" ][ "muRFcorrd" ]:
      mc_weights[ "MURFCORRD" ] = { "UP": "renormWeights[5] * {}".format( mc_weights[ "NOMINAL" ] ),
                                    "DN": "renormWeights[3] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "muR" ]:
      mc_weights[ "MUR" ] = { "UP": "renormWeights[4] * {}".format( mc_weights[ "NOMINAL" ] ),
                              "DN": "renormWeights[2] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "muF" ]:
      mc_weights[ "MUF" ] = { "UP": "renormWeights[1] * {}".format( mc_weights[ "NOMINAL" ] ),
                              "DN": "renormWeights[0] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "isr" ]:
      mc_weights[ "ISR" ] = { "UP": "renormPSWeights[0] * {}".format( mc_weights[ "NOMINAL" ] ),
                              "DN": "renormPSWeights[2] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "fsr" ]:
      mc_weights[ "FSR" ] = { "UP": "renormPSWeights[1] * {}".format( mc_weights[ "NOMINAL" ] ),
                              "DN": "renormPSWeights[3] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "toppt" ]:
      mc_weights[ "TOPPT" ] = { "UP": "({}) * {}".format( "topPtWeight13TeV" if "TTTo" in process else "1", mc_weights[ "NOMINAL" ] ),
                                "DN": "(1/{}) * {}".format( "topPtWeight13TeV" if "TTTo" in process else "1", mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "njet" ]:
      mc_weights[ "NJET" ] = { "UP": mc_weights[ "NOMINAL" ],
                               "DN": mc_weights[ "NOMINAL" ] }
    if config.systematics[ "MC" ][ "njetsf" ]:
=======
  if process not in list( samples.samples[ "DATA" ].keys() ):
    if not config.options[ "GENERAL" ][ "ABCDNN" ]:
      mc_weights[ "NOMINAL" ] += "*{}*{}".format( config.mc_weight, mc_weights[ "PROCESS" ] )
    else:
      mc_weights[ "NOMINAL" ] += "*transfer_{}*{}".format( config.params[ "GENERAL" ][ "ABCDNN TAG" ], mc_weights[ "PROCESS" ] )

  if process not in list( samples.samples[ "DATA" ].keys() ) and doSYST:
    #mc_weights[ "TRIGGER" ] = { "UP": weights[ "NOMINAL" ].replace( "triggerXSF", "(triggerXSF+triggerXSFUncert)" ),
    #                           "DN": weights[ "NOMINAL" ].replace( "triggerXSF", "(triggerXSF-triggerXSFUncert)" ) }
    if config.options[ "GENERAL" ][ "ABCDNN" ]:
      abcdnn_tag = config.params[ "GENERAL" ][ "ABCDNN TAG" ]
      mc_weights[ "TRANSFER" ] = { "UP": mc_weights[ "NOMINAL" ].replace( "transfer_{}".format( abcdnn_tag ), "(transfer_{}+transfer_err_{}".format( abcdnn_tag, abcdnn_tag ) ),
                                   "DN": mc_weights[ "NOMINAL" ].replace( "transfer_{}".format( abcdnn_tag ), "(transfer_{}-transfer_err_{}".format( abcdnn_tag, abcdnn_tag ) ) }
    if "pileup" in config.systematics[ "MC" ]:
      mc_weights[ "PILEUP" ] = { "UP": mc_weights[ "NOMINAL" ].replace( "pileupWeight", "pileupWeightUp" ),
                                 "DN": mc_weights[ "NOMINAL" ].replace( "pileupWeight", "pileupWeightDown" ) }
    mc_weights[ "PREFIRE" ] = { "UP": mc_weights[ "NOMINAL" ].replace("L1NonPrefiringProb_CommonCalc","L1NonPrefiringProbUp_CommonCalc"),
                                "DN": mc_weights[ "NOMINAL" ].replace("L1NonPrefiringProb_CommonCalc","L1NonPrefiringProbDn_CommonCalc") }
    if "murfcorrd" in config.systematics[ "MC" ]:
      mc_weights[ "MURFCORRD" ] = { "UP": "renormWeights[5] * {}".format( mc_weights[ "NOMINAL" ] ),
                                    "DN": "renormWeights[3] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if "muR" in config.systematics[ "MC" ]:
      mc_weights[ "MUR" ] = { "UP": "renormWeights[4] * {}".format( mc_weights[ "NOMINAL" ] ),
                              "DN": "renormWeights[2] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if "muF" in config.systematics[ "MC" ]:
      mc_weights[ "MUF" ] = { "UP": "renormWeights[1] * {}".format( mc_weights[ "NOMINAL" ] ),
                              "DN": "renormWeights[0] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if "isr" in config.systematics[ "MC" ]:
      mc_weights[ "ISR" ] = { "UP": "renormPSWeights[0] * {}".format( mc_weights[ "NOMINAL" ] ),
                              "DN": "renormPSWeights[2] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if "fsr" in config.systematics[ "MC" ]:
      mc_weights[ "FSR" ] = { "UP": "renormPSWeights[1] * {}".format( mc_weights[ "NOMINAL" ] ),
                              "DN": "renormPSWeights[3] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if "toppt" in config.systematics[ "MC" ]:
      mc_weights[ "TOPPT" ] = { "UP": "({}) * {}".format( "topPtWeight13TeV" if "TTTo" in process else "1", mc_weights[ "NOMINAL" ] ),
                                "DN": "(1/{}) * {}".format( "topPtWeight13TeV" if "TTTo" in process else "1", mc_weights[ "NOMINAL" ] ) }
    if "njet" in config.systematics[ "MC" ]:
      mc_weights[ "NJET" ] = { "UP": mc_weights[ "NOMINAL" ],
                               "DN": mc_weights[ "NOMINAL" ] }
    if "njetsf" in config.systematics[ "MC" ]:
>>>>>>> be39dd62d7ed57d9a1887dee7aa2416d25dddfed
      mc_weights[ "NJETSF" ] = { "UP": mc_weights[ "NOMINAL" ],
                                 "DN": mc_weights[ "NOMINAL" ] }
    # deep jet related systematics
    for syst in [ "LF", "lfstats1", "lfstats2", "HF", "hfstats1", "hfstats2", "cferr1", "cferr2", "jes" ]:
      if config.systematics[ "MC" ][ syst ]:
        mc_weights[ syst.upper() ] = {}
        for shift in [ "up", "dn" ]:
          mc_weights[ syst.upper() ][ shift.upper() ] = mc_weights[ "NOMINAL" ].replace( "btagDeepJetWeight", "btagDeepJetWeight_" + syst + shift ).replace( "btagDeepJet2DWeight_HTnj", "btagDeepJet2DWeight_HTnj_" + syst + shift )
  
  # modify cuts
  cuts = { "BASE": config.base_cut }
  if "TTToSemiLepton" in process and "HT500" in process: cuts[ "NOMINAL" ] = cuts[ "BASE" ] + " && isHTgt500Njetge9==1"
  elif "TTToSemiLepton" in process and "HT500" not in process: cuts[ "NOMINAL" ] = cuts[ "BASE" ] + " && isHTgt500Njetge9==0"
  else: cuts[ "NOMINAL" ] = cuts[ "BASE" ][:]
  if ( ( process.startswith( "TTTo" ) or process.startswith( "TTTW" ) or process.startswith( "TTTJ" ) or process.startswith( "TTTT" ) ) and "DNN" in variable ):
    cuts[ "NOMINAL" ] += " && isTraining == 3" # Used isTraining==1 in training and isTraining==2 in validation of training

  cuts[ "LEPTON" ] = " && isElectron==1" if category[ "LEPTON" ][0] == "E" else " && isMuon==1"
  cuts[ "NHOT" ] = " && NresolvedTops1pFake {}= {}".format( ">" if "p" in category[ "NHOT" ][0] else "=", category[ "NHOT" ][0][:-1] if "p" in category[ "NHOT" ][0] else category[ "NHOT" ][0] )
  cuts[ "NT" ] = " && NJetsTtagged {}= {}".format( ">" if "p" in category[ "NT" ][0] else "=", category[ "NT" ][0][:-1] if "p" in category[ "NT" ][0] else category[ "NT" ][0] )
  cuts[ "NW" ] = " && NJetsWtagged {}= {}".format( ">" if "p" in category[ "NW" ][0] else "=", category[ "NW" ][0][:-1] if "p" in category[ "NW" ][0] else category[ "NW" ][0] )
  cuts[ "NB" ] = " && NJetsCSV_JetSubCalc {}= {}".format( ">" if "p" in category[ "NB" ][0] else "=", category[ "NB" ][0][:-1] if "p" in category[ "NB" ][0] else category[ "NB" ][0] )
  cuts[ "NJ" ] = " && NJets_JetSubCalc {}= {}".format( ">" if "p" in category[ "NJ" ][0] else "=", category[ "NJ" ][0][:-1] if "p" in category[ "NJ" ][0] else category[ "NJ" ][0] )
 
  cuts[ "NOMINAL" ] += cuts[ "LEPTON" ] + cuts[ "NHOT" ] + cuts[ "NT" ] + cuts[ "NW" ] + cuts[ "NB" ] + cuts[ "NJ" ]
    
  # modify the cuts for shifts
  cuts[ "BTAG" ] = { "UP": cuts[ "NOMINAL" ].replace( "NJetsCSV_JetSubCalc", "NJetsCSV_JetSubCalc_bSFup" ),
                     "DN": cuts[ "NOMINAL" ].replace( "NJetsCSV_JetSubCalc", "NJetsCSV_JetSubCalc_bSFdn" ) }
  cuts[ "MISTAG" ] = { "UP": cuts[ "NOMINAL" ].replace( "NJetsCSV_JetSubCalc", "NJetsCSV_JetSubCalc_lSFup" ),
                       "DN": cuts[ "NOMINAL" ].replace( "NJetsCSV_JetSubCalc", "NJetsCSV_JetSubCalc_lSFdn" ) }
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
  categoryTag = "is{}nHOT{}nT{}nW{}nB{}nJ{}".format(
    category[ "LEPTON" ][0], category[ "NHOT" ][0], category[ "NT" ][0],
    category[ "NW" ][0], category[ "NB" ][0], category[ "NJ" ][0]
  )
  histTag = hist_tag( process, categoryTag )
  hists[ histTag ] = ROOT.TH1D( histTag, xLabel, len( histBins ) - 1, histBins )
  if doSYST:
    for syst in config.systematics[ "MC" ].keys():
      for shift in [ "UP", "DN" ]:
        histTag = hist_tag( process, categoryTag, syst.upper() + shift )
        hists[ histTag ] = ROOT.TH1D( histTag, xLabel, len( histBins ) - 1, histBins )
  if doPDF:
    for i in range( config.params[ "GENERAL" ][ "PDF RANGE" ] ):
      histTag = hist_tag( process, categoryTag, "PDF" + str(i) ) 
      hists[ histTag ] = ROOT.TH1D( histTag, xLabel, len( histBins ) - 1, histBins )
				
  # Sumw2() tells the hist to also store the sum of squares of weights
  for histTag in hists: hists[ histTag ].Sumw2()
	
  if verbose: 
    print( ">> Applying NOMINAL weights: {}".format( mc_weights[ "NOMINAL" ] ) )
    print( ">> Applying NOMINAL cuts: {}".format( cuts[ "NOMINAL" ] ) )

  # draw histograms
  histTag = hist_tag( process, categoryTag )
  rTree[ process ].Draw( 
    "{} >> {}".format( variableName, histTag ), 
    "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ "NOMINAL" ] ), 
    "GOFF" )

  if verbose: print( "  + NOMINAL: {} --> {}".format( rTree[ process ].GetEntries(), hists[ histTag ].Integral() ) )

  if process not in groups[ "DAT" ] and doSYST:
    if year in [ "16APV", "16", "17" ]:
      for shift in [ "UP", "DN" ]:
        rTree[ process ].Draw(
          "{} >> {}".format( variableName, hist_tag( process, categoryTag, "PREFIRE" + shift ) ),
          "{} * ({})".format( mc_weights[ "PREFIRE" ][ shift ], cuts[ "NOMINAL" ] ),
          "GOFF" )
    for syst in config.systematics[ "MC" ].keys():
      if not config.systematics[ "MC" ][ syst ]: continue
      for shift in [ "UP", "DN" ]:
        histTag = hist_tag( process, categoryTag, syst.upper() + shift )
        if syst.upper() in [ "PILEUP", "MURFCORRD", "MUR", "MUF", "ISR", "FSR", "NJET", "NJETSF", "CSVSHAPELF", "CSVSHAPEHF" ]:
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
        if ( syst.upper() in [ "LF", "LFSTAT1", "LFSTAT2", "HF", "HFSTAT1", "HFSTAT2", "CFERR1", "CFERR2" ] ) and ( category[ "NB" ][0] != "0p" ):
          rTree[ process ].Draw(
            "{} >> {}".format( variableName, histTag ), 
            "{} * ({})".format( mc_weights[ syst.upper() ][ shift ], cuts[ "NOMINAL" ] ), 
            "GOFF" )
        # process jec and jer
        if ( syst.upper() in [ "JEC", "JER" ] ): 
          rTree[ process ].Draw( 
            "{} >> {}".format( variableName, histTag ), 
            "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ "NOMINAL" ] ), 
            "GOFF" )
    if verbose: print( "  + SYSTEMATICS" ) 
	
  if doPDF:
    for i in range( config.params[ "GENERAL" ][ "PDF RANGE" ] ):
      histTag = hist_tag( process, categoryTag, "PDF" + str(i) )
      rTree[ process ].Draw( 
        "{} >> {}".format( variableName, histTag ), 
        "pdfWeights[{}] * {} * ({})".format( i, mc_weights[ "NOMINAL" ], cuts[ "NOMINAL" ] ), 
        "GOFF" )
    if verbose: print( "  + PDF" )
							
  for key in hists: hists[ key ].SetDirectory(0)
  return hists

def make_hists( groups, group, category ): 
  # only valid group arguments are DAT, SIG, BKG, TEST
  doSys = config.options[ "GENERAL" ][ "SYSTEMATICS" ] if group in [ "SIG", "BKG", "TEST" ] else False
  hists = {}
  for process in groups[ group ]:
    process_time = time.time()
    rFiles, rTrees = {}, {} 
    rFiles[ process ], rTrees[ process ] = read_tree( os.path.join( config.inputDir[ args.year ], "nominal/", samples.samples[ group ][ process ] + "_hadd.root" ) )
    if config.options[ "GENERAL" ][ "JET SHIFTS" ] and group in [ "SIG", "BKG" ]:
      for syst in [ "JEC", "JER" ]:
        for shift in [ "up", "down" ]:
          rFile[ process + syst + shift ], rTrees[ process + syst + shift ] = read_tree( os.path.join( config.inputDir, sys + shift, samples.samples[ group ][ process ] ) )
    hists.update( analyze( rTrees, args.year, process, args.variable, doSys, config.options[ "GENERAL" ][ "PDF" ], category, True ) )
    print( "[OK] Added hists for {} in {:.2f} minutes".format( process, round( ( time.time() - process_time ) / 60,2 ) ) )
    del rFiles, rTrees
  if config.options[ "GENERAL" ][ "UE" ] and group in [ "UE" ]:
    for process in groups[ "UE" ]:
      process_time = time.time()
      rTree = read_tree( os.path.join( config.inputDir[ args.year ], "nominal/", samples.samples[ "BKG" ][ process ] + "_hadd.root" ) )
      hists.update( analyze( rTree, args.year, process, args.variable, False, config.options[ "GENERAL" ][ "PDF" ], category, True ) )
      print( "[OK] Added hists for {} in {:.2f} minutes".format( process, round( ( time.time() - process_time ) / 60, 2 ) ) )
  if config.options[ "GENERAL" ][ "HDAMP" ] and group in [ "HD" ]:
    for process in groups[ "HD" ]:
      process_time = time.time()
      rTree = read_tree( os.path.join( config.inputDir[ args.year ], "nominal/", samples.samples[ "BKG" ][ process ] + "_hadd.root" ) )
      hists.update( analyze( rTree, args.year, process, args.variable, False, config.options[ "GENERAL" ][ "PDF" ], category, True ) )
      print( "[OK] Added hists for {} in {:.2f} minutes".format( process, round( ( time.time() - process_time ) / 60, 2 ) ) )
  categoryDir = "is{}nHOT{}nT{}nW{}nB{}nJ{}".format( category[ "LEPTON" ][0], category[ "NHOT" ][0], category[ "NT" ][0], category[ "NW" ][0], category[ "NB" ][0], category[ "NJ" ][0] )
  if not os.path.exists( "{}/{}".format( args.subDir, categoryDir ) ): os.system( "mkdir -vp {}/{}".format( args.subDir, categoryDir ) )
  pickle.dump( hists, open( "{}/{}/{}_{}.pkl".format( args.subDir, categoryDir, group, args.variable ), "wb" ) )

def main():
  if not config.options[ "GENERAL" ][ "TEST" ]:
    for group in [ "DAT", "BKG", "SIG" ]:
      group_time = time.time()
      print( "[START] Processing hists for {}".format( group ) )
      for key in category: print( "  - {}: {}".format( key, category[ key ] ) )
      make_hists( groups, group, category )
      print( "[DONE] Finished processing hists for {} in {} minutes".format( group, round( ( time.time() - group_time ) / 60, 2 ) ) )
  else:
    test_time = time.time() 
    print( "[START] Processing TEST hists" )
    for key in category: print( "  - {}: {}".format( key, category[ key ] ) )
    make_hists( groups, "TEST", category )
    print( "[DONE] Finished processing hists for TEST in {} minutes".format( round( ( time.time() - test_time ) / 60, 2 ) ) )

  print( "[DONE] Finished making hists in {}".format( round( ( time.time() - start_time ) / 60, 2 ) ) )

main()
