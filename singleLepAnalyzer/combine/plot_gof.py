import ROOT
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import mplhep as hep

parser = ArgumentParser()
parser.add_argument( "-d", "--data", required = True )
parser.add_argument( "-t", "--toys", required = True )
parser.add_argument( "-g", "--gof", required = True )
parser.add_argument( "-y", "--era", required = True )
args = parser.parse_args()

plt.style.use( hep.style.CMS )

rFile_d = ROOT.TFile( args.data )
rTree_d = rFile_d.Get( "limit" )
rTree_d.GetEntry(0)
gof_d = getattr( rTree_d, "limit" )

rFile_t = ROOT.TFile( args.toys )
rTree_t = rFile_t.Get( "limit" )
gof_t = []
for i in range( int( rTree_t.GetEntries() ) ):
  rTree_t.GetEntry(i)
  gof_t.append( getattr( rTree_t, "limit" ) )

plt.figure()
hep.cmstext( "Work in Progress" )
hep.lumitext( "{} (13 TeV)".format( args.era ) )
plt.hist( gof_t, bins = 21, label = "MC Toys" )
plt.vline( gof_d, 0, 100, label = "Obs." )
plt.xlabel( args.gof )
plt.ylabel( "Count" )
plt.legend( loc = "best" )
plt.show()
plt.savefig( "gof_{}.png".format( args.gof ) )
plt.close()
