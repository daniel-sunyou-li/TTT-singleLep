import CombineHarvester.CombineTools.ch as ch
from argparse import ArgumentParser
import os
import yaml
import ROOT

parser = ArgumentParser()
parser.add_argument( "-c", "--config", help = "YAML configuration file" )
parser.add_argument( "--validation", action = "store_true", help = "Combine custom datacard combinations" )
parser.add_argument( "--correlations", action = "store_true", help = "Adjust bin naming to account for correlations" )
args = parser.parse_args()
  
# global params
tag = config[ "CAMPAIGN_TAG" ] 
datacards = config[ "DATACARDS" ]

class file(object):
  def __init__( self, tag, workingDir ):
    self.tag = tag
    self.workingDir = workingDir
    self.count = 0
    pass
  def write_shell():
    self.file = open( "combined_{}/start_T2W.sh".format( self.tag ), "w" )
    self.file.write( "#!/bin/sh\n" )
    self.file.write( "set -e\n" )
    self.file.write( "ulimit -s unlimited\n" )
    self.file.write( "\n" )
    self.file.write( "cd {}".format( self.workingDir ) )
    self.file.write( "source /cvmfs/cms.cern.ch/cmsset_default.sh\n" )
    self.file.write( "eval `scramv1 runtime -sh`\n" )
    self.file.write( "cd {}/combined_{}/\n\n".format( self.workingDir, self.tag ) )
    self.file.write( "DATACARD=\n" )
    self.file.write( "case $1 in\n" )
    pass
  def write_condor():
    pass
  def write_to( self, text ):
      self.file.write( text )
  def add_datacard( self, datacard ):
    self.file.write( "  {})\n".format( self.count ) )
    self.file.write( "    DATACARD={}\n".format( datacard ) )
    self.file.write( "    ;;\n" )
    self.count += 1
  def close( self ):
    self.file.close()
  
class harvester(object):
  def __init__( self, datacards, config, analysis = "TTTX", era = "Run2UL" ):
    self.config = config
    self.analysis = analysis
    self.era = era
    self.datacards = datacards
    self.ch = ch.CombineHarvester()
    pass
  def load_datacards( self ):
    for datacard in self.datacards:
      self.ch.ParseDatacard( self.datacards[ datacard ], self.analysis, self.era, datacard, 0, "125" )
    pass
  def remove_uncertainties( self ):
    for key in config[ "REMOVE UNCERTAINTIES" ]:
      for source in config[ "REMOVE UNCERTAINTIES" ][ key ]:
        self.ch.FilterSysts( lambda x: x.channel() == channel and x.name() == source )
    pass
  def modify_uncertaintes( self, bValidation, bCorrelation ):
    pass
  def format_bin_names():
    pass
  def rename_uncertainties():
    pass
  def combine_correlations():
    pass

  
def main():
  os.system( "mkdir -vp combined_{}".format( tag ) )
  with open( args.config ) as f:
    config = yaml.safe_load( f )

  out = file( config[ "TAG" ] )
  condor = file( config[ "TAG" ] )
 
  ch_ttt = harvester()
  
  ch_ttt.load_datacards(
    datacards = config[ "DATACARDS" ]
  )
  ch_ttt.remove_uncertainties()
  ch_ttt.modify_uncertainties( args.validation, args.correlation )
  ch_ttt.format_bin_names()
  ch_ttt.rename_uncertainties()
  ch_ttt.combine_correlations()
  
  out.write_shell()
  condor.write_condor()
  
  
  
  
  
