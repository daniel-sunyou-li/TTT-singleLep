#1/usr/bin/env python

#input variables
varList = {}

# EDIT ME
bruxUserName = "dli50"
lpcUserName = "dsunyou"
eosUserName = "dali"
date = "10072020" # production date

step2Sample = {
  "2017": "FWLJMET102X_1lep2017_Oct2019_4t_{}_step2".format( date ),
  "2018": "FWLJMET102X_1lep2018_Oct2019_4t_{}_step2".format( date )
}

step3Sample = {
  "2017": "FWLJMET102X_1lep2017_Oct2019_3t_{}_step3".format( date ),
  "2018": "FWLJMET102X_1lep2018_Oct2019_3t_{}_step3".format( date )
}

step2DirBRUX = {
  "2017": "/mnt/hadoop/store/group/bruxljm/{}/".format( step2Sample[ "2017" ] ),
  "2018": "/mnt/hadoop/store/group/bruxljm/{}/".format( step2Sample[ "2018" ] )
}

step2DirLPC = {
  "2017": "~/nobackup/TTT-singleLep/CMSSW_9_4_6_patch1/src/TTT-singleLep/{}/".format( step2Sample[ "2017" ] ),
  "2018": "~/nobackup/TTT-singleLep/CMSSW_9_4_6_patch1/src/TTT-singleLep/{}/".format( step2Sample[ "2018" ] )
}

step3DirLPC = {
  "2017": "~/nobackup/TTT-singleLep/CMSSW_9_4_6_patch1/src/TTT-singleLep/{}/".format( step3Sample[ "2017" ] ),
  "2018": "~/nobackup/TTT-singleLep/CMSSW_9_4_6_patch1/src/TTT-singleLep/{}/".format( step3Sample[ "2018" ] )
}

step2DirEOS = {
  "2017": "root://cmseos.fnal.gov///store/user/{}/{}/".format( eosUserName, step2Sample[ "2017" ] ),
  "2018": "root://cmseos.fnal.gov///store/user/{}/{}/".format( eosUserName, step2Sample[ "2018" ] )
}

step3DirEOS = {
  "2017": "root://cmseos.fnal.gov///store/user/{}/{}/".format( eosUserName, step3Sample[ "2017" ] ),
  "2018": "root://cmseos.fnal.gov///store/user/{}/{}/".format( eosUserName, step3Sample[ "2018" ] )
}

# signal sample to be used in training
sig_training = {
  "2017": [ 
    "TTTJ_TuneCP5_13TeV-madgraph-pythia8_hadd.root",
    "TTTW_TuneCP5_13TeV-madgraph-pythia8_hadd.root"
  ],
  "2018": [ 
    "TTTJ_TuneCP5_13TeV-madgraph-pythia8_hadd.root",
    "TTTW_TuneCP5_13TeV-madgraph-pythia8_hadd.root"
  ]
}

# background samples to be used in training, only using ttbar events
bkg_training = {
  "2017": [
    "TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_hadd.root",
    "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_HT0Njet0_tt1b_hadd.root",
    "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_HT0Njet0_tt2b_hadd.root",
    "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_HT0Njet0_ttbb_hadd.root",
    "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_HT0Njet0_ttcc_hadd.root",
    "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_HT0Njet0_ttjj_1_hadd.root",
    "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_HT0Njet0_ttjj_2_hadd.root",
    "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_HT0Njet0_ttjj_3_hadd.root",
    "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_HT0Njet0_ttjj_4_hadd.root",
    "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_HT0Njet0_ttjj_5_hadd.root",
    "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_HT500Njet9_tt1b_hadd.root",
    "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_HT500Njet9_tt2b_hadd.root",
    "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_HT500Njet9_ttbb_hadd.root",
    "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_HT500Njet9_ttcc_hadd.root",
    "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_HT500Njet9_ttjj_hadd.root",
    "TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_tt1b_hadd.root",
    "TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_tt2b_hadd.root",
    "TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root",
    "TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_ttcc_hadd.root",
    "TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_ttjj_hadd.root",
    "TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_tt1b_hadd.root",
    "TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_tt2b_hadd.root",
    "TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root",
    "TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_ttcc_hadd.root",
    "TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_ttjj_hadd.root",
    "TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8_tt1b_hadd.root",
    "TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8_tt2b_hadd.root",
    "TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root",
    "TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8_ttcc_hadd.root",
    "TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8_ttjj_hadd.root"  
  ],
  "2018": [
    "TTTT_TuneCP5_13TeV-amcatnlo-pythia8_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_tt1b_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_tt2b_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttbb_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttcc_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_1_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_2_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_tt1b_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_tt2b_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_ttbb_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_ttcc_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_ttjj_hadd.root",
    "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_tt1b_hadd.root",
    "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_tt2b_hadd.root",
    "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_ttbb_hadd.root",
    "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_ttcc_hadd.root",
    "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_ttjj_hadd.root",
    "TTToHadronic_TuneCP5_13TeV-powheg-pythia8_tt1b_hadd.root",
    "TTToHadronic_TuneCP5_13TeV-powheg-pythia8_tt2b_hadd.root",
    "TTToHadronic_TuneCP5_13TeV-powheg-pythia8_ttbb_hadd.root",
    "TTToHadronic_TuneCP5_13TeV-powheg-pythia8_ttcc_hadd.root",
    "TTToHadronic_TuneCP5_13TeV-powheg-pythia8_ttjj_hadd.root",
    "TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8_tt1b_hadd.root",
    "TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8_tt2b_hadd.root",
    "TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8_ttbb_hadd.root",
    "TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8_ttcc_hadd.root",
    "TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8_ttjj_hadd.root"
  ]
}

varList["DNN"] = [
  ("AK4HTpMETpLepPt", "S_{T} [GeV]" , 0, 4000, 101),
  ("minMleppBjet", "min[M(l,b)] [GeV]", 0, 1000, 101),
  ("mass_minBBdr", "M(b,b) with min[#DeltaR(b,b)] [GeV]", 0, 1400, 51),
  ("deltaR_lepBJet_maxpt", "#DeltaR(l,b) with max[p_{T}(l,b)]", 0, 6.0, 51),
  ("lepDR_minBBdr", "#DeltaR(l,bb) with min[#DeltaR(b,b)]", -1, 10, 51),
  ("centrality", "Centrality", 0, 1.0, 51),
  ("deltaEta_maxBB", "max[#Delta#eta(b,b)]", -6, 11, 51),
  ("aveCSVpt", "ave(p_{T} weighted CSVv2) [GeV]", -0.3, 1.1, 101),
  ("aveBBdr", "ave[#DeltaR(b,b)]", 0, 6.0, 51),
  ("FW_momentum_0", "0^{th} FW moment [GeV]", 0, 1, 51),
  ("FW_momentum_1", "1^{st} FW moment [GeV]", 0, 1, 51),
  ("FW_momentum_2", "2^{nd} FW moment [GeV]", 0, 1, 51),
  ("FW_momentum_3", "3^{rd} FW moment [GeV]", 0, 1, 51),
  ("FW_momentum_4", "4^{th} FW moment [GeV]", 0, 1, 51),
  ("FW_momentum_5", "5^{th} FW moment [GeV]", 0, 1, 51),
  ("FW_momentum_6", "6^{th} FW moment [GeV]", 0, 1, 51),
  ("mass_maxJJJpt", "M(jjj) with max[p_{T}(jjj)] [GeV]", 0, 3000, 101),
  ("BJetLeadPt", "p_{T}{b_{1}) [GeV]", 0, 2000, 101),
  ("deltaR_minBB", "min[#DeltaR(b,b)]", 0, 6.0, 51),
  ("minDR_lepBJet", "min[#DeltaR(l,b)]", 0, 6.0, 51),
  ("MT_lepMet", "M_{T}(l,#slash{E}_{T}) [GeV]", 0, 250, 51),
  ("AK4HT", "H_{T} [GeV]", 0, 3000, 121),
  ("hemiout", "Hemiout [GeV]", 0, 3000, 101),
  ("theJetLeadPt", "p_{T}(j_{1}) [GeV]", 0, 1500, 101),
  ("corr_met_MultiLepCalc", "p_{T}^{miss} [GeV]", 0, 1500, 51),
  ("leptonPt_MultiLepCalc", "Lepton p_{T} [GeV]", 0, 600, 121),
  ("mass_lepJets0", "M(l,j_{1}) [GeV]", 0, 2200, 101), 
  ("mass_lepJets1", "M(l,j_{2}) [GeV]", 0, 3000, 101),
  ("mass_lepJets2", "M(l,j_{3}) [GeV]", 0, 3000, 101),
  ("MT2bb", "MT2bb [GeV]", 0, 400, 51),
  ("mass_lepBJet0", "M(l,b_{1}) [GeV]", 0, 1800, 101),
  ("mass_lepBJet_mindr", "M(l,b) with min[#DeltaR(l,b)] [GeV]", 0, 800, 51),
  ("secondJetPt", "p_{T}(j_{2}) [GeV]", 0, 2500, 101),
  ("fifthJetPt", "p_{T}(j_{5}) [GeV]", 0, 400, 101),
  ("sixthJetPt", "p_{T}(j_{6}) [GeV]", 0, 400, 51),
  ("PtFifthJet", "5^{th} jet p_{T} [GeV]", -1, 2000, 101),
  ("mass_minLLdr", "M(j,j) with min[#DeltaR(j,j)], j #neq b [GeV]", 0, 600, 51),
  ("mass_maxBBmass", "max[M(b,b)] [GeV]", 0, 2000, 101),
  ("deltaR_lepJetInMinMljet", "#DeltaR(l,j) with min M(l, j)", 0, 4.5, 101),
  ("deltaPhi_lepJetInMinMljet", "#DeltaPhi(l,j) with min M(l, j)", -4, 4, 51),
  ("deltaR_lepbJetInMinMlb", "#DeltaR(l,b) with min M(l, b)", 0, 6.0, 51),
  ("deltaPhi_lepbJetInMinMlb", "#DeltaPhi(l,b) with min M(l, b)", -11, 5, 101),
  ("M_allJet_W", "M(J_{all}, W_{lep}) [GeV]", 0, 10000, 201),
  ("HT_bjets", "HT(bjets) [GeV]", 0, 1800, 101),
  ("ratio_HTdHT4leadjets", "HT/HT(4 leading jets)", 0, 2.6, 51),
  ("csvJet3", "DeepCSV(3rdPtJet)", -2.2, 1.2, 101),
  ("csvJet4", "DeepCSV(4thPtJet)", -2.2, 1.2, 101),
  ("firstcsvb_bb", "DeepCSV(1stDeepCSVJet)", -2, 1.5, 51),
  ("secondcsvb_bb", "DeepCSV(2ndDeepCSVJet)", -2, 1.5, 51),
  ("thirdcsvb_bb", "DeepCSV(3rdDeepCSVJet)", -2, 1.5, 51),
  ("fourthcsvb_bb", "DeepCSV(4thDeepCSVJet)", -2, 1.5, 51),
  ("NJets_JetSubCalc", "AK4 jet multiplicity", 0, 15, 16),
  ("HT_2m", "HTwoTwoPtBjets [GeV]", -20, 5000, 201),
  ("Sphericity", "Sphericity", 0, 1.0, 51),
  ("Aplanarity", "Aplanarity", 0, 0.5, 51),
  ("minDR_lepJet", "min[#DeltaR(l,j)]", 0, 4, 51),
  ("BDTtrijet1", "trijet1 discriminator", -1, 1, 101),
  ("BDTtrijet2", "trijet2 discriminator", -1, 1, 101),
  ("BDTtrijet3", "trijet3 discriminator", -1, 1, 101),
  ("BDTtrijet4", "trijet4 discriminator", -1, 1, 51),
  ("NresolvedTops1pFake", "resolved t-tagged jet multiplicity", 0, 5, 6),
  ("NJetsTtagged", "t-tagged jet multiplicity", 0, 4, 5),
  ("NJetsWtagged", "W-tagged multiplicity", 0, 5, 6),
  ("NJetsCSV_MultiLepCalc", "b-tagged jet multiplicity", 0, 10, 11),
  ("HOTGoodTrijet1_mass", "HOTGoodTrijet1_mass [GeV]", 0, 300, 51),               # Trijet variables
  ("HOTGoodTrijet1_dijetmass", "HOTGoodTrijet1_dijetmass [GeV]", 0, 250, 51),
  ("HOTGoodTrijet1_pTratio", "HOTGoodTrijet1_pTratio" , 0, 1, 51),
  ("HOTGoodTrijet1_dRtridijet", "HOTGoodTrijet1_dRtridijet", 0, 4, 51),
  ("HOTGoodTrijet1_csvJetnotdijet", "HOTGoodTrijet1_csvJetnotdijet", -2.2, 1.2, 101),
  ("HOTGoodTrijet1_dRtrijetJetnotdijet", "HOTGoodTrijet1_dRtrijetJetnotdijet", 0, 4, 51),
  ("HOTGoodTrijet2_mass", "HOTGoodTrijet2_mass [GeV]", 0, 300, 51),
  ("HOTGoodTrijet2_dijetmass", "HOTGoodTrijet2_dijetmass [GeV]", 0, 250, 51),
  ("HOTGoodTrijet2_pTratio", "HOTGoodTrijet2_pTratio", 0, 1, 51),
  ("HOTGoodTrijet2_dRtridijet", "HOTGoodTrijet2_dRtridijet", 0, 4, 51),
  ("HOTGoodTrijet2_csvJetnotdijet", "HOTGoodTrijet2_csvJetnotdijet", -2.2, 1.2, 101),
  ("HOTGoodTrijet2_dRtrijetJetnotdijet", "HOTGoodTrijet2_dRtrijetJetnotdijet", 0, 4, 51)
]

varList["Step3"] = varList["DNN"][:] 
varList["Step3"].append( tuple( ( "DNN_disc_4j_40vars", "ttt discriminator (4j, 40vars)", 0, 1, 101) ) )
varList["Step3"].append( tuple( ( "DNN_disc_4j_50vars", "ttt discriminator (4j, 50vars)", 0, 1, 101) ) )
varList["Step3"].append( tuple( ( "DNN_disc_4j_76vars", "ttt discriminator (4j, 76vars)", 0, 1, 101) ) )
varList["Step3"].append( tuple( ( "DNN_disc_6j_40vars", "ttt discriminator (6j, 40vars)", 0, 1, 101) ) )
varList["Step3"].append( tuple( ( "DNN_disc_6j_50vars", "ttt discriminator (6j, 50vars)", 0, 1, 101) ) )
varList["Step3"].append( tuple( ( "DNN_disc_6j_76vars", "ttt discriminator (6j, 76vars)", 0, 1, 101) ) )

# weight event count

weightStr = "triggerXSF * pileupWeight * lepIdSF * EGammaGsfSF * isoSF * L1NonPrefiringProb_CommonCalc * " + \
            "(MCWeight_MultiLepCalc / abs(MCWeight_MultiLepCalc) ) * xsecEff * tthfWeight * njetsWeight * btagCSVWeight * btagCSVRenormWeight"

# general cut, add selection based cuts in training scripts

cut = {
  "lepPt":   20,
  "met":     60,
  "MT_lmet": 60,
  "JetPt0":  0,
  "JetPt1":  0,
  "JetPt2":  0,
  "minDR":   0.4,
  "HT":      250
}

cutStr =  "( ( leptonPt_MultiLepCalc > {} && isElectron ) || ".format( cut["lepPt"] ) + \
          "( leptonPt_MultiLepCalc > {} && isMuon ) ) && ".format( cut["lepPt"] ) + \
          "( corr_met_MultiLepCalc > {} ) && ".format( cut["met"] ) + \
          "( MT_lepMet > {} ) && ".format( cut["MT_lmet"] ) + \
          "( theJetPt_JetSubCalc_PtOrdered[0] > {} ) && ".format( cut["JetPt0"] ) + \
          "( theJetPt_JetSubCalc_PtOrdered[1] > {} ) && ".format( cut["JetPt1"] ) + \
          "( theJetPt_JetSubCalc_PtOrdered[2] > {} ) && ".format( cut["JetPt2"] ) + \
          "( minDR_lepJet > {} ) && ".format( cut["minDR"] ) + \
          "( AK4HT > {} ) && ".format( cut["HT"] ) + \
          "( DataPastTriggerX == 1 ) && ( MCPastTriggerX == 1 )"
