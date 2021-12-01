# last updated 11/30/2021 by Daniel Li
import os
from WMCore.Configuration import Configuration
config = Configuration()

# set string, automatically set by create_config_template.py
runConfig      = "CMSRUNCONFIG"
dataset        = "INPUT"
request        = "REQNAME" # this will be UL + the year
outputFolder   = "OUTFOLDER"
logFolder      = "LOGFOLDER" # this will be the sample key name
jsonData       = "JSONFORDATA"
isMC           = ISMC
isVLQsignal    = ISVLQSIGNAL
isTTbar        = ISTTBAR

# general
config.section_( "General" )
config.General.requestName = "{}_{}".format( request, logFolder )
config.General.workArea = "crab_submit_logs/{}/".format( request ) # might want to change this to not be hard-coded
config.General.transferLogs = True
config.General.transferOutputs = True

# job type
config.section_( "JobType" )
config.JobType.pluginName = "Analysis"
config.JobType.psetName = runConfig

# cmsRun params
config.JobType.pyCfgParams = [ "dataset=" + dataset ]
if isMC:
  config.JobType.pyCfgParams = [ "isMC=True" ]
else:
  config.JobType.pyCfgParams = [ "isMC=False" ]

if isTTbar:
  config.JobType.pyCfgParams += [ "isTTbar=True" ]

# runtime, memory, cores
if isMC:
  config.JobType.maxJobRuntimeMin = 2750 # minutes
config.JobType.maxMemoryMB = 4000 # MB, believed to be per core based on CRAB3FAQ TWiki, evidently not based on tests
config.JobType.numCores = 4 # use wisely if turned on.

# Data
config.section_("Data")
config.Data.inputDataset = dataset
config.Data.allowNonValidInputDataset = True
if isMC:
  config.Data.splitting = 'FileBased' # "LumiBased", "Automatic"
  config.Data.unitsPerJob = 1 # 2 if LumiBased # 1440 = 24 hours
else:
	config.Data.splitting = "Automatic"
	config.Data.unitsPerJob = 720 # 24 hours
	config.Data.lumiMask = jsonData
config.Data.inputDBS = "global"
config.Data.ignoreLocality = False
config.Data.publication = False
config.Data.outputDatasetTag = request
config.Data.outLFNDirBase = os.path.join( "OUTPATH", outputFolder )

# site
config.section_( "Site" )
config.Site.storageSite = "STORESITE"
