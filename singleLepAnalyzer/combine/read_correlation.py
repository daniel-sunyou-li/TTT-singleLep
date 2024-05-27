import ROOT
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument( "-f", "--file" )
parser.add_argument( "-b1", "--b1", default = 69 )
parser.add_argument( "-b2", "--b2", default = 70 )
args = parser.parse_args()

rFile = ROOT.TFile( args.file )
rTH2F = rFile.Get( "h_correlation" )
print( rTH2F.GetBinContent( int( args.b1 ), int( args.b2 ) ) )
