#!/usr/bin/python

import os, sys, json, time, math, datetime, pickle, itertools
sys.path.append( "../" )
sys.path.append( "../../" )
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

from ROOT import gROOT, TFile, TH1F, Double

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
    if args.verbose: print( ">> Scaling CMB ttbb histograms by a factor of {:.3f}".format( scaleHF ) )
    for category in categories:
      if hist_tag( variable, category, "TTBB" ) not in hists_[ "CMB" ].keys(): continue
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
        for i in range( config.params[ "GENERAL" ][ "PDF RANGE" ] ):
          hists_[ "CMB" ][ hist_tag( variable, category, "PDF" + str(i), "TTBB" ) ].Scale( scaleHF )
          hists_[ "CMB" ][ hist_tag( variable, category, "PDF" + str(i), "TTNOBB" ) ].Scale( scaleLF )
          
    return hists_
    
  def set_zero( hists_, categories, zero ):
    for hist_key in hists_:
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
      i = 0
      while hist_tag( prefix, groups[ "BKG" ][ "PROCESS" ][ group ][i] ) not in hists[ "BKG" ].keys():
        print( "[WARN] {} is empty, skipping...".format( groups[ "BKG" ][ "PROCESS" ][ group ][i] ) )
        i += 1
      hists[ "CMB" ][ hist_tag( group, category ) ] = hists[ "BKG" ][ hist_tag( prefix, groups[ "BKG" ][ "PROCESS" ][ group ][i] ) ].Clone( hist_tag( prefix, group ) )
      for process in groups[ "BKG" ][ "PROCESS" ][ group ][i:]: 
        if hist_tag( prefix, process ) not in hists[ "BKG" ].keys(): 
          print( "[WARN] {} is empty, skipping...".format( process ) )
          continue
        hists[ "CMB" ][ hist_tag( group, category ) ].Add( hists[ "BKG" ][ hist_tag( prefix, process ) ] )
    
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
          for process in groups[ "SIG" ][ "PROCESS" ][1:]: hists[ "CMB" ][ hist_tag( "SIG", sysTag, category ) ].Add( hists[ "SIG" ][ hist_tag( prefix, process ) ] )
          if args.verbose: print( ">> Combining {} BKG group histograms".format( syst.upper() + shift ) )
          for group in groups[ "BKG" ][ "PROCESS" ]:
            hists[ "CMB" ][ hist_tag( group, sysTag, category ) ] = hists[ "BKG" ][ hist_tag( prefix, groups[ "BKG" ][ "PROCESS" ][ group ][0] ) ].Clone( hist_tag( prefix, group ) )
            for process in groups[ "BKG" ][ "PROCESS" ][ group ][1:]: hists[ "CMB" ][ hist_tag( group, sysTag, category ) ].Add( hists[ "BKG" ][ hist_tag( prefix, process ) ] )
          
          for group in groups[ "BKG" ][ "SUPERGROUP" ]:
            hists[ "CMB" ][ hist_tag( group, sysTag, category ) ] = hists[ "BKG" ][ hist_tag( prefix, groups[ "BKG" ][ "SUPERGROUP" ][ group ][0] ) ].Clone( hist_tag( prefix, group ) )
            for process in groups[ "BKG" ][ "SUPERGROUP" ][ group ][1:]: hists[ "CMB" ][ hist_tag( group, sysTag, category ) ].Add( hists[ "BKG" ][ hist_tag( prefix, process ) ] )
     
    if config.options[ "GENERAL" ][ "PDF" ]:
      for i in range( config.params[ "GENERAL" ][ "PDF RANGE" ] ):
        prefix = "{}_PDF{}_{}_{}".format( variable, i, config.lumiStr[ args.year ], category )
        if args.verbose: print( ">> Combining PDF SIG histograms" )
        hists[ "CMB" ][ hist_tag( "SIG", "PDF" + str(i), category ) ] = hists[ "SIG" ][ hist_tag( prefix, groups[ "SIG" ][ "PROCESS" ][0] ) ].Clone( hist_tag( prefix, "SIG" )  )
        for process in groups[ "SIG" ][ "PROCESS" ][1:]: hists[ "CMB" ][ hist_tag( "SIG", "PDF" + str(i), category ) ].Add( hists[ "SIG" ][ hist_tag( prefix, process ) ] )
        
        for group in groups[ "BKG" ][ "PROCESS" ]:
          if args.verbose: print( ">> Combining PDF {} group histograms".format( group ) )
          hists[ "CMB" ][ hist_tag( group, "PDF" + str(i), category ) ] = hists[ "BKG" ][ hist_tag( prefix, groups[ "BKG" ][ "PROCESS" ][ group ][0] ) ].Clone( hist_tag( prefix, group ) )
          for process in groups[ "BKG" ][ "PROCESS" ][ group ][1:]: hists[ "CMB" ][ hist_tag( group, "PDF" + str(i), category ) ].Add( hists[ "BKG" ][ hist_tag( prefix, process ) ] )
          
        for group in groups[ "BKG" ][ "SUPERGROUP" ]:
          if args.verbose: print( ">> Combining PDF {} supergroup histograms".format( group ) )
          hists[ "CMB" ][ hist_tag( group, "PDF" + str(i), category ) ] = hists[ "BKG" ][ hist_tag( prefix, groups[ "BKG" ][ "SUPERGROUP" ][ group ][0] ) ].Clone( hist_tag( prefix, group ) )
          for process in groups[ "BKG" ][ "SUPERGROUP" ][ group ][1:]: hists[ "CMB" ][ hist_tag( group, "PDF" + str(i), category ) ].Add( hists[ "BKG" ][ hist_tag( prefix, process ) ] )
                                                                                                                                                     
  for key in hists[ "CMB" ]: hists[ "CMB" ][ key ].SetDirectory(0)
  if config.params[ "HISTS" ][ "TTHFSF" ] != 1 and "TTBB" in groups[ "BKG" ][ "TTBAR_GROUPS" ].keys(): hists = scale_ttbar( hists, config.params[ "HISTS" ][ "TTHFSF" ], config.params[ "HISTS" ][ "TTLFSF" ] )
  hists = set_zero( hists, categories, config.params[ "GENERAL" ][ "ZERO" ] )
 
  return hists

def combine_templates( hists, variable, categories, groups, templateDir ):
  print( ">> Writing Combine templates" )
  combine_name = "{}/template_combine_{}_UL{}.root".format( templateDir, variable, args.year )
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
          if args.verbose: print( "    + SIG (SYS): {}".format( process ) )
          if syst == "HD" and not config.options[ "GENERAL" ][ "HDAMP" ]: continue
          if syst == "UE" and not config.options[ "GENERAL" ][ "UE" ]: continue
          if syst.upper() == "TOPPT" or syst.upper() == "HT": continue
          for shift in [ "UP", "DN" ]:
            hists[ "SIG" ][ hist_tag( variable, syst.upper() + shift, lumiStr, category, process ) ].Write()
      if config.options[ "GENERAL" ][ "PDF" ]:
        if args.verbose: print( "    + SIG (PDF): {}".format( process ) )
        for i in range( config.params[ "GENERAL" ][ "PDF RANGE" ] ):
          hists[ "SIG" ][ hist_tag( variable, "PDF" + str(i), lumiStr, category, process ) ].Write()

    yield_total = sum( [ hists[ "CMB" ][ hist_tag( group, category ) ].Integral() for group in groups[ "BKG" ][ "SUPERGROUP" ] ] )
    for group in groups[ "BKG" ][ "SUPERGROUP" ]:
      scale_group = False
      error_group = Double(0)
      yield_group = hists[ "CMB" ][ hist_tag( group, category ) ].IntegralAndError( 1, hists[ "CMB" ][ hist_tag( group, category ) ].GetXaxis().GetNbins(), error_group )
      if ( yield_group / yield_total <= config.params[ "HISTS" ][ "MIN BKG YIELD" ] or error_group / yield_group >= config.params[ "HISTS" ][ "MAX BKG ERROR" ] ):
        scale_group = True
        if args.verbose and yield_group / yield_total <= config.params[ "HISTS" ][ "MIN BKG YIELD" ]: print( "[WARN] {} beneath yield threshold, scaling by {:.1e} in Combine template".format( group, config.params[ "GENERAL" ][ "ZERO" ] ) )
        if args.verbose and error_group / yield_group >= config.params[ "HISTS" ][ "MAX BKG ERROR" ]: print( "[WARN] {} above error threshold, scaling by {:.1e} in Combine template".format( group, config.params[ "GENERAL" ][ "ZERO" ] ) )
        hists[ "CMB" ][ hist_tag( group, category ) ].Scale( config.params[ "GENERAL" ][ "ZERO" ] )
      hists[ "CMB" ][ hist_tag( group, category ) ].Write()
      if args.verbose: print( "    + BKG SUPERGROUP: {}".format( group ) ) 
      if config.options[ "GENERAL" ][ "SYSTEMATICS" ]:
        for syst in config.systematics[ "MC" ] + [ "HD", "UE" ]:
          if syst == "HD" and not config.options[ "GENERAL" ][ "HDAMP" ]: continue
          if syst == "UE" and not config.options[ "GENERAL" ][ "UE" ]: continue
          for shift in [ "UP", "DN" ]:
            sysTag = syst.upper() + shift
            if scale_group:
              hists[ "CMB" ][ hist_tag( group, sysTag, category ) ].Scale( config.params[ "GENERAL" ][ "ZERO" ] )
            hists[ "CMB" ][ hist_tag( group, sysTag, category ) ].Write()
        if args.verbose: print( "    + BKG SUPERGROUP (SYS): {}".format( group ) )
            
      if config.options[ "GENERAL" ][ "PDF" ]:
        for i in range( config.params[ "GENERAL" ][ "PDF RANGE" ] ):
          if scale_group:
            hists[ "CMB" ][ hist_tag( group, sysTag, category ) ].Scale( config.params[ "GENERAL" ][ "ZERO" ] )
          hists[ "CMB" ][ hist_tag( group, "PDF" + str(i), category ) ].Write()
        if args.verbose: print( "    + BKG SUPERGROUP (PDF): {}".format( group ) )
                                   
  combine_file.Close()
  print( "[DONE] Finished writing Combine templates." )        

   
def make_tables( hists, categories, groups, variable, templateDir, lumiStr ):
  def initialize():
    yield_table = { "YIELD": {}, "ERROR": {} }
    for category in categories:
      for stat in yield_table: yield_table[ stat ][ category ] = {}
      if config.options[ "GENERAL" ][ "SYSTEMATICS" ]:
        for syst in config.systematics[ "MC" ] + [ "hd", "ue" ]:
          if syst.upper() == "HD" and not config.options[ "GENERAL" ][ "HDAMP" ]: continue
          if syst.upper() == "UE" and not config.options[ "GENERAL" ][ "UE" ]: continue
          for shift in [ "UP", "DN" ]:
            for stat in yield_table: yield_table[ stat ][ hist_tag( syst.upper() + shift, category ) ] = {}
    return yield_table
  
  def fill_yield( tables ):
    def get_yield( table, group, category ):
      for process in group: 
        if args.verbose: ( "   + {}".format( process ) )
        if process in groups[ "SIG" ][ "PROCESS" ]:
          table[ "YIELD" ][ category ][ process ] = hists[ "SIG" ][ hist_tag( variable, lumiStr, category, process ) ].Integral()
        else:
          table[ "YIELD" ][ category ][ process ] = hists[ "CMB" ][ hist_tag( process, category ) ].Integral()
        if config.options[ "GENERAL" ][ "SYSTEMATICS" ] and process not in [ "DAT" ]:
          for syst in config.systematics[ "MC" ] + [ "hd", "ue" ]:
            if syst.upper() == "HD" and not config.options[ "GENERAL" ][ "HDAMP" ]: continue
            if syst.upper() == "UE" and not config.options[ "GENERAL" ][ "UE" ]: continue
            for shift in [ "UP", "DN" ]:
              for stat in table: 
                if process in groups[ "SIG" ][ "PROCESS" ]:
                  table[ stat ][ hist_tag( syst.upper() + shift, category ) ][ process ] = hists[ "SIG" ][ hist_tag( variable, lumiStr, category, process ) ]
                else:
                  table[ stat ][ hist_tag( syst.upper() + shift, category ) ][ process ] = hists[ "CMB" ][ hist_tag( process, syst.upper() + shift, category ) ].Integral()
      return table

    for category in categories:
      if args.verbose: print( ">> Computing yields for DATA histograms" )
      tables = get_yield( tables, [ "DAT" ], category )
      if args.verbose: print( ">> Computing yields for SIGNAL histograms" )
      tables = get_yield( tables, groups[ "SIG" ][ "PROCESS" ], category )
      if args.verbose: print( ">> Computing yields for BACKGROUND physics groups" )
      tables = get_yield( tables, groups[ "BKG" ][ "PROCESS" ].keys(), category )
      if args.verbose: print( ">> Computing yields for BACKGROUND Combine groups" )
      tables = get_yield( tables, groups[ "BKG" ][ "SUPERGROUP" ].keys(), category )
      
      tables[ "YIELD" ][ category ][ "TOTAL BKG" ] = sum( [ hists[ "CMB" ][ hist_tag( process, category ) ].Integral() for process in groups[ "BKG" ][ "PROCESS" ] ] )
      tables[ "YIELD" ][ category ][ "DATA:BKG" ] = tables[ "YIELD" ][ category ][ "DAT" ] / ( tables[ "YIELD" ][ category ][ "TOTAL BKG" ] + config.params[ "GENERAL" ][ "ZERO" ] )
   
    return tables
  
  def fill_error( tables ):
    def get_error( table, group, category ):
      for process in group:
        if args.verbose: print( "   + {}".format( process ) )
        table[ "ERROR" ][ category ][ process ] = 0
        if process in groups[ "SIG" ][ "PROCESS" ]:
          for i in range( 1, hists[ "SIG" ][ hist_tag( variable, lumiStr, category, groups[ "SIG" ][ "PROCESS" ][0] ) ].GetXaxis().GetNbins() + 1 ):
            table[ "ERROR" ][ category ][ process ] += hists[ "SIG" ][ hist_tag( variable, lumiStr, category, process ) ].GetBinError(i)**2
        else:
          for i in range( 1, hists[ "CMB" ][ hist_tag( list( group )[0], category ) ].GetXaxis().GetNbins() + 1 ):
            table[ "ERROR" ][ category ][ process ] += hists[ "CMB" ][ hist_tag( process, category ) ].GetBinError(i)**2
        table[ "ERROR" ][ category ][ process ] = math.sqrt( table[ "ERROR" ][ category ][ process ] )
      return table

    for category in categories:
      if args.verbose: print( ">> Computing errors for DATA histograms" )
      tables = get_error( tables, [ "DAT" ], category )
      if args.verbose: print( ">> Computing errors for SIGNAL histograms" )
      tables = get_error( tables, groups[ "SIG" ][ "PROCESS" ], category )
      if args.verbose: print( ">> Computing errors for BACKGROUND physics groups" )
      tables = get_error( tables, groups[ "BKG" ][ "PROCESS" ].keys(), category )
      if args.verbose: print( ">> Computing errors for BACKGROUND Combine groups" )
      tables = get_error( tables, groups[ "BKG" ][ "SUPERGROUP" ].keys(), category )
     
      tables[ "ERROR" ][ category ][ "TOTAL BKG" ] = 0
      tables[ "ERROR" ][ category ][ "DATA:BKG" ] = 0
      for i in range( 1, hists[ "CMB" ][ hist_tag( list( groups[ "BKG" ][ "SUPERGROUP" ].keys() )[0], category ) ].GetXaxis().GetNbins() + 1 ):
        for group in groups[ "BKG" ][ "SUPERGROUP" ]:
          tables[ "ERROR" ][ category ][ "TOTAL BKG" ] += hists[ "CMB" ][ hist_tag( group, category ) ].GetBinError(i)**2
      tables[ "ERROR" ][ category ][ "TOTAL BKG" ] = math.sqrt( tables[ "ERROR" ][ category ][ "TOTAL BKG" ] ) 
      yield_d = tables[ "YIELD" ][ category ][ "DAT" ] 
      yield_b = tables[ "YIELD" ][ category ][ "TOTAL BKG" ]
      error_d = math.sqrt( yield_d )
      error_b = math.sqrt( yield_b )
      tables[ "ERROR" ][ category ][ "DATA:BKG" ] = math.sqrt( ( error_d / yield_b )**2 + ( yield_d * error_d / yield_b**2 )**2 )      
      tables[ "ERROR" ][ category ][ "DATA:BKG" ] = math.sqrt( tables[ "ERROR" ][ category ][ "DATA:BKG" ] )

    return tables

  tables = initialize()
  tables = fill_yield( tables )
  tables = fill_error( tables )

  return tables

def print_tables( tables, categories, groups, variable, templateDir ):
  def yield_table():
    def format_section( table, title, columns, precision ):
      pm = "{:." + precision + "f} pm {:." + precision + "f}"
      table.append( [ "YIELD:", title ] )
      table.append( [ "CATEGORY" ] + columns )
      sum_row = [ "TOTAL" ]
      process_stat = {
        key: {
          process: 0 for process in columns
        } for key in [ "YIELD", "ERROR" ]
      }
      for category in sorted( categories ):
        row = [ category ]
        for process in columns:
          row.append( pm.format(
            tables[ "YIELD" ][ category ][ process ],
            tables[ "ERROR" ][ category ][ process ]
          ) )
          process_stat[ "YIELD" ][ process ] += tables[ "YIELD" ][ category ][ process ]
          process_stat[ "ERROR" ][ process ] += tables[ "ERROR" ][ category ][ process ]**2
        table.append( row )
      for process in columns:
        process_stat[ "ERROR" ][ process ] = -1 if ":" in process else math.sqrt( process_stat[ "ERROR" ][ process ] )
        process_stat[ "YIELD" ][ process ] = -1 if ":" in process else process_stat[ "YIELD" ][ process ]
        sum_row.append( pm.format( 
          process_stat[ "YIELD" ][ process ],
          process_stat[ "ERROR" ][ process ]
        ) )
      table.append( sum_row )
      table.append( [ "" ] )
      table.append( [ "" ] )
      return table


    print( ">> Printing out the nominal table" )
    table = []

    table = format_section( table, "PHYSICS PROCESS", [ "DAT" ] + list( groups[ "BKG" ][ "PROCESS" ].keys() ), "2" )
    table = format_section( table, "COMBINE ANALYSIS", [ "DAT" ] + list( groups[ "BKG" ][ "SUPERGROUP" ].keys() ), "2" )
    table = format_section( table, "SIGNAL", groups[ "SIG" ][ "PROCESS" ], "3" )
    table = format_section( table, "SUMMARY", [ "TOTAL BKG", "DATA:BKG" ], "4" )

    return table

  def an_table():
    pass
  def pas_table( tables ):
    pass
  def systematic_table( tables ):
    pass
  def print_table( table, section_header, file_name ):
    def get_max_width( table, index ):
      max_width = 0
      for row in table:
        try:
          n = len( format( row[ index ] ) )
          if n > max_width: max_width = n
        except:
          pass
      return max_width

    def print_section( section ):
      column_padding = []
      max_columns = 0
      for row in section: 
        if len( row ) > max_columns: max_columns = len( row )
      for i in range( max_columns ): column_padding.append( get_max_width( section, i ) )
      for row in section:
        print >> file_name, format( row[0] ).ljust( column_padding[0] + 1 ),
        for i in range( 1, len( row ) ):
          column = format( row[i] ).ljust( column_padding[i] + 2 )
          print >> file_name, column,
        print >> file_name

    def get_section( table ):
      sections = []
      section = []
      for i, row in enumerate( table ):
        if section_header in row or i == len( table ) - 1: 
          if i != 0: sections.append( section )
          section = [ row ]
        else: section.append( row )
      return sections

    print( ">> Writing out {} table to: {}".format( section_header, file_name ) )
    for section in get_section( table ): print_section( section )    


  if not os.path.exists( os.path.join( templateDir, "tables/" ) ): os.system( "mkdir -vp {}".format( os.path.join( templateDir, "tables/" ) ) )
  print_table( yield_table(), "YIELD:", open( os.path.join( templateDir, "tables/", "yield_table.txt" ), "w" ) )


'''
def theta_templates( hists ):

def summary_templates( hists ):

'''

def main():
  start_time = time.time()

  template_prefix = config.region_prefix[ args.region ]
  templateDir = os.path.join( os.getcwd(), "{}_UL{}_{}".format( template_prefix, args.year, args.tag ) )
  categories = get_categories( templateDir )
  groups = samples.groups 
  systematics = config.systematics[ "MC" ]
  #if args.year in [ "16", "17" ]: systematics += [ "prefire" ]

  for variable in args.variables:
    print( ">> Producing histograms and tables for: {}".format( variable ) )
    hists = load_histograms( variable, templateDir, categories )
    for hist_key in hists:
      if hists[ hist_key ].keys() == []: continue
      print( ">> Modifying {} histograms".format( hist_key ) )
      hists = modify_histograms( hists, hist_key, config.params[ "HISTS" ][ "LUMISCALE" ], config.params[ "HISTS" ][ "REBIN" ] )
    hists = consolidate_histograms( hists, variable, categories, groups )
    #theta_templates( hists )
    combine_templates( hists, variable, categories, groups, templateDir )
    #summary_templates( hists )
    tables = make_tables( hists, categories, groups, variable, templateDir, config.lumiStr[ args.year ] )
    print_tables( tables, categories, groups, variable, templateDir )
    del hists
    #del tables

main()
