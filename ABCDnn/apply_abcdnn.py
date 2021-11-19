# apply a trained ABCDnn model to ttbar samples and create new step3's
# last updated 10/25/2021 by Daniel Li

import glob, os, sys, subprocess
import config
import numpy as np
from datetime import datetime
from argparse import ArgumentParser


# read in arguments
parser = ArgumentParser()
parser.add_argument( "-y", "--year", required = True, default = "2017" )
parser.add_argument( "-t", "--test", default = False )
parser.add_argument( "-l", "--log", default= "application_log_" + datetime.now().strftime("%d.%b.%Y") )
parser.add_argument( "-r", "--resubmit", action = "store_true" )
parser.add_argument( "-w", "--weights", required = True, help = "Trained weight tag" )
args = parser.parse_args()

# check if folder has necessary components

# paths 
condorDir    = config.step2DirEOS[ args.year ]
step3Samples = []

# determine which samples to run on
if args.test: print( ">> Running in test mode..." )
if args.resubmit: 
  print( ">> Running in resubmit mode, resubmitting the following samples" )
  doneSamples = [ sample for sample in subprocess.check_output( "eos root://cmseos.fnal.gov ls /store/user/{}/{}/nominal/".format( config.eosUserName, step3Sample ), shell = True ).split( "\n" )[:-1] if "abcdnn" in sample ]
  for sample in config.apply_samples[ args.year ]:
    if sample.replace( "hadd", "abcdnn" ) not in doneSamples: step3Samples.append( sample )
else: 
  print( ">> Applying trained model {} to the following samples:" )
  step3Samples = list( config.apply_samples[ args.year ][0] ) if args.test else config.apply_samples[ args.year ]
for sample in step3Samples:
  print( "    - {}".format( sample ) )

# general methods
def check_voms():
  print( ">> Checking VOMS" )
  try:
    output = subprocess.check_output( "voms-proxy-info", shell = True )
    if output.rfind( "timeleft" ) > - 1:
      if int( output[ output.rfind(": ")+2: ].replace( ":", "" ) ) > 0:
        print( "[OK ] VOMS found" )
        return True
      return False
  except: return False

def voms_init():
  if not check_voms():
    print( ">> Initializing VOMS" )
    output = subprocess.check_output( "voms-proxy-init --voms cms", shell = True )
    if "failure" in output:
      print( "[WARN] Incorrect password entered. Try again." )
      voms_init()
    print( "[OK ] VOMS initialized" )

def create_tar():
  tarDir = os.getcwd()
  if "ABCDnn.tgz" in os.listdir( os.getcwd() ): os.system( "rm ABCDnn.tgz" ) 
  os.system( "tar -C {} -zcvf ABCDnn.tgz --exclude=\"{}\" {}".format(
      os.getcwd()[:-(len("ABCDnn"))],
      "Data/*",
      "ABCDnn/"
    )
  )
  print( ">> Transferring ABCDnn.tgz to EOS" )
  os.system( "xrdcp -f ABCDnn.tgz root://cmseos.fnal.gov//store/user/{}".format( config.eosUserName ) )

def condor_job( fileName, condorDir, sampleDir, logDir, tag ):
  request_memory = "5120" 
  if "tttosemilepton" in fileName.lower() and "ttjj_hadd" in fileName.lower(): request_memory = "10240" 
  if args.resubmit != None: request_memory = "16384"
  dict = {
    "FILENAME"  : fileName,            
    "CONDORDIR" : condorDir,           
    "OUTPUTDIR" : sampleDir,   
    "TAG"       : tag,        
    "LOGDIR"    : logDir,              
    "EOSNAME"   : config.eosUserName,
    "MEMORY"    : request_memory
  }
  jdfName = "{}/{}_{}.job".format(logDir,fileName,tag)
  jdf = open(jdfName, "w")
  jdf.write(
"""universe = vanilla
Executable = apply_abcdnn.sh
Should_Transfer_Files = Yes
WhenToTransferOutput = ON_EXIT
request_memory = %(MEMORY)s
Output = %(LOGDIR)s/%(FILENAME)s_%(TAG)s.out
Error = %(LOGDIR)s/%(FILENAME)s_%(TAG)s.err
Log = %(LOGDIR)s/%(FILENAME)s_%(TAG)s.log
Notification = Never
Arguments = %(CONDORDIR)s %(FILENAME)s %(SAMPLEDIR)s %(EOSNAME)s %(TAG)s
Queue 1"""%dict
  )
  jdf.close()
  os.system( "condor_submit {}".format( jdfName ) )

def submit_jobs( files, key, condorDir, logDir, sampleDir ):
  os.system( "mkdir -p " + logDir )
  jobCount = 0
  for file in files[key]:
    if args.verbose: print( ">> Submitting Condor job for {}/{}".format( key, file ) )
    condor_job( file.split(".")[0], condorDir, sampleDir, logDir, key )
    jobCount += 1
  print( ">> {} jobs submitted for {}/...".format( jobCount, key ) )
  return jobCount

def main( files ):
  count = submit_jobs( files, "nominal", condorDir, logDir, sampleDir ):

voms_init()
main( step3Samples )




