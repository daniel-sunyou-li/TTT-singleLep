#!/usr/bin/env python

import os, sys, math
from argparse import ArgumentParser
sys.path.append( ".." )
from utils import hist_parse
import config

parser = ArgumentParser()
parser.add_argument( "-y", "--year", required = True, help = "16APV,16,17,18" )
parser.add_argument( "-t", "--tag", required = True )
parser.add_argument( "-r", "--region", required = True, help = ",".join( list( config.region_prefix.keys() ) ) )
parser.add_argument( "-v", "--variable", required = True )
parser.add_argument( "-m", "--mode", default = 0, help = "0,1,2,3" )
parser.add_argument( "--verbose", action = "store_true" )
args = parser.parse_args()

import CombineHarvester.CombineTools.ch as ch
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

def jet_count( category ):
  parts = category.split( "n" )
  jet_count = 0
  for part in parts:
    if part.startswith("is"): continue
    elif part.startswith("HOT"): jet_count += int( part[3] )
    else: jet_count += int( part[1] )
  return jet_count

class DataCard():
  def __init__( self, variable, year, region, tag, params, options,samples, prefix ):
    self.harvester = ch.CombineHarvester()
    self.variable = variable
    self.year = year
    self.region = region
    self.abcdnn = options[ "ABCDNN" ]
    self.tag = tag
    self.lumistr = config.lumiStr[ self.year ]
    self.regions = {
      "SIGNAL":  [],
      "CONTROL": []
    }
    self.samples = samples
    self.params = params
    self.options = options
    self.prefix = prefix
    
    self.templateName = "template_combine_{}_UL{}_rebinned_stat{}.root".format( 
      self.variable,
      self.year,
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
    self.limitPath = "limits_UL{}_{}_{}_{}/".format( self.year, self.variable, self.region, self.tag )
    if not os.path.exists( self.limitPath ): os.system( "mkdir -v {}".format( self.limitPath ) )
    os.system( "cp -vp {} {}".format( self.templatePath, os.path.join( os.getcwd(), self.limitPath ) ) )
    
    templateFile = ROOT.TFile( os.path.join( self.limitPath, self.templateName ) )
    self.hist_names = [ rKey.GetName() for rKey in templateFile.GetListOfKeys() if not hist_parse( rKey.GetName(), samples )[ "IS SYST" ] ]
    templateFile.Close()
    
    self.categories = { "ALL": list( set( hist_name.split( "_" )[-2] for hist_name in self.hist_names if ( "isE" in hist_name.split( "_" )[-2] or "isM" in hist_name.split( "_" )[-2] ) ) ) }
    self.categories[ "ABCDNN" ] = [ category for category in self.categories[ "ALL" ] if hist_parse( category, self.samples )[ "ABCDNN" ] ]
    self.categories[ "E" ] =   [ category for category in self.categories[ "ALL" ] if "isE" in category ]
    self.categories[ "M" ] =   [ category for category in self.categories[ "ALL" ] if "isM" in category ]
    self.categories[ "B" ] =   [ category for category in self.categories[ "ALL" ] if "nB0p" not in category ]
    self.categories[ "HOT" ] = [ category for category in self.categories[ "ALL" ] if "nHOI0p" not in category ]
    self.categories[ "T" ] =   [ category for category in self.categories[ "ALL" ] if "nT0p" not in category ]
    self.categories[ "W" ] =   [ category for category in self.categories[ "ALL" ] if "nW0p" not in category ]

    for nJ in range( 4, 11 ):
      self.categories[ "NJ{}".format( nJ ) ] = [ category for category in self.categories if "nJ{}".format( nJ ) in category ]

    print( "[INFO] Found {} categories:".format( len( self.categories[ "ALL" ] ) ) )
    for category in sorted( self.categories[ "ALL" ] ):
      print( "   + {}".format( category ) )
    
    self.signals = self.params[ "SIGNALS" ]
    self.backgrounds = self.params[ "BACKGROUNDS" ]
    self.data = self.params[ "DATA" ]
    self.muRF_norm = self.params[ "MURF NORM" ]
    self.isr_norm = self.params[ "ISR NORM" ]
    self.fsr_norm = self.params[ "FSR NORM" ]
    self.pdf_norm = self.params[ "PDF NORM" ]
    self.category_arr = { category: [ ( 0, "" ) ] for category in self.categories[ "ALL" ] }
    
    self.hist_groups = { key: {} for key in [ "SIG", "SIG SYST", "BKG", "BKG SYST", "DAT" ] }
    category_log = { key: {} for key in [ "SIG", "SIG SYST", "BKG", "BKG SYST", "DAT" ] }
    for hist_name in self.hist_names:
      parse = hist_parse( hist_name, samples )
      if parse[ "GROUP" ] == "SIG":
        if parse[ "IS SYST" ]: 
          if parse[ "CATEGORY" ] not in self.hist_groups[ "SIG SYST" ].keys():
            self.hist_groups[ "SIG SYST" ][ parse[ "CATEGORY" ] ] = [ parse[ "COMBINE" ] ]
          else: 
            self.hist_groups[ "SIG SYST" ][ parse[ "CATEGORY" ] ].append( parse[ "COMBINE" ] )
        else: 
          if parse[ "CATEGORY" ] not in self.hist_groups[ "SIG" ].keys():
            self.hist_groups[ "SIG" ][ parse[ "CATEGORY" ] ] = [ parse[ "COMBINE" ] ]
          else:
            self.hist_groups[ "SIG" ][ parse[ "CATEGORY" ] ].append( parse[ "COMBINE" ] )
      elif parse[ "GROUP" ] == "BKG":
        if self.abcdnn and parse[ "ABCDNN" ]:
          if parse[ "IS SYST" ]:
            if parse[ "SYST" ] == "ABCDNN": self.hist_groups[ "BKG SYST" ][ parse[ "CATEGORY" ] ] = [ parse[ "COMBINE" ] ]
          else:
            self.hist_groups[ "BKG" ][ parse[ "CATEGORY" ] ] = [ parse[ "COMBINE" ] ]
        else:
          if parse[ "IS SYST" ]: 
            if parse[ "CATEGORY" ] not in self.hist_groups[ "BKG SYST" ].keys():
              self.hist_groups[ "BKG SYST" ][ parse[ "CATEGORY" ] ] = [ parse[ "COMBINE" ] ]
            else: 
              self.hist_groups[ "BKG SYST" ][ parse[ "CATEGORY" ] ].append( parse[ "COMBINE" ] )
          else: 
            if parse[ "CATEGORY" ] not in self.hist_groups[ "BKG" ].keys():
              self.hist_groups[ "BKG" ][ parse[ "CATEGORY" ] ] = [ parse[ "COMBINE" ] ]
            else:
              self.hist_groups[ "BKG" ][ parse[ "CATEGORY" ] ].append( parse[ "COMBINE" ] )
      elif parse[ "GROUP" ] == "DAT":
        if parse[ "CATEGORY" ] not in self.hist_groups[ "DAT" ].keys():
          self.hist_groups[ "DAT" ][ parse[ "CATEGORY" ] ] = [ parse[ "COMBINE" ] ]
        else:
          self.hist_groups[ "DAT" ][ parse[ "CATEGORY" ] ].append( parse[ "COMBINE" ] )
    
          
    self.masses = ch.ValsFromRange( "690" )
    
  def define_regions( self, mode = 0 ):
  # mode 0: make all regions "SIGNAL REGION" --> default
  # mode 1: make only the uppermost region the "SIGNAL REGION"
  # mode 2: make only the lowermost region the "CONTROL REGION"
  # mode 3: make all regions "CONTROL REGION"
    print( "[START] Defining signal and control regions using mode {}".format( mode ) )
    min_category = jet_count( self.categories[ "ALL" ][0] )
    max_category = jet_count( self.categories[ "ALL" ][0] )
    for category in self.categories[ "ALL" ]:
      min_category = min( min_category, jet_count( category ) )
      max_category = max( max_category, jet_count( category ) )
    for category in self.categories[ "ALL" ]:
      if mode == 3:
        self.regions[ "CONTROL" ].append( category )
      elif mode == 2:
        if jet_count( category ) == min_category:
          self.regions[ "CONTROL" ].append( category )
        else:
          self.regions[ "SIGNAL" ].append( category )
      elif mode == 1:
        if jet_count( category ) == max_category:
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
      if category in self.regions[ "SIGNAL" ]:
        self.harvester.AddObservations( [ "*" ], [ self.prefix ], [ self.year ], [ category ], self.category_arr[ category ] )
        self.harvester.AddProcesses(    [ "*" ], [ self.prefix ], [ self.year ], [ category ], self.hist_groups[ "BKG" ][ category ], self.category_arr[ category ], False  )
        self.harvester.AddProcesses(    [ "" ],  [ self.prefix ], [ self.year ], [ category ], self.hist_groups[ "SIG" ][ category ], self.category_arr[ category ], True  )
        count[ "SR" ] += 1
      else:
        self.harvester.AddObservations( [ "all" ], [ self.prefix ], [ self.year ], [ category ], self.category_arr[ category ] )
        self.harvester.AddProcesses(    [ "all" ], [ self.prefix ], [ self.year ], [ category ], self.hist_groups[ "BKG" ][ category ], self.category_arr[ category ], False )
        count[ "CR" ] += 1
    print( "[DONE] Added {} categories to SR and {} categories to CR".format( count[ "SR" ], count[ "CR" ] ) )
  
  def add_yield_systematics( self ):
    print( "[START] Retrieving yield systematics from {}".format( self.templateName ) )
    count = 0
    
    self.harvester.cp().process( self.signals + self.backgrounds ).channel( self.categories[ "ALL" ] ).AddSyst( 
      self.harvester, "LUMI_$ERA", "lnN",
      ch.SystMap( "era" )( [ "16APV" ], config.systematics[ "LUMI" ][ "16APV" ] )( [ "16" ], config.systematics[ "LUMI" ][ "16" ] )( [ "17" ], config.systematics[ "LUMI" ][ "17" ] )( [ "18" ], config.systematics[ "LUMI" ][ "18" ] )
    )
    print( "   + Luminosity {}: {} (lnN)".format( self.year, config.systematics[ "LUMI" ][ self.year ] ) )
    count += 1
    
    self.harvester.cp().process( self.signals + self.backgrounds ).channel( self.categories[ "E" ] ).AddSyst( 
      self.harvester, "SF_EL_$ERA", "lnN",
      ch.SystMap( "era" )( [ "16APV" ], config.systematics[ "ID" ][ "E" ] )( [ "16" ], config.systematics[ "ID" ][ "E" ] )( [ "17" ], config.systematics[ "ID" ][ "E" ] )( [ "18" ], config.systematics[ "ID" ][ "E" ] )
    )
    print( "   + Trigger (el) {}: {} (lnN)".format( self.year, config.systematics[ "ID" ][ "E" ] ) )
    count += 1
    
    self.harvester.cp().process( self.signals + self.backgrounds ).channel( self.categories[ "M" ] ).AddSyst( 
      self.harvester, "SF_MU_$ERA", "lnN",
      ch.SystMap( "era" )( [ "16APV" ], config.systematics[ "ID" ][ "M" ] )( [ "16" ], config.systematics[ "ID" ][ "M" ] )( [ "17" ], config.systematics[ "ID" ][ "M" ] )( [ "18" ], config.systematics[ "ID" ][ "M" ] )
    )
    print( "   + Trigger (mu) {}: {} (lnN)".format( self.year, config.systematics[ "ID" ][ "E" ] ) )
    count += 1
   
    yield_categories = self.categories[ "ALL" ]
    if self.abcdnn:
      if config.options[ "MODIFY BINNING" ][ "SMOOTH" ]:
        abcdnn_tag = "ABCDNN"
      else:
        abcdnn_tag = "ABCDNN{}".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      self.harvester.cp().process( [ "ABCDNN" ] ).channel( self.categories[ "ABCDNN" ] ).AddSyst(
        self.harvester, abcdnn_tag, "lnN",
        ch.SystMap()( 1.0 )
      )
      yield_categories = [ category for category in self.categories[ "ALL" ] if category not in self.categories[ "ABCDNN" ] ]

    self.harvester.cp().process( [ bkg for bkg in self.backgrounds if bkg in [ "TTBB", "TTNOBB" ] ] ).channel( yield_categories ).AddSyst(
      self.harvester, "XSEC_TTBAR", "lnN",
      ch.SystMap()( config.systematics[ "XSEC" ][ "TTBAR" ] )
    )
    print( "   + TTBAR: {} (lnN)".format( config.systematics[ "XSEC" ][ "TTBAR" ] ) )
    count += 1
    
    self.harvester.cp().process( [ "EWK" ] ).channel( yield_categories ).AddSyst(
      self.harvester, "XSEC_EWK", "lnN",
      ch.SystMap()( config.systematics[ "XSEC" ][ "EWK" ] )
    )
    print( "   + EWK: {} (lnN)".format( config.systematics[ "XSEC" ][ "EWK" ] ) )
    count += 1
    
    self.harvester.cp().process( [ "TOP" ] ).channel( yield_categories ).AddSyst(
      self.harvester, "XSEC_TOP", "lnN",
      ch.SystMap()( config.systematics[ "XSEC" ][ "TOP" ] )
    )
    print( "   + TOP: {} (lnN)".format( config.systematics[ "XSEC" ][ "TOP" ] ) )
    count += 1
    
    self.harvester.cp().process( [ "TTH" ] ).channel( yield_categories ).AddSyst(
      self.harvester, "XSEC_TTH", "lnN",
      ch.SystMap()( config.systematics[ "XSEC" ][ "TTH" ] )
    )

    print( "[DONE] Added {} yield systematics".format( count ) )
    
  def add_shape_systematics( self ):
    print( "[START] Retrieving shape systematics from {}".format( self.templateName ) )
    count = 0
    
    apply_samples = []
    
    if config.options[ "COMBINE" ][ "SMOOTH" ]:
      pileup_tag = "PILEUP{}".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      prefire_tag = "PREFIRE{}$ERA".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      jec_tag = "JEC{}$ERA".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      jer_tag = "JER{}$ERA".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      hf_tag = "HF{}".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      lf_tag = "LF{}".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      hfstat1_tag = "HFSTATS1{}$ERA".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      hfstat2_tag = "HFSTATS2{}$ERA".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      lfstat1_tag = "LFSTATS1{}$ERA".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      lfstat2_tag = "LFSTATS2{}$ERA".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      cferr1_tag = "CFERR1{}".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      cferr2_tag = "CFERR2{}".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      abcdnn_tag = "ABCDNN{}".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
    else:
      pileup_tag = "PILEUP"
      prefire_tag = "PREFIRE$ERA"
      jec_tag = "JEC$ERA"
      jer_tag = "JER$ERA"
      hf_tag = "HF"
      lf_tag = "LF"
      hfstat1_tag = "HFSTATS1$ERA"
      hfstat2_tag = "HFSTATS2$ERA"
      lfstat1_tag = "LFSTATS1$ERA"
      lfstat2_tag = "LFSTATS2$ERA"
      cferr1_tag = "CFERR1"
      cferr2_tag = "CFERR2"
      abcdnn_tag = "ABCDNN"
     
    shape_categories = self.categories[ "ALL" ]
    if self.abcdnn:
      shape_categories = [ category for category in self.categories[ "ALL" ] if category not in self.categories[ "ABCDNN" ] ]
      self.harvester.cp().process( [ "ABCDNN" ] ).channel( self.categories[ "ABCDNN" ] ).AddSyst(
        self.harvester, abcdnn_tag, "shape",
        ch.SystMap()( config.systematics[ "ABCDNN" ] )
      )

    if config.systematics[ "MC" ][ "pileup" ]:
      self.harvester.cp().process( self.signals + self.backgrounds ).channel( shape_categories ).AddSyst(
        self.harvester, pileup_tag, "shape",
        ch.SystMap()( 1.0 )
      )
      print( "   + Pileup: 1.0 (shape)" )
      count += 1
      
    #if self.year in [ "16APV", "16", "17" ]:
    #  self.harvester.cp().process( self.signals + self.backgrounds ).channel( shape_categories ).AddSyst(
    #    self.harvester, prefire_tag, "shape",
    #    ch.SystMap( "era" )( [ "16APV" ], 1.0 )( [ "16" ], 1.0 )( [ "17" ], 1.0 )( [ "18" ], 1.0 )
    #  )
    #  print( "   + Prefire: 1.0 (shape)" )
    #  count += 1
      
    if config.systematics[ "MC" ][ "JEC" ]:
      self.harvester.cp().process( self.signals + self.backgrounds ).channel( shape_categories ).AddSyst(
        self.harvester, jec_tag, "shape",
        ch.SystMap( "era" )( [ "16APV" ], 1.0 )( [ "16" ], 1.0 )( [ "17" ], 1.0 )( [ "18" ], 1.0 )
      )
      print( "   + JEC: 1.0 (shape)" )
      count += 1
    
    if config.systematics[ "MC" ][ "JER" ]:
      self.harvester.cp().process( self.signals + self.backgrounds ).channel( shape_categories ).AddSyst(
        self.harvester, jer_tag, "shape",
        ch.SystMap( "era" )( [ "16APV" ], 1.0 )( [ "16" ], 1.0 )( [ "17" ], 1.0 )( [ "18" ], 1.0 )
      )
      print( "   + JER: 1.0 (shape)" ) 
      count += 1
    
    if config.systematics[ "MC" ][ "HF" ]:
      self.harvester.cp().process( self.signals + self.backgrounds ).channel( shape_categories ).AddSyst(
        self.harvester, hf_tag, "shape",
        ch.SystMap( "era" )( [ "16APV" ], 1.0 )( [ "16" ], 1.0 )( [ "17" ], 1.0 )( [ "18" ], 1.0 )
      )
      print( "   + HF: 1.0 (shape)" ) 
      count += 1
    
    if config.systematics[ "MC" ][ "LF" ]:
      self.harvester.cp().process( self.signals + self.backgrounds ).channel( shape_categories ).AddSyst(
        self.harvester, lf_tag, "shape",
        ch.SystMap( "era" )( [ "16APV" ], 1.0 )( [ "16" ], 1.0 )( [ "17" ], 1.0 )( [ "18" ], 1.0 )
      )
      print( "   + LF: 1.0 (shape)" )     
      count += 1
    
    if config.systematics[ "MC" ][ "hfstats1" ]:
      self.harvester.cp().process( self.signals + self.backgrounds ).channel( shape_categories ).AddSyst(
        self.harvester, hfstat1_tag, "shape",
        ch.SystMap( "era" )( [ "16APV" ], 1.0 )( [ "16" ], 1.0 )( [ "17" ], 1.0 )( [ "18" ], 1.0 )
      )
      print( "   + HFSTAT1: 1.0 (shape)" ) 
      count += 1
    
    if config.systematics[ "MC" ][ "lfstats1" ]:
      self.harvester.cp().process( self.signals + self.backgrounds ).channel( shape_categories ).AddSyst(
        self.harvester, lfstat1_tag, "shape",
        ch.SystMap( "era" )( [ "16APV" ], 1.0 )( [ "16" ], 1.0 )( [ "17" ], 1.0 )( [ "18" ], 1.0 )
      )
      print( "   + LFSTAT1: 1.0 (shape)" ) 
      count += 1
    
    if config.systematics[ "MC" ][ "cferr1" ]:
      self.harvester.cp().process( self.signals + self.backgrounds ).channel( shape_categories ).AddSyst(
        self.harvester, cferr1_tag, "shape",
        ch.SystMap( "era" )( [ "16APV" ], 1.0 )( [ "16" ], 1.0 )( [ "17" ], 1.0 )( [ "18" ], 1.0 )
      )
      print( "   + CFERR1: 1.0 (shape)" ) 
      count += 1
    
    if config.systematics[ "MC" ][ "hfstats2" ]:
      self.harvester.cp().process( self.signals + self.backgrounds ).channel( shape_categories ).AddSyst(
        self.harvester, hfstat2_tag, "shape",
        ch.SystMap( "era" )( [ "16APV" ], 1.0 )( [ "16" ], 1.0 )( [ "17" ], 1.0 )( [ "18" ], 1.0 )
      )
      print( "   + HFSTAT2: 1.0 (shape)" ) 
      count += 1
    
    if config.systematics[ "MC" ][ "lfstats2" ]:
      self.harvester.cp().process( self.signals + self.backgrounds ).channel( shape_categories ).AddSyst(
        self.harvester, lfstat2_tag, "shape",
        ch.SystMap( "era" )( [ "16APV" ], 1.0 )( [ "16" ], 1.0 )( [ "17" ], 1.0 )( [ "18" ], 1.0 )
      )
      print( "   + LFSTAT2: 1.0 (shape)" ) 
      count += 1
    
    if config.systematics[ "MC" ][ "cferr2" ]:
      self.harvester.cp().process( self.signals + self.backgrounds ).channel( shape_categories ).AddSyst(
        self.harvester, cferr2_tag, "shape",
        ch.SystMap( "era" )( [ "16APV" ], 1.0 )( [ "16" ], 1.0 )( [ "17" ], 1.0 )( [ "18" ], 1.0 )
      )
      print( "   + CFERR2: 1.0 (shape)" ) 
      count += 1
    
    print( "[DONE] Added {} standard systematics".format( count ) )
    
  def add_theory_systematics( self ):
    print( "[START] Retrieving theoretical systematics from {}".format( self.templateName ) )
    count = 0
    
    if config.options[ "MODIFY BINNING" ][ "SMOOTH" ]:
      pdf_tag = "PDF{}".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      murf_tag = "MURF{}".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      isr_tag = "ISR{}".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      fsr_tag = "FSR{}".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
    else:
      pdf_tag = "PDF"
      murf_tag = "MURF"
      isr_tag = "ISR"
      fsr_tag = "FSR"
   
    if self.options[ "PDF" ]:
      self.harvester.cp().process( self.signals + self.backgrounds ).channel( self.categories[ "ALL" ] ).AddSyst(
        self.harvester, pdf_tag, "shape",
        ch.SystMap()( 1.0 )
      )
      print( "   + PDF: 1.0 (shape)" )
      count += 1
    
    if config.systematics[ "MC" ][ "muR" ] or config.systematics[ "MC" ][ "muF" ]:
      self.harvester.cp().process( self.signals + self.backgrounds ).channel( self.categories[ "ALL" ] ).AddSyst(
        self.harvester, murf_tag, "shape",
        ch.SystMap()( 1.0 )
      )
      print( "   + MURF: 1.0 (shape)" )
      count += 1
    
    if config.systematics[ "MC" ][ "isr" ]:
      self.harvester.cp().process( self.signals + self.backgrounds ).channel( self.categories[ "ALL" ] ).AddSyst(
        self.harvester, isr_tag, "shape",
        ch.SystMap()( 1.0 )
      )
      print( "   + ISR: 1.0 (shape)" )
      count += 1
    
    if config.systematics[ "MC" ][ "fsr" ]:
      self.harvester.cp().process( self.signals + self.backgrounds ).channel( self.categories[ "ALL" ] ).AddSyst(
        self.harvester, fsr_tag, "shape",
        ch.SystMap()( 1.0 )
      )
      print( "   + FSR: 1.0 (shape)" )
      count += 1
  
    print( "[DONE] Added {} theoretical systematics".format( count ) )
  
  def add_TTHF_systematics( self ):
    if self.options[ "COMBINE" ][ "TTHF SYST" ]:
      print( "[START] Adding heavy flavor (TTBB) systematics" )
      tthf_categories = self.categories[ "ALL" ]
      if self.abcdnn:
        tthf_categories = [ category for category in self.categories[ "ALL" ] if category not in self.categories[ "ABCDNN" ] ]
      
      self.harvester.cp().process( [ "TTBB" ] ).channel( tthf_categories ).AddSyst(
        self.harvester, "TTHF", "lnN",
        ch.SystMap()( config.systematics[ "TTHF" ] )
      )
      print( "[DONE] Added TTHF: {} (lnN)".format( config.systematics[ "TTHF" ] ) )
    else:
      pass
  
  def add_shapes( self ):
    print( "[START] Retrieving histograms from {}".format( self.templateName ) )
    for category in self.categories[ "ALL" ]:
      key_bkg = { 
        "NOMINAL": "$PROCESS_{}$BIN_NOMINAL".format( category ),
        "SYST":    "$PROCESS_{}$BIN_$SYSTEMATIC".format( category )
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
    
  def rename_and_write( self ):
    print( "[START] Setting standardized bin names" )
    ch.SetStandardBinNames( self.harvester )
    
    writer = ch.CardWriter(
      "{}$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt".format( self.limitPath ),
      "{}$TAG/common/$ANALYSIS_$CHANNEL.input.root".format( self.limitPath )
    )
    writer.SetVerbosity(1)
    writer.WriteCards( "cmb", self.harvester )
    count = 0
    for category in sorted( self.categories[ "ALL" ] ):
      print( ">> Writing category: {}".format( category ) )
      writer.WriteCards( category, self.harvester.cp().channel( [ category ] ) )
      count += 1
    print( "[DONE] Wrote {} data cards".format( count ) )
    
  def create_workspace( self ):
    print( ">> Creating workspace for DataCard" )
    outDir = os.path.join( os.getcwd(), self.limitPath, "cmb/" )
    os.system( "combineTool.py -M T2W -i {} -o workspace.root --parallel 4".format( outDir ) )
    
def main():
  params = config.params[ "COMBINE" ].copy()
  options = config.options[ "COMBINE" ].copy()
  datacard = DataCard( 
    args.variable, 
    args.year, 
    args.region, 
    args.tag,
    params, 
    options,
    samples,
    "TTTX" 
  )
  datacard.define_regions( args.mode )
  datacard.add_datasets()
  datacard.add_yield_systematics()
  datacard.add_shape_systematics()
  datacard.add_theory_systematics()
  #datacard.add_TTHF_systematics()
  datacard.add_shapes()
  datacard.add_auto_MC_statistics()
  datacard.rename_and_write()
  
  datacard.create_workspace()
  
main()
