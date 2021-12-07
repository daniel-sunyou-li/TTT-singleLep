eosUserName = "dali"
postfix = "test"

inputPath = {
  year: "/eos/uscms/store/user/{}/FWLJMET106XUL_1lep20{}_3t_{}_step1hadds".format( eosUserName, year, postfix ) for year in [ "16", "17", "18" ]
}

outputPath = {
  year: "/eos/uscms/store/user/{}/FWLJMET106XUL_1lep20{}_3t_{}_step2".format( eosUserName, year, postfix ) for year in [ "16", "17", "18" ]
}

outputPath = "/store/user/{}/".format( eosUserName )
