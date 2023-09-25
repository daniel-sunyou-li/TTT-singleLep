#!/usr/bin/env python

import os, sys, math
import tqdm
import itertools
import ROOT
from argparse import ArgumentParser
sys.path.append( ".." )
from utils import hist_parse, abcdnn_tag
import config

parser = ArgumentParser()
parser.add_argument( "-y", "--year", default = "", help = "16APV,16,17,18" )
parser.add_argument( "-t", "--tag" )
parser.add_argument( "-r", "--region", help = ",".join( list( config.region_prefix.keys() ) ) )
parser.add_argument( "-v", "--variable" )
parser.add_argument( "-m", "--mode", default = 4, help = "0,1,2,3,4" )
parser.add_argument( "-c", "--card", help = "Datacard input to add systematic groups to" )
parser.add_argument( "--shapeSyst", action = "store_true" )
parser.add_argument( "--normSyst", action = "store_true" )
parser.add_argument( "--theorySyst", action = "store_true" )
parser.add_argument( "--xsecSyst", action = "store_true" )
parser.add_argument( "--verbose", action = "store_true" )
parser.add_argument( "--groups", action = "store_true", help = "Add systematic groups in datacard for systematic breakdown" )
args = parser.parse_args()

import CombineHarvester.CombineTools.ch as ch
import ROOT

if not args.groups:
  if args.year == "16APV": 
    import samplesUL16APV as samples
  elif args.year == "16":
    import samplesUL16 as samples
  elif args.year == "17": 
    import samplesUL17 as samples
  elif args.year == "18": 
    import samplesUL18 as samples
  else: quit( "[ERR] Invalid -y (--year) argument. Quitting" ) 

def jet_count( category ):
  parts = category.split( "n" )
  jet_count = 0
  for part in parts:
    if part.startswith("is"): continue
    elif part.startswith("HOT"): jet_count += int( part[3] )
    else: jet_count += int( part[1] )
  return jet_count

class DataCard():
  def __init__( self, variable, year, region, tag, params, options, samples, prefix ):
    self.harvester = ch.CombineHarvester()
    self.variable = variable
    self.year = year
    self.region = region
    self.abcdnn = options[ "ABCDNN" ]
    self.tag = tag
    self.lumistr = config.lumiStr[ self.year ]
    self.smooth = config.options[ "COMBINE" ][ "SMOOTH" ]
    self.smoothing = config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper()
    self.combine_sig = config.options[ "COMBINE" ][ "COMBINE SIGNALS" ]
    self.regions = {
      "SIGNAL":  [],
      "CONTROL": []
    }
    self.samples = samples
    self.params = params
    self.options = options
    self.prefix = prefix
    
    self.templateName = "template_combine_{}_UL{}_{}rebinned_merge{}_stat{}.root".format( 
      self.variable,
      self.year,
      "pseudo_" if config.options[ "MODIFY BINNING" ][ "TEST PSEUDO DATA" ] else "",
      config.params[ "MODIFY BINNING" ][ "MIN MERGE" ],
      str( config.params[ "MODIFY BINNING" ][ "STAT THRESHOLD" ] ).replace( ".", "p" )
    )
    self.templateDir = os.path.join( 
      os.getcwd(), 
      "../makeTemplates/", 
      "{}_UL{}_{}".format( 
        config.region_prefix[ args.region ],
        args.year,
        args.tag
      )
    )
     
    self.templatePath = os.path.join( self.templateDir, self.templateName )
    self.limitPath = "limits_UL{}_{}_{}_{}".format( self.year, self.variable, self.region, self.tag )
    if config.options[ "MODIFY BINNING" ][ "TEST PSEUDO DATA" ]:
      self.limitPath += "_pseudo"
    self.limitPath += "/"
    if not os.path.exists( self.limitPath ): os.system( "mkdir -v {}".format( self.limitPath ) )
    os.system( "cp -vp {} {}".format( self.templatePath, os.path.join( os.getcwd(), self.limitPath ) ) )
    
    templateFile = ROOT.TFile( os.path.join( self.limitPath, self.templateName ) )
    self.hist_names = [ rKey.GetName() for rKey in templateFile.GetListOfKeys() if not hist_parse( rKey.GetName(), samples )[ "IS SYST" ] ]
    
    self.categories = { "ALL": list( set( hist_name.split( "_" )[-2] for hist_name in self.hist_names if ( "isE" in hist_name.split( "_" )[-2] or "isM" in hist_name.split( "_" )[-2] ) ) ) }
    self.categories[ "ABCDNN" ] = [ category for category in self.categories[ "ALL" ] if hist_parse( category, self.samples )[ "ABCDNN" ] ]
    categories_exclude = list( 
      itertools.product( 
        *[ config.hist_bins[ "EXCLUDE" ][var_] for var_ in sorted( config.hist_bins[ "EXCLUDE" ] ) ]
      )
    )
    self.categories[ "EXCLUDE" ] = []
    for category in categories_exclude:
      cat_str = ""
      for i, var_ in enumerate( sorted( config.hist_bins[ "EXCLUDE" ] ) ):
        if var_ == "LEPTON":
          cat_str += "is" + category[i]
        else:
          cat_str += var_ + category[i]
      self.categories[ "EXCLUDE" ].append( cat_str )
    print( self.categories[ "EXCLUDE" ] )
    self.categories[ "SF" ] = self.categories[ "ALL" ]
    print( "All {} categories: {}".format( len( self.categories[ "ALL" ] ), self.categories[ "ALL" ] ) )
    print( "ABCDnn categories: {}".format( self.categories[ "ABCDNN" ] ) )
    if self.abcdnn:
      self.categories[ "SF" ] = [ category for category in self.categories[ "ALL" ] if category not in self.categories[ "ABCDNN" ] ]
    print( "SF categories: {}".format( self.categories[ "SF" ] ) )
    self.categories[ "E" ] =   [ category for category in self.categories[ "ALL" ] if "isE" in category ]
    self.categories[ "M" ] =   [ category for category in self.categories[ "ALL" ] if "isM" in category ]
    self.categories[ "B" ] =   [ category for category in self.categories[ "ALL" ] if "nB0p" not in category ]
    self.categories[ "HOT" ] = [ category for category in self.categories[ "ALL" ] if "nHOT0p" not in category ]
    self.categories[ "T" ] =   [ category for category in self.categories[ "ALL" ] if "nT0p" not in category ]
    self.categories[ "W" ] =   [ category for category in self.categories[ "ALL" ] if "nW0p" not in category ]

    for nJ in range( 4, 11 ):
      self.categories[ "NJ{}".format( nJ ) ] = [ category for category in self.categories if "nJ{}".format( nJ ) in category ]

    print( "[INFO] Found {} categories:".format( len( self.categories[ "ALL" ] ) ) )
    for category in sorted( self.categories[ "ALL" ] ):
      print( "   + {}".format( category ) )
    
    self.signals = "SIG" if self.combine_sig else self.params[ "SIGNALS" ] 
    self.backgrounds = self.params[ "BACKGROUNDS" ][:]
    #self.backgrounds.remove( "TTTT" )
    self.minor_backgrounds = config.params[ "ABCDNN" ][ "MINOR BKG" ][:]
    #self.minor_backgrounds.remove( "TTTT" )
    self.data = self.params[ "DATA" ]
    self.category_arr = { category: [ ( 0, "" ) ] for category in self.categories[ "ALL" ] }
    print( "[INFO] Process groups:" )
    print( ">> Signals: {}".format( self.signals ) )
    print( ">> Backgrounds: {}".format( self.backgrounds ) )
    print( ">> Minor Backgrounds: {}".format( self.minor_backgrounds ) )
    
    self.hist_groups = { key: {} for key in [ "SIG", "BKG", "DAT" ] }
    category_log = { key: {} for key in [ "SIG", "BKG", "DAT" ] }
    hist_list = [ hist_name for hist_name in set( self.hist_names ) if not ( hist_name.upper().endswith( "UP" ) or hist_name.upper().endswith( "DN" ) or hist_name.upper().endswith( "DOWN" ) ) ]
    exclude_count = 0
    for hist_name in hist_list:
      parse = hist_parse( hist_name, samples )
      if parse[ "GROUP" ] == "SIG" and self.combine_sig and parse[ "COMBINE" ] != "SIG": continue # use only the combined histogram
      if parse[ "GROUP" ] == "SIG" and not self.combine_sig and parse[ "COMBINE" ] == "SIG": continue
      if parse[ "IS SYST" ]: 
        continue
      if parse[ "CATEGORY" ] in self.categories[ "EXCLUDE" ]: continue
      if parse[ "GROUP" ] == "SIG":
        if parse[ "CATEGORY" ] not in self.hist_groups[ "SIG" ]:
          self.hist_groups[ "SIG" ][ parse[ "CATEGORY" ] ] = [ parse[ "COMBINE" ] ]
        else:
          self.hist_groups[ "SIG" ][ parse[ "CATEGORY" ] ].append( parse[ "COMBINE" ] )
      elif parse[ "GROUP" ] == "BKG":
        if templateFile.Get( hist_name ).Integral() < 1: 
          print( "[WARN] {} is beneath yield threshold, excluding...".format( hist_name )  )
          exclude_count += 1
          continue
        if parse[ "ABCDNN" ] and self.abcdnn:
          self.hist_groups[ "BKG" ][ parse[ "CATEGORY" ] ] = [ "ABCDNN" ] + config.params[ "ABCDNN" ][ "MINOR BKG" ]
        elif parse[ "COMBINE" ] == "ABCDNN" and not self.abcdnn:
          continue
        else:
          if parse[ "CATEGORY" ] not in self.hist_groups[ "BKG" ]:
            self.hist_groups[ "BKG" ][ parse[ "CATEGORY" ] ] = [ parse[ "COMBINE" ] ]
          else:
            self.hist_groups[ "BKG" ][ parse[ "CATEGORY" ] ].append( parse[ "COMBINE" ] )
      elif parse[ "GROUP" ] == "DAT":
        if parse[ "CATEGORY" ] not in self.hist_groups[ "DAT" ].keys():
          self.hist_groups[ "DAT" ][ parse[ "CATEGORY" ] ] = [ parse[ "COMBINE" ] ]
        else:
          self.hist_groups[ "DAT" ][ parse[ "CATEGORY" ] ].append( parse[ "COMBINE" ] )
    
    templateFile.Close()
    self.masses = ch.ValsFromRange( "690" )
    print( "[DONE] Finished assigning physics groups to datacard templates. Excluded {} processes failing statistical threshold requirement.".format( exclude_count ) )
    
  def define_regions( self, mode = 0 ):
  # mode 0: make all regions "SIGNAL REGION" --> default
  # mode 1: make only the uppermost region the "SIGNAL REGION"
  # mode 2: make only the lowermost region the "CONTROL REGION"
  # mode 3: make all regions "CONTROL REGION"
    print( "[START] Defining signal and control regions using mode {}".format( mode ) )
    upper_category = sorted( self.categories[ "ALL" ] )[-1].replace( "isE", "" ).replace( "isM", "" )
    lower_category = sorted( self.categories[ "ALL" ] )[0].replace( "isE", "" ).replace( "isM", "" )
    print( "[INFO] Least signal sensitive region: {}".format( lower_category ) )
    print( "[INFO] Most signal sensitive region: {}".format( upper_category ) ) 
    for category in self.categories[ "ALL" ]:
      if mode == "3":
        self.regions[ "CONTROL" ].append( category )
      elif mode == "2":
        if lower_category in category:
          self.regions[ "CONTROL" ].append( category )
        else:
          self.regions[ "SIGNAL" ].append( category )
      elif mode == "1":
        if upper_category in category:
          self.regions[ "SIGNAL" ].append( category )
        else:
          self.regions[ "CONTROL" ].append( category )
      else:
        self.regions[ "SIGNAL" ].append( category )
      
    print( "[INFO] Control Regions:" )
    for category in self.regions[ "CONTROL" ]:
      print( "   + {}".format( category ) )
    print( "[INFO] Signal Regions:" )
    for category in self.regions[ "SIGNAL" ]:
      print( "   + {}".format( category ) )
    print( "[DONE] {} Signal Regions, {} Control Regions".format( len( self.regions[ "SIGNAL" ] ), len( self.regions[ "CONTROL" ] ) ) )
      
  def add_datasets( self ):
    print( "[START] Adding MC processes and observations for CombineHarvester()" )
    count = { "SR": 0, "CR": 0 }
    for category in self.categories[ "ALL" ]:
      if category in self.categories[ "EXCLUDE" ]:
        print( "[WARN] Excluding category: {}".format( category ) )
        continue
      if category in self.regions[ "SIGNAL" ]:
        self.harvester.AddObservations( [ "*" ], [ self.prefix ], [ self.year ], [ category ], self.category_arr[ category ] )
        self.harvester.AddProcesses(    [ "*" ], [ self.prefix ], [ self.year ], [ category ], list( set( self.hist_groups[ "BKG" ][ category ] ) ), self.category_arr[ category ], False  )
        self.harvester.AddProcesses(    [ "" ],  [ self.prefix ], [ self.year ], [ category ], list( set( self.hist_groups[ "SIG" ][ category ] ) ), self.category_arr[ category ], True  )
        count[ "SR" ] += 1
      else:
        self.harvester.AddObservations( [ "all" ], [ self.prefix ], [ self.year ], [ category ], self.category_arr[ category ] )
        self.harvester.AddProcesses(    [ "all" ], [ self.prefix ], [ self.year ], [ category ], list( set( self.hist_groups[ "BKG" ][ category ] ) ), self.category_arr[ category ], False )
        count[ "CR" ] += 1
    print( "[DONE] Added {} categories to SR and {} categories to CR".format( count[ "SR" ], count[ "CR" ] ) )
  
  def add_norm( self, baseTag, groups, categories, values ):
    self.harvester.cp().process( groups ).channel( categories ).AddSyst( 
      self.harvester, baseTag, "lnN",
      ch.SystMap( "era" )( [ "16APV" ], values[ "16APV" ] )( [ "16" ], values[ "16" ] )( [ "17" ], values[ "17" ] )( [ "18" ], values[ "18" ] )
    )

  def add_shape( self, tag, groups, categories, smooth, decorrelate ):
    if smooth: tag += "LOWESS"
    if decorrelate:
      self.harvester.cp().process( groups ).channel( categories ).AddSyst(
        self.harvester, tag + "$ERA", "shape",
        ch.SystMap( "era" )( [ "16APV" ], 1.0 )( [ "16" ], 1.0 )( [ "17" ], 1.0 )( [ "18" ], 1.0 )
      )
    else:
      self.harvester.cp().process( groups ).channel( categories ).AddSyst(
        self.harvester, tag, "shape",
        ch.SystMap()( 1.0 )
      )
  
  def add_normalization_systematics( self ):
    print( "[START] Retrieving normalization systematics from {}".format( self.templateName ) )
   
    self.categories[ "SF" ] = self.categories[ "ALL" ]
    if self.abcdnn:
      self.categories[ "SF" ] = [ category for category in self.categories[ "ALL" ] if category not in self.categories[ "ABCDNN" ] ]

    self.add_norm( "LUMI_$ERA", self.signals, self.categories[ "ALL" ], config.systematics[ "LUMI" ] )
    self.add_norm( "LUMI_$ERA", self.backgrounds, self.categories[ "SF" ], config.systematics[ "LUMI" ] )
    if self.abcdnn: self.add_norm( "LUMI_$ERA", self.minor_backgrounds, self.categories[ "ABCDNN" ], config.systematics[ "LUMI" ] )

    self.add_norm( "LUMI_RUN2", self.signals, self.categories[ "ALL" ], config.systematics[ "LUMI_RUN2" ] )
    self.add_norm( "LUMI_RUN2", self.backgrounds, self.categories[ "SF" ], config.systematics[ "LUMI_RUN2" ] )
    if self.abcdnn: self.add_norm( "LUMI_RUN2", self.minor_backgrounds, self.categories[ "ABCDNN" ], config.systematics[ "LUMI_RUN2" ] )

    if self.year in [ "17", "18" ]:
      self.add_norm( "LUMI_17_18", self.signals, self.categories[ "ALL" ], config.systematics[ "LUMI_17_18" ] )
      self.add_norm( "LUMI_17_18", self.backgrounds, self.categories[ "SF" ], config.systematics[ "LUMI_17_18" ] )
      if self.abcdnn: self.add_norm( "LUMI_17_18", self.minor_backgrounds, self.categories[ "ABCDNN" ], config.systematics[ "LUMI_17_18" ] )
 
    self.add_norm( "ID_EL", self.signals, self.categories[ "E" ], config.systematics[ "ID" ][ "E" ] )
    self.add_norm( "ID_EL", self.backgrounds, [ category for category in self.categories[ "E" ] if category not in self.categories[ "ABCDNN" ] ], config.systematics[ "ID" ][ "E" ] )
    if self.abcdnn: self.add_norm( "ID_EL", self.minor_backgrounds, [ category for category in self.categories[ "E" ] if category in self.categories[ "ABCDNN" ] ], config.systematics[ "ID" ][ "E" ] )

    self.add_norm( "TRIG_EL_$ERA", self.signals, self.categories[ "E" ], config.systematics[ "TRIG" ][ "E" ] )
    self.add_norm( "TRIG_EL_$ERA", self.backgrounds, [ category for category in self.categories[ "E" ] if category not in self.categories[ "ABCDNN" ] ], config.systematics[ "TRIG" ][ "E" ] )
    if self.abcdnn: self.add_norm( "TRIG_EL_$ERA", self.minor_backgrounds, [ category for category in self.categories[ "E" ] if category in self.categories[ "ABCDNN" ] ], config.systematics[ "TRIG" ][ "E" ] )
    
    self.add_norm( "ISO_EL_$ERA", self.signals, self.categories[ "E" ], config.systematics[ "ISO" ][ "E" ] )
    self.add_norm( "ISO_EL_$ERA", self.backgrounds, [ category for category in self.categories[ "E" ] if category not in self.categories[ "ABCDNN" ] ], config.systematics[ "ISO" ][ "E" ] )
    if self.abcdnn: self.add_norm( "ISO_EL_$ERA", self.minor_backgrounds, [ category for category in self.categories[ "E" ] if category in self.categories[ "ABCDNN" ] ], config.systematics[ "ISO" ][ "E" ] )

    self.add_norm( "ID_MU", self.signals, self.categories[ "M" ], config.systematics[ "ID" ][ "M" ] )
    self.add_norm( "ID_MU", self.backgrounds, [ category for category in self.categories[ "M" ] if category not in self.categories[ "ABCDNN" ] ], config.systematics[ "ID" ][ "M" ] )
    if self.abcdnn: self.add_norm( "ID_MU_$ERA", self.minor_backgrounds, [ category for category in self.categories[ "M" ] if category in self.categories[ "ABCDNN" ] ], config.systematics[ "ID" ][ "M" ] )

    self.add_norm( "TRIG_MU_$ERA", self.signals, self.categories[ "M" ], config.systematics[ "TRIG" ][ "M" ] )
    self.add_norm( "TRIG_MU_$ERA", self.backgrounds, [ category for category in self.categories[ "M" ] if category not in self.categories[ "ABCDNN" ] ], config.systematics[ "TRIG" ][ "M" ] )
    if self.abcdnn: self.add_norm( "TRIG_MU_$ERA", self.minor_backgrounds, [ category for category in self.categories[ "M" ] if category in self.categories[ "ABCDNN" ] ], config.systematics[ "TRIG" ][ "M" ] )
    
    self.add_norm( "ISO_MU_$ERA", self.signals, self.categories[ "M" ], config.systematics[ "ISO" ][ "M" ] )
    self.add_norm( "ISO_MU_$ERA", self.backgrounds, [ category for category in self.categories[ "M" ] if category not in self.categories[ "ABCDNN" ] ], config.systematics[ "ISO" ][ "M" ] )
    if self.abcdnn: self.add_norm( "ISO_MU_$ERA", self.minor_backgrounds, [ category for category in self.categories[ "M" ] if category in self.categories[ "ABCDNN" ] ], config.systematics[ "ISO" ][ "M" ] )

    print( "[DONE] Finished adding normalization systematic uncertainties" )
    
  def add_shape_systematics( self ):
    print( "[START] Retrieving shape systematics from {}".format( self.templateName ) )
     
    useHOT = True
    useCSV = True
    for category in self.categories[ "SF" ]:
      if "nhot0p" in category.lower(): useHOT = False
      if "nb0p" in category.lower(): useCSV = False

    if config.systematics[ "MC" ][ "pileup" ][0]:
      bSmooth = self.smooth and config.systematics[ "MC" ][ "pileup" ][2]
      self.add_shape( "PILEUP", self.signals, self.categories[ "ALL" ], bSmooth, False )
      self.add_shape( "PILEUP", self.backgrounds, self.categories[ "SF" ], bSmooth, False )
      if self.abcdnn: self.add_shape( "PILEUP", self.minor_backgrounds, self.categories[ "ABCDNN" ], bSmooth, False )

    if config.systematics[ "MC" ][ "pileupJetID" ][0]:
      bSmooth = self.smooth and config.systematics[ "MC" ][ "pileupJetID" ][2]
      self.add_shape( "PILEUPJETID", self.signals, self.categories[ "ALL" ], bSmooth, False )
      self.add_shape( "PILEUPJETID", self.backgrounds, self.categories[ "SF" ], bSmooth, False )
      if self.abcdnn: self.add_shape( "PILEUPJETID", self.minor_backgrounds, self.categories[ "ABCDNN" ], bSmooth, False )

    if config.systematics[ "MC" ][ "prefire" ][0]:
      bSmooth = self.smooth and config.systematics[ "MC" ][ "prefire" ][2]
      self.add_shape( "PREFIRE", self.signals, self.categories[ "ALL" ], bSmooth, True )
      self.add_shape( "PREFIRE", self.backgrounds, self.categories[ "SF" ], bSmooth, True )
      if self.abcdnn: self.add_shape( "PREFIRE", self.minor_backgrounds, self.categories[ "ABCDNN" ], bSmooth, True )

    if config.systematics[ "MC" ][ "toppt" ][0]:
      bSmooth = self.smooth and config.systematics[ "MC" ][ "toppt" ][2]
      self.add_shape( "TOPPT", [ "TTBB", "TTNOBB" ], self.categories[ "SF" ], bSmooth, False )

    if config.systematics[ "MC" ][ "JEC" ][0]:
      bSmooth = self.smooth and config.systematics[ "MC" ][ "JEC" ][2]
      jec_tag = "JEC"
      if bSmooth: jec_tag += self.smoothing
      jec_tag += "$ERA"
      for systJEC in config.systematics[ "REDUCED JEC" ]:
        if not config.systematics[ "REDUCED JEC" ][ systJEC ]: continue
        jecSYST_tag = jec_tag.replace( "JEC", "JEC" + systJEC.replace( "Era", "20" + args.year ).replace( "APV", "" ).replace( "_", "" ) )
        if "Era" not in systJEC: jecSYST_tag = jecSYST_tag.replace( "$ERA", "" ) 
        self.add_shape( jecSYST_tag.upper(), self.signals, self.categories[ "ALL" ], False, False )
        self.add_shape( jecSYST_tag.upper(), self.backgrounds, self.categories[ "SF" ], False, False )
        if self.abcdnn: self.add_shape( jecSYST_tag.upper(), self.minor_backgrounds, self.categories[ "ABCDNN" ], False, False )
          
    if config.systematics[ "MC" ][ "JER" ][0]:
      bSmooth = self.smooth and config.systematics[ "MC" ][ "JER" ][2]
      self.add_shape( "JER", self.signals, self.categories[ "ALL" ], bSmooth, True )
      self.add_shape( "JER", self.backgrounds, self.categories[ "SF" ], bSmooth, True )
      if self.abcdnn: self.add_shape( "JER", self.minor_backgrounds, self.categories[ "ABCDNN" ], bSmooth, True )

    hot_backgrounds = [ background for background in self.backgrounds if background not in [ "QCD", "EWK" ] ]
    hot_minor_backgrounds = [ background for background in self.minor_backgrounds if background not in [ "QCD", "EWK" ] ]
    if config.systematics[ "MC" ][ "hotstat" ][0] and useHOT:
      bSmooth = self.smooth and config.systematics[ "MC" ][ "hotstat" ][2]
      #if args.year not in [ "16" ]: self.add_shape( "HOTSTAT", self.signals, self.categories[ "ALL" ], bSmooth, True )
      self.add_shape( "HOTSTAT", self.signals, self.categories[ "ALL" ], bSmooth, True )
      self.add_shape( "HOTSTAT", hot_backgrounds, self.categories[ "SF" ], bSmooth, True )
      if self.abcdnn: self.add_shape( "HOTSTAT", hot_minor_backgrounds, self.categories[ "ABCDNN" ], bSmooth, True )
    
    if config.systematics[ "MC" ][ "hotclosure" ][0] and useHOT:
      bSmooth = self.smooth and config.systematics[ "MC" ][ "hotclosure" ][2]
      #if args.year not in [ "16" ]: self.add_shape( "HOTCLOSURE", self.signals, self.categories[ "ALL" ], bSmooth, True )
      self.add_shape( "HOTCLOSURE", self.signals, self.categories[ "ALL" ], bSmooth, True )
      self.add_shape( "HOTCLOSURE", hot_backgrounds, self.categories[ "SF" ], bSmooth, True )
      if self.abcdnn: self.add_shape( "HOTCLOSURE", hot_minor_backgrounds, self.categories[ "ABCDNN" ], bSmooth, True )

    if config.systematics[ "MC" ][ "hotcspur" ][0] and useHOT:
      bSmooth = self.smooth and config.systematics[ "MC" ][ "hotcspur" ][2]
      #if args.year not in [ "16" ]: self.add_shape( "HOTCSPUR", self.signals, self.categories[ "ALL" ], bSmooth, True )
      self.add_shape( "HOTCSPUR", self.signals, self.categories[ "ALL" ], bSmooth, True )
      self.add_shape( "HOTCSPUR", hot_backgrounds, self.categories[ "SF" ], bSmooth, True )
      if self.abcdnn: self.add_shape( "HOTCSPUR", hot_minor_backgrounds, self.categories[ "ABCDNN" ], bSmooth, True )

    if config.systematics[ "MC" ][ "HF" ][0] and useCSV:
      bSmooth = self.smooth and config.systematics[ "MC" ][ "HF" ][2]
      self.add_shape( "HF", self.signals, self.categories[ "ALL" ], bSmooth, False )
      self.add_shape( "HF", self.backgrounds, self.categories[ "SF" ], bSmooth, False )
      if self.abcdnn: self.add_shape( "HF", self.minor_backgrounds, self.categories[ "ABCDNN" ], bSmooth, False )
    
    if config.systematics[ "MC" ][ "LF" ][0] and useCSV:
      bSmooth = self.smooth and config.systematics[ "MC" ][ "LF" ][2]
      self.add_shape( "LF", self.signals, self.categories[ "ALL" ], bSmooth, False )
      self.add_shape( "LF", self.backgrounds, self.categories[ "SF" ], bSmooth, False )
      if self.abcdnn: self.add_shape( "LF", self.minor_backgrounds, self.categories[ "ABCDNN" ], bSmooth, False )
         
    if config.systematics[ "MC" ][ "hfstats1" ][0] and useCSV:
      bSmooth = self.smooth and config.systematics[ "MC" ][ "hfstats1" ][2]
      self.add_shape( "HFSTATS1", self.signals, self.categories[ "ALL" ], bSmooth, True )
      self.add_shape( "HFSTATS1", self.backgrounds, self.categories[ "SF" ], bSmooth, True )
      if self.abcdnn: self.add_shape( "HFSTATS1", self.minor_backgrounds, self.categories[ "ABCDNN" ], bSmooth, True )
    
    if config.systematics[ "MC" ][ "hfstats2" ][0] and useCSV:
      bSmooth = self.smooth and config.systematics[ "MC" ][ "hfstats2" ][2]
      self.add_shape( "HFSTATS2", self.signals, self.categories[ "ALL" ], bSmooth, True )
      self.add_shape( "HFSTATS2", self.backgrounds, self.categories[ "SF" ], bSmooth, True )
      if self.abcdnn: self.add_shape( "HFSTATS2", self.minor_backgrounds, self.categories[ "ABCDNN" ], bSmooth, True )

    if config.systematics[ "MC" ][ "lfstats1" ][0] and useCSV:
      bSmooth = self.smooth and config.systematics[ "MC" ][ "lfstats1" ][2]
      self.add_shape( "LFSTATS1", self.signals, self.categories[ "ALL" ], bSmooth, True )
      self.add_shape( "LFSTATS1", self.backgrounds, self.categories[ "SF" ], bSmooth, True )
      if self.abcdnn: self.add_shape( "LFSTATS1", self.minor_backgrounds, self.categories[ "ABCDNN" ], bSmooth, True )
    
    if config.systematics[ "MC" ][ "lfstats2" ][0] and useCSV:
      bSmooth = self.smooth and config.systematics[ "MC" ][ "lfstats2" ][2]
      self.add_shape( "LFSTATS2", self.signals, self.categories[ "ALL" ], bSmooth, True )
      self.add_shape( "LFSTATS2", self.backgrounds, self.categories[ "SF" ], bSmooth, True )
      if self.abcdnn: self.add_shape( "LFSTATS2", self.minor_backgrounds, self.categories[ "ABCDNN" ], bSmooth, True )
    
    if config.systematics[ "MC" ][ "cferr1" ][0] and useCSV:
      bSmooth = self.smooth and config.systematics[ "MC" ][ "cferr1" ][2]
      self.add_shape( "CFERR1", self.signals, self.categories[ "ALL" ], bSmooth, False )
      self.add_shape( "CFERR1", self.backgrounds, self.categories[ "SF" ], bSmooth, False )
      if self.abcdnn: self.add_shape( "CFERR1", self.minor_backgrounds, self.categories[ "ABCDNN" ], bSmooth, False )

    if config.systematics[ "MC" ][ "cferr2" ][0] and useCSV:
      bSmooth = self.smooth and config.systematics[ "MC" ][ "cferr2" ][2]
      self.add_shape( "CFERR2", self.signals, self.categories[ "ALL" ], bSmooth, False )
      self.add_shape( "CFERR2", self.backgrounds, self.categories[ "SF" ], bSmooth, False )
      if self.abcdnn: self.add_shape( "CFERR2", self.minor_backgrounds, self.categories[ "ABCDNN" ], bSmooth, False )

    print( "[DONE] Added shape systematics" )
    
  def add_xsec( self, tag, groups, categories, value ):
    self.harvester.cp().process( groups ).channel( categories ).AddSyst(
      self.harvester, tag, "lnN",
      ch.SystMap()( value )
    )

  def add_model( self, tag, groups, categories, smooth ):
    if smooth: tag += self.smoothing
    self.harvester.cp().process( groups ).channel( categories ).AddSyst(
      self.harvester, tag, "shape",
      ch.SystMap()( 1.0 )
    )

  def add_xsec_systematics( self ): # this is used for studies only
    print( "[START] Adding cross-section systematics." )
    self.add_xsec( "XSEC_TTTW", [ "TTTW" ], self.categories[ "SF" ] + self.categories[ "ABCDNN" ], config.systematics[ "XSEC" ][ "TTTW" ] )
    self.add_xsec( "XSEC_TTTJ", [ "TTTJ" ], self.categories[ "SF" ] + self.categories[ "ABCDNN" ], config.systematics[ "XSEC" ][ "TTTJ" ] )
    self.add_xsec( "XSEC_TTTT", [ "TTTT" ], self.categories[ "SF" ] + self.categories[ "ABCDNN" ], config.systematics[ "XSEC" ][ "TTTT" ] )
    print( "[DONE]" )


  def add_theory_systematics( self ):
    print( "[START] Retrieving theoretical systematics from {}".format( self.templateName ) )
    
    self.add_xsec( "XSEC_TTTW", [ "TTTW" ], self.categories[ "SF" ] + self.categories[ "ABCDNN" ], config.systematics[ "XSEC" ][ "TTTW" ] )
    self.add_xsec( "XSEC_TTTJ", [ "TTTJ" ], self.categories[ "SF" ] + self.categories[ "ABCDNN" ], config.systematics[ "XSEC" ][ "TTTJ" ] )
    self.add_xsec( "XSEC_TTTT", [ "TTTT" ], self.categories[ "SF" ] + self.categories[ "ABCDNN" ], config.systematics[ "XSEC" ][ "TTTT" ] )
    self.add_xsec( "XSEC_TTBAR", [ "TTBB", "TTNOBB" ], self.categories[ "SF" ], config.systematics[ "XSEC" ][ "TTBAR" ] )
    self.add_xsec( "XSEC_EWK", [ "EWK" ], self.categories[ "SF" ], config.systematics[ "XSEC" ][ "EWK" ] )
    if self.abcdnn and "EWK" in config.params[ "ABCDNN" ][ "MINOR BKG" ]: self.add_xsec( "XSEC_EWK", [ "EWK" ], self.categories[ "ABCDNN" ], config.systematics[ "XSEC" ][ "EWK" ] )
    self.add_xsec( "XSEC_TOP", [ "TOP" ], self.categories[ "SF" ], config.systematics[ "XSEC" ][ "TOP" ] )
    if self.abcdnn and "TOP" in config.params[ "ABCDNN" ][ "MINOR BKG" ]: self.add_xsec( "XSEC_TOP", [ "TOP" ], self.categories[ "ABCDNN" ], config.systematics[ "XSEC" ][ "TOP" ] )
    self.add_xsec( "XSEC_TTH", [ "TTH" ], self.categories[ "SF" ], config.systematics[ "XSEC" ][ "TTH" ] )
    if self.abcdnn and "TTH" in config.params[ "ABCDNN" ][ "MINOR BKG" ]: self.add_xsec( "XSEC_TTH", [ "TTH" ], self.categories[ "ABCDNN" ], config.systematics[ "XSEC" ][ "TTH" ] )
    
    if config.options[ "GENERAL" ][ "PDF" ]:
      self.add_model( "PDF", self.signals, self.categories[ "ALL" ], False )
      #self.add_model( "ALPHAS", self.signals, self.categories[ "ALL" ], False )
      self.add_model( "PDF", self.backgrounds, self.categories[ "SF" ], False )
      self.add_model( "ALPHAS", self.backgrounds, self.categories[ "SF" ], False )
      if self.abcdnn: 
        self.add_model( "PDF", self.minor_backgrounds, self.categories[ "ABCDNN" ], False )
        self.add_model( "ALPHAS", self.minor_backgrounds, self.categories[ "ABCDNN" ], False )

    # handle PS weight uncertainty
    for syst in [ "isr", "fsr" ]:
      if not config.systematics[ "MC" ][ syst ][0]: continue
      bSmooth = True if config.systematics[ "MC" ][ syst ][2] else False
      if config.systematics[ "PS BREAKDOWN" ][ syst ]:
        for group in self.backgrounds: # config.params[ "COMBINE" ][ "BACKGROUNDS" ]:
          if group in [ "TTNOBB", "TTBB" ]:
            self.add_model( syst.upper() + "TTBAR", [ group ], self.categories[ "SF" ], bSmooth )
          else:
            self.add_model( syst.upper() + group, [ group ], self.categories[ "SF" ], bSmooth )
            if self.abcdnn:
              self.add_model( syst.upper() + group, [ group ], self.categories[ "ABCDNN" ], bSmooth )
        self.add_model( syst.upper() + "SIG", self.signals, self.categories[ "ALL" ], bSmooth )
      for pQCD in [ "G2GG", "G2QQ", "Q2QG", "X2XG" ]:
        for term in [ "muR", "cNS" ]:
          if not config.systematics[ "PS BREAKDOWN" ][ syst + pQCD + term ]: continue
          for group in config.params[ "COMBINE" ][ "BACKGROUNDS" ]:
            psTag = syst + pQCD + term
            if group in [ "TTNOBB", "TTBB" ]:
              self.add_model( psTag.upper() + "TTBAR", [ group ], self.categories[ "SF" ], bSmooth )
            else:
              self.add_model( psTag.upper() + group, [ group ], self.categories[ "SF" ], bSmooth )
              if self.abcdnn:
                self.add_model( psTag.upper() + group, [ group ], self.categories[ "ABCDNN" ], bSmooth )
          self.add_model( psTag.upper() + "SIG", self.signals, self.categories[ "ALL" ], bSmooth )

    for syst in [ "muR", "muF", "muRFcorrd" ]: # MURF adds MUR and MUF together in the same shift whereas MUENV takes the envelope
      if syst == "muR" and not config.systematics[ "MC" ][ "muR" ][0]: continue
      if syst == "muF" and not config.systematics[ "MC" ][ "muF" ][0]: continue
      if syst == "muRFcorrd" and not config.systematics[ "MC" ][ "muRFcorrd" ][0]: continue
      if syst == "muRF" and not ( config.systematics[ "MC" ][ "muR" ][0] or config.systematics[ "MC" ][ "muF" ][0] ): continue
      if syst == "muENV" and not ( config.systematics[ "MC" ][ "muR" ][0] or config.systematics[ "MC" ][ "muF" ][0] or config.systematics[ "MC" ][ "muRFcorrd" ][0] ): continue
      bSmooth = False
      if syst == "muR" and config.systematics[ "MC" ][ "muR" ][2]: bSmooth = True
      if syst == "muF" and config.systematics[ "MC" ][ "muF" ][2]: bSmooth = True
      if syst == "muRFcorrd" and config.systematics[ "MC" ][ "muRFcorrd" ][2]: bSmooth = True
      if syst == "muRF" and ( config.systematics[ "MC" ][ "muF" ][2] or config.systematics[ "MC" ][ "muR" ][2] ): bSmooth = True
      if syst == "muENV" and ( config.systematics[ "MC" ][ "muF" ][2] or config.systematics[ "MC" ][ "muR" ][2] or config.systematics[ "MC" ][ "muRFcorrd" ][2] ): bSmooth = True

      if config.options[ "COMBINE" ][ "MURF CORR TTTX" ]:
        self.add_model( syst.upper() + "TTTX", self.signals + [ "TTTT" ], self.categories[ "ALL" ], bSmooth )
      else:
        self.add_model( syst.upper() + "SIG", self.signals, self.categories[ "ALL" ], bSmooth )
        self.add_model( syst.upper() + "TTTT", [ "TTTT" ], self.categories[ "ALL" ], bSmooth )
     
      for group in self.backgrounds: # config.params[ "COMBINE" ][ "BACKGROUNDS" ]:
        if group in [ "TTTT" ]: continue
        if group in [ "TTNOBB", "TTBB" ]:
          self.add_model( syst.upper() + "TTBAR", [ group ], self.categories[ "SF" ], bSmooth )
        else:
          self.add_model( syst.upper() + group, [ group ], self.categories[ "SF" ], bSmooth )
          if self.abcdnn:
            self.add_model( syst.upper() + group, [ group ], self.categories[ "ABCDNN" ], bSmooth )
    
    print( "[DONE] Added theoretical systematics" )
  
  def add_ABCDNN_systematics( self ): 
    for category in self.categories[ "ABCDNN" ]:
      tag = abcdnn_tag( category )
      if args.normSyst:
        if "EXTABCDSYST" in config.params[ "ABCDNN" ][ "SYSTEMATICS" ]:    self.add_norm( "EXTABCDSYST$ERA", [ "ABCDNN" ], [ category ], config.systematics[ "EXTABCDSYST" ][ tag ] )
        if "EXTABCDSTAT" in config.params[ "ABCDNN" ][ "SYSTEMATICS" ]:    self.add_norm( "EXTABCDSTAT$ERA", [ "ABCDNN" ], [ category ], config.systematics[ "EXTABCDSTAT" ][ tag ]  )
        if "EXTABCDCLOSURE" in config.params[ "ABCDNN" ][ "SYSTEMATICS" ]: self.add_norm( "EXTABCDCLOSURE", [ "ABCDNN" ],  [ category ], config.systematics[ "EXTABCDCLOSURE" ][ tag ] )

    if args.shapeSyst:
      if config.systematics[ "MC" ][ "ABCDNNPEAK" ][0] and "ABCDNNPEAK" in config.params[ "ABCDNN" ][ "SYSTEMATICS" ]:
        bSmooth = self.smooth and config.systematics[ "MC" ][ "ABCDNNPEAK" ][2]
        self.add_shape( "ABCDNNPEAK", [ "ABCDNN" ], self.categories[ "ABCDNN" ], bSmooth, True )
      if config.systematics[ "MC" ][ "ABCDNNTAIL" ][0] and "ABCDNNTAIL" in config.params[ "ABCDNN" ][ "SYSTEMATICS" ]:
        bSmooth = self.smooth and config.systematics[ "MC" ][ "ABCDNNTAIL" ][2]
        self.add_shape( "ABCDNNTAIL", [ "ABCDNN" ], self.categories[ "ABCDNN" ], bSmooth, True )
      if config.systematics[ "MC" ][ "ABCDNNCLOSURE" ][0] and "ABCDNNCLOSURE" in config.params[ "ABCDNN" ][ "SYSTEMATICS" ]:
        bSmooth = self.smooth and config.systematics[ "MC" ][ "ABCDNNCLOSURE" ][2]
        self.add_shape( "ABCDNNCLOSURE", [ "ABCDNN" ], self.categories[ "ABCDNN" ], bSmooth, False )

    print( "[DONE] Added Extended ABCD normalization systematics and ABCDNN shape systematics" )

  def add_TTHF_systematics( self ):
    print( "[START] Adding heavy flavor (TTBB) systematics" )
    self.add_norm( "TTHF", [ "TTBB" ], self.categories[ "SF" ], config.systematics[ "TTHF" ] )    
    print( "[DONE]" )
  
  def add_shapes( self ):
    print( "[START] Retrieving histograms from {}".format( self.templateName ) )
    for category in tqdm.tqdm( self.categories[ "ALL" ] ):
      key_bkg = { 
        "NOMINAL":     "$PROCESS_{}$BIN_NOMINAL".format( category ),
        "SYST":        "$PROCESS_{}$BIN_$SYSTEMATIC".format( category ),
      }
      self.harvester.cp().channel( [ category ] ).era( [ self.year ] ).backgrounds().ExtractShapes(
        os.path.join( self.limitPath, self.templateName ), key_bkg[ "NOMINAL" ], key_bkg[ "SYST" ]
      )
      key_sig = { 
        "NOMINAL": "$PROCESS$MASS_{}$BIN_NOMINAL".format( category ),
        "SYST":    "$PROCESS$MASS_{}$BIN_$SYSTEMATIC".format( category )
      }
      if category not in self.regions[ "CONTROL" ]:
        self.harvester.cp().channel( [ category ] ).era( [ self.year ] ).signals().ExtractShapes(
          os.path.join( self.limitPath, self.templateName ), key_sig[ "NOMINAL" ], key_sig[ "SYST" ]
        )
    print( "[DONE]" )
  
  def add_auto_MC_statistics( self ):
    print( "[START] Adding auto MC statistics to DataCard" )
    self.harvester.AddDatacardLineAtEnd( "* autoMCStats 1." )
    print( "[DONE]" )
    
  def rename_and_write( self, limit = True ):
    print( "[START] Setting standardized bin names" )
    ch.SetStandardBinNames( self.harvester )
    
    writer = ch.CardWriter(
      "{}$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt".format( self.limitPath ),
      "{}$TAG/common/$ANALYSIS_$CHANNEL.input.root".format( self.limitPath )
    )
    writer.SetVerbosity(1)
    writer.WriteCards( "cmb", self.harvester )
    count = 0
    upper_category = sorted( self.categories[ "ALL" ] )[-1].replace( "isE", "" ).replace( "isM", "" )
    for category in sorted( self.categories[ "ALL" ] ):
      if category in self.categories[ "EXCLUDE" ]:
        continue
      print( ">> Writing category: {}".format( category ) )
      writer.WriteCards( category, self.harvester.cp().channel( [ category ] ) )
      count += 1
    print( "[DONE] Wrote {} data cards".format( count ) )
    
def main():
  params = config.params[ "COMBINE" ].copy()
  options = config.options[ "COMBINE" ].copy()
  tagShape = "" if args.shapeSyst else "noShape"
  tagNorm  = "" if args.normSyst else "noNorm"
  tagTheory = "" if args.theorySyst else "noTheory"
  tagSmooth = "" if not options[ "SMOOTH" ] else config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper()
  tagABCDnn = "" if not options[ "ABCDNN" ] else "ABCDNN"
  dTag = args.tag + "_" + tagABCDnn + tagShape + tagNorm + tagTheory + tagSmooth
  datacard = DataCard( 
    args.variable, 
    args.year, 
    args.region, 
    dTag,
    params, 
    options,
    samples,
    "TTTX" 
  )
  datacard.define_regions( args.mode )
  datacard.add_datasets()
  if args.normSyst:
    datacard.add_normalization_systematics()
  if args.shapeSyst:
    datacard.add_shape_systematics()
  if args.theorySyst:
    datacard.add_theory_systematics()
    datacard.add_TTHF_systematics()
  if args.xsecSyst:
    datacard.add_xsec_systematics()
  if options[ "ABCDNN" ]:
   datacard.add_ABCDNN_systematics()
  datacard.add_shapes()
  datacard.add_auto_MC_statistics()
  datacard.rename_and_write()
  
def add_groups_datacard( nDataCard ):
  tagSmooth = config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() if config.options[ "COMBINE"][ "SMOOTH" ] else ""
  doABCDNN = config.options[ "COMBINE" ][ "ABCDNN" ]
  groups = { "NORM": [], "SHAPE": [], "THEORY": [], "ABCDNN": [] }
  groups[ "NORM" ].append( "LUMI_RUN2" )
  groups[ "NORM" ].append( "LUMI_17_18" )
  groups[ "NORM" ].append( "ID_EL" )
  groups[ "NORM" ].append( "ID_MU" )
  groups[ "THEORY" ].append( "XSEC_TTTW" )
  groups[ "THEORY" ].append( "XSEC_TTTJ" )
  groups[ "THEORY" ].append( "XSEC_TTTT" )
  groups[ "THEORY" ].append( "XSEC_EWK" )
  groups[ "THEORY" ].append( "XSEC_TOP" )
  groups[ "THEORY" ].append( "XSEC_TTH" )
  groups[ "SHAPE" ].append( "PILEUP" )
  groups[ "SHAPE" ].append( "HF" )
  groups[ "SHAPE" ].append( "LF" )
  groups[ "SHAPE" ].append( "CFERR1" )
  groups[ "SHAPE" ].append( "CFERR2" )
  if not doABCDNN:
    groups[ "NORM" ].append( "TTHF" )
    groups[ "THEORY" ].append( "XSEC_TTBAR" )
  for era in [ "16APV", "16", "17", "18" ]:
    if era != args.year and args.year != "Run2": continue
    groups[ "NORM" ].append( "LUMI_{}".format( era ) )
    groups[ "NORM" ].append( "TRIG_EL_{}".format( era ) )
    groups[ "NORM" ].append( "ISO_EL_{}".format( era ) )
    groups[ "NORM" ].append( "TRIG_MU_{}".format( era ) )
    groups[ "NORM" ].append( "ISO_MU_{}".format( era ) )
    groups[ "SHAPE" ].append( "PREFIRE{}".format( era ) )
    groups[ "SHAPE" ].append( "HFSTATS1{}".format( era ) )
    groups[ "SHAPE" ].append( "HFSTATS2{}".format( era ) )
    groups[ "SHAPE" ].append( "LFSTATS1{}".format( era ) )
    groups[ "SHAPE" ].append( "LFSTATS2{}".format( era ) )
    groups[ "SHAPE" ].append( "HOTSTAT{}".format( era ) )
    groups[ "SHAPE" ].append( "HOTCSPUR{}".format( era ) )
    groups[ "SHAPE" ].append( "HOTCLOSURE{}".format( era ) )

    for systJEC in config.systematics[ "REDUCED JEC" ]:
      if not config.systematics[ "REDUCED JEC" ][ systJEC ]: continue
      jecSYST_tag = "JEC{}".format( tagSmooth ).replace( "JEC", "JEC" + systJEC.replace( "Era", "20" + era ).replace( "APV", "" ).replace( "_", "" ).upper() )
      if "Era" in systJEC:
        jecSYST_tag += era
      groups[ "SHAPE" ].append( jecSYST_tag )

  for theory in [ "MUR", "MUF", "ISR", "FSR" ]:
    groups[ "THEORY" ].append( theory + "SIG" )
    for process in config.params[ "COMBINE" ][ "BACKGROUNDS" ]:
      if process not in config.params[ "ABCDNN" ][ "MINOR BKG" ] and doABCDNN: continue
      if process in [ "TTNOBB", "TTBB" ]:
        groups[ "THEORY" ].append( theory + "TTBAR" )
      else:
        groups[ "THEORY" ].append( theory + process )
  groups[ "THEORY" ].append( "PDF" )
  groups[ "THEORY" ].append( "ALPHAS" )
  if doABCDNN:
    for era in [ "16APV", "16", "17", "18" ]:
      if args.year != "Run2" and era != args.year: continue
      groups[ "ABCDNN" ].append( "EXTABCDSYST{}".format( era ) )
      groups[ "ABCDNN" ].append( "EXTABCDSTAT{}".format( era ) )
      groups[ "ABCDNN" ].append( "ABCDNNPEAK{}".format( era ) )
      groups[ "ABCDNN" ].append( "ABCDNNTAIL{}".format( era ) )
    groups[ "ABCDNN" ].append( "EXTABCDCLOSURE" )
    groups[ "ABCDNN" ].append( "ABCDNNCLOSURE" )

  print( "Adding NORM group: {}".format( " ".join( groups[ "NORM" ] ) ) )
  print( "Adding SHAPE group: {}".format( " ".join( groups[ "SHAPE" ] ) ) )
  print( "Adding THEORY group: {}".format( " ".join( groups[ "THEORY" ] ) ) )
  print( "Adding ABCDNN group: {}".format( " ".join( groups[ "THEORY" ] ) ) )
  fDataCard = open( nDataCard, "a" )
  fDataCard.write( "NORM   group = {} \n".format( " ".join( groups[ "NORM" ] ) ) )
  fDataCard.write( "SHAPE  group = {} \n".format( " ".join( groups[ "SHAPE" ] ) ) )
  fDataCard.write( "THEORY group = {} \n".format( " ".join( groups[ "THEORY" ] ) ) )
  if doABCDNN:
    fDataCard.write( "ABCDNN group = {} \n".format( " ".join( groups[ "ABCDNN" ] ) ) )

  fDataCard.close()

if args.groups:
  add_groups_datacard( args.card )
else:
  main()
