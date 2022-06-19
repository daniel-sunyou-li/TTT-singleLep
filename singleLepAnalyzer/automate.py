import os,sys, time
import config
from argparse import ArgumentParser

cmsswbase = os.path.join( os.getcwd(), ".." )

parser = ArgumentParser()
parser.add_argument( "-s", "--step", required = True, help = "Options: 1-5" )
parser.add_argument( "-y", "--years", nargs = "+", required = True, help = "Options: 16APV, 16, 17, 18" )
parser.add_argument( "-t", "--tags", nargs = "+", required = True )
parser.add_argument( "-v", "--variables", nargs = "+", required = True )
parser.add_argument( "-r", "--region", default = "SR" )
parser.add_argument( "--verbose", action = "store_true" )
args = parser.parse_args()

if args.region not in list( config.region_prefix.keys() ): quit( "[ERR] Invalid option used for -r (--region). Quitting." )
verbose = "--verbose" if args.verbose else ""

def get_trainings( tags, years, variables ):
  trainings = []
  for tag in tags:
    for year in years:
      trainings.append( {
        "year": year,
        "variable": variables,
        "tag": tag,
        "path": config.inputDir[ year ]
      } )
  return trainings
    
  
def produce_templates():
  trainings = get_trainings( args.tags, args.years, args.variables )
  os.chdir( "makeTemplates" )
  for training in trainings:
    for variable in training[ "variable" ]:
      command = "python condor_templates.py -y {} -v {} -p {} -r {}".format(
        training[ "year" ],
        variable,
        training[ "tag" ],
        args.region
      )
      os.system( command ) 
      time.sleep( 1 )
  os.chdir( ".." )
                
def run_templates():
  trainings = get_trainings( args.tags, args.years, args.variables )
  os.chdir( "makeTemplates" )
  for training in trainings:
    for variable in training[ "variable" ]:
      if not os.path.exists( "condor_log" ): os.system( "mkdir -vp condor_log" )
      step2_name = "condor_step2_UL{}_{}_{}_{}".format( training[ "year" ], training[ "tag" ], variable, args.region )
      shell_name = "condor_log/{}.sh".format( step2_name )
      shell = open( shell_name, "w" )
      shell.write(
"#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd {} \n\
eval `scramv1 runtime -sh`\n\
cd {} \n\
python templates.py -y {} -t {} -v {} -r {} --verbose \n".format( cmsswbase, os.getcwd(), training[ "year" ], training[ "tag" ], variable, args.region )
      )
      shell.close()
      jdf_name = "condor_log/{}.job".format( step2_name )
      jdf = open( jdf_name, "w" )
      jdf.write(
"universe = vanilla \n\
Executable = {}\n\
Should_Transfer_Files = YES\n\
WhenToTransferOutput = ON_EXIT\n\
JobBatchName = SLA_step2_{}\n\
request_memory = 1024\n\
Output = condor_log/{}.out\n\
Error = condor_log/{}.err\n\
Log = condor_log/{}.log\n\
Notification = Error\n\
Arguments = \n\
Queue 1\n".format( shell_name, variable, step2_name, step2_name, step2_name ) 
      )
      jdf.close()
      os.system( "condor_submit {}".format( jdf_name ) )
      time.sleep( 1 )
    os.chdir( "../" )
  
def produce_binned_templates():
  trainings = get_trainings( args.tags, args.years, args.variables )
  os.chdir( "makeTemplates" )
  if not os.path.exists( "condor_config" ): os.system( "mkdir condor_config" )
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
python modify_binning.py -y {} -v {} -t {} -r {} \n\
python plot_templates.py -y {} -v {} -t {} -r {} --templates \n\ ".format( 
  cmsswbase, os.getcwd(), 
  train[ "year" ], variable, train[ "tag" ], args.region,
  train[ "year" ], variable, train[ "tag" ], args.region
)
      )
      shell.close()
      jdf_name = "condor_config/{}.job".format( condor_name ) 
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
      log_name = "log_{}_{}_{}".format( variable, training[ "year" ], training[ "tag" ] )
      shell_name = "{}/{}.sh".format( log_name, condor_name )
      if not os.path.exists( log_name ): os.system( "mkdir -vp {}".format( log_name ) )
      shell = open( shell_name, "w" )
      shell.write(
"#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd {} \n\
eval `scramv1 runtime -sh`\n\
cd {} \n\
python create_datacard.py -y {} -v {} -t {} -r {} --shapeSyst --normSyst  {} \n\
cd limits_UL{}_{}_{}\n\
combine -M Significance cmb/workspace.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 > significance.txt\n\
combine -M AsymptoticLimits cmb/workspace.root --run=blind --cminDefaultMinimizerStrategy 0> limits.txt\n\
cd ..\n".format(
  cmsswbase, os.getcwd(),
  training[ "year" ], variable, training[ "tag" ], args.region, verbose,
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
Output = {}.out \n\
Error = {}.err \n\
Log = {}.log \n\
Notification = Error \n\
Arguments = \n\
Queue 1""".format(
  os.getcwd(), shell_name,
  os.path.join( os.getcwd(), log_name, condor_name ), 
  os.path.join( os.getcwd(), log_name, condor_name ), 
  os.path.join( os.getcwd(), log_name, condor_name )
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
combineCards.py UL16APV=limits_UL16APV_{}/cmb/combined.txt.cmb UL16=limits_UL16_{}/cmb/combined.txt.cmb UL17=limits_UL17_{}/cmb/combined.txt.cmb  UL18=limits_UL18_{}/cmb/combined.txt.cmb > Results/{}.txt \n\
text2workspace.py results/{}.txt -o results/{}.root \n\
combine -M Significance Results/{}.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 > Results/significance_{}.txt \n\
combine -M AsymptoticLimits Results/{}.root --run=blind --cminDefaultMinimizerStrategy 0 > Results/limits_{}.txt".format(
  cmsswbase, os.getcwd(),
  combine_tag, combine_tag, combine_tag, combine_tag, combine_tag, combine_tag, combined_tag, combine_tag, combine_tag, combine_tag
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

if args.step == "1": produce_templates()
elif args.step == "2": run_templates()
elif args.step == "3": produce_binned_templates()
elif args.step == "4": run_combine()
elif args.step == "5": combine_years()
else:
  print( "[ERR] Invalid step option used" )
  
  
  
