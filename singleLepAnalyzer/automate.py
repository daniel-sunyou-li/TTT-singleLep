import os,sys, time
import config
from argparse import ArgumentParser

cmsswbase = os.path.join( os.getcwd(), ".." )

parser = ArgumentParser()
parser.add_argument( "-s", "--step", required = True, help = "Options: 1-5" )
parser.add_argument( "-y", "--years", nargs = "+",  help = "Options: 16APV, 16, 17, 18" )
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
    
def condor_template( logName, nameCondor ):
  jobName = os.path.join( logName, nameCondor + ".job" )
  jobFile = open( jobName, "w" )
  jobFile.write(
"""universe = vanilla \n\
Executable = {0}.sh \n\
Should_Transfer_Files = YES \n\
WhenToTransferOutput = ON_EXIT \n\
JobBatchName = {1} \n\
request_memory = 3072 \n\
Output = {0}.out \n\
Error = {0}.err \n\
Log = {0}.log \n\
Notification = Error \n\
Arguments = \n\
Queue 1""".format(
  os.path.join( os.getcwd(), logName, nameCondor ),
  nameCondor
)
  )
  jobFile.close()
  os.system( "condor_submit {}".format( jobName ) )
  
def make_templates():
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
                
def format_templates():
  trainings = get_trainings( args.tags, args.years, args.variables )
  doABCDnn = "--abcdnn" if config.options[ "GENERAL" ][ "ABCDNN" ] else ""
  for training in trainings:
    for variable in training[ "variable" ]:
      os.chdir( "makeTemplates" )
      nameLog = "log_UL{}_{}_{}_{}".format( training[ "year" ], variable, args.region, training[ "tag" ] )
      nameCondor = "SLA_step2_{}_{}_{}_{}".format( training[ "year" ], variable, args.region, training[ "tag" ] )
      if not os.path.exists( nameLog ): os.system( "mkdir -vp {}".format( nameLog ) )
      shell = open( "{}/{}.sh".format( nameLog, nameCondor ), "w" )
      shell.write(
"#!/bin/bash \n\
source /cvmfs/cms.cern.ch/cmsset_default.sh \n\
cd {0} \n\
eval `scramv1 runtime -sh` \n\
cd {1} \n\
python templates.py -y {2} -t {3} -v {4} -r {5} --verbose \n\
python modify_binning.py -y {2} -t {3} -v {4} -r {5} {6}".format( 
  cmsswbase, os.getcwd(), training[ "year" ], training[ "tag" ], variable, args.region, doABCDnn )
      )
      shell.close()
      condor_template( nameLog, nameCondor )
      os.chdir( "../" )
  
def plot_templates():
  trainings = get_trainings( args.tags, args.years, args.variables )
  for train in trainings:
    for variable in train[ "variable" ]:
      os.chdir( "makeTemplates" )
      nameLog = "log_UL{}_{}_{}_{}".format( training[ "year" ], variable, args.region, training[ "tag" ] )
      nameCondor = "SLA_step3_{}_{}_{}_{}".format( training[ "year" ], variable, args.region, training[ "tag" ] )
      shell = open( "{}/{}.sh".format( nameLog, nameCondor ), "w" )
      shell.write(
"#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd {0} \n\
eval `scramv1 runtime -sh`\n\
cd {1} \n\
python plot_templates.py -y {2} -v {3} -t {4} -r {5} --templates \n\ ".format( 
  cmsswbase, os.getcwd(), 
  train[ "year" ], variable, train[ "tag" ], args.region, doABCDNN,
)
      )
      shell.close()
      condor_template( nameLog, nameCondor )
      os.chdir( ".." )
 
def run_combine():
  trainings = get_trainings( args.tags, args.years, args.variables )
  tagSmooth = "" if not config.options[ "COMBINE" ][ "SMOOTH" ] else config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper()
  tagABCDnn = "" if not config.options[ "COMBINE" ][ "ABCDNN" ] else "ABCDNN"
  for training in trainings:
    for variable in training[ "variable" ]:
      os.chdir( "combine" )
      nameLog = "log_UL{}_{}_{}_{}".format( training[ "year" ], variable, args.region, training[ "tag" ] )
      nameCondor = "SLA_step4_{}_{}_{}_{}".format( training[ "year" ], variable, args.region, training[ "tag" ] )
      if not os.path.exists( nameLog ): os.system( "mkdir {}".format( nameLog ) )
      shell = open( os.path.join( nameLog, nameCondor + ".sh" ), "w" )
      shell.write(
"#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd {0} \n\
eval `scramv1 runtime -sh`\n\
cd {1} \n\
python create_datacard.py -y {2} -v {3} -t {4} -r {5} --normSyst --shapeSyst {6} \n\
python create_datacard.py -y {2} -v {3} -t {4} -r {5} {6} \n\
cd limits_UL{2}_{3}_{5}_{4}_{7}{8}\n\
combineTool.py -M T2W -i cmb/ -o workspace.root --parallel 4\n\
combine -M Significance cmb/workspace.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 > significance.txt\n\
combine -M AsymptoticLimits cmb/workspace.root --run=blind --cminDefaultMinimizerStrategy 0 > limits.txt\n\
cd ..\n\
cd limits_UL{2}_{3}_{5}_{4}_{7}noShapenoNorm{8}\n\
combineTool.py -M T2W -i cmb/ -o workspace.root --parallel 4 \n\
combine -M Significance cmb/workspace.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 > significance.txt\n\
combine -M AsymptoticLimits cmb/workspace.root --run=blind --cminDefaultMinimizerStrategy 0 > limits.txt\n\
cd ..\n".format(
  cmsswbase, os.getcwd(), training[ "year" ], variable, training[ "tag" ], args.region, verbose, tagABCDnn, tagSmooth
)
      )
      shell.close()
      condor_template( nameLog, nameCondor )
      os.chdir( ".." )
  
def combine_years():
  tagSmooth = "" if not config.options[ "COMBINE" ][ "SMOOTH" ] else config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper()
  tagABCDnn = "" if not config.options[ "COMBINE" ][ "ABCDNN" ] else "ABCDNN" 
  for variable in args.variables:
    for tag in args.tags:
      os.chdir( "combine" )
      nameLog = "log_{}_{}_{}".format( variable, args.region, training[ "tag" ] )
      nameCondor = "SLA_step5_{}_{}_{}_{}".format( variable, args.region, tag, tagABCDnn + tagSmooth )
      if not os.path.exists( nameLog ): os.system( "mkdir -vp {}".format( nameLog ) )
      tagAllSyst = "{}_{}_{}_{}{}".format( variable, args.region, tag, tagABCDnn, tagSmooth )
      tagNoSyst = "{}_{}_{}_{}noShapenoNorm{}".format( variable, args.region, tag, tagABCDnn, tagSmooth )
      shell = open( "{}/{}.sh".format( nameLog, nameCondor ), "w" )
      shell.write(
"#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh \n\
cd {0} \n\
eval `scramv1 runtime -sh` \n\
cd {1} \n\
mkdir -vp Results/{2}/ \n\
combineCards.py UL16APV=limits_UL16APV_{2}/cmb/combined.txt.cmb UL16=limits_UL16_{2}/cmb/combined.txt.cmb UL17=limits_UL17_{2}/cmb/combined.txt.cmb  UL18=limits_UL18_{2}/cmb/combined.txt.cmb > Results/{2}/workspace.txt \n\
text2workspace.py Results/{2}/workspace.txt -o Results/{2}/workspace.root \n\
combine -M Significance Results/{2}/workspace.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 > Results/{2}/significance.txt \n\
combine -M AsymptoticLimits Results/{2}/workspace.root --run=blind --cminDefaultMinimizerStrategy 0 > Results/{2}/limits.txt\n\
mkdir -vp Results/{3}/ \n\
combineCards.py UL16APV=limits_UL16APV_{3}/cmb/combined.txt.cmb UL16=limits_UL16_{3}/cmb/combined.txt.cmb UL17=limits_UL17_{3}/cmb/combined.txt.cmb  UL18=limits_UL18_{3}/cmb/combined.txt.cmb > Results/{3}/workspace.txt \n\
text2workspace.py Results/{3}/workspace.txt -o Results/{3}/workspace.root \n\
combine -M Significance Results/{3}/workspace.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 > Results/{3}/significance.txt \n\
combine -M AsymptoticLimits Results/{3}/workspace.root --run=blind --cminDefaultMinimizerStrategy 0 > Results/{3}/limits.txt".format(
  cmsswbase, os.getcwd(), tagAllSyst, tagNoSyst
)
    )
      shell.close()
      condor_template( nameLog, nameCondor )
      os.chdir( ".." )

def impact_plots_era():
  trainings = get_trainings( args.tags, args.years, args.variables )
  tagSmooth = "" if not config.options[ "COMBINE" ][ "SMOOTH" ] else config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper()
  tagABCDnn = "" if not config.options[ "COMBINE" ][ "ABCDNN" ] else "ABCDNN"
  postfix = tagABCDnn + tagSmooth
  for training in trainings:
    for variable in training[ "variable" ]:
      os.chdir( "combine" )
      nameCondor = "SLA_step6_{}_{}_{}_{}".format( training[ "year" ], training[ "tag" ], variable, postfix )
      nameLog = "log_UL{}_{}_{}_{}".format( training[ "year" ], variable, args.region, training[ "tag" ] )
      if not os.path.exists( nameLog ): os.system( "mkdir -vp {}".format( nameLog ) )
      shell = open( "{}/{}.sh".format( nameLog, nameCondor ), "w" )
      shell.write(
"#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd {0} \n\
eval `scramv1 runtime -sh` \n\
cd {1} \n\
cd limits_UL{2}_{3}_{4}_{5}_{6}/cmb/ \n\
combineTool.py -M Impacts -d workspace.root -m 125 --doInitialFit --robustFit 1 -t -1 --expectSignal 1 --rMin -100 --rMax 100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerType Minuit \n\
combineTool.py -M Impacts -d workspace.root -m 125 --doFits --robustFit 1 -t -1 --expectSignal 1 --rMin -100 --rMax 100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --exclude rgx{7} --cminDefaultMinimizerType Minuit \n\
combineTool.py -M Impacts -d workspace.root -m 125 -o impacts_UL{2}_{4}_{3}_{5}_{6}.json --exclude rgx{7} \n\
plotImpacts.py -i impacts_UL{2}_{4}_{3}_{5}_{6}.json -o impacts_UL{2}_{4}_{3}_{5}_{6} \n\
cd .. \n".format(
  cmsswbase, os.getcwd(), training[ "year" ], variable, args.region, training[ "tag" ], postfix, "\{prop_bin.*\}"
)
      )
      shell.close()
      condor_template( nameLog, nameCondor )
      os.chdir( ".." )
  

def uncertainty_breakdown():
  return


if args.step == "1": make_templates()
elif args.step == "2": format_templates()
elif args.step == "3": plot_templates()
elif args.step == "4": run_combine()
elif args.step == "5": combine_years()
elif args.step == "6": impact_plots_era()
else:
  print( "[ERR] Invalid step option used" ) 
