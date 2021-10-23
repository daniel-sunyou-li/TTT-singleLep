# updated 10/23 by Daniel Li
import numpy as np
from argparse import ArgumentParser

# import custom methods
import config

nTrans = len( [ var for var in config.variables if config.variables[ var ][ "transform" ] == True )

parser = ArgumentParser()
parser.add_argument( "-s", "--source", required = True )
parser.add_argument( "-t", "--target", required = True )
parser.add_arugment( "-v", "--verbose", store_action = True )
