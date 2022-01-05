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

def category_tag( category ):
  return "{}_nH{}_nT{}_nW{}_nB{}_nJ{}".format( 
    category[ "LEPTON" ], 
    category[ "NHOT" ], 
    category[ "NTOP" ], 
    category[ "NW" ], 
    category[ "NB" ], 
    category[ "NJ" ] 
  )
  
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
      N = {
        "TTBB": hists[ "CMB" ][ "TTBB_" + category_tag( category ) ].Integral(),
        "TTNOBB": hists[ "CMB" ][ "TTNOBB_" + category_tag( category ) ].Integral()
      }
      if config.ttLFsf == -1:
        try: ttLFsf = 1. + ( 1. - config.ttLFsf ) * ( N[ "TTBB" ] / N[ "TTNOBB" ] )
        except ZeroDivisionError: ttLFsf = 1.
      
      hists_[ "CMB" ][ "TTBB_" + categoryTag ].Scale( config.ttHFsf )
      hists_[ "CMB" ][ "TTNOBB_" + categoryTag ].Scale( ttLFsf )
      
      if args.systematics:
        for syst in config.systematics[ "MC" ] + [ "HD", "UE" ]:
          for shift in [ "UP", "DN" ]:
            if syst == "HD" and not args.hd: continue
            if syst == "UE" and not args.ue: continue
            hists_[ "CMB" ][ "TTBB_{}_{}{}".format( category_tag( category ), syst.upper(), shift.upper() ) ].Scale( config.ttHFsf )
            hists_[ "CMB" ][ "TTNOBB_{}_{}{}".format( category_tag( category ), syst.upper(), shift.upper() ) ].Scale( ttLFsf )
      if args.pdf:
        for i in range( pdf_range ):
          hists_[ "CMB" ][ "TTBB_{}_PDF{}".format( category_tag( category ), i ) ].Scale( config.ttHFsf )
          hists_[ "CMB" ][ "TTNOBB_{}_PDF{}".format( category_tag( category ), i ) ].Scale( ttLFsf )
          
    return hists_
    
  def set_zero( hists_ ):
    if args.verbose: print( ">> Setting 0 bins to be non-trivial ({}) in histograms".format( config.zero ) )
    for category in categories:
      for process in list( groups[ "BKG" ][ "GROUP" ].keys() ) + groups[ "SIG" ][ "PROCESS" ]:
        if hists[ "{}_{}".format( process, category_tag( category ) ) ].Integral() == 0: 
          hists[ "{}_{}".format( process, category_tag( category ) ) ].SetBinContent( 1, config.zero )
        if args.systematics:
          for syst in config.systematics + [ "HD", "UE" ]:
            for shift in [ "UP", "DN" ]:
              if syst == "HD" and not args.hd: continue
              if syst == "UE" and not args.ue: continue
              if hists[ "{}_{}_{}{}".format( process, category_tag( category ), syst.upper(), shift ) ].Integral() == 0:
                hists[ "{}_{}_{}{}".format( process, category_tag( category ), syst.upper(), shift ) ].SetBinContent( 1, config.zero )
    return hists_
  
  for category in categories:
    catTag = category_tag( category )
    prefix = "{}_{}_{}".format( variable, lumiStr, catTag )
    
    # combine data hists
    hists[ "CMB" ][ "DAT_{}".format( catTag ) ] = hists[ "DAT" ][ "{}_{}".format( prefix, groups[ "DAT" ][ "PROCESS" ][0] ) ].Clone( "{}_DAT".format( prefix ) )
    for process in groups[ "DAT" ][ "PROCESS" ][1:]: hists[ "CMB" ][ "DAT_{}".format( catTag ) ].Add( hists[ "DAT" ][ "{}_{}".format( prefix, process ) ] )
    
    # combine signal hists
    hists[ "CMB" ][ "SIG_{}".format( catTag ) ] = hists[ "SIG" ][ "{}_{}".format( prefix, groups[ "SIG" ][ "PROCESS" ][0] ) ].Clone( "{}_SIG".format( prefix ) )
    for process in groups[ "SIG" ][ "PROCESS" ][1:]: hists[ "CMB" ][ "SIG_{}".format( catTag ) ].Add( hists[ "SIG" ][ "{}_{}".format( prefix, process ) ] )
    
    # combine background hists
		for process in list( groups[ "BKG" ][ "PROCESS" ].keys() ):
      hists[ "CMB" ][ "{}_{}".format( process, catTag ) ] = hists[ "BKG" ][ "{}_{}".format( prefix, groups[ "BKG" ][ "PROCESS" ][0] ) ].Clone( "{}_{}".format( prefix, process )
    
                                                                    
                                                                    
  return hists
      
                              
               
  
nBRconf=len(BRs['BW'])
if not doBRScan: nBRconf=1

if year=='R16':
	from weights16 import *
elif year=='R17':
	from weights17 import *
elif year=='R18':
	from weights18 import *

lumiStr = str(targetlumi/1000).replace('.','p')+'fb' # 1/fb
if theDir.startswith('kinematics'): removeThreshold = 0.0
if not doAllSys: 
	doHDsys = False
	doUEsys = False
	doPDF = False
# if doPDF: writeSummaryHists = False

elcorrdSys = math.sqrt(lumiSys**2+eltrigSys**2+elIdSys**2+elIsoSys**2)#+njetSys**2)
mucorrdSys = math.sqrt(lumiSys**2+mutrigSys**2+muIdSys**2+muIsoSys**2)#+njetSys**2)

if not os.path.exists(outDir): 
	print outDir,'DOES NOT EXIST!!!'
	os._exit(1)
isEMlist = ['E','M']
catList = ['is'+x for x in os.walk(outDir).next()[1] if x.startswith('E_') or x.startswith('M_')]
catList.sort()
tagList = [x[4:] for x in catList if 'isE' in x]
nhottlist = list(set([x.split('_')[0] for x in tagList]))
nttaglist = list(set([x.split('_')[1] for x in tagList]))
nWtaglist = list(set([x.split('_')[2] for x in tagList]))
nbtaglist = list(set([x.split('_')[3] for x in tagList]))
njetslist = list(set([x.split('_')[4] for x in tagList]))

for tag in tagList:
	modTag = tag#[tag.find('nT'):tag.find('nJ')-3]
	modelingSys['data_'+modTag] = 0.
	modelingSys['qcd_'+modTag] = 0.
	if not addCRsys: #else CR uncertainties are defined in modSyst.py module 
		for proc in bkgProcs.keys():
			modelingSys[proc+'_'+modTag] = 0.
	modelingSys['ttbb_'+modTag]=math.sqrt(xsec_ttbar**2+ttHF**2+hDamp**2)#math.sqrt(QCDscale_ttbar**2+pdf_gg**2+ttHF**2)
	modelingSys['ttnobb_'+modTag]=math.sqrt(xsec_ttbar**2+hDamp**2)#math.sqrt(QCDscale_ttbar**2+pdf_gg**2)
	modelingSys['ttH_'+modTag]=xsec_ttH
	modelingSys['top_'+modTag]=xsec_top#math.sqrt(QCDscale_top**2+pdf_qg**2)
	modelingSys['ewk_'+modTag]=xsec_ewk#math.sqrt(QCDscale_ewk**2+pdf_qqbar**2)

