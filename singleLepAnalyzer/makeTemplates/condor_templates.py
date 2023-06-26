#!/usr/bin/python

import os,sys,datetime,itertools
from argparse import ArgumentParser
sys.path.append( "../" )
sys.path.append( "../singleLepAnalyzer/" )
import config
import utils

parser = ArgumentParser()
parser.add_argument( "-y", "--year", required = True, help = "[16,17,18]" )
parser.add_argument( "-v", "--variables", nargs = "+", required = True )
parser.add_argument( "-p", "--postfix", default = "test" )
parser.add_argument( "-r", "--region", required = True, help = "[SR,PS,TTCR,WJCR]" )
args = parser.parse_args()

thisDir = os.getcwd()

if args.region == "TTCR": 
  bins = config.hist_bins[ "VR" ]
elif args.region == "WJCR":
  bins = config.hist_bins[ "VR" ]
elif args.region == "SR":
  bins = config.hist_bins[ "SR" ]
elif args.region == "VR":
  bins = config.hist_bins[ "VR" ]
elif args.region == "BASELINE":
  bins = config.hist_bins[ "BASELINE" ]
elif args.region == "ABCDNN":
  bins = config.hist_bins[ "ABCDNN" ]
else:
  quit( "[ERR] Invalid region argument used. Quitting." )

categories_bin = list(
  itertools.product(
    *[ bins[ key_ ] for key_ in sorted( bins.keys() ) ]
  )
)

categories_key = [ key_ for key_ in sorted( bins.keys() ) ]
	
subDir = "{}_UL{}_{}".format( config.region_prefix[ args.region ], args.year, args.postfix )
outputPath = os.path.join( os.getcwd(), subDir )
if not os.path.exists( outputPath ): os.system( "mkdir -vp {}".format( outputPath ) )

nJobs = 0
for variable in args.variables:
  print( ">> Generating templates for {}".format( variable ) )

  for category in categories_bin:
    categoryTag = "is{}".format( category[ categories_key.index("LEPTON") ] )
    for key_ in categories_key:
      if key_ == "LEPTON": continue
      categoryTag += key_ + category[ categories_key.index(key_) ]
    skip = False
    if "NJ" in categories_key:
      jet_max = int( category[ categories_key.index("NJ") ].strip("p").strip("m").split("b")[-1] )
      jet_sum = 0
      for nj_ in [ "NH", "NT", "NW", "NB" ]:
        if nj_ in categories_key:
          jet_sum += int( category[ categories_key.index(nj_) ].strip("p").strip("m").split("b")[-1] )
      if jet_sum > jet_max: skip = True
      
    if not os.path.exists( os.path.join( outputPath, categoryTag ) ): os.system( "mkdir -vp {}".format( os.path.join( outputPath, categoryTag ) ) )
    os.chdir( os.path.join( outputPath, categoryTag ) )

    jobParams = {
      "VARIABLE": variable,
      "YEAR": args.year,
      "CATEGORY": categoryTag,
      "EXEDIR": thisDir,
      "SUBDIR": subDir,
      "POSTFIX": args.postfix
    }

    jdf = open( "condor_step1_{}.job".format( variable ), "w" )
    jdf.write(
"""universe = vanilla
Executable = %(EXEDIR)s/condor_templates.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
request_memory = 5000
Output = condor_step1_%(VARIABLE)s.out
Error = condor_step1_%(VARIABLE)s.err
Log = condor_step1_%(VARIABLE)s.log
JobBatchName = SLA_step1_%(YEAR)s_%(VARIABLE)s_%(POSTFIX)s
Notification = Error
Arguments = %(VARIABLE)s %(YEAR)s %(CATEGORY)s %(EXEDIR)s %(SUBDIR)s
Queue 1"""%jobParams
    )
    jdf.close()
    os.system( "condor_submit condor_step1_{}.job".format( variable ) )
    os.chdir( ".." )
    nJobs += 1
    if config.options[ "GENERAL" ][ "TEST" ]: 
      print( "[OPT] Testing one job." )
      break

print( "[DONE] Total jobs submitted: {}".format( nJobs ) )
