import ROOT
import numpy as np
import pickle
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument( "-f", "--file" )
parser.add_argument( "-k", "--key" )
parser.add_argument( "--getkeys", action = "store_true" )
parser.add_argument( "--stats", action = "store_true" )
parser.add_argument( "--bins", action = "store_true" )
parser.add_argument( "--abcdnn", action = "store_true" )
args = parser.parse_args()

if ".pkl" in args.file:
  hist = pickle.load( open( args.file, "rb" ) )
else:
  hist = ROOT.TFile( args.file )

if args.getkeys:
  if ".pkl" in args.file:
    hist_names = [ key for key in hist if args.key in key ]
  else:
    hist_names = [ key.GetName() for key in hist.GetListOfKeys() if args.key in key.GetName() ]
  print( "[INFO] Found {} keys with '{}' in the name".format( len( hist_names ), args.key ) )
  for hist_name in sorted( hist_names ):
    print( hist_name )
  quit()

if args.stats:
  print( "[INFO] Quick statistics for {} -> {}".format( args.file, args.key ) )
  if ".pkl" in args.file:
    print( "  + Bins: {}".format( hist[args.key].GetNbinsX() ) )
    nomTag = "{}_{}".format( args.key.split( "_" )[0], args.key.split( "_" )[1] )
    nomSum = hist[nomTag].GetSum()
    thisSum = hist[args.key].GetSum()
    print( "  + Integral: {} ({:.3f})".format( thisSum, thisSum / nomSum ) )
  else:
    print( "  + Bins: {}".format( hist.Get( args.key ).GetNbinsX() ) )
    nomTag = "{}_{}".format( args.key.split( "_" )[0], args.key.split( "_" )[1] )
    nomSum = hist.Get( nomTag ).GetSum()
    thisSum = hist.Get( args.key ).GetSum()
    print( "  + Integral: {:.2f} ({:.3f})".format( thisSum, thisSum / nomSum ) )

if args.bins:
  print( "[INFO] Bin-by-bin content for {} -> {}".format( args.file, args.key ) )
  if ".pkl" in args.file:
    for i in range( int( hist[args.key].GetNbinsX() ) + 3 ):
      print( "BIN {:4} = {:.3f}: {:.3f} pm {:.3f}".format( i, hist[args.key].GetBinCenter(i), hist[args.key].GetBinContent(i), hist[args.key].GetBinError(i) ) )
  else:
    for i in range( int( hist.Get( args.key ).GetNbinsX() ) + 3 ):
      print( "BIN {:4} = {:.3f}: {:.3f} pm {:.3f}".format( i, hist.Get( args.key ).GetBinCenter(i), hist.Get( args.key ).GetBinContent(i), hist.Get( args.key ).GetBinError(i) ) )

if args.abcdnn:
  if ".pkl" in args.file:
    hist_names = [ key for key in hist ]
  else:
    hist_names = [ key.GetName() for key in hist.GetListOfKeys() ]
  abcdnn_names = []
  for hist_name in sorted( hist_names ):
    if hist_name.endswith( "ABCDNN" ): abcdnn_names.append( hist_name )
  try:
    bins = np.zeros( hist.Get( abcdnn_names[0] ).GetNbinsX() )
  except:
    bins = np.zeros( hist[ abcdnn_names[0] ].GetNbinsX() ) 
  for hist_name in abcdnn_names:
    for i in range( len( bins ) ):
      try:
        bins[i] += hist.Get( hist_name ).GetBinContent(i) 
      except:
        bins[i] += hist[ hist_name ].GetBinContent(i)

  for i in range( len( bins ) ):
    print( "BIN {:4} = {:.5f}".format( i, bins[i] ) )


