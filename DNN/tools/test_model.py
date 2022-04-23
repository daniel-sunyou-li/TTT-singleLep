# this script loads in a trained model from the specified folder and applies it to a dataset and reports the average DNN discriminator value
# for the ttt signal samples, tttt and a ttbar sample

import os, sys, glob
from argparse import ArgumentParser
import numpy as np
import ROOT
from array import array
from json import loads as load_json

os.environ[ "KERAS_BACKEND" ] = "tensorflow"

import tensorflow as tf
import keras

parser = ArgumentParser()
parser.add_argument( "-m", "--model", required = True )
parser.add_argument( "-f", "--folder", required=True )
args = parser.parse_args()

execfile( "config.py" )

def load_cut_events( paths ):
  cut_events_pkl = []
  for path in paths:
    with open( path, "rb" ) as f:
      cut_event_pkl = pickle_load( f )
      cut_events_pkl.append( cut_event_pkl )

jsonFile = load_json( open( glob.glob( "{}/config*.json".format( args.folder ) )[0] ).read() )

model = tf.keras.models.load_model( args.model )

year = jsonFile[ "year" ]

files = [
  step2DirXRD[ year ] + "nominal/" + sig_training[ year ][0], # tttj
  #step2DirXRD[ year ] + "nominal/" + sig_training[ year ][1], # tttw
  step2DirXRD[ year ] + "nominal/" + bkg_training[ year ][5], 
  #config.step2DirXRD[ year ] + "nominal/" + config.bkg_training[ year ][1]  # ttjj
]

variables = [ variable.encode( "ascii", "ignore" ) for variable in jsonFile[ "variables" ] ]


for file in files:
  df = ROOT.RDataFrame( "ljmet", file )
  df_1 = df.Filter( "isTraining == 1" ).Filter( "DataPastTriggerX == 1 && MCPastTriggerX == 1" ).Filter( "isElectron == 1 || isMuon == 1" )
  df_2 = df_1.Filter( "NJetsCSV_JetSubCalc >= 2 && NJets_JetSubCalc >= 4" )
  df_3 = df_2.Filter( "AK4HT > 350 && corr_met_MultiLepCalc > 20 && minDR_lepJet > 0.4" )
  eventDict = df_3.AsNumpy( columns = variables )
  eventList = []
  for variable in sorted( variables ):
    eventList.append( eventDict[variable] )
  events = np.array( eventList ).transpose()
  disc = model.predict( events )[:,0]
  print( "{}: {:.4f} pm {:.4f}".format( file.split("/")[-1], np.mean( disc ), np.std( disc ) ) )
  print( "  >> {} events".format( len( disc ) ) )
  print( "  >> Minimum: {}".format( min( disc ) ) )
  print( "  >> Maximum: {}".format( max( disc ) ) ) 
