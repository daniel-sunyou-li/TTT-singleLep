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
parser.add_argument(      "dataset", help="The dataset folder to use variable importance results from.")
parser.add_argument("-o", "--sort-order", default="significance", help="Which attribute to sort variables by. Choose from (significance, freq, sum, mean, rms, or specify a filepath).")
parser.add_argument(      "--sort-increasing", action="store_true", help="Sort in increasing instead of decreasing order")
parser.add_argument("-n", "--numvars", default="all", help="How many variables, from the top of the sorted order, to use.")
parser.add_argument("-p", "--parameters", default=None, help="Specify a JSON folder with static and hyper parameters.")
args = parser.parse_args()

from correlation import reweight_importances
import config
sys.argv = []
import mltools

tree_folder = config.step2DirLPC[ year ] + "nominal/"
signal_files = [ os.path.join( tree_folder, sig ) for sig in ( config.sig_training[ year ] ) ]
background_files = [ os.path.join( tree_folder, bkg ) for bkg in ( config.bkg_training[ year ] ) ]

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
cut_variables = [ "AK4HT", "NJETS", "NBJETS", "MET", "LEPPT", "MT", "MINDR", "JET0PT", "JET1PT", "JET2PT" ]
cut = { variable: 0 for variable in cut_variables }
var_data = {}
with open( datafile_path, "r" ) as f:
  # Scroll to variable entries
  if "Year" in line: 
    year = line.split(":")[-1] 
    print( ">> Running year: {}".format( year ) )
  line = f.readline()
  for variable in cut_variables:
    if variable in line:
      cut[ variable ] = float( line.split(":")[-1] )
  while not "Normalization" in line:
    line = f.readline()
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
if args.numvars == "all":
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
print( ">> Creating hyper parameter optimization sub-directory: {}".format( args.dataset + subDirName + "/" ) )
os.system( "mkdir ./{}/".format( os.path.join( args.dataset, subDirName ) ) ) 
print( ">> Variables used in optimization:\n - {}".format( "\n - ".join( variables ) ) )

# Calculate re-weighted significance
LMS, QMS = reweight_importances( year, variables, [ var_data[ "significance" ][ var_data[ "variable name" ].index(v) ] for v in variables ], cuts["NJETS"], cuts["NBJETS"], cuts["AK4HT"] )
LMI, QMI = reweight_importances( year, variables, [ var_data[ "mean" ][ var_data[ "variable name" ].index(v) ] for v in variables ], cuts["NJETS"], cuts["NBJETS"], cuts["AK4HT"] )
LSI = sum( [ var_data[ "mean" ][ var_data[ "variable name" ].index(v) ] for v in variables ] )
LSS = sum( [ var_data[ "significance" ][ var_data[ "variable name" ].index(v) ] for v in variables ] )

print( ">> Cumulative Importance Metrics:" )
print( "   o LSI: {:.4f}".format( LSI ) )
print( "   o LMI: {:.4f}".format( sum(LMI) ) )
print( "   o QMI: {:.4f}".format( sum(QMI) ) )
print( "   o LSS: {:.4f}".format( LSS ) )
print( "   o LMS: {:.4f}".format( sum(LMS) ) )
print( "   o QMS: {:.4f}".format( sum(QMS) ) )

# Determine static and hyper parameter
timestamp = datetime.now()
CONFIG = {
  "static": [
    "year",
    "static",
    "epochs",
    "patience",
    "model_name",
    "tag",
    "log_file",
    "n_calls",
    "n_starts",
    "njets",
    "nbjets",
    "ak4ht",
    "weight_string",
    "cut_string",
    "start_index",
    "end_index",
    "variables",
    "LMS",
    "QMS",
    "LSI",
    "LSS",
    "LMI",
    "QMI"
  ],
    "epochs": 30,
    "patience": 5,
    "model_name": os.path.join( args.dataset, subDirName, "hpo_model.h5" ),

    "hidden_layers": [ 1, 3 ],
    "initial_nodes": [ len(variables), len(variables) * 10 ],
    "node_pattern": [ "static", "dynamic" ],
    "batch_power": [ 8, 11 ],
    "learning_rate": [ 1e-5, 1e-4, 1e-3, 1e-2],
    "regulator": [ "dropout", "none" ],
    "activation_function": [ "relu", "softplus", "elu" ],

    "n_calls": 20,
    "n_starts": 15,
    "start_index": subDirName.split( "to" )[0],
    "end_index": subDirName.split( "to" )[1]
}

# Update parameters given file
if args.parameters != None and os.path.exists(args.parameters):
  print(">> Loading updated parameters from {}.".format(args.parameters))
  with open(args.parameters, "r") as f:
    u_params = load_json(f.read())
    CONFIG.update(u_params)
    
tag = "{}j_{}to{}".format( cuts["NJETS"], subDirName.split( "to" )[0], subDirName.split( "to" )[1] )
CONFIG.update({
  "year":year,
  "tag": tag,
  "log_file": os.path.join(args.dataset, subDirName, "hpo_log_" + tag + ".txt"),
  "weight_string": config.weightStr,
  "cut_string": config.cutStr,
  "variables": variables,
  "LMS": sum(LMS),
  "QMS": sum(QMS),
  "LMI": sum(LMI),
  "QMI": sum(QMI),
  "LSI": LSI,
  "LSS": LSS,
  "njets": cuts["NJETS"],
  "nbjets": cuts["NBJETS"],
  "ak4ht": cuts["AK4HT"],
  "met": cuts["MET"],
  "leppt": cuts["LEPPT"],
  "mt": cuts["MT"],
  "mindr": cuts["MINDR"],
  "jet0pt": cuts["JET0PT"],
  "jet1pt": cuts["JET1PT"],
  "jet2pt": cuts["JET2PT"]
} )

# Save used parameters to file
config_file = os.path.join( args.dataset, subDirName, "config_" + CONFIG["tag"] + ".json" )
with open( config_file, "w" ) as f:
  f.write( write_json( CONFIG, indent=2 ) )
print( "[OK ] Parameters saved to dataset folder." )

# Start the logfile
logfile = open( CONFIG["log_file"], "w" )
logfile.write("{:7}, {:7}, {:7}, {:7}, {:9}, {:14}, {:10}, {:7}\n".format(
      "Hidden",
      "Nodes",
      "Rate",
      "Batch",
      "Pattern",
      "Regulator",
      "Activation",
      "AUC"
    )
  )

# Determine optimization space
opt_space = []
opt_order = {}
i = 0
for param, value in CONFIG.iteritems():
  if param not in CONFIG["static"]:
    if type(value[0]) == str:
      opt_space.append( Categorical(value, name=param) )
    elif param == "learning_rate":
      opt_space.append( Categorical(value, name=param) )
    else:
      opt_space.append( Integer(*value, name=param) )
    opt_order[param] = i
    i += 1

# Objective function

# Persist cut events to speed up process
cut_events = None

@use_named_args(opt_space)
def objective(**X):
  global cut_events
    
  print(">> Configuration:\n{}\n".format(X))
  if not "variables" in X: X["variables"] = CONFIG["variables"]
  if not "patience" in X: X["patience"] = CONFIG["patience"]
  if not "epochs" in X: X["epochs"] = CONFIG["epochs"]
  model = mltools.HyperParameterModel(
    X, 
    signal_files, background_files,
    cuts["NJETS"], cuts["NBJETS"], cuts["AK4HT"],
    CONFIG["model_name"]
  )
  save_paths = []
  parts = 1
  if int( cuts["AK4HT"] ) >= 500: parts = 1
  elif int( cuts["AK4HT"] ) >= 400: parts = 2
  elif int( cuts["AK4HT"] ) >= 300: parts = 3
  else: parts = 4

  for i in range( parts ):
    save_paths.append( os.path.join( os.getcwd(), "TTT_DNN_nJ{}_nB{}_HT{}_{}_{}.pkl".format( cuts["NJETS"], cuts["NBJETS"], cuts["AK4HT"], year, i + 1 ) ) )

  if cut_events is None:
    if not os.path.exists(save_paths[0]):
      print( ">> Generating saved cut event .pkl file." )
      print( "   >> Loading Trees..." )
      model.load_trees()
      print( "   >> Applying Cuts..." )
      #model.apply_cut_prq(save_paths)
      model.apply_cut()
      print( "   >> Saving Events to .pkl" )
      model.save_cut_events( save_paths )
    else:
      print( ">> Loading saved cut event .pkl files." )
      model.load_cut_events_pkl( save_paths )
    #cut_events = model.cut_events_prq.copy()
    cut_events = model.cut_events.copy()
  else:
    #model.cut_events_prq = cut_events.copy()
    model.cut_events = cut_events.copy()
    
  model.build_model()
  #model.train_model_prq()
  model.train_model_pkl()
    
  print( ">> Obtained ROC-Integral value: {}".format(model.auc_test))
  logfile.write('{:7}, {:7}, {:7}, {:7}, {:9}, {:14}, {:10}, {:7}\n'.format(
    str(X["hidden_layers"]),
    str(X["initial_nodes"]),
    str(X["learning_rate"]),
    str(2**X["batch_power"]),
    str(X["node_pattern"]),
    str(X["regulator"]),
    str(X["activation_function"]),
    str(round(model.auc_test, 5))
    )
  )
  opt_metric = log(1 - model.auc_test)
  print( ">> Metric: {:.4f}".format( opt_metric ) )
  return opt_metric

# Perform the optimization
start_time = datetime.now()

res_gp = gp_minimize(
            func = objective,
            dimensions = opt_space,
            n_calls = CONFIG["n_calls"],
            n_random_starts = CONFIG["n_starts"],
            verbose = True
            )

logfile.close()

# Report results
print(">> Writing optimized parameter log to: optimized_params_" + CONFIG["tag"] + ".txt and .json")
with open(os.path.join(args.dataset, subDirName, "optimized_params_" + CONFIG["tag"] + ".txt"), "w") as f:
  f.write("TTT DNN Hyper Parameter Optimization Parameters \n")
  f.write("Static and Parameter Space stored in: {}\n".format(config_file))
  f.write("Optimized Parameters:\n")
  f.write("    Hidden Layers: {}\n".format(res_gp.x[opt_order["hidden_layers"]]))
  f.write("    Initial Nodes: {}\n".format(res_gp.x[opt_order["initial_nodes"]]))
  f.write("    Batch Power: {}\n".format(res_gp.x[opt_order["batch_power"]]))
  f.write("    Learning Rate: {}\n".format(res_gp.x[opt_order["learning_rate"]]))
  f.write("    Node Pattern: {}\n".format(res_gp.x[opt_order["node_pattern"]]))
  f.write("    Regulator: {}\n".format(res_gp.x[opt_order["regulator"]]))
  f.write("    Activation Function: {}\n".format(res_gp.x[opt_order["activation_function"]]))
with open(os.path.join(args.dataset, subDirName, "optimized_params_" + CONFIG["tag"] + ".json"), "w") as f:
  f.write(write_json(dict([(key, res_gp.x[val]) for key, val in opt_order.iteritems()]), indent=2))
print( "[OK ] Finished optimization in: {}".format( datetime.now() - start_time ) )

