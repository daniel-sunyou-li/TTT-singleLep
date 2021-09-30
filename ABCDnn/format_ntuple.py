# this script takes an existing step3 ROOT file and formats it for use in the ABCDnn training script
# last modified September 29, 2021 by Daniel Li

import ROOT
from array import array
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument( "-y", "--year", default = "2017", help = "Year for sample" )
parser.add_argument( "-f", "--finalstate", required = True, help = "Final state of ttbar [Hadronic,Semilep,2L2nu]" )
parser.add_argument( "-sI", "--sIn", nargs = "*", default = [], help = "Source ROOT files to consolidate into one file" )
parser.add_argument( "-tI", "--tIn", nargs = "*", default = [], help = "Target ROOT files to consolidate into one file" )
parser.add_argument( "-sO", "--sOut", default = "source_ttbar", help = "Output name of source ROOT file" )
parser.add_argument( "-tO", "--tOut", default = "target_data", help = "Output name of target ROOT file" )
parser.add_argument( "-v", "--variables", nargs = "+", default = [ "AK4HT", "DNN" ], help = "Variables to transform" )
parser.add_argument( "-p", "--pEvents", default = 100, help = "Percent of events (0 to 100) to include from each file." )
args = parser.parse_args()

# some params to consider editing --> need to check this (09/29)
ttbar_xsec = 831.76
target_lumi = {
  "2016": 1.,
  "2017": 41530.,
  "2018": 1.
}
BR = {
  "Hadronic": 0.457,
  "Semilep": 0.438,
  "2L2nu": 0.105
}
num_MC = {
  "2016": 1,
  "2017": 109124472,
  "2018": 1
}

weight_ttbar = ttbar_xsec * target_lumi[ args.year ] * BR[ args.finalstate ] / num_MC[ args.year ]

class ToyTree:
  def __init__( self, name, trans_var ):
    # trans_var is transforming variables
    self.name = name
    self.rFile = ROOT.TFile( "{}.root".format( name ), "RECREATE" )
    self.rTree = ROOT.TTree( "Events", name )
    self.variables = { # variables that are used regardless of the transformation variables
      "NJets_JetSubCalc": { "ARRAY": array( "i", [0] ), "STRING": "NJets_JetSubCalc/I" },
      "NJetsCSV_MultiLepCalc": { "ARRAY": array( "i", [0] ), "STRING": "NJetsCSV_MultiLepCalc/I" },
      "xsecWeight": { "ARRAY": array( "f", [0] ), "STRING": "xsecWeight/F" }
    }
    
    for variable in trans_var:
      self.variables[ variable ] = { "ARRAY": array( "f", [0] ), "STRING": "{}/F".format( variable ) }
    
    self.selection = { # edit these accordingly
      "NJets_JetSubCalc": { "VALUE": 4, "CONDITION": [ ">=" ] },
      "NJetsCSV_MultiLepCalc": { "VALUE": 2, "CONDITION": [ ">=" ] },
      "corr_met_MultiLepCalc": { "VALUE": 30, "CONDITION": [ ">" ] },
      "MT_lepMet": { "VALUE": 0, "CONDITION": [ ">" ] },
      "minDR_lepJet": { "VALUE": 0.4, "CONDITION": [ ">" ] },
      "AK4HT": { "VALUE": 350, "CONDITION": [ ">" ] },
      "DataPastTriggerX": { "VALUE": 1, "CONDITION": [ "==" ] },
      "MCPastTriggerX": { "VALUE": 1, "CONDITION": [ "==" ] },
      "isTraining": { "VALUE": 3, "CONDITION": [ "==" ] }
    }
    
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
      
def format_ntuple( output, inputs, trans_var, weight = None ):
  ntuple = ToyTree( output, trans_var )
  for input in inputs:
    print( ">> Processing {}".format( input ) )
    rFile_in = ROOT.TFile.Open( "{}".format( input ) )
    rTree_in = rFile_in.Get( "ljmet" )
    branches_in = [ branch.GetName() for branch in rTree_in.GetListOfBranches() ]
    n_stop = int ( rTree_in.GetEntries() * float( args.pEvents ) / 100. )
    n_pass = 0
    for i in range( rTree_in.GetEntries() ):
      if n_pass >= n_stop: continue
      rTree_in.GetEntry(i)
      
      for variable in ntuple.selection: # apply the selection cut
        value = getattr( rTree_in, str( variable ) )
        if ntuple.selection[ variable ][ "CONDITION" ] == ">=":
          if value < ntuple.selection[ variable ][ "VALUE" ]: continue
        elif ntuple.selection[ variable ][ "CONDITION" ] == ">":
          if value <= ntuple.selection[ variable ][ "VALUE" ]: continue
        elif ntuple.selection[ variable ][ "CONDITION" ] == "<=":
          if value > ntuple.selection[ variable ][ "VALUE" ]: continue
        elif ntuple.selection[ variable ][ "CONDITION" ] == "<":
          if value >= ntuple.selection[ variable ][ "VALUE" ]: continue
        else:
          if value != ntuple.selection[ variable ][ "VALUE" ]: continue
          
      n_pass += 1
      
      event_data = {}
      for variable in ntuple.variables:
        if str( variable ) != "xsecWeight":
          if variable not in branches_in: 
            if i == 0: print( "[WARN] {} is not a valid branch in {}.root, skipping..." )
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

    print( ">> {} events from {}".format( n_stop, input ) )
    rFile_in.Close()
  ntuple.Write()
  
format_ntuple( inputs = args.sIn, output = args.sOut + "_mc" , weight = weight_ttbar, trans_var = args.variables )
format_ntuple( inputs = args.tIn, output = args.tOut + "_data" , weight = None, trans_var = args.variables )

                                                                                                  
