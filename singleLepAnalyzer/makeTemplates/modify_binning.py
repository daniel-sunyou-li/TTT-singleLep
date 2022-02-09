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


def get_categories( directory ):
  categories = [ directory for directory in os.walk( directory ).next()[1] if directory.startswith( "isE" ) or directory.startswith( "isM" ) ]
  return categories

def hist_tag( *args ):
  histTag = args[0]
  for arg in args[1:]: histTag += "_{}".format( arg )
  return histTag

def rebinning( file_path ):
  def rebin( rFile_in, xBins, hist_name, channel ): # done
    hist = rFile_in.Get( hist_name ).Rebin(
      len( xBins[ channel ] ) - 1,
      hist_name,
      xBins[ channel ]
    )
    hist.SetDirectory(0)
    utils.overflow( hist )
    utils.underflow( hist )
    
    if "DNN" in hist_name.upper() and args.blind and "DAT" in hist_name.upper():
      zeroBin = hist.FindBin(0)
      maxBin = hist.GetNbinsX() + 1
      for i in range( zeroBin, maxBin ): hist.SetBinContent( i, -100.0 )
        
    print( ">> Writing {}".format( hist_name ) )
    hist.Write()
  
    return hist
  
  def symmetrize_topPT_shift( hists, channel, hist_name ): # done
    for i in range( 1, hists[ channel ][ hist_name ].GetNbinsX() + 1 ):
      hists[ channel ][ hist_name ].SetBinContent( 
        i, 
        2. * hists[ channel ][ hist_name.replace( "_TOPPTDN", "" ) ].GetBinContent(i) - hists[ channel ][ hist_name.replace( "TOPPTDN", "TOPPTUP" ) ].GetBinContent(i) 
      )
      
    hists[ channel ][ hist_name ].Write()
      
    return hists

  def add_trigger_efficiency( hists, channel, hist_name ): # done
    # specify trigger efficiencies for the single leptons
    if "ISE" in hist_name.upper():
      hist_name_el = hists[ channel ][ hist_name ].GetName().replace( "TRIGEFF", "ELTRIGGEFF" )
      hists[ channel ][ hist_name_el ] = hists[ channel ][ hist_name ].Clone( hist_name_el )
      hists[ channel ][ hist_name_el ].Write()
    if "ISM" in hist_name.upper():
      hist_name_mu = hists[ channel ][ hist_name ].GetName().replace( "TRIGEFF", "MUTRIGEFF" )
      hists[ channel ][ hist_name_mu ] = hists[ channel ][ hist_name ].Clone( hist_name_mu )
      hists[ channel ][ hist_name_mu ].Write()
      
    return hists

  def uncorrelate_year( hists, channel, hist_name ): # done
    # differentiate the shifts by year
    hist_name_uncorr = hists[ channel ][ hist_name ].GetName().replace( "UP", "{}UP".format( args.year ) ).replace( "DN", "{}DN".format( args.year ) )
    hists[ channel ][ hist_name_uncorr ] = hists[ channel ][ hist_name ].Clone( hist_name_uncorr )
    hists[ channel ][ hist_name_uncorr ].Write()
    
    return hists

  def get_yield_stats( yields, yield_errors, hists, channel, hist_name ): # done
    # get the integral yield for each bin as well as the associated error
    yields[ channel ][ hist_name ] = hists[ channel ][ hist_name ].Integral()
    yields_errors[ channel ][ hist_name ] = 0
    for i in range( 1, hists[ channel ][ hist_name ].GetXaxis().GetNbins() + 1 ):
      yields_errors[ channel ][ hist_name ] += hists[ channel ][ hist_name ].GetBinError( i )**2
    yields_errors[ channel ][ hist_name ] = math.sqrt( yields_errors[ channel ][ hist_name ] )
    
    return yields, yield_errors
  
  def add_statistical_shapes( hists, channel ): # done
    # add shifts to the bin content for the statistical shape uncertainty
    def write_statistical_hists( hists, group, channel, hist_name_temp, i, nBB ):
      if hists[ channel ][ "TOTALBKG" ].GetNbinsX() == 1 or group == "SIG":
        for process in groups[ group ][ "PROCESS" ]:
          value = hists[ channel ][ hist_name_temp.replace( "DAT", process ) ].GetBinContent(i)
          if value == 0: continue
          error = hists[ channel ][ hist_name_temp.replace( "DAT", process ) ].GetBinError(i)
          hist_name_err = { shift: "{}__CMS_TTTX_{}_UL{}_{}_BIN{}{}".format(
            hists[ channel ][ hist_name_ch.replace( "DAT", process ) ].GetName(),
            channel, args.year, process, i, shift ) for shift in [ "UP", "DN" ] 
          }
          for shift in [ "UP", "DN" ]:
            hists[ channel ][ hist_name_err[ shift ] ] = hists[ channel ][ hist_name_temp.replace( "DAT", process ) ].Clone( hist_name_err[ shift ] )
            if shift == "UP": hists[ channel ][ hist_name_err[ shift ] ].SetBinContent( i, value + error )
            if shift == "DN": hists[ channel ][ hist_name_err[ shift ] ].SetBinContent( i, value - error )
            if value - error < 0: 
              print( ">> Correcting negative bin for {} in channel {}".format( hist_name_err[ shift ], channel ) )
              negative_bin_correction( hists[ channel ][ hist_name_err[ shift ] ] ) # need to update this
            if value - error == 0: hists[ channel ][ hist_name_err[ shift ] ].SetBinContent( i, value * 0.001 )
            hists[ channel ][ hist_name_err[ shift ] ].Write()
            nBB[ group ] += 1
      else:
        BKG_DOM, value = "", 0
        for process in groups[ group ][ "PROCESS" ]:
          if hists[ channel ][ hist_name_temp.replace( "DAT", process ) ].GetBinContent(i) > value:
            value = hists[ channel ][ hist_name_temp.replace( "DAT", process ) ].GetBinContent(i)
            BKG_DOM = process
        error = hists[ channel ].GetBinError(i)
        hist_name_err = { shift: "{}__CMS_TTTX_{}_UL{}_{}_BIN{}{}".format(
          hists[ channel ][ hist_name_temp.replace( "DAT", process ) ].GetName(),
          channel, args.year, process, i, shift ) for shift in [ "UP", "DN" ] 
        }
        for shift in [ "UP", "DN" ]:
          hists[ channel ][ hist_name_err[ shift ] ] = hists[ channel ][ hist_name_temp.replace( "DAT", process ) ].Clone( hist_name_err[ shift ] )
          if shift == "UP": hists[ channel ][ hist_name_err[ shift ] ].SetBinContent( i, value + error )
          if shift == "DN": hists[ channel ][ hist_name_err[ shift ] ].SetBinContent( i, value - error )
          if value - error < 0: negative_bin_correction( hists[ channel ][ hist_name_err[ shift ] ] )
          if value - error == 0: hists[ channel ][ hist_name_err[ shift ] ].SetBinContent( i, value * 0.001 )
          hists[ channel ][ hist_name_err[ shift ] ].Write()
          nBB[ group ] += 1
      
      return hists, nBB
  
    nBB = { "BKG": 0, "SIG": 0 }
    hist_name_temp = [ hist_name for hist_name in hist_names[ "DAT" ] if channel in hist_name ][0]
    # the TOTALBKG hist does not get written
    hists[ channel ][ "TOTALBKG" ] = hists[ channel ][ hist_name_temp.replace( "DAT", groups[ "BKG" ][ "PROCESS" ][0] ) ].Clone()
    for process in groups[ "BKG" ][ "PROCESS" ][1:]:
      hists[ channel ][ "TOTALBKG" ].Add( hists[ channel ][ hist_name_temp.replace( "DAT", process ) ] )
    for i in range( 1, hists[ channel ][ "TOTALBKG" ].GetNbinsX() + 1 ):
      error_ratio = hists[ channel ][ "TOTALBKG" ].GetBinError(i) / hists[ channel ][ "TOTALBKG" ].GetBinContent(i)
      if error_ratio <= error_threshold[ "BB" ]: 
        print( ">> Excluding bin {} in {} for statistical shape uncertainty ({:.6f})".format( i, channel, error_ratio ) )
        continue
      hists = write_statistical_hists( hists, "BKG", channel, hist_name_temp, i, nBB )
      hists = write_statistical_hists( hists, "SIG", channel, hist_name_temp, i, nBB )
    
    return hists
  
  def symmetrize_HOTclosure( hists, yields, channel, hist_name ): # done
    # make the up and down shifts of the HOTClosure systematic symmetric
    for i in range( 1, hists[ channel ][ hist_name ].GetNbinsX() + 1 ):
      hist_name_up = hist_name.replace( "HOTCLOSURE", "HOTCLOSUREUP" )
      hist_name_dn = hist_name.replace( "HOTCLOSURE", "HOTCLOSUREDN" )
      max_shift = max( 
        abs( hists[ channel ][ hist_name[ :hist_name.find( "_HOTCLOSURE" ) ] ].GetBinContent(i) - hists[ channel ][ hist_name_up ].GetBinContent(i) ),
        abs( hists[ channel ][ hist_name[ :hist_name.find( "_HOTCLOSURE" ) ] ].GetBinContent(i) - hists[ channel ][ hist_name_dn ].GetBinContent(i) )
      )
      hists[ channel ][ hist_name_up ].SetBinContent( i, hists[ channel ][ hist_name[:hist_name.find( "_HOTCLOSURE" )] ].GetBinContent(i) + max_shift )
      hists[ channel ][ hist_name_dn ].SetBinContent( i, hists[ channel ][ hist_name[:hist_name.find( "_HOTCLOSURE" )] ].GetBinContent(i) - max_shift )
    hists[ channel ][ hist_name_up ].Write()
    hists[ channel ][ hist_name_dn ].Write()
    
    hists_HOTClosure = {
      "UP": hists[ channel ][ hist_name_up ].Clone( hist_name.replace( "HOTCLOSURE", "HOTCLOSURE_{}UP".format( args.year ) ) ),
      "DN": hists[ channel ][ hist_name_dn ].Clone( hist_name.replace( "HOTCLOSURE", "HOTCLOSURE_{}DN".format( args.year ) ) )
    }
    for shift in hists_HOTClosure: hists_HOTClosure[ shift ].Write()
    yields[ hists[ channel ][ hist_name_up ].GetName() ] = hists[ channel ][ hist_name_up ].Integral()
    yields[ hists[ channel ][ hist_name_dn ].GetName() ] = hists[ channel ][ hist_name_dn ].Integral()
    
    return hists, yields
    
  def add_muRF_shapes( hists, yields, channel, hist_name, groups ): # done
    for process in groups[ "BKG" ][ "PROCESS" ]:
      if process in groups[ "BKG" ][ "TTBAR_PROCESS" ]: 
        process = "TT"
        hist_muRF = {
          "UP": hists[ channel ][ hist_name ].Clone( hist_name.replace( "MUR", "MURFUP" ) ),
          "DN": hists[ channel ][ hist_name ].Clone( hist_name.replace( "MUR", "MURFDN" ) )
        }
        hist_renorm = {
          "NOMINAL": hists[ channel ][ hist_name ],
          "MURUP": hists[ channel ][ hist_name.replace( "MUR", "MURUP" ) ],
          "MURDN": hists[ channel ][ hist_name.replace( "MUR", "MURDN" ) ],
          "MUFUP": hists[ channel ][ hist_name.replace( "MUR", "MUR" ) ],
          "MUFDN": hists[ channel ][ hist_name.replace( "MUR", "MUFDN" ) ],
          "MURFCORRDUP": hists[ channel ][ hist_name.replace( "MUR", "MURFCORRDUP" ) ],
          "MURFCORRDDN": hists[ channel ][ hist_name.replace( "MUR", "MURFCORRDDN" ) ]
        }
        for i in range( 1, hist_renorm[ "NOMINAL" ].GetNbinsX() + 1 ):
          weight_dict = { key: hist_renorm[ key ].GetBinContent(i) for key in hist_renorm }
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
          for key in hist_renorm:
            if weight_dict[ key ].GetBinContent(i) > weight_limit[ "MAX" ]: 
              weight_limit[ "MAX" ] = weight_dict[ key ].GetBinContent(i)
              weight_error[ "MAX" ] = weight_dict[ key ].GetBinError(i)
              weight_key[ "MAX" ] = key
            if weight_dict[ key ].GetBinContent(i) < weight_limit[ "MIN" ]: 
              weight_limit[ "MIN" ] = weight_dict[ key ].GetBinContent(i)
              weight_error[ "MIN" ] = weight_dict[ key ].GetBinError(i)
              weight_key[ "MIN" ] = key
          
          hist_muRF[ "UP" ].SetBinContent( i, weight_limit[ "MAX" ] )
          hist_muRF[ "UP" ].SetBinError( i, weight_error[ "MAX" ] )
          hist_muRF[ "DN" ].SetBinContent( i, weight_limit[ "MIN" ] )
          hist_muRF[ "DN" ].SetBinError( i, weight_error[ "MIN" ] )
          
        for shift in [ "UP", "DN" ]:
          yields[ hist_name.replace( "MUR", "MURF" + shift ) ] = hist_muRF[ shift ].Integral()
          if ( args.norm_theory_bkg and "SIG" not in hist_name ) or ( args.norm_theory_sig and "SIG" in hist_name ):
            hist_muRF[ shift ].Scale( hist_renorm[ "NOMINAL" ].Integral() / ( hist_muRF[ shift ].Integral() + config.zero ) )
          hist_muRF[ shift ].Write()
          hist_muRF_2 = hist_muRF[ shift ].Clone( hist_name.replace( "MUR{}".format( shift ), "MURF_{}{}".format( process, shift ) ) )
          hist_muRF_2.Write()
          hist_muRF_3 = hist_muRF[ shift ].Clone( hist_name.replace( "MUR{}".format( shift ), "MURF_{}_{}{}".format( process, args.year, shift ) ) )
          hist_muRF_3.Write()
          hist_muRF_4 = hist_muRF[ shift ].Clone( hist_name.replace( "MUR{}".format( shift ), "MURF_{}{}".format( args.year, shift ) ) )
          hist_muRF_4.Write()
          
      return hists
  
  def add_PS_weights( hists, yields, channel, hist_name ): # done
    for process in groups[ "BKG" ][ "PROCESS" ]:
      if process in groups[ "BKG" ][ "TTBAR_PROCESS" ]: process = "TT"
      hist_PSWeight = { shift: hists[ channel ][ hist_name ].Clone( hist_name.replace( "ISR" + shift, "PSWEIGHT" + shift ) ) for shift in [ "UP", "DN" ] }
      hist_dict = { "NOMINAL": hists[ channel ][ hist_name ] }
      for syst in [ "ISR", "FSR" ]:
        for shift in [ "UP", "DN" ]:
          hist_dict[ syst + shift ] = hists[ channel ][ hist_name.replace( "ISR", syst + shift ) ]
      for i in range( 1, hist_dict[ "NOMINAL" ].GetNbinsX() + 1 ):
        weight_dict = { key: hist_renorm[ key ].GetBinContent(i) for key in hist_renorm }
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
        for key in hist_renorm:
          if weight_dict[ key ].GetBinContent(i) > weight_limit[ "MAX" ]: 
            weight_limit[ "MAX" ] = weight_dict[ key ].GetBinContent(i)
            weight_error[ "MAX" ] = weight_dict[ key ].GetBinError(i)
            weight_key[ "MAX" ] = key
          if weight_dict[ key ].GetBinContent(i) < weight_limit[ "MIN" ]: 
            weight_limit[ "MIN" ] = weight_dict[ key ].GetBinContent(i)
            weight_error[ "MIN" ] = weight_dict[ key ].GetBinError(i)
            weight_key[ "MIN" ] = key
        
        #hist_PSWeight[ "UP" ].SetBinContent( i, weight_limit[ "MAX" ] )
        # symmetrize UP w.r.t. DN to fix large UP shifts due to unphysical LHE weights
        hist_PSWeight[ "UP" ].SetBinContent( i, 2 * hists[ channel ][ hist_name[:hist_name.find("_ISR")] ].GetBinContent(i) - hist_dict[ weight_key[ "MIN" ] ].GetBinContent(i) )
        hist_PSWeight[ "UP" ].SetBinError( i, weight_error[ "MAX" ] )
        hist_PSWeight[ "DN" ].SetBinContent( i, weight_limit[ "MIN" ] )
        hist_PSWeight[ "DN" ].SetBinError( i, weight_error[ "MIN" ] )
      
      for shift in [ "UP", "DN" ]:
        yields[ hist_PSWeight[ shift ].GetName() ] = hist_PSWeight[ shift ].Integral()
        if ( args.norm_theory_bkg and "SIG" not in hist_name ) or ( args.norm_theory_sig and "SIG" in hist_name ):
          hist_PSWeight[ shift ].Scale( hist_dict[ "NOMINAL" ].Integral() / ( hist_PSWeight[ shift ].Integral() + config.zero ) )
          hist_PSWeight[ shift ].Write()
          hist_PS_2 = hist_PSWeight[ shift ].Clone( hist_name.replace( "ISR", "{}_{}_{}{}".format( psWeight, process, args.year, shift ) ) )
          hist_PS_2.Write()
        for syst in [ "ISR", "FSR" ]:
          yields[ hist_name.replace( "ISR", syst + shift ) ] = hists[ channel ][ hist_name.replace( "ISR", syst + shift ) ].Integral()
          if ( args.norm_theory_bkg and "SIG" not in hist_name ) or ( args.norm_theory_sig and "SIG" in hist_name ):
            hists[ channel ][ hist_name.replace( "ISR", syst + shift ) ].Scale( hists[ channel ][ hist_name[:hist_name.find("_ISR")] ].Integral() / ( hists[ channel ][ hist_name.replace( "ISR", syst + shift ) ].Integral() + config.zero ) )
          hists[ channel ][ hist_name.replace( "ISR", syst + shift ) ].Write()
          
          hist_PS_3 = hists[ channel ][ hist_name.replace( "ISR", syst + shift ) ].Clone( hist_name.replace( "ISR", "{}_{}{}".format( syst, process, shift ) ) )
          hist_PS_3.Write()
          
          hist_PS_4 = hists[ channel ][ hist_name.replace( "ISR", syst + shift ) ].Clone( hist_name.replace( "ISR", "{}_{}_{}{}".format( syst, process, args.year, shift ) ) )
          hist_PS_4.Write()
          
  def add_PDF_shapes( hists, yields, channel, hist_name ): # done
    for process in groups[ "BKG" ][ "PROCESS" ]:
      hist_PDF = { shift: hists[ channel ][ hist_name ].Clone( hist_name.replace( "PDF0", "PDF" + shift ) ) for shift in [ "UP", "DN" ] }
      for i in range( 1, hist_PDF[ "UP" ].GetNbinsX() + 1 ):
        weight_dict = { i: hists[ channel ][ hist_name.replace( "PDF0", "PDF{}".format( i ) ) ].GetBinContent(i) for i in range( config.pdf_range ) }
        weight_key = {
          "MAX": 0,
          "MIN": 0
        }
        weight_limit = {
          "MAX": weight_dict[ 0 ].GetBinContent(i),
          "MIN": weight_dict[ 0 ].GetBinContent(i)
        }
        weight_error = {
          "MAX": weight_dict[ 0 ].GetBinError(i),
          "MIN": weight_dict[ 0 ].GetBinError(i)
        }
        for key in hist_renorm:
          if weight_dict[ key ].GetBinContent(i) > weight_limit[ "MAX" ]: 
            weight_limit[ "MAX" ] = weight_dict[ key ].GetBinContent(i)
            weight_error[ "MAX" ] = weight_dict[ key ].GetBinError(i)
            weight_key[ "MAX" ] = key
          if weight_dict[ key ].GetBinContent(i) < weight_limit[ "MIN" ]: 
            weight_limit[ "MIN" ] = weight_dict[ key ].GetBinContent(i)
            weight_error[ "MIN" ] = weight_dict[ key ].GetBinError(i)
            weight_key[ "MIN" ] = key

        hist_PDF[ "UP" ].SetBinContent( i, weight_limit[ "MAX" ] )
        hist_PDF[ "UP" ].SetBinError( i, weight_error[ "MAX" ] )
        hist_PDF[ "DN" ].SetBinContent( i, weight_limit[ "MIN" ] )
        hist_PDF[ "DN" ].SetBinError( i, weight_error[ "MIN" ] )
        
        for shift in [ "UP", "DN" ]:
          yields[ hist_PDF[ shift ].GetName() ] = hist_PDF[ shift ].Integral()
          if ( args.norm_theory_bkg and "SIG" not in hist_name ) or ( args.norm_theory_sig and "SIG" in hist_name ):
            hist_PSWeight[ shift ].Scale( hists[ channel ][ hist_name[:hist_name.find( "_PDF" )] ].Integral() / ( hist_PDF[ shift ].Integral() + config.zero ) )
            hist_PSWeight[ shift ].Write()
          hist_PDF_2 = hist_PDF[ shift ].Clone( hist_name.replace( "PDF0", "PDF_{}{}".format( args.year, shift ) ) )
          hist_PDF_2.Write()
          
  def add_smooth_shapes( hists, yields, rFile_out ): # kinda done
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
          hist[ "NEW" + shift ] = hist[ "SMOOTH" + shift ].Clone( hist[ "SMOOTH" + shift ].GetName().replace( shift, "_{}{}".format( args.year, shift ) ) )
          hist[ "NEW" + shift ].Write()
  
  print( ">> Rebinning file: {}".format( file_name ) )
  
  rFile_in = ROOT.TFile( file_name )
  
  hist_names = { "DAT": [ hist_name.GetName() for hist_name in rFile_in.GetListOfKeys() if "DAT" in key.GetName() ] }
  channels = [ hist_name[ hist_name.find( "fb_" ) + 3: hist_name.find( "DAT" ) ] for hist_name in hist_names[ "DAT" ] if "ISE" in hist_name ]
  hist_names[ "ALL" ] = { channel: [ hist_name.GetName() for hist_name in rFile_in.GetListOfKeys() if channel in hist_name.GetName() ] for channel in channels } 
  groups = group_process()
  
  rFile_out = ROOT.TFile( file_name.replace( ".root", "_rebinned_stat{}.root".format( error_threshold[ "STATISTICAL" ].replace( ".", "p" ) ) ), "RECREATE" )
  rebinned_hists, yields, yield_errors = {}, {}, {}
  
  hists_total = {}
  for hist_name in hist_names[ "DAT" ]:
    channel = hist_name[ hist_name.find( "fb_" ) + 3: hist_name.find( "DAT" ) ]
    data_hist[ channel ] = rFile_in.Get( hist_name ).Clone()
    first_process = 0
    try: 
      hists_total[ channel ] = rFile_in.Get( hist_name.replace( "DAT", groups[ "BKG" ][ "PROCESS" ][0] ) ).Clone()
    except:
      hists_total[ channel ] = rFile_in.Get( hist_name.replace( "DAT", groups[ "BKG" ][ "PROCESS" ][1] ) ).Clone()
      first_process = 1
    for process in groups[ "BKG" ][ "PROCESS" ][1:]:
      try:
        hists_total[ channel ].Add( rFile_in.Get( hist_name.replace( "DAT", process ) ) )
      except:
        print( "[WARN] Missing {} for {}, skipping process...".format( process, hist_name ) )
        pass

  for channel in channels:
    print( "  - Processing channel: {}".format( channel ) )
    rebinned_hists[ channel ] = {}
    yields[ channel ] = {}
    yield_errors[ channel ] = {}
    for hist_name in hist_names[ "ALL" ][ channel ]:
      if "_PDF" in hist_name.upper() and "UP_" not in hist_name.upper() and "DN_" not in hist_name.upper(): continue
      for syst in [ "MUR", "MUF", "ISR", "FSR" ]:
        for shift in [ "UP", "DN" ]:
          if syst + shift in hist_name.upper(): continue
      if args.sym_hot_closure_shift and "HOTCLOSURE" in hist_name.upper(): continue
      if "NH0P" in hist_name.upper() and "HOT" in hist_name.upper(): continue
      if "NB0P" in hist_name.upper() and ( "BTAG" in hist_name.upper() or "MISTAG" in hist_name.upper() ): continue
      if "TOPPTDN" in hist_name.upper() and args.sym_top_pt_shift: continue
      
      rebinned_hists[ channel ][ hist_name ] = rebin( rFile_in, xBins, hist_name, channel )
      
    # handle exceptions
    for hist_name in hist_names[ "ALL" ][ channel ]:
      if "TOPPTDN" in hist_name.upper() and args.sym_top_pt_shift:
        rebinned_hists = symmetrize_topPT_shift( rebinned_hists, channel, hist_name )
      if "TRIGEFF" in hist_name.upper():
        rebinned_hists = add_trigger_efficiency( rebinned_hists, channel, hist_name )
      if hist_name.upper().endswith( "UP" ) or hist_name.upper().endswith( "DN" ):
        rebinned_hists = uncorrelate_year( rebinned_hists, channel, hist_name )
        
    # get yields and yield error
    for hist_name in hist_names[ "ALL" ][ channel ]:
      yields, yields_errors = get_yield_stats( yields, yields_errors, hists, channel, hist_name )
      
    if args.stat_shapes:
      rebinned_hists = add_statistical_shapes( hists, channel )
      
    if args.sym_hot_closure_shift:
      for hist_name in hist_names[ "ALL" ][ channel ]:
        if "HOTCLOSURE" in hist_name.upper() and "NHOT0P" not in channel.upper():
          rebinned_hists = symmetrize_HOTclosure( hists, yields, channel, hist_name )
          
    if args.murf:
      for hist_name in hist_names[ "ALL" ][ channel ]:
        add_muRF_shapes( hists, yields, channel, hist_name, groups )
          
    if args.ps_weights:
      for hist_name in hist_names[ channel ]:
        add_PS_weights( hists, yields, channel, hist_name )
          
    if args.pdf:
      for hist_name in hist_names[ channel ]:
        add_PDF_shapes( hists, yields, channel, hist_name )
        
    if args.smoothing:
      for hist_name in hist_names[ channel ]:
        add_smooth_shapes( hists, yields, channel, hist_name )
      
  rFile_in.Close()
  rFile_out.Close()
      
  return rebinned_hists, yields, yield_errors
    
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
    
  categories = get_categories( templateDir )

  file_name = "template_combine_{}_UL{}.root".format( args.variable, args.year ) 
  file_path = os.path.join( templateDir, file_name )
  rebinned_hists, yields, yield_errors = rebinning( filepath, categories, options, params )
  quit()
    
  print_tables( hists )

main()
