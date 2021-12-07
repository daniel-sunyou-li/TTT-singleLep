import ROOT
import sys, os
import numpy as np
import argparse
import array
from ROOT import TFile, TTree

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="", help="The path to the analysis tree")
parser.add_argument("-l", "--label", default="", help="The name of the output file")
args = parser.parse_args()

if not os.path.exists( "renorm" ): os.system( "mkdir -v renorm" )

tfile = TFile.Open( args.file )
limits = {
  "NJ": [5,4,9],
  "HT": [40,150,4000]
}

fout = ROOT.TFile( "Weights_{}_extended_HT_cuts_sys.root".format( args.label ), "RECREATE" )

systematics = []
for shift in [ "up", "dn" ]:
  for systematic in [ "HF", "LF", "jes", "hfstats1", "hfstats2", "lfstats1dn", "lfstats2", "cferr1", "cferr2" ]:
    systematics.append( systematic + shift )
h2D = { "origin": {}, "weight": {}, "scale": {} }

h2D[ "origin" ][ "nominal" ] = ROOT.TH2F( "h2D_origin", "h2D_origin", limits["NJ"][0], limits["NJ"][1], limits["NJ"][2], limits["HT"][0], limits["HT"][1], limits["HT"][2] )
h2D[ "origin" ][ "nominal" ].Sumw2()
h2D[ "weight" ][ "nominal" ] = ROOT.TH2F( "h2D_weight", "h2D_weight", limits["NJ"][0], limits["NJ"][1], limits["NJ"][2], limits["HT"][0], limits["HT"][1], limits["HT"][2] )
h2D[ "weight" ][ "nominal" ].Sumw2()

# the nominal h2d[ "origin" ] gets cloned for the systematics scales
for systematic in systematics:
  h2D[ "weight" ][ systematic ] = ROOT.TH2F( "h2D_weight_{}".format( systematic ), "h2D_{}".format( systematic ), limits["NJ"][0], limits["NJ"][1], limits["NJ"][2], limits["HT"][0], limits["HT"][1], limits["HT"][2] )
  h2D[ "weight" ][ systematic ].Sumw2()

ttree = tfile = tfile.Get( "ljmet" )

ttree.SetBranchStatus("*", 0)
ttree.SetBranchStatus("NJets_JetSubCalc*", 1)
ttree.SetBranchStatus("theJetPt_JetSubCalc_PtOrdered*", 1)
ttree.SetBranchStatus("AK4HT*", 1)
ttree.SetBranchStatus("btagDeepJetWeight*", 1)
ttree.SetBranchStatus("leptonPt_MultiLepCalc*", 1)
ttree.SetBranchStatus("isElectron*", 1)
ttree.SetBranchStatus("isMuon*", 1)
ttree.SetBranchStatus("corr_met_MultiLepCalc*", 1)
ttree.SetBranchStatus("MCPastTrigger*", 1)

nEvents = ttree.GetEntries()

for i in range( nEvents ):
  ttree.GetEntry(i)
  if not ( ( ttree.leptonPt_MultiLepCalc > 20 and ttree.isElectron) or (ttree.leptonPt_MultiLepCalc > 20 and ttree.isMuon)): continue
  if not (ttree.corr_met_MultiLepCalc > 30): continue
  if not (ttree.MCPastTrigger): continue 
  njet = getattr( ttree, "NJets_JetSubCalc" ) 
  HT = getattr( ttree, "AK4HT" )
  if njet > 8: njet = 8

  h2D[ "origin" ][ "nominal" ].Fill( njet, HT ) # this gets cloned by the other systematics
  h2D[ "weight" ][ "nominal" ].Fill( njet, HT, getattr( ttree, "btagDeepJetWeight" ) )

  for systematic in systematics:
    h2D[ "weight" ][ systematic ].Fill( njet, HT, getattr( ttree, "btagDeepJetWeight_{}".format( systematic ) ) )

  if i in np.linspace( 0, nEvents, 11 ): print( ">> Finished processing {}% ({}/{}) events".format( float( i / nEvents ), i, nEvents ) )

h2D[ "scale" ][ "nominal" ] = h2D[ "origin" ][ "nominal" ].Clone()
h2D[ "scale" ][ "nominal" ].SetTitle( "h2D_scale" )
fout.WriteTObject( h2D[ "origin" ][ "nominal" ], "h2D_origin" )
fout.WriteTObject( h2D[ "weight" ][ "nominal" ], "h2D_weight" )
fout.WriteTObject( h2D[ "scale" ][ "nominal" ], "h2D_scale" )

for systematic in systematics:
  h2D[ "scale" ][ systematic ] = h2D[ "origin" ][ "nominal" ].Clone()
  h2D[ "scale" ][ systematic ].SetTitle( "h2D_scale_{}".format( systematic ) ) 
  h2D[ "scale" ][ systematic ].Divide( h2D[ "weight" ][ systematic ] )
  fout.WriteTObject( h2D[ "scale" ][ systematic ], "h2D_scale_{}".format( systematic ) )

fout.Close()
os.system( "mv {} renorm/".format( "Weights_{}_extended_HT_cuts_sys.root".format( args.label ) ) )
