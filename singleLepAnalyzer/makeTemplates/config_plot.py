import os, sys
sys.path.append( "../" )
import config
import ROOT

options = {
  "ALL SYSTEMATICS": True,
  "CR SYST": False,
  "REBINNED": True,
  "YIELDS": False,
  "NORM BIN WIDTH": False,
  "COMPARE SHAPES": False,
  "SCALE SIGNAL YIELD": True,
  "SCALE SIGNAL XSEC": False,
  "REAL PULL": False,
  "BLIND": False,
  "Y LOG": True,
  "SMOOTH": True,
  "SYMM SMOOTHING": False,
}

params = {
  "POSTFIX TEXT": "Preliminary",
  "INCLUDE LEP": [ "L" ], # E,M,L
  "ERROR BAND": [ "ALL" ], # "SHAPE ONLY", "SHAPE + NORM"
  "EXCLUDE SYST": [
    #"pdf", # this is fine
    #"pswgt", # this is fine
    #"pileup", # this is fine 
    "trigeff", # this one seems like there might be an issue --> way too huge? 
    #"muRF",
    "muRFcorrd", # this is fine
    "muR", # this is fine
    "muF", # this is fine
    "isr", # this is fine 
    "fsr", # this is fine 
    "hotstat",  # seems a bit large 
    "hotcspur",
    "hotclosure",
    "njet",
    "njetsf",
    "LF", # this is fine
    "lfstats1", # this one might have an issue
    "lfstats2", # this one might have an issue
    "HF", # this is fine
    "hfstats1",
    "hfstats2",
    "cferr1",
    "cferr2",
    "jes", # this one might have an issue
    "toppt",
    "ht",
    "JER", # this seems very large
    "JEC", # this seems very large
    "HD",
    "UE"
  ],
  "SCALE SIGNAL YIELD": 100,
  "DAT COLOR": ROOT.kBlack,
  "SIG COLOR": ROOT.kBlack,
  "SIG PULL COLOR": 2,
  "BKG COLORS": {
    "TT2B": ROOT.kRed + 3,
    "TT1B": ROOT.kRed - 3,
    "TTBB": ROOT.kRed,
    "TTCC": ROOT.kRed - 5,
    "TTJJ": ROOT.kRed - 7,
    "TTNOBB": ROOT.kRed - 7,
    "TOP": ROOT.kBlue,
    "TTH": ROOT.kGreen,
    "EWK": ROOT.kMagenta - 2,
    "QCD": ROOT.kOrange + 5,
    "TTBAR": ROOT.kRed,
    "ERROR": ROOT.kBlack,
  },
  "Y DIV": 0.35,
  "CANVAS": {
    "H REF": 700,
    "W REF": 800,
    "I PERIOD": 4,
    "I POSITION": 11,
  },
  "LEGEND": {
    "X1": 0.55,
    "Y1": 0.68,
    "X2": 0.95,
    "Y2": 0.88,
    "TEXT SIZE": 0.02
  }
}

for i in range( len( params[ "EXCLUDE SYST" ] ) ):
  params[ "EXCLUDE SYST" ][i] = params[ "EXCLUDE SYST" ][i].upper() 
  if options[ "SMOOTH" ]: params[ "EXCLUDE SYST" ][i] += config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper()

params[ "CANVAS" ][ "T" ] = 0.10 * params[ "CANVAS" ][ "H REF" ] 
params[ "CANVAS" ][ "B" ] = 0.12 * params[ "CANVAS" ][ "H REF" ] if options[ "BLIND" ] else 0.35 * params[ "CANVAS" ][ "H REF" ]
params[ "CANVAS" ][ "L" ] = 0.12 * params[ "CANVAS" ][ "W REF" ]
params[ "CANVAS" ][ "R" ] = 0.04 * params[ "CANVAS" ][ "W REF" ]
params[ "CANVAS" ][ "W" ] = 1. * params[ "CANVAS" ][ "W REF" ]
params[ "CANVAS" ][ "H" ] = 1. * params[ "CANVAS" ][ "W REF" ]
params[ "CANVAS" ][ "TAG X" ] = 0.82
params[ "CANVAS" ][ "TAG Y" ] = 0.60

params[ "LATEX SIZE" ] = 0.04
