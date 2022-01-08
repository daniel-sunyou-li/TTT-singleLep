#!/usr/bin/python

import os, sys, json, time, math, datetime, pickle, itertools
from argparse import ArgumentParser
import numpy as np
from array import array
import utils, samples
import config

parser = ArgumentParser()
parser.add_argument( "-y", "--year",   required = True )
parser.add_argument( "-t", "--tag", required = True )
parser.add_argument( "-sys", "--systematics", action = "store_true" )
parser.add_argument( "-ue", "--ue", action = "store_true" )
parser.add_argument( "-hd", "--hdamp", action = "store_true" )
parser.add_argument( "-pdf", "--pdf", action = "store_true" )
parser.add_argument( "-rpdf", "--renormPDF", action = "store_true", help = "Normalize renormalization/pdf uncertainties for signal processes" ) 
parser.add_argument( "-cr", "--crsys", action = "store_true" )
parser.add_argument( "-br", "--brscan", action = "store_true" )
parser.add_argument( "-sum", "--summary", action = "store_true", help = "Write Summary Histograms" )
parser.add_argument( "-scale", "--scale", action = "store_true", help = "Scale the signal cross section to 1 pb" )
parser.add_argument( "-ls", "--lumiscale", default = "1", help = "Rescale the target luminosity" )
parser.add_argument( "-rb", "--rebin", default = "-1", help = "Rebin the histograms by given value" )
args = parser.parse_args()

from ROOT import gROOT, TFile, TH1F

gROOT.SetBatch(1)
start_time = time.time()

cutString = ''#'lep30_MET100_NJets4_DR1_1jet250_2jet50'
theDir = 'templates_'+year+'_'+sys.argv[2]
outDir = os.getcwd()+'/'+theDir+'/'+cutString

systematics = config.systematics
if args.year in [ "16", "17" ]: systematics += [ "prefire" ]

def get_categories( directory ):
  category_names = [ "is{}".format( lep ) for lep in os.walk( directory ).next()[1] if lep.startswith( "E_" ) or lep.startswith( "M_" ) ]
  category_names.sort()
  categories = []
  for category_name in category_names:
    category_name = category_name.split( "_" )
    cateogory_dict = {}
    for name in category_name:
      if "IS" in name.upper(): category_dict[ "LEPTON" ] = name[-1]
      if "NH" in name.upper(): category_dict[ "NHOT" ] = name[-2:] if "p" in name else name[-1]
      if "NT" in name.upper(): category_dict[ "NTOP" ] = name[-2:] if "p" in name else name[-1]
      if "NW" in name.upper(): category_dict[ "NW" ] = name[-2:] if "p" in name else name[-1]
      if "NB" in name.upper(): category_dict[ "NB" ] = name[-2:] if "p" in name else name[-1]
      if "NJ" in name.upper(): category_dict[ "NJ" ] = name[-2:] if "p" in name else name[-1]
    categories.append( category_dict )
  return categories
  
def category_tag( category ):
  return "is{}nH{}nT{}nW{}nB{}nJ{}".format( 
    category[ "LEPTON" ], 
    category[ "NHOT" ], 
    category[ "NTOP" ], 
    category[ "NW" ], 
    category[ "NB" ], 
    category[ "NJ" ] 
  )
  
def hist_tag( *args ):
  histTag = args[0]
  for arg in args[1:]: histTag += "_{}".format( arg )
  return histTag
	
def group_process():
  groups = { group: {} for group in [ "BKG", "SIG", "DAT" ] }
  
  groups[ "DAT" ][ "PROCESS" ] = [ "DataE", "DataM" ]
  
  groups[ "SIG" ][ "PROCESS" ] = [ "TTTW", "TTTJ" ]
  
  
  ttbar = [ "TTToHadronic", "TTTo2L2Nu", "TTToSemiLeptonHT500", "TTToSemiLeptonicHT500", "TTToSemiLeptonic" ]
  groups[ "BKG" ][ "PROCESS" ] = {
    "WJETS": [ "WJetsHT200", "WJetsHT400", "WJetsHT600", "WJetsHT800", "WJetsHT1200", "WJetsHT2500" ],
    "DY": [ "DYHT200", "DYHT400", "DYHT600", "DYHT800", "DYHT1200", "DYHT2500" ],
    "QCD": [ "QCDHT200", "QCDHT300", "QCDHT500", "QCDHT700", "QCDHT1000", "QCDHT1500", "QCDHT2000" ],
    "VV": [ "WW", "WZ", "ZZ" ],
    "TOP": [ "Ts", "Tt", "Tbt", "TtW", "TbtW" ],
    "TTV": [ "TTWl", "TTZlM10", "TTHB", "TTHnoB" ], # TTZlM1to10 in-progress
    "TTXY": [ "TTTT", "TTWW", "TTWH", "TTHH", "TTZZ", "TTWZ", "TTZH" ],
    "TTJJ": [ tt + "TTJJ" for tt in ttbar if tt != "TTToSemiLeptonic" ], 
    "TTCC": [ tt + "TTCC" for tt in ttbar ],
    "TT1B": [ tt + "TT1B" for tt in ttbar ],
    "TT2B": [ tt + "TT2B" for tt in ttbar ],
    "TTBB": [ tt + "TTBB" for tt in ttbar ]
  }
  
  if args.year == "17": 
    groups[ "BKG" ][ "PROCESS" ][ "TTJJ" ] += [ "TTToSemiLeptonicTTJJ" + num for num in [ "1", "2", "3", "4" ] ]
    
  # grouped background processes
  groups[ "BKG" ][ "SUPERGROUP" ] = {
    "TTNOBB": np.array( [ groups[ "BKG" ][ "PROCESS" ][ process ] for process in [ "TTJJ", "TTCC", "TT1B", "TT2B" ] ] ).flatten().tolist(),
    "TTBB": groups[ "BKG" ][ "PROCESS" ][ "TTBB" ],
    "TOP": np.array( [ groups[ "BKG" ][ "PROCESS" ][ process ] for process in [ "TOP", "TTV", "TTXY" ] ] ).flatten().tolist(),
    "EWK": np.array( [ groups[ "BKG" ][ "PROCESS" ][ process ] for process in [ "WJETS", "DY", "VV" ] ] ).flatten().tolist(),
    "QCD": groups[ "BKG" ][ "PROCESS" ][ "QCD" ]
  }
  
  groups[ "BKG" ][ "TTBAR_GROUPS" ] = {
    group: groups[ "BKG" ][ "SUPERGROUP" ][ group ] for group in [ "TTNOBB", "TTBB" ]
  }
  
  groups[ "BKG" ][ "TTBAR_PROCESS" ] = {
    process: groups[ "BKG" ][ "PROCESS" ][ process ] for process in [ "TTJJ", "TTCC", "TT1B", "TT2B", "TTBB" ]
  }
  
  groups[ "BKG" ][ "HT" ] = {
    "EWK": groups[ "BKG" ][ "SUPERGROUP" ][ "EWK" ],
    "WJETS": groups[ "BKG" ][ "PROCESS" ][ "WJETS" ],
    "QCD": groups[ "BKG" ][ "SUPERGROUP" ][ "QCD" ]
  }
  
  groups[ "BKG" ][ "TOPPT" ] = {
    process: np.array( [ groups[ "BKG" ][ "PROCESS" ][ process ] for process in [ "TTJJ", "TTCC", "TTBB", "TT1B", "TT2B" ] ] ).flatten().tolist()
  }
  groups[ "BKG" ][ "TOPPT" ][ "TTBJ" ] = np.array( [ groups[ "BKG" ][ "PROCESS" ][ process] for process in [ "TT1B", "TT2B" ] ] ).flatten().tolist()
  groups[ "BKG" ][ "TOPPT" ][ "TTNOBB" ] = groups[ "BKG" ][ "SUPERGROUP" ][ "TTNOBB" ]
  
  groups[ "BKG" ][ "SYSTEMATICS" ] = {}
  syst_key = {
    "HD": "HDAMP", 
    "UE": "UE"
  }
  for syst in [ "HD", "UE" ]:
    for shift in [ "UP", "DN" ]:
      for flav in [ "JJ", "CC", "1B", "2B", "2B" ]:
        for tt in [ "TTToSemiLeptonic", "TTToHadronic", "TTTo2L2Nu" ]:
          groups[ "BKG" ][ "SYSTEMATICS" ][ "TT{}_{}{}".format( flav, syst, shift ) ] = [ "{}{}{}TT{}".format( tt, syst_key[ syst ], shift, flav ) ]
      groups[ "BKG" ][ "SYSTEMATICS" ][ "TTBJ_{}{}".format( syst, shift ) ] = []
      groups[ "BKG" ][ "SYSTEMATICS" ][ "TTNOBB_{}{}".format( syst, shift ) ] = []
      for flav in [ "1B", "2B" ]:
        groups[ "BKG" ][ "SYSTEMATICS" ][ "TTBJ_{}{}".format( syst, shift ) ] += groups[ "BKG" ][ "SYSTEMATICS" ][ "TT{}_{}{}".format( flav, syst, shift ) ]
      for flav in [ "JJ", "CC", "1B", "2B" ]:
        groups[ "BKG" ][ "SYSTEMATICS" ][ "TTNOBB_{}{}".format( syst, shift ) ] += groups[ "BKG" ][ "SYSTEMATICS" ][ "TT{}_{}{}".format( flav, syst, shift ) ]

  return groups
        
def load_histograms( variable, categories ): 
  hists = {
    "DAT": {},
    "BKG": {},
    "SIG": {},
    "CMB": {}
  }
  
  templateDir = os.path.join( os.getcwd(), "makeTemplates/templates_UL{}_{}".format( args.year, args.tag ) ) 
  for category in categories:
    categoryDir = os.path.join( templateDir, category_tag( category ) )
    hists[ "DAT" ].update( pickle.load( open( os.path.join( categoryDir, "data_{}.pkl".format( variable ) ), "rb" ) ) )
    hists[ "BKG" ].update( pickle.load( open( os.path.join( categoryDir, "bkg_{}.pkl".format( variable ) ), "rb" ) ) )
    hists[ "SIG" ].update( pickle.load( open( os.path.join( categoryDir, "sig_{}.pkl".format( variable ) ), "rb" ) ) )
    
  return hists
  
def modify_histograms( hists, doScale, doRebin, doNegCorr, doBinCorr ):
  def scale_luminosity( hists_ ):
    if args.verbose: print( ">> Re-scaling MC luminosity by factor: {}".format( args.lumiscale ) )
    for ikey in [ "BKG", "SIG" ]:
      for jkey in hists_[ ikey ]: hists[ ikey ][ jkey ].Scale( args.lumiscale )
    return hists_
  
  def rebinning( hists_ ):
    if args.verbose: print( ">> Re-binning histogram bins by: {}".format( args.rebin ) )
    for ikey in [ "BKG", "SIG", "DAT" ]:
      for jkey in hists_[ ikey ]: hists[ ikey ][ jkey ].Rebin( args.rebin )
    return hists_
  
  def negative_correction( hists_ ):
    def function( hist_ ):
      integral = hist.Integral()
      for i in range( hist_.GetNbinsX() + 2 ):
        if hist_.GetBinContent( i ) < 0:
          hist_.SetBinContent( i, 0 )
          hist_.SetBinError( i, 0 )
      if hist_.Integral() != 0 and integral > 0: hist.Scale( integral / hist.Integral() )
      return hist_
      
    if args.verbose: print( ">> Correcting negative histogram bins" )
    for ikey in [ "BKG", "SIG" ]:
      for jkey in hists_[ ikey ]:
        hists_[ ikey ][ jkey ] = function( hists_[ ikey ][ jkey ] )
    return hists_
  
  def bin_correction( hists_ ):
    def function( hist_ ):
      # overflow
      n = hist_.GetXaxis().GetNbins()
      content_over = hist_.GetBinContent( n ) + hist_.GetBinContent( n + 1 )
      error_over = math.sqrt( hist_.GetBinError( n )**2 + hist_.GetBinError( n + 1 )**2 )
      hist_.SetBinContent( n, content_over )
      hist_.SetBinError( n, error_over )
      hist_.SetBinContent( n + 1, 0 )
      hist_.SetBinError( n + 1, 0 )
      # underflow
      content_under = hist_.GetBinContent( 1 ) + hist_.GetBinContent( 0 )
      error_under = math.sqrt( hist_.GetBinError( 1 )**2 + hist_.GetBinError( 0 )**2 )
      hist_.SetBinContent( 1, content_under )
      hist_.SetBinError( 1, error_under )
      hist_.SetBinContent( 0, 0 )
      hist_.SetBinError( 0, 0 )
      return hist_
    
    if args.verbose: print( ">> Correcting over/under-flow bins" )
    for ikey in [ "DAT", "BKG", "SIG" ]:
      for jkey in hists_[ ikey ]:
        hists[ ikey ][ jkey ] = function( hists_[ ikey ][ jkey ] )
    
    return hists_
  
  if args.lumiscale != 1.: hists = scale_luminosity( hists )
  if args.rebin > 0: hists = rebinning( hists )
  hists = negative_correction( hists )
  hists = bin_correction( hists )
  
  return hists
  
def consolidate_histograms( hists, variable, categories ):
  def scale_ttbar( hists_ ):
    if args.verbose: print( ">> Scaling ttbb by a factor of {:.2f}".format( config.ttHFsf ) )
    for category in categories:
      catTag = category_tag( category )
      N = {
        "TTBB": hists[ "CMB" ][ hist_key( "TTBB", catTag ) ].Integral(),
        "TTNOBB": hists[ "CMB" ][ hist_key( "TTNOBB", catTag ) ].Integral()
      }
      if config.ttLFsf == -1:
        try: ttLFsf = 1. + ( 1. - config.ttLFsf ) * ( N[ "TTBB" ] / N[ "TTNOBB" ] )
        except ZeroDivisionError: ttLFsf = 1.
      
      hists_[ "CMB" ][ hist_key( "TTBB", catTag ) ].Scale( config.ttHFsf )
      hists_[ "CMB" ][ hist_key( "TTNOBB", catTag ) ].Scale( ttLFsf )
      
      if args.systematics:
        for syst in config.systematics[ "MC" ] + [ "HD", "UE" ]:
          if syst == "HD" and not args.hd: continue
          if syst == "UE" and not args.ue: continue
          for shift in [ "UP", "DN" ]:
            hists_[ "CMB" ][ hist_key( "TTBB", catTag, syst.upper() + shift ) ].Scale( config.ttHFsf )
            hists_[ "CMB" ][ hist_key( "TTNOBB", catTag, syst.upper() + shift ) ].Scale( ttLFsf )
      if args.pdf:
        for i in range( config.pdf_range ):
          hists_[ "CMB" ][ hist_key( "TTBB", catTag, "PDF" + i )  ].Scale( config.ttHFsf )
          hists_[ "CMB" ][ hist_key( "TTNOBB", catTag, "PDF" + i ) ].Scale( ttLFsf )
          
    return hists_
    
  def set_zero( hists_ ):
    if args.verbose: print( ">> Setting 0 bins to be non-trivial ({}) in histograms".format( config.zero ) )
    for category in categories:
      catTag = category_tag( category )
      for process in list( groups[ "BKG" ][ "GROUP" ].keys() ) + groups[ "SIG" ][ "PROCESS" ]:
        if hists[ hist_key( process, catTag ) ].Integral() == 0: 
          hists[ hist_key( process, catTag ) ].SetBinContent( 1, config.zero )
        if args.systematics:
          for syst in config.systematics + [ "HD", "UE" ]:
              if syst == "HD" and not args.hd: continue
              if syst == "UE" and not args.ue: continue
            for shift in [ "UP", "DN" ]:
              sysTag = syst.upper() + shift
              if hists[ hist_key( process, catTag, sysTag ) ].Integral() == 0:
                hists[ hist_key( process, catTag, sysTag ) ].SetBinContent( 1, config.zero )
    return hists_
  
  for category in categories:
    catTag = category_tag( category )
    prefix = "{}_{}_{}".format( variable, lumiStr, catTag )
    
    # combine data hists
    hists[ "CMB" ][ hist_key( "DAT", catTag ) ] = hists[ "DAT" ][ hist_key( prefix, groups[ "DAT" ][ "PROCESS" ][0] ) ].Clone( hist_key( prefix, "DAT" ) )
    for process in groups[ "DAT" ][ "PROCESS" ][1:]: hists[ "CMB" ][ hist_key( "DAT", catTag ) ].Add( hists[ "DAT" ][ hist_key( prefix, process ) ] )
    
    # combine signal hists
    hists[ "CMB" ][ hist_key( "SIG", catTag ) ] = hists[ "SIG" ][ hist_tag( prefix, groups[ "SIG" ][ "PROCESS" ][0] ) ].Clone( hist_key( prefix, "SIG" ) )
    for process in groups[ "SIG" ][ "PROCESS" ][1:]: hists[ "CMB" ][ hist_tag( "SIG", catTag ) ].Add( hists[ "SIG" ][ hist_tag( prefix, process ) ] )
    
    # combine background hists
		for process in groups[ "BKG" ][ "PROCESS" ]:
      hists[ "CMB" ][ hist_key( process, catTag ) ] = hists[ "BKG" ][ hist_key( prefix, groups[ "BKG" ][ "PROCESS" ][ process ][0] ) ].Clone( hist_key( prefix, process ) )
      for sample in groups[ "BKG" ][ "PROCESS" ][ process ][1:]: hists[ "CMB" ][ hist_key( process, catTag ) ].Add( hists[ "BKG" ][ hist_key( prefix, sample ) ] )
      
    for group in groups[ "BKG" ][ "SUPERGROUP" ]:
      hists[ "CMB" ][ hist_key( group, catTag ) ] = hists[ "BKG" ][ hist_key( prefix, groups[ "BKG" ][ "SUPERGROUP" ][ group ][0] ) ].Clone( hist_key( prefix, group ) )
      for sample in groups[ "BKG" ][ "SUPERGROUP" ][ group ][1:]: hists[ "CMB" ][ hist_key( group, catTag ) ].Add( hists[ "BKG" ][ hist_key( prefix, sample ) ] )
        
    if args.systematics:
      for syst in systematics + [ "HD", "UE" ]:
        if syst == "HD" and not args.hd: continue
        if syst == "UE" and not args.ue: continue
        for shift in [ "UP", "DN" ]:
          sysTag = syst.upper() + shift
          prefix = "{}_{}_{}_{}".format( variable, sysTag, lumiStr, catTag )
          
          hists[ "CMB" ][ hist_tag( "SIG", catTag, sysTag ) ] = hists[ "SIG" ][ hist_tag( prefix, groups[ "SIG" ][ "PROCESS" ][0] ) ].Clone( hist_tag( prefix, "SIG" ) )
          for process in groups[ "SIG" ][ "PROCESS" ][1:]: hists[ "CMB" ][ hists( "SIG", catTag, sysTag ) ].Add( hists[ "SIG" ][ hist_tag( prefix, process ) ] )
          
          for process in groups[ "BKG" ][ "PROCESS" ]:
            hists[ "CMB" ][ hist_key( process, catStr, sysTag ) ] = hists[ "BKG" ][ hist_key( prefix, groups[ "BKG" ][ "PROCESS" ][ process ][0] ) ].Clone( hist_key( prefix, process ) )
            for sample in groups[ "BKG" ][ "PROCESS" ][ process ][1:]: hists[ "CMB" ][ hist_key( process, catStr, sysTag ) ].Add( hists[ "BKG" ][ hist_key( prefix, sample ) ] )
          
          for group in groups[ "BKG" ][ "SUPERGROUP" ]:
            hists[ "CMB" ][ hist_key( group, catStr, sysTag ) ] = hists[ "BKG" ][ hist_key( prefix, groups[ "BKG" ][ "SUPERGROUP" ][ group ][0] ) ].Clone( hist_key( prefix, group ) )
            for sample in groups[ "BKG" ][ "SUPERGROUP" ][ group ][1:]: hists[ "CMB" ][ hist_key( group, catStr, sysTag ) ].Add( hists[ "BKG" ][ hist_key( prefix, sample ) ] )
     
    if args.pdf:
      for i in range( config.pdf_range)
        prefix = "{}_PDF{}_{}_{}".format( variable, i, lumiStr, catTag )
        
        hists[ "CMB" ][ hist_key( "SIG", catStr, "PDF" + i ) ] = hists[ "SIG" ][ hist_key( prefix, groups[ "SIG" ][ "PROCESS" ][0] ) ].Clone( hist_key( prefix, "SIG" )  )
        for sample in groups[ "SIG" ][ "PROCESS" ][1:]: hists[ "CMB" ][ hist_key( "SIG", catStr, "PDF" + i ) ].Add( hists[ "SIG" ][ hist_key( prefix, sample ) ] )
        
        for process in groups[ "BKG" ][ "PROCESS" ]:
          hists[ "CMB" ][ hist_key( process, catStr, "PDF" + i ) ] = hists[ "BKG" ][ hist_key( prefix, groups[ "BKG" ][ "PROCESS" ][ process ][0] ) ].Clone( hist_key( prefix, process ) )
          for sample in groups[ "BKG" ][ "PROCESS" ][ process ][1:] hists[ "CMB" ][ hist_key( process, catStr, "PDF" + i ) ].Add( hists[ "BKG" ][ hist_key( prefix, sample ) ] )
          
        for group in groups[ "BKG" ][ "SUPERGROUP" ]:
          hists[ "CMB" ][ hist_key( group, catStr, "PDF" + i ) ] = hists[ "BKG" ][ hist_key( prefix, groups[ "BKG" ][ "SUPERGROUP" ][ group ][0] ) ].Clone( hist_key( prefix, group ) )
          for sample in groups[ "BKG" ][ "SUPERGROUP" ][ group ][1:] hists[ "CMB" ][ hist_key( group, catStr, "PDF" + i ) ].Add( hists[ "BKG" ][ hist_key( prefix, sample ) ] )
                                                                                                                                                     
  for key in hists[ "CMB" ]: hists[ "CMB" ][ key ].SetDirectory(0)
  if ttHFsf != 1 and "TTBB" in groups[ "BKG" ][ "TTBAR_GROUPS" ].keys(): hists = scale_ttbar( hists )
  hists = set_zero( hists )
 
  return hists

def combine_templates( hists, variable, categories ):
  print( ">> Writing Combine templates" )
  combine_name = "template_combine_{}_{}.root".format( variable, lumiStr )
  combine_file = TFile( combine_name, "RECREATE" )
  
  for category in categories:
  	catTag = category_tag( category )
		
		histKey = "DAT_{}".format( catTag )
		hists[ "CMB" ][ hist_key( "DAT", catTag ) ].SetName( hists[ "CMB" ][ hist_key( "DAT", catTag ) ].GetName().replace( "DAT", "data_obs" ) )
		hists[ "CMB" ][ hist_key( "DAT", catTag ) ].Write()
		
		for process in groups[ "SIG" ][ "PROCESS" ]:
			hists[ "SIG" ][ hist_key( process, catTag ) ].SetName( hists[ "SIG" ][ hist_key( process, catTag ) ].GetName() )
			hists[ "SIG" ][ histKey ].Write()
			if args.systematics:
				for syst in config.systematics + [ "HD", "UE" ]:
					if syst == "HD" and not args.hd: continue
					if syst == "UE" and not args.ue: continue
					if syst.upper() == "TOPPT" or syst.upper() == "HT": continue
					for shift in [ "UP", "DN" ]:
						hists[ "SIG" ][ hist_key( process, catTag, syst.upper() + shift ) ].SetName( hists[ hist_key( process, catTag, syst.upper() + shift ) ].GetName() )
						hists[ "SIG" ][ hist_key( process, catTag, syst.upper() + shift ) ].Write()
			if args.pdf:
				for i in range( config.pdf_range ):
          hists[ "SIG" ][ hist_key( process, catTag, "PDF" + i ) ].SetName( hists[ hist_key( process, catTag, "PDF" + i ) ] ).GetName() )
          hists[ "SIG" ][ hist_key( process, catTag, "PDF" + i ) ].Write()
		
		bkg_total = sum( [ hists[ "CMB" ][ hist_key( group, catTag ) ].Integral() for group in groups[ "BKG" ][ "SUPERGROUP" ] ] )
    for group in groups[ "BKG" ][ "SUPERGROUP" ]:
      if hists[ "CMB" ][ hist_key( group, catTag ) ].Integral( 1, hists[ "CMB" ][ hist_key( group, catTag ) ].GetXaxis().GetNbins() ) / bkg_total <= config.ratio_threshold:
        print( "[WARN] {} beneath threshold, excluding from template".format( group ) )
        continue
      hists[ "CMB" ][ hist_key( group, catTag ) ].SetName( hists[ "CMB" ][ hist_key( group, catTag ) ].GetName() )
      hists[ "CMB" ][ hist_key( group, catTag ) ].Write()
      
      if args.systematics:
        for syst in config.systematics + [ "HD", "UE" ]:
          if syst == "HD" and not args.hd: continue
          if syst == "UE" and not args.ue: continue
          for shift in [ "UP", "DN" ]:
            sysTag = syst.upper() + shift
            hists[ "CMB" ][ hist_key( group, catTag, sysTag ) ].SetName( hists[ "CMB" ][ hist_key( group, catTag, sysTag ) ].GetName() )
            hists[ "CMB" ][ hist_key( group, catTag, sysTag ) ].Write()
            
      if args.pdf:
        for i in range( config.pdf_range ):
          hists[ "CMB" ][ hist_key( group, catTag, "PDF" + i ) ].SetName( hists[ "CMB" ][ hist_key( group, catTag, "PDF" + i ) ].GetName() )
          hists[ "CMB" ][ hist_key( group, catTag, "PDF" + i ) ].Write()
                                   
    combine_file.Close()
    print( "[DONE] Finished writing Combine templates." )        

    
"""
def make_tables( hists, variable ):
  def initialize():
    return tables
  
  def table_systematics( tables, category ):

    return tables
    
  return tables
  
def theta_templates( hists ):

def summary_templates( hists ):

def print_tables( tables, variable ):
  def nominal_table():
  
  def an_table():
  
  def pas_table( tables ):
  
  def systematic_table( tables ):
  
  def print_table():
"""
  
def main():
  groups = group_process()
  for variable in args.variables:
    print( ">> Producing histograms and tables for: {}".format( variable ) )
    hists = load_histograms( variable, categories )
    hists = correct_histograms( hists )
    hists = consolidate_histograms( hists )
    #tables = make_tables( hists )
    #theta_templates( hists )
    combine_templates( hists, variable, categories )
    #summary_templates( hists )
    #print_tables( tables, variable )
    del hists
    #del tables

