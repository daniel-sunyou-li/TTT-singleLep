import os, sys
import numpy as np
from json import dumps as write_json
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument( "-x1", "--x1", default = "AK4HT", help = "Select a variable to cut events on" )
parser.add_argument( "-x2", "--x2", default = "",   help = "Select a second variable to apply 2D cuts to events on" )
parser.add_argument( "-minDR", "--minDR", action = "store_true", help = "Apply minDR(lep,jet) > 0.4 veto" )
parser.add_argument( "-y",  "--year", default = "2017", help = "Select which year to use" )
parser.add_argument( "-v",  "--verbose", action = "store_true", help = "Verbose option" )
args = parser.parse_args()

# define the cuts of interest
cuts = {
  "AK4HT": np.linspace( 250., 700., 19 ),
  "leptonPt_MultiLepCalc": np.linspace( 20., 35., 16 ),
  "NJets_JetSubCalc": np.linspace( 3, 10, 8 ),
  "NJetsCSV_MultiLepCalc": np.linspace( 0, 5, 6 ),
  "corr_met_MultiLepCalc": np.linspace( 30, 200, 18 ),
  "MT_lepMet": np.linspace( 0, 200, 21 ),
}

if args.year not in [ "2017", "2018" ]:
  print( ">> {} not a valid option, quitting...".format( args.year ) )
  quit()
if args.x1 not in list( cuts.keys() ):
  print( "[ERR] {} not a valid option, quitting...".format( args.x1 ) )
  print( ">> Choose from: {}".format( list( cuts.keys() ) ) )
  quit()
if args.minDR:
  print( ">> Using minDR(lep,jet) > 0.4 veto" )

sys.argv = []

import ROOT
import config

bins = len( cuts[ args.x1 ].tolist() )

json_data = {
  "CUT": args.x1,
  "MINDR": args.minDR,
  "YEAR": args.year,
  "PLOT_BASIC": {
    args.x1: cuts[ args.x1 ].tolist(),
    "TTT": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(),
    "TTTT": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(),
    "TTBAR": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy()
  },
  "PLOT_LEP": {
    args.x1: cuts[ args.x1 ].tolist(),
    "TTT(e)": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(), "TTT(m)": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(),
    "TTTT(e)": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(), "TTTT(m)": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(),
    "TTBAR(e)": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(), "TTBAR(m)": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy()
  },
  "PLOT_TTXX": {
    args.x1: cuts[ args.x1 ].tolist(),
    "TTT": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(),
    "TTTT": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(),
    "TTJJ": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(),
    "TTCC": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(),
    "TTBB": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(),
    "TT1B": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(),
    "TT2B": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy()
  },
  "PLOT_SAMPLE": {
    args.x1: cuts[ args.x1 ].tolist(),
    "TTTW": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(),
    "TTTJ": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(),
    "TTTT": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(),
    "TTToHadronic": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(),
    "TTToSemiLeptonic_HT0Njet0": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(),
    "TTToSemiLeptonic_HT500Njet9": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(),
    "TTToSemiLepton_HT500Njet9": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy(),
    "TTTo2L2Nu": { "PASS": np.zeros( bins ).tolist(), "TOTAL": np.zeros( bins ).tolist() }.copy()
  }
}

base_cut =  "DataPastTriggerX == 1 && MCPastTriggerX == 1 && ( isElectron == 1 || isMuon == 1 )"
if args.minDR:
  base_cut += " && minDR_lepJet > 0.4 "

def get_RDF( path, cut ):
  rDF = ROOT.RDataFrame( "ljmet", path ).Filter( cut )
  rDF_e = rDF.Filter( "isElectron == 1" )
  rDF_m = rDF.Filter( "isMuon == 1" )
  return rDF, rDF_e, rDF_m

def apply_selection( rDF, rDF_e, rDF_m, value ):
  rDF_cut = rDF.Filter( "{} > {}".format( args.x1, value ) )
  rDF_e_cut = rDF_e.Filter( "{} > {}".format( args.x1, value ) )
  rDF_m_cut = rDF_m.Filter( "{} > {}".format( args.x1, value ) )
  return rDF_cut, rDF_e_cut, rDF_m_cut

for sample in config.sig_training[ args.year ]:
  sample_path = config.step2DirLPC[ args.year ] + "/nominal/" + sample
  print( ">> Analyzing signal sample: {}".format( sample ) )
  rDF, rDF_e, rDF_m = get_RDF( sample_path, base_cut )
  rDF_count = int( rDF.Count().GetValue() )
  rDF_e_count = int( rDF_e.Count().GetValue() )
  rDF_m_count = int( rDF_m.Count().GetValue() )
  for i, value in enumerate( cuts[ args.x1 ] ):
    rDF_cut, rDF_e_cut, rDF_m_cut = apply_selection( rDF, rDF_e, rDF_m, value )
    rDF_cut_count = int( rDF_cut.Count().GetValue() )
    rDF_e_cut_count = int( rDF_e_cut.Count().GetValue() )
    rDF_m_cut_count = int( rDF_m_cut.Count().GetValue() )
    selection = 100. * float( rDF_cut_count ) / float( rDF_count )
    e_selection = 100. * float( rDF_e_cut_count ) / float( rDF_e_count )
    m_selection = 100. * float( rDF_m_cut_count ) / float( rDF_m_count )
    if args.verbose: print( "   >> {} > {}: (electron) {}/{} = {:.2f}%, (muon) {}/{} = {:.2f}%".format( 
      args.x1, value, 
      rDF_e_cut_count, rDF_e_count, e_selection,
      rDF_m_cut_count, rDF_m_count, m_selection
    ) )
    json_data[ "PLOT_BASIC" ][ "TTT" ][ "TOTAL" ][i] += int( rDF_count )
    json_data[ "PLOT_BASIC" ][ "TTT" ][ "PASS"  ][i] += int( rDF_cut_count )
    json_data[ "PLOT_TTXX"  ][ "TTT" ][ "TOTAL" ][i] += int( rDF_count )
    json_data[ "PLOT_TTXX"  ][ "TTT" ][ "PASS"  ][i] += int( rDF_cut_count )
    json_data[ "PLOT_LEP"   ][ "TTT(e)" ][ "TOTAL" ][i] += int( rDF_e_count )
    json_data[ "PLOT_LEP"   ][ "TTT(e)" ][ "PASS"  ][i] += int( rDF_e_cut_count )
    json_data[ "PLOT_LEP"   ][ "TTT(m)" ][ "TOTAL" ][i] += int( rDF_m_count )
    json_data[ "PLOT_LEP"   ][ "TTT(m)" ][ "PASS"  ][i] += int( rDF_m_cut_count )
    if "TTTW" in sample:
      json_data[ "PLOT_SAMPLE" ][ "TTTW" ][ "TOTAL" ][i] += int( rDF_count )
      json_data[ "PLOT_SAMPLE" ][ "TTTW" ][ "PASS"  ][i] += int( rDF_cut_count )
    if "TTTJ" in sample:
      json_data[ "PLOT_SAMPLE" ][ "TTTJ" ][ "TOTAL" ][i] += int( rDF_count )
      json_data[ "PLOT_SAMPLE" ][ "TTTJ" ][ "PASS"  ][i] += int( rDF_cut_count )    

print( "[OK ] Signal acceptance:" )
for i in range( len( json_data[ "PLOT_BASIC" ][ "TTT" ][ "TOTAL" ] ) ):
  selection = 100. * json_data[ "PLOT_BASIC" ][ "TTT" ][ "PASS" ][i] / json_data[ "PLOT_BASIC" ][ "TTT" ][ "TOTAL" ][i]
  print( ">> {} > {}: {}/{} = {:.2f}%".format( 
    args.x1, json_data[ "PLOT_BASIC" ][ args.x1 ][i], 
    int( json_data[ "PLOT_BASIC" ][ "TTT" ][ "PASS" ][i] ), int( json_data[ "PLOT_BASIC" ][ "TTT" ][ "TOTAL" ][i] ),
    selection
  ) )

for sample in config.bkg_training[ args.year ]:
  sample_path = config.step2DirLPC[ args.year ] + "/nominal/" + sample
  print( ">> Analyzing background sample: {}".format( sample ) )
  rDF, rDF_e, rDF_m = get_RDF( sample_path, base_cut )
  rDF_count = int( rDF.Count().GetValue() )
  rDF_e_count = int( rDF_e.Count().GetValue() )
  rDF_m_count = int( rDF_m.Count().GetValue() )
  for i, value in enumerate( cuts[ args.x1 ] ):
    rDF_cut, rDF_e_cut, rDF_m_cut = apply_selection( rDF, rDF_e, rDF_m, value )
    rDF_cut_count = int( rDF_cut.Count().GetValue() )
    rDF_e_cut_count = int( rDF_e_cut.Count().GetValue() )
    rDF_m_cut_count = int( rDF_m_cut.Count().GetValue() )
    selection = 100. * float( rDF_cut_count ) / float( rDF_count )
    e_selection = 100. * float( rDF_e_cut_count ) / float( rDF_e_count )
    m_selection = 100. * float( rDF_m_cut_count ) / float( rDF_m_count )
    if args.verbose: print( "   >> {} > {}: (electron) {}/{} = {:.2f}%, (muon) {}/{} = {:.2f}%".format( 
      args.x1, value, 
      rDF_e_cut_count, rDF_e_count, e_selection,
      rDF_m_cut_count, rDF_m_count, m_selection
    ) )
    if "TTTT" in sample:
      json_data[ "PLOT_BASIC" ][ "TTTT" ][ "TOTAL" ][i] += int( rDF_count )
      json_data[ "PLOT_BASIC" ][ "TTTT" ][ "PASS"  ][i] += int( rDF_cut_count )
      json_data[ "PLOT_LEP"   ][ "TTTT(e)" ][ "TOTAL" ][i] += int( rDF_e_count )
      json_data[ "PLOT_LEP"   ][ "TTTT(e)" ][ "PASS"  ][i] += int( rDF_e_cut_count )
      json_data[ "PLOT_LEP"   ][ "TTTT(m)" ][ "TOTAL" ][i] += int( rDF_m_count )
      json_data[ "PLOT_LEP"   ][ "TTTT(m)" ][ "PASS"  ][i] += int( rDF_m_cut_count )
      json_data[ "PLOT_TTXX"  ][ "TTTT" ][ "TOTAL" ][i] += int( rDF_count )
      json_data[ "PLOT_TTXX"  ][ "TTTT" ][ "PASS"  ][i] += int( rDF_cut_count )    
      json_data[ "PLOT_SAMPLE" ][ "TTTT" ][ "TOTAL" ][i] += int( rDF_count )
      json_data[ "PLOT_SAMPLE" ][ "TTTT" ][ "PASS"  ][i] += int( rDF_cut_count )
    if "TTTo" in sample:
      json_data[ "PLOT_BASIC" ][ "TTBAR" ][ "TOTAL" ][i] += int( rDF_count )
      json_data[ "PLOT_BASIC" ][ "TTBAR" ][ "PASS"  ][i] += int( rDF_cut_count )
      json_data[ "PLOT_LEP" ][ "TTBAR(e)" ][ "TOTAL" ][i] += int( rDF_e_count )
      json_data[ "PLOT_LEP" ][ "TTBAR(e)" ][ "PASS"  ][i] += int( rDF_e_cut_count )
      json_data[ "PLOT_LEP" ][ "TTBAR(m)" ][ "TOTAL" ][i] += int( rDF_m_count )
      json_data[ "PLOT_LEP" ][ "TTBAR(m)" ][ "PASS"  ][i] += int( rDF_m_cut_count )
      for ttxx in [ "TTJJ", "TTCC", "TTBB", "TT1B", "TT2B" ]:
        if ttxx.lower() in sample:
          json_data[ "PLOT_TTXX" ][ ttxx ][ "TOTAL" ][i] += int( rDF_count )
          json_data[ "PLOT_TTXX" ][ ttxx ][ "PASS"  ][i] += int( rDF_cut_count )
      for ttbar in [ "TTToHadronic", "TTToSemiLepton_HT500Njet9", "TTTo2L2Nu" ]:
        if ttbar in sample:
          json_data[ "PLOT_SAMPLE" ][ ttbar ][ "TOTAL" ][i] += int( rDF_count )
          json_data[ "PLOT_SAMPLE" ][ ttbar ][ "PASS"  ][i] += int( rDF_cut_count )
      if "TTToSemiLeptonic" in sample:
        if "HT0Njet0" in sample:
          json_data[ "PLOT_SAMPLE" ][ "TTToSemiLeptonic_HT0Njet0" ][ "TOTAL" ][i] += int( rDF_count )
          json_data[ "PLOT_SAMPLE" ][ "TTToSemiLeptonic_HT0Njet0" ][ "PASS"  ][i] += int( rDF_cut_count )
        if "HT500Njet9" in sample:
          json_data[ "PLOT_SAMPLE" ][ "TTToSemiLeptonic_HT500Njet9" ][ "TOTAL" ][i] += int( rDF_count )
          json_data[ "PLOT_SAMPLE" ][ "TTToSemiLeptonic_HT500Njet9" ][ "PASS"  ][i] += int( rDF_cut_count )

print( "[OK ] TTTT acceptance:" )
for i in range( len( json_data[ "PLOT_BASIC" ][ "TTTT" ][ "TOTAL" ] ) ):
  if json_data[ "PLOT_BASIC" ][ "TTTT" ][ "TOTAL" ][i] != 0:
    selection = 100. * json_data[ "PLOT_BASIC" ][ "TTTT" ][ "PASS" ][i] / json_data[ "PLOT_BASIC" ][ "TTTT" ][ "TOTAL" ][i]
    print( ">> {} > {}: {}/{} = {:.2f}%".format( 
      args.x1, json_data[ "PLOT_BASIC" ][ args.x1 ][i], 
      int( json_data[ "PLOT_BASIC" ][ "TTTT" ][ "PASS" ][i] ), int( json_data[ "PLOT_BASIC" ][ "TTTT" ][ "TOTAL" ][i] ),
      selection
    ) )
  else: print( "[WARN] {} > {}: No events found".format( args.x1, json_data[ "PLOT_BASIC" ][ args.x1 ][i] ) )

print( "[OK ] TTBar acceptance:" )
for i in range( len( json_data[ "PLOT_BASIC" ][ "TTBAR" ][ "TOTAL" ] ) ):
  if json_data[ "PLOT_BASIC" ][ "TTBAR" ][ "TOTAL" ][i] != 0:
    selection = 100. * json_data[ "PLOT_BASIC" ][ "TTBAR" ][ "PASS" ][i] / json_data[ "PLOT_BASIC" ][ "TTBAR" ][ "TOTAL" ][i]
    print( ">> {} > {}: {}/{} = {:.2f}%".format( 
      args.x1, json_data[ "PLOT_BASIC" ][ args.x1 ][i], 
      int( json_data[ "PLOT_BASIC" ][ "TTBAR" ][ "PASS" ][i] ), int( json_data[ "PLOT_BASIC" ][ "TTBAR" ][ "TOTAL" ][i] ),
      selection
    ) )
  else: print( "[WARN] {} > {}: No events found".format( args.x1, json_data[ "PLOT_BASIC" ][ args.x1 ][i] ) )

save_name = "event_selection_{}".format( args.x1 )
if args.minDR: save_name += "_minDR"
save_name += "_{}.json".format( args.year )

with open( save_name, "w" ) as f:
  f.write( write_json( json_data, indent = 2 ) )
print( "[OK ] Finished writing results to {}".format( save_name ) )
