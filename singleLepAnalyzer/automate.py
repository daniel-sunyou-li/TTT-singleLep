import os, time
from argparse import ArgumentParser

cmsswbase = "/home/dli50/TTT_1lep/CMSSW_10_6_19/src"
cmsswbase = os.path.join( os.getcwd(), ".." )

parser = ArgumentParser()
parser.add_argument( "-s", "--step", required = True, help = "Options: 1-6" )
parser.add_argument( "-y", "--years", nargs = "+", required = True, help = "Options: 16, 17, 18" )
parser.add_argument( "-t", "--tags", nargs = "+", required = True )
parser.add_arugment( "-v", "--variables", nargs = "+", required = True )
args = parser.parse_args()


# this is used in step = 1, 2, 3, 4

def get_trainings( tags, years, variables ):
  trainings = []
  for tag in tags:
    for year in years:
      trainings.append( {
        "year": "UL{}".format( year ),
        "variable": variables,
        "tag": tag,
        "path": config.step3Dir[ year ]
      } )
  return trainings
    
  
def produce_templates():
  trainings = get_trainings( args.tags, args.years, args.variables )
  os.chdir( "makeTemplates" )
  for training in trainings:
    for variable in training[ "variable" ]:
      os.system( "python condor_templates.py -y {} -v {} -p {} -i {} -r {} --categorize".format( 
        training[ "year" ],
        variable,
        training[ "tag" ],
        training[ "path" ],
        "SR"
      ) )
      time.sleep( 1 )
  os.chdir( ".." )
                
def run_templates():
  trainings = get_trainings( args.tags, args.years, args.variables )
  os.chdir( "makeTemplates" )
  if not os.path.exists( "condor_config" ): os.system( "mkdir -vp condor_config" )
  for training in trainings:
    step2_name = "condor_step2_UL{}_{}".format( training[ "year" ], training[ "tag" ] )
    shell_name = "condor_config/{}.sh".format( step2_name )
    shell = open( shell_name, "w" )
    shell.write(
"#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd {} \n\
eval `scramv1 runtime -sh`\n\
cd {} \n\
python templates.py -y {} -t {} \n".format( cmsswbase, os.getcwd(), training[ "year" ], training[ "tag" ] )
    )
    shell.close()
    jdf_name = "condor_config/{}.job".format( step2_name )
    jdf = open( jdf_name, "w" )
    jdf.write(
"universe = vanilla \n\
Executable = {}/{}\n\
Should_Transfer_Files = YES\n\
WhenToTransferOutput = ON_EXIT\n\
JobBatchName = SLA_step2\n\
request_memory = 5000\n\
Output = {}/condor_log/{}.out\n\
Error = {}/condor_log/{}.err\n\
Log = {}/condor_log/{}.log\n\
Notification = Error\n\
Arguments = \n\
Queue 1\n".format( os.getcwd(), shell_name, os.getcwd(), step2_name, os.getcwd(), step2_name, os.getcwd(), step2_name ) 
    )
    jdf.close()
		os.system( "condor_submit {}".format( jdf_name ) )
		time.sleep(1)
	os.chdir("..")
  
def produce_binned_plots():
  trainings = get_trainings( args.tags, args.years, args.variables )
  os.chdir( "makeTemplates" )
  for train in trainings:
    for variable in train[ "variable" ]:
      condor_name = "condor_step3_{}_{}_{}".format( train[ "year" ], train[ "tag" ], variable )
      shell_name = "condor_config/{}.sh".format( condor_name )
      shell = open( shell_name, "w" )
      shell.write(
"#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd {} \n\
eval `scramv1 runtime -sh`\n\
cd {} \n\
python modify_binning.py -y {} -v {} -t {} \n\
python plot_templates.py -y {} -v {} -t {} \n\ ".format( 
  cmsswbase, os.getcwd(), 
  train[ "year" ], variable, train[ "tag" ], 
  train[ "year" ], variable, train[ "tag" ]
)
      )
      shell.close()
      jdf_name = "crab_config/{}.job".format( condor_name ) 
      jdf = open( jdf_name, "w" )
      jdf.write(
"""universe = vanilla \n\
Executable = {}/{}\n\
Should_Transfer_Files = YES\n\
WhenToTransferOutput = ON_EXIT\n\
JobBatchName = SLA_step3\n\
request_memory = 3072\n\
Output = {}/condor_log/{}.out\n\
Error = {}/condor_log/{}.err\n\
Log = {}/condor_log/{}.log\n\
Notification = Error\n\
Arguments = \n\
Queue 1""".format(
  os.getcwd(), shell_name,
  os.getcwd(), condor_name, os.getcwd(), condor_name, os.getcwd(), condor_name
)
      )
			jdf.close()
			os.system( "condor_submit {}".format( jdf_name ) )
	os.chdir( ".." )
  
def run_combine():
  trainings = get_trainings( args.tags, args.years, args.variables )
  os.chdir( "combine" )
  for training in trainings:
    for variable in training[ "variable" ]:
      condor_name = "condor_step4_{}_{}_{}".format( training[ "year" ], training[ "tag" ], variable )
      shell_name = "condor_config/{}.sh".format( condor_name )
      shell = open( shell_name, "w" )
      shell.write(
"#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd {} \n\
eval `scramv1 runtime -sh`\n\
cd {} \n\
python make_datacard.py -y {} -v {} -t {} \n\
cd limits_UL{}_{}_{}\n\
combine -M Significance cmb/workspace.root -t -l --expectSignal=1 --cminDefaultMinimizerStrategry 0 &> significance.txt\n\
combine -M AsymptoticLimits cmb/workspace.root --run=blind --cminDefaultMinimizerStrategy 0&> limits.txt\n\
cd ..\n".format(
  cmsswbase, os.getcwd(),
  training[ "year" ], variable, training[ "tag" ], 
  training[ "year" ], training[ "tag" ], variable,
)
      )
      shell.close()
      jdf_name = "condor_config/{}.job".format( condor_name )
      jdf = open( jdf_name, "w" )
      jdf.write(
"""universe = vanilla \n\
Executable = {}/{} \n\
Should_Transfer_Files = YES \n\
WhenToTransferOutput = ON_EXIT \n\
JobBatchName = SLA_step4 \n\
request_memory = 3072 \n\
Output = {}/conodr_log/{}.out \n\
Error = {}/condor_log/{}.err \n\
Log = {}/condor_log/{}.log \n\
Notification = Error \n\
Arguments = \n\
Queue 1""".format(
  os.getcwd(), shell_name,
  os.getcwd(), condor_name, os.getcwd(), condor_name, os.getcwd(), condor_name
)
      )
			jdf.close()
			os.system( "condor_submit {}".format( jdf_name ) )
	os.chdir( ".." )
  
def combine_years( tags, variables ):
  combinations = []

  for tag in tags:
    for variable in avariables:
      combinations.append( {
        "variable": variable,
        "tag": tags
      } )
      
  os.chdir( "combine" )
  for combination in combinations:
    combine_tag = "{}_{}".format( combination[ "tag" ], combination[ "variable" ] )
    condor_name = "condor_step5_{}".format( combine_tag )
    shell_name = "condor_config/{}.sh".format( condor_name )
    shell = open( shell_name, "w" )
    shell.write(
"#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh \n\
cd {} \n\
eval `scramv1 runtime -sh` \n\
cd {} \n\
combine_datacrads.py R17=limits_UL17_{}/cmb/combined.txt.cmb R18=limits_UL18_{}/cmb/combined.txt.cmb &> results/{}.txt \n\
text2workspace.py results/{}.txt -o results/{}.root \n\
combine -M Significance results/{}.root -t - --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> results/significance_{}.txt \n\
combine -M AsymptoticLimits results/{}.root --run=blind --cminDefaultMinimizerStrategy 0 &> results/limits_{}.txt".format(
  cmsswbase, os.getcwd(),
  combine_tag, combine_tag, combine_tag, combine_tag, combine_tag, combine_tag, combined_tag, combine_tag
)
    )
    shell.close()
    jdf_name = "condor_config/{}.job".format( condor_name )
    jdf = open( jdf_name, "w" )
    jdf.write(
"""universe = vanilla \n\
Executable = {}/{} \n\
Should_Transfer_Files = YES \n\
WhenToTransferOutput = ON_EXIT \n\
JobBatchName = SLA_step5 \n\
request_memory = 3072 \n\
Output = {}/condor_log/{}.out \n\
Error = {}/condor_log/{}.err \n\
Log = {}/condor_log/{}.log \n\
Notification = Error \n\
Arguments = \n\
Queue 1""".format(
  os.getcwd(), shell_name,
  os.getcwd(), condor_name, os.getcwd(), condor_name, os.getcwd(), condor_name
)
    )
    jdf.close()
    os.system( "condor_submit {}".format( jdf_name ) )
    os.chdir( ".." )

if args.step == 1: produce_templates()
elif args.step == 2: run_templates()
  
elif args.step == 3:
  
elif args.step == 4:
  
elif args.step == 5:
  
else:
  print( "[ERR] Invalid step option used" )
  
  
  
