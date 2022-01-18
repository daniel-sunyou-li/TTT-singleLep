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
parser.add_argument( "-c", "--categorize", action = "store_true" )
parser.add_argument( "-i", "--inputdir", required = True )
args = parser.parse_args()

thisDir = os.getcwd()

if args.categorize:
  if args.region == "TTCR": 
    bins = config.hist_bins[ "TEMPLATES" ]
  elif args.region == "WJCR":
    bins = config.hist_bins[ "TEMPLATES" ]
  elif args.region == "SR":
    bins = config.hist_bins[ "TEMPLATES" ]
  else:
    bins = config.hist_bins[ "TEMPLATES" ]
else: bins = config.hist_bins[ "BASELINE" ]

categories = list(
  itertools.product(
    bins[ "LEPTON" ],
    bins[ "NHOT" ],
    bins[ "NT" ],
    bins[ "NW" ],
    bins[ "NB" ],
    bins[ "NJ" ]
  )
)
	
prefix = "templates"
if args.region == "TTCR": prefix = "ttbar"
if args.region == "WJCR": prefix = "wjets"
if not args.categorize: prefix = "baseline"
subDir = "{}_UL{}_{}".format( prefix, args.year, args.postfix )
outputPath = os.path.join( os.getcwd(), subDir )
if not os.path.exists( outputPath ): os.system( "mkdir -vp {}".format( outputPath ) )

os.system( "cp ../weightsUL{}.py ../weights.py".format( args.year ) )
os.system( "cp ../samplesUL{}.py ../samples.py".format( args.year ) )
os.system( "cp ../analyze.py ../weights.py ../samples.py ../utils.py hists.py condor_templates.py condor_templates.sh {}".format( outputPath ) )
os.chdir( outputPath )

nJobs = 0
for variable in args.variables:
  print( ">> Generating templates for {}".format( variable ) )
  for category in categories:
    if utils.skip( category ): continue 
    categoryTag = "is{}nHOT{}nT{}nW{}nB{}nJ{}".format( 
      category[0],
      category[1],
      category[2],
      category[3],
      category[4],
      category[5]
    )
    if ( int(category[1][0]) + int(category[2][0]) + int(category[3][0]) + int(category[4][0]) ) > int(category[5][0]):
      print( "[WARN] {} is not topologically possible, skipping...".format( categoryTag ) )
      continue
    if ( int(category[5][0]) == 5 ) and ( ( int(category[1][0]) + int(category[2][0]) + int(category[3][0]) + int(category[4][0]) ) > 3 ): 
      print( "[WARN] {} has too few signal yield, skipping...".format( categoryTag ) )
      continue
      
    if not os.path.exists( os.path.join( outputPath, categoryTag ) ): os.system( "mkdir -vp {}".format( os.path.join( outputPath, categoryTag ) ) )
    os.chdir( categoryTag )

    jobParams = {
      "VARIABLE": variable,
      "YEAR": args.year,
      "LEPTON": category[0],
      "NHOT":  category[1],
      "NT": category[2],
      "NW": category[3],
      "NB": category[4],
      "NJ": category[5],
      "EXEDIR": os.path.join( thisDir, subDir ) 
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
JobBatchName = SLA_step1_3t
Notification = Error
Arguments = %(VARIABLE)s %(YEAR)s %(LEPTON)s %(NHOT)s %(NT)s %(NW)s %(NB)s %(NJ)s %(EXEDIR)s
Queue 1"""%jobParams
    )
    jdf.close()
    os.system( "condor_submit condor_step1_{}.job".format( variable ) )
    os.chdir( ".." )
    nJobs += 1
    if config.options[ "TEST" ]: 
      print( "[OPT] Testing one job." )
      break

print( "[DONE] Total jobs submitted: {}".format( nJobs ) )
