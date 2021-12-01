# last updated 11/23/2021 by Daniel Li

import os, sys, argparse, imp

parser = argparse.ArgumentParser()
parser.add_argument( "-y", "--year", default = "17" )
parser.add_argument( "-t", "--test", action = "store_true" )
parser.add_argument( "-n", "--nominal", action = "store_true" )
parser.add_argument( "-b", "--brux", action = "store_true", help = "Store on brux or lpc" )
parser.add_argument( "-o", "--outfolder", default = "default" )
args = parser.parse_args()

if args.test: print( "[OPT] Running in test mode. Only producing one template..." )

if args.year not in [ "16", "16APV", "17", "18" ]: 
  print( "[ERR] Invalid '--year' argument: {}.  Use: 16, 17, 18".format( args.year ) )
  sys.exit()

if not os.path.exists( args.outfolder ):
  print( ">> Creating new directory for CRAB outputs..." )
  outfolder = args.outfolder
  if args.outfolder == "default": outfolder = "crab_output_UL{}".format( args.year ) 
  os.system( "mkdir -p {}".format( outfolder ) )

#Sample list file
sampleListPath = "sampleUL{}.py".format( args.year )
sample = imp.load_source( "sampleUL{}".format( args.year ), sampleListPath, open( sampleListPath, "r" ) )

####################
### SET YOUR STRINGS
####################
#cmsRun config
runTemplate = "../runFWLJMetUL{}_template.py".format( args.year )

#folder to save the created crab configs
configDir = "crab_configs_UL{}".format( args.year ) 
if not os.path.exists( configDir ):
  print( ">> Creating new directory for CRAB configs..." )
  os.system( "mkdir -vp {}".format( configDir ) )

#the crab cfg template to copy from
configTemplate = "config_template.py"

#crab request name
request = "UL" + args.year

#eos out folder
outFolder = args.outfolder

# JSON for Data
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/DCUserPage
jsonData = {
  "16": "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt", # UL URL
  #"16": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt", # UL lxplus
  "16APV": "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt", # UL URL
  #"16APV": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt", # UL lxplus
  "17": "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt", # UL URL
  #"17": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt", # UL lxplus
  "18": "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt", # UL URL
  #"18": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt" # UL lxplus
}

if args.brux:
	outPath = "/store/group/bruxljm/"
	storeSite = "T3_US_Brown"
else:
	outPath = "/store/group/lpcljm/"
	storeSite = "T3_US_FNALLPC"

def create_config_template( sample_dict, **kwargs ):
  for sample_key in sample_dict:
    print( ">> Creating template for {}...".format( sample_key ) )
    configName = "config_{}.py".format( sample_key )
    configPath = os.path.join( configDir, configName )
    runName = "runFWLJMetUL{}_{}.py".format( args.year, sample_key )
    runPath = os.path.join( configDir, runName )

    #copy template file to new directory
    os.system( "cp {} {}".format( configTemplate, configPath ) )
    os.system( "cp {} {}".format( runTemplate, runPath ) )

    #replace strings in new crab file
    os.system( "sed -i 's|CMSRUNCONFIG|{}|g' {}".format( runPath, configPath ) )
    os.system( "sed -i 's|INPUT|{}|g' {}".format( sample_dict[ sample_key ], configPath ) )
    os.system( "sed -i 's|REQNAME|{}|g' {}".format( request, configPath ) )
    os.system( "sed -i 's|OUTFOLDER|{}|g' {}".format( outFolder, configPath ) )
    os.system( "sed -i 's|LOGFOLDER|{}|g' {}".format( sample_key, configPath ) )
    os.system( "sed -i 's|JSONFORDATA|{}|g' {}".format( jsonData, configPath ) )
    os.system( "sed -i 's|ISMC|{}|g' {}".format( kwargs["ISMC"], configPath ) )
    os.system( "sed -i 's|ISTTBAR|{}|g' {}".format( kwargs["ISTTBAR"], configPath ) )
    os.system( "sed -i 's|OUTPATH|{}|g' {}".format( outPath, configPath ) )
    os.system( "sed -i 's|STORESITE|{}|g' {}".format( storeSite, configPath ) )

    #replace strings in new cmsRun file
    if "EGamma" in sample_key or "Single" in sample_key:
      os.system( "sed -i 's|DATASET|{}|g' {}".format( sample_key, runPath ) )
    elif "ext" in sample_key:
      extcode = sample_key[ sample_key.find("ext"): ]
      os.system( "sed -i 's|DATASET|{}-{}|g' {}".format( sample_dict[ sample_key ].split('/')[1], extcode, runPath ) )
    else:
      os.system( "sed -i 's|DATASET|{}|g' {}".format( sample_dict[ sample_key ].split('/')[1], runPath ) )
    os.system( "sed -i 's|ISMC|{}|g' {}".format( kwargs["ISMC"], runPath ) )
    os.system( "sed -i 's|ISTTBAR|{}|g' {}".format( kwargs["ISTTBAR"], runPath ) )
    os.system( "sed -i 's|DOGENHT|{}|g' {}".format( kwargs["DOGENHT"], runPath ) )
    os.system( "sed -i 's|ISTEST|{}|g' {}".format( kwargs["ISTEST"], runPath ) )
    os.system( "sed -i 's|MAXEVENTS|{}|g' {}".format( kwargs["MAXEVENTS"], runPath ) )
    

if __name__ == "__main__":
  if args.test:
    create_config_template(
      sample.groups[ "TEST" ], # TTTW
      ISMC = "True",
      ISTTBAR = "False",
      DOGENHT = "False",
      ISTEST = "True",
      MAXEVENTS = "100"
    )
  else:
    create_config_template(
      sample.groups[ "SIGNAL" ], # TTTW and TTTJ
      ISMC = "True",
      ISTTBAR = "False",
      DOGENHT = "False",
      ISTEST = "False",
      MAXEVENTS = "-1"
    )
    
    create_config_template(
      sample.groups[ "DATA" ], # SingleElectron and SingleMuon
      ISMC = "False",
      ISTTBAR = "False",
      DOGENHT = "False",
      ISTEST = "False",
      MAXEVENTS = "-1"
    )
    
    create_config_template(
      sample.groups[ "TTBAR" ], # Semileptonic, Hadronic, 2L2Nu
      ISMC = "True",
      ISTTBAR = "True",
      DOGENHT = "False",
      ISTEST = "False",
      MAXEVENTS = "-1"
    )
    
    create_config_template(
      sample.groups[ "TOP" ], # Single Top and Rare Top Processes
      ISMC = "True",
      ISTTBAR = "False",
      DOGENHT = "False",
      ISTEST = "False",
      MAXEVENTS = "-1"
    )
    
    create_config_template(
      sample.groups[ "EWK" ], # VV
      ISMC = "True",
      ISTTBAR = "False",
      DOGENHT = "False",
      ISTEST = "False",
      MAXEVENTS = "-1"
    )
    
    create_config_template(
      sample.groups[ "EWKHT" ], # DY and WJets
      ISMC = "True",
      ISTTBAR = "False",
      DOGENHT = "True",
      ISTEST = "False",
      MAXEVENTS = "-1"
    )
    
    create_config_template(
      sample.groups[ "QCDHT" ], # QCD
      ISMC = "True",
      ISTTBAR = "False",
      DOGENHT = "True",
      ISTEST = "False",
      MAXEVENTS = "-1"
    )
