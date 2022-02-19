from argparse import ArgumentParser
import os, sys, math
sys.path.append( "../" )
import config
import tdrstyle
import config_plot

parser = ArgumentParser()
parser.add_argument( "-y", "--year", required = True, help = "16APV,16,17,18" )
parser.add_argument( "-r", "--region", required = True, help = "SR,BASELINE" )
parser.add_argument( "-t", "--tag", required = True )
parser.add_argument( "-v", "--variable", required = True )
parser.add_argument( "--verbose", action = "store_true" )
parser.add_argument( "--rebin", action = "store_true" )
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

def hist_tag( *args ):
  histTag = args[0]
  for arg in args[1:]: histTag += "_{}".format( arg )
  return histTag

def hist_parse( hist_name ):
  parse = {
    "PROCESS": "",
    "GROUP": "",
    "SYST": "",
    "SHIFT": "",
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
      parse[ "SHIFT" ] = part[-2:]
      parse[ "SYST" ] = part[:-2]
      parse[ "IS SYST" ] = True
    if "PDF" in part:
      parse[ "SHIFT" ] = part[-2:]
      parse[ "SYST" ] = "PDF{}".format( config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() ) if config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() in part else "PDF"
      parse[ "IS SYST" ] = True
    # handle category
    if part.startswith( "isE" ) or part.startswith( "isM" ) or part.startswith( "isL" ):
      parse[ "CATEGORY" ] = part
      parse[ "CHANNEL" ] = part[3:]
  return parse

def modeling_systematics( categories, groups ):
  systematics = {}
  for category in categories:
    if "isL" in category: continue
    if not config_plot.options[ "CR SYST" ]:
      for process in groups[ "BKG" ][ "PROCESS" ]:
        systematics[ hist_tag( process, category[2:] ) ] = 0.
    for group in groups[ "BKG" ][ "SUPERGROUP" ]:
      if group not in [ "TTBB", "TTNOBB", "TOP", "EWK" ]: continue
      if group == "TTBB": 
        systematics[ hist_tag( group, category[2:] ) ] = math.sqrt( config.systematics[ "XSEC" ][ "TTBAR" ]**2 + config.systematics[ "TTHF" ]**2 + config.systematics[ "HDAMP" ]**2 )
      elif group == "TTNOBB":
        systematics[ hist_tag( group, category[2:] ) ] = math.sqrt( config.systematics[ "XSEC" ][ "TTBAR" ]**2 + config.systematics[ "HDAMP" ]**2 )
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

def cms_lumi( pad, postfix ):
  print( ">> Formatting CMS header text" )
  header = { 
    "TEXT": "CMS",
    "TEXT FONT": 61,
    "TEXT SIZE": 0.75,
    "TEXT OFFSET": 0.10,
    "POSTFIX": postfix,
    "POSTFIX FONT": 52,
    "POSTFIX SIZE": 0.65,
    "LUMI TEXT": str( config.lumi[ args.year ] / 1000. ) + " (13 TeV)",
    "LUMI TEXT FONT": 42,
    "LUMI TEXT SIZE": 0.65,
    "LUMI TEXT OFFSET": 0.1,
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
  pad.cd()
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextAngle(0)
  latex.SetTextColor(ROOT.kBlack)
  latex.SetTextAlign(31)
  latex.SetTextSize( pad_dim["T"] * header[ "LUMI TEXT SIZE" ] )
  latex.DrawLatex( 1 - pad_dim["R"], 1 - pad_dim["T"] + header[ "LUMI TEXT OFFSET" ], header[ "LUMI TEXT" ] )
  pad.cd()
  latex.SetTextFont( header[ "TEXT FONT" ] )
  latex.SetTextSize( pad_dim["T"] * header[ "TEXT SIZE" ] )
  latex.SetTextAlign(11)
  latex.DrawLatex( 1 - pad_dim["L"], 1 - pad_dim["T"] + header[ "TEXT OFFSET" ], header[ "TEXT" ] )
  latex.SetTextFont( header[ "POSTFIX FONT" ] )
  latex.SetTextSize( header[ "POSTFIX SIZE" ] )
  latex.SetTextAlign(11)
  latex.DrawLatex( 1 - pad_dim["R"] + 0.20, 1 - pad_dim["T"] + header[ "TEXT OFFSET" ], header[ "POSTFIX" ] )
  
  pad.Update()

def load_histograms( groups, templateDir, rebinned, scale_signal_xsec, scale_signal_yield, norm_bin_width ):
  file_name = "template_combine_{}_UL{}".format( args.variable, args.year )
  if rebinned: file_name += "_rebin_stat{}".format( str( config.params[ "MODIFY BINNING" ][ "STAT THRESHOLD" ] ).replace( ".", "p" ) )
  
  rFile = ROOT.TFile.Open( os.path.join( templateDir, file_name + ".root" ) )
  histograms = { key: {} for key in [ "BKG", "SIG", "DAT", "TOTAL BKG", "TOTAL SIG", "TOTAL DAT" ] }
  groups_bkg = list( groups[ "BKG" ][ "PROCESS" ].keys() ) + list( groups[ "BKG" ][ "SUPERGROUP" ].keys() )
  groups_sig = groups[ "SIG" ][ "PROCESS" ] + [ "SIG" ]
  groups_dat = groups[ "DAT" ][ "PROCESS" ] + [ "DAT" ]
  categories = {
    "ALL": [],
    "DAT": [],
    "BKG": [],
    "SIG": []
  }
  
  print( "[START] Loading histograms from: {}".format( file_name + ".root" ) )
  count = 0
  syst_list = []
  for hist_name in rFile.GetListOfKeys():
    parse = hist_parse( hist_name )
    category = parse[ "CATEGORY" ]
    process = parse[ "PROCESS" ]
    syst = parse[ "SYST" ]
    if category not in categories[ "ALL" ]:
      categories[ "ALL" ].append( category )
    if process in groups_dat:
      if args.verbose: print( "   + DAT: {}".format( hist_name.GetName() ) )
      histograms[ "DAT" ][ hist_name.GetName() ] = rFile.Get( hist_name.GetName() ).Clone( hist_name.GetName() )
      if category not in categories[ "DAT" ]:
        histograms[ "TOTAL DAT" ][ category ] = histograms[ "DAT" ][ hist_name.GetName() ].Clone( "TOTAL DAT {}".format( category ) )
        categories[ "DAT" ].append( category )
      else:
        histograms[ "TOTAL DAT" ][ category ].Add( histograms[ "DAT" ][ hist_name.GetName() ] )
    elif process in groups_bkg:
      if args.verbose: print( "   + BKG: {}".format( hist_name.GetName()) )
      histograms[ "BKG" ][ hist_name.GetName() ] = rFile.Get( hist_name.GetName() ).Clone( hist_name.GetName() )   
      if category not in categories[ "BKG" ] and not parse[ "IS SYST" ]:
        histograms[ "TOTAL BKG" ][ category ] = histograms[ "BKG" ][ hist_name.GetName() ].Clone( "TOTAL BKG {}".format( category ) )
        categories[ "BKG" ].append( category )
      elif not parse[ "IS SYST" ]:
        histograms[ "TOTAL BKG" ][ category ].Add( histograms[ "BKG" ][ hist_name.GetName() ] )
    elif process in groups_sig:
      if args.verbose: print( "   + SIG: {}".format( hist_name.GetName() ) )
      scale = 1.
      if scale_signal_yield: scale *= config_plot.params[ "SCALE SIGNAL YIELD" ]
      if scale_signal_xsec: scale *= weights.weights[ process ]
      histograms[ "SIG" ][ hist_name.GetName() ] = rFile.Get( hist_name.GetName() ).Clone( hist_name.GetName() )
      histograms[ "SIG" ][ hist_name.GetName() ].Scale( scale )
      if category not in categories[ "SIG" ] and not parse[ "IS SYST" ]:
        histograms[ "TOTAL SIG" ][ category ] = histograms[ "SIG" ][ hist_name.GetName() ].Clone( "TOTAL SIG {}".format( category ) )
        categories[ "SIG" ].append( category )
      elif not parse[ "IS SYST" ]:
        histograms[ "TOTAL SIG" ][ category ].Add( histograms[ "SIG" ][ hist_name.GetName() ] )

    else:
      if args.verbose: print( "[WARN] {} does not belong to any of the groups: BKG, SIG, DAT, excluding...".format( process ) )
    count += 1
  print( "[DONE] Found {} histograms".format( count ) )

  print( "[START] Creating lepton categories" )
  categories[ "ALL" ].append( categories[ "ALL" ][0].replace( "isE", "isL" ).replace( "isM", "isL" ) )
  for key in histograms:
    print( "   o {}".format( key ) )
    hist_names = [ hist_name for hist_name in list( histograms[ key ].keys() ) if "isE" in hist_name ]
    for hist_name in hist_names:
      name_lepton = hist_name.replace( "isE", "isL" )
      histograms[ key ][ name_lepton ] = histograms[ key ][ hist_name ].Clone( name_lepton )
      histograms[ key ][ name_lepton ].Add( histograms[ key ][ hist_name.replace( "isE", "isM" ) ] )
      if "UP_" not in hist_name and "DN_" not in hist_name and "PDF" not in hist_name:  print( "     + {}: {}".format( name_lepton, histograms[ key ][ name_lepton ].Integral() ) )  
  print( "[DONE]" )

  if norm_bin_width:
    print( "[START] Normalizing yield and error by bin width" )
    for key in [ "BKG", "SIG", "DAT" ]:
      print( "   + {}".format( key ) )
      for hist_name in histograms[ key ]:
        normalization_bin_width( histograms[ key ][ hist_name ] )      
    
  print( "[START] Computing the uncertainty for different background iterations: SHAPE ONLY, SHAPE + NORMALIZATION, ALL" )
  error_bkg = {}
  
  systematics = modeling_systematics( categories[ "ALL" ], groups )
  for category in categories[ "ALL" ]:
    print( "   + {}".format( category ) )
    error_bkg[ category ] = {}
    for i in range( 1, histograms[ "BKG" ][ list( histograms[ "BKG" ].keys() )[0] ].GetNbinsX() + 1 ):
      error_bkg[ category ][i] = {
        "STAT": histograms[ "TOTAL BKG" ][ category ].GetBinError(i)**2,
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
              error_minus = histograms[ "BKG" ][ hist_name ].GetBinContent(i) - histograms[ "BKG" ][ hist_tag( hist_parts[0], syst.upper() + "DN", hist_parts[1], hist_parts[2], hist_parts[3] ) ].GetBinContent(i)
              if error_plus > 0: error_bkg[ category ][i][ "UP" ] += error_plus**2
              else: error_bkg[ category ][i][ "DN" ] += error_plus**2
              if error_minus > 0: error_bkg[ category ][i][ "DN" ] += error_minus**2
              else: error_bkg[ category ][i][ "UP" ] += error_plus**2
            except: pass
  print( "[DONE] Finished calculating statistical and systematic uncertainties" )

  print( "[START] Loading uncertainty bands into histograms" )
  for key in [ "SHAPE ONLY", "SHAPE + NORM", "ALL" ]:
    print( "   + {}".format( key ) )
    histograms[ "TOTAL BKG {}".format( key ) ] = {}
    for category in categories[ "ALL" ]:
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
    
  for category in categories[ "ALL" ]:
    for i in range( 1, histograms[ "TOTAL BKG" ][ category ].GetNbinsX() + 1 ):
      histograms[ "TOTAL BKG" ][ category ].SetBinError( 
        i, 
        ( histograms[ "TOTAL BKG ALL" ][ category ].GetErrorYlow( i - 1 ) + histograms[ "TOTAL BKG ALL" ][ category ].GetErrorYhigh( i - 1 ) ) / 2.
      )

  print( "[DONE] Finished loading uncertainty bands into histograms" )

  print( ">> Found categories:" )
  for category in sorted( categories[ "ALL" ] ): print( "   + {}".format( category ) )
  print( ">> Found systematics:" )
  for syst_name in syst_list: print( "   + {}".format( syst_name ) )
  print( "[DONE] Finished loading histograms." )
  for key in histograms:
    for hist_name in histograms[ key ]:
      try: histograms[ key ][ hist_name ].SetDirectory(0)
      except: pass
  return histograms, categories[ "ALL" ]
  
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

def format_lower_hist( hist, real_pull, variable ): 
  hist.GetXaxis().SetLabelSize(0.12)
  hist.GetXaxis().SetTitleSize(0.15)
  hist.GetXaxis().SetTitleOffset(0.95)
  hist.GetXaxis().SetNdivisions(506)
  
  if "NTJETS" in variable: hist.GetXaxis().SetNdivisions(5)
  elif "NWJETS" in variable: hist.GetXaxis().SetNdivisions(5)
  elif "NBJETS" in variable: hist.GetXaxis().SetNdivisions(6,ROOT.kFalse)
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

def plot_distribution( templateDir, lep, groups, hists, categories, lumiStr, plot_yields, blind, log, norm_bin_width, compare_shapes, rebinned, scale_signal_yield, real_pull ):
  print( "[START] Plotting histograms for Lepton = {}".format( lep ) )
  print( ">> Using options: " )
  print( "   + PLOT YIELDS: {}".format( plot_yields ) )
  print( "   + BLIND: {}".format( blind ) )
  print( "   + NORM BIN WIDTH: {}".format( norm_bin_width ) )
  print( "   + COMPARE SHAPES: {}".format( compare_shapes ) )
  print( "   + REBINNED: {}".format( rebinned ) )
  print( "   + SCALE SIGNAL YIELD: {}".format( scale_signal_yield ) )
  print( "   + REAL PULL: {}".format( real_pull ) )
  
  for category in categories:
    if "is" + lep not in category: continue
    print( ">> Plotting histogram {}".format( lep, category ) )

    for process in list( groups[ "BKG" ][ "SUPERGROUP" ].keys() ) + list( groups[ "BKG" ][ "PROCESS" ].keys() ):
      try:
        hists[ "BKG" ][ hist_tag( args.variable, lumiStr, category, process ) ].SetLineColor( config_plot.params[ "BKG COLORS" ][ process ] )
        hists[ "BKG" ][ hist_tag( args.variable, lumiStr, category, process ) ].SetFillColor( config_plot.params[ "BKG COLORS" ][ process ] )
        hists[ "BKG" ][ hist_tag( args.variable, lumiStr, category, process ) ].SetLineWidth(2)
      except: pass
    if plot_yields:
      try:
        hists[ "TOTAL BKG" ][ category ].SetMarkerSize(4)
        hists[ "TOTAL BKG" ][ category ].SetMarkerColor( config_plot.params[ "BKG COLORS" ][ process ] )
      except: pass

    print( ">> Plotting error band(s) for background:" )
    for error in config_plot.params[ "ERROR BAND" ]:
      print( "   + {}".format( error ) )

      hists[ "TOTAL BKG {}".format( error ) ][ category ].SetFillStyle(3004)
      hists[ "TOTAL BKG {}".format( error ) ][ category ].SetFillColor( config_plot.params[ "BKG COLORS" ][ "ERROR" ] )
      hists[ "TOTAL BKG {}".format( error ) ][ category ].SetLineColor( config_plot.params[ "BKG COLORS" ][ "ERROR" ] )
    
    hists[ "TOTAL SIG" ][ category ].SetLineColor( config_plot.params[ "SIG COLOR" ] )
    hists[ "TOTAL SIG" ][ category ].SetLineStyle(7)
    hists[ "TOTAL SIG" ][ category ].SetFillStyle(0)
    hists[ "TOTAL SIG" ][ category ].SetLineWidth(3)
    
    hists[ "TOTAL DAT" ][ category ].SetMarkerColor( config_plot.params[ "DAT COLOR" ] )
    hists[ "TOTAL DAT" ][ category ].SetMarkerSize(1.2)
    hists[ "TOTAL DAT" ][ category ].SetLineWidth(2)
    hists[ "TOTAL DAT" ][ category ].SetMarkerColor( config_plot.params[ "DAT COLOR" ] )
    if not plot_yields:
      hists[ "TOTAL DAT" ][ category ].SetMarkerStyle(20)
    else:
      hists[ "TOTAL DAT" ][ category ].SetMarkerSize(4)
    
    if not norm_bin_width:
      hists[ "TOTAL DAT" ][ category ].SetMaximum( 1.2 * max( hists[ "TOTAL DAT" ][ category ].GetMaximum(), hists[ "TOTAL BKG" ][ category ].GetMaximum() ) )
      hists[ "TOTAL DAT" ][ category ].GetYaxis().SetTitle( "Events / bin" )
    else:
      hists[ "TOTAL DAT" ][ category ].GetYaxis().SetTitle( "< Events / GeV >" )
    
    hists[ "TOTAL DAT" ][ category ].SetTitle( "" )
    
    canvas = ROOT.TCanvas( "c1", "c1", 50, 50, config_plot.params[ "CANVAS" ][ "W REF" ], config_plot.params[ "CANVAS" ][ "H REF" ] )
    
    y_divisions = 0.0 if blind else config_plot.params[ "Y DIV" ]
    
    pad = { 
      "UPPER": ROOT.TPad( "UPPER", "", 0, y_divisions, 1, 1 ),
      "LOWER": ROOT.TPad( "LOWER", "", 0, 0, 1, y_divisions )
    }
    
    format_upper_hist( pad[ "UPPER" ], hists[ "TOTAL DAT" ][ category ], hists[ "TOTAL DAT" ][ category ], blind, log )
    
    # prepare the ROOT canvas    
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    
     
    for key in pad:
      if blind and pad == "LOWER": continue
      pad[ key ].SetLeftMargin( config_plot.params[ "CANVAS" ][ "L" ] / config_plot.params[ "CANVAS" ][ "W" ] )
      pad[ key ].SetRightMargin( config_plot.params[ "CANVAS" ][ "R" ] / config_plot.params[ "CANVAS" ][ "W" ] )
      pad[ key ].SetFillColor(0)
      pad[ key ].SetBorderMode(0)
      pad[ key ].SetFrameFillStyle(0)
      pad[ key ].SetFrameBorderMode(0)
      if pad == "UPPER": 
        pad[ key ].SetTopMargin( config_plot.params[ "CANVAS" ][ "T" ] / config_plot.params[ "CANVAS" ][ "H" ] )
        if blind:
          pad[ key ].SetBottomMargin( config_plot.params[ "CANVAS" ][ "B" ] / config_plot.params[ "CANVAS" ][ "H" ] )
        else:
          pad[ key ].SetBottomMargin( 0.01 )
      elif pad == "LOWER":
        pad[ key ].SetTopMargin( 0.01 )
        pad[ key ].SetBottomMargin( config_plot.params["CANVAS" ][ "B" ] / config_plot.params[ "CANVAS" ][ "H" ] )
        pad[ key ].SetGridy()
      pad[ key ].Draw()
    
    pad[ "UPPER" ].cd()
    
    if compare_shapes:
      print( ">> Scaling signal yield to match background yield" )
      hists[ "TOTAL SIG" ][ category ].Scale( hists[ "TOTAL BKG" ][ category ].Integral() / hists[ "TOTAL SIG" ][ category ].Integral() )
    
    if not blind:
      if rebinned: hists[ "TOTAL DAT" ][ category ].Draw( "esamex1" )
      else: hists[ "TOTAL DAT" ][ category ].Draw( "esamex0" )
    else:
      if norm_bin_width: 
        hists[ "TOTAL SIG" ][ category ].GetYaxis().SetTitle( "< Events / GeV >" )
        normalization_bin_width( hists[ "TOTAL BKG" ][ category ] )
      else:
        hists[ "TOTAL SIG" ][ category ].GetYaxis().SetTitle( "Events / bin" )
      format_upper_hist( hists[ "TOTAL SIG" ][ category ], hists[ "TOTAL BKG" ][ category ] )
      hists[ "TOTAL SIG" ][ category ].Draw( "HIST" )
    
    bkg_stack = ROOT.THStack( "BKG STACK", "" )
    for process in list( groups[ "BKG" ][ "SUPERGROUP" ].keys() ):
      try:
        bkg_stack.Add( hists[ "BKG" ][ hist_tag( args.variable, lumiStr, category, process ) ] )
      except: pass
    bkg_stack.Draw( "SAME HIST" )
    
    if plot_yields:
      ROOT.gStyle.SetPaintTextFormat( "1.0f" )
      hists[ "TOTAL BKG" ][ category ].Draw( "SAME TEXT90" )
    hists[ "TOTAL SIG" ][ category ].Draw( "SAME HIST" )
    
    if not blind:
      if rebinned: hists[ "TOTAL DAT" ][ category ].Draw( "esamex1" )
      else: hists[ "TOTAL DAT" ][ category ].Draw( "esamex0" )
      if plot_yields: hists[ "TOTAL DAT" ][ category ].Draw( "SAME TEXT00" )
    
    pad[ "UPPER" ].RedrawAxis()
    
    for error in config_plot.params[ "ERROR BAND" ]:
      hists[ "TOTAL BKG {}".format( error ) ][ category ].Draw( "SAME E2" )
    
    # latex 
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize( config_plot.params[ "LATEX SIZE" ] )
    latex.SetTextAlign(21)
    
    splits = category.split( "n" )
    cat_text = {
      "LEP": splits[0][-1] + "+jets",
      "NHOT": "#geq{} resolved t".format( splits[1][3:-1] ) if "p" in splits[1] else "{} resolved t".format( splits[1][-1] ),
      "NT": "#geq{} t".format( splits[2][1:-1] ) if "p" in splits[2] else "{} t".format( splits[2][-1] ),
      "NW": "#geq{} W".format( splits[3][1:-1] ) if "p" in splits[3] else "{} W".format( splits[3][-1] ),
      "NB": "#geq{} b".format( splits[4][1:-1] ) if "p" in splits[4] else "{} b".format( splits[4][-1] ),
      "NJ": "#geq{} j".format( splits[5][1:-1] ) if "p" in splits[5] else "{} j".format( splits[5][-1] )
    }
    latex.DrawLatex( 
      config_plot.params[ "CANVAS" ][ "TAG X" ], config_plot.params[ "CANVAS" ][ "TAG Y" ],
      cat_text[ "LEP" ]
    )
    latex.DrawLatex(
      config_plot.params[ "CANVAS" ][ "TAG X" ], config_plot.params[ "CANVAS" ][ "TAG Y" ] - 0.06,
      ",".join( [ cat_text[ "NJ" ], cat_text[ "NB" ], cat_text[ "NW" ], cat_text[ "NT" ] ] )
    )
    latex.DrawLatex(
      config_plot.params[ "CANVAS" ][ "TAG X" ], config_plot.params[ "CANVAS" ][ "TAG Y" ] - 0.12,
      cat_text[ "NHOT" ]
    )
    
    if blind:
      legend = ROOT.TLegend( 0.45, 0.64, 0.95, 0.89 )
    else:
      legend = ROOT.TLegend( 0.60, 0.70, 0.95, 0.90 )
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
      legend.AddEntry( hists[ "BKG" ][ hist_tag( args.variable, lumiStr, category, group ) ], group, "f" ) 
    
    for error in config_plot.params[ "ERROR BAND" ]:
      legend.AddEntry( hists[ "TOTAL BKG {}".format( error ) ][ category ], error, "f" )
      
    if scale_signal_yield:
      legend.AddEntry( hists[ "TOTAL SIG" ][ category ], "SIG x{}".format( config_plot.params[ "SCALE SIGNAL YIELD" ] ), "l" )
    else:
      legend.AddEntry( hists[ "TOTAL SIG" ][ category ], "SIG", "l" )
    legend.Draw( "same" )
    
    cms_lumi( pad[ "UPPER" ], config_plot.params[ "POSTFIX TEXT" ] )
    
    pad[ "UPPER" ].Update()
    pad[ "UPPER" ].RedrawAxis()
    frame = pad[ "UPPER" ].GetFrame()
    pad[ "UPPER" ].Draw()
    
    if not blind:    
      pad[ "LOWER" ].cd()
      pull = hists[ "TOTAL DAT" ][ category ].Clone( "PULL" )
      if not real_pull:
        # draw the ratio plot
        pull.Divide( hists[ "TOTAL DAT" ][ category ], hists[ "TOTAL BKG" ][ category ] )
        for i in range( 1, hists[ "TOTAL DAT" ][ category ].GetNbinsX() + 1 ):
          i_label = i - 1
          if args.variable.upper() in [ "NJETS" ]:
            if i_label % 2 == 0: pull.GetXaxis().SetBinLabel( i, str( i_label ) )
            else: pull.GetXaxis().SetBinLabel( i, "" )
          elif args.variable.upper() in [ "NBJETS", "NWJETS", "NTJETS", "NHOTJETS" ]:
            pull.GetXaxis().SetBinLabel( i, str( i_label ) )
          elif args.variable.upper() in [ "DNN_3T" ]:
            if i_label % 5 == 0: pull.GetXaxis(  )
            
          if hists[ "TOTAL BKG" ][ category ].GetBinContent(i) != 0:
            pull.SetBinError( i, hists[ "TOTAL DAT" ][ category ].GetBinError(i) / hists[ "TOTAL BKG" ][ category ].GetBinContent(i) )
        
        pull.SetMaximum(2)
        pull.SetMinimum(0)
        pull.SetFillColor(1)
        pull.SetLineColor(1)
        format_lower_hist( 
          hists[ "TOTAL BKG" ][ category ],
          real_pull,
          args.variable
        )
        print( ">> Plotting un-blinded pull plot" )
        pull.Draw( "E0" )
        
        # draw the total uncertainty band of the ratio plot
        bkg_to_bkg = pull.Clone( "BKG TO BKG" )
        bkg_to_bkg.Divide( hists[ "TOTAL BKG" ][ category ], hists[ "TOTAL BKG" ][ category ] )
        
        pull_error = { error: ROOT.TGraphAsymmErrors( bkg_to_bkg.Clone( "FULL ERROR {}".format( error ) ) ) for error in [ "SHAPE ONLY", "SHAPE + NORM", "ALL" ] }
        
        for error in pull_error:
          for i in range( 0, hists[ "TOTAL BKG" ][ category ].GetNbinsX() + 2 ):
            if hists[ "TOTAL BKG" ][ category ].GetBinContent(i) != 0:
              pull_error[ error ].SetPointEYhigh( 
                i - 1, 
                hists[ "TOTAL BKG {}".format( error ) ][ category ].GetErrorYhigh(i-1) / hists[ "TOTAL BKG" ][ category ].GetBinContent(i) 
              )
              pull_error[ error ].SetPointEYlow(
                i - 1, 
                hists[ "TOTAL BKG {}".format( error ) ][ category ].GetErrorYlow(i-1) / hists[ "TOTAL BKG" ][ category ].GetBinContent(i) 
              )
          pull_error[ error ].SetFillStyle(3013)
          pull_error[ error ].SetFillColor(i+1)
          pull_error[ error ].SetLineColor(i+1)
          pull_error[ error ].SetMarkerSize(0)
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
        for i in ranger( 1, hists[ "TOTAL DAT" ][ category ].GetNbinsX() + 1 ):
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
    if rebinned: save_name += "_rebin_stat{}".format( str( config.params[ "MODIFY BINNING" ][ "STAT THRESHOLD" ] ).replace( ".", "p" ) )
    if real_pull: save_name += "_pull"
    if blind: save_name += "_blind"
    if config_plot.options[ "Y LOG" ]: save_name += "_logy"
    save_name += ".png"
    if not os.path.exists( os.path.join( templateDir, "plots/" ) ): os.system( "mkdir -vp {}".format( os.path.join( templateDir, "plots/" ) ) )
    canvas.SaveAs( os.path.join( templateDir, "plots/", save_name ) )

def main():
  tdrstyle.setTDRStyle()

  template_prefix = config.region_prefix[ args.region ] 
  templateDir = os.path.join( os.getcwd(), "{}_UL{}_{}".format( template_prefix, args.year, args.tag ) )
  hists, categories = load_histograms( 
    groups = samples.groups,
    templateDir = templateDir,
    rebinned = args.rebin,
    scale_signal_xsec = config_plot.options[ "SCALE SIGNAL XSEC" ],
    scale_signal_yield = config_plot.options[ "SCALE SIGNAL YIELD" ],
    norm_bin_width = config_plot.options[ "NORM BIN WIDTH" ],
  )
  table = stat_test( hists, categories )
  
  for lep in [ "E", "M", "L" ]:
    if lep in config_plot.params[ "INCLUDE LEP" ]:
      plot_distribution( 
        templateDir = templateDir, 
        lep = lep, 
        groups = samples.groups,
        hists = hists, 
        categories = categories, 
        lumiStr = config.lumiStr[ args.year ], 
        plot_yields = config_plot.options[ "YIELDS" ], 
        blind = config_plot.options[ "BLIND" ], 
        log = config_plot.options[ "Y LOG" ],
        norm_bin_width = config_plot.options[ "NORM BIN WIDTH" ], 
        compare_shapes = config_plot.options[ "COMPARE SHAPES" ], 
        rebinned = args.rebin, 
        scale_signal_yield = config_plot.options[ "SCALE SIGNAL YIELD" ], 
        real_pull = config_plot.options[ "REAL PULL" ]
      )

main()
