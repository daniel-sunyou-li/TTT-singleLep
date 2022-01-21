#!/usr/bin/python

import os, sys, time, math, datetime, pickle, itertools, getopt
import numpy as np
from argparse import ArgumentParser

sys.path.append( os.path.dirname( "../" ) ) 

import analyze
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

def make_hists( groups, group, category ): 
  # only valid group arguments are DATA, SIGNAL, BACKGROUND, TEST
  doSys = config.options[ "SYSTEMATICS" ] if group in [ "SIGNAL", "BACKGROUND", "TEST" ] else False
  hists = {}
  for process in groups[ group ]:
    process_time = time.time()
    rFiles, rTrees = {}, {} 
    rFiles[ process ], rTrees[ process ] = read_tree( os.path.join( config.inputDir[ args.year ], "nominal/", samples.samples[ group ][ process ] + "_hadd.root" ) )
    if config.options[ "GENERAL" ][ "JET SHIFTS" ] and group in [ "SIGNAL", "BACKGROUND" ]:
      for syst in [ "JEC", "JER" ]:
        for shift in [ "up", "down" ]:
          rFile[ process + syst + shift ], rTrees[ process + syst + shift ] = read_tree( os.path.join( config.inputDir, sys + shift, samples.samples[ group ][ process ] ) )
    hists.update( analyze.analyze( rTrees, args.year, process, args.variable, doSys, config.options[ "GENERAL" ][ "PDF" ], category, True ) )
    print( "[OK] Added hists for {} in {:.2f} minutes".format( process, round( ( time.time() - process_time ) / 60,2 ) ) )
    del rFiles, rTrees
  if config.options[ "GENERAL" ][ "UE" ] and group in [ "BACKGROUND" ]:
    for process in groups[ "UE" ]:
      process_time = time.time()
      rTree = read_tree( os.path.join( config.inputDir[ args.year ], "nominal/", samples.samples[ "BACKGROUND" ][ process ] + "_hadd.root" ) )
      hists.update( analyze.analyze( rTree, args.year, process, args.variable, False, config.options[ "GENERAL" ][ "PDF" ], category, True ) )
      print( "[OK] Added hists for {} in {:.2f} minutes".format( process, round( ( time.time() - process_time ) / 60, 2 ) ) )
  if config.options[ "GENERAL" ][ "HDAMP" ] and group in [ "BACKGROUND" ]:
    for process in groups[ "HD" ]:
      process_time = time.time()
      rTree = read_tree( os.path.join( config.inputDir[ args.year ], "nominal/", samples.samples[ "BACKGROUND" ][ process ] + "_hadd.root" ) )
      hists.update( analyze.analyze( rTree, args.year, process, args.variable, False, config.options[ "GENERAL" ][ "PDF" ], category, True ) )
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
