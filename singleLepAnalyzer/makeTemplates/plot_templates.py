from argparse import ArgumentParser
import os, sys, math
sys.path.append( "../" )
import config
import tdrstyle
import config_plot
from utils import hist_tag, hist_parse

parser = ArgumentParser()
parser.add_argument( "-y", "--year", required = True, help = "16APV,16,17,18" )
parser.add_argument( "-r", "--region", required = True, help = "SR,BASELINE" )
parser.add_argument( "-t", "--tag", required = True )
parser.add_argument( "-v", "--variable", required = True )
parser.add_argument( "--verbose", action = "store_true" )
parser.add_argument( "--rebin", action = "store_true" )
parser.add_argument( "--templates", action = "store_true" )
parser.add_argument( "--ratios", action = "store_true" )
parser.add_argument( "--systematics", action = "store_true" )
args = parser.parse_args()

if args.year == "16APV": 
  import samplesUL16APV as samples
elif args.year == "16":
  import samplesUL16 as samples
elif args.year == "17":
  import samplesUL17 as samples
elif args.year == "18":
  import samplesUL18 as samples
else: quit( "[ERR] Invalid -y (--year) argument. Use: 16APV, 16, 17, or 18" )

import ROOT

def modeling_systematics( categories, groups ):
  systematics = {}
  for category in categories:
    if not config_plot.options[ "CR SYST" ]:
      for process in groups[ "BKG" ][ "PROCESS" ]:
        systematics[ hist_tag( process, category ) ] = 0.
    for group in groups[ "BKG" ][ "SUPERGROUP" ]:
      if group == "TTBB": 
        systematics[ hist_tag( group, category ) ] = math.sqrt( ( config.systematics[ "XSEC" ][ "TTBAR" ][1] - 1.0 )**2 + ( config.systematics[ "TTHF" ] - 1.0 )**2 + ( config.systematics[ "HDAMP" ] - 1.0 )**2 )
      elif group == "TTNOBB":
        systematics[ hist_tag( group, category ) ] = math.sqrt( ( config.systematics[ "XSEC" ][ "TTBAR" ][1] - 1.0 )**2 + ( config.systematics[ "HDAMP" ] - 1.0 )**2 )
      elif group in config.systematics[ "XSEC" ].keys():
        systematics[ hist_tag( group, category ) ] = config.systematics[ "XSEC" ][ group ] - 1.0
  return systematics

def normalization_uncertainty( hist, i, modeling_systematic ):
  parse = hist_parse( hist.GetName(), samples )
  correlated_syst = 0
  correlated_syst += ( config.systematics[ "LUMI" ][ args.year ] - 1.0 )**2
  if "isE" in parse[ "CATEGORY" ]:
    correlated_syst += ( config.systematics[ "TRIG" ][ "E" ] - 1.0 )**2
    correlated_syst += ( config.systematics[ "ID" ][ "E" ] - 1.0 )**2
    correlated_syst += ( config.systematics[ "ISO" ][ "E" ] - 1.0 )**2
  elif "isM" in parse[ "CATEGORY" ]:
    correlated_syst += ( config.systematics[ "TRIG" ][ "M" ] - 1.0 )**2
    correlated_syst += ( config.systematics[ "ID" ][ "M" ] - 1.0 )**2
    correlated_syst += ( config.systematics[ "ISO" ][ "M" ] - 1.0 )**2
  elif "isL" in parse[ "CATEGORY" ]:
    correlated_syst += ( config.systematics[ "TRIG" ][ "M" ] - 1.0 )**2 + ( config.systematics[ "TRIG" ][ "E" ] - 1.0 )**2
    correlated_syst += ( config.systematics[ "ID" ][ "M" ] - 1.0 )**2 + ( config.systematics[ "ID" ][ "E" ] - 1.0 )**2
    correlated_syst += ( config.systematics[ "ISO" ][ "M" ] - 1.0)**2 + ( config.systematics[ "ISO" ][ "E" ] - 1.0 )**2
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

def cms_lumi( pad, postfix, blind ):
  print( "  >> Formatting CMS header text" )
  header = { 
    "TEXT": "CMS",
    "TEXT FONT": 61,
    "TEXT SIZE": 1.5,
    "TEXT OFFSET": 0.2,
    "POSTFIX": postfix,
    "POSTFIX FONT": 52,
    "POSTFIX SIZE": 0.9,
    "LUMI TEXT": str( config.lumi[ args.year ] / 1000. ) + "fb^{-1} (13 TeV)",
    "LUMI TEXT FONT": 42,
    "LUMI TEXT SIZE": 0.9,
    "LUMI TEXT OFFSET": 0.2,
  }
  pad_dim = {
    "H": pad.GetWh(),
    "W": pad.GetWw(),
    "L": pad.GetLeftMargin(),
    "T": pad.GetTopMargin(),
    "R": pad.GetRightMargin(),
    "B": pad.GetBottomMargin(),
    "E": 0.025,
  }
  
  pad.SetTopMargin( 0.08 )

  pad.cd()
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextAngle(0)
  latex.SetTextColor(ROOT.kBlack)
  latex.SetTextAlign(31)
  latex.SetTextSize( pad_dim["T"] * header[ "LUMI TEXT SIZE" ] )
  latex.DrawLatex( 1 - pad_dim["R"], 1 - ( 1. + header[ "LUMI TEXT OFFSET" ] ) * pad_dim[ "T" ], header[ "LUMI TEXT" ] )
  
  pad.cd()
  latex.SetTextFont( header[ "TEXT FONT" ] )
  latex.SetTextSize( pad_dim["T"] * header[ "TEXT SIZE" ] )
  latex.SetTextAlign(11)
  latex.DrawLatex( pad_dim["L"], 1 - ( 1. + header[ "TEXT OFFSET" ] ) * pad_dim[ "T" ], header[ "TEXT" ] )
  latex.SetTextFont( header[ "POSTFIX FONT" ] )
  latex.SetTextSize( pad_dim[ "T" ] * header[ "POSTFIX SIZE" ] )
  latex.SetTextAlign(11)
  if blind:
    latex.DrawLatex( pad_dim["L"] + 0.13, 1 - ( 1. + header[ "TEXT OFFSET" ] ) * pad_dim[ "T" ], header[ "POSTFIX" ] )
  else:
    latex.DrawLatex( pad_dim["L"] + 0.10, 1 - ( 1. + header[ "TEXT OFFSET" ] ) * pad_dim[ "T" ], header[ "POSTFIX" ] )
  
  pad.Update()

def load_histograms( groups, templateDir, rebinned, scale_signal_xsec, scale_signal_yield, norm_bin_width, smooth ):
  file_name = "template_combine_{}_UL{}".format( args.variable, args.year )
  if rebinned: file_name += "_rebinned_stat{}".format( str( config.params[ "MODIFY BINNING" ][ "STAT THRESHOLD" ] ).replace( ".", "p" ) ) 
  rFile = ROOT.TFile.Open( os.path.join( templateDir, file_name + ".root" ) )
  histograms = { key: {} for key in [ "BKG", "SIG", "DAT", "TOTAL BKG", "TOTAL SIG", "TOTAL DAT" ] }
  
  print( "[START] Loading histograms from: {}".format( file_name + ".root" ) )
  count = 0
  syst_list = []
  hist_names = [ key.GetName() for key in rFile.GetListOfKeys() ]
  categories = []
  for hist_name in sorted( hist_names ):
    if args.year in hist_name or "isL" in hist_name: continue # skip the uncorrelated histogram and lepton categories
    if hist_name.endswith( "Down" ) or hist_name.endswith( "Up" ) or hist_name.endswith( "NOMINAL" ): continue # skip combine hists
    if config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() in hist_name and not smooth: continue
    parse = hist_parse( hist_name, samples )
    syst = parse[ "IS SYST" ]
    syst_name = parse[ "SYST" ]
    if syst and config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() not in hist_name and smooth: continue
    if "ELTRIG" in syst_name or "MUTRIG" in syst_name or "BIN" in syst_name: continue
    if syst_name in config_plot.params[ "EXCLUDE SYST" ]: continue
    if syst_name in config.systematics[ "MC" ]:
      if not config.systematics[ "MC" ][ syst_name ]: continue
    if syst and syst_name not in syst_list: syst_list.append( syst_name )
    process = parse[ "PROCESS" ]
    category = parse[ "CATEGORY" ]
    if category not in categories:
      categories.append( category )

    if parse[ "GROUP" ] == "DAT":
      if args.verbose: print( "  + DAT: {}".format( hist_name ) )
      histograms[ "DAT" ][ hist_name ] = rFile.Get( hist_name ).Clone( hist_name )
      try:
        histograms[ "TOTAL DAT" ][ category ].Add( histograms[ "DAT" ][ hist_name ] )
      except:
        histograms[ "TOTAL DAT" ][ category ] = histograms[ "DAT" ][ hist_name ].Clone()
    elif parse[ "GROUP" ] == "BKG":
      if args.verbose and not parse[ "IS SYST" ]: print( "  + BKG: {}".format( hist_name) )
      histograms[ "BKG" ][ hist_name ] = rFile.Get( hist_name ).Clone( hist_name )  
      if not parse[ "IS SYST" ]:
        try:
          histograms[ "TOTAL BKG" ][ category ].Add( histograms[ "BKG" ][ hist_name ] )
        except:
          histograms[ "TOTAL BKG" ][ category ] = histograms[ "BKG" ][ hist_name ].Clone()
    elif parse[ "GROUP" ] == "SIG":
      if args.verbose and not parse[ "IS SYST" ]: print( "  + SIG: {}".format( hist_name ) )
      scale = 1.
      if scale_signal_yield: scale *= config_plot.params[ "SCALE SIGNAL YIELD" ]
      if scale_signal_xsec: scale *= weights.weights[ process ]
      histograms[ "SIG" ][ hist_name ] = rFile.Get( hist_name ).Clone( hist_name )
      histograms[ "SIG" ][ hist_name ].Scale( scale )
      if not parse[ "IS SYST" ]:
        try:
          histograms[ "TOTAL SIG" ][ category ].Add( histograms[ "SIG" ][ hist_name ] )
        except:
          histograms[ "TOTAL SIG" ][ category ] = histograms[ "SIG" ][ hist_name ].Clone()
    else:
      if args.verbose: print( "  [WARN] {} does not belong to any of the groups: BKG, SIG, DAT, excluding...".format( hist_name ) )
    count += 1
  print( "[DONE] Found {} histograms".format( count ) )

  print( "[START] Creating lepton categories" )
  count = 0
  for hist_key in histograms:
    print( "   o {}".format( hist_key ) )
    hist_names = [ hist_name for hist_name in histograms[ hist_key ].keys() if "isE" in hist_name ]
    for hist_name in hist_names:
      name_lepton = hist_name.replace( "isE", "isL" )
      parse = hist_parse( name_lepton, samples )
      if parse[ "CATEGORY" ] not in categories: categories.append( parse[ "CATEGORY" ] )
      histograms[ hist_key ][ name_lepton ] = histograms[ hist_key ][ hist_name ].Clone( name_lepton )
      histograms[ hist_key ][ name_lepton ].Add( histograms[ hist_key ][ hist_name.replace( "isE", "isM" ) ] )
      if not parse[ "IS SYST" ]:  print( "     + {}: {}".format( name_lepton, histograms[ hist_key ][ name_lepton ].Integral() ) ) 
      count += 1
  print( "[DONE] Created {} lepton categories".format( count ) )

  if norm_bin_width:
    print( "[START] Normalizing yield and error by bin width" )
    for key in [ "BKG", "SIG", "DAT" ]:
      print( "   + {}".format( key ) )
      for hist_name in histograms[ key ]:
        normalization_bin_width( histograms[ key ][ hist_name ] )      
    print( "[DONE]" )

  print( "[START] Computing the uncertainty for different background iterations: SHAPE ONLY, SHAPE + NORMALIZATION, ALL" )
  error_bkg = {}
  
  systematics = modeling_systematics( categories, groups )
  print( "  [START] Calculating statistical uncertainty" )
  for category in categories:
    print( "     + {}".format( category ) )
    error_bkg[ category ] = {}
    for i in range( 1, histograms[ "TOTAL BKG" ][ category ].GetNbinsX() + 1 ):
      error_bkg[ category ][i] = {
        "STAT": histograms[ "TOTAL BKG" ][ category ].GetBinError(i)**2,
        "NORM": 0,
        "UP": 0,
        "DN": 0
      }
      for group in list( groups[ "BKG" ][ "SUPERGROUP" ].keys() ):
        try: error_bkg[ category ][i][ "NORM" ] += normalization_uncertainty( histograms[ "BKG" ][ hist_tag( group, category ) ], i, systematics[ hist_tag( group, category ) ] )
        except: pass
      if not config_plot.options[ "ALL SYSTEMATICS" ]: continue
      for syst in syst_list:
        for group in list( groups[ "BKG" ][ "SUPERGROUP" ].keys() ):
          try:
            error_up = histograms[ "BKG" ][ hist_tag( group, category, syst + "UP" ) ].GetBinContent(i) - histograms[ "BKG" ][ hist_tag( group, category ) ].GetBinContent(i)
            error_dn = histograms[ "BKG" ][ hist_tag( group, category ) ].GetBinContent(i) - histograms[ "BKG" ][ hist_tag( group, category, syst + "DN" ) ].GetBinContent(i)
            if error_up > 0: error_bkg[ category ][i]["UP"] += error_up**2
            else: error_bkg[ category ][i]["DN"] += error_up**2
            if error_dn > 0: error_bkg[ category ][i]["DN"] += error_dn**2
            else: error_bkg[ category ][i]["UP"] += error_dn**2
          except:
            pass
      if args.verbose:
        print( "       > Bin {}: STAT = {:.3f}, NORM = {:.3f}, UP = {:.3f}, DOWN = {:.3f}".format( i, math.sqrt( error_bkg[ category ][i]["STAT"] ), math.sqrt( error_bkg[ category ][i]["NORM"] ), math.sqrt( error_bkg[ category ][i]["UP"] ), math.sqrt( error_bkg[ category ][i]["DN" ] ) ) )
  print( "[DONE] Finished calculating statistical and systematic uncertainties" )

  print( "[START] Loading uncertainty bands into histograms" )
  for key in [ "SHAPE ONLY", "SHAPE + NORM", "ALL" ]:
    print( "   + {}".format( key ) )
    histograms[ "TOTAL BKG {}".format( key ) ] = {}
    for category in categories:
      histograms[ "TOTAL BKG {}".format( key ) ][ category ] = ROOT.TGraphAsymmErrors( histograms[ "TOTAL BKG" ][ category ].Clone( "TOTAL BKG {}".format( key ) ) )
      total_error = {}
      for i in range( 1, histograms[ "TOTAL BKG" ][ category ].GetNbinsX() + 1 ):
        total_error[i] = {}
        for shift in [ "UP", "DN" ]: 
          total_error[i][ shift ] = error_bkg[ category ][i][ "STAT" ] 
          if key in [ "SHAPE + NORM", "ALL" ]: total_error[i][ shift ] += error_bkg[ category ][i][ "NORM" ]
          if key in [ "ALL" ]: total_error[i][ shift ] += error_bkg[ category ][i][ shift ]
          total_error[i][ shift ] = math.sqrt( total_error[i][ shift ] )
        histograms[ "TOTAL BKG {}".format( key ) ][ category ].SetPointEYhigh( i - 1, total_error[i][ "UP" ] )
        histograms[ "TOTAL BKG {}".format( key ) ][ category ].SetPointEYlow( i - 1, total_error[i][ "DN" ] )
    
  for category in categories:
    for i in range( 1, histograms[ "TOTAL BKG" ][ category ].GetNbinsX() + 1 ):
      histograms[ "TOTAL BKG" ][ category ].SetBinError( 
        i, 
        ( histograms[ "TOTAL BKG ALL" ][ category ].GetErrorYlow( i - 1 ) + histograms[ "TOTAL BKG ALL" ][ category ].GetErrorYhigh( i - 1 ) ) / 2.
      )

  print( "[DONE] Finished loading uncertainty bands into histograms" )

  print( ">> Found categories:" )
  for category in sorted( categories ): print( "   + {}".format( category ) )
  print( ">> Found systematics:" )
  for syst_name in syst_list: print( "   + {}".format( syst_name ) )
  print( "[DONE] Finished loading histograms." )
  for key in histograms:
    for hist_name in histograms[ key ]:
      try: histograms[ key ][ hist_name ].SetDirectory(0)
      except: pass
  return histograms, categories
  
def format_upper_hist( pad, hist, hist_bkg, blind, log_scale ):
  if "NTJETS" in hist.GetName(): hist.GetXaxis().SetNdivisions(5)
  elif "NWJETS" in hist.GetName(): hist.GetXaxis().SetNdivisions(5)
  elif "NBJETS" in hist.GetName(): hist.GetXaxis().SetNdivisions(6,ROOT.kFalse)
  pad.cd()
  hist.GetYaxis().CenterTitle()
  hist.GetYaxis().SetTitle( "Events/bin" )
  
  if blind:
    hist.GetXaxis().SetLabelSize(0.045)
    hist.GetXaxis().SetTitleSize(0.055)
    hist.GetYaxis().SetLabelSize(0.045)
    hist.GetYaxis().SetTitleSize(0.055)
    hist.GetYaxis().SetTitleOffset(1.15)
    hist.GetXaxis().SetNdivisions(506)
  else:
    hist.GetXaxis().SetLabelSize(0)
    hist.GetXaxis().SetTitleSize(0)
    hist.GetYaxis().SetLabelSize(0.04)
    hist.GetYaxis().SetTitleSize(0.05)
    hist.GetYaxis().SetTitleOffset(1.15)
    pad.SetBottomMargin(0)
  if log_scale:
    pad.SetLogy()
    hist.SetMaximum( 2e1 * hist_bkg.GetMaximum() )
    hist.SetMinimum( 1e-2 )
  else:
    hist.SetMaximum( 1.3 * hist_bkg.GetMaximum() )
    hist.SetMinimum( 0.0 )

def format_lower_hist( pad, hist, real_pull, variable ): 
  pad.SetTopMargin(0)
  pad.SetBottomMargin(0.25)

  hist.GetXaxis().SetTitle( config.plot_params[ "VARIABLES" ][ variable ][2] )
  hist.GetXaxis().SetLabelSize(0.10)
  hist.GetXaxis().SetTitleSize(0.12)
  hist.GetXaxis().SetTitleOffset(0.95)
  hist.GetXaxis().SetNdivisions(506)
  
  if "NTJETS" in variable: hist.GetXaxis().SetNdivisions(5)
  elif "NWJETS" in variable: hist.GetXaxis().SetNdivisions(5)
  elif "NBJETS" in variable: hist.GetXaxis().SetNdivisions(6,ROOT.kFalse)
  else: hist.GetXaxis().SetNdivisions(506)
  
  hist.GetYaxis().SetLabelSize(0.10)
  hist.GetYaxis().SetTitleSize(0.12)
  hist.GetYaxis().SetTitleOffset(0.37)
  hist.GetYaxis().SetTitle( "Data/Bkg" )
  hist.GetYaxis().SetNdivisions(506)
  
  if real_pull: 
    hist.GetYaxis().SetRangeUser( min( -2.99, 0.8 * hist.GetBinCOntent( hist.GetMaximumBin() ) ), max( 2.99, 1.2 * hist.GetBinContent( hist.GetMaximumBin() ) ) )
  else:
    hist.GetYaxis().SetRangeUser( 0.01, 1.99 )
  hist.GetYaxis().CenterTitle()

def stat_test( histograms, categories ):
  print( "[START] Computing MC and Data agreement statistics by category:" )
  stats = {}
  table = []
  for category in categories:
    row = [ category ]
    hist_test = {
      "BKG": histograms[ "TOTAL BKG" ][ category ].Clone(),
      "DAT": histograms[ "TOTAL DAT" ][ category ].Clone()
    }
    for i in range( 1, hist_test[ "BKG" ].GetNbinsX() + 1 ):
      hist_test[ "BKG" ].SetBinError( i, ( histograms[ "TOTAL BKG ALL" ][ category ].GetErrorYlow( i - 1 ) + histograms[ "TOTAL BKG ALL" ][ category ].GetErrorYhigh( i - 1 ) ) / 2 )
    
    KS_prob = hist_test[ "BKG" ].KolmogorovTest( hist_test[ "DAT" ] )
    KS_prob_X = hist_test[ "BKG" ].KolmogorovTest( hist_test[ "DAT" ], "X" )
    Chi2_prob = hist_test[ "DAT" ].Chi2Test( hist_test[ "BKG" ], "UW" )
    Chi2 = hist_test[ "DAT" ].Chi2Test( hist_test[ "BKG" ], "UW CHI2" )
    
    if hist_test[ "DAT" ].Chi2Test( hist_test[ "BKG" ], "UW CHI2/NDF" ) != 0: NDOF = Chi2 / hist_test[ "DAT" ].Chi2Test( hist_test[ "BKG" ], "UW CHI2/NDF" )
    else: NDOF = 0
    
    stats[ category ] = {
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
    print( "   + BKG: {:.1f}, DAT: {}, Ratio = {:.3f}".format( stats[ category ][ "BKG" ], stats[ category ][ "DAT" ], stats[ category ][ "RATIO" ] ) )
    print( "   + KS (p): {:.3e}, KS (p) X: {:.3e}".format( KS_prob, KS_prob_X ) )
    print( "   + Chi2 (p): {:.1f}, Chi2: {:.1f}, NDOF: {}".format( Chi2, Chi2, int(NDOF) ) )
    
    table.append( row )
    
  print( "[DONE] Finished calculating statistics" )
  return table

def plot_distribution( templateDir, lep, groups, hists, categories, lumiStr, plot_yields, blind, log, norm_bin_width, compare_shapes, rebinned, smooth_syst, scale_signal_yield, real_pull ):
  print( "[START] Plotting histograms for Lepton = {}".format( lep ) )
  print( ">> Using options: " )
  print( "   + PLOT YIELDS: {}".format( plot_yields ) )
  print( "   + SMOOTH SYST: {}".format( smooth_syst ) )
  print( "   + BLIND: {}".format( blind ) )
  print( "   + NORM BIN WIDTH: {}".format( norm_bin_width ) )
  print( "   + COMPARE SHAPES: {}".format( compare_shapes ) )
  print( "   + REBINNED: {}".format( rebinned ) )
  print( "   + SCALE SIGNAL YIELD: {}".format( scale_signal_yield ) )
  print( "   + REAL PULL: {}".format( real_pull ) )
  
  for category in categories:
    if "is" + lep not in category: continue
    print( ">> Plotting histogram {}".format( category ) )
   
    # prepare the ROOT TCanvas
    canvas = ROOT.TCanvas( category, category, 60, 60, config_plot.params[ "CANVAS" ][ "W REF" ], config_plot.params[ "CANVAS" ][ "H REF" ] )
    canvas.cd()
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
   
    # prepare the pads
    y_divisions = 0.0 if blind else config_plot.params[ "Y DIV" ]
    
    pad = { 
      "UPPER": ROOT.TPad( "UPPER", "", 0, y_divisions, 1, 1 ),
    }
    if not blind:
      pad[ "LOWER" ] = ROOT.TPad( "LOWER", "", 0, 0, 1, y_divisions )

     
    for key in pad:
      pad[ key ].SetLeftMargin( config_plot.params[ "CANVAS" ][ "L" ] / config_plot.params[ "CANVAS" ][ "W" ] )
      pad[ key ].SetRightMargin( config_plot.params[ "CANVAS" ][ "R" ] / config_plot.params[ "CANVAS" ][ "W" ] )
      pad[ key ].SetFillColor(0)
      pad[ key ].SetBorderMode(0)
      pad[ key ].SetFrameFillStyle(0)
      pad[ key ].SetFrameBorderMode(0)
      if pad == "LOWER":
        pad[ key ].SetGridy()
      pad[ key ].Draw()

    pad[ "UPPER" ].cd() 
    
    # prepare and draw the signal histograms
    print( "   >> Plotting signal histogram" )
    
    if compare_shapes:
      print( "   [OPT] Scaling signal yield to match background yield" )
      hists[ "TOTAL SIG" ][ category ].Scale( hists[ "TOTAL BKG" ][ category ].Integral() / hists[ "TOTAL SIG" ][ category ].Integral() )

    hists[ "TOTAL SIG" ][ category ].SetLineColor( config_plot.params[ "SIG COLOR" ] )
    hists[ "TOTAL SIG" ][ category ].SetLineStyle(7)
    hists[ "TOTAL SIG" ][ category ].SetFillStyle(0)
    hists[ "TOTAL SIG" ][ category ].SetLineWidth(3)
    hists[ "TOTAL SIG" ][ category ].GetYaxis().SetTitle( "Events/bin" )
    if norm_bin_width:
      hists[ "TOTAL SIG" ][ category ].GetYaxis().SetTitle( "<Events/GeV>" )
    hists[ "TOTAL SIG" ][ category ].Draw( "HIST" )
   
    # prepare and draw the background histograms
    print( "  >> Plotting stacked background histograms" )
    for process in sorted( groups[ "BKG" ][ "SUPERGROUP" ].keys(), reverse = True ):
      try:
        hists[ "BKG" ][ hist_tag( process, category ) ].SetLineColor( config_plot.params[ "BKG COLORS" ][ process ] )
        hists[ "BKG" ][ hist_tag( process, category ) ].SetFillColor( config_plot.params[ "BKG COLORS" ][ process ] )
        hists[ "BKG" ][ hist_tag( process, category ) ].SetLineWidth(2)
      except: pass
    if plot_yields:
      try:
        hists[ "TOTAL BKG" ][ category ].SetMarkerSize(4)
        hists[ "TOTAL BKG" ][ category ].SetMarkerColor( config_plot.params[ "BKG COLORS" ][ process ] )
      except: pass
    bkg_stack = ROOT.THStack( "BKG STACK", "" )
    for group in sorted( groups[ "BKG" ][ "SUPERGROUP" ].keys() ):
      try:    bkg_stack.Add( hists[ "BKG" ][ hist_tag( group, category ) ] )
      except: pass
    
    bkg_stack.Draw( "SAME HIST" )
    hists[ "TOTAL SIG" ][ category ].Draw( "SAME HIST" )

    print( "  >> Plotting error band(s) for background:" )
    for error in config_plot.params[ "ERROR BAND" ]:
      print( "   + {}".format( error ) )

      hists[ "TOTAL BKG {}".format( error ) ][ category ].SetFillStyle(3004)
      hists[ "TOTAL BKG {}".format( error ) ][ category ].SetFillColor( config_plot.params[ "BKG COLORS" ][ "ERROR" ] )
      hists[ "TOTAL BKG {}".format( error ) ][ category ].SetLineColor( config_plot.params[ "BKG COLORS" ][ "ERROR" ] )
      hists[ "TOTAL BKG {}".format( error ) ][ category ].Draw( "SAME E2" )
     
    format_upper_hist( pad[ "UPPER" ], hists[ "TOTAL SIG" ][ category ], hists[ "TOTAL BKG" ][ category ], blind, log )

    # draw data if unblinded
    if not blind:
      hists[ "TOTAL DAT" ][ category ].SetMarkerColor( config_plot.params[ "DAT COLOR" ] )
      hists[ "TOTAL DAT" ][ category ].SetMarkerSize(1.2)
      hists[ "TOTAL DAT" ][ category ].SetLineWidth(2)
      hists[ "TOTAL DAT" ][ category ].SetMarkerColor( config_plot.params[ "DAT COLOR" ] )
      hists[ "TOTAL DAT" ][ category ].SetTitle( "" )
      
      if not norm_bin_width: hists[ "TOTAL DAT" ][ category ].SetMaximum( 1.2 * max( hists[ "TOTAL DAT" ][ category ].GetMaximum(), hists[ "TOTAL BKG" ][ category ].GetMaximum() ) )
    
      if not plot_yields: hists[ "TOTAL DAT" ][ category ].SetMarkerStyle(20)
      else: hists[ "TOTAL DAT" ][ category ].SetMarkerSize(3)

      if rebinned: hists[ "TOTAL DAT" ][ category ].Draw( "esamex1" )
      else: hists[ "TOTAL DAT" ][ category ].Draw( "esamex0" )
      
      if plot_yields:
        ROOT.gStyle.SetPaintTextFormat( "1.0f" )
        hists[ "TOTAL DAT" ][ category ].Draw( "SAME TEXT00" )
    
    #pad[ "UPPER" ].RedrawAxis()
    
    # latex 
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex_size = config_plot.params[ "LATEX SIZE" ] if not blind else 0.6 * config_plot.params[ "LATEX SIZE" ]
    latex.SetTextSize( latex_size )
    latex.SetTextAlign(21)
    
    splits = category.split( "n" )
    cat_text = {
      "LEP": splits[0][-1] + " + jets",
      "NHOT": "N_{HOT}#geq" + splits[1][3:-1] if "p" in splits[1] else "N_{HOT}=" + splits[1][-1],
      "NT": "N_{t}#geq" + splits[2][1:-1] if "p" in splits[2] else "N_{t}=" + splits[2][-1],
      "NW": "N_{W}#geq" + splits[3][1:-1] if "p" in splits[3] else "N_{W}=" + splits[3][-1],
      "NB": "N_{b}#geq" + splits[4][1:-1] if "p" in splits[4] else "N_{b}=" + splits[4][-1],
      "NJ": "N_{j}#geq" + splits[5][1:-1] if "p" in splits[5] else "N_{j}=" + splits[5][-1]
    }
    mod_x = 0.9 if blind else 1.0
    mod_y = 1.1 if blind else 1.0
    latex.DrawLatex( 
      config_plot.params[ "CANVAS" ][ "TAG X" ] * mod_x, config_plot.params[ "CANVAS" ][ "TAG Y" ] * mod_y,
      cat_text[ "LEP" ]
    )
    latex.DrawLatex(
      config_plot.params[ "CANVAS" ][ "TAG X" ] * mod_x, ( config_plot.params[ "CANVAS" ][ "TAG Y" ] - 0.05 ) * mod_y,
      ", ".join( [ cat_text[ "NJ" ], cat_text[ "NB" ], cat_text[ "NW" ], cat_text[ "NT" ] ] )
    )
    latex.DrawLatex(
      config_plot.params[ "CANVAS" ][ "TAG X" ] * mod_x, ( config_plot.params[ "CANVAS" ][ "TAG Y" ] - 0.10 ) * mod_y,
      cat_text[ "NHOT" ] 
    )
    
    if blind:
      legend = ROOT.TLegend( 0.65, 0.7, 0.95, 0.88 )
    else:
      legend = ROOT.TLegend( 0.65, 0.63, 0.95, 0.88 )
    legend.SetShadowColor(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetLineColor(0)
    legend.SetLineStyle(0)
    legend.SetBorderSize(0)
    legend.SetNColumns(2)
    legend.SetTextFont(42)
    legend.SetTextSize( config_plot.params[ "LEGEND" ][ "TEXT SIZE" ] )

    if not blind:
      legend.AddEntry( hists[ "TOTAL DAT" ][ category ], "DATA", "ep" )
    
    for group in list( groups[ "BKG" ][ "SUPERGROUP" ].keys() ):
      legend.AddEntry( hists[ "BKG" ][ hist_tag( group, category ) ], group, "f" ) 
    for error in config_plot.params[ "ERROR BAND" ]:
      legend.AddEntry( hists[ "TOTAL BKG {}".format( error ) ][ category ], error, "f" )
      
    if scale_signal_yield:
      legend.AddEntry( hists[ "TOTAL SIG" ][ category ], "SIG x{}".format( config_plot.params[ "SCALE SIGNAL YIELD" ] ), "l" )
    else:
      legend.AddEntry( hists[ "TOTAL SIG" ][ category ], "SIG", "l" )
    legend.Draw( "SAME" )
    
    cms_lumi( pad[ "UPPER" ], config_plot.params[ "POSTFIX TEXT" ], blind )
    
    pad[ "UPPER" ].Update()
    #pad[ "UPPER" ].RedrawAxis()
    frame = pad[ "UPPER" ].GetFrame()
    #pad[ "UPPER" ].Draw()
    
    if not blind:
      pad[ "LOWER" ].cd()
      pull = hists[ "TOTAL DAT" ][ category ].Clone()
      if not real_pull:
        # draw the ratio plot
        pull.Divide( hists[ "TOTAL DAT" ][ category ], hists[ "TOTAL BKG" ][ category ] )
        for i in range( 1, hists[ "TOTAL DAT" ][ category ].GetNbinsX() + 1 ):
          #print( "[INFO] {} bin {}: DAT / BKG = {} / {} = {:.2f}".format( category, i, hists[ "TOTAL DAT" ][ category ].GetBinContent(i), hists[ "TOTAL BKG" ][ category ].GetBinContent(i), pull.GetBinContent(i) ) )
          i_label = i - 1
          if args.variable.upper() in [ "NJETS" ]:
            if i_label % 2 == 0: pull.GetXaxis().SetBinLabel( i, str( i_label ) )
            else: pull.GetXaxis().SetBinLabel( i, "" )
          elif args.variable.upper() in [ "NBJETS", "NWJETS", "NTJETS", "NHOTJETS" ]:
            pull.GetXaxis().SetBinLabel( i, str( i_label ) )
            
          if hists[ "TOTAL BKG" ][ category ].GetBinContent(i) != 0:
            pull.SetBinError( i, hists[ "TOTAL DAT" ][ category ].GetBinError(i) / hists[ "TOTAL BKG" ][ category ].GetBinContent(i) )
        
        pull.SetMaximum(2)
        pull.SetMinimum(0)
        pull.SetFillColor(1)
        pull.SetLineColor(1)
        format_lower_hist(
          pad[ "LOWER" ],
          pull,
          real_pull,
          args.variable
        )
        print( "  >> Plotting un-blinded pull plot" )
        pull.Draw( "E1" )
        line = ROOT.TLine( min( config.plot_params[ "VARIABLES" ][ args.variable ][1] ), 1, max( config.plot_params[ "VARIABLES" ][ args.variable ][1] ), 1 )
        line.SetLineColor( ROOT.kBlack )
        line.SetLineWidth(2)
        line.Draw("SAME")

        # draw the total uncertainty band of the ratio plot
        bkg_to_bkg = pull.Clone()
        bkg_to_bkg.Divide( hists[ "TOTAL BKG" ][ category ], hists[ "TOTAL BKG" ][ category ] )
        
        pull_error = { error: ROOT.TGraphAsymmErrors( bkg_to_bkg.Clone() ) for error in config_plot.params[ "ERROR BAND" ] }
        
        for i, error in enumerate( pull_error ):
          for j in range( 0, hists[ "TOTAL BKG" ][ category ].GetNbinsX() + 2 ):
            if hists[ "TOTAL BKG" ][ category ].GetBinContent(j) != 0:
              pull_error[ error ].SetPointEYhigh( 
                j - 1, 
                hists[ "TOTAL BKG {}".format( error ) ][ category ].GetErrorYhigh(j-1) / hists[ "TOTAL BKG" ][ category ].GetBinContent(j) 
              )
              pull_error[ error ].SetPointEYlow(
                j - 1, 
                hists[ "TOTAL BKG {}".format( error ) ][ category ].GetErrorYlow(j-1) / hists[ "TOTAL BKG" ][ category ].GetBinContent(j) 
              )
          pull_error[ error ].SetFillStyle(3013)
          pull_error[ error ].SetFillColor(1+i)
          pull_error[ error ].SetLineColor(1+i)
          pull_error[ error ].SetMarkerSize(1)
          ROOT.gStyle.SetHatchesLineWidth(1)
          pull_error[ error ].Draw( "SAME E2" )
        
        pull_legend = ROOT.TLegend( config_plot.params[ "LEGEND" ][ "X1" ], config_plot.params[ "LEGEND" ][ "Y1" ], config_plot.params[ "LEGEND" ][ "X2" ], config_plot.params[ "LEGEND" ][ "Y2" ] )
        ROOT.SetOwnership( pull_legend, 0 )
        pull_legend.SetShadowColor(0)
        pull_legend.SetNColumns(3)
        pull_legend.SetFillColor(0)
        pull_legend.SetFillStyle(0)
        pull_legend.SetLineColor(0)
        pull_legend.SetLineStyle(0)
        pull_legend.SetBorderSize(0)
        pull_legend.SetTextFont(42)
        pull_legend.SetTextSize( 0.02 + config_plot.params[ "LEGEND" ][ "TEXT SIZE" ] )

        for error in config_plot.params[ "ERROR BAND" ]:
          if error in [ "ALL" ] and config_plot.options[ "ALL SYSTEMATICS" ]:
            pull_legend.AddEntry( pull_error[ error ], "BKG ERR (STAT #oplus SYST)", "f" )
          else:
            pull_legend.AddEntry( pull_error[ error ], "BKG ERR ({})".format( error ), "f" )
            
        pull_legend.Draw( "SAME" )
        pull.Draw( "SAME" )
        pad[ "LOWER" ].RedrawAxis()
        
      if real_pull:
        pad[ "LOWER" ].cd()  
        for i in range( 1, hists[ "TOTAL DAT" ][ category ].GetNbinsX() + 1 ):
          label_i = i - 1
          if "NJETS" in args.variable:
            if label_i % 2 == 0: pull.GetXaxis().SetBinLabel( i, str( label_i ) )
            else: pull.GetXaxis().SetBinLabel( i, "" ) 
          if "NBJETS" in args.variable or "NRESOLVEDTOPS" in args.variable or "NWJETS" in args.variable or "NTJETS" in args.variable:
            pull.GetXaxis().SetBinLabel( i, str( label_i ) )
          if hists[ "DAT" ][ category ].GetBinContent( i ) != 0:
            error_MC = 0.5 * ( hists[ "TOTAL BKG ALL" ][ category ].GetErrorYhigh( i - 1 ) + hists[ "TOTAL BKG ALL" ][ category ].GetErrorYlow( i - 1 ) )
            pull.SetBinContent( i, ( hists[ "TOTAL DAT" ][ category ].GetBinContent(i) - hists[ "TOTAL BKG" ].GetBinContent(i) ) / math.sqrt( error_MC**2 + hists[ "TOTAL DAT" ][ category ].GetBinError(i)**2 ) )
          else:
            pull.SetBinContent( i, 0. )
        pull.SetMaximum(3)
        pull.SetMinimum(-3)
        pull.SetFillColor( config_plots.params[ "SIG PULL COLOR" ] )
        pull.SetLineColor( config_plots.params[ "SIG PULL COLOR" ] )
        format_lower_hist( 
          hists[ "TOTAL BKG" ][ category ],
          real_pull,
          args.variable
        )
        pull.GetYaxis().SetTitle( "#frac{(OBS-BKG)}{#sigma}" )
        pull.Draw( "HIST" )
    
    save_name = hist_tag( args.variable, category )
    if rebinned: save_name += "_rebinned_stat{}".format( str( config.params[ "MODIFY BINNING" ][ "STAT THRESHOLD" ] ).replace( ".", "p" ) )
    if real_pull: save_name += "_pull"
    if blind: save_name += "_blind"
    if config_plot.options[ "Y LOG" ]: save_name += "_logy"
    save_name += ".png"
    if not os.path.exists( os.path.join( templateDir, "plots/" ) ): os.system( "mkdir -vp {}".format( os.path.join( templateDir, "plots/" ) ) )
    canvas.SaveAs( os.path.join( templateDir, "plots/", save_name ) )

def plot_background_ratio( hists, categories, lepton, groups, templateDir ):
  categories_lep = []
  for category in categories:
    if "is"+lepton in category: categories_lep.append( category )

  canvas = ROOT.TCanvas( "BACKGROUND RATIO", "BACKGROUND RATIO", 50, 50, 750, 500 )
  canvas.cd()
  canvas.SetFillColor(0)
  canvas.SetBorderMode(0)
  canvas.SetFrameFillStyle(0)
  canvas.SetFrameBorderMode(0)

  pad = {
    "UPPER": ROOT.TPad( "UPPER", "", 0, config_plot.params[ "Y DIV" ], 1 ,1 ),
    "LOWER": ROOT.TPad( "LOWER", "", 0, 0, 1, config_plot.params[ "Y DIV" ] )
  }
  
  pad[ "UPPER" ].SetBottomMargin(0)
  pad[ "LOWER" ].SetTopMargin(0)
  pad[ "LOWER" ].SetBottomMargin(0.50)
  for key in pad:
    pad[ key ].SetLeftMargin(  config_plot.params[ "CANVAS" ][ "L" ] / config_plot.params[ "CANVAS" ][ "W" ] )
    pad[ key ].SetRightMargin( config_plot.params[ "CANVAS" ][ "R" ] / config_plot.params[ "CANVAS" ][ "W" ] ) 
    pad[ key ].SetFillColor(0)
    pad[ key ].SetBorderMode(0)
    pad[ key ].SetFrameFillStyle(0)
    pad[ key ].SetFrameBorderMode(0)
    pad[ key ].Draw()

  ratio_stack = ROOT.THStack( "RATIO STACK", "" )
  ratio_legend = ROOT.TLegend( 0.35, 0.7, 0.8, 0.9 )
  ratio_legend.SetShadowColor(0)
  ratio_legend.SetFillStyle(0)
  ratio_legend.SetLineColor(0)
  ratio_legend.SetBorderSize(0)
  ratio_legend.SetLineStyle(0)
  ratio_legend.SetNColumns(3)
  ratio_legend.SetTextFont(42)
  ratio_legend.SetTextSize(0.04)

  ratio_hists = {}
  ratio_data = ROOT.TH1F( "DATA RATIO", "DATA RATIO", len( categories_lep ), 0, len( categories_lep ) )
  for group in list( groups[ "BKG" ][ "SUPERGROUP" ].keys() ):
    ratio_hists[ group ] = ROOT.TH1F( group, group, len( categories_lep ), 0, len( categories_lep ) )
    ratio_legend.AddEntry( ratio_hists[ group ], group, "f" )
    for i, category in enumerate( sorted( categories_lep ) ):
      ratio_hists[ group ].SetBinContent( i + 1, float( hists[ "BKG" ][ hist_tag( group, category ) ].Integral() ) / float( hists[ "TOTAL BKG" ][ category ].Integral() ) )
    ratio_hists[ group ].SetLineColor( config_plot.params[ "BKG COLORS" ][ group ] )
    ratio_hists[ group ].SetFillColor( config_plot.params[ "BKG COLORS" ][ group ] )
    ratio_hists[ group ].SetLineWidth(2)
    ratio_stack.Add( ratio_hists[ group ] )
  for i, category in enumerate( sorted( categories_lep ) ):
    ratio_data.SetBinContent( i + 1, float( hists[ "DAT" ][ hist_tag( "data_obs", category ) ].Integral() ) / float( hists[ "TOTAL BKG" ][ category ].Integral() ) )
    ratio_data.GetXaxis().SetBinLabel( i + 1, category )

  ratio_data.SetMinimum( 0.50 )
  ratio_data.SetMaximum( 1.05 )
  ratio_data.GetXaxis().SetLabelSize( 0.09 )
  ratio_data.GetYaxis().SetTitle( "Data/Bkg" )
  ratio_data.GetYaxis().SetTitleOffset( 0.50 )
  ratio_data.GetYaxis().CenterTitle()
  ratio_data.LabelsOption( "v" )

  pad[ "UPPER" ].cd()
  ratio_stack.SetMaximum(1.3)
  ratio_stack.SetMinimum(0.0)
  ratio_stack.Draw( "HIST" )
  ratio_legend.Draw( "SAME HIST" )
  
  cms_lumi( pad[ "UPPER" ], config_plot.params[ "POSTFIX TEXT" ], False )

  pad[ "UPPER" ].Update()
  pad[ "UPPER" ].RedrawAxis()

  pad[ "LOWER" ].cd()

  ratio_data.Draw( "HIST" )

  pad[ "LOWER" ].RedrawAxis()
  pad[ "LOWER" ].Update()

  save_name = "background_{}_ratio.png".format( lepton )
  canvas.SaveAs( os.path.join( templateDir, "plots/", save_name ) )

def main():
  tdrstyle.setTDRStyle()

  template_prefix = config.region_prefix[ args.region ] 
  templateDir = os.path.join( os.getcwd(), "{}_UL{}_{}".format( template_prefix, args.year, args.tag ) )
  hists, categories = load_histograms( 
    groups = samples.groups,
    templateDir = templateDir,
    rebinned = config_plot.options[ "REBINNED" ],
    scale_signal_xsec = config_plot.options[ "SCALE SIGNAL XSEC" ],
    scale_signal_yield = config_plot.options[ "SCALE SIGNAL YIELD" ],
    norm_bin_width = config_plot.options[ "NORM BIN WIDTH" ],
    smooth = config_plot.options[ "SMOOTH" ]
  )
  #table = stat_test( hists, categories )
  blind = config_plot.options[ "BLIND" ] 
  if args.region != "BASELINE" and not config.options[ "GENERAL" ][ "FINAL ANALYSIS" ]: 
    print( "[WARN] Not running final analysis for binned templates --> blinding data" )
    blind = True
  for lep in [ "E", "M", "L" ]:
    if lep in config_plot.params[ "INCLUDE LEP" ]:
      if args.templates:
        plot_distribution( 
          templateDir = templateDir, 
          lep = lep, 
          groups = samples.groups,
          hists = hists, 
          categories = categories, 
          lumiStr = config.lumiStr[ args.year ], 
          plot_yields = config_plot.options[ "YIELDS" ], 
          blind = blind, 
          log = config_plot.options[ "Y LOG" ],
          norm_bin_width = config_plot.options[ "NORM BIN WIDTH" ],
          smooth_syst = config_plot.options[ "SMOOTH" ],
          compare_shapes = config_plot.options[ "COMPARE SHAPES" ], 
          rebinned = config_plot.options[ "REBINNED" ], 
          scale_signal_yield = config_plot.options[ "SCALE SIGNAL YIELD" ], 
          real_pull = config_plot.options[ "REAL PULL" ]
        )
      if args.ratios:
        plot_background_ratio(
          hists = hists,
          categories = categories,
          lepton = lep,
          groups = samples.groups,
          templateDir = templateDir
        )
main()
