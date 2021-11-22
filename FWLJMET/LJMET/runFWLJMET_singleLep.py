import FWCore.ParameterSet.Config as cms
import os

relBase = os.environ[ "CMSSW_BASE" ]

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing( "analysis" )
options.register( "isMC", True, VarParsing.multiplicity.singleton, VarParsing.varType.bool, "Is MC" )
options.register( "isTTbar", True, VarParsing.multiplicity.singleton, VarParsing.varType.bool, "Is TTbar" )
options.register( "doGenHT", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool, "Do Gen HT" )
options.register( "isTest", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool, "Is Test" )
options.register( "era", "2017", VarParsing.multiplicity.singleton, VarParsing.varType.string, "Sample Era" )

options.setDefault( "maxEvents", 10 )
