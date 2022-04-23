# this script loads in a trained model from the specified folder and applies it to a dataset and reports the average DNN discriminator value
# for the ttt signal samples, tttt and a ttbar sample

import os, sys, glob
from argparse import ArgumentParser
import numpy as np
import ROOT
from array import array
from json import loads as load_json
from pickle import load as pickle_load

os.environ[ "KERAS_BACKEND" ] = "tensorflow"

import tensorflow as tf
import keras

parser = ArgumentParser()
parser.add_argument( "-m", "--model", required = True )
parser.add_argument( "-f", "--folder", required=True )
args = parser.parse_args()

execfile( "config.py" )

jsonFile = load_json( open( glob.glob( "{}/config*.json".format( args.folder ) )[0] ).read() )

model = tf.keras.models.load_model( args.model )

year = jsonFile[ "year" ]

files = [
"TTT_DNN_nJ4_nB2_HT350_17_1.pkl",
"TTT_DNN_nJ4_nB2_HT350_17_2.pkl",
"TTT_DNN_nJ4_nB2_HT350_17_3.pkl"
]

CUT_VARIABLES = [
  "leptonPt_MultiLepCalc", "isElectron", "isMuon",
  "corr_met_MultiLepCalc", "MT_lepMet", "minDR_lepJet",
  "DataPastTriggerX", "MCPastTriggerX", "isTraining", 
  "AK4HT", "NJetsCSV_JetSubCalc", "NJets_JetSubCalc" 
]

WEIGHT_VARIABLES = [
  "triggerXSF", "pileupWeight", "lepIdSF", 
  "EGammaGsfSF", "isoSF", "L1NonPrefiringProb_CommonCalc",
  "MCWeight_MultiLepCalc", "xsecEff", "tthfWeight",
  "btagDeepJetWeight", "btagDeepJet2DWeight_HTnj"
]

ML_VARIABLES = [ x[0] for x in varList[ "DNN" ] ]

VARIABLES = list( sorted( list( set( ML_VARIABLES ).union( set( CUT_VARIABLES ) ).union( set( WEIGHT_VARIABLES ) ) ) ) ) 

variables = [ variable.encode( "ascii", "ignore" ) for variable in jsonFile[ "variables" ] ]
positions = { variable: VARIABLES.index( variable ) for variable in variables }
var_mask = [ positions[ variable ] for variable in positions ]


events = []
for file in files:
  with open( file, "rb" ) as f:
    event = pickle_load( f )
    events.append( event )

signals = events[0][ "signal" ].copy()
bkgs = events[0][ "background" ].copy()
del events[0]
while len( events ) > 0:
  while len( events[0][ "signal" ].keys() ) > 0:
    key = events[0][ "signal" ].keys()[0]
    signals[ key ].extend( events[0][ "signal" ][ key ] )
    del events[0][ "signal" ][ key ]
  while len( events[0][ "background" ].keys() ) > 0:
    key = events[0][ "background" ].keys()[0]
    bkgs[ key ].extend( events[0][ "background" ][ key ] )
    del events[0][ "background" ][ key ]
  del events[0]

input_sig = np.concatenate( [ signals[ key ] for key in signals ] )[:,var_mask]
input_bkg = np.concatenate( [ bkgs[ key ] for key in bkgs ] )[:,var_mask]

print( variables )
print( var_mask )
print( input_sig[0] )

disc_sig = model.predict( input_sig )[:,0]
disc_bkg = model.predict( input_bkg )[:,0]

print( "[INFO] Signal: {:.3f} pm {:.3f}".format( np.mean( disc_sig ), np.std( disc_sig ) ) )
print( "  >> Minimum: {}".format( min( disc_sig ) ) )
print( "  >> Maximum: {}".format( max( disc_sig ) ) )

print( "[INFO] Background: {:.3f} pm {:.3f}".format( np.mean( disc_bkg ), np.std( disc_bkg ) ) )
print( "  >> Minimum: {}".format( min( disc_bkg ) ) )
print( "  >> Maximum: {}".format( max( disc_bkg ) ) )
