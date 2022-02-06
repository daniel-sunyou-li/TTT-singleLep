import ROOT

options = {
  "ONE BAND": True,
  "ALL SYSTEMATICS": True,
  "REBINNED": True,
  "YIELDS": True,
  "NORM BIN WIDTH": False,
  "COMPARE SHAPES": False,
  "SCALE SIGNAL YIELD": False,
  "REAL PULL": False,
}

params = {
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
    "TTBAR": ROOT.kRed
  },
  "ERROR BAND": "ALL", # "SHAPE ONLY", "SHAPE + NORM"
  "Y DIV": 0.35,
  "CANVAS": {
    "H REF": 600,
    "W REF": 800,
    "PERIOD": 4
  }
}

params[ "CANVAS" ][ "T" ] = 0.10 * params[ "CANVAS" ][ "H REF" ] 
params[ "CANVAS" ][ "B" ] = 0.12 * params[ "CANVAS" ][ "H REF" ] if options[ "GENERAL" ][ "BLIND" ] else 0.35 params[ "CANVAS" ][ "H REF" ]
params[ "CANVAS" ][ "L" ] = 0.12 * params[ "CANVAS" ][ "W REF" ]
params[ "CANVAS" ][ "R" ] = 0.04 * params[ "CANVAS" ][ "W REF" ]
params[ "CANVAS" ][ "TAG X" ] = 0.76
params[ "CANVAS" ][ "TAG Y" ] = 0.62 if options[ "GENERAL" ][ "BLIND" ] else 0.49

params[ "GENERAL" ][ "LATEX SIZE" ] = 0.04 if options[ "GENERAL" ][ "BLIND" ] else 0.06