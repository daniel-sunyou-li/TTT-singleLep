import os
from argparse import ArgumentParser
from json import loads as load_json
from json import dump as dump_json
from datetime import datetime
from shutil import rmtree, copy
import tensorflow as tf
import numpy as np

import config
import mltools

parser = ArgumentParser()
parser.add_argument( "datasets", nargs="*", default=[], help="The dataset folders to search for HPO information")
parser.add_argument( "-f", "--folder", default="auto", help="The name of the output folder.")
parser.add_argument( "-k", "--num-folds", default="5", help="The number of cross-validation iterations to perform for each configuration")
parser.add_argument( "-m", "--metric", default = "AUC", help="Metric for best model options: STABLE,LOSS,ACC,AUC" )
parser.add_argument( "--no-cut-save", action="store_true", help="Do not attempt to load or create saved cut event files.")
args = parser.parse_args()

if args.metric not in [ "STABLE", "LOSS", "ACC", "AUC" ]:
  quit( "[ERR] Invalid model evaluation metric selected, choose from: STABLE, LOSS, ACC, AUC. Quitting..." )

print( ">> Final Model Training: k-fold Cross Validation" )

# Look for HPO data files
hpo_data = {}
datasets = args.datasets
if args.datasets == []:
  datasets = [ d for d in os.listdir(os.getcwd()) if os.path.isdir(d) and d.startswith("dataset") ]
print(">> Using Datasets:\n - {}".format("\n - ".join(datasets)))
for dataset in datasets:
  if os.path.exists(dataset):
    if os.path.isdir(dataset):
      for dfile in os.listdir(dataset):
        if dfile.startswith("optimized_params") and dfile.endswith(".json"):
          try:
            with open( os.path.join( dataset, dfile ), "r") as f:
              hpo_data[os.path.join(dataset, dfile)] = load_json(f.read())
          except:
            print("[WARN] Unable to read JSON from {}.".format(os.path.join(dataset, dfile)))
    else:
      try:
        with open(dataset, "r") as f:
          hpo_data[dataset] = load_json(f.read())
      except:
        print("[WARN] Unable to read JSON from {}.".format(dataset))
        
# Create output folder
folder = args.folder
if folder == "auto":
  folder = "final_" + datetime.now().strftime("%d.%b.%Y")
if not os.path.exists(folder):
  os.mkdir(folder)

# Assign configuration order
config_order = list(sorted(hpo_data.keys(), key=lambda p: os.path.getmtime(p)))

# Open output file
summary_f = open(os.path.join(folder, "summary.txt"), "w")
summary_f.write("Final Training Summary: {}\n\n".format(datetime.now().strftime("%d.%b.%Y")))
summary_f.write("Index , Parameters , Model , AUC , Accuracy , Loss \n")

data = {}

# Go through all configurations
for config_num, config_path in enumerate(config_order):
  print(">> Now processing configuration #{} from {}.".format(config_num + 1, config_path))

  cv_folder = os.path.join(folder, "cross_validation")
  if not os.path.exists(cv_folder):
    os.mkdir(cv_folder)
        
  # Load JSON data
  parameters = None
  with open(config_path, "r") as f:
    parameters = load_json(f.read())

  # Load variables list
  with open(config_path.replace("optimized_params", "config"), "r") as f:
    config_json = load_json(f.read())
    parameters["variables"] = config_json["variables"]
    #parameters["patience"] = config_json["patience"][-1] if type(config_json["patience"]) == list else config_json["patience"]
    parameters["patience"] = 5
    #parameters["epochs"] = config_json["epochs"][-1] if type(config_json["epochs"]) == list else config_json["epochs"]
    parameters["epochs"] = 50
  print( ">> Using njets >= {} and nbjets >= {}".format( config_json[ "njets" ], config_json[ "nbjets" ] ) )
  
  model_path = os.path.join(folder, "final_model_{}j_{}to{}.tf".format( config_json[ "njets" ], config_json[ "start_index" ], config_json[ "end_index" ] ) )
  parts = 1
  if int( config_json["ak4ht"] ) >= 500: parts = 1
  elif int( config_json["ak4ht"] ) >= 400: parts = 2
  else: parts = 3
  save_paths = []
  for i in range( parts ):
    save_paths.append( os.path.join( os.getcwd(), "TTT_DNN_nJ{}_nB{}_HT{}_{}_{}.pkl".format( config_json[ "njets" ], config_json[ "nbjets" ], config_json[ "ak4ht" ], config_json["year"], i + 1 ) ) )  

  # Gather list of signal and background folders
  tree_folder = config.step2DirXRD[ config_json["year"] ] + "nominal"
  signal_files = [ os.path.join( tree_folder, sig ) for sig in config.sig_training[ config_json["year"] ] ]
  background_files = [ os.path.join( tree_folder, bkg ) for bkg in config.bkg_training[ config_json["year"] ] ]
  
  model = mltools.CrossValidationModel(
    parameters,
    signal_files, background_files, float( config_json["ratio"] ), 
    cv_folder, 
    config_json["njets"], config_json["nbjets"], config_json["ak4ht"], config_json["leppt"], config_json["met"], config_json["mt"], config_json["mindr"],
    int(args.num_folds ), args.metric )
  if not args.no_cut_save:
    if not os.path.exists(save_paths[0]):
      print( ">> Generating saved cut event files." )
      model.apply_cut()
      model.save_cut_events( save_paths )
    else:
      print( ">> Loading saved cut event files." )
      model.load_cut_events( save_paths )
  else:
    model.apply_cut()

  print( ">> Starting cross-validation." )
    
  model.train_model()

  print( ">> Collecting results." )

  for k in range(model.num_folds):
    print(">> Configuration {}.{} finished with ROC-Integral value: {}{}.".format(
      config_num, k, model.auc_test[k], " (best)" if k == model.best_fold else "" ) )
    summary_f.write(" , ".join([str(x) for x in [str(config_num) + "." + str(k), config_path, model_path if k == model.best_fold else "unsaved", model.auc_test[k], model.accuracy[k], model.loss[k]]]) + "\n" )
  print( ">> AUC (test)  = {:.4f} +- {:.4f}".format( np.mean( model.auc_test ), np.std( model.auc_test ) ) )
  print( ">> AUC (train) = {:.4f} +- {:.4f}".format( np.mean( model.auc_train ), np.std( model.auc_train ) ) )
  data[config_path] = {
    "config_id": config_num,
    "config_path": config_path,
    "model_path": model_path,
    "parameters": parameters,        
    "best_model": model.best_fold,
    "auc_test": model.auc_test,
    "auc_train": model.auc_train,
    "auc_test_k": [ np.mean(model.auc_test), np.std(model.auc_test) ],
    "auc_train_k": [ np.mean(model.auc_train), np.std(model.auc_train) ],
    "fpr_train": [",".join([str(x) for x in fpr]) for fpr in model.fpr_train],
    "tpr_train": [",".join([str(x) for x in tpr]) for tpr in model.tpr_train],
    "fpr_test": [",".join([str(x) for x in fpr]) for fpr in model.fpr_test],
    "tpr_test": [",".join([str(x) for x in tpr]) for tpr in model.tpr_test]
  }

  print( ">> Preserving best model file as {}".format( model_path ) )
  copy( model.model_paths[ model.best_fold ], model_path )
  #rmtree(cv_folder)

summary_f.close()

print( ">> Writing final data file to {}".format( os.path.join( folder, "data.json" ) ) )
with open( os.path.join( folder, "data.json" ), "w" ) as f:
  dump_json(data, f, indent=2)

print( "[OK ] Done." )
