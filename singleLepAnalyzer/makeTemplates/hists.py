#!/usr/bin/python

import os, sys, time, math, datetime, pickle, itertools, getopt
import numpy as np
from array import array
from argparse import ArgumentParser

sys.path.append( os.path.dirname( "../" ) ) 

from utils import hist_tag, abcdnn_tag, contains_category
import config
from xsec import xsec

parser = ArgumentParser()
parser.add_argument( "-v", "--variable", default = "HT" )
parser.add_argument( "-y", "--year", default = "17" )
parser.add_argument( "-c", "--category", default = "isENB1pNH0pNJ4p" )
parser.add_argument( "-sd", "--subDir", default = "test" )
args = parser.parse_args()

if args.year == "16APV":
  import samplesUL16APV as samples 
elif args.year == "16":
  import samplesUL16 as samples
elif args.year == "17":
  import samplesUL17 as samples
elif args.year == "18":
  import samplesUL18 as samples
else:
  quit( "[ERR] Invalid -y (--year) option used. Quitting..." )

import ROOT

ROOT.gROOT.SetBatch(1)
start_time = time.time()

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

def analyze( rTree, nHist, year, process, variable, doSYST, doPDF, doABCDNN, category, verbose ):
  variableName = config.plot_params[ "VARIABLES" ][ variable ][0]
  histBins = array( "d", config.plot_params[ "VARIABLES" ][ variable ][1] )
  xLabel = config.plot_params[ "VARIABLES" ][ variable ][2]
  print( ">> Processing {} for 20{} {}".format( variable, year, process ) )

  
  # modify weights
  # scale up MC samples used in DNN training where dataset partitioned into 60/20/20 so scale isTraining==1 by 1.667
  mc_weights = { "NOMINAL": "1.667" if ( ( process.startswith( "TTTo" ) or process.startswith( "TTTW" ) or process.startswith( "TTTJ" ) ) and "DNN" in variable ) else "1" } # weights only applied to MC
  if process in xsec:
    nTrueHist = nHist[ process ]
    for splitPrefix in samples.split:
      if splitPrefix in process:
        for splitProcess in samples.split[ splitPrefix ]:
          if process != splitProcess: nTrueHist += nHist[ splitProcess ]
        print( "[INFO] {} was hadded into more than one file, consolidating numTrueHist across split files: {} --> {}".format( process, nHist[ process ], nTrueHist ) )
    mc_weights[ "PROCESS" ] = "( {:.2f} * {:.10f} / {:.1f} )".format( config.lumi[ args.year ], xsec[ process ], nTrueHist ) 
  elif process in samples.samples[ "DAT" ]:
    mc_weights[ "PROCESS" ] = "1"
  else:
    sys.exit( "[ERROR] {} is neither data nor does it have a cross-section listed. Exiting...".format( process ) )

  if doABCDNN:
    abcdnnTag = ""
    for tag in config.params[ "ABCDNN" ][ "TAG" ]:
      if contains_category( category, config.params[ "ABCDNN" ][ "TAG" ][ tag ] ):
        abcdnnTag = str( tag )
    if abcdnnTag == "":
      quit( "[ERR] Couldn't find a compatible ABCDnn configuration for category: {}".format( category ) )
    abcdnnName     = variableName + "_{}".format( abcdnnTag )
    print( "   + Including ABCDnn Histograms with tag {}".format( abcdnnTag ) )
    mc_weights[ "ABCDNN" ] = "transfer_{}".format( abcdnnTag ) 

  if process.startswith( "TTTo" ): # https://twiki.cern.ch/twiki/bin/view/Sandbox/JamesKeaveneySandbox
    mc_weights[ "NOMINAL" ] += " * topPtWeight13TeV"

  if process not in groups[ "DAT" ]:
    mc_weights[ "NOMINAL" ] += "*{}*{}".format( config.mc_weight, mc_weights[ "PROCESS" ] )

  if process not in groups["DAT"] and ( "NB" in category and "NB0p" not in category):
    mc_weights[ "NOMINAL" ] += " * btagDeepJetWeight * btagDeepJet2DWeight_HTnj" 

  if year in [ "16APV" ]: # since 2016 pre-VFP and post-VFP were produced collectively for EOY, use default to custom only for 2016APV
    mc_weights[ "NOMINAL" ] = mc_weights[ "NOMINAL" ].replace( "triggerSF", "1" )
   
  if process not in groups[ "DAT" ] and doSYST:
    if config.systematics[ "MC" ][ "pileup" ][0]:
      mc_weights[ "PILEUP" ] = { "UP": mc_weights[ "NOMINAL" ].replace( "pileupWeight", "pileupWeightUp" ),
                                 "DN": mc_weights[ "NOMINAL" ].replace( "pileupWeight", "pileupWeightDown" ) }
    if config.systematics[ "MC" ][ "pileupJetID" ][0]:
      mc_weights[ "PILEUPJETID" ] = { "UP": mc_weights[ "NOMINAL" ].replace( "pileupJetIDWeight", "pileupJetIDWeightUp" ),
                                      "DN": mc_weights[ "NOMINAL" ].replace( "pileupJetIDWeight", "pileupJetIDWeightDown" ) }
    if config.systematics[ "MC" ][ "prefire" ]:
      mc_weights[ "PREFIRE" ] = { "UP": mc_weights[ "NOMINAL" ].replace("L1NonPrefiringProb_CommonCalc","L1NonPrefiringProbUp_CommonCalc"),
                                  "DN": mc_weights[ "NOMINAL" ].replace("L1NonPrefiringProb_CommonCalc","L1NonPrefiringProbDown_CommonCalc") }
    if config.systematics[ "MC" ][ "muRFcorrd" ][0]:
      mc_weights[ "MURFCORRD" ] = { "UP": "renormWeights[5] * {}".format( mc_weights[ "NOMINAL" ] ),
                                    "DN": "renormWeights[3] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "muR" ][0]:
      mc_weights[ "MUR" ] = { "UP": "renormWeights[4] * {}".format( mc_weights[ "NOMINAL" ] ),
                              "DN": "renormWeights[2] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "muF" ][0]:
      mc_weights[ "MUF" ] = { "UP": "renormWeights[1] * {}".format( mc_weights[ "NOMINAL" ] ),
                              "DN": "renormWeights[0] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "isr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "isr" ]: 
      mc_weights[ "ISR" ] = { "UP": "renormPSWeights[0] * {}".format( mc_weights[ "NOMINAL" ] ),
                              "DN": "renormPSWeights[2] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "fsr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "fsr" ]:
      mc_weights[ "FSR" ] = { "UP": "renormPSWeights[1] * {}".format( mc_weights[ "NOMINAL" ] ),
                              "DN": "renormPSWeights[3] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "fsr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "fsrG2GGmuR" ]: 
      mc_weights[ "FSRG2GGMUR" ] = { "UP": "renormPSWeights[5] * {}".format( mc_weights[ "NOMINAL" ] ),
                                     "DN": "renormPSWeights[4] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "fsr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "fsrG2QQmuR" ]: 
      mc_weights[ "FSRG2QQMUR" ] = { "UP": "renormPSWeights[7] * {}".format( mc_weights[ "NOMINAL" ] ),
                                     "DN": "renormPSWeights[6] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "fsr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "fsrQ2QGmuR" ]: 
      mc_weights[ "FSRQ2QGMUR" ] = { "UP": "renormPSWeights[9] * {}".format( mc_weights[ "NOMINAL" ] ),
                                     "DN": "renormPSWeights[8] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "fsr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "fsrX2XGmuR" ]: 
      mc_weights[ "FSRX2XGMUR" ] = { "UP": "renormPSWeights[11] * {}".format( mc_weights[ "NOMINAL" ] ),
                                     "DN": "renormPSWeights[10] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "fsr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "fsrG2GGcNS" ]: 
      mc_weights[ "FSRG2GGCNS" ] = { "UP": "renormPSWeights[13] * {}".format( mc_weights[ "NOMINAL" ] ),
                                     "DN": "renormPSWeights[12] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "fsr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "fsrG2QQcNS" ]: 
      mc_weights[ "FSRG2QQCNS" ] = { "UP": "renormPSWeights[15] * {}".format( mc_weights[ "NOMINAL" ] ),
                                     "DN": "renormPSWeights[14] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "fsr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "fsrQ2QGcNS" ]: 
      mc_weights[ "FSRQ2QGCNS" ] = { "UP": "renormPSWeights[17] * {}".format( mc_weights[ "NOMINAL" ] ),
                                     "DN": "renormPSWeights[16] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "fsr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "fsrX2XGcNS" ]: 
      mc_weights[ "FSRX2XGCNS" ] = { "UP": "renormPSWeights[19] * {}".format( mc_weights[ "NOMINAL" ] ),
                                     "DN": "renormPSWeights[18] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "isr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "isrG2GGmuR" ]:
      mc_weights[ "ISRG2GGMUR" ] = { "UP": "renormPSWeights[21] * {}".format( mc_weights[ "NOMINAL" ] ),
                                     "DN": "renormPSWeights[20] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "isr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "isrG2QQmuR" ]:
      mc_weights[ "ISRG2QQMUR" ] = { "UP": "renormPSWeights[23] * {}".format( mc_weights[ "NOMINAL" ] ),
                                     "DN": "renormPSWeights[22] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "isr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "isrQ2QGmuR" ]:
      mc_weights[ "ISRQ2QGMUR" ] = { "UP": "renormPSWeights[25] * {}".format( mc_weights[ "NOMINAL" ] ),
                                     "DN": "renormPSWeights[24] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "isr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "isrX2XGmuR" ]:
      mc_weights[ "ISRX2XGMUR" ] = { "UP": "renormPSWeights[27] * {}".format( mc_weights[ "NOMINAL" ] ),
                                     "DN": "renormPSWeights[26] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "isr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "isrG2GGcNS" ]:
      mc_weights[ "ISRG2GGCNS" ] = { "UP": "renormPSWeights[29] * {}".format( mc_weights[ "NOMINAL" ] ),
                                     "DN": "renormPSWeights[28] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "isr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "isrG2QQcNS" ]:
      mc_weights[ "ISRG2QQCNS" ] = { "UP": "renormPSWeights[31] * {}".format( mc_weights[ "NOMINAL" ] ),
                                     "DN": "renormPSWeights[30] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "isr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "isrQ2QGcNS" ]:
      mc_weights[ "ISRQ2QGCNS" ] = { "UP": "renormPSWeights[33] * {}".format( mc_weights[ "NOMINAL" ] ),
                                     "DN": "renormPSWeights[32] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "isr" ][0] and config.systematics[ "PS BREAKDOWN" ][ "isrX2XGcNS" ]:
      mc_weights[ "ISRX2XGCNS" ] = { "UP": "renormPSWeights[35] * {}".format( mc_weights[ "NOMINAL" ] ),
                                     "DN": "renormPSWeights[34] * {}".format( mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "toppt" ][0]:
      mc_weights[ "TOPPT" ] = { "UP": "({}) * {}".format( "topPtWeight13TeV" if "TTTo" in process else "1", mc_weights[ "NOMINAL" ] ),
                                "DN": "(1/{}) * {}".format( "topPtWeight13TeV" if "TTTo" in process else "1", mc_weights[ "NOMINAL" ] ) }
    if config.systematics[ "MC" ][ "ABCDNNPEAK" ][0] and doABCDNN and "ABCDNNPEAK" in config.params[ "ABCDNN" ][ "SYSTEMATICS" ]:
      mc_weights[ "ABCDNN ABCDNNPEAK" ] = { "UP": mc_weights[ "ABCDNN" ].replace( abcdnnName, abcdnnName + "_PEAKUP" ), 
                                            "DN": mc_weights[ "ABCDNN" ].replace( abcdnnName, abcdnnName + "_PEAKDN" ) }
    if config.systematics[ "MC" ][ "ABCDNNTAIL" ][0] and doABCDNN and "ABCDNNTAIL" in config.params[ "ABCDNN" ][ "SYSTEMATICS" ]:
      mc_weights[ "ABCDNN ABCDNNTAIL" ] = { "UP": mc_weights[ "ABCDNN" ].replace( abcdnnName, abcdnnName + "_TAILUP" ),
                                            "DN": mc_weights[ "ABCDNN" ].replace( abcdnnName, abcdnnName + "_TAILDN" ) }
    if config.systematics[ "MC" ][ "ABCDNNCLOSURE" ][0] and doABCDNN and "ABCDNNCLOSURE" in config.params[ "ABCDNN" ][ "SYSTEMATICS" ]:
      mc_weights[ "ABCDNN ABCDNNCLOSURE" ] = { "UP": mc_weights[ "ABCDNN" ].replace( abcdnnName, abcdnnName + "_CLOSUREUP" ),
                                               "DN": mc_weights[ "ABCDNN" ].replace( abcdnnName, abcdnnName + "_CLOSUREDN" ) }

    # deep jet related systematics
    for syst in [ "LF", "lfstats1", "lfstats2", "HF", "hfstats1", "hfstats2", "cferr1", "cferr2" ]:
      if config.systematics[ "MC" ][ syst ]:
        mc_weights[ syst.upper() ] = {}
        for shift in [ "up", "dn" ]:
          mc_weights[ syst.upper() ][ shift.upper() ] = mc_weights[ "NOMINAL" ].replace( "btagDeepJetWeight", "btagDeepJetWeight_" + syst + shift ).replace( "btagDeepJet2DWeight_HTnj", "btagDeepJet2DWeight_HTnj_" + syst + shift )
  
  # modify cuts
  cuts = { "BASE": config.base_cut }
  cuts[ "LEPTON" ] = " && is Electron == 1" if "isE" in category else " && isMuon == 1"
  if "TTToSemiLepton" in process and "HT500" in process: cuts[ "NOMINAL" ] = cuts[ "BASE" ] + cuts[ "LEPTON" ] + " && isHTgt500Njetge9==1"
  elif "TTToSemiLepton" in process and "HT500" not in process: cuts[ "NOMINAL" ] = cuts[ "BASE" ] + cuts[ "LEPTON" ] + " && isHTgt500Njetge9==0"
  else: cuts[ "NOMINAL" ] = cuts[ "BASE" ] + cuts[ "LEPTON" ]
  cuts[ "ABCDNN" ] = cuts[ "BASE" ] + cuts[ "LEPTON" ]
  if ( ( process.startswith( "TTTo" ) or process.startswith( "TTTW" ) or process.startswith( "TTTJ" ) ) and "DNN" in variable ):
    cuts[ "NOMINAL" ] += " && ( isTraining == 1 )" # isTraining==1 used for application (60%) and isTraining==2 (20%) and 3 (20%) used in training/validation
  if year == "18" and "isE" in category: # exclude electrons that fall in this HEM region which resulted in many misidentifications of jets as electrons
    cuts[ "NOMINAL" ] += " && ( leptonEta_MultiLepCalc > -1.3 || ( leptonPhi_MultiLepCalc < -1.57 || leptonPhi_MultiLepCalc > -0.87 ) )"

  category_vars = []
  category_cond = {}
  for param_ in sorted( config.plot_params[ "VARIABLES" ].keys() ):
    if str(param_) in category:
      category_vars.append( str(param_) )
  for var_a in category_vars:
    if category_vars.index( var_a ) == len( category_vars ) - 1:
      category_cond[var_a] = category.split( var_a )[1]
    else:
      for var_b in category_vars:
        if category_vars.index( var_b ) - category_vars.index( var_a ) == 1:
          category_cond[var_a] = category.split( var_a )[1].split( var_b )[0]

  for key_ in category_cond:
    sign_ = "=="
    if "b" in category_cond[ key_ ]:
      cuts[key_] = " && {0} >= {1} && {0} <= {2}".format( config.plot_params["VARIABLES"][key_][0], *category_cond[ key_ ].split("b") )
    else:
      if "p" in category_cond[ key_ ]: sign_ = ">="
      elif "m" in category_cond[ key_ ]: sign_ = "<="
      cuts[key_] = " && {} {} {}".format( config.plot_params["VARIABLES"][key_][0], sign_, category_cond[key_] if sign_ == "==" else category_cond[key_][:-1] )
    cuts["NOMINAL"] += cuts[key_]
    cuts["ABCDNN"] += cuts[key_]
 
  # modify the cuts for shifts
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
    
  # declare histograms
  hists = {}
  histTag = hist_tag( process, category )
  hists[ histTag ] = ROOT.TH1D( histTag, xLabel, len( histBins ) - 1, histBins )
  
  if doABCDNN:
    histTag = hist_tag( process, category, "ABCDNN" ) 
    hists[ histTag ] = ROOT.TH1D( histTag, xLabel, len( histBins ) - 1, histBins )
    
  if doSYST:
    for syst in config.systematics[ "MC" ]:
      if not config.systematics[ "MC" ][ syst ][0]: continue
      for shift in [ "UP", "DN" ]:
        if doABCDNN and syst.upper() in config.params[ "ABCDNN" ][ "SYSTEMATICS" ]:
          histTag = hist_tag( process, category, "ABCDNN", syst.upper() + shift )
          hists[ histTag ] = ROOT.TH1D( histTag, xLabel, len( histBins ) - 1, histBins )
        if "ABCD" not in syst.upper():
          if syst.upper() == "JEC":
            for systJEC in config.systematics[ "REDUCED JEC" ]:
              if not config.systematics[ "REDUCED JEC" ][ systJEC ]: continue
              histTag = hist_tag( process, category, "JEC" + systJEC.upper().replace( "ERA", "20" + args.year ).replace( "APV", "" ).replace( "_", "" ) + shift )
              hists[ histTag ] = ROOT.TH1D( histTag, xLabel, len( histBins ) - 1, histBins )
          elif syst.upper() in [ "ISR", "FSR" ]:
            for pQCD in [ "G2GG", "G2QQ", "Q2QG", "X2XG" ]:
              for term in [ "cNS", "muR" ]:
                if not config.systematics[ "PS BREAKDOWN" ][ syst + pQCD + term ]: continue
                histTag = hist_tag( process, category, syst.upper() + pQCD + term.upper() + shift )
                hists[ histTag ] = ROOT.TH1D( histTag, xLabel, len( histBins ) - 1, histBins )
            if config.systematics[ "PS BREAKDOWN" ][ syst ]:
              histTag = hist_tag( process, category, syst.upper() + shift )
              hists[ histTag ] = ROOT.TH1D( histTag, xLabel, len( histBins ) - 1, histBins )
          else:
            histTag = hist_tag( process, category, syst.upper() + shift )
            hists[ histTag ] = ROOT.TH1D( histTag, xLabel, len( histBins ) - 1, histBins )
  if doPDF:
    for i in range( config.params[ "GENERAL" ][ "PDF RANGE" ] ):
      histTag = hist_tag( process, category, "PDF" + str(i) ) 
      hists[ histTag ] = ROOT.TH1D( histTag, xLabel, len( histBins ) - 1, histBins )


  # Sumw2() tells the hist to also store the sum of squares of weights
  for histTag in hists: hists[ histTag ].Sumw2()
	
  if verbose: 
    print( ">> Applying NOMINAL weights: {}".format( mc_weights[ "NOMINAL" ] ) )
    if doABCDNN:
      print( ">> Including ABCDnn weights: {}".format( mc_weights[ "ABCDNN" ] ) )
    
    print( ">> Applying NOMINAL cuts: {}".format( cuts[ "NOMINAL" ] ) )
    if doABCDNN:
      print( ">> Applying ABCDnn cuts: {}".format( cuts[ "ABCDNN" ] ) )

  # draw histograms
  histTag = hist_tag( process, category )
  rTree[ process ].Draw( 
    "{} >> {}".format( variableName, histTag ), 
    "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ "NOMINAL" ] ), 
    "GOFF" )

  if verbose: print( "  + NOMINAL: {} --> {}".format( rTree[ process ].GetEntries(), hists[ histTag ].Integral() ) )

  if doABCDNN:
    rTree[ process + "_ABCDNN" ].Draw(
      "{} >> {}".format( abcdnnName, hist_tag( process, category, "ABCDNN" ) ),
      "{} * ({})".format( mc_weights[ "ABCDNN" ], cuts[ "ABCDNN" ] ),
      "GOFF"
    )
    if verbose: print( "  + ABCDNN: {} --> {}".format( rTree[ process ].GetEntries(), hists[ hist_tag( process, category, "ABCDNN" ) ].Integral() ) )

  if process not in groups[ "DAT" ] and doSYST:
    nSyst, nSystABCDNN = 0, 0
    for syst in config.systematics[ "MC" ].keys():
      if not config.systematics[ "MC" ][ syst ][0]: continue
      for shift in [ "UP", "DN" ]:
        histTag = hist_tag( process, category, syst.upper() + shift )
        if syst.upper() in [ "PREFIRE" ]:
          rTree[ process ].Draw(
            "{} >> {}".format( variableName, histTag ),
            "{} * ({})".format( mc_weights[ syst.upper() ][ shift ], cuts[ "NOMINAL" ] ),
            "GOFF"
          )
          nSyst += 1
        elif syst.upper() in [ "ISR", "FSR" ]:
          for term in [ "cNS", "muR" ]:
            for pQCD in [ "G2GG", "G2QQ", "Q2QG", "X2XG" ]:
              if not config.systematics[ "PS BREAKDOWN" ][ syst + pQCD + term ]: continue
              pQCDTag = hist_tag( process, category, syst.upper() + pQCD + term.upper() + shift )
              rTree[ process ].Draw(
                "{} >> {}".format( variableName, pQCDTag ),
                "{} * ({})".format( mc_weights[ syst.upper() + pQCD + term.upper() ][ shift ], cuts[ "NOMINAL" ] ),
                "GOFF"
              )
              nSyst += 1
          if config.systematics[ "MC" ][ syst ][0]:
            rTree[ process ].Draw(
              "{} >> {}".format( variableName, histTag ),
              "{} * ({})".format( mc_weights[ syst.upper() ][ shift ], cuts[ "NOMINAL" ] ),
              "GOFF"
            )
        elif syst.upper() in [ "PILEUP", "PILEUPJETID", "MURFCORRD", "MUR", "MUF" ]:
          rTree[ process ].Draw( 
            "{} >> {}".format( variableName, histTag ), 
            "{} * ({})".format( mc_weights[ syst.upper() ][ shift ], cuts[ "NOMINAL" ] ), 
            "GOFF" 
          )
          nSyst += 1
        # hot-tagging plots
        elif syst.upper() in [ "HOTSTAT", "HOTCSPUR", "HOTCLOSURE" ] and ( "NH" in category and "NH0p" not in category ):
          rTree[ process ].Draw( 
            "{} >> {}".format( variableName, histTag ), 
            "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ syst.upper() ][ shift ] ), 
            "GOFF" 
          )
          nSyst += 1
        # t-tagging plots
        elif syst.upper() in [ "TAU32", "JMST", "JMRT" ] and ( "NT" in category and "NT0p" not in category ):
          if "ttagged" in variableName.lower() or "tjet" in variableName.lower():
            shift_indx = 2*np.argwhere( np.array([ "TAU32", "JMST", "JMRT" ]) == syst.upper() )[0,0] + np.argwhere( np.array([ "UP", "DN" ]) == shift )[0,0]
            rTree[ process ].Draw( 
              "{}_shifts[{}] >> {}".format( variableName, shift_indx, histTag ), 
              "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ syst.upper() ][ shift ] ), 
              "GOFF" 
            )
            nSyst += 1
          else: 
            rTree[ process ].Draw( 
              "{} >> {}".format( variableName, histTag ), 
              "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ syst.upper() ][ shift ] ), 
              "GOFF" 
            )
            nSyst += 1
        # W-tagging plots
        elif syst in [ "TAU21", "JMSW", "JMRW", "TAU21PT" ] and ( "NW" in category and "NW0p" not in category ):
          if "wtagged" in variableName.lower() or "wjet" in variableName.lower():
            shift_indx = 2*np.argwhere( np.array([ "TAU21", "JMSW", "JMRW", "TAU21PT" ]) == syst.upper() )[0,0] + np.argwhere( np.array([ "UP", "DN" ]) == shift )[0,0]
            rTree[ process ].Draw( 
              "{}_shifts[{}] >> {}".format( variableName, shift_indx, histTag ), 
              "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ syst.upper() ][ shift ] ), 
              "GOFF" 
            )
            nSyst += 1
          else: 
            rTree[ process ].Draw( 
              "{} >> {}".format( variableName, histTag ), 
              "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ syst.upper() ][ shift ] ), 
              "GOFF" 
            )
            nSyst += 1
        # b-tagging plots
        elif syst.upper() in [ "LF", "LFSTATS1", "LFSTATS2", "HF", "HFSTATS1", "HFSTATS2", "CFERR1", "CFERR2" ] and ( "NB" in category and "NB0p" not in category ):
          rTree[ process ].Draw(
            "{} >> {}".format( variableName, histTag ), 
            "{} * ({})".format( mc_weights[ syst.upper() ][ shift ], cuts[ "NOMINAL" ] ), 
            "GOFF" 
          )
          nSyst += 1
        # process jec and jer
        elif syst.upper() in [ "JER" ]: 
          rTree[ process + syst.upper() + shift ].Draw( 
            "{} >> {}".format( variableName, histTag ), 
            "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ "NOMINAL" ] ), 
            "GOFF" 
          )
          nSyst += 1
        elif syst.upper() in [ "JEC" ]:
          for systJEC in config.systematics[ "REDUCED JEC" ]:
            if not config.systematics[ "REDUCED JEC" ][ systJEC ]: continue
            rTree[ process + "JEC" + systJEC.upper().replace( "ERA", "20" + args.year ).replace( "APV", "" ).replace( "_", "" ) + shift ].Draw(
              "{} >> {}".format( variableName, hist_tag( process, category, "JEC" + systJEC.upper().replace( "ERA", "20" + args.year ).replace( "APV", "" ).replace( "_", "" ) + shift ) ),
              "{} * ({})".format( mc_weights[ "NOMINAL" ], cuts[ "NOMINAL" ] ),
              "GOFF" 
            )
            nSyst += 1
        elif syst.upper() in [ "TOPPT" ]:
          rTree[ process ].Draw(
            "{} >> {}".format( variableName, histTag ),
            "{} * ({})".format( mc_weights[ syst.upper() ][ shift ], cuts[ "NOMINAL" ] )
          )
          nSyst += 1
        else:
          print( "[WARN] {} turned on, but excluded for {} in traditional SF {}...".format( syst.upper() + shift, process, category ) )
        if syst.upper() in config.params[ "ABCDNN" ][ "SYSTEMATICS" ] and doABCDNN and config.systematics[ "MC" ][ syst ][0]:
          print( "[ABCDNN] Including {} for ABCDnn {} {}".format( syst.upper() + shift, process, category ) )
          if syst.upper() == "ABCDNNCLOSURE":
            rTree[ process + "_ABCDNN" ].Draw(
              "{} >> {}".format( abcdnnName + "_CLOSURE" + shift, hist_tag( process, category, "ABCDNN", syst.upper() + shift ) ),
              "{} * ({})".format( mc_weights[ "ABCDNN {}".format( syst.upper() ) ][ shift ], cuts[ "ABCDNN" ] ),
              "GOFF"
            )
            nSystABCDNN += 1
          elif syst.upper() == "ABCDNNTAIL":
            rTree[ process + "_ABCDNN" ].Draw(
              "{} >> {}".format( abcdnnName + "_TAIL" + shift, hist_tag( process, category, "ABCDNN", syst.upper() + shift ) ),
              "{} * ({})".format( mc_weights[ "ABCDNN {}".format( syst.upper() ) ][ shift ], cuts[ "ABCDNN" ] ),
              "GOFF"
            )
            nSystABCDNN += 1
          elif syst.upper() == "ABCDNNPEAK":
            rTree[ process + "_ABCDNN" ].Draw(
              "{} >> {}".format( abcdnnName + "_PEAK" + shift, hist_tag( process, category, "ABCDNN", syst.upper() + shift ) ),
              "{} * ({})".format( mc_weights[ "ABCDNN {}".format( syst.upper() ) ][ shift ], cuts[ "ABCDNN" ] ),
              "GOFF"
            )
            nSystABCDNN += 1
    if verbose: print( "[DONE] Added {} systematics and {} ABCDnn systematics".format( nSyst, nSystABCDNN ) ) 
	
  if doPDF:
    for i in range( config.params[ "GENERAL" ][ "PDF RANGE" ] ):
      histTag = hist_tag( process, category, "PDF" + str(i) )
      rTree[ process ].Draw( 
        "{} >> {}".format( variableName, histTag ), 
        "pdfWeights[{}] * {} * ({})".format( i, mc_weights[ "NOMINAL" ], cuts[ "NOMINAL" ] ), 
        "GOFF" 
      )
    if verbose: print( "  + PDF" )
							
  for key in hists: hists[ key ].SetDirectory(0)
  return hists

def numTrueHist( useJES, useABCDNN ):
  def add_process( nHist, group, key, process, shift, postfix ):
    rFile = ROOT.TFile.Open( os.path.join( config.inputDir[ args.year ].replace( "step3", "step1hadds" ), shift + "/", samples.samples[ group ][ process ] + "_{}.root".format( postfix ) ) )
    nHist[ key ] = rFile.Get( "NumTrueHist" ).Integral()
    rFile.Close()
    return nHist

  print( "[START] Retrieving the MC hist count" )
  nHist = {}
  for group in [ "BKG", "SIG" ]:
    for process in groups[ group ]:
      nHist = add_process( nHist, group, process, process, "nominal", "hadd" )
      for shift in [ "up", "down" ]:
        shift_ = "UP" if shift == "up" else "DN"
        if useJES:
          if config.systematics[ "MC" ][ "JEC" ][0]:
            for systJEC in config.systematics[ "REDUCED JEC" ]:
              if not config.systematics[ "REDUCED JEC" ][ systJEC ]: continue
              systJEC_ = systJEC.replace( "Era", "20" + args.year ).replace( "APV", "" )
              if systJEC.upper() == "TOTAL":
                add_process( nHist, group, "JEC" + systJEC_.upper() + shift_.upper(), process, "JEC" + shift, "hadd" )
              else:
                add_process( nHist, group, "JEC" + systJEC_.replace( "_", "" ).upper() + shift_.upper(), process, systJEC_ + shift, "hadd" )
          if config.systematics[ "MC" ][ "JER" ][0]:
            add_process( nHist, group, "JER" + shift_.upper(), process, "JER" + shift, "hadd" )
  return nHist

def make_hists( groups, group, category, nHist, useABCDNN ): 
  # only valid group arguments are DAT, SIG, BKG, TEST
  doSys = config.options[ "GENERAL" ][ "SYSTEMATICS" ] if group in [ "SIG", "BKG", "TEST" ] else False
  hists = {}
  for process in groups[ group ]:
    process_time = time.time()
    rFiles, rTrees = {}, {} 
    variable = args.variable
    isABCDNN = False
    if useABCDNN and args.variable in config.params[ "ABCDNN" ][ "TRANSFER VARIABLES" ] and process in samples.groups[ "BKG" ][ "ABCDNN" ]: 
      for tag in config.params[ "ABCDNN" ][ "TAG" ]:
        if contains_category( category, config.params[ "ABCDNN" ][ "TAG" ][ tag ] ):
          print( "[INFO] Using ABCDnn tag {} sample for: {}".format( tag, process ) )
          isABCDNN = True
          rFiles[ process + "_ABCDNN" ], rTrees[ process + "_ABCDNN" ] = read_tree( os.path.join( config.inputDir[ args.year ].replace( "step3", "step3_ABCDnn" ), "nominal/", samples.samples[ group ][ process ] + "_ABCDnn_hadd.root" ) ) 
    rFiles[ process ], rTrees[ process ] = read_tree( os.path.join( config.inputDir[ args.year ], "nominal/", samples.samples[ group ][ process ] + "_hadd.root" ) )
    if group in [ "SIG", "BKG", "TEST" ]:
      for shift in [ "up", "down" ]:
        shift_ = "UP" if shift == "up" else "DN"
        if config.systematics[ "MC" ][ "JEC" ][0]:
          for systJEC in config.systematics[ "REDUCED JEC" ]:
            systJEC_ = systJEC.replace( "Era", "20" + args.year ).replace( "APV", "" )
            if config.systematics[ "REDUCED JEC" ][ systJEC ]:
              if systJEC == "Total":
                rFiles[ process + "JEC" + systJEC_.upper() + shift_ ], rTrees[ process + "JEC" + systJEC_.upper() + shift_ ] = read_tree( os.path.join( config.inputDir[ args.year ], "JEC" + shift, samples.samples[ group ][ process ] + "_hadd.root" ) )
              else:
                rFiles[ process + "JEC" + systJEC_.upper().replace( "_", "" ) + shift_ ], rTrees[ process + "JEC" + systJEC_.upper().replace( "_", "" ) + shift_ ] = read_tree( os.path.join( config.inputDir[ args.year ], systJEC_ + shift, samples.samples[ group ][ process ] + "_hadd.root" ) )
        if config.systematics[ "MC" ][ "JER" ][0]:
          rFiles[ process + "JER" + shift_ ], rTrees[ process + "JER" + shift_ ] = read_tree( os.path.join( config.inputDir[ args.year ], "JER" + shift, samples.samples[ group ][ process ] + "_hadd.root" ) )
    hists.update( analyze( rTrees, nHist, args.year, process, variable, doSys, config.options[ "GENERAL" ][ "PDF" ], isABCDNN, category, True ) )
    print( "[OK] Added hists for {} in {:.2f} minutes".format( process, round( ( time.time() - process_time ) / 60,2 ) ) )
    del rFiles, rTrees

  if config.options[ "GENERAL" ][ "UE" ] and group in [ "UE" ]:
    for process in groups[ "UE" ]:
      process_time = time.time()
      rTree = read_tree( os.path.join( config.inputDir[ args.year ], "nominal/", samples.samples[ "BKG" ][ process ] + "_hadd.root" ) )
      hists.update( analyze( rTree, nHist, args.year, process, variable, False, config.options[ "GENERAL" ][ "PDF" ], False, category, True ) )
      print( "[OK] Added hists for {} in {:.2f} minutes".format( process, round( ( time.time() - process_time ) / 60, 2 ) ) )

  if config.options[ "GENERAL" ][ "HDAMP" ] and group in [ "HD" ]:
    for process in groups[ "HD" ]:
      process_time = time.time()
      rTree = read_tree( os.path.join( config.inputDir[ args.year ], "nominal/", samples.samples[ "BKG" ][ process ] + "_hadd.root" ) )
      hists.update( analyze( rTree, nHist, args.year, process, variable, False, config.options[ "GENERAL" ][ "PDF" ], False, category, True ) )
      print( "[OK] Added hists for {} in {:.2f} minutes".format( process, round( ( time.time() - process_time ) / 60, 2 ) ) )

  if not os.path.exists( "{}/{}".format( args.subDir, category ) ): os.system( "mkdir -vp {}/{}".format( args.subDir, category ) )
  pickle.dump( hists, open( "{}/{}/{}_{}.pkl".format( args.subDir, category, group, args.variable ), "wb" ) )

def main():
  nHist = numTrueHist( config.options[ "GENERAL" ][ "SYSTEMATICS" ], config.options[ "GENERAL" ][ "ABCDNN" ] )
  if not config.options[ "GENERAL" ][ "TEST" ]:
    for group in [ "DAT", "BKG", "SIG" ]:
      group_time = time.time()
      print( "[START] Processing hists {} for {}".format( args.category, group ) )
      make_hists( groups, group, args.category, nHist, config.options[ "GENERAL" ][ "ABCDNN" ] )
      print( "[DONE] Finished processing hists for {} in {} minutes".format( group, round( ( time.time() - group_time ) / 60, 2 ) ) )
  else:
    test_time = time.time() 
    print( "[START] Processing hists {} for TEST".format( args.category ) )
    make_hists( groups, "TEST", args.category, nHist, config.options[ "GENERAL" ][ "ABCDNN" ] )
    print( "[DONE] Finished processing hists for TEST in {} minutes".format( round( ( time.time() - test_time ) / 60, 2 ) ) )

  print( "[DONE] Finished making hists in {}".format( round( ( time.time() - start_time ) / 60, 2 ) ) )

main()
