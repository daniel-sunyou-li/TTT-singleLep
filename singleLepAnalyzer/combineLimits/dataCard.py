#!/usr/bin/env python

import os, sys, math
from argparse import ArgumentParser
sys.path.append( "../" )
import config

parser = ArgumentParser()
parser.add_argument( "-y", "--year", required = True, help = "16APV,16,17,18" )
parser.add_argument( "-t", "--tag", required = True )
parser.add_argument( "-r", "--region", required = True, help = ",".join( list( config.region_prefix.keys() ) ) )
parser.add_argument( "-v", "--variable", required = True )
parser.add_argument( "--verbose", action = "store_true" )
args = parser.parse_args()

import ROOT


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

def jet_count( category )
  parts = category.split( "n" )
  jet_count = 0
  for part in parts:
    if part.startswith("is"): continue
    elif part.startswith("HOT"): jet_count += int( part[3] )
    else part.startswith("B"): jet_count += int( part[1] )
  return jet_count

class DataCard():
  def __init__( variable, year, region, tag, params, options, prefix ):
    self.harvester = ch.CombineHarvester()
    self.variable = variable
    self.year = year
    self.region = region
    self.tag = tag
    self.lumistr = config.lumiStr[ self.year ]
    self.regions = {
      "SIGNAL":  [],
      "CONTROL": []
    }
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
    os.system( "cp -vp {} ./{}".format( self.templatePath, self.limitPath ) )
    
    templateFile = ROOT.TFile( templateName )
    self.hist_names = [ rKey.GetName() for rKey in self.templateFile.GetListOfKeys() if not hist_parse( rKey.GetName() )[ "IS SYST" ] ]
    templateFile.Close()
    
    self.categories = { "ALL": list( set( hist_name.split( "_" )[-2] for hist_name in self.hist_names ) ) }
    self.categories[ "E" ] =   [ category for category in self.categories[ "ALL" ] if "isE" in category ]
    self.categories[ "M" ] =   [ category for category in self.categories[ "ALL" ] if "isM" in category ]
    self.categories[ "B" ] =   [ category for category in self.categories[ "ALL" ] if "nB0p" not in category ]
    self.categories[ "HOT" ] = [ category for category in self.categories[ "ALL" ] if "nHOI0p" not in category ]
    self.categories[ "T" ] =   [ category for category in self.categories[ "ALL" ] if "nT0p" not in category ]
    self.categories[ "W" ] =   [ category for category in self.categories[ "ALL" ] if "nW0p" not in category ]

    for nJ in range( 4, 11 ):
      self.categories[ "NJ{}".format( nJ ) ] = [ category for category in self.categories if "nJ{}".format( nJ ) in category ]
    
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
      parse = hist_parse( hist_name )
      if parse[ "GROUP" ] == "SIG":
        if parse[ "IS SYST" ]: 
          if parse[ "CATEGORY" ] not in self.hist_groups[ "SIG SYST" ].keys():
            self.hist_groups[ "SIG SYST" ][ parse[ "CATEGORY" ] ] = [ parse[ "PROCESS" ] ]
          else: 
            self.hist_groups[ "SIG SYST" ][ parse[ "CATEGORY" ] ].append( parse[ "PROCESS" ] )
        else: 
          if parse[ "CATEGORY" ] not in self.hist_groups[ "SIG" ].keys():
            self.hist_groups[ "SIG" ][ parse[ "CATEGORY" ] ] = [ parse[ "PROCESS" ] ]
          else:
            self.hist_groups[ "SIG" ][ parse[ "CATEGORY" ] ].append( parse[ "PROCESS" ] )
      elif parse[ "GROUP" ] == "BKG":
        if parse[ "IS SYST" ]: 
          if parse[ "CATEGORY" ] not in self.hist_groups[ "BKG SYST" ].keys():
            self.hist_groups[ "BKG SYST" ][ parse[ "CATEGORY" ] ] = [ parse[ "PROCESS" ] ]
          else: 
            self.hist_groups[ "BKG SYST" ][ parse[ "CATEGORY" ] ].append( parse[ "PROCESS" ] )
        else: 
          if parse[ "CATEGORY" ] not in self.hist_groups[ "BKG" ].keys():
            self.hist_groups[ "BKL" ][ parse[ "CATEGORY" ] ] = [ parse[ "PROCESS" ] ]
          else:
            self.hist_groups[ "BKG" ][ parse[ "CATEGORY" ] ].append( parse[ "PROCESS" ] )
      else:
        if parse[ "CATEGORY" ] not in self.hist_groups[ "DAT" ].keys():
          self.hist_groups[ "DAT" ][ parse[ "CATEGORY" ] ] = [ parse[ "PROCESS" ] ]
        else:
          self.hist_groups[ "DAT" ][ parse[ "CATEGORY" ] ].append( parse[ "PROCESS" ] )
          
    self.masses = ch.ValsFromRange( "690" )
    
  def define_regions( self, mode = 0 ):
  # mode 0: make all regions "SIGNAL REGION" --> default
  # mode 1: make only the uppermost region the "SIGNAL REGION"
  # mode 2: make only the lowermost region the "CONTROL REGION"
  # mode 3: make all regions "CONTROL REGION"
    print( "[START] Defining signal and control regions using mode {}".format( mode ) )
    min_category = jet_count[ self.categories[ "ALL" ][0] ]
    max_category = jet_count[ self.categories[ "ALL" ][0] ]
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
  
  def add_systematics( self ):
    print( "[START] Retrieving systematic uncertainties from {}".format( self.templateName ) )
    count = 0
    print( ">> Adding systematics for both signal and background processes:" )
    
    self.harvester.cp().process( self.signals + self.backgrounds ).channel( self.categories][ "ALL" ] ).AddSyst( 
      self.harvester, "LUMI_$ERA", "lnN",
      self.harvester.SystMap( "era" )( [ "16APV" ], config.systematics[ "LUMI" ][ "16APV" ] )( [ "16" ], config.systematics[ "LUMI" ][ "16" ] )( [ "17" ], config.systematics[ "LUMI" ][ "17" ] )( [ "18" ], config.systematics[ "LUMI" ][ "18" ] )
    )
    print( "   + Luminosity {}: {} (lnN)".format( self.year, config.systematics[ "LUMI" ][ self.year ] ) )
    count += 1
    
    self.harvester.cp().process( self.signals + self.backgrounds ).channel( self.categories[ "E" ] ).AddSyst( 
      self.harvester, "SF_EL_$ERA", "lnN",
      self.harvester.SystMap( "era" )( [ "16APV" ], config.systematics[ "ID" ][ "E" ] )( [ "16" ], config.systematics[ "ID" ][ "E" ] )( [ "17" ], config.systematics[ "ID" ][ "E" ] )( [ "18" ], config.systematics[ "ID" ][ "E" ] )
    )
    print( "   + Trigger (el) {}: {} (lnN)".format( self.year, config.systematics[ "ID" ][ "E" ] ) )
    count += 1
    
    self.harvester.cp().process( self.signals + self.backgrounds ).channel( self.categories[ "M" ] ).AddSyst( 
      self.harvester, "SF_MU_$ERA", "lnN",
      self.harvester.SystMap( "era" )( [ "16APV" ], config.systematics[ "ID" ][ "M" ] )( [ "16" ], config.systematics[ "ID" ][ "M" ] )( [ "17" ], config.systematics[ "ID" ][ "M" ] )( [ "18" ], config.systematics[ "ID" ][ "M" ] )
    )
    print( "   + Trigger (mu) {}: {} (lnN)".format( self.year, config.systematics[ "ID" ][ "E" ] ) )
    count += 1
    
    self.harvester.cp().process( [ bkg for bkg in self.backgrounds if "TT" in bkg ] ).channel( self.categories[ "ALL" ] ).AddSyst(
      self.harvester, "xsec_ttbar", "lnN",
      self.harvester.SystMap()( config.systematics[ "XSEC" ][ "TTBAR" ] )
    )
    print( "   + TTBAR: {} (lnN)".format( config.systematics[ "XSEC" ][ "TTBAR" ] ) )
    count += 1
    
    self.harvester.cp().process( [ "EWK" ] ).channel( self.categories[ "ALL" ] ).AddSyst(
      self.harvester, "xsec_ewk", "lnN",
      self.harvester.SystMap()( config.systematics[ "XSEC" ][ "EWK" ] )
    )
    print( "   + EWK: {} (lnN)".format( config.systematics[ "XSEC" ][ "EWK" ] ) )
    count += 1
    
    self.harvester.cp().process( [ "TOP" ] ).channel( self.categories[ "ALL" ] ).AddSyst(
      self.harvester, "xsec_top", "lnN",
      self.harvester.SystMap()( config.systematics[ "XSEC" ][ "TOP" ] )
    )
    print( "   + TOP: {} (lnN)".format( config.systematics[ "XSEC" ][ "TOP" ] ) )
    count += 1
    
    if config.options[ "MODIFY BINNING" ][ "SMOOTH" ]:
      jec_tag = "JEC_{}_$ERA".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      jer_tag = "JER_{}_$ERA".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      hf_tag = "HF_{}_$ERA".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      lf_tag = "LF_{}_$ERA".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      hfstat1_tag = "HFSTAT1_{}_$ERA".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      lfstat1_tag = "LFSTAT1_{}_$ERA".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
      cfstat1_tag = "CFSTAT1_{}_$ERA".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )
    else:
      jec_tag = "JEC_$ERA"
      jer_tag = "JER_$ERA"
      hf_tag = "HF_$ERA"
      lf_tag = "LF_$ERA"
      hfstat1_tag = "HFSTAT1_$ERA"
      lfstat1_tag = "LFSTAT1_$ERA"
      cfstat1_tag = "CFSTAT1_$ERA"
      
    self.harvester.cp().process( self.signals + self.backgrounds ).channel( self.categories[ "ALL" ] ).AddSyst(
      self.harvester, jec_tag, "shape",
      self.harvester.SystMap( "era" )( [ "16APV" ], 1.0 )( [ "16" ], 1.0 )( [ "17" ], 1.0 )( [ "18" ], 1.0 )
    )
    print( "   + JEC: 1.0 (shape)" )
    count += 1
    
    self.harvester.cp().process( self.signals + self.backgrounds ).channel( self.categories[ "ALL" ] ).AddSyst(
      self.harvester, jer_tag, "shape",
      self.harvester.SystMap( "era" )( [ "16APV" ], 1.0 )( [ "16" ], 1.0 )( [ "17" ], 1.0 )( [ "18" ], 1.0 )
    )
    print( "   + JER: 1.0 (shape)" ) 
    count += 1
    
    self.harvester.cp().process( self.signals + self.backgrounds ).channel( self.categories[ "ALL" ] ).AddSyst(
      self.harvester, hf_tag, "shape",
      self.harvester.SystMap( "era" )( [ "16APV" ], 1.0 )( [ "16" ], 1.0 )( [ "17" ], 1.0 )( [ "18" ], 1.0 )
    )
    print( "   + HF: 1.0 (shape)" ) 
    count += 1
    
    self.harvester.cp().process( self.signals + self.backgrounds ).channel( self.categories[ "ALL" ] ).AddSyst(
      self.harvester, lf_tag, "shape",
      self.harvester.SystMap( "era" )( [ "16APV" ], 1.0 )( [ "16" ], 1.0 )( [ "17" ], 1.0 )( [ "18" ], 1.0 )
    )
    print( "   + LF: 1.0 (shape)" )     
    count += 1
    
    self.harvester.cp().process( self.signals + self.backgrounds ).channel( self.categories[ "ALL" ] ).AddSyst(
      self.harvester, hfstat1_tag, "shape",
      self.harvester.SystMap( "era" )( [ "16APV" ], 1.0 )( [ "16" ], 1.0 )( [ "17" ], 1.0 )( [ "18" ], 1.0 )
    )
    print( "   + HFSTAT1: 1.0 (shape)" ) 
    count += 1
    
    print( "[DONE] Added {} standard systematics".format( count ) )
    
  def add_TTHF_systematics( self ):
    if self.params[ "TTHF SYST" ]:
      print( "[START] Adding heavy flavor (TTBB) systematics" )
      self.harvester.cp().process( [ "TTBB" ] ).channel( self.categories[ "ALL" ] ).AddSyst(
        self.harvester, "TTHF", "lnN",
        self.harvester.SystMap()( config.systematics[ "TTHF" ] )
      )
      print( "[DONE] Added TTHF: {} (lnN)".format( config.systematics[ "TTHF" ] ) )
    else:
      pass
  
  def add_shapes( self ):
    print( "[START] Retrieving shape uncertainties from {}".format( self.templateName ) )
    for category in self.categories[ "ALL" ]:
      key_bkg = { 
        "NOMINAL": "$PROCESS_{}_$BIN".format( category )
        "SYST":    "$PROCESS_{}_$BIN_$SYSTEMATIC".format( category )
      }
      self.harvester.cp().channel( [ category ] ).era( [ self.year ] ).backgrounds().ExtractShapes(
        self.templateName, key_bkg[ "NOMINAL" ], key_bkg[ "SYST" ]
      )
      key_sig = { 
        "NOMINAL": "$PROCESS$MASS_{}_$BIN".format( category )
        "SYST":    "$PROCESS$MASS_{}_$BIN_$SYSTEMATIC".format( category )
      }
      if category not in self.regions[ "CONTROL" ]:
        self.harvester.cp().channel( [ category ] ).era( [ self.year ] ).signals().ExtractShapes(
          self.templateName, key_sig[ "NOMINAL" ], key_sig[ "SYST" ]
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
    "TTTX" 
  )
  datacard.define_regions()
  datacard.add_datasets()
  datacard.add_systematics()
  datacard.add_TTHF_systematics()
  datacard.add_shapes()
  datacard.add_auto_MC_statistics()
  datacard.rename_and_write()
  
  datacard.create_workspace()
  
main()
