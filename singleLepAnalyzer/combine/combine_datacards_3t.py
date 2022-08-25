import CombineHarvester.CombineTools.ch as ch
from argparse import ArgumentParser
import os
import yaml
import ROOT

parser = ArgumentParser()
parser.add_argument( "-c", "--config", help = "YAML configuration file" )
args = parser.parse_args()

with open( args.config ) as f:
  config = yaml.safe_load( f )
  
# global params
tag = config[ "CAMPAIGN_TAG" ] 
datacards = config[ "DATACARDS" ]
  
os.system( "mkdir -vp combined_{}".format( tag ) )

T2W = open( "combined_{}/prepareT2W.sh".format( tag ), "w" )
T2W.write( "#!/bin/sh\n" )
T2W.write( "set -e\n" )
T2W.write( "ulimit -s unlimited\n\n" )
T2W.write( "cd \n" )
T2W.write( "source /cvmfs/cms.cern.ch/cmsset_default.sh\n" )
T2W.write( "eval `scramv1 runtime -sh`\n" )
T2W.write( "cd \n" )
T2W.write( "DATACARD=\n" )
T2W.write( "case $1 in\n" )

T2W_COUNT = 0

class 
