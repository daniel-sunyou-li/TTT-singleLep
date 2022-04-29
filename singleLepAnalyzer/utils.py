#!/usr/bin/python

import sys,math
import numpy as np
import config
from ROOT import *

def contains_category( category, categories ):
  for key in config.params[ "ABCDNN" ][ "CONTROL VARIABLES" ]:
    if category[ key ][0] not in categories[ key ]:
      return False
  return True

def hist_parse( hist_name, samples ):
  parse = {
    "PROCESS": "",    # mostly used in templates.py to associate to Combine group
    "GROUP": "",      # returns a process' analysis group (i.e. DAT, BKG, SIG)
    "COMBINE": "",    # returns a process' associated Combine group
    "SYST": "",       # returns the systematic name
    "SHIFT": "",      # returns the systematic shift
    "IS SYST": False, # bool if systematic histogram
    "CATEGORY": "",   # full category with lepton type and jet multiplicities
    "CHANNEL": "",    # jet multiplicities
    "ABCDNN": False   # bool if the category is in ABCDNN SR
  }
  parts = hist_name.split( "_" )
  for part in parts:
    if part in samples.groups[ "DAT" ][ "PROCESS" ] + [ "DAT", "data", "obs" ]: 
      parse[ "PROCESS" ] = part
      parse[ "GROUP" ] = "DAT"
      parse[ "COMBINE" ] = "data_obs"
    elif part in samples.groups[ "SIG" ][ "PROCESS" ] + [ "SIG" ]:
      parse[ "PROCESS" ] = part
      parse[ "GROUP" ] = "SIG"
      parse[ "COMBINE" ] = part
    elif part in samples.groups[ "BKG" ][ "SUPERGROUP" ].keys() + [ "ABCDNN" ]:
      parse[ "GROUP" ] = "BKG"
      parse[ "COMBINE" ] = part
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
      parse[ "IS SYST" ] = True
      if part.endswith( "UP" ) or part.endswith( "DN" ):
        parse[ "SHIFT" ] = part[-2:]
        parse[ "SYST" ] = "PDF{}".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() ) if config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() in part else "PDF"
      else:
        parse[ "SHIFT" ] = part[3:]
        parse[ "SYST" ] = "PDF"

    if part.startswith( "is" ):
      parse[ "CATEGORY" ] = part
      parse[ "CHANNEL" ] = part[3:]
  
  abcdnnX = config.params[ "ABCDNN" ][ "CONTROL VARIABLES" ][0]
  abcdnnY = config.params[ "ABCDNN" ][ "CONTROL VARIABLES" ][1]
  abcdnnCheckX = abcdnnX.lower() + config.hist_bins[ "ABCDNN" ][ abcdnnX ][0] in parse[ "CATEGORY" ].lower()
  abcdnnCheckY = abcdnnY.lower() + config.hist_bins[ "ABCDNN" ][ abcdnnY ][0] in parse[ "CATEGORY" ].lower()
  if abcdnnCheckX and abcdnnCheckY:
    parse[ "ABCDNN" ] = True

  return parse

def hist_tag( *args ):
  histTag = args[0]
  for arg in args[1:]: histTag += "_{}".format( arg )
  return histTag
