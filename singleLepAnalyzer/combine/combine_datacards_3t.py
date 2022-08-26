import CombineHarvester.CombineTools.ch as ch
from argparse import ArgumentParser
import os
import yaml
import ROOT

parser = ArgumentParser()
parser.add_argument( "-c", "--config", help = "YAML configuration file" )
parser.add_argument( "--validation", action = "store_true", help = "Combine custom datacard combinations" )
parser.add_argument( "--correlations", action = "store_true", help = "Adjust bin naming to account for correlations" )
parser.add_argument( "--positive", action = "store_true", help = "Turn off zero and/or negative bins" )
parser.add_argument( "--verbose", action = "store_true", help = "Verbosity of messages" )
args = parser.parse_args()

def hist_key( *args ):
  key = args[0]
  for arg in args[1:]: key += "_{}".format( arg )
  return key
  
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
  def __init__( self, datacards, tag, postfix, removeUnct, verbose, analysis = "TTTX", era = "Run2UL" ):
    print( "[COMBINE] Instantiating harvester class for {} {} analysis".format( era, analysis ) )
    print( "  [INFO] Verbosity {}".format( "ON" if verbose else "OFF" ) )
    self.verbose = verbose        # verbosity of messages
    self.analysis = analysis      # analysis tag, arbitrary
    self.era = era                # era tag, arbitrary
    self.datacards = datacards    # dictionary of datacard paths associated to each analysis channel
    self.tag = tag                # tag used for combination campaign
    self.postfix = postfix        # dictionary of postfixes associated to each analysis channel
    self.removeUnct = removeUnct  # dictionary of uncertainties to remove from each datacard
    self.ch = ch.CombineHarvester()
    pass
  
  def load_datacards( self ):
    print( "[COMBINE] Parsing through datacards, and extracting and organizing bin information" )
    if self.verbose: print( "  [INFO] Considering {} datacards".format( len( self.datacards ) ) )
    self.bins_sorted = { "ALL": [] }
    for datacard in self.datacards:
      self.bins_sorted[ datacard ] = []
      self.ch.ParseDatacard( self.datacards[ datacard ], self.analysis, self.era, datacard, 0, "125" )
      self.ch.cp().channel( [ datacard ] ).ForEachObj( lambda x: self.bins_sorted[ "ALL" ].append( ( x.bin(), hist_key( datacard, x.bin() ) ) ) )
      self.ch.cp().channel( [ datacard ] ).ForEachObj( lambda x: self.bins_dict[ datacard ].append( hist_key( datacard, x.bin() ) ) )
    pass
  
  def remove_uncertainties( self ):
    for key in self.removeUnct:
      for source in self.removeUnct[ key ]:
        self.ch.FilterSysts( lambda x: x.channel() == channel and x.name() == source )
    pass
  
  def format_bin_names( self ):
    print( "[COMBINE] Renaming bins to distinguish channels in final datacard..." )
    for datacard in self.datacards:
      self.ch.cp().channel( [ datacard ] ).ForEachObj( lambda x: x.set_bin( hist_key( datacard, x.bin() ) ) )
    print( "[COMBINE] Renaming autoMCstats bins..." )
    for old, new in list( set( self.bins_sorted[ "ALL" ] ) ):
      self.ch.RenameAutoMCStatsBin( old, new )
    pass
  
  def rename_uncertainties( self ):
    def rename_uncertainty( postfix ):
      def rename_function( x ):
        if x.type() != "rateParam": x.set_name( hist_key( x.name(), suffix ) )
      return rename_function
     
    for analysis in self.postfix:
      postfix = self.config[ "POSTFIX" ][ analysis ]
      self.ch.cp().channel( [ analysis ] ).ForEachSyst( rename_uncertainty( postfix ) )
    pass
  
  def modify_uncertainties( self, bPositive, bValidation, bCorrelation ):
    if bPositive:
      print( "[COMBINE] Turning off zero and/or negative bins" )
      self.ch.FilterProces( lambda x: x.rate() <= 0 )
      self.ch.FilterSysts( lambda x: x.type() == "shape" and x.value_u() <= 0 )
      self.ch.FilterSysts( lambda x: x.type() == "shape" and x.value_d() <= 0 )
    pass
  
  def write_datacard( self ):
    print( "[COMBINE] Preparing main datacard" )
    rOut = ROOT.TFile( "combined_{0}/{1}_combined_{0}.root".format( self.tag, self.analysis ), "RECREATE" )
    self.ch.WriteDatacard( "combined_{}/{}_combined_{}.txt".format( self.tag, self.analysis ), rOut )
    rOut.Close()
  
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
  
  
  
  
  
