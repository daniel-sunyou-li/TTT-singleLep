# this script takes an existing step3 ROOT file and formats it for use in the ABCDnn training script
# last modified September 29, 2021 by Daniel Li

import ROOT
from array import array
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument( "-f", nargs = "*", default = [], help = "ROOT files to consolidate into one file" )
parser.add_argument( "-v", nargs = "+", default = [ "AK4HT", "DNN" ], help = "Variables to transform" )
args = parser.parse_args()

class ToyTree:
  def __init__( self, name, trans_var ):
    # trans_var is transforming variables
    self.name = name
    self.rFile = ROOT.TFile( "{}.root".format( name ), "RECREATE" )
    self.rTree = ROOT.TTree( "Events", name )
    self.variables = {
      "NJets_JetSubCalc": { "ARRAY": array( "i", [0] ), "STRING": "NJets_JetSubCalc/I" },
      "NJetsCSV_MultiLepCalc": { "ARRAY": array( "i", [0] ), "STRING": "NJetsCSV_MultiLepCalc/I" },
      "xsecWeight": { "ARRAY": array( "f", [0] ), "STRING": "xsecWeight/F" }
    }
    self.selection = {
      "NJets_JetSubCalc": {},
      "NJetsCSV_MultiLepCalc": {}
    }
    for variable in trans_var:
      self.variables[ variable ] = { "ARRAY": array( "f", [0] ), "STRING": "{}/F".format( variable ) }
    
    for variable in self.variables:
      self.rTree.Branch( str( variable ), self.variables[ variable ][ "ARRAY" ], self.variables[ variable ][ "STRING" ] )
    
  def Fill( self, event_data ):
    for variable in self.variables:
      self.variables[ variable ][ "ARRAY" ][0] = event_data[ variable ]
    self.rTree.Fill()
  
  def Write( self ):
      print( ">> Writing {} entries to {}.root".format( self.rTree.GetEntries(), self.name ) )
      self.rFile.Write()
      self.rFile.Close()
      
def format_ntuple( output, inputs, selection, weight = None ):
  ntuple = ToyTree( output )
  for input in inputs:
    print( ">> Processing {}".format( input ) )
    rFile_in = ROOT.TFile( "{}.root".format( input ), "READ" )
    rTree_in = rFile_in.Get( "ljmet" )
    branches_in = [ branch.GetName() for branch in rTree_in.GetListOfBranches() ]
    for i in range( rTree_in.GetEntries() ):
      rTree_in.GetEntry(i)
      
      for variable in selection:
        value = getattr( rTree_in, str( variable ) )
        if value < selection[ variable ]: continue
      
      event_data = {}
      for variable in ntuple.variables:
        if str( variable ) != "xsecWeight":
          if variable not in branches_in: 
            if i == 0: print( "[WARN] {} is not a valid branch in {}.root, skipping...")
            continue
            
          event_data[ variable ] = getattr( rTree_in, str( variable ) )
      
      if weight == None:
        event_data[ "xsecWeight" ] = 1
      else:
        event_data[ "xsecWeight" ] = getattr( rTree_in, "triggerXSF" ) * getattr( rTree_in, "pileupWeight" ) * getattr( rTree_in, "lepIdSF" )
        event_data[ "xsecWeight" ] *= getattr( rTree_in, "isoSF" ) * getattr( rTree_in, "L1NonPrefiringProb_CommonCalc" )
        event_data[ "xsecWeight" ] *= getattr( rTree_in, "MCWeight_MultiLepCalc" ) / abs( getattr( rTree_in, "MCWeight_MultiLepCalc" ) )
        event_data[ "xsecWeight" ] *= weight * 3
        
      ntuple.Fill( event_data )
    rFile_in.Close()
  ntuple.Write()
  

                                                                                                  
                                                                                                  
        
      
      

  
