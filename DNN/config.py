#!/usr/bin/env python

#input variables
varList = {}

# EDIT ME
bruxUserName = "dli50"
lpcUserName = "dsunyou"
eosUserName = "dali"
postfix = "3t"

years = [ "16APV", "16", "17", "18" ]

step2Sample = { year: "FWLJMET106XUL_singleLep20{}UL_RunIISummer20_{}_step2".format( year, postfix ) for year in years }

step3Sample = { year: step2Sample[ year ].replace( "step2", "step3" ) for year in years }

step2DirBRUX = { year: "root://brux30.hep.brown.edu:1094//store/user/{}/{}/".format( eosUserName, step2Sample[ year ] ) for year in years }

step3DirBRUX = { year: "root://brux30.hep.brown.edu:1094//store/user/{}/{}/".format( eosUserName, step3Sample[ year ] ) for year in years }

step2DirLPC = { year: "~/nobackup/CMSSW_10_6_29/src/TTT-singleLep/DNN/{}/".format( step2Sample[ year ] ) for year in years }

step3DirLPC = { year: "~/nobackup/CMSSW_10_6_29/src/TTT-singleLep/DNN/{}/".format( step3Sample[ year ] ) for year in years }

#step2DirXRD = { year: "root://cmsxrootd.fnal.gov//store/user/{}/{}/".format( eosUserName, step2Sample[ year ] ) for year in years }
step2DirXRD = { year: "root://brux30.hep.brown.edu:1094//store/user/{}/{}/".format( eosUserName, step2Sample[ year ] ) for year in years }

step3DirXRD = { year: "root://cmsxrootd.fnal.gov//store/user/{}/{}/".format( eosUserName, step3Sample[ year ] ) for year in years }

step2DirEOS = { year: "root://cmseos.fnal.gov///store/user/{}/{}/".format( eosUserName, step2Sample[ year ] ) for year in years }

step3DirEOS = { year: "root://cmseos.fnal.gov///store/user/{}/{}/".format( eosUserName, step3Sample[ year ] ) for year in years }

params = {
  "WEIGHT XSEC": True, # weight MC samples by cross-section
  "TRAIN TEST SPLIT": 0.20, # fraction of all events passing selection, used for validation test after training model
  "VALIDATION SPLIT": 0.20, # fraction of remaining events after training-test split, used during each epoch for validation loss
  "DROPOUT": 0.50, # dropout rate if dropout is used in DNN, default value is 0.50 per original paper by Hinton, et. al. (2012)
  "HPO": { # hyper parameter optimization settings
    "CALLS":    30,  # total number of hpo iterations
    "STARTS":   20,  # number of randomly sampled hpo iterations
    "EPOCHS":   100, # number of epochs to survey at each hpo iteration
    "PATIENCE": 5,  # number of epochs before early stopping 
    "OPT SPACE": { # add multiple values to list VALUE for HPO search, otherwise sets fixed value 
      "HIDDEN LAYERS":          { "TYPE": "INTEGER",     "VALUE": [ 1, 3 ] },  # number of hidden layers
      "HIDDEN NODES":           { "TYPE": "INTEGER",     "VALUE": [ 10, 40 ] }, # number of nodes per hidden layer
      "BATCH POWER":            { "TYPE": "INTEGER",     "VALUE": [ 4, 7 ] },  # number of events in batch as 2^N
      "LEARNING RATE":          { "TYPE": "CATEGORICAL", "VALUE": [ 0.0001, 0.0005, 0.001, 0.005 ] }, # learning rate step size for Adam optimizer
      "TRAINING REGULATOR":     { "TYPE": "CATEGORICAL", "VALUE": [ "DROPOUT", "BATCH NORMALIZATION", "BOTH", "NONE" ] }, # training regulators
      "ACTIVATION FUNCTION":    { "TYPE": "CATEGORICAL", "VALUE": [ "relu", "elu", "softplus" ] }, # non-linear activation function for hidden node output
      "ACTIVATION REGULARIZER": { "TYPE": "CATEGORICAL", "VALUE": [ "NONE" ] }, # adds the activation output to loss function
      "KERNEL INITIALIZER":     { "TYPE": "CATEGORICAL", "VALUE": [ "he_normal", "RandomNormal" ] }, # prior to sample initial node weights from
      "KERNEL REGULARIZER":     { "TYPE": "CATEGORICAL", "VALUE": [ "l2", "NONE" ] }, # adds the node weight value to the loss function
      "KERNEL CONSTRAINT":      { "TYPE": "CATEGORICAL", "VALUE": [ "maxnorm", "NONE" ] }, # constrains weights of hidden layer 
      "BIAS REGULARIZER":       { "TYPE": "CATEGORICAL", "VALUE": [ "NONE" ] }, # adds the node bias value to the loss function
    }
  },
  "KFCV": { # k-fold cross validation settings
    "EPOCHS": 5000,
    "PATIENCE": 20,
    "SAVE AUC POINTS": 20,
  }
}

# sample JES shifts
shifts = {
  "JER": True,
  "JEC": False, # fully de-correlated, corresponds to total JEC from LJMet
  "FlavorQCD": True,
  "FlavorPureGluon": False,
  "FlavorPureQuark": False,
  "FlavorPureCharm": False,
  "FlavorPureBottom": False,
  "RelativeBal": True,
  "RelativeSample_Era": True,
  "HF": True,
  "HF_Era": True,
  "BBEC1": True,
  "BBEC1_Era": True,
  "EC2": True,
  "EC2_Era": True,
  "Absolute": True,
  "Absolute_Era": True
}

# signal sample to be used in training
sig_training = { 
  year: [
    #"TTTJ_TuneCP5_13TeV-madgraph-pythia8_hadd.root", # make sure TTTJ is first
    #"TTTW_TuneCP5_13TeV-madgraph-pythia8_hadd.root"
    "TTTT_TuneCP5_13TeV-amcatnlo-pythia8_hadd.root"
  ] for year in years
}

# background samples to be used in training, only using ttbar events
bkg_training = {
  year: [
    #"TTTT_TuneCP5_13TeV-amcatnlo-pythia8_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_1_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_2_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_3_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_4_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_5_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_6_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_7_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_8_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_9_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_10_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttcc_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_tt1b_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_tt2b_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttbb_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_tt1b_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_tt2b_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_ttbb_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_ttcc_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_ttjj_hadd.root",
    #"TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_tt1b_hadd.root",
    #"TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_tt2b_hadd.root",
    #"TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_ttbb_hadd.root",
    #"TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_ttcc_hadd.root",
    #"TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_ttjj_hadd.root",
    #"TTToHadronic_TuneCP5_13TeV-powheg-pythia8_tt1b_hadd.root",
    #"TTToHadronic_TuneCP5_13TeV-powheg-pythia8_tt2b_hadd.root",
    #"TTToHadronic_TuneCP5_13TeV-powheg-pythia8_ttbb_hadd.root",
    #"TTToHadronic_TuneCP5_13TeV-powheg-pythia8_ttcc_hadd.root",
    #"TTToHadronic_TuneCP5_13TeV-powheg-pythia8_ttjj_hadd.root",
    #"TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8_tt1b_hadd.root",
    #"TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8_tt2b_hadd.root",
    #"TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8_ttbb_hadd.root",
    #"TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8_ttcc_hadd.root",
    #"TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8_ttjj_hadd.root"  
  ] for year in years
}

varList["DNN"] = [
  #("AK4HTpMETpLepPt", "S_{T} [GeV]" , 0, 4000, 101),  # poor data/MC agreement
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
  ("leptonCharge_MultiLepCalc", "Lepton Charge", -1, 1, 3 ),
  ("mass_lepJets0", "M(l,j_{1}) [GeV]", 0, 2200, 101), 
  ("mass_lepJets1", "M(l,j_{2}) [GeV]", 0, 3000, 101),
  ("mass_lepJets2", "M(l,j_{3}) [GeV]", 0, 3000, 101),
  ("MT2bb", "MT2bb [GeV]", 0, 400, 51),
  ("mass_lepBJet0", "M(l,b_{1}) [GeV]", 0, 1800, 101),
  ("mass_lepBJet_mindr", "M(l,b) with min[#DeltaR(l,b)] [GeV]", 0, 800, 51),
  ("secondJetPt", "p_{T}(j_{2}) [GeV]", 0, 2500, 101),
  ("fifthJetPt", "p_{T}(j_{5}) [GeV]", 0, 400, 101), # poor data/MC 
  ("sixthJetPt", "p_{T}(j_{6}) [GeV]", 0, 400, 51),  # poor data/MC
  #("PtFifthJet", "5^{th} jet p_{T} [GeV]", -1, 2000, 101), # poor data/MC
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
  ("firstcsvb_bb", "DeepJet(1st)", -2, 1.5, 51),
  ("secondcsvb_bb", "DeepJet(2nd)", -2, 1.5, 51),
  ("thirdcsvb_bb", "DeepJet(3rd)", -2, 1.5, 51),
  ("fourthcsvb_bb", "DeepJet(4th)", -2, 1.5, 51),
  ("NJets_JetSubCalc", "AK4 jet multiplicity", 0, 15, 16),
  #("NJetsForward_JetSubCalc", "AK4 forward jet multiplicity", 0, 5, 6),
  ("NJetsPU_JetSubCalc", "Pileup jet multiplicity", 0, 5, 6),
  ("theJetEtaAverageNotBJet_JetSubCalc", "Average LF Jet #eta", 0, 3, 31 ),
  ("theJetEtaAverage_JetSubCalc", "Average Jet #eta", 0, 3, 31 ),
  ("theJetEtaPtWeighted_JetSubCalc", "p_T Weighted Average Jet #eta", 0, 3, 31 ),
  ("theJetEta_JetNotBJetMaxPt_JetSubCalc", "Max p_T LF Jet #eta", 0, 3, 31 ),
  ("HT_2m", "HTwoTwoPtBjets [GeV]", -20, 5000, 201),
  ("Sphericity", "Sphericity", 0, 1.0, 51),
  ("Aplanarity", "Aplanarity", 0, 0.5, 51),
  ("minDR_lepJet", "min[#DeltaR(l,j)]", 0, 4, 51),
  ("BDTtrijet1", "trijet1 discriminator", -1, 1, 101),
  ("BDTtrijet2", "trijet2 discriminator", -1, 1, 101),
  ("BDTtrijet3", "trijet3 discriminator", -1, 1, 101),
  ("BDTtrijet4", "trijet4 discriminator", -1, 1, 51),
  ("NresolvedTops1pFake", "resolved t-tagged jet multiplicity", 0, 5, 6),
  #("NJetsTtagged", "t-tagged jet multiplicity", 0, 4, 5), # not used in three top
  #("NJetsWtagged", "W-tagged multiplicity", 0, 5, 6), # not used in three top
  ("NJetsCSV_JetSubCalc", "b-tagged jet multiplicity", 0, 10, 11),
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
varList["Step3"].append( tuple( ( "DNN_3t", "ttt discriminator", 0, 1, 101) ) )

# weight event count

weightStr = "triggerXSF * triggerSF * pileupWeight * lepIdSF * EGammaGsfSF * isoSF * L1NonPrefiringProb_CommonCalc * " + \
            "(MCWeight_MultiLepCalc / abs(MCWeight_MultiLepCalc) ) * xsecEff * tthfWeight * btagDeepJetWeight * btagDeepJet2DWeight_HTnj"

# general cut, add selection based cuts in training scripts

base_cut =  "DataPastTriggerX == 1 && MCPastTriggerX == 1 && !TMath::IsNaN(theJetEtaAverageNotBJet_JetSubCalc)"

# branches to add to step3 ntuple
branches = [
"isElectron", "isMuon",
"triggerXSF", "triggerSF", 
"isHTgt500Njetge9",
"pileupWeight", "pileupWeightUp", "pileupWeightDown",
"pileupJetIDWeight", "pileupJetIDWeightUp", "pileupJetIDWeightDown",
"lepIdSF", "EGammaGsfSF", "isoSF", 
"L1NonPrefiringProb_CommonCalc", "L1NonPrefiringProbUp_CommonCalc", "L1NonPrefiringProbDown_CommonCalc",
"renormWeights", "renormPSWeights", "pdfWeights",
"MCWeight_MultiLepCalc", "xsecEff", "tthfWeight", "btagDeepJetWeight", "btagDeepJet2DWeight_HTnj", "DataPastTriggerX", "MCPastTriggerX", "isTraining", "topPtWeight13TeV", 
"leptonPt_MultiLepCalc", "leptonEta_MultiLepCalc", "leptonPhi_MultiLepCalc", "corr_met_MultiLepCalc", "MT_lepMet", "minDR_lepJet", "AK4HT", 
"theJetPt_JetSubCalc_PtOrdered", "theJetEta_JetSubCalc_PtOrdered", "NJetsPU_JetSubCalc", "NJetsCSV_JetSubCalc", "NJetsWtagged", "NJetsTtagged", "NresolvedTops1pFake",
"NJetsWtagged_shifts", "NJetsTtagged_shifts", "NresolvedTops1pFake_shifts"
]

for syst in [ "LF", "lfstats1", "lfstats2", "HF", "hfstats1", "hfstats2", "cferr1", "cferr2" ]:
  for shift in [ "up", "dn" ]:
    branches.append( "btagDeepJetWeight_" + syst + shift )
    branches.append( "btagDeepJet2DWeight_HTnj_" + syst + shift )

