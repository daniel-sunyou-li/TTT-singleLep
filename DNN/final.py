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
parser.add_argument( "-d", "--dataset", required = True, help="The dataset folders to search for HPO information")
parser.add_argument( "-f", "--folder", default="auto", help="The name of the output folder.")
parser.add_argument( "-k", "--num-folds", default="5", help="The number of cross-validation iterations to perform for each configuration")
parser.add_argument( "-m", "--metric", default = "AUC", help="Metric for best model options: STABLE,LOSS,ACC,AUC" )
parser.add_argument( "--no-cut-save", action="store_true", help="Do not attempt to load or create saved cut event files.")
parser.add_argument( "--ensemble", action="store_true", help="Final model is the weighted ensemble of all k models." )
parser.add_argument( "--override", action="store_true", help="Write new event file." )
args = parser.parse_args()

if args.metric not in [ "STABLE", "LOSS", "ACC", "AUC" ]:
  quit( "[ERR] Invalid model evaluation metric selected, choose from: STABLE, LOSS, ACC, AUC. Quitting..." )

print( "[START] Final Model Training: k-fold Cross Validation" )

# Look for HPO data files
hpo_data = {}
print("[INFO] Using dataset: {}".format(args.dataset))
if os.path.exists(args.dataset):
  if os.path.isdir(args.dataset):
    for dfile in os.listdir(args.dataset):
      if dfile.startswith("optimized_params") and dfile.endswith(".json"):
        try:
          with open( os.path.join( args.dataset, dfile ), "r") as f:
            hpo_data[os.path.join( args.dataset, dfile)] = load_json(f.read())
        except:
          quit("[ERR] Unable to read JSON from {}. Quitting...".format(os.path.join(args.dataset, dfile)))
  else:
    try:
      with open(args.dataset, "r") as f:
        hpo_data[args.dataset] = load_json(f.read())
    except:
      print("[WARN] Unable to read JSON from {}.".format(args.dataset))
        
# Create output folder
folder = args.folder
if folder == "auto":
  folder = "final_" + datetime.now().strftime("%d.%b.%Y")
if not os.path.exists(folder):
  os.mkdir(folder)

# Open output file
summary_f = open(os.path.join(folder, "log_kfcv.txt"), "w")
summary_f.write("Final Training Summary: {}\n\n".format(datetime.now().strftime("%d.%b.%Y")))
summary_f.write("Index , Parameters , Model , AUC , Accuracy , Loss \n")

data = {}

cv_folder = os.path.join(folder, "cross_validation")
if not os.path.exists(cv_folder):
  os.mkdir(cv_folder)
        
# Load JSON data
parameters = {}
for file_ in os.listdir( args.dataset ):
  if file_.startswith( "config" ) and file_.endswith( ".json" ):
    with open( os.path.join( args.dataset, file_ ), "r" ) as f:
      parameters.update( load_json(f.read()) )
  if file_.startswith( "optimized" ) and file_.endswith( ".json" ):
    with open( os.path.join( args.dataset, file_ ), "r" ) as f:
      parameters.update( load_json(f.read()) )
parameters["PATIENCE"] = config.params["KFCV"]["PATIENCE"]
parameters["EPOCHS"]    = config.params["KFCV"]["EPOCHS"]
  
model_path = os.path.join(folder, "final_model_{}.tf".format( parameters[ "TAG" ] ) )
  
save_path = os.path.join( args.dataset.split("/")[0], "events.root" )

# Gather list of signal and background folders
  
model = mltools.CrossValidationModel(
  parameters,
  parameters["SIGNAL FILES"], parameters["BACKGROUND FILES"], parameters["VARIABLES"], 
  float( parameters["RATIO"] ), cv_folder, parameters[ "EVENT CUT" ],
  int(args.num_folds ), args.metric 
)

print( ">> Checking for saved events at: {}".format(save_path) )
if not os.path.exists(save_path):
  print( ">> Generating saved cut event files." )
  model.apply_cut()
  model.save_cut_events( save_path, config.params[ "WEIGHT XSEC" ] )
  model.load_cut_events( save_path, config.params[ "WEIGHT XSEC" ] )
else:
  print( ">> Loading saved cut event files." )
  model.load_cut_events( save_path, config.params[ "WEIGHT XSEC" ], args.override )
print( ">> Starting cross-validation." )
    
model.train_model()

print( ">> Collecting results." )
for k in range(model.num_folds):
  print(">> Finished iteration {} with ROC-Integral value: {}{}.".format(
    k, model.auc_test[k], " (best)" if k == model.best_fold else "" ) )
  summary_f.write(" , ".join([str(x) for x in [ str(k), model_path if k == model.best_fold else "unsaved", model.auc_test[k], model.accuracy[k], model.loss[k]]]) + "\n" )
print( ">> AUC (test)  = {:.4f} +- {:.4f}".format( np.mean( model.auc_test ), np.std( model.auc_test ) ) )
print( ">> AUC (train) = {:.4f} +- {:.4f}".format( np.mean( model.auc_train ), np.std( model.auc_train ) ) )
data = {
  "MODEL PATH": model_path,
  "PARAMETERS": parameters,        
  "BEST MODEL": model.best_fold,
  "AUC TEST": model.auc_test,
  "AUC TRAIN": model.auc_train,
  "AUC TEST K": [ np.mean(model.auc_test), np.std(model.auc_test) ],
  "AUC TRAIN K": [ np.mean(model.auc_train), np.std(model.auc_train) ],
  "LOSS TRAIN": model.loss_train[ model.best_fold ],
  "LOSS VALIDATION": model.loss_validation[ model.best_fold ],
  "FPR TRAIN": [",".join(["{:.5f}".format(x) for x in fpr]) for fpr in model.fpr_train],
  "TPR TRAIN": [",".join(["{:.5f}".format(x) for x in tpr]) for tpr in model.tpr_train],
  "FPR TEST": [",".join(["{:.5f}".format(x) for x in fpr]) for fpr in model.fpr_test],
  "TPR TEST": [",".join(["{:.5f}".format(x) for x in tpr]) for tpr in model.tpr_test]
}

if args.ensemble:
  print( ">> Saving final model as ensemble of all models as {}".format( model_path ) )
  model.ensemble_models( model_path )
else:
  print( ">> Preserving best model file as {}".format( model_path ) )
  copy( model.model_paths[ model.best_fold ], model_path )
  #rmtree(cv_folder)

summary_f.close()

print( ">> Writing final data file to {}".format( os.path.join( folder, "data.json" ) ) )
with open( os.path.join( folder, "data.json" ), "w" ) as f:
  dump_json(data, f, indent=2)

print( "[DONE] Finished training and selecting model for application." )
