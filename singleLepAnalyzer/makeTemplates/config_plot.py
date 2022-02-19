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
  "Y LOG": True
}

params = {
  "POSTFIX TEXT": "Preliminary",
  "INCLUDE LEP": [ "L" ], # E,M,L
  "ERROR BAND": [ "ALL" ], # "SHAPE ONLY", "SHAPE + NORM"
  "SCALE SIGNAL YIELD": 10,
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
    "EWK": ROOT.kMagenta - 2,
    "QCD": ROOT.kOrange + 5,
    "TTBAR": ROOT.kRed,
    "ERROR": ROOT.kBlack,
  },
  "Y DIV": 0.35,
  "CANVAS": {
    "H REF": 600,
    "W REF": 800,
    "I PERIOD": 4,
    "I POSITION": 11,
  },
  "LEGEND": {
    "X1": 0.18,
    "Y1": 0.80,
    "X2": 0.80,
    "Y2": 0.90,
    "TEXT SIZE": 0.04
  }
}

params[ "CANVAS" ][ "T" ] = 0.10 * params[ "CANVAS" ][ "H REF" ] 
params[ "CANVAS" ][ "B" ] = 0.12 * params[ "CANVAS" ][ "H REF" ] if options[ "BLIND" ] else 0.35 * params[ "CANVAS" ][ "H REF" ]
params[ "CANVAS" ][ "L" ] = 0.12 * params[ "CANVAS" ][ "W REF" ]
params[ "CANVAS" ][ "R" ] = 0.04 * params[ "CANVAS" ][ "W REF" ]
params[ "CANVAS" ][ "W" ] = 1. * params[ "CANVAS" ][ "W REF" ]
params[ "CANVAS" ][ "H" ] = 1. * params[ "CANVAS" ][ "W REF" ]
params[ "CANVAS" ][ "TAG X" ] = 0.82
params[ "CANVAS" ][ "TAG Y" ] = 0.66 if options[ "BLIND" ] else 0.49

params[ "LATEX SIZE" ] = 0.03 if options[ "BLIND" ] else 0.04
