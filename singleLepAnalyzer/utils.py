#!/usr/bin/python

import sys,math
import numpy as np
import config
from ROOT import *

def contains_category( category, categories ):
  for key in config.params[ "ABCDNN" ][ "CONTROL VARIABLES" ]:
    if category[ key ][0] not in categories[ key ]:
      print( category[ key ][0], categories[ key ] )
      return False
  return True

def hist_parse( hist_name, samples ):
  parse = {
    "PROCESS": "",
    "GROUP": "",
    "COMBINE": "",
    "SYST": "",
    "SHIFT": "",
    "IS SYST": False,
    "CATEGORY": "",
    "CHANNEL": ""
  }
  parts = hist_name.split( "_" )
  for part in parts:
    if part in samples.groups[ "SIG" ][ "PROCESS" ] + [ "SIG" ]:
      parse[ "PROCESS" ] = part
      parse[ "GROUP" ] = "SIG"
      parse[ "COMBINE" ] = part
    elif part in samples.groups[ "BKG" ][ "SUPERGROUP" ].keys():
      parse[ "PROCESS" ] = part
      parse[ "GROUP" ] = "BKG"
      parse[ "COMBINE" ] = part
    elif part in samples.groups[ "DAT" ][ "PROCESS" ] + [ "DAT", "data", "obs" ]:
      parse[ "PROCESS" ] = part
      parse[ "GROUP" ] = "DAT"
      parse[ "COMBINE" ] = "data_obs"
    elif part in samples.groups[ "BKG" ][ "ALL" ]:
      parse[ "PROCESS" ] = part
      parse[ "GROUP" ] = "BKG"
      for group in samples.groups[ "BKG" ][ "SUPERGROUP" ].keys():
        if part in samples.groups[ "BKG" ][ "SUPERGROUP" ][ group ]:
          parse[ "COMBINE" ] = group

    if part.endswith( "UP" ) or part.endswith( "DN" ):
      parse[ "SHIFT" ] = part[-2:]
      parse[ "SYST" ] = part[:-2]
      parse[ "IS SYST" ] = True
    if "PDF" in part:
      if part.endswith( "UP" ) or part.endswith( "DN" ):
        parse[ "SHIFT" ] = part[-2:]
        parse[ "SYST" ] = "PDF{}".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() ) if config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() in part else "PDF"
      else:
        parse[ "SHIFT" ] = part[3:]
        parse[ "SYST" ] = "PDF"
      parse[ "IS SYST" ] = True

    if part.startswith( "is" ):
      parse[ "CATEGORY" ] = part
      parse[ "CHANNEL" ] = part[3:]
  return parse

def hist_tag( *args ):
  histTag = args[0]
  for arg in args[1:]: histTag += "_{}".format( arg )
  return histTag
