#!/usr/bin/python

import os,sys,datetime,itertools
from argparse import ArgumentParser
sys.path.append( os.path.dirname(os.getcwd()) )
from utils import *
import config, utils

parser = ArgumentParser()
parser.add_argument( "-y", "--year", required = True, help = "[16,17,18]" )
parser.add_argument( "-v", "--variables", nargs = "+", required = True )
parser.add_argument( "-p", "--postfix", default = "test" )
parser.add_argument( "-r", "--region", required = True, help = "[SR,PS,TTCR,WJCR]" )
parser.add_argument( "-c", "--categorize", action = "store_true" )
parser.add_argument( "-i", "--inputdir", required = True )
args = parser.parse_args()

thisDir = os.getcwd()

if args.categorize: bins = config.bins[ "templates" ]
else: bins = config.bins[ "baseline" ]

categories = list(
  itertools.product(
    bins[ "lepton" ],
    bins[ "nHOT" ],
    bins[ "nT" ],
    bins[ "nW" ],
    bins[ "nB" ],
    bins[ "nJ" ]
  )
)
	
prefix = "templates"
if args.region == "TTCR": prefix = "ttbar"
if args.region == "WJCR": prefix = "wjets"
if not args.categorize: prefix = "kinematics_{}".format( args.region )
subDir = "{}_UL{}_{}".format( prefix, args.year, args.postfix )
outputPath = os.path.join( os.getcwd(), subDir )
if not os.path.exists( outputPath ): os.system( "mkdir -vp {}".format( outputDir ) )

os.system( "cp ../weightsUL{}.py ../weights.py".format( args.year ) )
os.system( "cp ../samplesUL{}.py ../samples.py".format( args.year ) )
os.system( "cp ../analyze.py ../weights.py ../samples.py ../utils.py hists.py condor_templates.py condor_templates.sh {}".format( outputPath ) )
os.chdir( outputPath )

nJobs = 0
for variable in args.variable:
  print( ">> Generating templates for {}".format( variable ) )
	for category in categories:
		if utils.skip( category ): continue 
		categoryTag = "{}_nHOT{}_nT{}_nW{}_nB{}_nJ{}".format( 
      category[0],
      category[1],
      category[2],
      category[3],
      category[4],
      category[5]
    )
		if (int(cat[1][0])+int(cat[2][0])+int(cat[3][0])+int(cat[4][0])) > int(cat[5][0]):
			print( "[WARN] {} is not topologically possible, skipping...".format( catDir ) )
			continue
		if (int(cat[5][0])==5) and ( ( int(cat[1][0])+int(cat[2][0])+int(cat[3][0])+int(cat[4][0]) ) > 3 ): 
			print( "[WARN] {} has too few signal yield, skipping...".format( catDir ) )
			continue
		if not os.path.exists( os.path.join( outputPath, categoryTag ) ): os.system( "mkdir {}".format( os.path.join( outputPath, categoryTag ) ) )
		os.chdir( categoryTag )
	
		jobParams = {
      "OUTPUTPATH": outputPath,
      "VARIABLE": variable,
      "REGION": args.region,
      "CATEGORIZE": args.categorize,
      "YEAR": args.year,
      "LEPTON": category[0],
      "NHOT":  category[1],
      "NT": category[2],
      "NW": category[3],
      "NB": category[4],
      "NJ": category[5],
      "INPUTDIR": args.inputdir,
			"EXEDIR": thisDir}
	
		jdf = open( "condor_{}.job".format( variable ), "w" )
		jdf.write(
"""universe = vanilla
Executable = %(OUTPUTPATH)s/condor_templates.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
request_memory = 5000
Output = condor_%(VARIABLE)s.out
Error = condor_%(VARIABLE)s.err
Log = condor_%(VARIABLE)s.log
JobBatchName = SLA_step1_3t
Notification = Error
Arguments = %(OUTPUTPATH)s %(VARIABLE)s %(REGION)s %(CATEGORIZE)s %(YEAR)s %(LEPTON)s %(NHOT)s %(NT)s %(NW)s %(NB)s %(NJ)s %(EXEDIR)s
Queue 1"""%job_params)
		jdf.close()
		os.system( "condor_submit condor_{}.job".format( variable ) )
		os.chdir( ".." )
		nJobs += 1

print( "[DONE] Total jobs submitted: {}".format( nJobs ) )
