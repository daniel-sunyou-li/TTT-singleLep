#!/usr/bin/python

import os, sys, time, math, datetime, pickle, itertools, getopt
import numpy as np
from argparse import ArgumentParser

sys.path.append( os.path.dirname( os.getcwd() ) )

import ROOT
import weights
import analyze
import samples
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
parser.add_argument( "-c", "--categorize", action = "store_true" )
parser.add_argument( "-t", "--test", action = "store_true" )
parser.add_argument( "-s", "--shifts", action = "store_true" )
parser.add_argument( "-hd", "--hdamp", action = "store_true" )
parser.add_argument( "-ue", "--ue", action = "store_true" )
parser.add_argument( "-p", "--pdf", action = "store_true" )
parser.add_argument( "-sys", "--systematics", action = "store_true" )
args = parser.parse_args()

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
  "BACKGROUND": [ str( process ) for process in samples.samples[ "BACKGROUND" ] ],
  "UE": [ str( process ) for process in samples.samples[ "UE" ] ],
  "HD": [ str( process ) for process in samples.samples[ "HD" ] ],
  "TEST": [ str( process ) for process in samples.samples[ "TEST" ] ]
}

backgrounds = list( samples.samples[ "BACKGROUND" ].keys() )
hdamp = list( samples.samples[ "HD" ].keys() )
ue = list( samples.samples[ "UE" ].keys() )
signals = list( samples.samples[ "SIGNAL" ].keys() )
data = list( samples.samples[ "DATA" ].keys() )
         		
def read_tree( file ):
  if not os.path.exists(file):
    print("[ERR] {} does not exist.  Exiting program...".format(file))
    sys.exit(1)
  rootFile = TFile( file, "READ" )
  rootTree = rootFile.Get( "ljmet" )
  return rootTree

def make_hists( groups, group ): 
  # only valid group arguments are DATA, SIGNAL, BACKGROUND
  doSys = args.systematics if group in [ "SIGNAL", "BACKGROUND" ] else False
  hists = {}
  for process in groups[ group ]:
    process_time = time.time()
    rTrees = {}
    rTrees[ process ] = read_tree( os.path.join( config.inputDir, "nominal/", samples.samples[ group ][ process ] ) )
    if args.shifts and group in [ "SIGNAL", "BACKGROUND" ]:
      for sys in [ "JEC", "JER" ]:
        for shift in [ "up", "down" ]:
          rTrees[ process + sys + shift ] = read_tree( os.path.join( config.inputDir, sys + shift, samples.samples[ group ][ process ] ) )
    hists.update( analyze.analyze( rTrees, args.year, process, args.variable, doSys, args.pdf, category, True ) )
    print( "[OK] Added hists for {} in {:.2f} minutes".format( process, round( ( time.time() - process_time ) / 60,2 ) ) )
    del rTrees
  if args.ue and group in [ "BACKGROUND" ]:
    for process in groups[ "UE" ]:
      process_time = time.time()
      rTree = read_tree( os.path.join( config.inputDir, "nominal/", samples.samples[ "UE" ][ process ] ) )
      hists.update( analyze.analyze( rTree, args.year, process, args.variable, False, args.pdf, category, True ) )
      del rTree
      print( "[OK] Added hists for {} in {:.2f} minutes".format( process, round( ( time.time() - process_time ) / 60,2 ) ) )
  if args.hdamp and group in [ "BACKGROUND" ]:
    for process in groups[ "HD" ]:
      process_time = time.time()
      rTree = read_tree( os.path.join( config.inputDir, "nominal/", samples.samples[ "HD"][ process ] ) )
      hists.update( analyze.analyze( rTree, args.year, process, args.variable, False, args.pdf, category, True ) )
      del rTree
      print( "[OK] Added hists for {} in {:.2f} minutes".format( process, round( ( time.time() - process_time ) / 60,2 ) ) )
  pickle.dump( hists, open( "{}_{}.pkl".format( group, args.variable ), "wb" ) )
  
for group in [ "DATA", "BACKGROUND", "SIGNAL" ]:
  group_time = time.time()
  print( ">> Processing hists for {}".format( group ) )
  make_hists( groups, group )
  print( "[DONE] Finished processing hists for {} in {} minutes".format( group, round( ( time.time() - group_time ) / 60,2 ) ) )
  
print( "[DONE] Finished making hists in {}".format( % (round( (time.time() - start_time ) / 60, 2 ) ) )
