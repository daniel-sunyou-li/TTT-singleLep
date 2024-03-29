import os, sys
sys.path.append( "../" )
import config
import ROOT

options = {
  "ALL SYSTEMATICS": True,
  "CR SYST": False,
  "REBINNED": False,
  "ABCDNN": False,
  "YIELDS": False,
  "NORM BIN WIDTH": False,
  "COMPARE SHAPES": False,
  "SCALE SIGNAL YIELD": True,
  "SCALE SIGNAL XSEC": False,
  "REAL PULL": False,
  "BLIND": False,
  "Y LOG": True,
  "SMOOTH": True,
}

params = {
  "POSTFIX TEXT": "Preliminary",
  "INCLUDE LEP": [ "E", "M", "L" ], # E,M,L
  "ERROR BAND": [ "STAT", "NORM", "SHAPE" ], # STAT, SHAPE, NORM
  "EXCLUDE SYST": [ # templates will contain some systematics that are being unused, so exclude them from the plots 
    "PDFEWK", "PDFQCD", "PDFTOP", "PDFTTBAR", "PDFTTH", "PDFSIG", "PDFTTTT", "PDFST",
    "PSWGT", "PSWGTSIG", "PSWGTTTBAR", "PSWGTTOP", "PSWGTTTH", "PSWGTEWK", "PSWGTQCD", "PSWGTTTTT", "PSWGTST",
    #"PILEUP", 
    #"PREFIRE",
    #"MURSIG", "MURTTBAR", "MURTOP", "MURTTH", "MUREWK", "MURQCD",
    #"MUFSIG", "MUFTTBAR", "MUFTOP", "MUFTTH", "MUFEWK", "MUFQCD",
    "MURFSIG", "MURFTTBAR", "MURFTOP", "MURFTTH", "MURFEWK", "MURFQCD", "MURFTTTT", "MURFST",
    "MUENVSIG", "MUENVTTBAR", "MUENVTOP", "MUENVTTH", "MUENVEWK", "MUENVQCD", "MUENVTTTT", "MUEVNST",
    #"MURFCORRD", "MURFCORRDSIG", "MURFCORRDTTBAR", "MURFCORRDTOP", "MURFCORRDTTH", "MURFCORRDEWK", "MURFCORRDQCD",
    #"MUENV", "MURF", "MUF", "MUR", "MURFCORRD",
    #"ISR",  
    #"FSR",   
    #"HOTSTAT",   
    #"HOTCSPUR",
    #"HOTCLOSURE",
    #"LF", # this is fine
    #"LFSTATS2", # this one might have an issue
    #"lfstats2", # this one might have an issue
    #"HF", # this is fine
    #"hfstats1",
    #"hfstats2",
    #"cferr1",
    #"cferr2",
    #"JER", 
    #"JEC", 
  ],
  "SCALE SIGNAL YIELD": 1000,
  "DAT COLOR": ROOT.kBlack,
  "SIG COLOR": ROOT.kBlack,
  "SIG PULL COLOR": 2,
  "BKG COLORS": {
    "TTJJ": ROOT.kRed - 7,
    "TTCC": ROOT.kRed - 5,
    "TT1B": ROOT.kRed - 3,
    "TT2B": ROOT.kRed + 3,
    "TTBB": ROOT.kOrange + 7, 
    "TTNOBB": ROOT.kOrange - 2,
    "TTTT": ROOT.kAzure - 3,
    "TTH": ROOT.kAzure + 10,  
    "EWK": ROOT.kGreen + 2,
    "TOP": ROOT.kTeal + 1, 
    "ST": ROOT.kSpring + 7,
    "QCD": ROOT.kViolet + 1,
    "TTBAR": ROOT.kOrange - 2,
    "ABCDNN": ROOT.kOrange - 2,
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
    "X1": 0.15,
    "Y1": 0.80,
    "X2": 0.45,
    "Y2": 0.88,
    "TEXT SIZE": 0.02
  }
}

for i in range( len( params[ "EXCLUDE SYST" ] ) ):
  params[ "EXCLUDE SYST" ][i] = params[ "EXCLUDE SYST" ][i].upper() 
  if options[ "SMOOTH" ]: params[ "EXCLUDE SYST" ].append( params[ "EXCLUDE SYST" ][i] + config.params[ "MODIFY BINNING" ][ "SMOOTHING ALGO" ].upper() )

params[ "CANVAS" ][ "T" ] = 0.10 * params[ "CANVAS" ][ "H REF" ] 
params[ "CANVAS" ][ "B" ] = 0.12 * params[ "CANVAS" ][ "H REF" ] if options[ "BLIND" ] else 0.35 * params[ "CANVAS" ][ "H REF" ]
params[ "CANVAS" ][ "L" ] = 0.12 * params[ "CANVAS" ][ "W REF" ]
params[ "CANVAS" ][ "R" ] = 0.04 * params[ "CANVAS" ][ "W REF" ]
params[ "CANVAS" ][ "W" ] = 1. * params[ "CANVAS" ][ "W REF" ]
params[ "CANVAS" ][ "H" ] = 1. * params[ "CANVAS" ][ "W REF" ]
params[ "CANVAS" ][ "TAG X" ] = 0.20
params[ "CANVAS" ][ "TAG Y" ] = 0.76

params[ "LATEX SIZE" ] = 0.04
