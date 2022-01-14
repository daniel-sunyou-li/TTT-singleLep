# this script loads in a trained model from the specified folder and applies it to a dataset and reports the average DNN discriminator value
# for the ttt signal samples, tttt and a ttbar sample

import os, sys, glob
from argparse import ArgumentParser
import numpy as np
import ROOT
from array import array
from json import loads as load_json
import os, sys

os.environ[ "KERAS_BACKEND" ] = "tensorflow"

import tensorflow as tf
import keras
import config

parser = ArgumentParser()
parser.add_argument( "-f", "--folder", required=True )
args = parser.parse_args()
 
jsonFile = load_json( open( glob.glob( "{}/config*.json".format( args.folder ) )[0] ).read() )
model = tf.keras.models.load_model( glob.glob( "{}/*.tf".format( args.folder ) )[0] )

year = jsonFile[ "year" ]

files = [
  config.step2DirXRD[ year ] + "nominal/" + config.sig_training[ year ][0], # tttj
  config.step2DirXRD[ year ] + "nominal/" + config.sig_training[ year ][1], # tttw
  #config.step2DirXRD[ year ] + "nominal/" + config.bkg_training[ year ][0], # tttt
  #config.step2DirXRD[ year ] + "nominal/" + config.bkg_training[ year ][1]  # ttjj
]

variables = jsonFile[ "variables" ]

for file in files:
  rootFile = ROOT.TFile.Open( file );
  rootTree = rootFile.Get( "ljmet" );
  npTree = np.asarray( rootTree.AsMatrix( [ variable.encode( "ascii", "ignore" ) for variable in variables ] ) )
  events = model.predict( npTree )
  print( "{}: {:.4f} pm {:.4f}".format( file.split("/")[-1], np.mean( events ), np.std( events ) ) )
  print( "  >> {} events".format( len( events ) ) )
  print( "  >> Minimum: {}".format( min( events ) ) )
  print( "  >> Maximum: {}".format( max( events ) ) ) 
