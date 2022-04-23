# import libraries and other scripts
import glob, os, sys, subprocess
import config
import numpy as np
from XRootD import client
from datetime import datetime
from argparse import ArgumentParser
from json import loads as load_json
from json import dump as dump_json

execfile( "EOSSafeUtils.py" )

# read in arguments
parser = ArgumentParser()
parser.add_argument("-y","--year",required=True,help="[16APV,16,17,18]")
parser.add_argument("-l","--log",default="application_log_" + datetime.now().strftime("%d.%b.%Y"),help="Condor job log folder")
parser.add_argument("-i","--inLoc",default="BRUX",help="Step2 file location: BRUX,LPC")
parser.add_argument("-o","--outLoc",default="BRUX",help="Step3 file location: BRUX,LPC")
parser.add_argument("--resubmit",action="store_true",help="Identify failed jobs from Condor logs within the input directory")
parser.add_argument("--verbose", action="store_true", help="Verbosity option")
parser.add_argument("--test", action="store_true", help="If true, produce step3 file for only one sample")
parser.add_argument("--shifts", action="store_true", help="Include JEC/JER samples")
parser.add_argument("folders", nargs="+", help="Folders where model/weights, results are stored")

args = parser.parse_args()

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

def check_samples( inLoc, outLoc, shifts, year ):
  xrdClient = client.FileSystem( "root://brux30.hep.brown.edu:1094/" )
  fStep2 = {}
  fStep3 = {}
  for shift in shifts:
    if inLoc == "LPC":
      eosDir = os.path.join( "/eos/uscms/", config.step2DirEOS[ year ].split( "///" )[1] )
      fStep2[ shift ] = EOSlistdir( os.path.join( eosDir, config.step2Sample[ year ], shift ) )
    elif inLoc == "BRUX":
      status, dirList = xrdClient.dirlist( os.path.join( "/" + config.step2DirBRUX[ year ].split( "//" )[-1], shift ) )
      fStep2[ shift ] = [ item.name for item in dirList ]

    if outLoc == "LPC":
      try:
        eosDir = os.path.join( "/eos/uscms/", config.step3DirEOS[ year ].split( "///" )[1] )
        fStep3[ shift ] = EOSlistdir( os.path.join( eos_dir, config.step3Sample[ year ], shift ) )
      except:
        fStep3[ shift ] = []
    elif outLoc == "BRUX":
      try:
        status, dirList = xrdClient.dirlist( os.path.join( config.step3DirBRUX[ year ], shift ) )
        fStep3[ shift ] = [ item.name for item in dirList ]
      except:
        fStep3[ shift ] = []
  return fStep2, fStep3

def get_jobs( fStep2, fStep3, shifts, log, resubmit, test ):
  sFiles = { shift: [] for shift in shifts }  

  if resubmit:
    print( "[OPT] Running resubmission" )
    count = 0
    outFiles = [ file for file in os.listdir( log ) if ".out" in file ]
    logFiles = [ file for file in os.listdir( log ) if ".log" in file ]

    for oFile in outFiles:
      with open( os.path.join( log, oFile ) ).readlines() as lines:
        if "[OK]" not in lines[-1]:
          sampleName = oFile.split( "hadd" )[0] + "hadd.root"
          sampleTag = oFile.split( "hadd_" )[1].split( "." )[0]
          try: sFiles[ sampleTag ].append( sampleName )
          except: sFiles[ sampleTag ] = [ sampleName ]
          resubmit_count += 1
          if args.verbose: print( ">> Resubmitting failed job: {}".format( sampleName ) )
  
    for lFile in logFiles:
      if lFile.split( "." )[0] + ".out" not in outFiles:
        sampleName = lFile.split( "hadd" )[0] + "hadd.root"
        sampleTag = lFile.split( "hadd_" )[1].split( "." )[0]
        try: sFiles[ sampleTag ].append( sampleName )
        except: sFiles[ sampleTag ] = [ sampleName ]
        resubmit_count += 1
        if args.verbose: print( ">> Resubmitting suspended job: {}".format( sampleName ) )

    for shift in shifts:
      sFiles[shift] = []
      for i, fName in enumerate( fStep2[shift] ):
        if fName not in fStep3[shift]:
          try: sFiles[shift].append(file)
          except: sFiles[shift] = [ file ]
          resubmit_count += 1
          if args.verbose: print( ">> Resubmitting missing step3 job: {}".format( file ) )

    print( ">> {} samples to resubmit".format( resubmit_count ) )
    if resubmit_count == 0: quit( "[ERR] No samples to resubmit, quitting..." )

  else:
    for shift in shifts:
      print( ">> {} samples to submit:".format( shift ) )
      for i, fName in enumerate( sorted( fStep2[shift] ) ):
        print( "   {:<4} {}".format( str(i+1) + ".", fName ) ) 
        sFiles[shift].append(fName)
        if test: break

  return sFiles 

def check_json( folders ):
  jsonFiles = []
  jsonNames = []
  print( ">> Checking for .json parameter files" )
  for folder in folders:
    jsonCheck = glob.glob( "{}/config*.json".format(folder) )
    if len(jsonCheck) > 0:
      if args.verbose: print( "  + {}".format( jsonCheck[0] ) )
      jsonNames.append(jsonCheck[0])
      jsonFiles.append(load_json(open(jsonCheck[0]).read()))
    else:
      quit( "[ERR] No config .json file was found in {}, exiting program...".format( folder ) )

  return jsonFiles, ",".join( jsonNames )

def check_model( folders ):
  models = []
  for folder in folders:
    modelCheck = glob.glob("{}/*.tf".format(folder))
    opt_model = None
    for modelName in modelCheck:
      if "final" in modelName.lower(): opt_model = modelName
    if len(modelCheck) > 0:
      if args.verbose: print( "  + {}".format(opt_model))
      models.append(opt_model)
    else:
      quit( "[ERR] No model found in {}, exiting program...".format(folder) )

  return ",".join( models )
   
 
def submit_condor( fileName, inputDir, outputDir, logDir, shift, models, params ):
  request_memory = "10240" 
  if "tttosemilepton" in fileName.lower() and "ttjj_hadd" in fileName.lower(): request_memory = "14336" 
  if args.resubmit: request_memory = "16384"
  dict = {
    "MODEL"     : models,       
    "PARAMFILE" : params,
    "FILENAME"  : fileName.split( "." )[0],
    "INPUTFILE" : os.path.join( inputDir, shift, fileName ),
    "OUTPUTDIR" : os.path.join( outputDir, shift ),
    "LOGDIR"    : logDir,              
    "SHIFT"     : shift,                  
    "MEMORY"    : request_memory
  }
  jdfName = "{}/{}/{}.job".format( logDir, shift, fileName.split( "." )[0] )
  jdf = open(jdfName, "w")
  jdf.write(
"""universe = vanilla
Executable = application.sh
Should_Transfer_Files = Yes
WhenToTransferOutput = ON_EXIT
request_memory = %(MEMORY)s
Requirements = has_avx == true
Transfer_Input_Files = %(MODEL)s, %(PARAMFILE)s, step3.py, config.py
Output = %(LOGDIR)s/%(SHIFT)s/%(FILENAME)s.out
Error = %(LOGDIR)s/%(SHIFT)s/%(FILENAME)s.err
Log = %(LOGDIR)s/%(SHIFT)s/%(FILENAME)s.log
Notification = Never
Arguments = %(FILENAME)s.root %(INPUTFILE)s %(OUTPUTDIR)s
Queue 1"""%dict
  )
  jdf.close()
  os.system( "condor_submit {}".format( jdfName ) )

def submit_jobs( sFiles, shift, inputDir, outputDir, logDir, models, params ):
  os.system( "mkdir -vp {}/{}".format( logDir, shift ) )
  jobCount = 0
  for fName in sFiles[shift]:
    if args.verbose: print( ">> Submitting Condor job for {}/{}".format( shift, fName ) )
    submit_condor( fName, inputDir, outputDir, logDir, shift, models, params )
    jobCount += 1
  print( ">> {} jobs submitted for {}...".format( jobCount, shift ) )
  return jobCount

def main():    
  print( "[START] Submitting step3 application jobs...")
  voms_init()
  shifts = [ "nominal" ] if not args.shifts else [ "JECup", "JECdown", "JERup", "JERdown" ]

  step2Dir = config.step2DirBRUX[ args.year ] if args.inLoc == "BRUX" else config.step2DirEOS[ args.year ]
  step3Dir = config.step3DirBRUX[ args.year ] if args.outLoc == "BRUX" else config.step3DirEOS[ args.year ]

  fStep2, fStep3 = check_samples( args.inLoc, args.outLoc, shifts, args.year )
  jsonFiles, params = check_json( args.folders )
  models = check_model( args.folders )

  submitFiles = get_jobs( fStep2, fStep3, shifts, args.log, args.resubmit, args.test )

  count = 0
  for shift in shifts:
    count += submit_jobs(
      submitFiles, 
      shift,
      step2Dir,
      step3Dir,
      args.log,
      models,
      params
    )

  print("\n>> {} total jobs submitted...".format(count))
  if args.verbose: print( ">> Condor job logs stored in {}".format( args.log ) )

main()
