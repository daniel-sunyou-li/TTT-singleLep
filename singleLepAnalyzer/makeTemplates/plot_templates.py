from argparse import ArgumentParser
import os, sys, math
sys.path.append( "../" )
import config
import CMS_lumi, tdrstyle

parser = ArgumentParser()
parser.add_argument( "-y", "--year", required = True, help = "16,17,18" )
parser.add_argument( "-r", "--region", required = True, help = "SR,BASELINE" )
parser.add_argument( "-t", "--tag", required = True )
parser.add_argument( "-v", "--variable", required = True )
parser.add_argument( "--verbose", action = "store_true" )
parser.add_argument( "--rebin", action = "store_true" )
args = parser.parse_args()

import ROOT

def hist_tag( *args ):
  histTag = args[0]
  for arg in args[1:]: histTag += "_{}".format( arg )
  return histTag
def modeling_systematics( categories ):
  systematics = {}
  for category in categories:
    if "isL" in category: continue
    if not config.plot_params[ "PLOTTING" ][ "ADD CR SYST" ]:
      for process in groups[ "BKG" ][ "PROCESS" ]:
        systematics[ hist_tag( process, category[2:] ) ] = 0.
    for group in groups[ "BKG" ][ "SUPERGROUP" ]:
      if group == "TTBB": 
        systematics[ hist_tag( group, category[2:] ) ] = math.sqrt( config.systematics[ "XSEC" ][ group ]**2 + config.systematics[ "TTHF" ]**2 + config.systematics[ "HDAMP" ]**2 )
      elif group == "TTNOBB":
        systematics[ hist_tag( group, category[2:] ) ] = math.sqrt( config.systematics[ "XSEC" ][ group ]**2 + config.systematics[ "HDAMP" ]**2 )
      else:
        systematics[ hist_tag( group, category[2:] ) ] = config.systematics[ "XSEC" ][ group ]
  return systematics

def normalization_uncertainty( hist, i, modeling_systematic ):
  correlated_syst = 0
  for syst in [ "LUMI", "TRIG", "ID", "ISO" ]:
    correlated_syst += config.systematics[ syst ][ args.year ]**2 
  correlated_syst = math.sqrt( correlated_syst )
  uncertainty = ( correlated_syst**2 + modeling_systematic**2 ) * hist.GetBinContent(i)**2
  return uncertainty

def normalization_bin_width( histogram ):
  histogram.SetBinContent( 0, 0 )
  histogram.SetBinContent( histogram.GetNbinsX() + 1, 0 )
  histogram.SetBinError( 0, 0 )
  histogram( histogram.GetNbinsX() + 1, 0 )
  
  for i in range( 1, histogram.GetNbinsX() + 1 ):
    width = histogram.GetBinWidth(i)
    content = histogram.GetBinContent(i)
    error = histogram.GetBinError(i)
    
    histogram.SetBinContent( i, content / width )
    histogram.SetBinError( i, error / width )

def load_histograms( templateDir, rebinned, scale_signal_xsec, scale_signal_yield, bin_width_norm ):
  file_name = "template_combine_{}_UL{}"
  if rebinned: file_name += "_rebin_stat{}".format( str( config.params[ "MODIFY BINNING" ][ "STAT THRESHOLD" ] ).replace( ".", "p" ) )
  
  rFile = ROOT.TFile.Open( os.path.join( templateDir, file_name + ".root" ) )
  histograms = { key: {} for key in [ "BKG", "SIG", "DAT", "TOTAL BKG", "TOTAL SIG" ] }
  categories = []
  
  print( ">> Loading histograms from: {}".format( file_name + ".root" ) )
  for hist_name in rFile.GetListOfKeys():
    syst = False
    parts = hist_name.GetName().split( "_" )
    if len( parts ) == len( args.variable.split( "_" ) ) + 4: syst = True
    process = parts[-1]
    category = parts[-2]
    if category not in categories: 
      categories.append( category )
      histograms[ "TOTAL BKG" ][ category ], histograms[ "TOTAL SIG" ][ category ] = 0, 0
      
    if process in groups[ "DAT" ][ "PROCESS" ] + [ "DAT" ]:
      if args.verbose: print( "   + DAT: {}".format( process ) )
      histograms[ "DAT" ][ hist_name ] = rFile.Get( hist_name.GetName() ).Clone()
    elif process in groups[ "BKG" ][ "PROCESS" ] + groups[ "BKG" ][ "SUPERGROUP" ]:
      if args.verbose: print( "   + BKG: {}".format( process ) )
      histograms[ "BKG" ][ hist_name ] = rFile.Get( hist_name.GetName() ).Clone()
      if not syst:
        histograms[ "TOTAL BKG" ][ category ] += histograms[ "BKG" ][ hist_name ].Integral()
    elif process in groups[ "SIG" ][ "PROCESS" ] + [ "SIG" ]:
      if args.verbose: print( "   + SIG: {}".format( process ) )
      histograms[ "SIG" ][ hist_name ] = rFile.Get( hist_name.GetName() ).Clone()
      if scale_signal_yield != 1:
        histograms[ "SIG" ][ hist_name ].Scale( scale_signal_yield )
      if scale_signal_xsec:
        histograms[ "SIG" ][ hist_name ].Scale( weights.weights[ process.split( "_" )[-1] ] )
      if not syst:
        histograms[ "TOTAL SIG" ][ category ] += histograms[ "SIG" ][ hist_name ].Integral()
    else:
      if args.verbose: print( "[WARN] {} does not belong to any of the groups: BKG, SIG, DAT, excluding...".format( process ) )
  
  if args.verbose: print( ">> Computing category total backgrounds for lepton inclusive categories" )
  for category in histograms[ "TOTAL BKG" ]:
    if "isM" in category: continue
    histograms[ "TOTAL BKG" ][ category.replace( "isE", "isL" ) ] = histograms[ "TOTAL" ][ category ] + histograms[ "TOTAL" ][ category.replace( "isE", "isM" ) ]
  
  print( ">> Merging the electron and muon categories" )
  for key in histograms:
    hist_names = [ hist_name for hist_name in list( histograms[ key ].keys() ) if "isE" in hist_name ]
    for hist_name in hist_names:
        name_lepton = hist_name.replace( "isE", "isL" )
        histograms[ key ][ name_lepton ] = histograms[ key ][ hist_name ].Clone( name_lepton )
        histograms[ key ][ name_lepton ].Add( histograms[ key ][ hist_name.replace( "isE", "isM" ) ] )
        if key == "SIG":
          if scale_signal_xsec:
            histograms[ key ][ name_lepton ].Scale( weights.weights[ hist_name.split( "_" )[-1] ] )
          if scale_signal_yield != 1:
            histograms[ key ][ name_lepton ].Scale( scale_signal_yield )
            
  if bin_width_norm:
    print( ">> Normalizing yield and error by bin width" )
    for key in [ "BKG", "SIG", "DAT" ]:
      for hist_name in histograms[ key ]:
        normalization_bin_width( histograms[ key ][ hist_name ] )      
    
  print( ">> Computing the uncertainty for different background iterations: SHAPE ONLY, SHAPE + NORMALIZATION, ALL" )
  error_bkg = {}
  
  systematics = modeling_systematics( categories )
  for category in categories:
    error_bkg[ category ] = {}
    for i in range( 1, histograms[ "BKG" ][ list( histograms[ "BKG" ].keys() )[0] ].GetNbinsX() + 1 ):
      error_bkg[ category ][i] = {
        "STAT": histograms[ "TOTAL BKG" ][ category ].GetBinError(i)**2
        "NORM": 0,
        "UP": 0,
        "DN": 0
      }
      for hist_name in histograms[ "BKG" ]:
        for syst in config.systematics[ "MC" ]: 
          if syst.upper() in hist_name: continue # only nominal categories
        if category not in hist_name: continue
        process = hist_name.split( "_" )[-1]
        try: error_bkg[ category ][i][ "NORM" ] += normalization_uncertainty( histograms[ "BKG" ][ hist_name ], i, systematics[ hist_tag( process, category ) ] )
        except: pass
                
        if config.options[ "GENERAL" ][ "SYSTEMATICS" ]:
          for syst in config.systematics[ "MC" ]:
            if syst.upper() not in hist_name: continue
            try:
              hist_parts = hist_name.split( "_" )
              error_plus =  histograms[ "BKG" ][ hist_tag( hist_parts[0], syst.upper() + "UP", hist_parts[1] ) ].GetBinContent(i) - histograms[ "BKG" ][ hist_name ].GetBinContent(i)
              error_minus = histograms[ "BKG" ][ hist_name ].GetBinContent(i) - histograms[ "BKG" ][ hist_tag( hist_parts[0], syst.upper() + "DN", hist_parts[1], hist_parts[2], hist_parts[3] ].GetBinContent(i)
              if error_plus > 0: error_bkg[ category ][i][ "UP" ] += error_plus**2
              else: error_bkg[ category ][i][ "DN" ] += error_plus**2
              if error_minus > 0: error_bkg[ category ][i][ "DN" ] += error_minus**2
              else: error_bkg[ category ][i][ "UP" ] += error_plus**2
            except: pass
  
  for key in [ "SHAPE ONLY", "SHAPE + NORM", "ALL" ]:
    histograms[ "TOTAL BKG {}".format( key ) ] = {}
    for hist_name in histograms[ "BKG" ]:
      category = hist_name.split( "_" )[-2]
      histograms[ "TOTAL BKG {}".format( key ) ][ category ] =  ROOT.TGraphAsymmErrors( histograms[ "TOTAL BKG" ][ category ].Clone( "TOTAL BKG {}".format( key ) ) )
      total_error = {}
      for i in range( 1, histograms[ "TOTAL BKG {}".format( key ) ][ category ].GetNbinsX() + 1 ):
        total_error[i] = {}
        for shift in [ "UP", "DN" ]: 
          total_error[i][ shift ] = error_bkg[ category ][i][ "STAT" ] }
          if key in [ "SHAPE + NORM", "ALL" ]: total_error[i][ shift ] += error_bkg[ category ][i][ "NORM" ]
          if key in [ "ALL" ]: total_error[i][ shift ] += error_bkg[ category ][i][ shift ]
          total_error[i][ shift ] = math.sqrt( total_error[i][ shift ] )
        histograms[ "TOTAL BKG {}".format( key ) ][ category ].SetPointEYhigh( i - 1, total_error[i][ "UP" ] )
        histograms[ "TOTAL BKG {}".format( key ) ][ category ].SetPointEYlow( i - 1, total_error[i][ "DN" ] )
    
  return histograms, categories
  
def format_upper_hist( pad, hist, hist_bkg, blind, log_scale ):
  hist.GetXaxis().SetLabelSize(0)
  if "NTJETS" in hist.GetName(): hist.GetXaxis().SetNdivisions(5)
  elif "NWJETS" in hist.GetName(): hist.GetXaxis().SetNdivisions(5)
  elif "NBJETS" in hist.GetName(): hist.GetXaxis().SetNdivisions(6,ROOT.kFalse)
  hist.GetXaxis().SetNdivisions(506)
  
  if blind:
    hist.GetXaxis().SetLabelSize(0.045)
    hist.GetXaxis().SetTitleSize(0.055)
    hist.GetYaxis().SetLabelSize(0.045)
    hist.GetYaxis().SetTitleSize(0.055)
    hist.GetYaxis().SetTitleOffset(1.15)
    hist.GetXaxis().SetNdivisions(506)
  else:
    hist.GetYaxis().SetLabelSize(0.07)
    hist.GetYaxis().SetTitleSize(0.08)
    hist.GetYaxis().SetTitleOffset(0.71)
  hist.GetYaxis().CenterTitle()
  hist.SetMinimum(0.0000101)
  if log_scale:
    pad.SetLogy()
    hist.SetMaximum( 2e2 * hist_bkg.GetMaximum() )
  else:
    hist.SetMaximum( 1.3 * hist_bkg.GetMaximum() )

def format_lower_hist( pad, hist, hist_bkg, blind, log_scale, real_pull ): 
  hist.GetXaxis().SetLabelSize(0.12)
  hist.GetXaxis().SetTitleSize(0.15)
  hist.GetXaxis().SetTitleOffset(0.95)
  hist.GetXaxis().SetNdivisions(506)
  
  if "NTJETS" in hist.GetName(): hist.GetXaxis().SetNdivisions(5)
  elif "NWJETS" in hist.GetName(): hist.GetXaxis().SetNdivisions(5)
  elif "NBJETS" in hist.GetName(): hist.GetXaxis().SetNdivisions(6,ROOT.kFalse)
  hist.GetXaxis().SetNdivisions(506)
  
  hist.GetYaxis().SetLabelSize(0.12)
  hist.GetYaxis().SetTitleSize(0.14)
  hist.GetYaxis().SetTitleOffset(0.37)
  hist.GetYaxis().SetTitle( "Data/Bkg" )
  hist.GetYaxis().SetNdivisions(506)
  
  if real_pull: 
    hist.GetYaxis().SetRangeUser( min( -2.99, 0.8 * hist.GetBinCOntent( hist.GetMaximumBin() ) ), max( 2.99, 1.2 * hist.GetBinContent( hist.GetMaximumBin() ) ) )
  else:
    hist.GetYaxis().SetRangeUser( 0.01, 1.99 )
  hist.GetYaxis().CenterTitle()

def stat_test( histograms, categories ):
  stats = {}
  table = []
  for category in categories:
    row = [ category ]
    hist_test = {
      "BKG": histograms[ "TOTAL BKG" ][ category ].Clone()
      "DAT": histograms[ "DAT" ][ category ].Clone()
    }
    for i in range( 1, hist_test[ "BKG" ].GetNbinsX() + 1 ):
      hist_test[ "BKG" ].SetBinError( i, ( histograms[ "TOTAL BKG ALL" ][ category ].GetErrorYlow( i - 1 ) + histograms[ "TOTAL BKG ALL" ][ category ].GetErrorYhigh( i - 1 ) ) / 2 )
    
    KS_prob = hist_test[ "BKG" ].KolmogorovTest( hist_test[ "DAT" ] )
    KS_prob_X = hist_test[ "BKG" ].KolmogorovTest( hist_test[ "DAT" ], "X" )
    Chi2_prob = hist_test[ "DAT" ].Chi2Test( hist_test[ "BKG" ], "UW" )
    Chi2 = hist_test[ "DAT" ].Chi2Test( hist_test[ "BKG" ], "UW CHI2" )
    
    if hist_test[ "DAT" ].Chi2Test( hist_test[ "BKG" ], "UW CHI2/NDF" ) != 0: NDOF = Chi2 / hist_test[ "DAT" ].Chi2Test( hist_test[ "BKG" ], "UW CHI2/NDF" )
    else: NDOF = 0
    
    stats = {
      "BKG": hist_test[ "BKG" ].Integral(),
      "DAT": hist_test[ "DAT" ].Integral(),
      "RATIO": hist_test[ "DAT" ].Integral() / hist_test[ "BKG" ].Integral(),
      "KS (p)": KS_prob,
      "KS (p) X": KS_prob_X,
      "CHI2 (p)": Chi2_prob,
      "CHI2": Chi2,
      "CHI2 NDOF": NDOF
    }
    
    for stat in stats: row.append( stats[ stat ] )
    
    print( ">> Statistics for {}:".format( category ) )
    print( "   + BKG: {}, DAT: {}, Ratio = {}".format( stats[ category ][ "BKG" ], stats[ category ][ "DAT" ], stats[ category ][ "RATIO" ] ) )
    print( "   + KS (p): {}, KS (p) X: {}".format( KS_prob, KS_prob_X ) )
    print( "   + Chi2 (p): {}, Chi2: {}, NDOF: {}".format( Chi2, Chi2, NDOF ) )
    
    table.append( row )
    
  return table

def plot_distribution( templateDir, lep, hists, categories, systematics, lumiStr, plot_yields, blind, norm_bin_width, compare_shapes, rebinned, scale_signal_yield, real_pull, one_band ):
  for category in categories:
    if "is" + lep not in category: continue
    if hists[ "BKG" ][ hist_tag( args.variable, lumiStr, category, "QCD" ) ].Integral() / hists[ "TOTAL BKG" ][ category ].Integral() < 
    
    for process in list( groups[ "BKG" ][ "SUPERGROUP" ].keys() ) + list( groups[ "BKG" ][ "PROCESS" ].keys() ):
      try:
        hists[ "BKG" ][ hist_tag( variable, lumiStr, category, process ) ].SetLineColor( plot_params.params[ "BKG COLORS" ][ process ] )
        hists[ "BKG" ][ hist_tag( variable, lumiStr, category, process ) ].SetFillColor( plot_params.params[ "BKG COLORS" ][ process ] )
        hists[ "BKG" ][ hist_tag( variable, lumiStr, category, process ) ].SetLineWidth(2)
      except: pass
    if plot_yields:
      hists[ "TOTAL BKG" ][ category ].SetMarkerSize(4)
      hists[ "TOTAL BKG" ][ category ].SetMarkerColor( plot_params.params[ "BKG COLORS" ][ process ] )
    
    print( ">> Plotting {} error band for background.".format( plot_params.params[ "ERROR BAND" ] ) )
    hists[ "TOTAL BKG {}".format( plot_params.params[ "ERROR BAND" ] ) ][ category ].SetFillStyle(3004)
    hists[ "TOTAL BKG {}".format( plot_params.params[ "ERROR BAND" ] ) ][ category ].SetFillColor( plot_params.params[ "BKG COLORS" ][ "ERROR" ] )
    hists[ "TOTAL BKG {}".format( plot_params.params[ "ERROR BAND" ] ) ][ category ].SetLineColor( plot_params.params[ "BKG COLORS" ][ "ERROR" ] )
    
    hists[ "TOTAL SIG" ][ category ].SetLineColor( plot_params.params[ "SIG COLOR" ] )
    hists[ "TOTAL SIG" ][ category ].SetLineStyle(7)
    hists[ "TOTAL SIG" ][ category ].SetFillStyle(0)
    hists[ "TOTAL SIG" ][ category ].SetLineWidth(3)
    
    hists[ "DAT" ][ category ].SetMarkerColor( plot_params.params[ "DAT COLOR" ] )
    hists[ "DAT" ][ category ].SetMarkerSize(1.2)
    hists[ "DAT" ][ category ].SetLineWidth(2)
    hists[ "DAT" ][ category ].SetMarkerColor( plot_params.params[ "DAT COLOR" ] )
    if not plot_yields:
      hists[ "DAT" ][ category ].SetMarkerStyle(20)
    else:
      hists[ "DAT" ][ category ].SetMarkerSize(4)
    
    if not norm_bin_width:
      hists[ "DAT" ][ category ].SetMaximum( 1.2 * max( hists[ "DAT" ][ category ].GetMaximum(), hists[ "TOTAL BKG" ][ category ].GetMaximum() ) )
      hists[ "DAT" ][ category ].GetYaxis().SetTitle( "Events / bin" )
    else:
      hists[ "DAT" ][ category ].GetYaxis().SetTitle( "< Events / GeV >" )
    
    hists[ "DAT" ][ category ].SetTitle( "" )
    format_upper_hist( hists[ "DAT" ][ category ], hists[ "DAT" ][ category ] )
    
    # prepare the ROOT canvas    
    canvas = ROOT.TCanvas( "c1", "c1", 50, 50, W, H )
    canvas.SetFillColor(0)
    canvas.SetBorderOrder(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    
    y_divisions = 0.0 if blind else plot_params.params[ "Y DIVISION" ]
    
    pad = { 
      "UPPER": ROOT.TPad( "UPPER", "", 0, y_divisions, 1, 1 ),
      "LOWER": ROOT.TPad( "LOWER", "", 0, 0, 1, y_divisions )
    }
    
    for key in pad:
      if blind and pad == "LOWER": continue
      pad[ key ].SetLeftMargin( plot_params[ "CANVAS" ][ "L" ] / plot_params[ "CANVAS" ][ "W" ] )
      pad[ key ].SetRightMargin( plot_params[ "CANVAS" ][ "R" ] / plot_params[ "CANVAS" ][ "W" ] )
      pad[ key ].SetFillColor(0)
      pad[ key ].SetBorderMode(0)
      pad[ key ].SetFrameFillStyle(0)
      pad[ key ].SetFrameBorderMode(0)
      if pad == "UPPER": 
        pad[ key ].SetTopMargin( plot_params[ "CANVAS" ][ "T" ] / plot_params[ "CANVAS" ][ "H" ] )
        if blind:
          pad[ key ].SetBottomMargin( plot_params[ "CANVAS" ][ "B" ] / plot_params[ "CANVAS" ][ "H" ] )
        else:
          pad[ key ].SetBottomMargin( 0.01 )
      elif pad == "LOWER":
        pad[ key ].SetTopMargin( 0.01 )
        pad[ key ].SetBottomMargin( plot_params[ "CANVAS" ][ "B" ] / plot_params[ "CANVAS" ][ "H" ] )
        pad[ key ].SetGridy()
      pad[ key ].Draw()
    
    pad[ "UPPER" ].cd()
    
    if compare_shapes:
      hists[ "TOTAL SIG" ][ category ].Scale( hists[ "TOTAL BKG" ][ category ].Integral() / hists[ "TOTAL SIG" ][ category ].Integral() )
    
    if not blind:
      if rebinned: hists[ "DAT" ][ category ].Draw( "esamex1" )
      else: hists[ "DAT" ][ category ].Draw( "esamex0" )
    else:
      if norm_bin_width: 
        hists[ "TOTAL SIG" ][ category ].GetYaxis().SetTitle( "< Events / GeV >" )
        normalization_bin_width( hists[ "TOTAL BKG" ][ category ] )
      else:
        hists[ "TOTAL SIG" ][ category ].GetYaxis().SetTitle( "Events / bin" )
      format_upper_hist( hists[ "TOTAL SIG" ][ category ], hists[ "TOTAL BKG" ][ category ] )
      hists[ "TOTAL SIG" ][ category ].Draw( "HIST" )
    
    bkg_stack = ROOT.THStack( "bkg_stack", "" )
    for process in list( groups[ "BKG" ][ "SUPERGROUP" ].keys() ):
      try:
        bkg_stack.Add( hists[ "BKG" ][ hist_tag( variable, lumiStr, category, process ) ] )
      except: pass
    bkg_stack.Draw( "SAME HIST" )
    
    if plot_yields:
      ROOT.gStyle.SetPaintTextFormat( "1.0f" )
      hists[ "TOTAL BKG" ][ category ].Draw( "SAME TEXT90" )
    hists[ "TOTAL SIG" ][ category ].Draw( "SAME HIST" )
    
    if not blind:
      if rebinned: hists[ "DAT" ][ category ].Draw( "esamex1" )
      else: hists[ "DAT" ][ category ].Draw( "esamex0" )
      if plot_yields: hists[ "DAT" ][ category ].Draw( "SAME TEXT00" )
    
    pad[ "UPPER" ].RedrawAxis()
    hists[ "TOTAL BKG {}".format( plot_params.params[ "ERROR BAND" ] ) ][ category ].Draw( "SAME E2" )
    
    # latex 
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize( plot_params.params[ "GENERAL" ][ "LATEX SIZE" ] )
    latex.SetTextAlign(21)
    
    splits = category.split( "n" )
    cat_text = {
      "LEP": splits[0][-1] + "+jets",
      "NHOT": "#geq{} resolved t".format( splits[1][-2:] ) if "p" in splits[1] else "{} resolved t".format( splits[1][-1] ),
      "NT": "#geq{} t".format( splits[2][-2:] ) if "p" in splits[2] else "{} t".format( splits[2][-1] ),
      "NW": "#geq{} W".format( splits[3][-2:] ) if "p" in splits[3] else "{} W".format( splits[3][-1] ),
      "NB": "#geq{} b".format( splits[4][-2:] ) if "p" in splits[4] else "{} b".format( splits[4][-1] ),
      "NJ": "#geq{} j".format( splits[5][-2:] ) if "p" in splits[5] else "{} j".format( splits[5][-1] )
    }
    latex.DrawLatex( 
      plot_params.params[ "CANVAS" ][ "TAG X" ], plot_params.params[ "CANVAS" ][ "TAG Y" ],
      cat_text[ "LEP" ]
    )
    latex.DrawLatex(
      plot_params.params[ "CANVAS" ][ "TAG X" ], plot_params.params[ "CANVAS" ][ "TAG Y" ],
      cat_text[ "NJ" ] + cat_text[ "NB" ] + cat_text[ "NW" ] + cat_text[ "NT" ]
    )
    latex.DrawLatex(
      plot_params.params[ "CANVAS" ][ "TAG X" ], plot_params.params[ "CANVAS" ][ "TAG Y" ],
      cat_text[ "NHOT" ]
    )
    
    if blind:
      legend = ROOT.TLegend( 0.45, 0.64, 0.95, 0.89 )
    else:
      legend = ROOT.TLegend( 0.45, 0.52, 0.95, 0.87 )
    legend.SetShadowColor(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetLineColor(0)
    legend.SetLineStyle(0)
    legend.SetBorderSize(0)
    legend.SetNColumns(2)
    legend.SetTextFont(62)

    if not blind:
      legend.AddEntry( hists[ "DAT" ][ hist_tag( variable, lumiStr, category, "DAT" ) ], "DATA", "ep" )
    
    for group in list( groups[ "BKG" ][ "SUPERGROUP" ].keys() ):
      legend.AddEntry( hists[ "BKG" ][ hist_tag( variable, lumiStr, category, group ) ], group, "f" ) 
    legend.AddEntry( hists[ "TOTAL BKG {}".format( plot_params.params[ "ERROR BAND" ] ) ][ category ], "BKG UNC.", "f" )
      
    if scale_signal_yield != 1:
      legend.AddEntry( hists[ "TOTAL SIG" ][ category ], "SIG x{}".format( scale_signal_yield ), "l" )
    else:
      legend.AddEntry( hists[ "TOTAL SIG" ][ category ], "SIG", "l" )
    legend.Draw( "same" )
    
    CMS_lumi.CMS_lumi( pad[ "UPPER" ], plot_params.params[ "CANVAS" ][ "I PERIOD" ], plot_params.params[ "CANVAS" ][ "I POSITION" ] )
    
    pad[ "UPPER" ].Update()
    pad[ "UPPER" ].RedrawAxis()
    frame = pad[ "UPPER" ].GetFrame()
    pad[ "UPPER" ].Draw()
    
    if not blind:    
      pad[ "LOWER" ].cd()
      pull = hists[ "DAT" ][ category ].Clone( "pull" )
      if not real_pull:
        # draw the ratio plot
        pull.Divide( hists[ "DAT" ][ category ], hists[ "TOTAL BKG" ][ category ] )
        for i in range( 1, hists[ "DAT" ][ category ].GetNbinsX() + 1 ):
          i_label = i - 1
          if variable.upper() in [ "NJETS" ]:
            if i_label % 2 == 0: pull.GetXaxis().SetBinLabel( i, str( i_label ) )
            else: pull.GetXaxis().SetBinLabel( i, "" )
          if variable.upper() in [ "NBJETS", "NWJETS", "NTJETS", "NHOTJETS" ]:
            pull.GetXaxis().SetBinLabel( i, str( i_label ) )
          if hists[ "TOTAL BKG" ].GetBinContent(i) != 0:
            pull.SetBinError( i, hists[ "DAT" ][ category ].GetBinError(i) / hists[ "TOTAL BKG" ].GetBinContent(i) )
        
        pull.SetMaximum(3)
        pull.SetMinimum(0)
        pull.SetFillColor(1)
        pull.SetLineColor(1)
        format_lower_hist( pull, variable )
        print( ">> Plotting un-blinded pull plot" )
        pull.Draw( "E0" )
        
        # draw the total uncertainty band of the ratio plot
        bkg_to_bkg = pull.Clone( "BKG TO BKG" )
        bkg_to_bkg.Divide( hists[ "TOTAL BKG" ][ category ], hists[ "TOTAL" ][ category ] )
        
        pull_error = { error: ROOT.TGraphAsymmErrors( bkg_to_bkg.Clone( "FULL ERROR {}".format( error ) ) ) for error in [ "SHAPE ONLY", "SHAPE + NORM", "ALL" ] }
        
        for error in pull_error:
          for i in range( 0, hists[ "DAT" ].GetNbinsX() + 2 ):
            if hists[ "TOTAL BKG" ].GetBinContent(i) != 0:
              pull_error.SetPointEYhigh( 
                i - 1, 
                hists[ "TOTAL BKG {}".format( error ) ][ category ].GetErrorYhigh(i-1) / hists[ "TOTAL BKG" ][ category ].GetBinContent(i) 
              )
              pull_error.SetPointEYlow(
                i - 1, 
                hists[ "TOTAL BKG {}".format( error ) ][ category ].GetErrorYlow(i-1) / hists[ "TOTAL BKG" ][ category ].GetBinContent(i) 
              )
          pull_error[ error ].SetFillStyle(3013)
          pull_error[ error ].SetFillColor(1)
          pull_error[ error ].SetLineColor(1)
          pull_error[ error ].SetMarkerSize(0)
          ROOT.gStyle.SetHatchesLineWidth(1)
          pull_error[ error ].Draw( "SAME E2" )
        
        pull_legend = ROOT.TLegend( 0.14, 0.87, 0.85, 0.96 )
        ROOT.SetOwnership( pull_legend, 0 )
        pull_legend.SetShadowColor(0)
        pull_legend.SetNColumns(3)
        pull_legend.SetFillColor(0)
        pull_legend.SetFillStyle(0)
        pull_legend.SetLineColor(0)
        pull_legend.SetLineStyle(0)
        pull_legend.SetBorderSize(0)
        pull_legend.SetTExtFont(42)
        
        if not one_band:
          for error in pull_errors:
            pull_legend.AddEntry( pull_error[ error ], error, "f" )
        else:
          if plot_params.options[ "ALL SYSTEMATICS" ]:
            pull_legend.AddEntry( pull_error[ "ALL" ], "BKG ERR (STAT #oplus SYST)", "f" )
          else:
            pull_legend.AddEntry( pull_error[ "SHAPE ONLY" ], "BKG ERR ({})".format( "SHAPE ONLY" ), "f" )
            
        pull_legend.Draw( "SAME" )
        pull.Draw( "SAME" )
        pad[ "LOWER" ].RedrawAxis()
        
      if real_pull:
        pad[ "LOWER" ].cd()
        
        pull = hists[ "DAT" ][ category ].Clone( "PULL" )
        for i in ranger( 1, hists[ "DAT" ][ category ].GetNbinsX() + 1 ):
          label_i = i - 1
          if "NJETS" in variable:
            if label_i % 2 == 0: pull.GetXaxis().SetBinLabel( i, str( label_i ) )
            else: pull.GetXaxis().SetBinLabel( i, "" ) 
          if "NBJETS" in variable or "NRESOLVEDTOPS" in variable or "NWJETS" in variable or "NTJETS" in variable:
            pull.GetXaxis().SetBinLabel( i, str( label_i ) )
          if hists[ "DAT" ][ category ].GetBinContent( i ) != 0:
            error_MC = 0.5 * ( hists[ "TOTAL BKG ALL" ][ category ].GetErrorYhigh( i - 1 ) + hists[ "TOTAL BKG ALL" ][ category ].GetErrorYlow( i - 1 ) )
            pull.SetBinContent( i, ( hists[ "DAT" ][ category ].GetBinContent(i) - hists[ "TOTAL BKG" ].GetBinContent(i) ) / math.sqrt( error_MC**2 + hists[ "DAT" ][ category ].GetBinError(i)**2 ) )
          else:
            pull.SetBinContent( i, 0. )
        pull.SetMaximum(3)
        pull.SetMinimum(-3)
        pull.SetFillColor( plot_params[ "SIG PULL COLOR" ] )
        pull.SetLineColor( plot_params[ "SIG PULL COLOR" ] )
        format_lower_hist( pull, variable )
        pull.GetYaxis().SetTitle( "#frac{(OBS-BKG)}{#sigma}" )
        pull.Draw( "HIST" )
    
    save_name = hist_tag( variable, category )
    if rebinned: save_name += "_rebin_stat{}".format( str( config.params[ "MODIFY BINNING" ][ "STAT THRESHOLD" ] ).replace( ".", "p" ) )
    if real_pull: save_name += "_pull"
    if blind: save_name += "_blind"
    if one_band: save_name += "_oneband"
    if plot_params.options[ "YLOG" ]: save_name += "_logy"
    save_name += ".png"
    canvas.SaveAs( os.path.join( templateDir, "plots/", save_name ) )

def main():
  tdrstyle.setTDRStyle()

  template_prefix = config.region_prefix[ args.region ] 
  templateDir = os.path.join( os.getcwd(), "{}_UL{}_{}".format( template_prefix, args.year, args.tag ) )
  hists, categories = load_histograms( templateDir )
  table = stat_test( hists, categories )
  
  for lep in [ "E", "M", "L" ]:
    if lep in plot_params.params[ "INCLUDE LEP" ]:
      plot_distribution( 
        templateDir = templateDir, 
        lep = lep, 
        hists = hists, 
        categories = categories, 
        systematics = plot_params.options[ "SYSTEMATICS" ], 
        lumiStr = config.lumiStr[ args.year ], 
        plot_yields = plot_params.options[ "YIELDS" ], 
        blind = plot_params.options[ "BLIND" ], 
        norm_bin_width = plot_params.options[ "NORM BIN WIDTH" ], 
        compare_shapes = plot_params.options[ "COMPARE SHAPES" ], 
        rebinned = args.rebin, 
        scale_signal_yield = plot_params.options[ "SCALE SIGNAL YIELD" ], 
        real_pull = plot_params.options[ "REAL PULL" ], 
        one_band = plot_params.options[ "ONE BAND" ]
      )
  