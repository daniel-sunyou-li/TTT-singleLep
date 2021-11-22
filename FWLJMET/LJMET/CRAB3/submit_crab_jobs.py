import os, sys, argparse, imp

parser = argparse.ArgumentParser()
parser.add_argument( "-y", "--year", action = "store", help = "Options = [16, 16APV, 17, 18]" )
parser.add_argument( "-t", "--test", action = "store_true" )
args = parser.parse_args()

if args.test:
  print( ">> [OPT] Submitting test job..." )

if args.year not in [ "16", "16APV", "17", "18" ]: 
  sys.exit( "[ERR] Invalid --year option used, choose from: [ 16, 16APV, 17, 18 ]. Exiting..." )
  
sampleListPath = "sampleUL{}.py".format( args.year )
samples = imp.load_source( "Sample", sampleListPath, open( sampleListPath, "r" ) )

crabConfigDir = os.path.join( os.getcwd(), "/crabConfigs{}/".format( args.year ) )

def submit_crab_jobs( group, sample_dict ):

	for dataset in sample_dict[ group ]:

		print( ">> Submitting from {}: {}".format( group, dataset ) )

		crabConfig = os.path.join( crabConfigDir, "crab_config_{}.py".format( dataset ) )

		os.system( "echo crab submit {}".format( crabConfig ) )
		os.system( "crab submit {}".format( crabConfig ) )


if __name__ == '__main__':
  if args.test:
    submit_crab_jobs( "TEST",   samples.groups )
  else:
    submit_crab_jobs( "QCD",    sample.groups )
    submit_crab_jobs( "EWK",    sample.groups )
    submit_crab_jobs( "EWKHT",  sample.groups )
    submit_crab_jobs( "TOP",    sample.groups )
    submit_crab_jobs( "TTBAR",  sample.groups )
    submit_crab_jobs( "SIGNAL", sample.groups )
    submit_crab_jobs( "DATA",   sample.groups )
