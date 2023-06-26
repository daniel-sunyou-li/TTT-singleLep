import os, sys
from datetime import datetime
from argparse import ArgumentParser
from json import loads as load_json
from json import dumps as write_json
from math import log

from skopt.space import Real, Integer, Categorical
from skopt.utils import use_named_args
from skopt import gp_minimize

parser = ArgumentParser()
parser.add_argument(      "dataset", help = "The dataset folder to use variable importance results from.")
parser.add_argument("-o", "--sort-order", default = "significance", help = "Which attribute to sort variables by. Choose from (significance, freq, sum, mean, rms, or specify a filepath).")
parser.add_argument(      "--sort-increasing", action = "store_true", help = "Sort in increasing instead of decreasing order")
parser.add_argument("-n", "--numvars", default = "all", help = "How many variables, from the top of the sorted order, to use.")
parser.add_argument("-r", "--ratio", default = "1", help = "Ratio of background to signal training samples. Default = 1, -1 to use all background" )
parser.add_argument("-t", "--tag", default = "", help = "Tag to add to the results directory name (i.e. DNN_[N1]to[N2]_[TAG]") 
parser.add_argument("--override", action = "store_true", help = "Override existing ROOT file containing events for training" )
parser.add_argument("--Run2", action = "store_true", help = "Run on the full Run 2 dataset for training" )
args = parser.parse_args()

sys.argv = []

from correlation import reweight_importances
import config
import mltools

# Load dataset
datafile_path = None
if os.path.exists( args.dataset ):
  for f in os.listdir( args.dataset ):
    if f.startswith( "VariableImportanceResults" ):
      datafile_path = os.path.join( args.dataset, f )
      break
      
if datafile_path == None:
  raise IOError( "[ERR] {} is not a valid dataset!".format( args.dataset ) )
  
print( ">> Loading variable importance data from {}.".format( datafile_path ) )
# Read the data file
selection = ""
var_data = {}
years = []
with open( datafile_path, "r" ) as f:
  # Scroll to variable entries
  line = f.readline()
  if "Year" in line: 
    years_ = line.split(":")[-1][:-1].split(",")
    for year in years_:
      years.append( year )
    print( ">> Including years: {}".format( year ) )
  while not "Normalization" in line:
    line = f.readline()
    if "Selection" in line:
      selection = line.split(":")[-1][:-1]
      print( ">> Event selection: {}".format( selection ) )
    if line == "":
      raise IOError( ">> End of File Reached, no data found." )
  # Data reached.
  # Read headers
  headers = [ h.strip().rstrip().lower().replace(".", "") for h in f.readline().rstrip().split("/") ]
  print( ">> Found data columns: {}".format(", ".join(headers)) )
  for h in headers:
    var_data[h] = []
  # Read data
  line = f.readline().rstrip()
  while line != "":
    content = [c.strip().rstrip() for c in line.split("/")]
    content[0] = content[0].rstrip(".")
    for i, h in enumerate(headers):
      if i == 1:
        var_data[h].append(content[i])
      elif "inf" in content[i]:
        print( "[WARN] Replaced infinite value with 0!" )
        var_data[h].append( 0 )
      else:
        var_data[h].append( float( content[i] ) if "." in content[i] else int( content[i] ) )
    line = f.readline().rstrip()

# Determine variable sort order
var_order = []
if os.path.exists(args.sort_order):
  print( ">> Reading variable sort order from {}.".format( args.sort_order ) )
  with open(args.sort_order, "r") as f:
    for line in f.readlines():
      if line != "":
        var_name = line.rstrip().strip()
        if not var_name in var_data[ "variable name" ]:
          print( "[WARN] Data for variable {} not found in dataset. Skipping.".format( var_name ) )
        else:
          var_order.append( var_name )
    print( ">> Found {} variables.".format( len( var_order ) ) )
else:
  sort_order = args.sort_order.lower()
  if sort_order not in var_data:
    print( ">> Invalid sort option: {}. Using \"significance\".".format( sort_order ) )
    sort_order = "significance"
  else:
    print( ">> Sorting {} variables by {}.".format( len( var_data[ "variable name" ] ), sort_order ) )
  sorted_vars = sorted( [ (n, i) for i, n in enumerate( var_data[ "variable name" ] ) ],
                       key=lambda p: var_data[ sort_order ][ p[1] ] )
  if not args.sort_increasing:
    sorted_vars = reversed( sorted_vars )
  var_order = [ v[0] for v in sorted_vars ]
  
# Determine the variables to use
variables = None
subDirName = None
if args.numvars == "ALL":
  variables = var_order
  subDirName = "1to{}".format( len(variables) )
else:
  if ":" in args.numvars:
    indices = [ int(x) for x in args.numvars.split(":") ]
    variables = var_order[ ( indices[0] - 1 ):indices[1] ]
    subDirName = "{}to{}".format( indices[0], indices[1] )
  else:
    variables = var_order[:int(args.numvars)]
    subDirName = "1to{}".format( len(variables) )
if args.tag != "":
  subDirName += "_{}".format( args.tag )
print( ">> Creating hyper parameter optimization sub-directory: {}".format( args.dataset + subDirName + "/" ) )
os.system( "mkdir ./{}/".format( os.path.join( args.dataset, subDirName ) ) ) 
print( ">> Variables used in optimization:\n - {}".format( "\n - ".join( variables ) ) )

signal_files = []
background_files = []
if args.Run2: years = [ "16APV", "16", "17", "18" ]
for year in years:
  tree_folder = config.step2DirXRD[ year ] + "nominal/"
  for sig_ in config.sig_training[ year ]:
    signal_files.append( os.path.join( tree_folder, sig_ ) )
  for bkg_ in config.bkg_training[ year ]:
    if year == "18" and "TTTT" in bkg_: bkg_ = bkg_.replace( "_hadd", "_1_hadd" )
    background_files.append( os.path.join( tree_folder, bkg_ ) )

# Calculate re-weighted significance
LMS, QMS = reweight_importances( 
  year, variables, [ var_data[ "significance" ][ var_data[ "variable name" ].index(v) ] for v in variables ], selection
)
LMI, QMI = reweight_importances( 
  year, variables, [ var_data[ "mean" ][ var_data[ "variable name" ].index(v) ] for v in variables ], selection
)
LSI = sum( [ var_data[ "mean" ][ var_data[ "variable name" ].index(v) ] for v in variables ] )
LSS = sum( [ var_data[ "significance" ][ var_data[ "variable name" ].index(v) ] for v in variables ] )

print( "[INFO] Cumulative Importance Metrics:" )
print( "  + LSI: {:.4f}".format( LSI ) )
print( "  + LMI: {:.4f}".format( sum(LMI) ) )
print( "  + QMI: {:.4f}".format( sum(QMI) ) )
print( "  + LSS: {:.4f}".format( LSS ) )
print( "  + LMS: {:.4f}".format( sum(LMS) ) )
print( "  + QMS: {:.4f}".format( sum(QMS) ) )

# Set static parameters and hyper parameter ranges
timestamp = datetime.now()
CONFIG = {
  "STATIC": [
    "YEAR",
    "BACKGROUND FILES",
    "SIGNAL FILES",
    "RATIO",
    "EPOCHS",
    "PATIENCE",
    "MODEL NAME",
    "TAG",
    "LOG FILE",
    "HPO CALLS",
    "HPO STARTS",
    "EVENT WEIGHT",
    "EVENT CUT",
    "START INDEX",
    "END INDEX",
    "VARIABLES",
    "LMS",
    "QMS",
    "LSI",
    "LSS",
    "LMI",
    "QMI"
  ],
    "EPOCHS": config.params[ "HPO" ][ "EPOCHS" ],
    "PATIENCE": config.params[ "HPO" ][ "PATIENCE" ],
    "MODEL NAME": os.path.join( args.dataset, subDirName, "hpo_model.h5" ),
    "HPO CALLS": config.params[ "HPO" ][ "CALLS" ],
    "HPO STARTS": config.params[ "HPO" ][ "STARTS" ],
    "START INDEX": subDirName.split( "to" )[0],
    "END INDEX": subDirName.split( "to" )[1].split( "_" )[0]
}

tag = "{}to{}".format( subDirName.split( "to" )[0], subDirName.split( "to" )[1] )
CONFIG.update({
  "YEAR":",".join(years),
  "BACKGROUND FILES": background_files, 
  "SIGNAL FILES": signal_files,
  "RATIO": args.ratio,
  "TAG": tag,
  "LOG FILE": os.path.join(args.dataset, subDirName, "hpo_log_" + tag + ".txt"),
  "EVENT WEIGHT": config.weightStr,
  "VARIABLES": variables,
  "LMS": sum(LMS),
  "QMS": sum(QMS),
  "LMI": sum(LMI),
  "QMI": sum(QMI),
  "LSI": LSI,
  "LSS": LSS,
  "EVENT CUT": selection
} )

# Save used parameters to file
config_file = os.path.join( args.dataset, subDirName, "config_" + CONFIG["TAG"] + ".json" )
with open( config_file, "w" ) as f:
  f.write( write_json( CONFIG, indent=2 ) )
print( "[OK] Configuration file saved." )

# Start the logfile
logfile = open( CONFIG["LOG FILE"], "w" )
headers = " ".join( [ param_ for param_ in config.params[ "HPO" ][ "OPT SPACE" ] ] )
logfile.write( headers + " AUC\n" )

# Determine optimization space
opt_space = [] # hyper parameter ranges input for scikit-optimize
opt_order = {} # bookkeeping for order in which the hyper parameters are input, necessary to retrieve optimized value from X
i = 0
for param in config.params[ "HPO" ][ "OPT SPACE" ]:
  if len( config.params[ "HPO" ][ "OPT SPACE" ][ param ][ "VALUE" ] ) < 2: continue
  if param not in CONFIG[ "STATIC" ]:
    opt_order[ param ] = i
    i += 1
  if config.params[ "HPO" ][ "OPT SPACE" ][ param ][ "TYPE" ] == "CATEGORICAL":
    opt_space.append( Categorical( config.params[ "HPO" ][ "OPT SPACE" ][ param ][ "VALUE" ], name = param ) )
  elif config.params[ "HPO" ][ "OPT SPACE" ][ param ][ "TYPE" ] == "INTEGER":
    opt_space.append( Integer( *config.params[ "HPO" ][ "OPT SPACE" ][ param ][ "VALUE" ], name = param ) )
  elif config.params[ "HPO" ][ "OPT SPACE" ][ param ][ "TYPE" ] == "REAL LINEAR":
    opt_space.append( Real( *config.params[ "HPO" ][ "OPT SPACE" ][ param ][ "VALUE" ], name = param ) )
  elif config.params[ "HPO" ][ "OPT SPACE" ][ param ][ "TYPE" ] == "REAL LOG":
    opt_space.append( Real( *config.params[ "HPO" ][ "OPT SPACE" ][ param ][ "VALUE" ], name = param, prior = "log-uniform", base = 10 ) )
  else:
    quit( "[ERR] Invalid hyper parameter optimization category '{}' for parameter '{}'. Options are: CATEGORICAL, INTEGER, REAL LINEAR, REAL LOG.".format( config.params[ "HPO" ][ "OPT SPACE" ][ param ][ "TYPE" ], param ) )
    
# Objective function

# Persist cut events to speed up process
cut_events = None

@use_named_args(opt_space)
def objective(**X):
  global cut_events
    
  print(">> Configuration:\n{}\n".format(X))
  for param in config.params[ "HPO" ][ "OPT SPACE" ]:
    if len( config.params[ "HPO" ][ "OPT SPACE" ][ param ][ "VALUE" ] ) == 1:
      X[param] = config.params[ "HPO" ][ "OPT SPACE" ][ param ][ "VALUE" ][0]
  if not "VARIABLES" in X: X["VARIABLES"] = CONFIG["VARIABLES"]
  if not "PATIENCE" in X: X["PATIENCE"] = CONFIG["PATIENCE"]
  if not "EPOCHS" in X: X["EPOCHS"] = CONFIG["EPOCHS"]
  model = mltools.HyperParameterModel(
    X, 
    signal_files, background_files, var_order, 
    float(args.ratio), selection, CONFIG["MODEL NAME"],
  )

  save_path = os.path.join( args.dataset, "events.root" )
  if cut_events is None:
    if not os.path.exists(save_path):
      print( "[START] Formatting events passing filter into ROOT file." )
      model.apply_cut()
      model.save_cut_events( save_path, weighted = config.params[ "WEIGHT XSEC" ] )
      print( "[DONE]" )
      model.load_cut_events( save_path, weighted = config.params[ "WEIGHT XSEC" ], override = False )
    else:
      print( "[START] Loading events from ROOT file {}/events.root".format( args.dataset ) )
      model.load_cut_events( save_path, weighted = config.params[ "WEIGHT XSEC" ], override = args.override )
      print( "[DONE]" )
    cut_events = model.cut_events.copy()
  else:
    model.cut_events = cut_events.copy()
    
  model.build_model()
  model.train_model( variables )
    
  print( "[INFO] Obtained validation AUC score: {:.4f}".format( model.auc_test ) )
  row = " ".join( [ "{:<" + str( len( param_ ) ) + "}" for param_ in config.params[ "HPO" ][ "OPT SPACE" ] if len( config.params[ "HPO" ][ "OPT SPACE" ][ param_ ][ "VALUE" ] ) > 1 ] )
  logfile.write( row.format( *[ X[param_] for param_ in config.params[ "HPO" ][ "OPT SPACE" ] ] ) + " {}\n".format( round( model.auc_test, 4 ) ) )

  opt_metric = log( 1. - model.auc_test)
  print( "  + Optimization Metric: log( 1 - AUC ) = {:.4f}".format( opt_metric ) )
  return opt_metric

# Perform the optimization
start_time = datetime.now()

res_gp = gp_minimize(
  func = objective,
  dimensions = opt_space,
  n_calls = CONFIG["HPO CALLS"],
  n_random_starts = CONFIG["HPO STARTS"],
  verbose = True
)

logfile.close()

# Report results
print(">> Writing optimized parameter log to: optimized_params_" + CONFIG["TAG"] + ".txt and .json")
with open(os.path.join(args.dataset, subDirName, "optimized_params_" + CONFIG["TAG"] + ".txt"), "w") as f:
  f.write("CONFIG FILE: {}\n".format( config_file ) )
  f.write("HPO:\n")
  for param_ in config.params[ "HPO" ][ "OPT SPACE" ]:
    if len( config.params[ "HPO" ][ "OPT SPACE" ][ param_ ][ "VALUE" ] ) > 1:
      f.write( "{}:{}\n".format( param_, res_gp.x[opt_order[param_]] ) )
    else:
      f.write( "{}:{}\n".format( param_, config.params[ "HPO" ][ "OPT SPACE" ][ param_ ][ "VALUE" ][0] ) )
with open( os.path.join( args.dataset, subDirName, "optimized_params_" + CONFIG["TAG"] + ".json"), "w") as f:
  json_dict = dict( [ ( key, res_gp.x[val] ) for key, val in opt_order.iteritems() ] )
  for param_ in config.params[ "HPO" ][ "OPT SPACE" ]:
    if len( config.params[ "HPO" ][ "OPT SPACE" ][ param_ ][ "VALUE" ] ) == 1:
      json_dict.update( { param_: config.params[ "HPO" ][ "OPT SPACE" ][ param_ ][ "VALUE" ][0] } )
  f.write( write_json( json_dict, indent = 2 ) )
print( "[DONE] Finished hyper parameter optimization in: {}".format( datetime.now() - start_time ) )
