#!/usr/bin/env python

#input variables
varList = {}

# EDIT ME
bruxUserName = "dli50"
lpcUserName = "dsunyou"
eosUserName = "dali"
postfix = "deepJetV1"

years = [ "17" ]

step2Sample = { year: "FWLJMET106XUL_1lep20{}_3t_{}_step2".format( year, postfix ) for year in years }

step3Sample = { year: step2Sample[ year ].replace( "step2", "step3" ) for year in years }

step2DirBRUX = { year: "/isilon/hadoop/store/user/dali/{}/".format( step2Sample[ year ] ) for year in years }

step2DirLPC = { year: "~/nobackup/TTT-singleLep/CMSSW_10_6_19/src/TTT-singleLep/DNN/{}/".format( step2Sample[ year ] ) for year in years }

step3DirLPC = { year: "~/nobackup/TTT-singleLep/CMSSW_10_6_19/src/TTT-singleLep/DNN/{}/".format( step3Sample[ year ] ) for year in years }

step2DirXRD = { year: "root://cmsxrootd.fnal.gov//store/user/{}/{}/".format( eosUserName, step2Sample[ year ] ) for year in years }

step3DirXRD = { year: "root://cmsxrootd.fnal.gov//store/user/{}/{}/".format( eosUserName, step3Sample[ year ] ) for year in years }

step2DirEOS = { year: "root://cmseos.fnal.gov///store/user/{}/{}/".format( eosUserName, step2Sample[ year ] ) for year in years }

step3DirEOS = { year: "root://cmseos.fnal.gov///store/user/{}/{}/".format( eosUserName, step3Sample[ year ] ) for year in years }

# signal sample to be used in training
sig_training = {
  "17": [ 
    "TTTJ_TuneCP5_13TeV-madgraph-pythia8_hadd.root", # make sure TTTJ is first
    "TTTW_TuneCP5_13TeV-madgraph-pythia8_hadd.root"
  ]
}

# background samples to be used in training, only using ttbar events
bkg_training = {
  "17": [
    "TTTT_TuneCP5_13TeV-amcatnlo-pythia8_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_1_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_2_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_3_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_4_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttcc_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_tt1b_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_tt2b_hadd.root",
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttbb_hadd.root",
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

shift_keys = {
  "": "",
  "UEdn": "down",
  "UEup": "up",
  "HDAMPup": "hdampUP",
  "HDAMPdn": "hdampDN"
}

all_samples = { 
  "17": {
    "TTTJ": "TTTJ_TuneCP5_13TeV-madgraph-pythia8_hadd.root",
    "TTTW": "TTTW_TuneCP5_13TeV-madgraph-pythia8_hadd.root",
    "TTTT": "TTTT_TuneCP5_13TeV-amcatnlo-pythia8_hadd.root",
    "TTHH": "TTHH_TuneCP5_13TeV-madgraph-pythia8_hadd.root",
    "TTWH": "TTWH_TuneCP5_13TeV-madgraph-pythia8_hadd.root",
    "TTWW": "TTWW_TuneCP5_13TeV-madgraph-pythia8_hadd.root",
    "TTWZ": "TTWZ_TuneCP5_13TeV-madgraph-pythia8_hadd.root",
    "TTZH": "TTZH_TuneCP5_13TeV-madgraph-pythia8_hadd.root",
    "TTZZ": "TTZZ_TuneCP5_13TeV-madgraph-pythia8_hadd.root",
    "TTWl": "TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_hadd.root",
    "TTWq": "TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_hadd.root",
    "TTZlM10": "TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_hadd.root",
    #"TTZlM1to10": "TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8_hadd.root",
    "TTHnoB": "ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_hadd.root",
    "TTHB": "ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8_hadd.root",
 
    "DataE": "SingleElectron_hadd.root",
    "DataM": "SingleMuon_hadd.root",
  
    "DY200":  "DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_hadd.root",
    "DY400":  "DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_hadd.root",
    "DY600":  "DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_hadd.root",
    "DY800":  "DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_hadd.root",
    "DY1200": "DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_hadd.root",
    "DY2500": "DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_hadd.root",
  
    "QCD200":  "QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraph-pythia8_hadd.root",
    "QCD300":  "QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraph-pythia8_hadd.root",
    "QCD500":  "QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8_hadd.root",
    "QCD700":  "QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraph-pythia8_hadd.root",
    "QCD1000": "QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraph-pythia8_hadd.root",
    "QCD1500": "QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8_hadd.root",
    "QCD2000": "QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraph-pythia8_hadd.root",
  
    "Ts": "ST_s-channel_4f_leptonDecays_13TeV_amcatnlo-pythia_hadd.root",
    "Tbt": "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8_hadd.root",
    "Tt": "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_hadd.root",
    "TbtW": "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8_hadd.root",
    "TtW": "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8_hadd.root",

    "WJets200": "WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root",
    "WJets400": "WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root",
    "WJets600": "WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root",
    "WJets800": "WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root",
    "WJets1200": "WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root",
    "WJets2500": "WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root",
  
    "WW": "WW_TuneCP5_13TeV-pythia8_hadd.root",
    "WZ": "WZ_TuneCP5_13TeV-pythia8_hadd.root",
    "ZZ": "ZZ_TuneCP5_13TeV-pythia8_hadd.root"
  },
}

shift_key = {
  "TuneCP5": "",
  "TuneCP5up": "UEUP",
  "TuneCP5down": "UEDN",
  "hdampUP_TuneCP5": "HDUP",
  "hdampDOWN_TuneCP5": "HDDN"
}

for year in years:
  for tt in [ "SemiLeptonic", "SemiLepton", "2L2Nu", "Hadronic" ]:
    for jj in [ "tt1b", "tt2b", "ttbb", "ttcc", "ttjj" ]:
      for shift in shift_key:
        if tt == "SemiLeptonic" and shift == "TuneCP5":
          for n in ["1","2","3","4"]:
            all_samples[ year ][ "TTTo{}_{}_{}_{}".format( tt, jj, shift_key[ shift ], n ) ] = "TTTo{}_{}_13TeV-powheg-pythia8_{}_{}_hadd.root".format( tt, shift, jj, n )
        else:
          all_samples[ year ][ "TTTo{}_{}_{}".format( tt, jj, shift_key[ shift ] ) ] = "TTTo{}_{}_13TeV-powheg-pythia8_{}_hadd.root".format( tt, shift, jj ) 
   
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
  ("firstcsvb_bb", "DeepJet(1st)", -2, 1.5, 51),
  ("secondcsvb_bb", "DeepJet(2nd)", -2, 1.5, 51),
  ("thirdcsvb_bb", "DeepJet(3rd)", -2, 1.5, 51),
  ("fourthcsvb_bb", "DeepJet(4th)", -2, 1.5, 51),
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

weightStr = "triggerXSF * pileupWeight * lepIdSF * EGammaGsfSF * isoSF * L1NonPrefiringProb_CommonCalc * " + \
            "(MCWeight_MultiLepCalc / abs(MCWeight_MultiLepCalc) ) * xsecEff * tthfWeight * btagDeepJetWeight * btagDeepJet2DWeight_HTnj"

# general cut, add selection based cuts in training scripts

base_cut =  "( DataPastTriggerX == 1 ) && ( MCPastTriggerX == 1 )"
