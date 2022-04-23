#!/usr/bin/env python

import os, sys, glob
from argparse import ArgumentParser
import numpy as np
import ROOT
from ROOT import TFile, TTree
from array import array
from json import loads as load_json
import os, sys

os.environ["KERAS_BACKEND"] = "tensorflow"

import tensorflow as tf
import keras
import config


# read in arguments
parser = ArgumentParser()
parser.add_argument("-f","--file",required=True)
args = parser.parse_args()

modelNames = glob.glob("*.tf")
jsonNames  = glob.glob("*.json")

def setup( modelNames, jsonNames ):
    models = []
    varlist = []
    indexlist = []
    taglist = []
    jetlist = []
    # load in the json parameter files and get the variables used and the jet cut
    for jsonName in sorted(jsonNames):
        jsonFile = ( load_json( open( jsonName ).read() ) ) 
        varlist.append( list( jsonFile[ "variables" ] ) )
        indexlist.append( [ jsonFile[ "start_index" ], jsonFile[ "end_index" ] ] )
        taglist.append( jsonFile[ "tag" ] )
        jetlist.append( jsonFile[ "njets"] )
        print( ">> Using parameters file: {} with {} variables and {} jets".format( jsonName, len( jsonFile[ "variables" ] ), jsonFile[ "njets" ] ) )
    # load in the keras DNN models
    for modelName in sorted( modelNames ):
        print( ">> Testing model: {}".format( modelName ) )
        models.append( tf.keras.models.load_model( modelName ) )

    return models, varlist, jetlist, indexlist, taglist


def get_predictions( models, varlist, fName, tName = "ljmet" ):
    events = []
    discs = []
    df = ROOT.RDataFrame( tName, fName )

    for variables in varlist:
        if df.Count() == 0: 
            events.append( np.asarray([]) )
        else:
            eventDict = df.AsNumpy( columns = [ variable.encode( "ascii", "ignore" ) for variable in variables ] )
            eventList = []
            for variable in sorted( variables ):
                eventList.append( eventDict[ variable ] )
            events.append( np.array( eventList ).transpose() )
    
    for i, model in enumerate(models):
        if df.Count() == 0: 
            discs.append( np.asarray([]) )
        else: 
            discs.append( model.predict( events[i] ) )
        print( "[INFO] Discriminator stats: {:.3f} pm {:.3f}".format( np.mean( discs[i] ), np.std( discs[i] ) ) )
    return discs 
        

def fill_tree( modelNames, jetlist, varlist, indexlist, disclist, taglist, rootTree ): 
    out = TFile( args.file.split( "/" )[-1], "RECREATE" );
    out.cd()
    newTree = rootTree.CloneTree(0);
    DNN_disc = {}
    disc_name = {}
    branches = {}
    for i, modelName in enumerate( sorted( modelNames ) ):
        DNN_disc[ modelName ] = array( "f", [0.] )
        disc_name[ modelName ] = "DNN_{}".format( str( taglist[i] ) )
        print( ">> Creating new step3 branch: {}".format( disc_name[ modelName ] ) )
        branches[ modelName ] = newTree.Branch( disc_name[ modelName ], DNN_disc[ modelName ], disc_name[ modelName ] + "/F" );
        print( "   - {:.4f} pm {:.4f}".format( np.mean( disclist[i] ), np.std( disclist[i] ) ) )
    for i in range( len(disclist[0]) ):
        rootTree.GetEntry(i)
        for j, modelName in enumerate( sorted( modelNames ) ):
            DNN_disc[ modelName ][0] = disclist[j][i]
        newTree.Fill()
    print( "[OK] Successfully added {} new discriminators".format( len( modelNames ) ) )
    newTree.Write()
    out.Write()
    out.Close()

def main():
    print( "[START] Running the step3 production..." )
    models, varlist, jetlist, indexlist, taglist = setup( modelNames, jsonNames )
    rootFile = TFile.Open( args.file );
    rootTree = rootFile.Get( "ljmet" ); 
    print( ">> Creating step3 for sample: {}.root".format( args.file ) )
    disclist = get_predictions( models, varlist, args.file, "ljmet" )
    fill_tree( modelNames, jetlist, varlist, indexlist, disclist, taglist, rootTree )
    print( "[DONE] Finished adding {} DNN discriminator branches to {}".format( len( disclist ), args.file ) )

main()
