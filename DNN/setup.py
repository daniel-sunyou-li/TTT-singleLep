#!/usr/bin/env python

import os, sys, getpass, pexpect, subprocess
from subprocess import check_output
from subprocess import call as sys_call
from argparse import ArgumentParser

sys.path.insert(0,"../DNN")

import config

# setup the working area
home = os.path.expanduser( "~/nobackup/TTT-singleLep/CMSSW_10_6_19/src/TTT-singleLep/DNN/" )
brux_pwd = None

parser = ArgumentParser()
parser.add_argument( "-y",   "--year",        default = "17",      help = "Which production year samples to transfer" )
parser.add_argument( "-sys", "--systematics", action = "store_true", help = "Include the systematic samples" )
parser.add_argument( "-t",   "--tar",         action = "store_true", help = "Tar the CMSSW directory and transfer to EOS" )
parser.add_argument( "-eos", "--eos",         action = "store_true", help = "Transfer from BRUX to EOS" )
parser.add_argument( "-v",   "--verbose",     action = "store_true", help = "Turn verbosity on" )
args = parser.parse_args()

if args.year not in [ "16", "17", "18" ]: sys.exit( "[ERR] {} is an invalid option for -y (--year). Choose from: 16, 17, 18." )

all_samples      = config.all_samples[ args.year ]
sig_training     = config.sig_training[ args.year ] 
bkg_training     = config.bkg_training[ args.year ]
training_samples = sig_training + bkg_training
step2Sample      = config.step2Sample[ args.year ]  
step2DirBRUX     = config.step2DirBRUX[ args.year ] 
step2DirLPC      = config.step2DirLPC[ args.year ]
step2DirXRD      = config.step2DirXRD[ args.year ]
step2DirEOS      = config.step2DirEOS[ args.year ]

samples = [ all_samples[ sample_key ][0] for sample_key in all_samples.keys() ]

def print_options():
  print( ">> OPTIONS:" )
  print( "{} Include systematic samples".format( "[ON ]" if args.systematics else "[OFF]" ) )
  print( "{} CMSSW Tar".format( "[ON ]" if args.tar else "[OFF]" ) )
  print( "{} Verbosity".format( "[ON ]" if args.verbose else "[OFF]" ) )
  
def check_voms(): # used in voms_init
  print( ">> Checking grid certificate validation (VOMS)..." )
  try:
    output = check_output("voms-proxy-info", shell = True)
    print( output.rfind("timeleft") )
    print( output[ output.rfind(": ") + 2: ] )
    if output.rfind( "timeleft" ) > -1:
      if int( output[ output.rfind( ": " ) + 2: ].replace(":","") ) > 0:
        print( "[OK ] VOMS found" )
        return True
    return False
  except:
    return False
  
def voms_init(): # run independently
  if not check_voms():
    print( ">> Initializing grid certificate..." )
    output = check_output( "voms-proxy-init --rfc --voms cms", shell = True )
    if "failure" in output:
      print( ">> Incorrect password entered, try again." )
      voms_init()
    print( "[OK ] Grid certificate initialized" )
    
def brux_auth():
  global brux_pwd
  print( ">> Password for {}@brux.hep.brown.edu".format( config.bruxUserName ) )
  if brux_pwd == None:
    brux_pwd = getpass.getpass( ">> Password: " )
  
def brux_to_lpc( directoryBRUX, sample, step2Dir ):
  print( ">> Transffering {} to {}".format( os.path.join( directoryBRUX, sample ), step2Dir ) )
  child = pexpect.spawn( "scp -r {}@brux.hep.brown.edu:{} ./{}".format(
    config.bruxUserName,
    os.path.join( directoryBRUX, sample ),
    step2Dir
    ))
    
  opt = 1
  while opt == 1:
    opt = child.expect( [ config.bruxUserName + "@brux.hep.brown.edu's password: ",
      "Are you sure you want to continue connecting (yes/no)? " ] )
    if opt == 1:
      child.sendline( "yes" )
  child.sendline( brux_pwd )
  child.interact()
  

def brux_to_eos( year, systematics, samples ):
  include_systematics = "" if not systematics else ", including systematics"
  print( ">> Transferring samples from BRUX to LPC for {} samples{}".format( year, include_systematics ) )
  # create the necessary directories
  # create directories in lpc
  if step2Sample not in os.listdir( home ):
    print( ">> Creating LPC directory for Step2 samples" )
    sys_call( "mkdir -p {}{}".format( home, step2Sample ), shell = True )
  if "nominal" not in os.listdir( os.path.join( home, step2Sample ) ):
    print( ">> Creating LPC directory for nominal samples" )
    os.system( "mkdir -p {}{}/nominal".format( home, step2Sample ) )
  if args.systematics:
    for syst in [ "JEC", "JER" ]:
      for dir in [ "up", "down" ]:
        if syst + dir not in os.listdir( home + step2Sample ):
          print( ">> Creating LPC directory for systematic: {}{}".format( syst, dir ) )
          os.system( "mkdir -p {}{}/{}{}".format( home, step2Sample, syst, dir ) )
          
# create directories in EOS
  eosContent = subprocess.check_output( "eos root://cmseos.fnal.gov ls /store/user/{}/".format( config.eosUserName ), shell=True )
  if step2Sample not in eosContent:
    print(">> Creating EOS directory for nominal samples")
    sys_call( "eos root://cmseos.fnal.gov mkdir /store/user/{}/{}".format( config.eosUserName, step2Sample ), shell = True )
  if "nominal" not in subprocess.check_output( "eos root://cmseos.fnal.gov ls /store/user/{}/{}".format ( config.eosUserName, step2Sample ), shell = True ):
    sys_call( "eos root://cmseos.fnal.gov mkdir /store/user/{}/{}/nominal".format( config.eosUserName, step2Sample ), shell = True )
  if args.systematics:
    for syst in [ "JEC", "JER" ]:
      for dir in [ "up", "down" ]:
        if syst + dir not in subprocess.check_output( "eos root://cmseos.fnal.gov ls /store/user/{}/{}".format( config.eosUserName, step2Sample ), shell = True ):
          print( ">> Creating EOS directory for systematic: {}{}".format( syst, dir ) )
          sys_call( "eos root://cmseos.fnal.gov mkdir /store/user/{}/{}/{}{}".format( config.eosUserName, step2Sample, syst, dir ), shell = True )

  eos_samples = {
    "nominal": check_output( "eos root://cmseos.fnal.gov ls /store/user/{}/{}/nominal/".format( config.eosUserName, step2Sample ), shell = True )
  }

  if args.systematics:
    for syst in [ "JEC", "JER" ]:
      for dir in [ "up", "down" ]:
        eos_samples[ syst + dir ] = check_output( "eos root://cmseos.fnal.gov ls /store/user/{}/{}/{}{}/".format( config.eosUserName, step2Sample, syst, dir ), shell = True )

# transfer samples from BRUX to EOS 
  for sample in samples:
    if sample not in eos_samples[ "nominal" ]:
      if sample not in os.listdir( "{}{}/nominal/".format( home, step2Sample ) ):
        print( ">> Transferring {} to {}/nominal/".format( sample, step2Sample ) )
        brux_to_lpc(
          os.path.join( step2DirBRUX, "nominal" ),
          sample,
          os.path.join( step2Sample, "nominal" )
        ) 

      print( ">> Transferring {} to /nominal/ EOS".format( sample ) )
      sys_call( "xrdcp {} {}".format(
        os.path.join( step2DirLPC, "nominal", sample ),
        os.path.join( step2DirEOS, "nominal" )
      ), shell = True )
      print( ">> Removing {} files from /nominal/ LPC".format( sample ) )
      os.system( "rm {}".format( os.path.join( step2DirLPC, "nominal", sample ) ) )
      print( "[OK ] {} exists in /nominal/ on EOS, skipping...".format( sample ) ) 
      
    if args.systematics:
      for syst in [ "JEC", "JER" ]:
        for dir in [ "up", "down" ]:
          if "up" in sample.lower() or "down" in sample.lower(): continue
          if "muon" in sample.lower() or "electron" in sample.lower() or "egamma" in sample.lower() or "jetht" in sample.lower(): continue
          if sample not in eos_samples[ syst + dir ]:
            if sample not in os.listdir( os.path.join( home, step2Sample, syst + dir ) ):
              print( ">> Transferring {} to {}".format( sample, os.path.join( step2Sample, syst + dir ) ) )
              brux_to_lpc(
                os.path.join( step2DirBRUX, syst + dir ),
                sample,
                os.path.join( step2Sample, syst + dir )
              ) 
              print( ">> Removing {} from /{}{}/ on LPC".format( sample, syst, dir ) )
            print( ">> Transferring {} to /{}{}/ on EOS".format( sample, syst, dir ) )
            sys_call( "xrdcp {} {}/".format(
              os.path.join( step2DirLPC, syst + dir, sample ),
              os.path.join( step2DirEOS, syst + dir )
            ), shell = True )
            if args.remove:
              print( ">> Removing all {} files from /{}{}/ LPC".format( sample, syst, dir ) )
              os.system( "rm {}".format( os.path.join( step2DirLPC, syst + dir, sample ) ) ) 
          else: print( "[OK ] {} exists in /{}{}/ on EOS, skipping...".format( sample, syst, dir ) )
    print( "[OK ] Transfer of {} from BRUX to EOS complete.  Proceeding to next sample.\n".format( sample ) ) 

  print( "[OK ] All samples transferred..." )

def create_tar():
  # tar the CMSSW repo
  tarDir = "CMSSW_10_6_9/src/TTT-singleLep/"
  if "CMSSW1069_ttt.tgz" in os.listdir( home ):
    print( ">> Deleting existing CMSSW1069_ttt.tgz" ) 
    os.system( "rm {}{}".format( home, "CMSSW1069_ttt.tgz" ) )
  print( ">> Creating new tar file for CMSSW1069_ttt.tgz" )
  os.system( "tar -C ~/nobackup/TTT-singleLep/ -zcvf CMSSW1069_ttt.tgz --exclude=\"{}\" --exclude=\"{}\" --exclude=\"{}\" --exclude=\"{}\" --exclude=\"{}\" --exclude=\"{}\" --exclude=\"{}\" --exclude=\"{}\"  --exclude=\"{}\" --exclude=\"{}\" --exclude=\"{}\" {}".format(
    tarDir + "LJMet-Slimmer-3tops/*",
    tarDir + "singleLepAnalyzer/*",
    tarDir + "FWLJMET/*",
    tarDir + "ABCDnn/*",
    tarDir + "DNN/condor_log*",
    tarDir + "DNN/dataset*",
    tarDir + "DNN/application_log*",
    tarDir + "DNN/notebooks/*",
    tarDir + "DNN/*.pkl",
    tarDir + "*.tgz",
    tarDir + ".git/*",
    "CMSSW_10_6_9/" 
  ) )
  print( ">> Transferring CMSSW1069_ttt.tgz to EOS" )
  os.system( "xrdcp -f CMSSW1069_ttt.tgz root://cmseos.fnal.gov//store/user/{}".format( config.eosUserName ) )
  print( "[OK ] Transfer complete!" )
 
def main():
  partial = print_options()
  voms_init()
  if args.eos: brux_auth()
  if args.eos: brux_to_eos( args.year, args.systematics, samples )
  if args.tar: create_tar()  

main()
