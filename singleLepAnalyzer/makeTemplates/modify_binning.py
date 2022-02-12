#!/usr/bin/python

import os, sys, time, math, fnmatch
sys.path.append( os.path.dirname( os.getcwd() ) )
from array import array
import utils
import config
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument( "-y", "--year", required = True )
parser.add_argument( "-t", "--tag", required = True )
parser.add_argument( "-r", "--region", required = True )
parser.add_argument( "-v", "--variable", required = True )
parser.add_argument( "--verbose", action = "store_true" )
args = parser.parse_args()

import ROOT

if args.year == "16APV": 
  import samplesUL16APV as samples
  import weightsUL16APV as weights
elif args.year == "16":
  import samplesUL16 as samples
  import weightsUL16 as weights
elif args.year == "17": 
  import samplesUL17 as samples
  import weightsUL17 as weights
elif args.year == "18": 
  import samplesUL18 as samples
  import weightsUL18 as weights
else: quit( "[ERR] Invalid -y (--year) argument. Quitting" )

def hist_tag( *args ):
  histTag = args[0]
  for arg in args[1:]: histTag += "_{}".format( arg )
  return histTag

def syst_parse( hist_name ):
  parts = hist_name.split( "_" )
  if len( parts ) == len( args.variable.split( "_" ) ) + 4: 
    syst_name = parts[len( args.variable.split( "_" ) )]
    if "UP" in syst_name or "DN" in syst_name: syst_name = syst_name[:-2]
    if "PDF" in syst_name: syst_name = syst_name[:3]
    return True, syst_name
  else:
    return False, ""
      
def overflow( hist ):
  nbins = hist.GetXaxis().GetNbins()
  yields = hist.GetBinContent( nbins ) + hist.GetBinContent( nbins + 1 )
  error = math.sqrt( hist.GetBinError( nbins )**2 + hist.GetBinError( nbins + 1 )**2 )
  hist.SetBinContent( nbins, yields )
  hist.SetBinError( nbins, error )
  hist.SetBinContent( nbins + 1, 0 )
  hist.SetBinError( nbins + 1, 0 )
  
def underflow( hist ):
  nbins = hist.GetXaxis().GetNbins()
  yields = hist.GetBinContent( 0 ) + hist.GetBinContent( 1 )
  error = math.sqrt( hist.GetBinError( 0 )**2 + hist.GetBinError( 1 )**2 )
  hist.SetBinContent( 1, yields )
  hist.SetBinError( 1, error )
  hist.SetBinContent( 0, 0 )
  hist.SetBinError( 0, 0 ) 
  
class ModifyTemplate():
  def __init__( self, filepath, options, params, groups, variable ):
    self.filepath = filepath
    self.options = options
    self.params = params
    self.groups = groups
    self.variable = variable
    self.rebinned = {}
    self.yields = {}
    print( "[INFO] Running ModifyTemplate() with the following options" )
    for option in self.options:
      print( "  + {}: {}".format( option, self.options[ option ] ) )
    print( "[INFO] Running ModifyTemplate() with the following parameters" )
    for param in self.params:
      print( "  + {}: {}".format( param, self.params[ param ] ) )
    self.load_histograms()
    self.get_xbins()
    self.rebin()
    
  def load_histograms( self ):
    print( "[START] Loading histograms from {}".format( self.filepath ) )
    self.rFile = { "INPUT":  ROOT.TFile( self.filepath ) }
    self.hist_names = [ hist_name.GetName() for hist_name in self.rFile[ "INPUT" ].GetListOfKeys() ]
    self.categories = list( set( hist_name.split( "_" )[-2] for hist_name in self.hist_names ) )
    self.channels = list( set( category[3:] for category in self.categories ) )
    
    groups_bkg = list( self.groups[ "BKG" ][ "PROCESS" ].keys() ) + list( self.groups[ "BKG" ][ "SUPERGROUP" ].keys() )
    groups_sig = self.groups[ "SIG" ][ "PROCESS" ] + [ "SIG" ]
    groups_dat = self.groups[ "DAT" ][ "PROCESS" ] + [ "DAT" ]
    category_log = { key: [] for key in [ "ALL", "DAT", "BKG", "SIG" ] }
    self.histograms = { key: {} for key in [ "BKG", "SIG", "DAT", "TOTAL BKG", "TOTAL SIG", "TOTAL DAT" ] }
    count = 0 
    for hist_name in self.hist_names:
      syst, syst_name = syst_parse( hist_name )
      parts = hist_name.split( "_" )
      process = parts[-1]
      category = parts[-2]
      if category not in category_log[ "ALL" ]:
        category_log[ "ALL" ].append( category )

      if process in groups_dat:
        if args.verbose and not syst: print( "   + DAT: {}".format( hist_name ) )
        self.histograms[ "DAT" ][ hist_name ] = self.rFile[ "INPUT" ].Get( hist_name ).Clone( hist_name )
        if category not in category_log[ "DAT" ] and not syst:
          self.histograms[ "TOTAL DAT" ][ category ] = self.histograms[ "DAT" ][ hist_name ].Clone( "TOTAL DAT {}".format( category ) )
          category_log[ "DAT" ].append( category )
        elif not syst:
          self.histograms[ "TOTAL DAT" ][ category ].Add( self.histograms[ "DAT" ][ hist_name ] )
      elif process in groups_bkg:
        if args.verbose and not syst: print( "   + BKG: {}".format( hist_name ) )
        self.histograms[ "BKG" ][ hist_name ] = self.rFile[ "INPUT" ].Get( hist_name ).Clone( hist_name )   
        if category not in category_log[ "BKG" ] and not syst:
          self.histograms[ "TOTAL BKG" ][ category ] = self.histograms[ "BKG" ][ hist_name ].Clone( "TOTAL BKG {}".format( category ) )
          category_log[ "BKG" ].append( category )
        elif not syst:
          self.histograms[ "TOTAL BKG" ][ category ].Add( self.histograms[ "BKG" ][ hist_name ] )
      elif process in groups_sig:
        if args.verbose and not syst: print( "   + SIG: {}".format( hist_name ) )
        self.histograms[ "SIG" ][ hist_name ] = self.rFile[ "INPUT" ].Get( hist_name ).Clone( hist_name )
        if category not in category_log[ "SIG" ] and not syst:
          self.histograms[ "TOTAL SIG" ][ category ] = self.histograms[ "SIG" ][ hist_name ].Clone( "TOTAL SIG {}".format( category ) )
          category_log[ "SIG" ].append( category )
        elif not syst:
          self.histograms[ "TOTAL SIG" ][ category ].Add( self.histograms[ "SIG" ][ hist_name ] )
      else:
        if args.verbose: print( "[WARN] {} does not belong to any of the groups: BKG, SIG, DAT, excluding...".format( process ) )
      count += 1
    
    print( ">> Creating lepton categories" )
    for channel in self.channels:
      category_log[ "ALL" ].append( "isL" + channel )
    for key in self.histograms:
      print( "   o {}".format( key ) )
      key_hist_names = [ hist_name for hist_name in self.histograms[ key ].keys() if "isE" in hist_name ]
      for hist_name in key_hist_names:
        name_lepton = hist_name.replace( "isE", "isL" )
        self.histograms[ key ][ name_lepton ] = self.histograms[ key ][ hist_name ].Clone( name_lepton )
        self.histograms[ key ][ name_lepton ].Add( self.histograms[ key ][ hist_name.replace( "isE", "isM" ) ] )
        if "UP_" not in hist_name and "DN_" not in hist_name and "PDF" not in hist_name:  print( "     + {}: {}".format( name_lepton, self.histograms[ key ][ name_lepton ].Integral() ) )  
    
    for hist_key in self.histograms:
      for hist_name in self.histograms[ hist_key ]:
        self.histograms[ hist_key ][ hist_name ].SetDirectory(0)
    
    self.rFile[ "INPUT" ].Close()
    print( "[DONE] Found {} histograms".format( count ) )
  
  def get_xbins( self ): # done
  # get the new histogram bins that satisfy the requirement bin error / yield <= threshold
    print( "[START] Determining modified histogram binning" )
    self.xbins = { key: {} for key in [ "MERGED", "LIMIT", "MODIFY" ] } # change OLD --> merged and NEW --> limit
    for channel in self.channels:
      N_BINS = self.histograms[ "TOTAL BKG" ][ "isL" + channel ].GetNbinsX()
      self.xbins[ "MERGED" ][ channel ] = [ self.histograms[ "TOTAL BKG" ][ "isL" + channel ].GetXaxis().GetBinUpEdge( N_BINS ) ]
      bin_content = {
        key_lep: {
          key_type: {
            key_stat: 0. for key_stat in [ "YIELD", "ERROR" ]
          } for key_type in [ "TOTAL BKG", "TOTAL DAT" ]
        } for key_lep in [ "isE", "isM" ]
      }
      N_MERGED = 0
      for i in range( 1, N_BINS + 1 ):
        N_MERGED += 1
        if self.params[ "STAT THRESHOLD" ] > 1.0:
          if N_MERGED < self.params[ "MIN MERGE" ]: 
            continue
          else:
            self.xbins[ "MERGED" ][ channel ].append( self.histograms[ "TOTAL BKG" ][ "isL" + channel ].GetXaxis().GetBinLowEdge( N_BINS + 1 - i ) )
            N_MERGED = 0
        else:
          for key_type in [ "TOTAL BKG", "TOTAL DAT" ]:
            for key_lep in [ "isE", "isM" ]:
                bin_content[ key_lep ][ key_type ][ "YIELD" ] += self.histograms[ key_type ][ key_lep + channel ].GetBinContent( N_BINS + 1 - i )
                bin_content[ key_lep ][ key_type ][ "ERROR" ] += self.histograms[ key_type ][ key_lep + channel ].GetBinError( N_BINS + 1 - i )**2
          if N_MERGED < self.params[ "MIN MERGE" ]: 
            continue
          else:
            if math.sqrt( bin_content[ "isE" ][ "TOTAL BKG" ][ "ERROR" ] ) / bin_content[ "isE" ][ "TOTAL BKG" ][ "YIELD" ] <= self.params[ "STAT THRESHOLD" ]:
              if math.sqrt( bin_content[ "isL" ][ "TOTAL BKG" ][ "ERROR" ] ) / bin_content[ "isL" ][ "TOTAL BKG" ][ "YIELD" ] <= self.params[ "STAT THRESHOLD" ]:
                for key_type in [ "TOTAL BKG", "TOTAL DAT" ]:
                  for key_lep in [ "isE", "isM" ]:
                    for key_stat in [ "YIELD", "ERROR" ]:
                      bin_content[ key_lep ][ key_type ][ key_stat ] = 0
                      N_MERGED = 0
                      self.xbins[ "MERGED" ][ channel ].append( self.histograms[ "isL" + channel ].GetXaxis().GetBinLowEdge( N_BINS + 1 - i ) )
       
      if self.params[ "STAT THRESHOLD" ] <= 1.0:
        if self.histograms[ "TOTAL BKG" ][ "isE" + channel ].GetBinContent(1) == 0. or self.histograms[ "TOTAL BKG" ][ "isM" + channel ].GetBinContent(1) == 0.:
          if len( self.xbins[ "MERGED" ][ channel ] ) > 2: 
            del self.xbins[ "MERGED" ][ channel ][-2]
        for key_lep in [ "isE", "isM" ]:
          if self.histograms[ "TOTAL BKG" ][ key_lep + channel ].GetBinError(1) / self.histograms[ "TOTAL BKG" ][ key_lep + channel ].GetBinContent(1) > self.params[ "STAT THRESHOLD" ]:
            if len( self.xbins[ "MERGED" ][ channel ] ) > 2: 
              del self.xbins[ "MERGED" ][ channel ][-2]
              continue
      
      self.N_NEWBINS = len( self.xbins[ "MERGED" ][ channel ] )
      self.xbins[ "LIMIT" ][ channel ] = []
      for i in range( self.N_NEWBINS ):
        self.xbins[ "LIMIT" ][ channel ].append( self.xbins[ "MERGED" ][ channel ][ self.N_NEWBINS - 1 - i ] )
      
      self.xbins[ "LIMIT" ][ channel ][0] = max( min( config.plot_params[ "VARIABLES" ][ args.variable ][1] ), self.xbins[ "LIMIT" ][ channel ][0] )
      self.xbins[ "LIMIT" ][ channel ][-1] = min( max( config.plot_params[ "VARIABLES" ][ args.variable ][1] ), self.xbins[ "LIMIT" ][ channel ][-1] )
      
      for i in range( 1, len( self.xbins[ "LIMIT" ][ channel ] ) - 1 ):
        if self.xbins[ "LIMIT" ][ channel ][i] <= self.xbins[ "LIMIT" ][ channel ][0] or self.xbins[ "LIMIT" ][ channel ][i] >= self.xbins[ "LIMIT" ][ channel ][-1]:
          del self.xbins[ "LIMIT" ][ channel ][i]
          
      self.xbins[ "MODIFY" ][ channel ] = array( "d", self.xbins[ "LIMIT" ][ channel ] )
      print( "[DONE] Total bins went from {} -> {} with {} threshold".format( N_BINS, self.N_NEWBINS, self.params[ "STAT THRESHOLD" ] ) )
        
  def rebin( self ): # done
  # merge the histogram bins using an uncertainty threshold requiring bin error / yield <= threshold
  # the merging requirements are determined in self.get_xbins()
    print( "[START] Rebinning histograms" )
    count = 0
    for hist_key in self.histograms:
      print( ">> Rebinning {}".format( hist_key ) )
      self.rebinned[ hist_key ] = {}
      for hist_name in self.histograms[ hist_key ]:
        xbins_channel = None
        for channel in self.xbins[ "MODIFY" ]:
          if channel in hist_name:
            xbins_channel = self.xbins[ "MODIFY" ][ channel ]
        self.rebinned[ hist_key ][ hist_name ] = self.histograms[ hist_key ][ hist_name ].Rebin(
          len( xbins_channel ) - 1,
          hist_name,
          xbins_channel
        )
        self.rebinned[ hist_key ][ hist_name ].SetDirectory(0)
        overflow( self.rebinned[ hist_key ][ hist_name ] )
        underflow( self.rebinned[ hist_key ][ hist_name ] )
        
        if self.options[ "BLIND" ] and "DAT" in hist_key:
          zero_bin = self.rebinned[ hist_key ][ hist_name ].FindBin(0)
          max_bin = self.rebinned[ hist_key ][ hist_name ].GetNbinsX() + 1
          for i in range( zero_bin, max_bin ):
            self.rebinned[ hist_key ][ hist_name ].SetBinContent( i, -100.0 )
        count += 1
    
    print( "[DONE] {} histograms rebinned".format( count ) )
  
  def compute_yield_stats(): # done
  # get the integral yield for each bin as well as the associated error
    print( "[START] Retrieving yields and errors for each histogram's bins." )
    count = 0
    for hist_key in self.rebinned:
      print( ">> Retrieving yields and errors for {}".format( hist_key ) )
      self.yields[ hist_key ] = {}
      for hist_name in self.rebinned[ hist_key ]:
        syst, syst_name = syst_parse( hist_name )
        self.yields[ hist_key ][ hist_name ] = {
          "COUNT": self.rebinned[ hist_key ][ hist_name ].Integral(),
          "ERROR": 0
        }
        for i in range( 1, self.rebinned[ hist_key ][ hist_name ].GetXaxis().GetNbins() + 1 ):
          self.yields[ "ERROR" ] += self.rebinned[ hist_key ][ hist_name ].GetBinError(i)**2
        self.yields[ hist_key ][ hist_name ][ "ERROR" ] = math.sqrt( self.yields[ hist_key ][ hist_name ][ "ERROR" ] )
        if args.verbose and not syst: 
          print( "   + {}: {:.2f} pm {:.2f}".format( 
            hist_name, 
            self.yields[ hist_key ][ hist_name ][ "COUNT" ],
            self.yields[ hist_key ][ hist_name ][ "ERROR" ]
          ) )
        count += 1
    print( "[DONE] Calculated yields for {} histograms".format( count ) )  
          
  def add_trigger_efficiency(): # done
  # specify trigger efficiencies for the single leptons
    print( "[START] Differentiating trigger efficiency histogram naming between lepton flavors" )
    count = 0
    for hist_key in self.rebinned:
      for hist_name in self.rebinned[ hist_key ]:
        if "TRIGEFF" not in hist_name.upper(): continue
        if "ISE" in hist_name.upper():
          hist_name_el = self.rebinned[ hist_key ][ hist_name ].GetName().replace( "TRIGEFF", "ELTRIGGEFF" )
          self.rebinned[ hist_key ][ hist_name_el ] = self.rebinned[ hist_key ][ hist_name ].Clone( hist_name_el )
          self.rebinned[ hist_key ][ hist_name_el ].SetDirectory(0)
        if "ISM" in hist_name.upper():
          hist_name_mu = self.rebinned[ hist_key ][ hist_name ].GetName().replace( "TRIGEFF", "MUTRIGGEFF" )
          self.rebinned[ hist_key ][ hist_name_mu ] = self.rebinned[ hist_key ][ hist_name ].Clone( hist_name_mu )
          self.rebinned[ hist_key ][ hist_name_el ].SetDirectory(0)
        count += 1
    print( "[DONE] Adjusted trigger naming for {} histograms.".format( count ) )
    
  def uncorrelate_year(): # done
  # differentiate the shifts by year
    print( "[START] Differentiating systematic shifts by year" )
    count = 0
    for hist_key in self.rebinned:
      for hist_name in self.rebinned[ hist_key ]:
        syst, syst_name = syst_parse( hist_name )
        if syst:
          hist_name_new = self.rebinned[ hist_key ][ hist_name ].GetName().replace( "UP", "{}UP".format( args.year ) ).replace( "DN", "{}DN".format( args.year ) )
          self.rebinned[ hist_key ][ hist_name_new ] = self.rebinned[ hist_key ][ hist_name ].Clone( hist_name_new )
          self.rebinned[ hist_key ][ hist_name_new ].SetDirectory(0)
          count += 1
    print( "[DONE] Adjusted systematic shift names for {} histograms".format( count ) )
    
  def symmetrize_topPT_shift(): # done
  # symmetrize the up and down shifts for toppt systematic
    print( "[START] Symmetrizing the toppt systematic shifts" )
    count = 0
    for hist_key in self.rebinned:
      for hist_name in self.rebinned[ hist_key ]:
        if "TOPPTDN" not in hist_name.upper(): continue # adjust TOPPTDN to TOPPTUP
        for i in range( 1, self.rebinned[ hist_key ][ hist_name ].GetNbinsX() + 1 ):
          self.rebinned[ hist_key ][ hist_name ].SetBinContent(
            i, 2. * self.rebinned[ hist_key ][ hist_name.replace( "_TOPPTDN", "" ) ].GetBinContent(i) - self.rebinned[ hist_key ][ hist_name.replace( "DN", "UP" ) ].GetBinContent(i) 
          )
        count += 1
    print( "[DONE] Adjusted {} toppt histograms".format( count ) )

  def add_statistical_shapes(): # done
  # add shifts to the bin content for the statistical shape uncertainty
    def write_statistical_hists( category, group, i, nBB ):
      if self.rebinned[ "TOTAL BKG" ][ hist_name ].GetNbinsX() == 1 or group == "SIG":  
        for sig_name in self.rebinned[ "SIG" ]:
          syst, syst_name = syst_parse( sig_name )
          if syst: continue
          yields = {
            "COUNT": self.rebinned[ "SIG" ][ sig_name ].GetBinContent(i),
            "ERROR": self.rebinned[ "SIG" ][ sig_name ].GetBinError(i)
          }
          if yields[ "COUNT" ] == 0: continue
          shift_name = { 
            shift: "{}__CMS_TTTX_UL{}_{}_BIN{}{}".format(
              sig_name.split( "_" )[-1],
              args.year, category, i, shift  
            ) for shift in [ "UP", "DN" ] 
          }
          for shift in [ "UP", "DN" ]:
            self.rebinned[ "SIG" ][ shift_name[ shift ] ] = self.rebinned[ "SIG" ][ sig_name ].Clone( shift_name[ shift ] ) 
            if shift == "UP": self.rebinned[ "SIG" ][ shift_name[ shift ] ].SetBinContent( i, yields[ "COUNT" ] + yields[ "ERROR" ] )
            if shift == "DN": self.rebinned[ "SIG" ][ shift_name[ shift ] ].SetBinContent( i, yields[ "COUNT" ] - yields[ "ERROR" ] )
            if yields[ "COUNT" ] - yields[ "ERROR" ] < 0:
              print( ">> Correcting negative bin {} for {}".format( i, sig_name ) )
              negative_bin_correction( self.rebinned[ "SIG" ][ shift_name[ shift ] ] )
            if yields[ "COUNT" ] - yields[ "ERROR" ] == 0:
              print( ">> Setting zero bin {} for {} to non-zero value".format( i, sig_name ) )
              self.rebinned[ "SIG" ][ shift_name[ shift ] ].SetBinContent( i, yields[ "COUNT" ] * 0.001 )
            self.rebinned[ "SIG" ][ shift_name[ shift ] ].SetDirectory(0)
          nBB[ "SIG" ] += 1
      else:
        bkg_max = ""
        count_max = 0
        for bkg_name in self.rebinned[ "BKG" ]:
          syst, syst_name = syst_parse( bkg_name )
          if syst: continue
          if count_max < self.rebinned[ "BKG" ][ bkg_name ].GetBinContent(i):
            count_max = self.rebinned[ "BKG" ][ bkg_name ].GetBinContent(i)
            bkg_max = bkg_name
        error_max = self.rebinned[ "BKG" ][ bkg_max ].GetBinError(i)
        print( "   + {} is the dominant background process in bin {}: {:.2f} pm {:.2f}".format(
          bkg_max, i, count_max, error_max 
        ) )
        shift_name = {
          shift: "{}__CMS_TTTX_UL{}_{}_BIN{}{}".format(
            bkg_max.split( "_" )[-1],
            args.year, category, i, shift
          ) for shift in [ "UP", "DN" ]
        }
        for shift in [ "UP", "DN" ]:
          self.rebinned[ "BKG" ][ shift_name[ shift ] ] = self.rebinned[ "BKG" ][ bkg_max ].Clone( shift_name[ shift ] )
          if shift == "UP": self.rebinned[ "BKG" ][ shift_name[ shift ] ].SetBinContent( i, count_max + error_max )
          if shift == "DN": self.rebinned[ "BKG" ][ shift_name[ shift ] ].SetBinContent( i, count_max - error_max )
          if count_max - error_max < 0:
            print( ">> Correcting negative bin {} for {}".format( i, bkg_max ) )
            negative_bin_correction( self.rebinned[ "BKG" ][ shift_name[ shift ] ] )
          if count_max - error_max == 0:
            print( ">> Setting zero bin {} for {} to non-zero value".format( i, bkg_max ) )
            self.rebinned[ "BKG" ][ shift_name[ shift ] ].SetBinContent( i, count_max * 0.001 )
          self.rebinned[ "BKG" ][ shift_name[ shift ] ].SetDirectory(0)
        nBB[ "BKG" ] += 1
          
    print( "[START] Adding statistical shape systematics" )
    nBB = { "BKG": 0, "SIG": 0 }
    for hist_name in self.rebinned[ "TOTAL BKG" ]:
      count = { "INCLUDE": 0, "EXCLUDE": 0 }
      for i in range( 1, self.rebinned[ "TOTAL BKG" ][ hist_name ] ):
        error_ratio = self.rebinned[ "TOTAL BKG" ][ hist_name ].GetBinError(i) / self.rebinned[ "TOTAL BKG" ][ hist_name ].GetBinContent(i)
        if error_ratio <= self.params[ "THRESHOLD BB" ]:
          count[ "EXCLUDE" ] += 1
          continue
        write_statistical_hists( hist_name, "SIG", i, nBB )
        write_statistical_hists( hist_name, "BKG", i, nBB )
        count[ "INCLUDE" ] += 1
      print( ">> {}: {}/{} bins excluded".format( hist_name, count[ "EXCLUDE" ], count[ "EXCLUDE" ] + count[ "INCLUDE" ] ) )
    print( "[DONE] {} Signal BB shapes added, {} Background BB shapes added".format( nBB[ "SIG" ], nBB[ "BKG" ] ) )
          

              
  def symmetrize_HOTclosure(): # done
    # make the up and down shifts of the HOTClosure systematic symmetric
    print( "[START] Symmetrizing the HOT closure systematic down shifts to match the up shifts" )
    count = 0
    for hist_key in self.rebinned:
      for hist_name in self.rebinned[ hist_key ]:
        if "HOTCLOSUREUP" not in hist_name.upper(): continue
        HOT_name = {
          "NOM": hist_name.replace( "_HOTCLOSUREUP", "" ),
          "UP": hist_name,
          "DN": hist_name.replace( "UP", "DN" )
        }
        for i in range( 1, self.rebinned[ hist_key ][ hist_name ].GetNbinsX() + 1 ):
          max_shift = max(
            abs( self.rebinned[ hist_key ][ HOT_name[ "NOM" ] ].GetBinContent(i) - self.rebinned[ hist_key ][ HOT_name[ "UP" ] ].GetBinContent(i) ),
            abs( self.rebinned[ hist_key ][ HOT_name[ "NOM" ] ].GetBinContent(i) - self.rebinned[ hist_key ][ HOT_name[ "DN" ] ].GetBinContent(i) )
          )
          self.rebinned[ hist_key ][ HOT_name[ "UP" ] ].SetBinContent( i, self.rebinned[ hist_key ][ HOT_name[ "NOM" ] ].GetBinContent(i) + max_shift )
          self.rebinned[ hist_key ][ HOT_name[ "DN" ] ].SetBinContent( i, self.rebinned[ hist_key ][ HOT_name[ "NOM" ] ].GetBinContent(i) - max_shift )
        count += 1
    print( "[DONE] Adjusted the HOT closure systematic shift for {} histograms".format( count ) )    
    
  def add_muRF_shapes(): # done
  # adding MU RF systematic shapes
    print( "[START] Adding MU RF systematic shapes" )
    count = 0
    for hist key in self.rebinned[ "SIG", "BKG" ]:
      for hist_name in self.rebinned[ hist_key ]:
        if "MURUP" not in hist_name.upper(): continue
        hist_muRF = { "NOMINAL": self.rebinned[ hist_key ][ hist_name.replace( "_MURUP", "" ) ].Clone() }
        for syst in [ "MURUP", "MURDN", "MUFUP", "MUFDN", "MURFCORRDUP", "MURFCORRDDN" ]:
          hist_muRF[ syst ] = self.rebinned[ hist_key ][ hist_name.replace( "MURUP", syst ) ].Clone()
        hist_muRF[ "MURFUP" ] = self.rebinned[ hist_key ][ hist_name ].Clone( hist_name.replace( "MURUP", "MURFUP" ) )
        hist_muRF[ "MURFDN" ] = self.rebinned[ hist_key ][ hist_name ].Clone( hist_name.replace( "MURDN", "MURFDN" ) )
        for i in range( 1, hist_muRF[ "NOMINAL" ].GetNbinsX() + 1 ):
          weight_dict = { key: hist_muRF[ key ].GetBinContent(i) for key in hist_muRF }
          weight_key = {
            "MAX": "NOMINAL",
            "MIN": "NOMINAL"
          }
          weight_limit = {
            "MAX": weight_dict[ "NOMINAL" ].GetBinContent(i),
            "MIN": weight_dict[ "NOMINAL" ].GetBinContent(i)
          }
          weight_error = {
            "MAX": weight_dict[ "NOMINAL" ].GetBinError(i),
            "MIN": weight_dict[ "NOMINAL" ].GetBinError(i)
          }
          for key in hist_muRF:
            if weight_dict[ key ].GetBinContent(i) > weight_limit[ "MAX" ]: 
              weight_limit[ "MAX" ] = weight_dict[ key ].GetBinContent(i)
              weight_error[ "MAX" ] = weight_dict[ key ].GetBinError(i)
              weight_key[ "MAX" ] = key
            if weight_dict[ key ].GetBinContent(i) < weight_limit[ "MIN" ]: 
              weight_limit[ "MIN" ] = weight_dict[ key ].GetBinContent(i)
              weight_error[ "MIN" ] = weight_dict[ key ].GetBinError(i)
              weight_key[ "MIN" ] = key

          hist_muRF[ "MURFUP" ].SetBinContent( i, weight_limit[ "MAX" ] )
          hist_muRF[ "MURFUP" ].SetBinError( i, weight_error[ "MAX" ] )
          hist_muRF[ "MURFDN" ].SetBinContent( i, weight_limit[ "MIN" ] )
          hist_muRF[ "MURFDN" ].SetBinError( i, weight_error[ "MIN" ] )

        if self.options[ "NORM THEORY SYST {}".format( hist_key ) ]:
          hist_muRF[ "MURFUP" ].Scale( hist_muRF[ "NOMINAL" ].Integral() / ( hist_muRF[ "MURFUP" ].Integral() + config.params[ "GENERAL" ][ "ZERO" ] ) )
          hist_muRF[ "MURFDN" ].Scale( hist_muRF[ "NOMINAL" ].Integral() / ( hist_muRF[ "MURFDN" ].Integral() + config.params[ "GENERAL" ][ "ZERO" ] ) )

        process = hist_name.split( "_" )[-1]
        for shift in [ "UP", "DN" ]:
          hist_muRF[ "MURF__{}_{}".format( shift, process ) ] = hist_muRF[ "MURF{}".format( shift ) ].Clone( "MURF__{}_{}".format( shift, process ) )
          hist_muRF[ "MURF__{}_{}_{}".format( shift, process, args.year ) ] = hist_muRF[ "MURF{}".format( shift ) ].Clone( "MURF__{}_{}_{}".format( shift, process, args.year ) )
          hist_muRF[ "MURF__{}_{}".format( shift, args.year ) ] = hist_muRF[ "MURF{}".format( shift ) ].Clone( "MURF__{}_{}".format( shift, args.year ) )

        for muRF_key in hist_muRF:
          if muRF_key in self.rebinned[ hist_key ].keys():
            del self.rebinned[ hist_key ][ muRF_key ]
          self.rebinned[ hist_key ][ muRF_key ] = hist_muRF[ muRF_key ].Clone( muRF_key )
          self.rebinned[ hist_key ][ muRF_key ].SetDirectory(0)
          count += 1  
    print( "[DONE] Adjusted {} MU R/F histograms".format( count ) ) 
  
  def add_PSWeight_shapes(): # done
    print( "[START] Adding PS weights" )
    count = 0
    for hist_key in [ "SIG", "BKG" ]:
      for hist_name in self.rebinned[ hist_key ]:
        if "ISRUP" not in hist_name.upper(): continue
        hist_PSWeight = { "NOMINAL": self.rebinned[ hist_key ][ hist_name.replace( "_ISRUP", "" ) ].Clone( "NOMINAL" ) }
        hist_PSWeight[ "PSWGTUP" ] = self.rebinned[ hist_key ][ hist_name ].Clone( hist_name.replace( "MURUP", "PSWGTUP" ) )
        hist_PSWeight[ "PSWGTDN" ] = self.rebinned[ hist_key ][ hist_name ].Clone( hist_name.replace( "MURDN", "PSWGTDN" ) )
        for syst in [ "ISR", "FSR" ]:
          for shift in [ "UP", "DN" ]:
            hist_PSWeight[ syst + shift ] = self.rebinned[ hist_key ][ hist_name.replace( "ISRUP", syst + shift ) ].Clone( syst + shift )
        for i in range( 1, hist_dict[ "NOMINAL" ].GetNbinsX() + 1 ):
          weight_key = {
            "MAX": "NOMINAL",
            "MIN": "NOMINAL"
          }
          weight_limit = {
            "MAX": hist_PSWeight[ "NOMINAL" ].GetBinContent(i),
            "MIN": hist_PSWeight[ "NOMINAL" ].GetBinContent(i)
          }
          weight_error = {
            "MAX": hist_PSWeight[ "NOMINAL" ].GetBinError(i),
            "MIN": hist_PSWeight[ "NOMINAL" ].GetBinError(i)
          }
          for key in hist_PSWeight:
            if hist_PSWeight[ key ].GetBinContent(i) > weight_limit[ "MAX" ]:
              weight_limit[ "MAX" ] = hist_PSWeight[ key ].GetBinContent(i)
              weight_error[ "MAX" ] = hist_PSWeight[ key ].GetBinError(i)
              weight_key[ "MAX" ] = key
            if hist_dict[ key ].GetBinContent(i) < weight_limit[ "MIN" ]:
              weight_limit[ "MIN" ] = hist_PSWeight[ key ].GetBinContent(i)
              weight_error[ "MIN" ] = hist_PSWeight[ key ].GetBinError(i)
              weight_key[ "MIN" ] = key
        
          # in-case symmetrization is needed for PSWGTUP:
          # hist_PSWeight[ "PSWGTUP" ].SetBinContent( i, 2 * hist_PSWeight[ "NOMINAL" ].GetBinContent(i) - weight_limit[ "MIN" ].GetBinContent(i) )
          hist_PSWeight[ "PSWGTUP" ].SetBinContent( i, weight_limit[ "MAX" ] )
          hist_PSWeight[ "PSWGTUP" ].SetBinError( i, weight_error[ "MAX" ] )
          hist_PSWeight[ "PSWGTDN" ].SetBinContent( i, weight_limit[ "MIN" ] )
          hist_PSWeight[ "PSWGTDN" ].SetBinError( i, weight_error[ "MIN" ] )
        
        if self.options[ "NORM THEORY SYST {}".format( hist_key ) ]:
          hist_PSWeight[ "PSWGTUP" ].Scale( hist_PSWeight[ "NOMINAL" ].Integral() / ( hist_PSWeight[ "PSWGTUP" ].Integral() + config.params[ "GENERAL" ][ "ZERO" ] ) )
          hist_PSWeight[ "PSWGTDN" ].Scale( hist_PSWeight[ "NOMINAL" ].Integral() / ( hist_PSWeight[ "PSWGTDN" ].Integral() + config.params[ "GENERAL" ][ "ZERO" ] ) )
        
        process = hist_name.split( "_" )[-1]
        for shift in [ "UP", "DN" ]:
          hist_PSWeight[ "PSWGT__{}_{}".format( shift, process ) ] = hist_PSWeight[ hist_name.replace( "ISRUP", "ISR" + shift ) ].Clone( "PSWGT__{}_{}".format( shift, process ) )
          hist_PSWeight[ "PSWGT__{}_{}_{}".format( shift, process, args.year ) ] = hist_PSWeight[ hist_name.replace( "ISRUP", "ISR" + shift ) ].Clone( "PSWGT__{}_{}_{}".format( shift, process, args.year ) )
          hist_PSWeight[ "PSWGT__{}_{}".format( shift, args.year ) ] = hist_PSWeight[ hist_name.replace( "ISRUP", "ISR" + shift ) ].Clone( "PSWGT__{}_{}".format( shift, args.year ) )

        for PSWGT_key in hist_PSWeight:
          if muRF_key in self.rebinned[ hist_key ].keys():
            del self.rebinned[ hist_key ][ muRF_key ]
          self.rebinned[ hist_key ][ PSWGT_key ] = hist_PSWeight[ PSWGT_key ].Clone( PSWGT_key )\
          self.rebinned[ hist_key ][ PSWGT_key ].SetDirectory(0)
          count += 1
    print( "[DONE] Adjusted {} PS Weight histograms".format( count ) )
          
  def add_PDF_shapes(): # done
    print( "[START] Adding PDF shape systematics" )
    count = 0
    for hist_key in [ "SIG", "BKG" ]:
      for hist_name in self.rebinned[ hist_key ]:
        if "PDF0" not in hist_name: continue
        hist_PDF = { 
          "NOMINAL": self.rebinned[ hist_key ][ hist_name.replace( "_PDF0", "" ) ].Clone( "NOMINAL" ),
          "PDFUP": self.rebinned[ hist_key ][ hist_name ].Clone( "PDFUP" ),
          "PDFDN": self.rebinned[ hist_key ][ hist_name ].Clone( "PDFDN" )
        }
        for i in config.params[ "GENERAL" ][ "PDF RANGE" ]:
          hist_PDF[ "PDF{}".format(i) ] = self.rebinned[ hist_key ][ hist_name.replace( "PDF0", "PDF{}".format(i) ) ].Clone( "PDF{}".format(i) )
        for i in range( 1, hist_PDF[ "NOMINAL" ].GetNbinsX() + 1 ):
          weight_key = {
            "MAX": "NOMINAL",
            "MIN": "NOMINAL"
          }
          weight_limit = {
            "MAX": hist_PDF[ "NOMINAL" ].GetBinContent(i),
            "MIN": hist_PDF[ "NOMINAL" ].GetBinContent(i)
          }
          weight_error = {
            "MAX": hist_PDF[ "NOMINAL" ].GetBinError(i),
            "MIN": hist_PDF[ "NOMINAL" ].GetBinError(i)
          }
          for key in hist_PDF:
            if hist_PDF[ key ].GetBinContent(i) > weight_limit[ "MAX" ]:
              weight_limit[ "MAX" ] = hist_PDF[ key ].GetBinContent(i)
              weight_error[ "MAX" ] = hist_PDF[ key ].GetBinError(i)
              weight_key[ "MAX" ] = key
            if hist_PDF[ key ].GetBinContent(i) < weight_limit[ "MIN" ]:
              weight_limit[ "MIN" ] = hist_PDF[ key ].GetBinContent(i)
              weight_error[ "MIN" ] = hist_PDF[ key ].GetBinError(i)
              weight_key[ "MIN" ] = key
          
          hist_PDF[ "PDFUP" ].SetBinContent( i, weight_limit[ "MAX" ] )
          hist_PDF[ "PDFUP" ].SetBinError( i, weight_error[ "MAX" ] )
          hist_PDF[ "PDFDN" ].SetBinContent( i, weight_limit[ "MIN" ] )
          hist_PDF[ "PDFDN" ].SetBinError( i, weight_error[ "MIN" ] )

        if self.options[ "NORM THEORY SYST {}".format( hist_key ) ]:
          hist_PDF[ "PDFUP" ].Scale( hist_PDF[ "NOMINAL" ].Integral() / ( hist_PDF[ "PDFUP" ].Integral() + config.params[ "GENERAL" ][ "ZERO" ] ) )
          hist_PDF[ "PDFDN" ].Scale( hist_PDF[ "NOMINAL" ].Integral() / ( hist_PDF[ "PDFDN" ].Integral() + config.params[ "GENERAL" ][ "ZERO" ] ) )
        
        for shift in [ "UP", "DN" ]:
          hist_PDF[ "PDF__{}_{}".format( shift, args.year ) ] = hist_PDF[ "PDF{}".format( shift ) ].Clone( "PDF__{}_{}".format( shift, args.year ) )
          count += 1
    print( "[DONE] Adjusted {} PDF systematic histograms".format( count ) )
          
  def add_smooth_shapes(): # kinda done
    print( "[START] Smoothing systematic shapes using {} smoothing".format( self.params[ "SMOOTHING ALGO" ] ) )
    count = 0
    for hist_key in [ "BKG", "SIG" ]:
      for hist_name in self.rebinned[ hist_key ]:
        syst, syst_name = syst_parse( hist_name )
        if syst.upper() + "UP" in hist_name.upper() and syst_name.upper() not in [ syst_exclude.upper() for syst_exclude in self.params[ "EXCLUDE SMOOTH" ] ]:
          hist_syst = {
            "NOMINAL": self.rebinned[ hist_key ][ hist_name.replace( "_{}UP".format( syst.upper() ), "" ) ].Clone( "NOMINAL" ),
            syst.upper() + "UP": self.rebinned[ hist_key ][ hist_name ].Clone( syst.upper() + "UP" ),
            syst.upper() + "DN": self.rebinned[ hist_key ][ hist_name ].Clone( syst.upper() + "DN" )
          }
          smooth_shape( hist_syst, self.params[ "SMOOTHING ALGO" ], self.params[ "SYMM SMOOTHING" ] )
          
          for shift in [ "UP", "DN" ]:
            self.rebinned[ hist_key ][ "{}__{}_{}".format( syst.upper(), shift, args.year ) ] = hist_syst[ syst.upper() + shift ].Clone( "{}__{}_{}".format( syst.upper(), shift, args.year ) )
            self.rebinned[ hist_key ][ "{}__{}_{}".format( syst.upper(), shift, args.year ) ].SetDirectory(0)
            count += 1
      print( "[DONE] Smoothed {} systematic histograms" )
    
    for process in groups[ "OUTPUT" ]:
      if "DAT" in process: continue
      syst_output = []
      for syst in syst_output:
        hist = {
          "NOMINAL": rFile_out.Get( "{}_{}".format( bin_name, process ) ),
          "UP": rFile_out.Get( "{}_{}UP".format( bin_name, process ) ),
          "DN": rFile_out.Get( "{}_{}DN".format( bin_name, process ) )
        }
        for shift in [ "UP", "DN" ]: 
          hist[ "SMOOTH" + shift ] = smooth_shape( hist[ "NOMINAL" ], hist[ "UP" ], hist[ "DN" ], config.smoothing_algo, args.smoothing )
          hist[ "SMOOTH" + shift ].Write()
          yields[ hist[ "SMOOTH" + shift ].GetName() ] = hist[ "SMOOTH" + shift ].Integral()
          hist[ "LIMIT" + shift ] = hist[ "SMOOTH" + shift ].Clone( hist[ "SMOOTH" + shift ].GetName().replace( shift, "_{}{}".format( args.year, shift ) ) )
          hist[ "LIMIT" + shift ].Write()
  
  def write( self ):
    self.outpath = self.filepath.replace( ".root", "_rebinned_stat{}.root".format( self.params[ "STAT THRESHOLD" ].replace( ".", "p" ) ) )
    print( "[START] Storing modified histograms in {}".format( self.outpath ) )
    self.rFile[ "OUTPUT" ] = ROOT.TFile( self.outpath, "RECREATE" )
    count = 0
    for hist_key in self.rebinned:
      for hist_name in self.rebinned[ hist_key ]:
        self.rebinned[ hist_key ][ hist_name ].Write()
        count += 1
    print( "[DONE] {} histograms written.".format( count ) )
    self.rFile[ "OUTPUT" ].Close()
    
def get_shape_uncertainty( hists, process, channel ): # needs some fixes to the hist name 
  if not args.add_shapes: return 0
  systematics = sorted( [ hist_name[ hist_name.find( process ) + len( process ) + 2: hist_name.find( "UP" ) ] for hist_name in yields[ channel ].keys() if channel in hist_name and process in hist_name and "UP" in hist_name ] )
  total_shift = { shift: 0 for shift in [ "UP", "DN" ] }
  prefix = hist_names[ channel ][ "ALL" ][0][:hist_names[ channel ][ "ALL" ]]
  hist_nominal = hist_names[ channel ][ process ]
  for syst in config.systematics["MC"]:
    if syst in systematics_remove or ( args.smoothing and config.smooth_algo not in syst ): continue
    if args.norm_theory_sig and process in groups[ "SIG" ][ "PROCESS" ] and ( "PDF" in syst or "MURF" in syst or "ISR" in syst or "FSR" in syst or "PSWEIGHT" in syst ): continue
    if args.norm_theory_bkg and process not in groups[ "SIG" ][ "PROCESS" ] and ( "PDF" in syst or "MURF" in syst or "ISR" in syst or "FSR" in syst or "PSWEIGHT" in syst ): continue
    for shift in [ "UP", "DN" ]:
      hist_shape = "{}{}_{}{}".format( prefix, process, syst, shift )
      shift = yields[ channel ][ hist_names[ channel ][ process ].GetName() ] / ( yields[ channel ][ nominal ] + config.zero ) - 1
      if shift > 0: total_shift[ shift ] += shift**2
      if shift < 0: total_shift[ shift ] += shift**2
    shape_uncertainty_percent = ( math.sqrt( total_shift[ "UP" ] ) + math.sqrt( total_shift[ "DN" ] ) ) / 2
    return shape_uncertainty_percent
    
def print_tables():
  table = []
  table = yield_tables( table )
  table = systematic_tables( table )
  summary_templates()
  
def main():
  # parse options and parameters
  template_prefix = config.region_prefix[ args.region ]
  templateDir = os.path.join( os.getcwd(), "{}_UL{}_{}".format( template_prefix, args.year, args.tag ) )
  
  params = config.params[ "MODIFY BINNING" ].copy()
  options = config.options[ "MODIFY BINNING" ].copy()
  if args.region == "BASELINE":
    print( "[WARN] Running BASELINE region, overriding the following options and parameters:" )
    print( "   > STAT THRESHOLD: {} --> 1.1".format( params[ "STAT THRESHOLD" ] ) )
    print( "   > SMOOTHING: {} --> False".format( options[ "SMOOTH" ] ) )
    params[ "STAT THRESHOLD" ] = 1.1 
    options[ "SMOOTH" ] = False
    if args.variable.upper() == "HT" or args.variable.upper() == "LEPPT":
      print( "   > MIN MERGE ({}): {} --> 4".format( args.variable, params[ "MIN MERGE" ] ) )
      params[ "MIN MERGE" ] = 4
    elif "NJET" in args.variable.upper() or "NBJET" in args.variable.upper() or "NHOT" in args.variable.upper():
      print( "   > MIN MERGE ({}): {} --> 1".format( args.variable, params[ "MIN MERGE" ] ) )
      params[ "MIN MERGE" ] = 1
    else:
      print( "   > MIN MERGE: {} --> 2".format( params[ "MIN MERGE" ] ) )
      params[ "MIN MERGE" ] = 2
  else:
    if not config.params[ "GENERAL" ][ "FINAL ANALYSIS" ]:
      print( "[WARN] Running {} region, turning on blinding".format( args.region ) )
      options[ "BLIND" ] = True
    
  file_name = "template_combine_{}_UL{}.root".format( args.variable, args.year ) 
  file_path = os.path.join( templateDir, file_name )

  # default rebin/merge histograms
  template = ModifyTemplate( file_path, options, params, samples.groups, args.variable )  
  
  ## handling systematics
  #if options[ "TRIGGER EFFICIENCY" ]:
  #  template.add_trigger_efficiency()
  #if options[ "UNCORRELATE YEARS" ]:
  #  template.uncorrelate_years()
  #if params[ "SYMM TOP PT" ]:
  #  template.symmetrize_topPT_shift()
  #if params[ "SYMM HOTCLOSURE" ]:
  #  template.symmetrize_HOTclosure()
  #if params[ "SHAPE STAT" ]:
  #  template.add_statistical_shapes()
  #if params[ "MURF SHAPES" ]:
  #  template.add_muRF_shapes()
  #if params[ "PS WEIGHTS" ]:
  #  template.add_PS_weights()
  #if params[ "PDF" ]:
  #  template.add_PDF_shapes()
  #if params[ "SMOOTH" ]:
  #  template.add_smooth_shapes()
    
  
  # calculate yields
  template.compute_yield_stats()
    
  #print_tables( template.table )
        
  #template.write()
  
main()
