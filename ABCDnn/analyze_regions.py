# this script takes in multiple ROOT files and parses them for the event multiplicity in a 2D phase space of two control variables
# last modified September 29, 2021 by Daniel Li

import ROOT
import numpy as np
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument( "-f", "--files", nargs = "+", required = True, help = "ROOT files to read in" )
parser.add_argument( "-x1", "--x1", default = "NJets_JetSubCalc", help = "First control variable" )
parser.add_argument( "-x2", "--x2", default = "NJetsCSV_MultiLepCalc", help = "Second control variable" )
args = parser.parse_args()

rFiles = {}
rTrees = {}

for file in args.files:
  rFiles[ file ] = ROOT.TFile.Open( file )
  rTrees[ file ] = rFiles[ file ].Get( "Events" )

# get event information
n_event = {}
for file in rTrees:
  n_event[ file ] = {
    
  

