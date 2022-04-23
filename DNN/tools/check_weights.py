import ROOT
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument( "-y", "--year", default = "17" )
parser.add_argument( "-f", "--file" )
args = parser.parse_args()

rFile = ROOT.TFile.Open( "root://cmsxrootd.fnal.gov//store/user/dsunyou/FWLJMET106XUL_1lep20{}_3t_deepJetV1_step2/nominal/{}".format( args.year, args.file ) )

rTree = rFile.Get( "ljmet" )

vars_to_check = [
  "triggerXSF", "pileupWeight", "lepIdSF", "EGammaGsfSF", "isoSF", "L1NonPrefiringProb_CommonCalc",
  "MCWeight_MultiLepCalc", "xsecEff", "tthfWeight", "btagDeepJetWeight", "btagDeepJet2DWeight_HTnj"
]

for i in range(10):
  rTree.GetEntry(i)
  print( ">> Event {}".format( i ) )
  for var in vars_to_check:
    print( "  - {}: {}".format( var, getattr( rTree, var ) ) )
  
