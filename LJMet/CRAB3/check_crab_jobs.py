import os, argparse, imp

parser = argparse.ArgumentParser()
parser.add_argument( "-f", "--folder", required = True )
parser.add_argument( "-y", "--year", required = True )
parser.add_argument( "-r", "--resubmit", action = "store_true" )
parser.add_argument( "-k", "--kill", action = "store_true" )
parser.add_argument( "-g", "--group", required = True )
parser.add_argument( "-s", "--systematics", action = "store_true" )
parser.add_argument( "-v", "--verbose", action = "store_true" )
args = parser.parse_args()

if args.year not in [ "16", "17", "18" ]: sys.exit( "[ERR] Invalid year option. Use: 16, 17, 18." )
if not os.path.exists( args.folder ): sys.exit( "[ERR] {} is not a valid condor directory.".format( args.folder ) )
if args.group not in [ "ALL", "TEST", "DATA", "SIGNAL", "TTBAR", "TOP", "EWK", "EWKHT", "QCDHT" ]: sys.exit( "[ERR] {} is an invalid group.".format( args.group ) )

samples = imp.load_source( "Samples", "sampleUL{}.py".format( args.year ), open( "sampleUL{}.py".format( args.year ), "r" ) )

def check_crab_jobs( group, samples_dict ):
  for sample in samples_dict[ group ]:
    if not args.systematics and ( "up" in sample.lower() or "dn" in sample.lower() ): continue
    if args.resubmit:
      print( ">> Resubmitting {}: {}".format( group, sample ) )
      os.system( "crab resubmit {}".format( os.path.join( args.folder, "crab_UL{}_{}".format( args.year, sample ) ) ) )
    elif args.kill:
      print( ">> Killing {}: {}".format( group, sample ) )
      os.system( "crab kill {}".format( os.path.join( args.folder, "crab_UL{}_{}".format( args.year, sample ) ) ) )
    else:
      print( ">> Checking {}: {}".format( group, sample ) )
      if args.verbose: os.system( "crab status --verboseErrors {}".format( os.path.join( args.folder, "crab_UL{}_{}".format( args.year, sample ) ) ) )
      else: os.system( "crab status {}".format( os.path.join( args.folder, "crab_UL{}_{}".format( args.year, sample ) ) ) )

if __name__ == "__main__":
  if args.group == "ALL":
    for group in [ "TEST", "DATA", "SIGNAL", "TTBAR", "TOP", "EWK", "EWKHT", "QCDHT" ]:
      check_crab_jobs( group, samples.groups )
  else:
    check_crab_jobs( args.group, samples.groups )
