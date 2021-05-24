import os

cmsswbase = "/home/dli50/TTT_1lep/CMSSW_10_2_13/src"

step = 1 # steps range from 1 through 6
postfixes = []
years = ["17"] 
variables = [
  "DNN_4j_1to50"
]

paths = {
  "16": "/home/dli50/TTT_1lep/CMSSW_10_2_13/src/FWLJMET102X_1lep2016_Feb2020_3t_02182021_step3/",
  "17": "/home/dli50/TTT_1lep/CMSSW_10_2_13/src/FWLJMET102X_1lep2017_Oct2019_3t_02182021_step3/",
  "18": "/home/dli50/TTT_1lep/CMSSW_10_2_13/src/FWLJMET102X_1lep2018_Oct2019_3t_02182021_step3/"
}

# this is used in step = 1, 2, 3, 4
trainings = []

for postfix in postfixes:
  for year in years:
    trainings.append(
      {
        "year": "R" + year,
        "variable": variables,
        "postfix": postfix,
        "path": paths[ year ]
      }
    )
    
# this is used in step 5 to combine years
combinations = []

for postfix in postfixes:
  for variable in variables:
    combinations.append(
      {
        "variable": variable,
        "postfix": postfix
      }
    )
    
if step==1:
	os.chdir( "makeTemplates" )
	for training in trainings:
		for variable in training[ "variable" ]:
			os.system( "python doCondorTemplates.py {} {} {} {}".format( training["year"], variable, training["postfix"], training['path'] ) )
			time.sleep( 2 )
	os.chdir( ".." )
  
if step==2:
	os.chdir( "makeTemplates")
	for train in trainings:
		shell_name = 'cfg/condor_step2_'+train['year']+'_'+train['postfix']+'.sh'
		shell=open(shell_name,'w')
		shell.write(
'#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd '+cmsswbase+'\n\
eval `scramv1 runtime -sh`\n\
cd '+os.getcwd()+'\n\
python doTemplates.py '+train['year']+' '+train['postfix']+'\n')
		shell.close()
		jdf_name = 'cfg/condor_step2_'+train['year']+'_'+train['postfix']+'.job'
		jdf=open(jdf_name,'w')
		jdf.write(
'universe = vanilla\n\
Executable = '+os.getcwd()+'/'+shell_name+'\n\
Should_Transfer_Files = YES\n\
WhenToTransferOutput = ON_EXIT\n\
request_memory = 5000\n\
Output = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.out\n\
Error = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.err\n\
Log = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.log\n\
Notification = Error\n\
Arguments = \n\
Queue 1\n')
		jdf.close()
		os.system('condor_submit '+jdf_name)
		print(shell_name)
		# os.system('source '+shell_name+' & ')
		time.sleep(2)
	os.chdir('..')
  
  
  
