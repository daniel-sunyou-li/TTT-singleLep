from DataFormats.FWLite import Handle, Events
from argparse import ArgumentParser
import numpy as np

parser = ArgumentParser()
parser.add_argument( "-y", "--year", required = True, help = "16APV,16,17,18" )
parser.add_argument( "-n", "--nEvents", default = -1, help = "Max number of events to run on (default = -1)" )
parser.add_argument( "--deepJet", action = "store_true" )
args = parser.parse()

class Efficiency():
  def __init__( self, year, max_events config ):
    self.year = year
    self.max_events = max_events
    self.events = Events( config[ self.year ][ "SAMPLE" ] )
    self.pt_space = config[ "PT SPACE" ]
    self.eta_space = config[ "ETA SPACE" ]
    self.taggers = []
    self.handles = {}
    self.collection = {}
    self.wp = {}
    self.discriminator = {}
    self.tag = {}
    self.true = {}
    self.efficiency = {}
    
  def get_index( self, pt, eta ):
    
    
  def add_deepJet_b( self ):
    print( "[INFO] Adding efficiency calculation for: deepJet (b)" )
    self.taggers.append( "deepJet b" )
    self.handles[ "deepJet b" ] = Handle( "std::vector<pat::Jet>" )
    self.collection[ "deepJet b" ] = "slimmedJets"
    self.wp[ "deepJet b" ] = config[ "deepJet b" ][ self.year ] 
    self.discriminator[ "deepJet b" ] = [ 
      "pfDeepFlavourJetTags:probb",
      "pfDeepFlavourJetTags:probbb",
      "pfDeepFlavourJetTags:problepb"
    ]
    
  def eval_deepJet_b( self, pt, eta, bdisc, id ):
    i_pt, i_eta = self.get_index( pt, eta )
    disc_val = 0
    for prob in self.discriminator[ "deepJet b" ]:
      disc_val += bdisc[ prob ]
    for wp in self.wp[ "deepJet b" ]:
      if disc_val > self.wp[ "deepJet b" ][ wp ]:
        self.tag[ "deepJet b" ][ wp ][ i_pt, i_eta ] += 1
    if abs( id ) == 5:
      self.true[ "deepJet b" ][ i_pt, i_eta ] += 1
    
  def add_deepCSV_b( self ):
    self.taggers.append( "deepCSV" )
    self.handles[ "deepCSV" ] = Handle( "std::vector<pat::Jet>" )
    self.collection[ "deepCSV" ] = "slimmedJets"
    self.wp[ "deepCSV" ] = config[ "deepCSV" ][ self.year ]
    self.discriminator[ "deepCSV" ] = [
      "pfDeepCSVJetTags:probb",
      "pfDeepCSVJetTags:probbb"
    ]
    
  def eval_deepCSV( self, pt, eta, bdisc, id ):
    i_pt, i_eta = self.get_index( pt, eta )
    disc_val = 0
    for prob in self.discriminator[ "deepCSV b" ]:
      disc_val += bdisc[ prob ]
    for wp in self.wp[ "deepCSV b" ]:
      if disc_val > self.wp[ "deepCSV b" ][ wp ]:
        self.tag[ "deepCSV b" ][ wp ][ i_pt, i_eta ] += 1
    if abs( id ) == 5:
      self.true[ "deepCSV b" ][ i_pt, i_eta ] += 1
    
  def format_data( self ):
    print( "[START] Initializing containers for results" )
    print( "[INFO] Containers have dimension: ({},{})".format( len( self.pt_range ), len( self.eta_range ) ) )
    for tagger in self.taggers:
      print( "   + {}".format( tagger ) )
      self.tag[ tagger ] = {
        wp: np.zeros( ( len( self.pt_range ), len( self.eta_range ) ) ) for wp in self.wp[ tagger ]
      }
      self.efficiency[ tagger ] = {
        wp: None for wp in self.wp[ tagger ] 
      }
      self.true[ tagger ] = np.zeros( ( len( self.pt_range ) + 1, len( self.eta_range ) + 1 ) )
    print( "[DONE]" )
    
  def event_loop():
    print( "[START] Looping through events and calculating efficiencies" )
    for i, event in self.events:
      if i == self.max_events: 
        print( "[WARN] Stopping at {} events."format( i + 1 ) )
        break
      for tagger in self.taggers:
        event.getByLabel( self.collection[ tagger ], self.handles[ tagger ] )
        for jet in self.handles[ tagger ].product():
          if jet.pt() < min( self.pt_space ) or abs( jet.eta() ) > max( self.eta_space ): continue
          if tagger == "deepJet b": eval_deepJet_b( jet.pt(), jet.eta(), jet.bDiscriminator(), jet.partonFlavour() )
          if tagger == "deepCSV b": eval_deepCSV_b( jet.pt(), jet.eta(), jet.bDiscriminator(), jet.partonFlavour() )
    print( "[DONE]" )
  
  def calculate_efficiency( self ):
    print( "[START] Calculating tagger efficiencies" )
    count = 0
    for tagger in self.taggers:
      print( ">> Tagger: {}".format( tagger ) )
      for wp in self.wp[ tagger ]:
        self.efficiency[ tagger ][ wp ] = self.tag[ tagger ][ wp ] / self.true[ tagger ]
        print( "   + {}".format( wp ) )
        count += 1
    print( "[DONE] {} efficiency matrices calculated".format( count ) )
    
  def print_efficiency( self );
    print( "[START] Printing efficiency tables" )
    for tagger in self.taggers:
      for wp in self.wp[ tagger ]:
        print( ">> {}: {}".format( tagger, wp ) )
        print( "(x,y) = (eta,pt) |" ),
        for i_eta in range( len( self.eta_range ) - 1 ):
          print( " {:>8}-{:<6} |".format( self.eta_range[ i_eta ], self.eta_range[ i_eta + 1 ] ) ),
        for i_pt in range( len( self.pt_range ) - 1 ):
          print( "{:>8}-{:<7}
        
    
    
    
    
    
