#!/usr/bin/env python

import os, sys, glob
from argparse import ArgumentParser
import numpy as np
import ROOT
from ROOT import TFile, TTree
from array import array
from json import loads as load_json
import os, sys
#import tqdm

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
    # load in the json parameter files and get the variables used and the jet cut
    for jsonName in sorted( jsonNames ):
        jsonFile = ( load_json( open( jsonName ).read() ) ) 
        varlist.append( sorted( jsonFile[ "VARIABLES" ] ) )
        indexlist.append( [ jsonFile[ "START INDEX" ], jsonFile[ "END INDEX" ] ] )
        taglist.append( jsonFile[ "TAG" ] )
        print( ">> Using parameters file: {} with {} variables".format( jsonName, len( jsonFile[ "VARIABLES" ] ) ) )
    # load in the keras DNN models
    for modelName in sorted( modelNames ):
        print( ">> Testing model: {}".format( modelName ) )
        models.append( tf.keras.models.load_model( modelName ) )

    return models, varlist, indexlist, taglist


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
    del df
    return discs 
        

def fill_tree( fileName, modelNames, varlist, indexlist, disclist, taglist, rootTree ): 
    out = TFile( fileName.split( "/" )[-1], "RECREATE" );
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
    models, varlist, indexlist, taglist = setup( modelNames, jsonNames )
    rootFile = TFile.Open( args.file )
    rootTree = rootFile.Get( "ljmet" ) 
    rootTree.SetBranchStatus( "*", 0 )
    branches = []
    for varlist_ in varlist:
      for bName in varlist_:
        if bName not in branches: branches.append( str(bName) )
    for bName in config.branches:
      if bName not in branches: branches.append( str(bName) )
    for branch in branches: 
      print( "[INFO] Including branch: {}".format( branch ) ) 
      rootTree.SetBranchStatus( branch, 1 )
    print( ">> Creating step3 for sample: {}".format( args.file ) )
    disclist = get_predictions( models, varlist, args.file, "ljmet" )
    fill_tree( args.file, modelNames, varlist, indexlist, disclist, taglist, rootTree )
    print( "[DONE] Finished adding {} DNN discriminator branches to {}".format( len( disclist ), args.file ) )

main()
