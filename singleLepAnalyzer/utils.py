#!/usr/bin/python

import itertools
import sys,math
import numpy as np
import config
from ROOT import *

def contains_category( category, categories ):
  categories_keys = sorted( [ key for key in categories.keys() ] )
  categories_comb = list(
    itertools.product(
      *[ categories[key_] for key_ in categories_keys ]
    )
  )
  category_tags = []
  for category_ in categories_comb:
    tag_ = "is{}".format( category_[ categories_keys.index( "LEPTON" ) ] )
    for key_ in categories_keys:
      if key_ == "LEPTON": continue
      tag_ += key_ + category_[ categories_keys.index( key_ ) ]
    category_tags.append( tag_ )

  if category in category_tags: return True
  else: return False

def category_tag( category ):
  tag = category[ "LEPTON" ][0]
  for key_ in sorted( category ):
    if key_ == "LEPTON": continue
    tag += key_.upper() + category[key_][0]
  return tag

def abcdnn_tag( category ):
  tag = ""
  for tag_ in config.params["ABCDNN"]["TAG"]:
    tagABCDNN = ""
    for key_ in sorted( config.params["ABCDNN"]["TAG"][tag_] ):
      if key_ == "LEPTON": continue
      tagABCDNN += key_ + config.params["ABCDNN"]["TAG"][tag_][key_][0]
    if tagABCDNN in category:
      tag = tag_
  return tag

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
        parse[ "SYST" ] = part[:-2]
      else:
        parse[ "SHIFT" ] = part[3:]
        parse[ "SYST" ] = "PDF"

    if part.startswith( "is" ):
      parse[ "CATEGORY" ] = part
      parse[ "CHANNEL" ] = part[3:]
  
  check_tag = {}
  for tag_ in config.params["ABCDNN"]["TAG"]:
    check_tag[tag_] = False
    if contains_category( parse["CATEGORY"], config.params["ABCDNN"]["TAG"][tag_] ):
      check_tag[tag_] = True

  # check each possible ABCDnn category and if histogram is in at least one of the categories, then flag as using ABCDnn
  for tag_ in check_tag:
    if check_tag[tag_]:
      parse["ABCDNN"] = True

  return parse

def hist_tag( *args ):
  histTag = args[0]
  for arg in args[1:]: histTag += "_{}".format( arg )
  return histTag
