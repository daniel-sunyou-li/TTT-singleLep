# this script takes an existing step3 ROOT file and formats it for use in the ABCDnn training script
# last modified September 29, 2021 by Daniel Li

import ROOT
from array import array

class ToyTree:
  def __init__( self, name, x1, x2 ):
    self.name = name
    self.rFile = ROOT.TFile( "{}.root".format( name ), "RECREATE" )
    self.rTree = ROOT.TTree( "Events", name )
    self.variables = {
      "nJet": array( "i", [0] ),
      "nbJet": array( "i", [0] ),
      "met": array( "f", [0] ),
      
    }
    self.nJet = array( 'i', [0] )
    self.nbJet = array( 'i', [0] )
    self.met = array( 'f', [0] )
    self.bjht = array( 'f', [0] )
    self.sphericity = array( 'f', [0] )
    self.xsecWeight = array( 'f', [0] )
    self.rTree.Branch( "nJet", self.nJet, "nJets/I" )
    self.rTree.Branch( "nbJet", self.nbJet, "nbJets/I" )
    self.rTree.Branch( "met", self.met, "met/F" )
    self.rTree.Branch( "bjht", self.bjht, "bjht/F" )
    self.rTree.Branch( "sphericity", self.sphericity, "sphericity/F" )
    self.rTree.Branch( "xsecWeight", self.xsecWeight, "xsecWeight/F" )
    
  def Fill( self, event_data ):
    self.nJet[0] = event_data[ "nJet" ]
    self.nbJet[0] = event_data[ "nbJet" ]
    self.
    
    
    self.rTree.Fill()
