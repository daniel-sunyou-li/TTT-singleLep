# updated 10/23 by Daniel Li
import numpy as np
from argparse import ArgumentParser

# import custom methods
import config

parser = ArgumentParser()
parser.add_argument( "-s", "--source", default = "", required = False )
parser.add_argument( "-t", "--target", default = "", required = False )
parser.add_argument( "-h", "--hpo", store_action = True )
parser.add_arugment( "-v", "--verbose", store_action = True )
args = parser.parse_args()

if args.source != "": config.params[ "EVENTS" ][ "SOURCE" ] = os.path.join( config.data_path, args.source )
if args.target != "": config.params[ "EVENTS" ][ "TARGET" ] = os.path.join( config.data_path, args.target )

nTrans = len( [ var for var in config.variables if config.variables[ var ][ "transform" ] == True ] )

space = []
if args.hpo:
  for hp in config.hyper[ "OPTIMIZE" ]:
    if config.hyper[ "OPTIMIZE" ][ hp ][ i ] == "CAT": 
      space.append( Categorical( config.hyper[ "OPTIMIZE" ][ hp ][0], name = str(hp) ) ) )
    elif config.hyper[ "OPTIMIZE" ][ hp ][ i ] == "INT":
      space.append( Integer( config.hyper[ "OPTIMIZE" ][ hp ][0][0]
      
               
               
