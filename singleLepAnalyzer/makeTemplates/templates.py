#!/usr/bin/python

import os, sys, json, time, math, datetime, pickle, itertools
sys.path.append( "../" )
from argparse import ArgumentParser
import numpy as np
from array import array
import utils
import config

parser = ArgumentParser()
parser.add_argument( "-y", "--year",   required = True )
parser.add_argument( "-t", "--tag", required = True )
parser.add_argument( "-v", "--variables", nargs = "+", required = True )
parser.add_argument( "-r", "--region", required = True )
parser.add_argument( "--verbose", action = "store_true" )
args = parser.parse_args()

# parse options
if args.region not in list( config.region_prefix.keys() ): quit( "[ERR] Invalid region argument used. Quiting..." )
if args.year == "16":
  import samplesUL16 as samples
elif args.year == "17":
  import samplesUL17 as samples
elif args.year == "18":
  import samplesuL18 as samples
else:
  quit( "[ERR] Invalid -y (--year) argument used. Quitting" )

from ROOT import gROOT, TFile, TH1F

gROOT.SetBatch(1)

def get_categories( directory ):
  categories = [ directory for directory in os.walk( directory ).next()[1] if directory.startswith( "isE" ) or directory.startswith( "isM" ) ]
  return categories
  
def hist_tag( *args ):
  histTag = args[0]
  for arg in args[1:]: histTag += "_{}".format( arg )
  return histTag
        
def load_histograms( variable, templateDir, categories ): 
  hists =  { key: {} for key in [ "DAT", "BKG", "SIG", "CMB", "TEST" ] }
  
  for category in categories:
    categoryDir = os.path.join( templateDir, category )
    if config.options[ "GENERAL" ][ "TEST" ]:
      hists[ "TEST" ].update( pickle.load( open( os.path.join( categoryDir, "TEST_{}.pkl".format( variable ) ), "rb" ) ) )
    else:
      hists[ "DAT" ].update( pickle.load( open( os.path.join( categoryDir, "DATA_{}.pkl".format( variable ) ), "rb" ) ) )
      hists[ "BKG" ].update( pickle.load( open( os.path.join( categoryDir, "BACKGROUND_{}.pkl".format( variable ) ), "rb" ) ) )
      hists[ "SIG" ].update( pickle.load( open( os.path.join( categoryDir, "SIGNAL_{}.pkl".format( variable ) ), "rb" ) ) )
    
  return hists
  
def modify_histograms( hists, hist_key, scale, rebin ):
  def scale_luminosity( hists_, hist_key, scale ):
    if args.verbose: print( ">> Re-scaling {} MC luminosity by factor: {}".format( hist_key, scale ) )
    for hist_name in hists_[ hist_key ]:
      process = hist_name.split( "_" )[-1]
      if process in samples.samples[ "SIGNAL" ].keys() or process in samples.samples[ "BACKGROUND" ].keys():
        if args.verbose: print( "  + {}".format( hist_name ) )
        hists_[ hist_name ].Scale( scale )
    return hists_
  
  def rebinning( hists_, hist_key, rebin ):
    if args.verbose: print( ">> Re-binning {} histogram bins by: {}".format( hist_key, rebin ) )
    for hist_name in hists_[ hist_key ]:
      if args.verbose: print( "  + {}".format( hist_name ) )
      hists_[ hist_key ][ hist_name ].Rebin( rebin )
    return hists_
  
  def negative_correction( hists_, hist_key ):
    def function( hist_ ):
      change = False
      integral = hist_.Integral()
      for i in range( hist_.GetNbinsX() + 2 ):
        if hist_.GetBinContent( i ) < 0:
          hist_.SetBinContent( i, 0 )
          hist_.SetBinError( i, 0 )
          change = True
      if hist_.Integral() != 0 and integral > 0: hist_.Scale( integral / hist_.Integral() )
      return hist_, change
      
    if args.verbose: print( ">>  Correcting negative {} histogram bins".format( hist_key ) )
    for hist_name in hists_[ hist_key ]:
      process = hist_name.split( "_" )[-1]
      if process in samples.samples[ "SIGNAL" ].keys() or process in samples.samples[ "BACKGROUND" ].keys():
        hists_[ hist_key ][ hist_name ], change = function( hists_[ hist_key ][ hist_name ] )
        if change and args.verbose: print( "  + {}".format( hist_name ) )
    return hists_
  
  def bin_correction( hists_, hist_key ):
    def overflow( hist_ ):
      n = hist_.GetXaxis().GetNbins()
      content_over = hist_.GetBinContent( n ) + hist_.GetBinContent( n + 1 )
      error_over = math.sqrt( hist_.GetBinError( n )**2 + hist_.GetBinError( n + 1 )**2 )
      hist_.SetBinContent( n, content_over )
      hist_.SetBinError( n, error_over )
      hist_.SetBinContent( n + 1, 0 )
      hist_.SetBinError( n + 1, 0 )
      return hist_

    def underflow( hist_ ):
      content_under = hist_.GetBinContent( 1 ) + hist_.GetBinContent( 0 )
      error_under = math.sqrt( hist_.GetBinError( 1 )**2 + hist_.GetBinError( 0 )**2 )
      hist_.SetBinContent( 1, content_under )
      hist_.SetBinError( 1, error_under )
      hist_.SetBinContent( 0, 0 )
      hist_.SetBinError( 0, 0 )
      return hist_
    
    if args.verbose: print( ">>  Correcting {} over/under-flow bins".format( hist_key ) )
    for hist_name in hists_[ hist_key ]:
      hists_[ hist_key ][ hist_name ] = overflow( hists_[ hist_key ][ hist_name ] )
      hists_[ hist_key ][ hist_name ] = underflow( hists_[ hist_key ][ hist_name ] )
    
    return hists_
  
  if scale != 1.: hists = scale_luminosity( hists, hist_key, scale )
  if rebin > 0: hists = rebinning( hists, hist_key, rebin )
  hists = negative_correction( hists, hist_key )
  hists = bin_correction( hists, hist_key )
  
  return hists
  
def consolidate_histograms( hists, variable, categories, groups ):
  def scale_ttbar( hists_, scaleHF, scaleLF ):
    if hist_tag( variable, category, "TTBB" ) not in hists_[ "CMB" ].keys(): return hists_
    if hist_tag( variable, category, "TTNOBB" ) not in hists_[ "CMB" ].keys(): return hists_
    if args.verbose: print( ">> Scaling CMB ttbb histograms by a factor of {:.3f}".format( scaleHF ) )

    for category in categories:
      N = {
        "TTBB": hists[ "CMB" ][ hist_tag( variable, category, "TTBB" ) ].Integral(),
        "TTNOBB": hists[ "CMB" ][ hist_tag( variable, category, "TTNOBB" ) ].Integral()
      }
      if scaleLF == -1:
        try: scaleLF = 1. + ( 1. - scaleLF ) * ( N[ "TTBB" ] / N[ "TTNOBB" ] )
        except ZeroDivisionError: scaleLF = 1.
      
      hists_[ "CMB" ][ hist_tag( variable, category, "TTBB" ) ].Scale( scaleHF )
      hists_[ "CMB" ][ hist_tag( variable, category, "TTNOBB" ) ].Scale( scaleLF )
      
      if config.options[ "GENERAL" ][ "SYSTEMATICS" ]:
        for syst in config.systematics[ "MC" ] + [ "HD", "UE" ]:
          if syst == "HD" and not config.options[ "GENERAL" ][ "HDAMP" ]: continue
          if syst == "UE" and not config.options[ "GENERAL" ][ "UE" ]: continue
          for shift in [ "UP", "DN" ]:
            hists_[ "CMB" ][ hist_tag( variable, category, syst.upper() + shift, "TTBB" ) ].Scale( scaleHF )
            hists_[ "CMB" ][ hist_tag( variable, category, syst.upper() + shift, "TTNOBB" ) ].Scale( scaleLF )
      if config.options[ "GENERAL" ][ "PDF" ]:
        for i in range( config.params[ "PDF RANGE" ] ):
          hists_[ "CMB" ][ hist_tag( variable, category, "PDF" + i, "TTBB" ) ].Scale( scaleHF )
          hists_[ "CMB" ][ hist_tag( variable, category, "PDF" + i, "TTNOBB" ) ].Scale( scaleLF )
          
    return hists_
    
  def set_zero( hists_, hist_key, categories, zero ):
    if args.verbose: print( ">> Setting {} 0 bins to be non-trivial ({:.3e}) in histograms".format( hist_key, zero ) )
    for category in categories:
      for hist_name in hists_[ hist_key ]:
        process = hist_name.split( "_" )[-1]
        if process in list( samples.samples[ "DATA" ].keys() ): continue
        if hists_[ hist_key ][ hist_name ].Integral() == 0: 
          hists_[ hist_key ][ hist_name ].SetBinContent( 1, zero )
    return hists_

  if args.verbose: print( ">> Consolidating histograms by their grouping of: DAT, BKG and SIG" )
  for category in categories:
    prefix = "{}_{}_{}".format( variable, config.lumiStr[ args.year ], category )

    # combine SIG, DAT and TEST histograms into the CMB histogram
    for hist_key in hists:
      if hist_key == "CMB" or hist_key == "BKG": continue
      if hists[ hist_key ].keys() == []: continue
      if args.verbose: print( ">> Combining {} histograms".format( hist_key ) )
      hists[ "CMB" ][ hist_tag( hist_key, category ) ] = hists[ hist_key ][ hist_tag( prefix, groups[ hist_key ][ "PROCESS" ][0] ) ].Clone( hist_tag( prefix, hist_key ) )
      for process in groups[ hist_key ][ "PROCESS" ][1:]: hists[ "CMB" ][ hist_tag( hist_key, category ) ].Add( hists[ hist_key ][ hist_tag( prefix, process ) ] )
    
    # combine background hists
    for group in groups[ "BKG" ][ "PROCESS" ]:
      if args.verbose: print( ">> Combining group {} histograms".format( group ) )
      hists[ "CMB" ][ hist_tag( group, category ) ] = hists[ "BKG" ][ hist_tag( prefix, groups[ "BKG" ][ "PROCESS" ][ group ][0] ) ].Clone( hist_tag( prefix, group ) )
      for process in groups[ "BKG" ][ "PROCESS" ][ group ][1:]: hists[ "CMB" ][ hist_tag( group, category ) ].Add( hists[ "BKG" ][ hist_tag( prefix, process ) ] )
    
    for group in groups[ "BKG" ][ "SUPERGROUP" ]:
      print( ">> Combining super group {} histograms".format( group ) )
      hists[ "CMB" ][ hist_tag( group, category ) ] = hists[ "BKG" ][ hist_tag( prefix, groups[ "BKG" ][ "SUPERGROUP" ][ group ][0] ) ].Clone( hist_tag( prefix, group ) )
      for process in groups[ "BKG" ][ "SUPERGROUP" ][ group ][1:]: hists[ "CMB" ][ hist_tag( group, category ) ].Add( hists[ "BKG" ][ hist_tag( prefix, process ) ] )
        
    if config.options[ "GENERAL" ][ "SYSTEMATICS" ]:
      for syst in config.systematics[ "MC" ] + [ "HD", "UE" ]:
        if syst == "HD" and not config.options[ "GENERAL" ][ "HDAMP" ]: continue
        if syst == "UE" and not config.options[ "GENERAL" ][ "UE" ]: continue
        for shift in [ "UP", "DN" ]:
          sysTag = syst.upper() + shift
          prefix = "{}_{}_{}_{}".format( variable, sysTag, config.lumiStr[ args.year ], category )
          
          if args.verbose: print( ">> Combining {} SIG histograms".format( syst.upper() + shift ) )
          hists[ "CMB" ][ hist_tag( "SIG", sysTag, category ) ] = hists[ "SIG" ][ hist_tag( prefix, groups[ "SIG" ][ "PROCESS" ][0] ) ].Clone( hist_tag( prefix, "SIG" ) )
          for process in groups[ "SIG" ][ "PROCESS" ][1:]: hists[ "CMB" ][ hists( "SIG", sysTag, category ) ].Add( hists[ "SIG" ][ hist_tag( prefix, process ) ] )
          if args.verbose: print( ">> Combining {} BKG group histograms".format( syst.upper() + shift ) )
          for group in groups[ "BKG" ][ "PROCESS" ]:
            hists[ "CMB" ][ hist_tag( group, sysTag, category ) ] = hists[ "BKG" ][ hist_tag( prefix, groups[ "BKG" ][ "PROCESS" ][ group ][0] ) ].Clone( hist_tag( prefix, group ) )
            for process in groups[ "BKG" ][ "PROCESS" ][ group ][1:]: hists[ "CMB" ][ hist_tag( group, sysTag, category ) ].Add( hists[ "BKG" ][ hist_tag( prefix, process ) ] )
          
          for group in groups[ "BKG" ][ "SUPERGROUP" ]:
            hists[ "CMB" ][ hist_tag( group, sysTag, category ) ] = hists[ "BKG" ][ hist_tag( prefix, groups[ "BKG" ][ "SUPERGROUP" ][ group ][0] ) ].Clone( hist_tag( prefix, group ) )
            for process in groups[ "BKG" ][ "SUPERGROUP" ][ group ][1:]: hists[ "CMB" ][ hist_tag( group, sysTag, category ) ].Add( hists[ "BKG" ][ hist_tag( prefix, process ) ] )
     
    if config.options[ "GENERAL" ][ "PDF" ]:
      for i in range( config.params[ "PDF RANGE" ] ):
        prefix = "{}_PDF{}_{}_{}".format( variable, i, config.lumiStr[ args.year ], category )
        if args.verbose: print( ">> Combining PDF SIG histograms" )
        hists[ "CMB" ][ hist_tag( "SIG", "PDF" + i, category ) ] = hists[ "SIG" ][ hist_tag( prefix, groups[ "SIG" ][ "PROCESS" ][0] ) ].Clone( hist_tag( prefix, "SIG" )  )
        for process in groups[ "SIG" ][ "PROCESS" ][1:]: hists[ "CMB" ][ hist_tag( "SIG", "PDF" + i, category ) ].Add( hists[ "SIG" ][ hist_tag( prefix, process ) ] )
        
        for group in groups[ "BKG" ][ "PROCESS" ]:
          if args.verbose: print( ">> Combining PDF {} group histograms".format( group ) )
          hists[ "CMB" ][ hist_tag( group, "PDF" + i, category ) ] = hists[ "BKG" ][ hist_tag( prefix, groups[ "BKG" ][ "PROCESS" ][ group ][0] ) ].Clone( hist_tag( prefix, group ) )
          for process in groups[ "BKG" ][ "PROCESS" ][ group ][1:]: hists[ "CMB" ][ hist_tag( group, "PDF" + i, category ) ].Add( hists[ "BKG" ][ hist_tag( prefix, process ) ] )
          
        for group in groups[ "BKG" ][ "SUPERGROUP" ]:
          if args.verbose: print( ">> Combining PDF {} supergroup histograms".format( group ) )
          hists[ "CMB" ][ hist_tag( group, "PDF" + i, category ) ] = hists[ "BKG" ][ hist_tag( prefix, groups[ "BKG" ][ "SUPERGROUP" ][ group ][0] ) ].Clone( hist_tag( prefix, group ) )
          for process in groups[ "BKG" ][ "SUPERGROUP" ][ group ][1:]: hists[ "CMB" ][ hist_tag( group, "PDF" + i, category ) ].Add( hists[ "BKG" ][ hist_tag( prefix, process ) ] )
                                                                                                                                                     
  for key in hists[ "CMB" ]: hists[ "CMB" ][ key ].SetDirectory(0)
  if ttHFsf != 1 and "TTBB" in groups[ "BKG" ][ "TTBAR_GROUPS" ].keys(): hists = scale_ttbar( hists )
  hists = set_zero( hists )
 
  return hists

def combine_templates( hists, variable, categories ):
  print( ">> Writing Combine templates" )
  combine_name = "template_combine_{}_UL{}.root".format( variable, args.year )
  combine_file = TFile( combine_name, "RECREATE" )
  lumiStr = config.lumiStr[ args.year ]
  for category in categories:
    print( ">> Writing Combine templates for category: {}".format( category ) )
    hists[ "CMB" ][ hist_tag( "DAT", category ) ].Write()
    if args.verbose: print( "    + DAT: {}".format( hist_tag( "DAT", category ) ) )
    
    for process in groups[ "SIG" ][ "PROCESS" ]:
      hists[ "SIG" ][ hist_tag( variable, lumiStr, category, process ) ].Write()
      if args.verbose: print( "    + SIG: {}".format( hist_tag( variable, lumiStr, category, process ) ) )
      if config.options[ "GENERAL" ][ "SYSTEMATICS" ]:
        for syst in config.systematics[ "MC" ] + [ "HD", "UE" ]:
          if syst == "HD" and not config.options[ "GENERAL" ][ "HDAMP" ]: continue
          if syst == "UE" and not config.options[ "GENERAL" ][ "UE" ]: continue
          if syst.upper() == "TOPPT" or syst.upper() == "HT": continue
          for shift in [ "UP", "DN" ]:
            hists[ "SIG" ][ hist_tag( variable, syst.upper() + shift, lumiStr, category, process ) ].Write()
          if args.verbose: print( "    + SIG (SYS): {}".format( hist_tag( variable, syst.upper(), lumiStr, category, process ) ) )
      if config.options[ "GENERAL" ][ "PDF" ]:
        for i in range( config.params[ "PDF RANGE" ] ):
          hists[ "SIG" ][ hist_tag( variable, "PDF" + i, lumiStr, category, process ) ].Write()
        if args.verbose: print( "    + SIG (PDF): {}".format( hist_tag( ariable, "PDF" + i, lumiStr, category, process ) ) )

    bkg_total = sum( [ hists[ "CMB" ][ hist_tag( group, category ) ].Integral() for group in groups[ "BKG" ][ "SUPERGROUP" ] ] )
    for group in groups[ "BKG" ][ "SUPERGROUP" ]:
      if hists[ "CMB" ][ hist_tag( group, category ) ].Integral( 1, hists[ "CMB" ][ hist_tag( group, category ) ].GetXaxis().GetNbins() ) / bkg_total <= config.ratio_threshold:
        if args.verbose: print( "[WARN] {} beneath threshold, excluding from template".format( group ) )
        continue
      hists[ "CMB" ][ hist_tag( group, category ) ].Write()
      if args.verbose: print( "    + BKG SUPERGROUP: {}".format( group ) ) 
      if config.options[ "GENERAL" ][ "SYSTEMATICS" ]:
        for syst in config.systematics + [ "HD", "UE" ]:
          if syst == "HD" and not config.options[ "GENERAL" ][ "HDAMP" ]: continue
          if syst == "UE" and not config.options[ "GENERAL" ][ "UE" ]: continue
          for shift in [ "UP", "DN" ]:
            sysTag = syst.upper() + shift
            hists[ "CMB" ][ hist_tag( group, sysTag, category ) ].Write()
        if args.verbose: print( "    + BKG SUPERGROUP (SYS): {}".format( group ) )
            
      if config.options[ "GENERAL" ][ "PDF" ]:
        for i in range( config.params[ "PDF RANGE" ] ):
          hists[ "CMB" ][ hist_tag( group, "PDF" + i, category ) ].Write()
        if args.verbose: print( "    + BKG SUPERGROUP (PDF): {}".format( group ) )
                                   
    combine_file.Close()
    print( "[DONE] Finished writing Combine templates." )        

   
def make_tables( hists, categories, groups, variable, lumiStr ):
  def initialize():
    yield_table = { "YIELD": {}, "ERROR": {} }
    for category in categories:
      for stat in yield_table: yield_table[ stat ][ category ] = {}
      if config.options[ "GENERAL" ][ "SYSTEMATICS" ]:
        for syst in config.options[ "SYSTEMATICS" ][ "MC" ] + [ "hd", "ue" ]:
          if syst.upper() == "HD" and not config.options[ "GENERAL" ][ "HDAMP" ]: continue
          if syst.upper() == "UE" and not config.options[ "GENERAL" ][ "UE" ]: continue
          for shift in [ "UP", "DN" ]:
            for stat in yield_table: yield_table[ stat ][ hist_tag( syst.upper() + shift, category ) ] = {}
    return yield_table
  
  def fill_yield( tables ):
    def get_yield( table, group, category ):
      for process in group: 
        if args.verbose: ( "   + {}".format( process ) )
        table[ "YIELD" ][ category ][ process ] = hists[ "CMB" ][ hist_tag( variable, lumiStr, category, process ) ].Integral()
        if config.options[ "GENERAL" ][ "SYSTEMATICS" ] and process not in samples.group[ "DATA" ][ "PROCESS" ]:
          for syst in config.options[ "SYSTEMATICS" ][ "MC" ] + [ "hd", "ue" ]:
            if syst.upper() == "HD" and not config.options[ "GENERAL" ][ "HDAMP" ]: continue
            if syst.upper() == "UE" and not config.options[ "GENERAL" ][ "UE" ]: continue
            for shift in [ "UP", "DN" ]:
              for stat in yield_table: yield_table[ stat ][ hist_tag( syst.upper() + shift, category ) ][ process ] = hists[ "CMB" ][ hist_tag( variable, syst.upper() + shift, lumiStr, category, process ) ].Integral()
      return table

    for category in categories:
      if args.verbose: print( ">> Computing yields for DATA histograms" )
      tables = get_yield( tables, groups[ "DATA" ][ "PROCESS" ].keys(), category )
      if args.verbose: print( ">> Computing yields for SIGNAL histograms" )
      tables = get_yield( tables, groups[ "SIGNAL" ][ "PROCESS" ].keys(), category )
      if args.verbose: print( ">> Computing yields for BACKGROUND physics groups" )
      tables = get_yield( tables, groups[ "BACKGROUND" ][ "PROCESS" ].keys(), category )
      if args.verbose: print( ">> Computing yields for BACKGROUND Combine groups" )
      tables = get_yield( tables, groups[ "BACKGROUND" ][ "SUPERGROUP" ].keys(), category )
      
      tables[ "YIELD" ][ hist_tag( variable, category ) ][ "TOTAL BKG" ] = sum( [ hists[ "CMB" ][ hist_tag( variable, lumiStr, category, process ) ].Integral() for process in groups[ "BACKGROUND" ][ "PROCESS" ] ] )
      tables[ "YIELD" ][ hist_tag( variable, category ) ][ "DATA:BKG" ] = tables[ "YIELD" ][ hist_tag( variable, category ) ][ "TOTAL BKG" ]
   
    return tables
  
  def fill_error(tables):
    return tables

  tables = initialize()
  tables = fill_yield( tables )

  return tables

'''  
def theta_templates( hists ):

def summary_templates( hists ):

def print_tables( tables, variable ):
  def nominal_table():
  
  def an_table():
  
  def pas_table( tables ):
  
  def systematic_table( tables ):
  
  def print_table():
'''

def main():
  start_time = time.time()

  template_prefix = config.region_prefix[ args.region ]
  templateDir = os.path.join( os.getcwd(), "{}_UL{}_{}".format( template_prefix, args.year, args.tag ) )
  print( templateDir )
  categories = get_categories( templateDir )
  groups = samples.groups 
  systematics = config.systematics[ "MC" ]
  if args.year in [ "16", "17" ]: systematics += [ "prefire" ]

  for variable in args.variables:
    print( ">> Producing histograms and tables for: {}".format( variable ) )
    hists = load_histograms( variable, templateDir, categories )
    for hist_key in hists:
      if hists[ hist_key ].keys() == []: continue
      print( ">> Modifying {} histograms".format( hist_key ) )
      hists = modify_histograms( hists, hist_key, config.params[ "LUMISCALE" ], config.params[ "REBIN" ] )
    hists = consolidate_histograms( hists, variable, categories, groups )
    #tables = make_tables( hists )
    #theta_templates( hists )
    combine_templates( hists, variable, categories )
    #summary_templates( hists )
    #print_tables( tables, variable )
    del hists
    #del tables

main()
