import numpy as np

years = [ "16APV", "16", "17", "18" ]

postfix = "3t"
inputDir = { year: "/isilon/hadoop/store/user/dali/FWLJMET106XUL_singleLep20{}UL_RunIISummer20_{}_step3/".format( year, postfix ) for year in years }

# target lumis in 1/pb for each year
lumi = {
  "16APV": 19520., # from pdmv
  "16": np.around( 16810. * 0.995 ),    # from pdmv, missing a few LJMet files from Run2016F
  "17": 41480.,    # calculated using brilcalc on GoldenJSON 
  "18": 59832.     # calculated using brilcalc on GoldenJSON
}
lumiStr = { year: str( lumi[ year ] / 1000. ).replace( ".", "p" ) + "fb" for year in lumi }

# Branching ratios
BR = {
  "BW" : [0.0,0.50,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0],
  "TH" : [0.5,0.25,0.0,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0],
  "TZ" : [0.5,0.25,1.0,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]
}

# boolean options that need to be coordinated across template making
options = {
  "GENERAL": {
    "TEST": False,        # run on limited samples
    "HDAMP": False,       # hdamp systematics
    "UE": False,          # ue systematics
    "PDF": True,          # pdf systematics
    "SYSTEMATICS": True,  # include other systematics defined in systematics[ "MC" ]
    "ABCDNN": False,
    "FINAL ANALYSIS": False
  },
  "HISTS": {
    "RENORM PDF": True, # renormalize the PDF weights
    "SUMMARY": False,   # produce summary templates
    "SCALE SIGNAL 1PB": False, # Scale the signal xsec to 1 PB for future studies
  },
  "MODIFY BINNING": {
    "BLIND": True,
    "PDF": True,                   # add PDF systematic uncertainty
    "CR SYST": False,              # add systematic uncertainty to control region
    "SHAPE SYST": True,            # add systematic uncertainty shapes
    "SHAPE STAT": True,            # add statistical uncertainty shapes
    "MURF SHAPES": True,
    "PS WEIGHTS": True,            # Construct Parton Shower weights
    "NORM THEORY SIG SYST": True,  # normalize the theoretical systematics (MURF, PS WEIGHTS, PDF) for the signal
    "NORM THEORY BKG SYST": False, # normalize the theoretical systematics (MURF, PS WEIGHTS, PDF) for the background
    "SYMM SMOOTHING": True,
    "SYMM TOP PT": True,
    "SYMM HOTCLOSURE": True,
    "SCALE SIGNAL XSEC": False,
    "ADD SHAPE SYST YIELD": True,
    "SMOOTH": True,
    "UNCORRELATE YEARS": True,
    "TRIGGER EFFICIENCY": False,
  },
  "COMBINE": {
    "TTHF SYST": True,
    "PDF": True,
    "ABCDNN": False,
    "SMOOTH": True
  }
}
# non-boolean parameters used in creating templates
params = {
  "GENERAL": {
    "ZERO": 1e-12,      # default non-zero value for zero to prevent division by zero
    "REBIN": -1,        # rebin histogram binning, use -1 to keep original binning
    "PDF RANGE": 100,   # PDF range
  },
  "ABCDNN": {
    "TAG": "nJ6pnB2p",                      # ABCDnn transformed variable tag i.e. <varname>_<tag>
    "MC SCALE": 0.1,                        # fraction of total MC samples used when training ABCDnn 
    "CONTROL VARIABLES":  [ "NJ", "NB" ],   # X and Y control variables to define regions
    "TRANSFER VARIABLES": [ "HT", "DNN" ],  # transformed variables
    "GROUPS": [ "TTBB", "TTNOBB" ],         # MC samples used in ABCDnn training
    "SYSTEMATICS": [ "ABCDNNSAMPLE", "ABCDNNMODEL", "ABCDNNCLOSURE", "MUR", "MUF", "MURFCORRD", "ISR", "FSR" ],
  },
  "HISTS": {
    "LUMISCALE": 1,         # scale the luminosity multiplicatively in templates
    "REBIN": -1,            # rebin histograms to have this number of bins
    "TTHFSF": 4.7/3.9,      # from TOP-18-002 (v34), set to 1 if tt heavy flavor scaling not used
    "TTLFSF": -1.,          # if ttLFsf -1, compute automatically using ttHFsf, else set manually
    "MIN BKG YIELD": 0.015, # minimum yield threshold for a bkg group to be included in combine analysis ( default = 0.015 )
    "MAX BKG ERROR": 0.50   # maximum uncertainty threshold for a bkg group to be included in combine analysis ( default = 0.50 )
  },
  "MODIFY BINNING": {
    "STAT THRESHOLD": 0.3,      # the ratio of yield error to yield must be below this value per bin ( default = 0.3 )
    "MIN MERGE": 1,             # merge at least this number of bins
    "THRESHOLD BB": 0.05 ,      # total bkg statistical uncertainty threshold to assign bin-by-bin nuisances  ( default = 0.05 )
    "SMOOTHING ALGO": "lowess", # smoothing algorithm to use
    "REMOVE SYST FROM YIELD": [ # list of systematics to exclude from yield calculation
      "HDAMP", "UE", 
      "NJET", "NJETSF", "PSWGT", "BTAG"
    ],
    "EXCLUDE SMOOTH": [
      "TOPPT", "HT" 
    ]
  },
  "COMBINE": {
    "BACKGROUNDS": [ "TTNOBB", "TTBB", "TOP", "EWK", "QCD", "TTH" ], 
    "DATA": [ "data_obs" ],
    "SIGNALS": [ "TTTW", "TTTJ" ],
  }  
}


# systematic uncertainty sources
systematics = {
  "MC": {  # to be added as histograms
    "pileup": True, 
    "prefire": True,
    "pileupJetID": True,
    "trigeff": False,   
    "muRFcorrd": True, 
    "muR": True, 
    "muF": True, 
    "isr": True, 
    "fsr": True, 
    "hotstat": True, 
    "hotcspur": True, 
    "hotclosure": True,
    "njet": False,
    "njetsf": False,
    "LF": True, 
    "lfstats1": True, 
    "lfstats2": True, 
    "HF": True, 
    "hfstats1": True, 
    "hfstats2": True, 
    "cferr1": True, 
    "cferr2": True,
    "toppt": True, 
    "ht": False,
    "ABCDNNSAMPLE": True,      # Normal error propagation of extended ABCD equation in analysis SR
    "ABCDNNMODEL": True,
    "ABCDNNCLOSURE": True,
    "JER": True, 
    "JEC": True,
    "HD": False,
    "UE": False
  },
  "REDUCED JEC": {
    "Total": False,
    "FlavorQCD": True,
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
  },
  "LUMI": { # uncorrelated
    "16APV": 1.007,
    "16": 1.007,
    "17": 1.020,
    "18": 1.015
  },
  "LUMI_RUN2": { # Full Run2 correlated
    "16APV": 1.004,
    "16": 1.004,
    "17": 1.009,
    "18": 1.020
  },
  "LUMI_17_18": { # 2017 and 2018 correlated
    "16APV": 1.00,
    "16": 1.00,
    "17": 1.006,
    "18": 1.002
  },
  "TRIG": {
    "E": 1.03, 
    "M": 1.03,
  },
  "ID": {
    "E": 1.015,
    "M": 1.010
  },
  "ISO": {
    "E": 1.025,
    "M": 1.025
  },
  "XSEC": {
    "TTBAR": [ 0.945, 1.048 ],
    "TTH": 1.12,
    "TOP": 1.20,
    "EWK": 1.06  #[ 0.927, 1.051 ]
  },
  # all of the Extended ABCD uncertainties calculated using specific analysis region (i.e. nJ = {4,5,6+} and nB = {2,3+} ), make sure using corresponding uncertainty value for given analysis regions
  "EXTABCDSYST": {
    "16APV": 1.000,
    "16": 1.000,
    "17": 1.021, # nJ5pnB2p = 1.012, nJ6pnB2p = 1.014, nJ6pnB3p = 1.021
    "18": 1.000
  },
  "EXTABCDSTAT": {
    "16APV": 1.000,
    "16": 1.000,
    "17": 1.010, # nJ5pnB2p = 1.005, nJ6pnB2p = 1.004, nJ6pnB3p = 1.010
    "18": 1.000
  },
  "EXTABCDCLOSURE": {
    "16APV": 1.000,
    "16": 1.000,
    "17": 1.093, # nJ5pnB2p = 1.151, nJ6pnB2p = 1.166, nJ6pnB3p = 1.093
    "18": 1.00
  },
  "PILEUP": 1.046,
  "TTHF": 1.13,
  "HDAMP": 1.085,
  "MURF NORM": { 
    "TTNOBB": 1.36,
    "TTBB": 1.36,
    "TOP": 1.47,
    "EWK": 1.31,
    "QCD": 1.38
  },
  "ISR NORM": {
    "TTNOBB": 1.17,
    "TTBB": 1.15,
    "TOP": 1.16,
    "EWK": 1.00,
    "QCD": 1.11
  },
  "FSR NORM": {
    "TTNOBB": 1.33,
    "TTBB": 1.68,
    "TOP": 1.24,
    "EWK": 1.00,
    "QCD": 1.21
  },
  "PDF NORM": {
    "TTNOBB": 1.00,
    "TTBB": 1.00,
    "TOP": 1.20,
    "EWK": 1.00,
    "QCD": 1.01
  }
}

# binning configuration for the templates

region_prefix = {
  "SR": "templates_SR",
  "VR": "templates_VR",
  "TTCR": "ttbar",
  "WJCR": "wjets",
  "BASELINE": "baseline",
  "ABCDNN": "abcdnn"
}

hist_bins = {
  "SR": {
    "LEPTON": [ "E", "M" ],
    "NHOT": [ "0", "1p" ],
    "NT": [ "0p" ],
    "NW": [ "0p" ],
    "NB": [ "1p" ],
    "NJ": [ "4", "5p" ]
  },
  "VR": {
    "LEPTON": [ "E", "M" ],
    "NHOT": [ "0p" ],
    "NT": [ "0p" ],
    "NW": [ "0p" ],
    "NB": [ "2", "3p" ],
    "NJ": [ "5", "6" ]
  },
  "BASELINE": {
    "LEPTON": [ "E", "M" ],
    "NHOT": [ "0p" ],
    "NT": [ "0p" ],
    "NW": [ "0p" ],
    "NB": [ "1p" ],
    "NJ": [ "4p" ]
  },
  "ABCDNN": { # edit these based on ABCDnn training signal region
    "LEPTON": [ "E", "M" ],
    "NHOT": [ "0p" ],
    "NT": [ "0p" ],
    "NW": [ "0p" ],
    "NB": [ "2p" ],
    "NJ": [ "6p" ] 
  }
}

event_cuts = {
  "pt_electron": 20,
  "pt_muon": 20,
  "pt_jet": 30,
  "met": 20,
  "mt": 0,
  "ht": 350
}

base_cut = "DataPastTriggerX == 1 && MCPastTriggerX == 1 "
base_cut += " && ( ( leptonPt_MultiLepCalc > {} && isElectron == 1 ) || ( leptonPt_MultiLepCalc > {} && isMuon == 1 ) )".format( event_cuts[ "pt_electron" ], event_cuts[ "pt_muon" ] )
base_cut += " && AK4HT > {} && corr_met_MultiLepCalc > {} && MT_lepMet > {} && minDR_lepJet > 0.4".format( event_cuts[ "ht" ], event_cuts[ "met" ], event_cuts[ "mt" ] )
mc_weight = "triggerXSF * triggerSF * pileupWeight * pileupJetIDWeight * lepIdSF * EGammaGsfSF * isoSF"
mc_weight += " * ( MCWeight_MultiLepCalc / abs( MCWeight_MultiLepCalc ) )"

# plotting configuration
def bins( min_, max_, nbins_ ):
  return np.linspace( min_, max_, nbins_ ).tolist()

plot_params = {
  "VARIABLES": {
    "LEPPT": ( "leptonPt_MultiLepCalc", bins( 0, 600, 41 ), "Lepton p_{T} [GeV]" ),
    "LEPETA": ( "leptonEta_MultiLepCalc", bins( -2.4, 2.4, 21 ), "Lepton #eta" ),
    "MINDR_LJ": ( "minDR_lepJet", bins( 0, 3, 31 ), "min(#DeltaR(l,jet))" ),
    "JETPT": ( "theJetPt_JetSubCalc_PtOrdered", bins( 0, 1500, 41 ), "AK4 Jet p_{T} [GeV]" ),
    "JETETA": ( "theJetEta_JetSubCalc_PtOrdered", bins( -2.4, 2.4, 21 ), "AK4 Jet #eta" ),
    "MET": ( "corr_met_MultiLepCalc", bins( 0, 1000, 41 ), "E_{T}^{miss} [GeV]" ),
    "HT": ( "AK4HT", bins( 0, 3000, 41 ), "H_{T} [GeV]" ),
    "NJETS": ( "NJets_JetSubCalc", bins( 0, 14, 15 ), "AK4 Jet Multiplicity" ),
    "NPU": ( "NJetsPU_JetSubCalc", bins( 0, 5, 6 ), "Pileup (T) Jet Multiplicity" ),
    "NBJETS": ( "NJetsCSV_JetSubCalc", bins( 0, 7, 8 ), "Medium DeepJet Multiplicity" ),
    "NWJETS": ( "NJetsWtagged", bins( 0, 6, 7 ), "W-tagged Jet Multiplicity" ),
    "NTJETS": ( "NJetsTtagged", bins( 0, 4, 5 ), "t-tagged Jet Multiplicity" ),
    "DNN": ( "DNN_1to40_3t", bins( 0, 1, 51 ), "DNN" ),
    "DNN3": ( "DNN_1to3_3t", bins( 0, 1, 51 ), "DNN (1-3)" ),
    "DNN5": ( "DNN_1to5_3t", bins( 0, 1, 51 ), "DNN (1-5)" ),
    "DNN10": ( "DNN_1to10_3t", bins( 0, 1, 51 ), "DNN (1-10)" ),
    "DNN20": ( "DNN_1to20_3t", bins( 0, 1, 51 ), "DNN (1-20)" ),
    "DNN30": ( "DNN_1to30_3t", bins( 0, 1, 51 ), "DNN (1-30)" ),
    "DNN40": ( "DNN_1to40_3t", bins( 0, 1, 51 ), "DNN (1-40)" ),
    "ST": ( "AK4HTpMETpLepPt", bins( 0, 4000, 41 ), "S_T [GeV]"  ),
    "MINM_LB": ( "minMleppBjet", bins( 0, 1000, 41 ), "min[M(l,b)] [GeV]" ),
    "M_MINBBDR": ( "mass_minBBdr", bins( 0, 1400, 41 ), "M(b,b) with min(#DeltaR(b,b)) [GeV]" ),
    "DR_LB": ( "deltaR_lepBJet_maxpt", bins( 0, 6.0, 21 ), "#DeltaR(l,b) with max[p_{T}(l,b)]" ),
    "DR_LBB": ( "lepDR_minBBdr", bins( -1, 10, 21 ), "#DeltaR(l,bb) with min[#DeltaR(b,b)]" ),
    "CENTRALITY": ( "centrality", bins( 0, 1.0, 21 ), "Centrality" ),
    "DE_BB": ( "deltaEta_maxBB", bins( -6, 11, 21 ), "max[#Delta#eta(b,b)]" ),
    "PT_CSV": ( "aveCSVpt", bins( -0.3, 1.1, 41 ), "ave(p_{T} weighted CSVv2) [GeV]" ),
    "DR_BB": ( "aveBBdr", bins( 0, 6.0, 21 ), "ave[#DeltaR(b,b)]" ),
    "FW0": ( "FW_momentum_0", bins( 0, 1, 21 ), "0^{th} FW moment [GeV]" ),
    "FW1": ( "FW_momentum_1", bins( 0, 1, 21 ), "1^{st} FW moment [GeV]" ),
    "FW2": ( "FW_momentum_2", bins( 0, 1, 21 ), "2^{nd} FW moment [GeV]" ),
    "FW3": ( "FW_momentum_3", bins( 0, 1, 21 ), "3^{rd} FW moment [GeV]" ),
    "FW4": ( "FW_momentum_4", bins( 0, 1, 21 ), "4^{th} FW moment [GeV]" ),
    "FW5": ( "FW_momentum_5", bins( 0, 1, 21 ), "5^{th} FW moment [GeV]" ),
    "FW6": ( "FW_momentum_6", bins( 0, 1, 21 ), "6^{th} FW moment [GeV]" ),
    "M_JJJ": ( "mass_maxJJJpt", bins( 0, 3000, 41 ), "M(jjj) with max[p_{T}(jjj)] [GeV]" ),
    "PT_B1": ( "BJetLeadPt", bins( 0, 500, 51 ), "p_{T}{b_{1}) [GeV]" ),
    "MINDR_BB": ( "deltaR_minBB", bins( 0, 6, 21 ), "min[#DeltaR(b,b)]" ),
    "MINDR_LB": ( "minDR_lepBJet", bins( 0, 6, 21 ), "min[#DeltaR(l,b)]" ),
    "MT_LMET": ( "MT_lepMet", bins( 0, 250, 41 ), "M_{T}(l,#slash{E}_{T}) [GeV]" ),
    "HEMIOUT": ( "hemiout", bins( 0, 2000, 41 ), "Hemiout [GeV]" ),
    "M_LJ0": ( "mass_lepJets0", bins( 0, 2000, 41 ), "M(l,j_{1}) [GeV]" ),
    "M_LJ1": ( "mass_lepJets1", bins( 0, 2000, 41 ), "M(l,j_{2}) [GeV]" ),
    "M_LJ2": ( "mass_lepJets2", bins( 0, 2000, 41 ), "M(l,j_{3}) [GeV]" ),
    "MT2BB": ( "MT2bb", bins( 0, 400, 41 ), "MT2bb [GeV]" ),
    "M_LB0": ( "mass_lepBJet0", bins( 0, 1800, 41 ), "M(l,b_{1}) [GeV]" ),
    "M_MINDR_LB": ( "mass_lepBJet_mindr", bins( 0, 1000, 21 ), "M(l,b) with min[#DeltaR(l,b)] [GeV]" ),
    "PT_J1": ( "theJetLeadPt", bins( 0, 500, 51 ), "p_{T}(j_{1}) [GeV]" ),
    "PT_J2": ( "secondJetPt", bins( 0, 500, 51 ), "2^{nd} Jet p_{T} [GeV]" ),
    "PT_J5": ( "fifthJetPt", bins( 0, 300, 31 ), "5^{th} Jet p_{T} [GeV]" ),
    "PT_J6": ( "sixthJetPt", bins( 0, 200, 21 ), "6^{th} Jet p_{T} [GeV]" ),
    "J5PT": ( "PtFifthJet", bins( 0, 800, 41 ), "5^{th} Jet p_{T} [GeV]" ),
    "M_MINLLDR": ( "mass_minLLdr", bins( 0, 600, 41 ), "M(j,j) with min[#DeltaR(j,j)], j #neq b [GeV]" ),
    "M_MAXBB": ( "mass_maxBBmass", bins( 0, 2000, 41 ), "max[M(b,b)] [GeV]" ),
    "DR_MINLJ": ( "deltaR_lepJetInMinMljet", bins( 0, 4.5, 21 ), "#DeltaR(l,j) with min M(l, j)" ),
    "DP_MINLJ": ( "deltaPhi_lepJetInMinMljet", bins( -4, 4, 21 ), "#Delta #Phi(l,j) with min M(l, j)" ),
    "DR_MINLB": ( "deltaR_lepbJetInMinMlb", bins( 0, 4.5, 21 ), "#DeltaR(l,b) with min M(l, b)" ),
    "DP_MINLB": ( "deltaPhi_lepbJetInMinMlb", bins( -11, 5, 21 ), "#Delta #Phi(l,b) with min M(l, b)" ),
    "M_JW": ( "M_allJet_W", bins( 0, 7000, 41 ), "M(J_{all}, W_{lep}) [GeV]" ),
    "HT_B": ( "HT_bjets", bins( 0, 1800, 41 ), "HT(bjets) [GeV]" ),
    "RATIO_HT": ( "ratio_HTdHT4leadjets", bins( 1, 2.1, 21 ),  "HT/HT(4 leading jets)" ),
    "CSV_J3": ( "csvJet3", bins( 0, 1, 41 ), "DeepCSV(3rdPtJet)" ),
    "CSV_J4": ( "csvJet4", bins( 0, 1, 41 ), "DeepCSV(4thPtJet)" ),
    "CSVB_1": ( "firstcsvb_bb", bins( 0, 1, 41 ), "DeepJet (1st)" ),
    "CSVB_2": ( "secondcsvb_bb", bins( 0, 1, 41 ), "DeepJet (2nd)" ),
    "CSVB_3": ( "thirdcsvb_bb", bins( 0, 1, 41 ), "DeepJet (3rd)" ),
    "CSVB_4": ( "fourthcsvb_bb", bins( 0, 1, 41 ), "DeepJet (4th)" ),
    "HT_2M": ( "HT_2m", bins( 0, 3000, 41 ), "H_{T}(b_{1},b_{2}) [GeV]" ),
    "SPHERICITY": ( "Sphericity", bins( 0, 1.0, 21 ), "Sphericity" ),
    "APLANARITY": ( "Aplanarity", bins( 0, 0.5, 21 ), "Aplanarity" ),
    "BDT3J_1": ( "BDTtrijet1", bins( -1, 1, 41 ), "trijet1 discriminator" ),
    "BDT3J_2": ( "BDTtrijet2", bins( -1, 1, 41 ), "trijet2 discriminator" ),
    "BDT3J_3": ( "BDTtrijet3", bins( -1, 1, 41 ), "trijet3 discriminator" ),
    "BDT3J_4": ( "BDTtrijet4", bins( -1, 1, 41 ), "trijet4 discriminator" ),
    "NHOT": ( "NresolvedTops1pFake", bins( 0, 4, 5 ), "Resolved t-tagged jet multiplicity" ),
    "HOT1_MASS": ( "HOTGoodTrijet1_mass", bins( 0, 250, 41 ), "HOTGoodTrijet1_mass [GeV]" ),
    "HOT1_DJMASS": ( "HOTGoodTrijet1_dijetmass", bins( 0, 250, 41 ), "HOTGoodTrijet1_dijetmass [GeV]" ),
    "HOT1_PTRATIO": ( "HOTGoodTrijet1_pTratio", bins( 0, 1, 41 ), "HOTGoodTrijet1_pTratio" ),
    "HOT1_DRJJ": ( "HOTGoodTrijet1_dRtridijet", bins( 0, 4, 21 ), "HOTGoodTrijet1_dRtridijet" ),
    "HOT1_CSVNOJJ": ( "HOTGoodTrijet1_csvJetnotdijet", bins( -2.2, 1.2, 41 ), "HOTGoodTrijet1_csvJetnotdijet" ),
    "HOT1_DRNOJJ": ( "HOTGoodTrijet1_dRtrijetJetnotdijet", bins( 0, 4, 21 ), "HOTGoodTrijet1_dRtrijetJetnotdijet" ),
    "HOT2_MASS": ( "HOTGoodTrijet2_mass", bins( 0, 300, 41 ), "HOTGoodTrijet2_mass [GeV]" ),
    "HOT2_DJMASS": ( "HOTGoodTrijet2_dijetmass", bins( 0, 200, 41 ), "HOTGoodTrijet2_dijetmass [GeV]" ),
    "HOT2_PTRATIO": ( "HOTGoodTrijet2_pTratio", bins( 0, 1, 41 ), "HOTGoodTrijet2_pTratio" ),
    "HOT2_DRJJ": ( "HOTGoodTrijet2_dRtridijet", bins( 0, 4, 21 ), "HOTGoodTrijet2_dRtridijet" ),
    "HOT2_CSVNOJJ": ( "HOTGoodTrijet2_csvJetnotdijet", bins( 0, 1, 41 ), "HOTGoodTrijet2_csvJetnotdijet" ),
    "HOT2_DRNOJJ": ( "HOTGoodTrijet2_dRtrijetJetnotdijet", bins( 0, 4, 21 ), "HOTGoodTrijet2_dRtrijetJetnotdijet" ),
  }
}


