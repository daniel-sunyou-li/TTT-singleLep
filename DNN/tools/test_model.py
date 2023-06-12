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

year = jsonFile[ "YEAR" ].split( "," )[0]
files = [ jsonFile[ "SIGNAL FILES" ][0].encode( "ascii", "ignore" ), jsonFile[ "BACKGROUND FILES" ][0].encode( "ascii", "ignore" ) ]
variables = [ variable.encode( "ascii", "ignore" ) for variable in jsonFile[ "VARIABLES" ] ]

for file in files:
  df = ROOT.RDataFrame( "ljmet", file )
  df_filter = df.Filter( jsonFile[ "EVENT CUT" ].encode( "ascii", "ignore" ) )
  eventDict = df_filter.AsNumpy( columns = variables )
  eventList = []
  for variable in sorted( variables ):
    eventList.append( eventDict[variable] )
  events = np.array( eventList ).transpose()
  disc = model.predict( events )[:,0]
  hist = np.histogram( disc, bins = np.linspace( 0, 1, 11 ) )
  print( "{}: {:.4f} pm {:.4f}".format( file.split("/")[-1], np.mean( disc ), np.std( disc ) ) )
  print( "  >> {} events".format( len( disc ) ) )
  print( "  >> Minimum: {}".format( min( disc ) ) )
  print( "  >> Maximum: {}".format( max( disc ) ) ) 
  print( "  >> Bins: {}".format( hist[0] ) )
