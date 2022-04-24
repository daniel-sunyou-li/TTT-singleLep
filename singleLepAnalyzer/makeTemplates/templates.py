#!/usr/bin/python

import os, sys, json, time, math, datetime, pickle, itertools
sys.path.append( "../" )
sys.path.append( "../../" )
from argparse import ArgumentParser
import numpy as np
from array import array
from utils import hist_parse, hist_tag
import config

parser = ArgumentParser()
parser.add_argument( "-y", "--year",   required = True )
parser.add_argument( "-t", "--tag", required = True )
parser.add_argument( "-v", "--variables", nargs = "+", required = True )
parser.add_argument( "-r", "--region", required = True )
parser.add_argument( "--verbose", action = "store_true" )
args = parser.parse_args()

# parse options
doABCDNN = True if config.options[ "GENERAL" ][ "ABCDNN" ]  else False
if args.region not in list( config.region_prefix.keys() ): quit( "[ERR] Invalid region argument used. Quiting..." )
if args.year == "16APV":
  import samplesUL16APV as samples
elif args.year == "16":
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
  
def load_histograms( variable, templateDir, categories ): 
  print( "[START] Loading histograms from {} for {}".format( templateDir, variable ) )
  sTime = time.time()
  hists =  {}
  
  for category in categories:
    if args.verbose: print( "  >> Loading category: {}".format( category ) )
    categoryDir = os.path.join( templateDir, category )
    hist_keys = [ filename.split( "_" )[0] for filename in os.listdir( categoryDir ) if filename.endswith( ".pkl" ) ]
    for hist_key in hist_keys:
      if hist_key == "TEST" and not config.options[ "GENERAL" ][ "TEST" ]: continue
      if hist_key not in hists: hists[ hist_key ] = {}
      hists[ hist_key ].update( pickle.load( open( os.path.join( categoryDir, "{}_{}.pkl".format( hist_key, variable ) ), "rb" ) ) ) 
  count = 0
  for hist_key in hists:
    count += len( hists[ hist_key ].keys() )

  print( "[DONE] Finished loading {} histograms in {:.2f} minutes".format( count, ( time.time() - sTime ) / 60 ) )
  return hists
  
def clean_histograms( hists, hist_key, scale, rebin ):
  def scale_luminosity( hists_, hist_key, scale ):
    print( "  [START] Scaling {} MC luminosity by factor: {}".format( hist_key, scale ) )
    count = 0
    for hist_name in hists_[ hist_key ]:
      parse = hist_parse( hist_name, samples )
      if parse[ "GROUP" ] in [ "BKG", "SIG" ]:
        if args.verbose: print( "  + {}".format( hist_name ) )
        hists_[ hist_name ].Scale( scale )
        count += 1
    print( "  [DONE] {} histograms scaled".format( count ) )
    return hists_
  
  def rebinning( hists_, hist_key, rebin ):
    print( "  [START] Re-binning {} histogram bins by: {}".format( hist_key, rebin ) )
    count = 0
    for hist_name in hists_[ hist_key ]:
      if args.verbose: print( "  + {}".format( hist_name ) )
      hists_[ hist_key ][ hist_name ].Rebin( rebin )
      count += 1
    print( "  [DONE] Re-binned {} histograms".format( count ) )
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
      
    print( "  [START] Correcting negative {} histogram bins".format( hist_key ) )
    count = 0
    for hist_name in hists_[ hist_key ]:
      parse = hist_parse( hist_name, samples )
      if parse[ "GROUP" ] in [ "SIG", "BKG" ]:
        hists_[ hist_key ][ hist_name ], change = function( hists_[ hist_key ][ hist_name ] )
        if change: 
          count += 1
    print( "  [DONE] Corrected {} negative bins".format( count ) )
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
    
    if args.verbose: print( "  [START] Correcting {} over/under-flow bins".format( hist_key ) )
    for hist_name in hists_[ hist_key ]:
      hists_[ hist_key ][ hist_name ] = overflow( hists_[ hist_key ][ hist_name ] )
      hists_[ hist_key ][ hist_name ] = underflow( hists_[ hist_key ][ hist_name ] )
    
    print( "  [DONE]" )
    return hists_
 
  sTime = time.time()
  print( "[START] Cleaning {} histograms".format( hist_key ) )
  if scale != 1.: hists = scale_luminosity( hists, hist_key, scale )
  if rebin > 0: hists = rebinning( hists, hist_key, rebin )
  hists = negative_correction( hists, hist_key )
  hists = bin_correction( hists, hist_key )
  print( "[DONE] Finished cleaning histograms in {:.2f} minutes".format( ( time.time() - sTime ) / 60. ) )
  return hists
  
def combine_histograms( hists, variable, categories, groups, doABCDNN ):
  def scale_ttbar( hists_, scaleHF, scaleLF ):
    print( "  [START] Scaling CMB ttbb histograms by a factor of {:.3f}".format( scaleHF ) )
    count = 0
    for category in sorted( categories ):
      if hist_tag( "TTBB", category ) not in hists_[ "CMB" ].keys(): continue
      N = {
        "TTBB": hists[ "CMB" ][ hist_tag( "TTBB", category ) ].Integral(),
        "TTNOBB": hists[ "CMB" ][ hist_tag( "TTNOBB", category ) ].Integral()
      }
      if scaleLF < 0:
        try: scaleLF = max( 0, 1. + ( 1. - scaleHF ) * ( N[ "TTBB" ] / N[ "TTNOBB" ] ) )
        except ZeroDivisionError: scaleLF = 1.
      if args.verbose: print( "     + {} ({:.3f}): {} --> {}:".format( category, scaleLF, N[ "TTNOBB" ], N[ "TTNOBB" ] * scaleLF ) )

      hists_[ "CMB" ][ hist_tag( "TTBB", category ) ].Scale( scaleHF )
      hists_[ "CMB" ][ hist_tag( "TTNOBB", category ) ].Scale( scaleLF )
      count += 1

      if config.options[ "GENERAL" ][ "SYSTEMATICS" ]:
        for syst in config.systematics[ "MC" ].keys():
          if not config.systematics[ "MC" ][ syst ] or syst == "ABCDNN": continue
          if syst.upper() == "HD" and not config.options[ "GENERAL" ][ "HDAMP" ]: continue
          if syst.upper() == "UE" and not config.options[ "GENERAL" ][ "UE" ]: continue
          for shift in [ "UP", "DN" ]:
            hists_[ "CMB" ][ hist_tag( "TTBB", category, syst.upper() + shift ) ].Scale( scaleHF )
            hists_[ "CMB" ][ hist_tag( "TTNOBB", category, syst.upper() + shift ) ].Scale( scaleLF )
            count += 1
      if config.options[ "GENERAL" ][ "PDF" ]:
        for i in range( config.params[ "GENERAL" ][ "PDF RANGE" ] ):
          hists_[ "CMB" ][ hist_tag( "TTBB", category, "PDF" + str(i) ) ].Scale( scaleHF )
          hists_[ "CMB" ][ hist_tag( "TTNOBB", category, "PDF" + str(i) ) ].Scale( scaleLF )
          count += 1
    print( "  [DONE] Scaled {} ttbb (ttnobb) histograms by {:.3f}".format( count, scaleHF ) )
    return hists_
    
  def set_zero( hists_, categories, zero ):
    print( "  [START] Setting 0 bins to be non-trivial ({:.3e}) in histograms".format( zero ) )
    count = 0
    for hist_key in hists_:
      for hist_name in hists_[ hist_key ]:
        parse = hist_parse( hist_name, samples )
        if parse[ "GROUP" ] == "DAT": continue
        if hists_[ hist_key ][ hist_name ].Integral() == 0: 
          hists_[ hist_key ][ hist_name ].SetBinContent( 1, zero )
          count += 1
    print( "  [DONE] Set {} 0 bins to be non-trivial".format( count ) )
    return hists_

  print( "[START] Consolidating histograms by Higgs Combine grouping" )
  sTime = time.time()
  count = {}
  hists[ "CMB" ] = {}
  for hist_key in hists:
    if hist_key == "CMB": continue
    print( "  + {}".format( hist_key ) )
    count[ hist_key ] = 0
    for hist_name in sorted( hists[ hist_key ].keys() ):
      parse = hist_parse( hist_name, samples )
      if doABCDNN and "ABCDNN" in hist_name and hist_key == "BKG": 
        if parse[ "PROCESS" ] in config.params[ "ABCDNN" ][ "GROUPS" ]:
          if parse[ "IS SYST" ] and ( parse[ "SYST" ].upper() in [ "ABCDNN", "MUR", "MUF", "MURFCORRD", "FSR", "ISR" ] or "PDF" in parse[ "SYST" ] ):
            try: hists[ "CMB" ][ hist_tag( "ABCDNN", parse[ "CATEGORY" ], parse[ "SYST" ] + parse[ "SHIFT" ] ) ].Add( hists[ hist_key ][ hist_name ] )
            except: hists[ "CMB" ][ hist_tag( "ABCDNN", parse[ "CATEGORY" ], parse[ "SYST" ] + parse[ "SHIFT" ] ) ] = hists[ hist_key ][ hist_name ].Clone( hist_tag( "ABCDNN", parse[ "CATEGORY" ], parse[ "SYST" ] + parse[ "SHIFT" ] ) )
          elif not parse[ "IS SYST" ]:
            print( ">> Including {} > {} for ABCDNN".format( hist_key, hist_name ) )
            try: hists[ "CMB" ][ hist_tag( "ABCDNN", parse[ "CATEGORY" ] ) ].Add( hists[ hist_key ][ hist_name ] )
            except: hists[ "CMB" ][ hist_tag( "ABCDNN", parse[ "CATEGORY" ] ) ] = hists[ hist_key ][ hist_name ].Clone( hist_tag( "ABCDNN", parse[ "CATEGORY" ] ) )
        else:
          continue
      if parse[ "IS SYST" ]:
        try: hists[ "CMB" ][ hist_tag( parse[ "COMBINE" ], parse[ "CATEGORY" ], parse[ "SYST" ] + parse[ "SHIFT" ] ) ].Add( hists[ hist_key ][ hist_name ] )
        except: hists[ "CMB" ][ hist_tag( parse[ "COMBINE" ], parse[ "CATEGORY" ], parse[ "SYST" ] + parse[ "SHIFT" ] ) ] = hists[ hist_key ][ hist_name ].Clone( hist_tag( parse[ "COMBINE" ], parse[ "CATEGORY" ], parse[ "SYST" ] + parse[ "SHIFT" ] ) )
      else:
        try: hists[ "CMB" ][ hist_tag( parse[ "COMBINE" ], parse[ "CATEGORY" ] ) ].Add( hists[ hist_key ][ hist_name ] )
        except: hists[ "CMB" ][ hist_tag( parse[ "COMBINE" ], parse[ "CATEGORY" ] ) ] = hists[ hist_key ][ hist_name ].Clone( hist_tag( parse[ "COMBINE" ], parse[ "CATEGORY" ] ) )
      count[ hist_key ] += 1

  for key in hists[ "CMB" ]: hists[ "CMB" ][ key ].SetDirectory(0)
  if config.params[ "HISTS" ][ "TTHFSF" ] != 1: hists = scale_ttbar( hists, config.params[ "HISTS" ][ "TTHFSF" ], config.params[ "HISTS" ][ "TTLFSF" ] )
  hists = set_zero( hists, categories, config.params[ "GENERAL" ][ "ZERO" ] )
  print( "[DONE] Consolidated histograms into Combine groupings in {:.2f} minutes:".format( ( time.time() - sTime ) / 60. ) )
  for key in count:
    print( "   + {}: {}".format( key, count[ key ] ) )
  return hists

def write_combine( hists, variable, categories, groups, templateDir, doABCDNN ):
  print( "[START] Writing Combine templates" )
  sTime = time.time()
  combine_name = "{}/template_combine_{}_UL{}.root".format( templateDir, variable, args.year )
  combine_file = TFile( combine_name, "RECREATE" )

  for category in categories:
    print( ">> Writing category: {}".format( category ) )
    hists[ "CMB" ][ hist_tag( "data_obs", category ) ].Write()
    if args.verbose: print( "   + DAT > {}: {}".format( hist_tag( "data_obs", category ), hists[ "CMB" ][ hist_tag( "data_obs", category ) ].Integral() ) )

    for process in groups[ "SIG" ][ "PROCESS" ]:
      hists[ "CMB" ][ hist_tag( process, category ) ].Write()
      if args.verbose: print( "   + SIG > {}: {}".format( hist_tag( process, category ), hists[ "CMB" ][ hist_tag( process, category ) ].Integral() ) )
      if config.options[ "GENERAL" ][ "SYSTEMATICS" ]:
        if args.verbose: print( "   + SIG (SYST): {}".format( hist_tag( process, category ) ) )
        for syst in config.systematics[ "MC" ].keys():
          if not config.systematics[ "MC" ][ syst ] or syst == "ABCDNN": continue
          if syst == "HD" and not config.options[ "GENERAL" ][ "HDAMP" ]: continue
          if syst == "UE" and not config.options[ "GENERAL" ][ "UE" ]: continue
          for shift in [ "UP", "DN" ]:
            hists[ "CMB" ][ hist_tag( process, category, syst.upper() + shift ) ].Write()
      if config.options[ "GENERAL" ][ "PDF" ]:
        if args.verbose: print( "   + SIG (PDF): {}".format( hist_tag( process, category ) ) )
        for i in range( config.params[ "GENERAL" ][ "PDF RANGE" ] ):
          hists[ "CMB" ][ hist_tag( process, category, "PDF" + str(i) ) ].Write()

    yield_total = sum( [ hists[ "CMB" ][ hist_tag( group, category ) ].Integral() for group in groups[ "BKG" ][ "SUPERGROUP" ] if hist_tag( group, category ) in hists[ "CMB" ].keys() ] )
    for group in groups[ "BKG" ][ "SUPERGROUP" ]:
      scale_group = False
      error_group = Double(0)
      if hist_tag( group, category ) not in hists[ "CMB" ].keys(): continue
      yield_group = hists[ "CMB" ][ hist_tag( group, category ) ].IntegralAndError( 1, hists[ "CMB" ][ hist_tag( group, category ) ].GetXaxis().GetNbins(), error_group )
      if ( yield_group / yield_total <= config.params[ "HISTS" ][ "MIN BKG YIELD" ] or error_group / yield_group >= config.params[ "HISTS" ][ "MAX BKG ERROR" ] ):
        scale_group = True
        if args.verbose and yield_group / yield_total <= config.params[ "HISTS" ][ "MIN BKG YIELD" ]: print( "[WARN] {} beneath yield threshold, scaling by {:.1e} in Combine template".format( group, config.params[ "GENERAL" ][ "ZERO" ] ) )
        if args.verbose and error_group / yield_group >= config.params[ "HISTS" ][ "MAX BKG ERROR" ]: print( "[WARN] {} above error threshold, scaling by {:.1e} in Combine template".format( group, config.params[ "GENERAL" ][ "ZERO" ] ) )
        hists[ "CMB" ][ hist_tag( group, category ) ].Scale( config.params[ "GENERAL" ][ "ZERO" ] )
      hists[ "CMB" ][ hist_tag( group, category ) ].Write()
      if args.verbose: print( "   + BKG SUPERGROUP > {}: {}".format( hist_tag( group, category ), hists[ "CMB" ][ hist_tag( group, category ) ].Integral() ) ) 
      if config.options[ "GENERAL" ][ "SYSTEMATICS" ]:
        for syst in config.systematics[ "MC" ].keys():
          if syst.upper() == "HD" and not config.options[ "GENERAL" ][ "HDAMP" ]: continue
          if syst.upper() == "UE" and not config.options[ "GENERAL" ][ "UE" ]: continue
          if syst == "ABCDNN": continue
          for shift in [ "UP", "DN" ]:
            sysTag = syst.upper() + shift
            if scale_group:
              hists[ "CMB" ][ hist_tag( group, category, sysTag ) ].Scale( config.params[ "GENERAL" ][ "ZERO" ] )
            hists[ "CMB" ][ hist_tag( group, category, sysTag ) ].Write()
        if args.verbose: print( "    + BKG SUPERGROUP (SYS): {}".format( group ) )
            
      if config.options[ "GENERAL" ][ "PDF" ]:
        for i in range( config.params[ "GENERAL" ][ "PDF RANGE" ] ):
          if scale_group:
            hists[ "CMB" ][ hist_tag( group, category, "PDF" + str(i) ) ].Scale( config.params[ "GENERAL" ][ "ZERO" ] )
          hists[ "CMB" ][ hist_tag( group, category, "PDF" + str(i) ) ].Write()
        if args.verbose: print( "    + BKG SUPERGROUP (PDF): {}".format( group ) )
  
    if doABCDNN and hist_parse( category, samples )[ "ABCDNN" ]:
      hists[ "CMB" ][ hist_tag( "ABCDNN", category ) ].Write()
      if args.verbose: print( "   + BKG SUPERGROUP > {}: {}".format( hist_tag( "ABCDNN", category ), hists[ "CMB" ][ hist_tag( "ABCDNN", category ) ].Integral() ) )
      if config.systematics[ "MC" ][ "ABCDNN" ]:
        hists[ "CMB" ][ hist_tag( "ABCDNN", category, "ABCDNNUP" ) ].Write()
        hists[ "CMB" ][ hist_tag( "ABCDNN", category, "ABCDNNDN" ) ].Write()

  combine_file.Close()
  print( "[DONE] Finished writing Combine templates in {:.2f} minutes".format( ( time.time() - sTime ) / 60. ) ) 
   
def make_tables( hists, categories, groups, variable, templateDir, lumiStr, doABCDNN ):
  def initialize():
    yield_table = { "YIELD": {}, "ERROR": {} }
    for category in categories:
      for stat in yield_table: yield_table[ stat ][ category ] = {}
      if config.options[ "GENERAL" ][ "SYSTEMATICS" ]:
        for syst in config.systematics[ "MC" ].keys():
          if not config.systematics[ "MC" ][ syst ]: continue
          if syst.upper() == "HD" and not config.options[ "GENERAL" ][ "HDAMP" ]: continue
          if syst.upper() == "UE" and not config.options[ "GENERAL" ][ "UE" ]: continue
          for shift in [ "UP", "DN" ]:
            for stat in yield_table: yield_table[ stat ][ hist_tag( category, syst.upper() + shift ) ] = {}
    return yield_table
  
  def fill_yield( tables ):
    def get_yield( table, hist_key, group, category ):
      for process in group: 
        if args.verbose: ( "   + {}".format( process ) )
        table[ "YIELD" ][ category ][ process ] = hists[ hist_key ][ hist_tag( process, category ) ].Integral()
        if config.options[ "GENERAL" ][ "SYSTEMATICS" ] and "DAT" not in process.upper():
          for syst in config.systematics[ "MC" ].keys():
            if not config.systematics[ "MC" ][ syst ]: continue
            if process == "ABCDNN" and syst != "ABCDNN": continue
            if syst.upper() == "HD" and not config.options[ "GENERAL" ][ "HDAMP" ]: continue
            if syst.upper() == "UE" and not config.options[ "GENERAL" ][ "UE" ]: continue
            for shift in [ "UP", "DN" ]:
              table[ "YIELD" ][ hist_tag( category, syst.upper() + shift ) ][ process ] = hists[ hist_key ][ hist_tag( process, category, syst.upper() + shift ) ].Integral()
      return table

    for category in categories:
      if args.verbose: print( ">> Computing yields for DATA histograms" )
      tables = get_yield( tables, "CMB", [ "data_obs" ], category )
      if args.verbose: print( ">> Computing yields for SIGNAL histograms" )
      tables = get_yield( tables, "CMB", groups[ "SIG" ][ "PROCESS" ], category )
      #if args.verbose: print( ">> Computing yields for BACKGROUND physics groups" )
      #tables = get_yield( tables, "BKG", groups[ "BKG" ][ "PROCESS" ].keys(), category )
      if doABCDNN and hist_parse( category, samples )[ "ABCDNN" ]:
        if args.verbose: print( ">> Computing yields for ABCDNN BACKGROUND Combine groups" )
        tables = get_yield( tables, "CMB", [ "ABCDNN" ], category )
      else:
        if args.verbose: print( ">> Computing yields for BACKGROUND Combine groups" )
        tables = get_yield( tables, "CMB", groups[ "BKG" ][ "SUPERGROUP" ].keys(), category )
      
      tables[ "YIELD" ][ category ][ "TOTAL BKG" ] = 0
      for group in groups[ "BKG" ][ "SUPERGROUP" ]:
        if hist_tag( group, category ) not in hists[ "CMB" ].keys() or ( doABCDNN and hist_parse( category, samples )[ "ABCDNN" ] ): continue
        tables[ "YIELD" ][ category ][ "TOTAL BKG" ] += hists[ "CMB" ][ hist_tag( group, category ) ].Integral()
      if doABCDNN and hist_parse( category, samples )[ "ABCDNN" ]:
        tables[ "YIELD" ][ category ][ "TOTAL BKG" ] += hists[ "CMB" ][ hist_tag( "ABCDNN", category ) ].Integral()

      tables[ "YIELD" ][ category ][ "DATA:BKG" ] = tables[ "YIELD" ][ category ][ "data_obs" ] / ( tables[ "YIELD" ][ category ][ "TOTAL BKG" ] + config.params[ "GENERAL" ][ "ZERO" ] )
   
    return tables
  
  def fill_error( tables ):
    def get_error( table, hist_key, group, category ):
      for process in group:
        if args.verbose: print( "   + {}".format( process ) )
        table[ "ERROR" ][ category ][ process ] = 0
        for i in range( 1, hists[ hist_key ][ hist_tag( process, category ) ].GetXaxis().GetNbins() + 1 ):
          table[ "ERROR" ][ category ][ process ] += hists[ hist_key ][ hist_tag( process, category ) ].GetBinError(i)**2
        table[ "ERROR" ][ category ][ process ] = math.sqrt( table[ "ERROR" ][ category ][ process ] )
      return table

    for category in categories:
      if args.verbose: print( ">> Computing errors for DATA histograms" )
      tables = get_error( tables, "CMB", [ "data_obs" ], category )
      if args.verbose: print( ">> Computing errors for SIGNAL histograms" )
      tables = get_error( tables, "CMB", groups[ "SIG" ][ "PROCESS" ], category )
      #if args.verbose: print( ">> Computing errors for BACKGROUND physics groups" )
      #tables = get_error( tables, "BKG", groups[ "BKG" ][ "PROCESS" ].keys(), category )
      if doABCDNN and hist_parse( category, samples )[ "ABCDNN" ]:
        if args.verbose: print( ">> Computing errors for ABCDNN BACKGROUND Combine groups" )
        tables = get_error( tables, "CMB", [ "ABCDNN" ], category )
      else:
        if args.verbose: print( ">> Computing errors for BACKGROUND Combine groups" )
        tables = get_error( tables, "CMB", groups[ "BKG" ][ "SUPERGROUP" ].keys(), category )
    

      tables[ "ERROR" ][ category ][ "TOTAL BKG" ] = 0
      tables[ "ERROR" ][ category ][ "DATA:BKG" ] = 0
      for group in groups[ "BKG" ][ "SUPERGROUP" ]:
        if hist_tag( group, category ) not in hists[ "CMB" ].keys(): continue
        if doABCDNN and hist_parse( category, samples )[ "ABCDNN" ]: continue
        for i in range( 1, hists[ "CMB" ][ hist_tag( group, category ) ].GetXaxis().GetNbins() + 1 ):
          tables[ "ERROR" ][ category ][ "TOTAL BKG" ] += hists[ "CMB" ][ hist_tag( group, category ) ].GetBinError(i)**2
      if doABCDNN and hist_parse( category, samples )[ "ABCDNN" ]:
        tables[ "ERROR" ][ category ][ "TOTAL BKG" ] += hists[ "CMB" ][ hist_tag( "ABCDNN", category ) ].GetBinError(i)**2

      tables[ "ERROR" ][ category ][ "TOTAL BKG" ] = math.sqrt( tables[ "ERROR" ][ category ][ "TOTAL BKG" ] ) 
      yield_d = tables[ "YIELD" ][ category ][ "data_obs" ] 
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
          if process not in tables[ "YIELD" ][ category ].keys():
            row.append( pm.format(
              0,0
            ) )
          else:
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

    #table = format_section( table, "PHYSICS PROCESS", [ "DAT" ] + list( groups[ "BKG" ][ "PROCESS" ].keys() ), "2" )
    table = format_section( table, "COMBINE ANALYSIS", [ "data_obs" ] + list( groups[ "BKG" ][ "SUPERGROUP" ].keys() ), "2" )
    table = format_section( table, "COMBINE ABCDNN", [ "data_obs", "ABCDNN" ], "2" )
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


def main():
  start_time = time.time()

  template_prefix = config.region_prefix[ args.region ]
  templateDir = os.path.join( os.getcwd(), "{}_UL{}_{}".format( template_prefix, args.year, args.tag ) )
  categories = get_categories( templateDir )
  groups = samples.groups 
  systematics = [ str(syst) for syst in config.systematics[ "MC" ].keys() if config.systematics[ "MC" ][ syst ] ]
  if args.year in [ "16APV", "16", "17" ]: systematics += [ "prefire" ]

  for variable in args.variables:
    hists = load_histograms( variable, templateDir, categories )
    for hist_key in hists:
      if hists[ hist_key ].keys() == []: continue
      hists = clean_histograms( hists, hist_key, config.params[ "HISTS" ][ "LUMISCALE" ], config.params[ "HISTS" ][ "REBIN" ] )
    hists = combine_histograms( hists, variable, categories, groups, config.options[ "GENERAL" ][ "ABCDNN" ] )
    write_combine( hists, variable, categories, groups, templateDir, config.options[ "GENERAL" ][ "ABCDNN" ] )
    tables = make_tables( hists, categories, groups, variable, templateDir, config.lumiStr[ args.year ], config.options[ "GENERAL" ][ "ABCDNN" ] )
    print_tables( tables, categories, groups, variable, templateDir )
    del hists
    #del tables

main()
