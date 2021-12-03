import os, sys, argparse, imp

parser = argparse.ArgumentParser()
parser.add_argument( "-y", "--year", action = "store", help = "Options = [16, 16APV, 17, 18]" )
parser.add_argument( "-c", "--configDir", required = True )
parser.add_argument( "-g", "--group", default = "TEST" ) 
args = parser.parse_args()

if args.group not in [ "TEST", "ALL", "SIGNAL", "DATA", "QCD", "EWK", "EWKHT", "TOP", "TTBAR" ]:
  sys.exit( "[ERR] {} is an invalid group.".format( args.group ) )
else:
  print( ">> Submitting {} job(s)...".format( args.group ) )

if args.year not in [ "16", "16APV", "17", "18" ]: 
  sys.exit( "[ERR] Invalid --year option used, choose from: [ 16, 16APV, 17, 18 ]. Exiting..." )
  
sampleListPath = "sampleUL{}.py".format( args.year )
samples = imp.load_source( "Sample", sampleListPath, open( sampleListPath, "r" ) )

crabConfigDir = args.configDir

def submit_crab_jobs( group, sample_dict ):
  for dataset in sample_dict[ group ]:
    print( ">> Submitting from {}: {}".format( group, dataset ) )
    crabConfig = os.path.join( crabConfigDir, "config_{}.py".format( dataset ) )

    os.system( "echo crab submit {}".format( crabConfig ) )
    os.system( "crab submit {}".format( crabConfig ) )


if __name__ == '__main__':
  if args.group == "ALL":
    for group in [ "SIGNAL", "DATA", "QCD", "EWK", "EWKHT", "TOP", "TTBAR" ]:
      submit_crab_jobs( group, samples.groups )
  else:
    submit_crab_jobs( args.group, samples.groups )
