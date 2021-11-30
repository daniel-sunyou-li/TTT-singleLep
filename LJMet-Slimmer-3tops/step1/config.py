lpcUserName = "dsunyou"

inputDir = {
  year: "/eos/uscms/store/user/{}/FWLJMET106XUL_1lep{}_3t/".format( lpcUserName, year ) for year in ["2016","2017","2018"]
}

outputPath = "/eos/uscms/store/user/{}/".format( lpcUserName )
outDir = "/eos/uscms/"

condorPath = "/uscms_data/home/{}/nobackup/TTT-singleLep/CMSSW_10_6_19/src/TTT-singleLep/LJMet-Slimmer-3tops/step1/".format( userName )
                                                             
