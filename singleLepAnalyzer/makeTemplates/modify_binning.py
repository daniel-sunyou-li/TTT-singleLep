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

def hist_parse( hist_name ):
  parse = {
    "PROCESS": "",
    "GROUP": "",
    "SYST": "",
    "IS SYST": False,
    "CATEGORY": "",
    "CHANNEL": ""
  }
  parts = hist_name.split( "_" )
  for part in parts:
    # handle process first
    if part in samples.groups[ "SIG" ][ "PROCESS" ] + [ "SIG" ]:
      parse[ "PROCESS" ] = part
      parse[ "GROUP" ] = "SIG"
    elif part in samples.groups[ "BKG" ][ "PROCESS" ].keys():
      parse[ "PROCESS" ] = part
      parse[ "GROUP" ] = "BKG"
    elif part in samples.groups[ "BKG" ][ "SUPERGROUP" ].keys():
      parse[ "PROCESS" ] = part
      parse[ "GROUP" ] = "BKG"
    elif part in samples.groups[ "DAT" ][ "PROCESS" ] + [ "DAT" ]:
      parse[ "PROCESS" ] = part
      parse[ "GROUP" ] = "DAT"
    # handle systematic
    if part.endswith( "UP" ) or part.endswith( "DN" ):
      parse[ "SYST" ] = part[:-2]
      parse[ "IS SYST" ] = True
    elif "PDF" in part:
      parse[ "SYST" ] = "PDF"
      parse[ "IS SYST" ] = True
    # handle category
    if part.startswith( "isE" ) or part.startswith( "isM" ) or part.startswith( "isL" ):
      parse[ "CATEGORY" ] = part
      parse[ "CHANNEL" ] = part[3:]
  return parse


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

def negative_bin_correction( hist ):
  integral = hist.Integral()
  for i in range( 0, hist.GetNbinsX() + 2 ):
    if hist.GetBinContent(i) < 0:
      hist.SetBinContent( i, config.params[ "GENERAL" ][ "ZERO" ] )
      hist.SetBinError( i, config.params[ "GENERAL" ][ "ZERO" ] )
  if hist.Integral() != 0 and integral > 0: 
    hist.Scale( integral / hist.Integral() )


def smooth_shape( hist_n, hist_d, hist_u, algo = "lowess" , symmetrize = True ):
  hist_name = hist_n.GetName()
  graph_error = {
    path: {
      shift: ROOT.TGraphErrors() for shift in [ "UP", "DN" ]
    } for path in [ "IN", "OUT" ]
  }
  graph_smooth = {
    shift: ROOT.TGraphSmooth( hist_name + "_{}_{}".format( shift, algo.upper() ) ) for shift in [ "UP", "DN" ]
  }
  hist = {
    path: {
      "UP": hist_u.Clone( "{}__{}".format( hist_n.GetName(), algo.upper() ) ),
      "DN": hist_d.Clone( "{}__{}".format( hist_d.GetName(), algo.upper() ) )
    } for path in [ "IN", "OUT" ]
  }
  for shift in [ "UP", "DN" ]:
    hist[ "IN" ][ shift ].Divide( hist_n )

  for i in range( 1, hist_n.GetNbinsX() + 1 ):
    x = ( hist[ "IN" ][ "UP" ].GetBinLowEdge(i) + hist[ "IN" ][ "UP" ].GetBinLowEdge(i+1) ) / 2
    y = {
      "UP": hist[ "IN" ][ "UP" ].GetBinContent(i),
      "DN": hist[ "IN" ][ "DN" ].GetBinContent(i)
    }
    for shift in [ "UP", "DN" ]:
      if symmetrize:
        graph_error[ "IN" ][ shift ].SetPoint( i - 1, x, 1 + ( y[ "UP" ] + y[ "DN" ] ) / 2 )
      else:
        graph_error[ "IN" ][ shift ].SetPoint( i - 1, x, y[ shift ] )
  for shift in [ "UP", "DN" ]:
    if algo.upper() == "SUPER":
      graph_error[ "OUT" ][ shift ] = graph_smooth[ shift ].SmoothSuper( graph_error[ "IN" ][ shift ], "", 9, 0 )
    elif algo.upper() == "KERN":
      graph_error[ "OUT" ][ shift ] = graph_smooth[ shift ].SmoothKern( graph_error[ "IN" ][ shift ], "normal", 5.0 )
    elif algo.upper() == "LOWESS":
      graph_error[ "OUT" ][ shift ] = graph_smooth[ shift ].SmoothLowess( graph_error[ "IN" ][ shift ], "", 0.9 )

  for i in range( 1, hist_n.GetNbinsX() + 1 ):
    for shift in [ "UP", "DN" ]:
      hist[ "OUT" ][ shift ].SetBinContent( i, hist_n.GetBinContent(i) * graph_error[ "OUT" ][ shift ].GetY()[i-1] )
  return hist[ "OUT" ]

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
    syst_log = { key: [] for key in [ "SIG SYST", "BKG SYST" ] }
    self.histograms = { key: {} for key in [ "BKG", "BKG SYST", "SIG", "SIG SYST", "DAT", "TOTAL BKG", "TOTAL SIG", "TOTAL DAT" ] }
    count = 0
    print( "[INFO] Found {} histograms".format( len( self.hist_names ) ) ) 
    for hist_name in sorted( self.hist_names ):
      parse = hist_parse( hist_name ) 
      if parse[ "CATEGORY" ] not in category_log[ "ALL" ]:
        category_log[ "ALL" ].append( parse[ "CATEGORY" ] )

      if parse[ "GROUP" ] == "DAT":
        if args.verbose and not parse[ "IS SYST" ]: print( "   + DAT: {}".format( hist_name ) )
        self.histograms[ "DAT" ][ hist_name ] = self.rFile[ "INPUT" ].Get( hist_name ).Clone( hist_name )
        if parse[ "CATEGORY" ] not in category_log[ "DAT" ]:
          self.histograms[ "TOTAL DAT" ][ parse[ "CATEGORY" ] ] = self.histograms[ "DAT" ][ hist_name ].Clone( "DAT_TOTAL_{}".format( parse[ "CATEGORY" ] ) )
          category_log[ "DAT" ].append( parse[ "CATEGORY" ] )
        else:
          self.histograms[ "TOTAL DAT" ][ parse[ "CATEGORY" ] ].Add( self.histograms[ "DAT" ][ hist_name ] )
      elif parse[ "GROUP" ] == "BKG":
        if args.verbose and not parse[ "IS SYST" ]: print( "   + BKG: {}".format( hist_name ) )
        if parse[ "IS SYST" ]:
          self.histograms[ "BKG SYST" ][ hist_name ] = self.rFile[ "INPUT" ].Get( hist_name ).Clone( hist_name )
          if parse[ "SYST" ] not in syst_log[ "BKG SYST" ]: syst_log[ "BKG SYST" ].append( parse[ "SYST" ] )
        else:
          self.histograms[ "BKG" ][ hist_name ] = self.rFile[ "INPUT" ].Get( hist_name ).Clone( hist_name )   
          if parse[ "CATEGORY" ] not in category_log[ "BKG" ]:
            self.histograms[ "TOTAL BKG" ][ parse[ "CATEGORY" ] ] = self.histograms[ "BKG" ][ hist_name ].Clone( "BKG_TOTAL_{}".format( parse[ "CATEGORY" ] ) )
            category_log[ "BKG" ].append( parse[ "CATEGORY" ] )
          else:
            self.histograms[ "TOTAL BKG" ][ parse[ "CATEGORY" ] ].Add( self.histograms[ "BKG" ][ hist_name ] )
      elif parse[ "GROUP" ] == "SIG":
        if args.verbose and not parse[ "IS SYST" ]: print( "   + SIG: {}".format( hist_name ) )
        if parse[ "IS SYST" ]:
          self.histograms[ "SIG SYST" ][ hist_name ] = self.rFile[ "INPUT" ].Get( hist_name ).Clone( hist_name )
          if parse[ "SYST" ] not in syst_log[ "SIG SYST" ]: syst_log[ "SIG SYST" ].append( parse[ "SYST" ] )
        else:
          self.histograms[ "SIG" ][ hist_name ] = self.rFile[ "INPUT" ].Get( hist_name ).Clone( hist_name )
          if parse[ "CATEGORY" ] not in category_log[ "SIG" ]:
            self.histograms[ "TOTAL SIG" ][ parse[ "CATEGORY" ] ] = self.histograms[ "SIG" ][ hist_name ].Clone( "SIG_TOTAL_{}".format( parse[ "CATEGORY" ] ) )
            category_log[ "SIG" ].append( parse[ "CATEGORY" ] )
          else:
            self.histograms[ "TOTAL SIG" ][ parse[ "CATEGORY" ] ].Add( self.histograms[ "SIG" ][ hist_name ] )
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
        parse = hist_parse( name_lepton )
        self.histograms[ key ][ name_lepton ] = self.histograms[ key ][ hist_name ].Clone( name_lepton )
        self.histograms[ key ][ name_lepton ].Add( self.histograms[ key ][ hist_name.replace( "isE", "isM" ) ] )
        if not parse[ "IS SYST" ]: print( "     + {}: {}".format( name_lepton, self.histograms[ key ][ name_lepton ].Integral() ) )  
      if "SYST" in key:
        for syst in syst_log[ key ]:
          print( "    + {}".format( syst ) )
    total_count = 0
    for hist_key in self.histograms:
      for hist_name in self.histograms[ hist_key ]:
        self.histograms[ hist_key ][ hist_name ].SetDirectory(0)
        total_count += 1

    self.rFile[ "INPUT" ].Close()
    print( "[DONE] Found {} histograms, loaded {} histograms".format( count, total_count ) )
  
  def get_xbins( self ): # done
  # get the new histogram bins that satisfy the requirement bin error / yield <= threshold
    print( "[START] Determining modified histogram binning" )
    self.xbins = { key: {} for key in [ "MERGED", "LIMIT", "MODIFY" ] } 
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
              if math.sqrt( bin_content[ "isM" ][ "TOTAL BKG" ][ "ERROR" ] ) / bin_content[ "isM" ][ "TOTAL BKG" ][ "YIELD" ] <= self.params[ "STAT THRESHOLD" ]:
                for key_type in [ "TOTAL BKG", "TOTAL DAT" ]:
                  for key_lep in [ "isE", "isM" ]:
                    for key_stat in [ "YIELD", "ERROR" ]:
                      bin_content[ key_lep ][ key_type ][ key_stat ] = 0
                      N_MERGED = 0
                self.xbins[ "MERGED" ][ channel ].append( self.histograms[ "TOTAL BKG" ][ "isL" + channel ].GetXaxis().GetBinLowEdge( N_BINS + 1 - i ) ) 
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
      i = 1
      print( ">> {} original binning: [{},{}] ({})".format( channel, self.xbins[ "LIMIT" ][ channel ][0], self.xbins[ "LIMIT" ][ channel ][-1], N_BINS ) )
      while i < len( self.xbins[ "LIMIT" ][ channel ] ) - 1:
        if self.xbins[ "LIMIT" ][ channel ][i] <= self.xbins[ "LIMIT" ][ channel ][0] or self.xbins[ "LIMIT" ][ channel ][i] >= self.xbins[ "LIMIT" ][ channel ][-1]:
          del self.xbins[ "LIMIT" ][ channel ][i]
        else:
          i += 1
          
      self.xbins[ "MODIFY" ][ channel ] = array( "d", self.xbins[ "LIMIT" ][ channel ] )
      print( "   + New binning: [{},{}] ({}) with {} threshold".format( 
        self.xbins[ "MODIFY" ][ channel ][0], self.xbins[ "MODIFY" ][ channel ][1], i + 1, 
        self.params[ "STAT THRESHOLD" ] 
      ) )
        
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
  
  def compute_yield_stats( self ): # done
  # get the integral yield for each bin as well as the associated error
    print( "[START] Retrieving yields and errors for each histogram's bins." )
    count = 0
    for hist_key in self.rebinned:
      print( ">> Retrieving yields and errors for {}".format( hist_key ) )
      self.yields[ hist_key ] = {}
      hist_names = sorted( self.rebinned[ hist_key ].keys() )
      for hist_name in hist_names:
        parse = hist_parse( hist_name )
        self.yields[ hist_key ][ hist_name ] = {
          "COUNT": self.rebinned[ hist_key ][ hist_name ].Integral(),
          "ERROR": 0
        }
        for i in range( 1, self.rebinned[ hist_key ][ hist_name ].GetXaxis().GetNbins() + 1 ):
          self.yields[ hist_key ][ hist_name ][ "ERROR" ] += self.rebinned[ hist_key ][ hist_name ].GetBinError(i)**2
        self.yields[ hist_key ][ hist_name ][ "ERROR" ] = math.sqrt( self.yields[ hist_key ][ hist_name ][ "ERROR" ] )
        if args.verbose and not parse[ "IS SYST" ]: 
          print( "   + {}: {:.2f} pm {:.2f}".format( 
            hist_name, 
            self.yields[ hist_key ][ hist_name ][ "COUNT" ],
            self.yields[ hist_key ][ hist_name ][ "ERROR" ]
          ) )
        count += 1
    print( "[DONE] Calculated yields for {} histograms".format( count ) )  
          
  def add_trigger_efficiency( self ): # done
  # specify trigger efficiencies for the single leptons
    print( "[START] Differentiating trigger efficiency histogram naming between lepton flavors" )
    count = 0
    for hist_key in [ "BKG SYST", "SIG SYST" ]:
      hist_names = self.rebinned[ hist_key ].keys()
      for hist_name in hist_names:
        parse = hist_parse( hist_name )
        if parse[ "SYST" ].upper() !=  "TRIGEFF": continue
        if parse[ "CATEGORY" ].startswith( "isE" ):
          hist_name_el = self.rebinned[ hist_key ][ hist_name ].GetName().replace( "TRIGEFF", "ELTRIGGEFF" )
          self.rebinned[ hist_key ][ hist_name_el ] = self.rebinned[ hist_key ][ hist_name ].Clone( hist_name_el )
          self.rebinned[ hist_key ][ hist_name_el ].SetDirectory(0)
          count += 1
        if parse[ "CATEGORY" ].startswith( "isM" ):
          hist_name_mu = self.rebinned[ hist_key ][ hist_name ].GetName().replace( "TRIGEFF", "MUTRIGGEFF" )
          self.rebinned[ hist_key ][ hist_name_mu ] = self.rebinned[ hist_key ][ hist_name ].Clone( hist_name_mu )
          self.rebinned[ hist_key ][ hist_name_el ].SetDirectory(0)
          count += 1
    print( "[DONE] Adjusted trigger naming for {} histograms.".format( count ) )
    
  def uncorrelate_years( self ): # done
  # differentiate the shifts by year
    print( "[START] Differentiating systematic shifts by year" )
    count = 0
    for hist_key in [ "BKG SYST", "SIG SYST" ]:
      hist_names = self.rebinned[ hist_key ].keys()
      for hist_name in hist_names:
        parse = hist_parse( hist_name )
        if parse[ "IS SYST" ]:
          hist_name_new = self.rebinned[ hist_key ][ hist_name ].GetName().replace( "UP_", "{}UP_".format( args.year ) ).replace( "DN_", "{}DN_".format( args.year ) )
          self.rebinned[ hist_key ][ hist_name_new ] = self.rebinned[ hist_key ][ hist_name ].Clone( hist_name_new )
          self.rebinned[ hist_key ][ hist_name_new ].SetDirectory(0)
          count += 1
    print( "[DONE] Adjusted systematic shift names by year for {} histograms".format( count ) )
    
  def symmetrize_topPT_shift( self ): # done
  # symmetrize the up and down shifts for toppt systematic
    print( "[START] Symmetrizing the toppt systematic shifts" )
    count = 0
    for hist_key in [ "SIG SYST", "BKG SYST" ]:
      hist_names = self.rebinned[ hist_key ].keys()
      for hist_name in hist_names:
        if "TOPPTDN" not in hist_name.upper(): continue # adjust TOPPTDN to TOPPTUP
        for i in range( 1, self.rebinned[ hist_key ][ hist_name ].GetNbinsX() + 1 ):
          self.rebinned[ hist_key ][ hist_name ].SetBinContent(
            i, 2. * self.rebinned[ hist_key ][ hist_name.replace( "_TOPPTDN", "" ) ].GetBinContent(i) - self.rebinned[ hist_key ][ hist_name.replace( "DN", "UP" ) ].GetBinContent(i) 
          )
        count += 1
    print( "[DONE] Adjusted {} toppt histograms".format( count ) )

  def add_statistical_shapes( self ): # done
  # add shifts to the bin content for the statistical shape uncertainty
    def write_statistical_hists( category, group, i, nBB ):
      count = { key: 0 for key in [ "NEGATIVE", "ZERO" ] }
      if self.rebinned[ "TOTAL BKG" ][ category ].GetNbinsX() == 1 or group == "SIG":  
        hist_names = self.rebinned[ group ].keys()
        for hist_name in sorted( hist_names ):
          parse = hist_parse( hist_name )
          if parse[ "IS SYST" ]: continue
          yields = {
            "COUNT": self.rebinned[ group ][ hist_name ].GetBinContent(i),
            "ERROR": self.rebinned[ group ][ hist_name ].GetBinError(i)
          }
          if yields[ "COUNT" ] == 0: continue
          shift_name = { 
            shift: "{}_{}_BIN{}_{}".format( parse[ "PROCESS" ], category, i, shift ) for shift in [ "UP", "DN" ] 
          }
          for shift in [ "UP", "DN" ]:
            self.rebinned[ group ][ shift_name[ shift ] ] = self.rebinned[ group ][ hist_name ].Clone( shift_name[ shift ] ) 
            if shift == "UP": self.rebinned[ group ][ shift_name[ shift ] ].SetBinContent( i, yields[ "COUNT" ] + yields[ "ERROR" ] )
            if shift == "DN": self.rebinned[ group ][ shift_name[ shift ] ].SetBinContent( i, yields[ "COUNT" ] - yields[ "ERROR" ] )
            if yields[ "COUNT" ] - yields[ "ERROR" ] < 0:
              negative_bin_correction( self.rebinned[ group ][ shift_name[ shift ] ] )
              count[ "NEGATIVE" ] += 1
            if yields[ "COUNT" ] - yields[ "ERROR" ] == 0:
              self.rebinned[ group ][ shift_name[ shift ] ].SetBinContent( i, yields[ "COUNT" ] * config.params[ "GENERAL" ][ "ZERO" ] )
              count[ "ZERO" ] += 1
            self.rebinned[ group ][ shift_name[ shift ] ].SetDirectory(0)
          nBB[ group ] += 1
      else:
        bkg_max = ""
        count_max = 0
        bkg_names = self.rebinned[ "BKG" ].keys()
        for bkg_name in bkg_names:
          parse = hist_parse( bkg_name )
          if parse[ "IS SYST" ]: continue
          if count_max < self.rebinned[ "BKG" ][ bkg_name ].GetBinContent(i):
            count_max = self.rebinned[ "BKG" ][ bkg_name ].GetBinContent(i)
            bkg_max = bkg_name
        error_max = self.rebinned[ "BKG" ][ bkg_max ].GetBinError(i)
        parse = hist_parse( bkg_max )
        shift_name = {
          shift: "{}_{}_BIN{}_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], i, shift ) for shift in [ "UP", "DN" ]
        }
        count = { key: 0 for key in [ "NEGATIVE", "ZERO" ] }
        for shift in [ "UP", "DN" ]:
          self.rebinned[ "BKG" ][ shift_name[ shift ] ] = self.rebinned[ "BKG" ][ bkg_max ].Clone( shift_name[ shift ] )
          if shift == "UP": self.rebinned[ "BKG" ][ shift_name[ shift ] ].SetBinContent( i, count_max + error_max )
          if shift == "DN": self.rebinned[ "BKG" ][ shift_name[ shift ] ].SetBinContent( i, count_max - error_max )
          if count_max - error_max < 0:
            negative_bin_correction( self.rebinned[ "BKG" ][ shift_name[ shift ] ] )
            count[ "NEGATIVE" ] += 1
          if count_max - error_max == 0:
            self.rebinned[ "BKG" ][ shift_name[ shift ] ].SetBinContent( i, count_max * 0.001 )
            count[ "ZERO" ] += 1
          self.rebinned[ "BKG" ][ shift_name[ shift ] ].SetDirectory(0)
        nBB[ "BKG" ] += 1
      if args.verbose and ( count[ "NEGATIVE" ] > 0 or count[ "ZERO" ] > 0 ):
        print( "[INFO] Corrections for {}, bin {}/{}:".format( hist_name, i, self.rebinned[ group ][ hist_name ].GetNbinsX() ) )
        print( "   + Negative Correction: {}".format( count[ "NEGATIVE" ] ) )
        print( "   + Zero Correction: {}".format( count[ "ZERO" ] ) )
          
    print( "[START] Adding statistical shape systematics, excluding bins beneath {} significance:".format( self.params[ "THRESHOLD BB" ] ) )
    nBB = { "BKG": 0, "SIG": 0 }
    hist_names = self.rebinned[ "TOTAL BKG" ].keys()
    for category in self.categories:
      count = { "INCLUDE": 0, "EXCLUDE": 0 }
      for i in range( 1, self.rebinned[ "TOTAL BKG" ][ category ].GetNbinsX() + 1 ):
        error_ratio = self.rebinned[ "TOTAL BKG" ][ category ].GetBinError(i) / self.rebinned[ "TOTAL BKG" ][ category ].GetBinContent(i)
        if error_ratio <= self.params[ "THRESHOLD BB" ]: # don't include the bin shape uncertainty if it's already very small
          count[ "EXCLUDE" ] += 1
          continue
        write_statistical_hists( category, "SIG", i, nBB )
        write_statistical_hists( category, "BKG", i, nBB )
        count[ "INCLUDE" ] += 1
      print( "[INFO] {}: {}/{} bins shapes included".format( category, count[ "INCLUDE" ], count[ "EXCLUDE" ] + count[ "INCLUDE" ] ) )
    print( "[DONE] {} Signal bin shapes added, {} Background bin shapes added".format( nBB[ "SIG" ], nBB[ "BKG" ] ) )
      

  def symmetrize_HOTclosure( self ): # done
    # make the up and down shifts of the HOTClosure systematic symmetric
    print( "[START] Symmetrizing the HOT closure systematic down shifts to match the up shifts" )
    count = 0
    for hist_key in [ "SIG SYST", "BKG SYST" ]:
      hist_names = self.rebinned[ hist_key ].keys()
      for hist_name in hist_names:
        if "HOTCLOSUREUP" not in hist_name.upper(): continue
        HOT_name = {
          "NOM": hist_name.replace( "_HOTCLOSUREUP", "" ),
          "UP": hist_name,
          "DN": hist_name.replace( "UP", "DN" )
        }
        for i in range( 1, self.rebinned[ hist_key ][ hist_name ].GetNbinsX() + 1 ):
          max_shift = max(
            abs( self.rebinned[ hist_key.split( " " )[0] ][ HOT_name[ "NOM" ] ].GetBinContent(i) - self.rebinned[ hist_key ][ HOT_name[ "UP" ] ].GetBinContent(i) ),
            abs( self.rebinned[ hist_key.split( " " )[0] ][ HOT_name[ "NOM" ] ].GetBinContent(i) - self.rebinned[ hist_key ][ HOT_name[ "DN" ] ].GetBinContent(i) )
          )
          self.rebinned[ hist_key ][ HOT_name[ "UP" ] ].SetBinContent( i, self.rebinned[ hist_key.split( " " )[0] ][ HOT_name[ "NOM" ] ].GetBinContent(i) + max_shift )
          self.rebinned[ hist_key ][ HOT_name[ "DN" ] ].SetBinContent( i, self.rebinned[ hist_key.split( " " )[0] ][ HOT_name[ "NOM" ] ].GetBinContent(i) - max_shift )
        count += 1
    print( "[DONE] Adjusted the HOT closure systematic shift for {} histograms".format( count ) )    
    
  def add_muRF_shapes( self ): # done
  # adding MU RF systematic shapes
    print( "[START] Adding MU R+F systematic shapes" )
    count = 0
    for hist_key in [ "SIG SYST", "BKG SYST" ]:
      hist_names = self.rebinned[ hist_key ].keys()
      for hist_name in hist_names:
        parse = hist_parse( hist_name )
        if "MURUP" not in hist_name.upper(): continue
        hist_muRF = { "NOMINAL": self.rebinned[ hist_key.split( " " )[0] ][ hist_name.replace( "_MURUP", "" ) ].Clone() }
        for syst in [ "MURUP", "MURDN", "MUFUP", "MUFDN", "MURFCORRDUP", "MURFCORRDDN" ]:
          hist_muRF[ syst ] = self.rebinned[ hist_key ][ hist_name.replace( "MURUP", syst ) ].Clone()
        hist_muRF[ "MURFUP" ] = self.rebinned[ hist_key ][ hist_name ].Clone()
        hist_muRF[ "MURFDN" ] = self.rebinned[ hist_key ][ hist_name ].Clone()
        for i in range( 1, hist_muRF[ "NOMINAL" ].GetNbinsX() + 1 ):
          weight_dict = { key: hist_muRF[ key ].Clone() for key in hist_muRF }
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

        if self.options[ "NORM THEORY {}".format( hist_key ) ]:
          hist_muRF[ "MURFUP" ].Scale( hist_muRF[ "NOMINAL" ].Integral() / ( hist_muRF[ "MURFUP" ].Integral() + config.params[ "GENERAL" ][ "ZERO" ] ) )
          hist_muRF[ "MURFDN" ].Scale( hist_muRF[ "NOMINAL" ].Integral() / ( hist_muRF[ "MURFDN" ].Integral() + config.params[ "GENERAL" ][ "ZERO" ] ) )

        for shift in [ "UP", "DN" ]:
          self.rebinned[ hist_key ][ "{}_{}_MURF_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], shift ) ] = hist_muRF[ "MURF{}".format( shift ) ].Clone( "{}_{}_MURF_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], shift ) )
          self.rebinned[ hist_key ][ "{}_{}_MURF_{}_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], shift, args.year ) ] = hist_muRF[ "MURF{}".format( shift ) ].Clone( "{}_{}_MURF_{}_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], shift, args.year ) )
          self.rebinned[ hist_key ][ "{}_{}_MURF_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], shift ) ].SetDirectory(0)
          self.rebinned[ hist_key ][ "{}_{}_MURF_{}_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], shift, args.year ) ].SetDirectory(0)
          count += 2 
    print( "[DONE] Created {} MU R+F histograms".format( count ) ) 
  
  def add_PSWeight_shapes( self ): # done
    print( "[START] Adding PS weights systematics" )
    count = 0
    for hist_key in [ "SIG SYST", "BKG SYST" ]:
      hist_names = self.rebinned[ hist_key ].keys()
      for hist_name in hist_names:
        parse = hist_parse( hist_name )
        if "ISRUP" not in hist_name.upper(): continue
        hist_PSWeight = { "NOMINAL": self.rebinned[ hist_key.split( " " )[0] ][ hist_name.replace( "_ISRUP", "" ) ].Clone() }
        hist_PSWeight[ "PSWGTUP" ] = self.rebinned[ hist_key ][ hist_name ].Clone()
        hist_PSWeight[ "PSWGTDN" ] = self.rebinned[ hist_key ][ hist_name ].Clone()
        for syst in [ "ISR", "FSR" ]:
          for shift in [ "UP", "DN" ]:
            hist_PSWeight[ syst + shift ] = self.rebinned[ hist_key ][ hist_name.replace( "ISRUP", syst + shift ) ].Clone()
        for i in range( 1, hist_PSWeight[ "NOMINAL" ].GetNbinsX() + 1 ):
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
            if hist_PSWeight[ key ].GetBinContent(i) < weight_limit[ "MIN" ]:
              weight_limit[ "MIN" ] = hist_PSWeight[ key ].GetBinContent(i)
              weight_error[ "MIN" ] = hist_PSWeight[ key ].GetBinError(i)
              weight_key[ "MIN" ] = key
        
          # in-case symmetrization is needed for PSWGTUP:
          # hist_PSWeight[ "PSWGTUP" ].SetBinContent( i, 2 * hist_PSWeight[ "NOMINAL" ].GetBinContent(i) - weight_limit[ "MIN" ].GetBinContent(i) )
          hist_PSWeight[ "PSWGTUP" ].SetBinContent( i, weight_limit[ "MAX" ] )
          hist_PSWeight[ "PSWGTUP" ].SetBinError( i, weight_error[ "MAX" ] )
          hist_PSWeight[ "PSWGTDN" ].SetBinContent( i, weight_limit[ "MIN" ] )
          hist_PSWeight[ "PSWGTDN" ].SetBinError( i, weight_error[ "MIN" ] )
        
        if self.options[ "NORM THEORY {}".format( hist_key ) ]:
          for shift in [ "UP", "DN" ]:
            for syst in [ "PSWGT", "ISR", "FSR" ]:
              hist_PSWeight[ syst + shift ].Scale( hist_PSWeight[ "NOMINAL" ].Integral() / ( hist_PSWeight[ syst + shift ].Integral() + config.params[ "GENERAL" ][ "ZERO" ] ) )
        
        for syst in [ "PSWGT", "ISR", "FSR" ]:
          for shift in [ "UP", "DN" ]:
            self.rebinned[ hist_key ][ "{}_{}_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], syst + shift ) ] = hist_PSWeight[ syst + shift ].Clone( "{}_{}_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], syst + shift ) )
            self.rebinned[ hist_key ][ "{}_{}_{}_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], syst + shift, args.year ) ] = hist_PSWeight[ syst + shift ].Clone( "{}_{}_{}_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], syst + shift, args.year ) )
            self.rebinned[ hist_key ][ "{}_{}_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], syst + shift ) ].SetDirectory(0)
            self.rebinned[ hist_key ][ "{}_{}_{}_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], syst + shift, args.year ) ].SetDirectory(0)
            count += 2

    print( "[DONE] Created {} PS Weight histograms".format( count ) )
          
  def add_PDF_shapes( self ): # done
    print( "[START] Adding PDF shape systematics" )
    count = 0
    for hist_key in [ "SIG SYST", "BKG SYST" ]:
      hist_names = self.rebinned[ hist_key ].keys()
      for hist_name in hist_names:
        parse = hist_parse( hist_name )
        if "PDF0" not in hist_name: continue
        hist_PDF = { 
          "NOMINAL": self.rebinned[ hist_key.split( " " )[0] ][ hist_name.replace( "_PDF0", "" ) ].Clone(),
          "PDFUP": self.rebinned[ hist_key ][ hist_name ].Clone(),
          "PDFDN": self.rebinned[ hist_key ][ hist_name ].Clone()
        }
        for i in range( config.params[ "GENERAL" ][ "PDF RANGE" ] ):
          hist_PDF[ "PDF{}".format(i) ] = self.rebinned[ hist_key ][ hist_name.replace( "PDF0", "PDF{}".format(i) ) ].Clone( "PDF{}".format(i) )
        for i in range( 1, hist_PDF[ "NOMINAL" ].GetNbinsX() + 1 ):
          weight_key = {
            "MAX": "PDF0",
            "MIN": "PDF0"
          }
          weight_limit = {
            "MAX": hist_PDF[ "PDF0" ].GetBinContent(i),
            "MIN": hist_PDF[ "PDF0" ].GetBinContent(i)
          }
          weight_error = {
            "MAX": hist_PDF[ "PDF0" ].GetBinError(i),
            "MIN": hist_PDF[ "PDF0" ].GetBinError(i)
          }
          for j in range( config.params[ "GENERAL" ][ "PDF RANGE" ] ):
            if hist_PDF[ "PDF{}".format(j) ].GetBinContent(i) > weight_limit[ "MAX" ]:
              weight_limit[ "MAX" ] = hist_PDF[ "PDF{}".format(j) ].GetBinContent(i)
              weight_error[ "MAX" ] = hist_PDF[ "PDF{}".format(j) ].GetBinError(i)
              weight_key[ "MAX" ] = key
            if hist_PDF[ "PDF{}".format(j) ].GetBinContent(i) < weight_limit[ "MIN" ]:
              weight_limit[ "MIN" ] = hist_PDF[ "PDF{}".format(j) ].GetBinContent(i)
              weight_error[ "MIN" ] = hist_PDF[ "PDF{}".format(j) ].GetBinError(i)
              weight_key[ "MIN" ] = key
          
          hist_PDF[ "PDFUP" ].SetBinContent( i, weight_limit[ "MAX" ] )
          hist_PDF[ "PDFUP" ].SetBinError( i, weight_error[ "MAX" ] )
          hist_PDF[ "PDFDN" ].SetBinContent( i, weight_limit[ "MIN" ] )
          hist_PDF[ "PDFDN" ].SetBinError( i, weight_error[ "MIN" ] )

        if self.options[ "NORM THEORY {}".format( hist_key ) ]:
          hist_PDF[ "PDFUP" ].Scale( hist_PDF[ "NOMINAL" ].Integral() / ( hist_PDF[ "PDFUP" ].Integral() + config.params[ "GENERAL" ][ "ZERO" ] ) )
          hist_PDF[ "PDFDN" ].Scale( hist_PDF[ "NOMINAL" ].Integral() / ( hist_PDF[ "PDFDN" ].Integral() + config.params[ "GENERAL" ][ "ZERO" ] ) )
        
        for shift in [ "UP", "DN" ]:
          self.rebinned[ hist_key ][ "{}_{}_PDF_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], shift ) ] = hist_PDF[ "PDF{}".format( shift ) ].Clone( "{}_{}_PDF_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], shift ) )
          self.rebinned[ hist_key ][ "{}_{}_PDF_{}_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], shift, args.year ) ] = hist_PDF[ "PDF{}".format( shift ) ].Clone( "{}_{}_PDF_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], shift, args.year ) )
          self.rebinned[ hist_key ][ "{}_{}_PDF_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], shift ) ].SetDirectory(0)
          self.rebinned[ hist_key ][ "{}_{}_PDF_{}_{}".format( parse[ "PROCESS" ], parse[ "CATEGORY" ], shift, args.year ) ].SetDirectory(0)
          count += 2

    print( "[DONE] Adjusted {} PDF systematic histograms".format( count ) )
          
  def add_smooth_shapes( self ): # done
    print( "[START] Smoothing systematic shapes using {} smoothing".format( self.params[ "SMOOTHING ALGO" ] ) )
    count = 0
    for hist_key in [ "BKG SYST", "SIG SYST" ]:
      hist_names = self.rebinned[ hist_key ].keys()
      for hist_name in hist_names:
        if "UP_" not in hist_name: continue
        parse = hist_parse( hist_name )
        if parse[ "SYST" ].upper() in [ syst_exclude.upper() for syst_exclude in self.params[ "EXCLUDE SMOOTH" ] ]: continue
        hist_syst = {
          "NOMINAL": self.rebinned[ hist_key.split( " " )[0] ][ hist_tag( args.variable, config.lumiStr[ args.year ], parse[ "CATEGORY" ], parse[ "PROCESS" ] ) ].Clone(),
          "UP": self.rebinned[ hist_key ][ hist_name ].Clone(),
          "DN": self.rebinned[ hist_key ][ hist_name.replace( "UP_", "DN_" ) ].Clone()
        }
        smooth_hist = smooth_shape( hist_syst[ "NOMINAL" ], hist_syst[ "DN" ], hist_syst[ "UP" ], algo = self.params[ "SMOOTHING ALGO" ] , symmetrize = self.options[ "SYMM SMOOTHING" ] )
        for shift in [ "UP", "DN" ]:
          smooth_name = "{}_{}".format( hist_name.replace( "{}UP".format( parse[ "SYST" ].upper() ), parse[ "SYST" ].upper() + shift ), self.params[ "SMOOTHING ALGO" ] )
          self.rebinned[ hist_key ][ smooth_name ] = smooth_hist[ shift ].Clone( smooth_name )
          self.rebinned[ hist_key ][ "{}_{}".format( smooth_name, args.year ) ] = smooth_hist[ shift ].Clone( "{}_{}".format( smooth_name, args.year ) )
          self.rebinned[ hist_key ][ smooth_name ].SetDirectory(0)
          self.rebinned[ hist_key ][ "{}_{}".format( smooth_name, args.year ) ].SetDirectory(0)
          count += 2
    print( "[DONE] Added {} smoothed systematic histograms".format( count ) )
      
  def write( self ):
    self.outpath = self.filepath.replace( ".root", "_rebinned_stat{}.root".format( str( self.params[ "STAT THRESHOLD" ] ).replace( ".", "p" ) ) )
    print( "[START] Storing modified histograms in {}".format( self.outpath ) )
    self.rFile[ "OUTPUT" ] = ROOT.TFile( self.outpath, "RECREATE" )
    count = 0
    for hist_key in self.rebinned:
      print( "   + {}".format( hist_key ) )
      for hist_name in self.rebinned[ hist_key ]:
        if "TOTAL" in hist_key: 
          self.rebinned[ hist_key ][ hist_name ].SetName( "TOTAL_{}_{}".format( hist_key.split( " " )[-1], hist_name ) )
        if "DAT" in hist_name:
          self.rebinned[ hist_key ][ hist_name ].SetName( self.rebinned[ hist_key ][ hist_name ].GetName().replace( "DAT", "data_obs" ) )
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
    if not config.options[ "GENERAL" ][ "FINAL ANALYSIS" ]:
      print( "[WARN] Running {} region, turning on blinding".format( args.region ) )
      options[ "BLIND" ] = True
    
  file_name = "template_combine_{}_UL{}.root".format( args.variable, args.year ) 
  file_path = os.path.join( templateDir, file_name )

  # default rebin/merge histograms
  template = ModifyTemplate( file_path, options, params, samples.groups, args.variable )  
  
  ## handling systematics
  if options[ "SYMM TOP PT" ]:
    template.symmetrize_topPT_shift()
  if options[ "TRIGGER EFFICIENCY" ]:
    template.add_trigger_efficiency()
  if options[ "UNCORRELATE YEARS" ]:
    template.uncorrelate_years()
  if options[ "SHAPE STAT" ]:
    template.add_statistical_shapes()
  if options[ "SYMM HOTCLOSURE" ]:
    template.symmetrize_HOTclosure()
  if options[ "MURF SHAPES" ]:
    template.add_muRF_shapes()
  if options[ "PS WEIGHTS" ]:
    template.add_PSWeight_shapes()
  if options[ "PDF" ]:
    template.add_PDF_shapes()
  if options[ "SMOOTH" ]:
    template.add_smooth_shapes()
   
  # calculate yields
  #template.compute_yield_stats()
    
  #print_tables( template.table )
        
  template.write()
  
main()
