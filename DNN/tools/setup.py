#!/usr/bin/env python

import os, sys, getpass, pexpect, subprocess
from subprocess import check_output
from subprocess import call as sys_call
from argparse import ArgumentParser

sys.path.insert(0,"../DNN")

import config

# setup the working area
home = os.path.expanduser( "~/nobackup/CMSSW_10_6_29/src/TTT-singleLep/DNN/" )
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

def create_tar():
  # tar the CMSSW repo
  tarDir = "CMSSW_10_6_29/src/TTT-singleLep/"
  if "CMSSW106_ttt.tgz" in os.listdir( home ):
    print( ">> Deleting existing CMSSW106_ttt.tgz" ) 
    os.system( "rm {}{}".format( home, "CMSSW106_ttt.tgz" ) )
  print( ">> Creating new tar file for CMSSW106_ttt.tgz" )
  tar_command = "tar -C ~/nobackup/TTT-singleLep/ -zcvf CMSSW106_ttt.tgz"
  excludes = [
    "PhysicsTools",
    "RecoEgamma",
    "RecoJets",
    "RecoMET",
    "TopTagger",
    "LJMet-Slimmer-3tops",
    "LJMet",
    "WeightAnalyzer/*"
    "singleLepAnalyzer/*",
    "DNN/notebooks/*",
    "DNN/condor_log*",
    "DNN/dataset*",
    "DNN/application_log*",
    "DNN/*.pkl",
    "*.so",
    "*.tgz",
    ".git/*"
  ]
  for exclude in excludes: tar_command += " --exclude=\"{}\"".format( exclude )
  tar_command += " CMSSW_10_6_29/"
  os.system( tar_command )
  
  print( ">> Transferring CMSSW106_ttt.tgz to EOS" )
  os.system( "xrdcp -f CMSSW106_ttt.tgz root://cmseos.fnal.gov//store/user/{}".format( config.eosUserName ) )
  print( "[OK ] Transfer complete!" )
 
def main():
  partial = print_options()
  voms_init()
  if args.tar: create_tar()  

main()
