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
  
