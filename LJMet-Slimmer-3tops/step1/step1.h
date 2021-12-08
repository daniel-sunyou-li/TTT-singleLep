//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Jun 26 06:05:34 2019 by ROOT version 6.12/07
// from TTree ljmet/ljmet
// found on file: /eos/uscms/store/user/lpcljm/FWLJMET102X_1lep2017_052219/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/singleLep2017/190614_213007/0000/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_1.root
//////////////////////////////////////////////////////////

#ifndef step1_h
#define step1_h

#include <iostream>
#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include "TH1.h"

// Header file for the classes stored in the TTree if any.
#include "vector"
#include "TLorentzVector.h"
#include "HardcodedConditions.h"
#include "BTagCalibForLJMet.h"

enum shift:char;

using namespace std;

class step1 {
public :
   TTree          *inputTree;   //!pointer to the analyzed TTree or TChain
   TFile          *inputFile, *outputFile;
   Int_t           fCurrent; //!current Tree number in a TChain

   Bool_t          isSig=false;
   Bool_t          isTTTT=false;
   Bool_t          isMadgraphBkg=false;
   Bool_t          isMC=false;
   Bool_t          isSM=false;
   Bool_t          isSE=false;
   Bool_t          isHad=false;
   Bool_t          isTOP=false;
   Bool_t          isTT=false;
   Bool_t          isTTToSemiLeptonHT500Njet9=false;
   Bool_t          isTTV=false;
   Bool_t          isTTHbb=false;
   Bool_t          isTTHnonbb=false;
   Bool_t          isTTTX=false;
   Bool_t          isTTVV=false;
   Bool_t          isVV=false;
   Bool_t          isST=false;
   Bool_t          isSTt=false;
   Bool_t          isSTtW=false;
   Bool_t          isTTSemilepIncHT0Njet0=false;
   Bool_t          isTTSemilepIncHT500Njet9=false;
   Bool_t          outTTBB=false;
   Bool_t          outTT2B=false;
   Bool_t          outTT1B=false;
   Bool_t          outTTCC=false;
   Bool_t          outTTLF=false;
   Int_t           SigMass=-1;
   Int_t           Year=2017;
   TString         sample_="";
   std::string     sample="";
   
   // Fixed size dimensions of array or collections stored in the TTree if any.

   // NEW BRANCHES
   Int_t           isHTgt500Njetge9;
   Int_t           isElectron;
   Int_t           isMuon;
   Int_t           MCPastTriggerX;
   Int_t           MCPastTrigger;
   Int_t           MCLepPastTrigger;
   Int_t           MCHadPastTrigger;
   Int_t           MCPastTriggerOR;
   Int_t           MCPastTriggerLepTight;
   Int_t           MCPastTriggerHTTight;
   Int_t           DataPastTriggerX;
   Int_t           DataPastTrigger;
   Int_t           DataLepPastTrigger;
   Int_t           DataHadPastTrigger;
   Int_t           DataPastTriggerOR;
   Int_t           DataPastTriggerLepTight;
   Int_t           DataPastTriggerHTTight;

   Int_t           HLT_Ele15_IsoVVVL_PFHT450 = 0;
   Int_t           HLT_Ele28_eta2p1_WPTight_Gsf_HT150 = 0;
   Int_t           HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned = 0;
   Int_t           HLT_Mu15_IsoVVVL_PFHT450 = 0;
   Int_t           HLT_PFHT400_SixJet30_DoubleBTagCSV_p056 = 0;
   Int_t           HLT_Ele32_WPTight_Gsf = 0;
   Int_t           HLT_Ele35_WPTight_Gsf = 0;
   Int_t           HLT_IsoMu24 = 0;
   Int_t           HLT_IsoMu24_eta2p1 = 0;
   Int_t           HLT_IsoMu27 = 0;
   Int_t           HLT_PFHT380_SixJet32_DoubleBTagCSV_p075 = 0;
   Int_t           HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2 = 0;
   Int_t           HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2 = 0;
   Int_t           HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94 = 0;


   Float_t         pileupWeight;
   Float_t         pileupWeightUp;
   Float_t         pileupWeightDown;
   Float_t         isoSF;
   Float_t         lepIdSF;
   Float_t         EGammaGsfSF;
   Float_t         triggerSF;
   Float_t         triggerHadSF;
   Float_t         triggerXSF;
   Float_t         HTSF_Pol;
   Float_t         HTSF_PolUp;
   Float_t         HTSF_PolDn;
   vector<double>  renormWeights;
   vector<double>  renormPSWeights;
   vector<double>  alphaSWeights;
   vector<double>  pdfWeights;
   vector<double>  pdfNewWeights;
   float_t         pdfNewNominalWeight;
   Float_t         njetsWeight;
   Float_t         njetsWeightUp;
   Float_t         njetsWeightDown;
   Float_t         tthfWeight;
   Float_t         btagCSVRenormWeight;

   Float_t         leptonPt_MultiLepCalc;
   Float_t         leptonEta_MultiLepCalc;
   Float_t         leptonPhi_MultiLepCalc;
   Float_t         leptonEnergy_MultiLepCalc;
   vector<double>  *topBestGenPt_HOTTaggerCalc;
   Float_t         leptonMVAValue_MultiLepCalc;
   Float_t         leptonMiniIso_MultiLepCalc;
   Float_t         leptonRelIso_MultiLepCalc;
   Float_t         leptonDxy_MultiLepCalc;
   Float_t         leptonDz_MultiLepCalc;
   Int_t           leptonCharge_MultiLepCalc;

   Int_t           NJets_JetSubCalc;
   Int_t           NJetsCSV_MultiLepCalc; // DeepCSV
   Int_t           NJetsCSVwithSF_MultiLepCalc;
   Int_t           NJetsCSVwithSF_MultiLepCalc_bSFup;
   Int_t           NJetsCSVwithSF_MultiLepCalc_bSFdn;
   Int_t           NJetsCSVwithSF_MultiLepCalc_lSFup;
   Int_t           NJetsCSVwithSF_MultiLepCalc_lSFdn;
   Int_t           NJetsCSV_JetSubCalc; // DeepJet 
   Int_t           NJetsCSVwithSF_JetSubCalc;
   Int_t           NJetsCSVwithSF_JetSubCalc_bSFup;
   Int_t           NJetsCSVwithSF_JetSubCalc_bSFdn;
   Int_t           NJetsCSVwithSF_JetSubCalc_lSFup;
   Int_t           NJetsCSVwithSF_JetSubCalc_lSFdn;

   vector<int>     maxProb_JetSubCalc_PtOrdered;
   vector<int>     theJetAK8SDSubjetIndex_JetSubCalc_PtOrdered;
   vector<int>     theJetAK8SDSubjetSize_JetSubCalc_PtOrdered;
   vector<int>     NJetsCSVwithSF_JetSubCalc_shifts;
   vector<int>  theJetIndex_JetSubCalc_PtOrdered;
   vector<double>  theJetPt_JetSubCalc_PtOrdered;
   vector<double>  theJetEta_JetSubCalc_PtOrdered;
   vector<double>  theJetPhi_JetSubCalc_PtOrdered;
   vector<double>  theJetEnergy_JetSubCalc_PtOrdered;
   vector<double>  theJetDeepFlavB_JetSubCalc_PtOrdered;
   vector<double>  AK4JetDeepCSVb_MultiLepCalc_PtOrdered;
   vector<double>  AK4JetDeepCSVbb_MultiLepCalc_PtOrdered;
   vector<double>  AK4JetDeepCSVc_MultiLepCalc_PtOrdered;
   vector<double>  AK4JetDeepCSVudsg_MultiLepCalc_PtOrdered;
   vector<double>  AK4JetDeepFlavb_MultiLepCalc_PtOrdered;
   vector<double>  AK4JetDeepFlavbb_MultiLepCalc_PtOrdered;
   vector<double>  AK4JetDeepFlavc_MultiLepCalc_PtOrdered;
   vector<double>  AK4JetDeepFlavg_MultiLepCalc_PtOrdered;
   vector<double>  AK4JetDeepFlavlepb_MultiLepCalc_PtOrdered;
   vector<double>  AK4JetDeepFlavuds_MultiLepCalc_PtOrdered;
   vector<int>     AK4JetBTag_MultiLepCalc_PtOrdered;
   vector<int>     AK4JetBTag_bSFup_MultiLepCalc_PtOrdered;
   vector<int>     AK4JetBTag_bSFdn_MultiLepCalc_PtOrdered;
   vector<int>     AK4JetBTag_lSFup_MultiLepCalc_PtOrdered;
   vector<int>     AK4JetBTag_lSFdn_MultiLepCalc_PtOrdered;
   vector<int>     theJetHFlav_JetSubCalc_PtOrdered;
   vector<int>     theJetPFlav_JetSubCalc_PtOrdered;
   vector<int>     theJetBTag_JetSubCalc_PtOrdered;
   vector<int>     theJetBTag_bSFup_JetSubCalc_PtOrdered;
   vector<int>     theJetBTag_bSFdn_JetSubCalc_PtOrdered;
   vector<int>     theJetBTag_lSFup_JetSubCalc_PtOrdered;
   vector<int>     theJetBTag_lSFdn_JetSubCalc_PtOrdered;

   Float_t         AK4HTpMETpLepPt;
   Float_t         AK4HT;

   Float_t         minMleppJet;
   Float_t         deltaR_lepMinMlj;
   Float_t         minDR_lepJet;
   Float_t         minDR_jetJet;
   Float_t         ptRel_lepJet;
   Float_t         ptRel_lepAK8;
   Float_t         minDPhi_MetJet;
   Float_t         MT_lepMet;
   Float_t         MT_lepMetmod;
   double          deltaR_jetJets;
   vector<double>  deltaR_lepJets;
   vector<double>  minDR_jetJets;
   vector<double>  deltaPhi_lepJets;
   vector<double>  mass_lepJets;

   Float_t         BJetLeadPt;
   Float_t         BJetLeadPt_bSFup;
   Float_t         BJetLeadPt_bSFdn;
   Float_t         BJetLeadPt_lSFup;
   Float_t         BJetLeadPt_lSFdn;
   Float_t         minMleppBjetPt;
   Float_t         minMleppBjet;
   Float_t         minMleppBjet_bSFup;
   Float_t         minMleppBjet_bSFdn;
   Float_t         minMleppBjet_lSFup;
   Float_t         minMleppBjet_lSFdn;
   Float_t         deltaR_lepMinMlb;
   Float_t         deltaR_lepMinMlb_bSFup;
   Float_t         deltaR_lepMinMlb_bSFdn;
   Float_t         deltaR_lepMinMlb_lSFup;
   Float_t         deltaR_lepMinMlb_lSFdn;
   vector<double>  BJetLeadPt_shifts;
   vector<double>  minMleppBjetPt_shifts;
   vector<double>  minMleppBjet_shifts;
   vector<double>  deltaR_lepBJets;
   vector<double>  deltaR_lepBJets_bSFup;
   vector<double>  deltaR_lepBJets_bSFdn;
   vector<double>  deltaR_lepBJets_lSFup;
   vector<double>  deltaR_lepBJets_lSFdn;
   vector<double>  mass_lepBJets;
   vector<double>  mass_lepBJets_bSFup;
   vector<double>  mass_lepBJets_bSFdn;
   vector<double>  mass_lepBJets_lSFup;
   vector<double>  mass_lepBJets_lSFdn;

   Int_t           NJetsAK8_JetSubCalc;
   Float_t         minDR_leadAK8otherAK8;
   Float_t         minDR_lepAK8;
   vector<double>  deltaR_lepAK8s;
   vector<double>  theJetAK8CHSPrunedMass_JetSubCalc_PtOrdered;
   vector<double>  theJetAK8NjettinessTau1_JetSubCalc_PtOrdered;
   vector<double>  theJetAK8NjettinessTau2_JetSubCalc_PtOrdered;
   vector<double>  theJetAK8NjettinessTau3_JetSubCalc_PtOrdered;
   vector<double>  theJetAK8CHSTau1_JetSubCalc_PtOrdered;
   vector<double>  theJetAK8CHSTau2_JetSubCalc_PtOrdered;
   vector<double>  theJetAK8CHSTau3_JetSubCalc_PtOrdered;
   vector<double>  theJetAK8Pt_JetSubCalc_PtOrdered;
   vector<double>  theJetAK8Eta_JetSubCalc_PtOrdered;
   vector<double>  theJetAK8Phi_JetSubCalc_PtOrdered;
   vector<double>  theJetAK8Mass_JetSubCalc_PtOrdered;
   vector<double>  theJetAK8Energy_JetSubCalc_PtOrdered;
   vector<double>  theJetAK8CHSSoftDropMass_JetSubCalc_PtOrdered;
   vector<double>  theJetAK8SoftDropRaw_PtOrdered;
   vector<double>  theJetAK8SoftDropCorr_PtOrdered;
   vector<double>  theJetAK8SoftDrop_PtOrdered;
   vector<double>  theJetAK8DoubleB_JetSubCalc_PtOrdered;
   vector<int>     theJetAK8Wmatch_JetSubCalc_PtOrdered;
   vector<int>     theJetAK8Tmatch_JetSubCalc_PtOrdered;
   vector<int>     theJetAK8Zmatch_JetSubCalc_PtOrdered;
   vector<int>     theJetAK8Hmatch_JetSubCalc_PtOrdered;
   vector<double>  theJetAK8MatchedPt_JetSubCalc_PtOrdered;
   vector<int>     theJetAK8Truth_JetSubCalc_PtOrdered;
   vector<int>     theJetAK8Indx_Wtagged;
   vector<double>  theJetAK8SoftDropRaw_JetSubCalc_PtOrdered;
   vector<double>  theJetAK8SoftDropCorr_JetSubCalc_PtOrdered;
   vector<double>  theJetAK8SoftDrop_JetSubCalc_PtOrdered;
   vector<double>  theJetAK8SoftDrop_JetSubCalc_JMSup_PtOrdered;
   vector<double>  theJetAK8SoftDrop_JetSubCalc_JMSdn_PtOrdered;
   vector<double>  theJetAK8SoftDrop_JetSubCalc_JMRup_PtOrdered;
   vector<double>  theJetAK8SoftDrop_JetSubCalc_JMRdn_PtOrdered;
   vector<int>     theJetAK8SDSubjetNDeepCSVMSF_JetSubCalc_PtOrdered;
   vector<int>     theJetAK8SDSubjetNDeepCSVL_JetSubCalc_PtOrdered;

   Int_t           NJetsWtagged;
   Float_t         WJetLeadPt;
   vector<int>     NJetsWtagged_shifts;

   Int_t           NJetsTtagged;
   Float_t         TJetLeadPt;
   vector<int>     NJetsTtagged_shifts;
   
   Float_t         recLeptonicTopPt;
   Float_t         recLeptonicTopEta;
   Float_t         recLeptonicTopPhi;
   Float_t         recLeptonicTopMass;
   Int_t           recLeptonicTopJetIdx;
   Float_t         genTopPt;
   Float_t         genAntiTopPt;
   Float_t         topPtWeight13TeV;

   Int_t           NresolvedTops1pFakeNoSF;
   Int_t           NresolvedTops2pFakeNoSF;
   Int_t           NresolvedTops5pFakeNoSF;
   Int_t           NresolvedTops10pFakeNoSF;
   Int_t           NresolvedTops1pFake;
   Int_t           NresolvedTops2pFake;
   Int_t           NresolvedTops5pFake;
   Int_t           NresolvedTops10pFake;
   vector<int>     NresolvedTops1pFake_shifts;
   vector<int>     NresolvedTops2pFake_shifts;
   vector<int>     NresolvedTops5pFake_shifts;
   vector<int>     NresolvedTops10pFake_shifts;

   float	   btagCSVWeight;
   float 	   btagCSVWeight_HFup;
   float           btagCSVWeight_HFdn;
   float           btagCSVWeight_LFup;
   float           btagCSVWeight_LFdn;

   float           btagDeepJetWeight;
   float           btagDeepJetWeight_HFup;
   float           btagDeepJetWeight_HFdn;
   float           btagDeepJetWeight_LFup;
   float           btagDeepJetWeight_LFdn;
   float           btagDeepJetWeight_jesup;
   float           btagDeepJetWeight_jesdn;
   float           btagDeepJetWeight_hfstats1up;
   float           btagDeepJetWeight_hfstats1dn;
   float           btagDeepJetWeight_hfstats2up;
   float           btagDeepJetWeight_hfstats2dn;
   float           btagDeepJetWeight_cferr1up;
   float           btagDeepJetWeight_cferr1dn;
   float           btagDeepJetWeight_cferr2up;
   float           btagDeepJetWeight_cferr2dn;
   float           btagDeepJetWeight_lfstats1up;
   float           btagDeepJetWeight_lfstats1dn;
   float           btagDeepJetWeight_lfstats2up;
   float           btagDeepJetWeight_lfstats2dn;
   

   // Declaration of leaf types
   Int_t           lumi_CommonCalc;
   Int_t           nTrueInteractions_MultiLepCalc;
   Int_t           run_CommonCalc;
   Int_t           topNAK4_HOTTaggerCalc;
   Int_t           topNtops_HOTTaggerCalc;
   Long64_t        event_CommonCalc;
   Double_t        HTfromHEPUEP_MultiLepCalc;
   Double_t        L1NonPrefiringProbDown_CommonCalc;
   Double_t        L1NonPrefiringProbUp_CommonCalc;
   Double_t        L1NonPrefiringProb_CommonCalc;
   Double_t        MCWeight_MultiLepCalc;
   Double_t        corr_met_MultiLepCalc;
   Double_t        corr_met_phi_MultiLepCalc;
   Double_t        corr_metmod_MultiLepCalc;
   Double_t        corr_metmod_phi_MultiLepCalc;
   Double_t        ttbarMass_TTbarMassCalc;
   vector<int>     *AK4JetBTag_MultiLepCalc;
   vector<int>     *AK4JetBTag_bSFdn_MultiLepCalc;
   vector<int>     *AK4JetBTag_bSFup_MultiLepCalc;
   vector<int>     *AK4JetBTag_lSFdn_MultiLepCalc;
   vector<int>     *AK4JetBTag_lSFup_MultiLepCalc;
   vector<int>     *HadronicVHtID_JetSubCalc;
   vector<int>     *LHEweightids_MultiLepCalc;
   vector<int>     *allTopsID_TTbarMassCalc;
   vector<int>     *allTopsStatus_TTbarMassCalc;
   vector<int>     *elMother_id_MultiLepCalc;
   vector<int>     *elNumberOfMothers_MultiLepCalc;
   vector<int>     *genID_MultiLepCalc;
   vector<int>     *genIndex_MultiLepCalc;
   vector<int>     *genMotherID_MultiLepCalc;
   vector<int>     *genMotherIndex_MultiLepCalc;
   vector<int>     *genStatus_MultiLepCalc;
   vector<int>     *genTtbarIdCategory_TTbarMassCalc;
   vector<int>     *genTtbarId_TTbarMassCalc;
   vector<int>     *maxProb_JetSubCalc;
   vector<int>     *muMother_id_MultiLepCalc;
   vector<int>     *muNumberOfMothers_MultiLepCalc;
   vector<int>     *theJetAK8SDSubjetHFlav_JetSubCalc;
   vector<int>     *theJetAK8SDSubjetIndex_JetSubCalc;
   vector<int>     *theJetAK8SDSubjetNDeepCSVL_JetSubCalc;
   vector<int>     *theJetAK8SDSubjetNDeepCSVMSF_JetSubCalc;
   vector<int>     *theJetAK8SDSubjetSize_JetSubCalc;
   vector<int>     *theJetBTag_JetSubCalc;
   vector<int>     *theJetBTag_bSFdn_JetSubCalc;
   vector<int>     *theJetBTag_bSFup_JetSubCalc;
   vector<int>     *theJetBTag_lSFdn_JetSubCalc;
   vector<int>     *theJetBTag_lSFup_JetSubCalc;
   vector<int>     *theJetHFlav_JetSubCalc;
   vector<int>     *theJetPFlav_JetSubCalc;
   vector<int>     *topID_TTbarMassCalc;
   vector<int>     *topJet1Index_HOTTaggerCalc;
   vector<int>     *topJet2Index_HOTTaggerCalc;
   vector<int>     *topJet3Index_HOTTaggerCalc;
   vector<int>     *topWID_TTbarMassCalc;
   vector<int>     *topbID_TTbarMassCalc;
   vector<int>     *viSelMCTriggersEl_MultiLepCalc;
   vector<int>     *viSelMCTriggersHad_MultiLepCalc;
   vector<int>     *viSelMCTriggersMu_MultiLepCalc;
   vector<int>     *viSelTriggersEl_MultiLepCalc;
   vector<int>     *viSelTriggersHad_MultiLepCalc;
   vector<int>     *viSelTriggersMu_MultiLepCalc;
   vector<double>  *AK4JetDeepCSVb_MultiLepCalc;
   vector<double>  *AK4JetDeepCSVbb_MultiLepCalc;
   vector<double>  *AK4JetDeepCSVc_MultiLepCalc;
   vector<double>  *AK4JetDeepCSVudsg_MultiLepCalc;
   vector<double>  *AK4JetDeepFlavb_MultiLepCalc;
   vector<double>  *AK4JetDeepFlavbb_MultiLepCalc;
   vector<double>  *AK4JetDeepFlavc_MultiLepCalc;
   vector<double>  *AK4JetDeepFlavg_MultiLepCalc;
   vector<double>  *AK4JetDeepFlavlepb_MultiLepCalc;
   vector<double>  *AK4JetDeepFlavuds_MultiLepCalc;
   vector<double>  *HadronicVHtD0E_JetSubCalc;
   vector<double>  *HadronicVHtD0Eta_JetSubCalc;
   vector<double>  *HadronicVHtD0Phi_JetSubCalc;
   vector<double>  *HadronicVHtD0Pt_JetSubCalc;
   vector<double>  *HadronicVHtD1E_JetSubCalc;
   vector<double>  *HadronicVHtD1Eta_JetSubCalc;
   vector<double>  *HadronicVHtD1Phi_JetSubCalc;
   vector<double>  *HadronicVHtD1Pt_JetSubCalc;
   vector<double>  *HadronicVHtD2E_JetSubCalc;
   vector<double>  *HadronicVHtD2Eta_JetSubCalc;
   vector<double>  *HadronicVHtD2Phi_JetSubCalc;
   vector<double>  *HadronicVHtD2Pt_JetSubCalc;
   vector<double>  *HadronicVHtEnergy_JetSubCalc;
   vector<double>  *HadronicVHtEta_JetSubCalc;
   vector<double>  *HadronicVHtPhi_JetSubCalc;
   vector<double>  *HadronicVHtPt_JetSubCalc;
   vector<double>  *LHEweights_MultiLepCalc;
   vector<double>  *NewPDFweights_MultiLepCalc;
   vector<double>  *allTopsEnergy_TTbarMassCalc;
   vector<double>  *allTopsEta_TTbarMassCalc;
   vector<double>  *allTopsPhi_TTbarMassCalc;
   vector<double>  *allTopsPt_TTbarMassCalc;
   vector<double>  *elEnergy_MultiLepCalc;
   vector<double>  *elEta_MultiLepCalc;
   vector<double>  *elMiniIso_MultiLepCalc;
   vector<double>  *elPhi_MultiLepCalc;
   vector<double>  *elPt_MultiLepCalc;
   vector<double>  *elRelIso_MultiLepCalc;
   vector<double>  *evtWeightsMC_MultiLepCalc;
   vector<double>  *genEnergy_MultiLepCalc;
   vector<double>  *genEta_MultiLepCalc;
   vector<double>  *genJetEnergyNoClean_MultiLepCalc;
   vector<double>  *genJetEnergy_MultiLepCalc;
   vector<double>  *genJetEtaNoClean_MultiLepCalc;
   vector<double>  *genJetEta_MultiLepCalc;
   vector<double>  *genJetPhiNoClean_MultiLepCalc;
   vector<double>  *genJetPhi_MultiLepCalc;
   vector<double>  *genJetPtNoClean_MultiLepCalc;
   vector<double>  *genJetPt_MultiLepCalc;
   vector<double>  *genPhi_MultiLepCalc;
   vector<double>  *genPt_MultiLepCalc;
   vector<double>  *muEnergy_MultiLepCalc;
   vector<double>  *muEta_MultiLepCalc;
   vector<double>  *muMiniIso_MultiLepCalc;
   vector<double>  *muPhi_MultiLepCalc;
   vector<double>  *muPt_MultiLepCalc;
   vector<double>  *muRelIso_MultiLepCalc;
   vector<double>  *theJetAK8CHSPrunedMass_JetSubCalc;
   vector<double>  *theJetAK8CHSSoftDropMass_JetSubCalc;
   vector<double>  *theJetAK8CHSTau1_JetSubCalc;
   vector<double>  *theJetAK8CHSTau2_JetSubCalc;
   vector<double>  *theJetAK8CHSTau3_JetSubCalc;
   vector<double>  *theJetAK8DoubleB_JetSubCalc;
   vector<double>  *theJetAK8Energy_JetSubCalc;
   vector<double>  *theJetAK8Eta_JetSubCalc;
   vector<double>  *theJetAK8Mass_JetSubCalc;
   vector<double>  *theJetAK8NjettinessTau1_JetSubCalc;
   vector<double>  *theJetAK8NjettinessTau2_JetSubCalc;
   vector<double>  *theJetAK8NjettinessTau3_JetSubCalc;
   vector<double>  *theJetAK8Phi_JetSubCalc;
   vector<double>  *theJetAK8Pt_JetSubCalc;
   vector<double>  *theJetAK8SoftDropCorr_JetSubCalc;
   vector<double>  *theJetAK8SoftDropRaw_JetSubCalc;
   vector<double>  *theJetAK8SoftDrop_JMRdn_JetSubCalc;
   vector<double>  *theJetAK8SoftDrop_JMRup_JetSubCalc;
   vector<double>  *theJetAK8SoftDrop_JMSdn_JetSubCalc;
   vector<double>  *theJetAK8SoftDrop_JMSup_JetSubCalc;
   vector<double>  *theJetAK8SoftDrop_JetSubCalc;
   vector<double>  *theJetDeepFlavB_JetSubCalc;
   vector<double>  *theJetEnergy_JetSubCalc;
   vector<double>  *theJetEta_JetSubCalc;
   vector<double>  *theJetPhi_JetSubCalc;
   vector<double>  *theJetPt_JetSubCalc;
   vector<double>  *topBestGenEnergy_HOTTaggerCalc;
   vector<double>  *topBestGenEta_HOTTaggerCalc;
   vector<double>  *topBestGenPhi_HOTaggerCalc;
   vector<double>  *topBestGenPt_HOTTaggerCalc;
   vector<double>  *topDRmax_HOTTaggerCalc;
   vector<double>  *topDThetaMax_HOTTaggerCalc;
   vector<double>  *topDThetaMin_HOTTaggerCalc;
   vector<double>  *topDiscriminator_HOTTaggerCalc;
   vector<double>  *topEnergy_TTbarMassCalc;
   vector<double>  *topEta_HOTTaggerCalc;
   vector<double>  *topEta_TTbarMassCalc;
   vector<double>  *topMass_HOTTaggerCalc;
   vector<double>  *topMass_TTbarMassCalc;
   vector<double>  *topNconstituents_HOTTaggerCalc;
   vector<double>  *topPhi_HOTTaggerCalc;
   vector<double>  *topPhi_TTbarMassCalc;
   vector<double>  *topPt_HOTTaggerCalc;
   vector<double>  *topPt_TTbarMassCalc;
   vector<double>  *topType_HOTTaggerCalc;
   vector<double>  *topWEnergy_TTbarMassCalc;
   vector<double>  *topWEta_TTbarMassCalc;
   vector<double>  *topWPhi_TTbarMassCalc;
   vector<double>  *topWPt_TTbarMassCalc;
   vector<double>  *topbEnergy_TTbarMassCalc;
   vector<double>  *topbEta_TTbarMassCalc;
   vector<double>  *topbPhi_TTbarMassCalc;
   vector<double>  *topbPt_TTbarMassCalc;
   vector<string>  *vsSelMCTriggersEl_MultiLepCalc;
   vector<string>  *vsSelMCTriggersHad_MultiLepCalc;
   vector<string>  *vsSelMCTriggersMu_MultiLepCalc;
   vector<string>  *vsSelTriggersEl_MultiLepCalc;
   vector<string>  *vsSelTriggersHad_MultiLepCalc;
   vector<string>  *vsSelTriggersMu_MultiLepCalc;

   // List of branches
   TBranch        *b_lumi_CommonCalc;   //!
   TBranch        *b_nTrueInteractions_MultiLepCalc;   //!
   TBranch        *b_run_CommonCalc;   //!
   TBranch        *b_topNAK4_HOTTaggerCalc;   //!
   TBranch        *b_topNtops_HOTTaggerCalc;   //!
   TBranch        *b_event_CommonCalc;   //!
   TBranch        *b_HTfromHEPUEP_MultiLepCalc;   //!
   TBranch        *b_L1NonPrefiringProbDown_CommonCalc;   //!
   TBranch        *b_L1NonPrefiringProbUp_CommonCalc;   //!
   TBranch        *b_L1NonPrefiringProb_CommonCalc;   //!
   TBranch        *b_MCWeight_MultiLepCalc;   //!
   TBranch        *b_corr_met_MultiLepCalc;   //!
   TBranch        *b_corr_met_phi_MultiLepCalc;   //!
   TBranch        *b_corr_metmod_MultiLepCalc;   //!
   TBranch        *b_corr_metmod_phi_MultiLepCalc;   //!
   TBranch        *b_ttbarMass_TTbarMassCalc;   //!
   TBranch        *b_AK4JetBTag_MultiLepCalc;   //!
   TBranch        *b_AK4JetBTag_bSFdn_MultiLepCalc;   //!
   TBranch        *b_AK4JetBTag_bSFup_MultiLepCalc;   //!
   TBranch        *b_AK4JetBTag_lSFdn_MultiLepCalc;   //!
   TBranch        *b_AK4JetBTag_lSFup_MultiLepCalc;   //!
   TBranch        *b_HadronicVHtID_JetSubCalc;   //!
   TBranch        *b_LHEweightids_MultiLepCalc;   //!
   TBranch        *b_allTopsID_TTbarMassCalc;   //!
   TBranch        *b_allTopsStatus_TTbarMassCalc;   //!
   TBranch        *b_elNumberOfMothers_MultiLepCalc;   //!
   TBranch        *b_genID_MultiLepCalc;   //!
   TBranch        *b_genIndex_MultiLepCalc;   //!
   TBranch        *b_genMotherID_MultiLepCalc;   //!
   TBranch        *b_genMotherIndex_MultiLepCalc;   //!
   TBranch        *b_genStatus_MultiLepCalc;   //!
   TBranch        *b_genTtbarIdCategory_TTbarMassCalc;   //!
   TBranch        *b_genTtbarId_TTbarMassCalc;   //!
   TBranch        *b_maxProb_JetSubCalc;   //!
   TBranch        *b_muMother_id_MultiLepCalc;   //!
   TBranch        *b_muNumberOfMothers_MultiLepCalc;   //!
   TBranch        *b_theJetAK8SDSubjetHFlav_JetSubCalc;   //!
   TBranch        *b_theJetAK8SDSubjetIndex_JetSubCalc;   //!
   TBranch        *b_theJetAK8SDSubjetNDeepCSVL_JetSubCalc;   //!
   TBranch        *b_theJetAK8SDSubjetNDeepCSVMSF_JetSubCalc;   //!
   TBranch        *b_theJetAK8SDSubjetSize_JetSubCalc;   //!
   TBranch        *b_theJetBTag_JetSubCalc;   //!
   TBranch        *b_theJetBTag_bSFdn_JetSubCalc;   //!
   TBranch        *b_theJetBTag_bSFup_JetSubCalc;   //!
   TBranch        *b_theJetBTag_lSFdn_JetSubCalc;   //!
   TBranch        *b_theJetBTag_lSFup_JetSubCalc;   //!
   TBranch        *b_theJetHFlav_JetSubCalc;   //!
   TBranch        *b_theJetPFlav_JetSubCalc;   //!
   TBranch        *b_topID_TTbarMassCalc;   //!
   TBranch        *b_topJet1Index_HOTTaggerCalc;   //!
   TBranch        *b_topJet2Index_HOTTaggerCalc;   //!
   TBranch        *b_topJet3Index_HOTTaggerCalc;   //!
   TBranch        *b_topWID_TTbarMassCalc;   //!
   TBranch        *b_topbID_TTbarMassCalc;   //!
   TBranch        *b_viSelMCTriggersEl_MultiLepCalc;   //!
   TBranch        *b_viSelMCTriggersHad_MultiLepCalc;   //!
   TBranch        *b_viSelMCTriggersMu_MultiLepCalc;   //!
   TBranch        *b_viSelTriggersEl_MultiLepCalc;   //!
   TBranch        *b_viSelTriggersHad_MultiLepCalc;   //!
   TBranch        *b_viSelTriggersMu_MultiLepCalc;   //!
   TBranch        *b_AK4JetDeepCSVb_MultiLepCalc;   //!
   TBranch        *b_AK4JetDeepCSVbb_MultiLepCalc;   //!
   TBranch        *b_AK4JetDeepCSVc_MultiLepCalc;   //!
   TBranch        *b_AK4JetDeepCSVudsg_MultiLepCalc;   //!
   TBranch        *b_AK4JetDeepFlavb_MultiLepCalc;   //!
   TBranch        *b_AK4JetDeepFlavbb_MultiLepCalc;   //!
   TBranch        *b_AK4JetDeepFlavc_MultiLepCalc;   //!
   TBranch        *b_AK4JetDeepFlavg_MultiLepCalc;   //!
   TBranch        *b_AK4JetDeepFlavlepb_MultiLepCalc;   //!
   TBranch        *b_AK4JetDeepFlavuds_MultiLepCalc;   //!
   TBranch        *b_HadronicVHtD0E_JetSubCalc;   //!
   TBranch        *b_HadronicVHtD0Eta_JetSubCalc;   //!
   TBranch        *b_HadronicVHtD0Phi_JetSubCalc;   //!
   TBranch        *b_HadronicVHtD0Pt_JetSubCalc;   //!
   TBranch        *b_HadronicVHtD1E_JetSubCalc;   //!
   TBranch        *b_HadronicVHtD1Eta_JetSubCalc;   //!
   TBranch        *b_HadronicVHtD1Phi_JetSubCalc;   //!
   TBranch        *b_HadronicVHtD1Pt_JetSubCalc;   //!
   TBranch        *b_HadronicVHtD2E_JetSubCalc;   //!
   TBranch        *b_HadronicVHtD2Eta_JetSubCalc;   //!
   TBranch        *b_HadronicVHtD2Phi_JetSubCalc;   //!
   TBranch        *b_HadronicVHtD2Pt_JetSubCalc;   //!
   TBranch        *b_HadronicVHtEnergy_JetSubCalc;   //!
   TBranch        *b_HadronicVHtEta_JetSubCalc;   //!
   TBranch        *b_HadronicVHtPhi_JetSubCalc;   //!
   TBranch        *b_HadronicVHtPt_JetSubCalc;   //!
   TBranch        *b_LHEweights_MultiLepCalc;   //!
   TBranch        *b_NewPDFweights_MultiLepCalc;   //!
   TBranch        *b_allTopsEnergy_TTbarMassCalc;   //!
   TBranch        *b_allTopsEta_TTbarMassCalc;   //!
   TBranch        *b_allTopsPhi_TTbarMassCalc;   //!
   TBranch        *b_allTopsPt_TTbarMassCalc;   //!
   TBranch        *b_elEnergy_MultiLepCalc;   //!
   TBranch        *b_elEta_MultiLepCalc;   //!
   TBranch        *b_elMother_id_MultiLepCalc;
   TBranch        *b_elMiniIso_MultiLepCalc;   //!
   TBranch        *b_elPhi_MultiLepCalc;   //!
   TBranch        *b_elPt_MultiLepCalc;   //!
   TBranch        *b_elRelIso_MultiLepCalc;   //!
   TBranch        *b_evtWeightsMC_MultiLepCalc;   //!
   TBranch        *b_genEnergy_MultiLepCalc;   //!
   TBranch        *b_genEta_MultiLepCalc;   //!
   TBranch        *b_genJetEnergyNoClean_MultiLepCalc;   //!
   TBranch        *b_genJetEnergy_MultiLepCalc;   //!
   TBranch        *b_genJetEtaNoClean_MultiLepCalc;   //!
   TBranch        *b_genJetEta_MultiLepCalc;   //!
   TBranch        *b_genJetPhiNoClean_MultiLepCalc;   //!
   TBranch        *b_genJetPhi_MultiLepCalc;   //!
   TBranch        *b_genJetPtNoClean_MultiLepCalc;   //!
   TBranch        *b_genJetPt_MultiLepCalc;   //!
   TBranch        *b_genPhi_MultiLepCalc;   //!
   TBranch        *b_genPt_MultiLepCalc;   //!
   TBranch        *b_muEnergy_MultiLepCalc;   //!
   TBranch        *b_muEta_MultiLepCalc;   //!
   TBranch        *b_muMiniIso_MultiLepCalc;   //!
   TBranch        *b_muPhi_MultiLepCalc;   //!
   TBranch        *b_muPt_MultiLepCalc;   //!
   TBranch        *b_muRelIso_MultiLepCalc;   //!
   TBranch        *b_theJetAK8CHSPrunedMass_JetSubCalc;   //!
   TBranch        *b_theJetAK8CHSSoftDropMass_JetSubCalc;   //!
   TBranch        *b_theJetAK8CHSTau1_JetSubCalc;   //!
   TBranch        *b_theJetAK8CHSTau2_JetSubCalc;   //!
   TBranch        *b_theJetAK8CHSTau3_JetSubCalc;   //!
   TBranch        *b_theJetAK8DoubleB_JetSubCalc;   //!
   TBranch        *b_theJetAK8Energy_JetSubCalc;   //!
   TBranch        *b_theJetAK8Eta_JetSubCalc;   //!
   TBranch        *b_theJetAK8Mass_JetSubCalc;   //!
   TBranch        *b_theJetAK8NjettinessTau1_JetSubCalc;   //!
   TBranch        *b_theJetAK8NjettinessTau2_JetSubCalc;   //!
   TBranch        *b_theJetAK8NjettinessTau3_JetSubCalc;   //!
   TBranch        *b_theJetAK8Phi_JetSubCalc;   //!
   TBranch        *b_theJetAK8Pt_JetSubCalc;   //!
   TBranch        *b_theJetAK8SoftDropCorr_JetSubCalc;   //!
   TBranch        *b_theJetAK8SoftDropRaw_JetSubCalc;   //!
   TBranch        *b_theJetAK8SoftDrop_JMRdn_JetSubCalc;   //!
   TBranch        *b_theJetAK8SoftDrop_JMRup_JetSubCalc;   //!
   TBranch        *b_theJetAK8SoftDrop_JMSdn_JetSubCalc;   //!
   TBranch        *b_theJetAK8SoftDrop_JMSup_JetSubCalc;   //!
   TBranch        *b_theJetAK8SoftDrop_JetSubCalc;   //!
   TBranch        *b_theJetDeepFlavB_JetSubCalc;   //!
   TBranch        *b_theJetEnergy_JetSubCalc;   //!
   TBranch        *b_theJetEta_JetSubCalc;   //!
   TBranch        *b_theJetPhi_JetSubCalc;   //!
   TBranch        *b_theJetPt_JetSubCalc;   //!
   TBranch        *b_topBestGenEnergy_HOTTaggerCalc;  //!
   TBranch        *b_topBestGenEta_HOTTaggerCalc;  //!
   TBranch        *b_topBestGenPhi_HOTTaggerCalc; //!
   TBranch        *b_topBestGenPt_HOTTaggerCalc; //!
   TBranch        *b_topDRmax_HOTTaggerCalc;   //!
   TBranch        *b_topDThetaMax_HOTTaggerCalc;   //!
   TBranch        *b_topDThetaMin_HOTTaggerCalc;   //!
   TBranch        *b_topDiscriminator_HOTTaggerCalc;   //!
   TBranch        *b_topEnergy_TTbarMassCalc;   //!
   TBranch        *b_topEta_HOTTaggerCalc;   //!
   TBranch        *b_topEta_TTbarMassCalc;   //!
   TBranch        *b_topMass_HOTTaggerCalc;   //!
   TBranch        *b_topMass_TTbarMassCalc;   //!
   TBranch        *b_topNconstituents_HOTTaggerCalc;   //!
   TBranch        *b_topPhi_HOTTaggerCalc;   //!
   TBranch        *b_topPhi_TTbarMassCalc;   //!
   TBranch        *b_topPt_HOTTaggerCalc;   //!
   TBranch        *b_topPt_TTbarMassCalc;   //!
   TBranch        *b_topType_HOTTaggerCalc;   //!
   TBranch        *b_topWEnergy_TTbarMassCalc;   //!
   TBranch        *b_topWEta_TTbarMassCalc;   //!
   TBranch        *b_topWPhi_TTbarMassCalc;   //!
   TBranch        *b_topWPt_TTbarMassCalc;   //!
   TBranch        *b_topbEnergy_TTbarMassCalc;   //!
   TBranch        *b_topbEta_TTbarMassCalc;   //!
   TBranch        *b_topbPhi_TTbarMassCalc;   //!
   TBranch        *b_topbPt_TTbarMassCalc;   //!
   TBranch        *b_vsSelMCTriggersEl_MultiLepCalc;   //!
   TBranch        *b_vsSelMCTriggersHad_MultiLepCalc;   //!
   TBranch        *b_vsSelMCTriggersMu_MultiLepCalc;   //!
   TBranch        *b_vsSelTriggersEl_MultiLepCalc;   //!
   TBranch        *b_vsSelTriggersHad_MultiLepCalc;   //!
   TBranch        *b_vsSelTriggersMu_MultiLepCalc;   //!
 
   step1(TString inputFileName, TString outputFileName, Int_t Year_);
   virtual ~step1();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop(TString inTreeName, TString outTreeName, const BTagCalibrationForLJMet* calib, const BTagCalibrationForLJMet* calib_DJ);
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
   virtual void     saveHistograms();
   bool             applySF(bool& isTagged, float tag_SF, float tag_eff);
};

#endif

#ifdef step1_cxx
step1::step1(TString inputFileName, TString outputFileName, Int_t Year_) : inputTree(0), inputFile(0), outputFile(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.

  Year = Year_;
  isSig  = (inputFileName.Contains("TTTW") || inputFileName.Contains("TTTJ") );
  if(isSig){
    isTTTX = true;
    SigMass = -1;
  }  
  else SigMass = -1;
  
  if(inputFileName.Contains("17B")) Era = "17B";
  else if(inputFileName.Contains("17C")) Era = "17C";
  else if(inputFileName.Contains("17D")) Era = "17DEF";
  else if(inputFileName.Contains("17E")) Era = "17DEF";
  else if(inputFileName.Contains("17F")) Era = "17DEF";
  else if(inputFileName.Contains("18A")) Era = "18AB";
  else if(inputFileName.Contains("18B")) Era = "18AB";
  else if(inputFileName.Contains("18C")) Era = "18CD";
  else if(inputFileName.Contains("18D")) Era = "18CD";
  else Era = "";
  
  isMadgraphBkg = (inputFileName.Contains("QCD") || inputFileName.Contains("madgraphMLM"));
  isTOP = ( inputFileName.Contains("ST") || inputFileName.Contains("ttZ") || inputFileName.Contains("ttW") || inputFileName.Contains("ttH") || inputFileName.Contains("TTTo"));
  isTT = inputFileName.Contains( "TTTo" );
  if( isSig ) isTT = false;
  isTTToSemiLeptonHT500Njet9 = inputFileName.Contains( "TTToSemiLepton_HT500Njet9_Tune" );
  isST = ( inputFileName.Contains( "ST_t-channel" ) || inputFileName.Contains( "ST_tW" ) || inputFileName.Contains( "ST_s-channel" ));
  isSTt = inputFileName.Contains( "ST_t-channel" );
  isSTtW = inputFileName.Contains( "ST_tW" );
  isTTV = ( inputFileName.Contains( "TTZTo" ) || inputFileName.Contains("TTWJetsTo") );
  isTTHbb = inputFileName.Contains( "ttHTobb_" );
  isTTHnonbb = inputFileName.Contains( "ttHToNonbb_" );
  isTTTT = inputFileName.Contains( "TTTT" );
  isTTVV = (inputFileName.Contains("TTHH") || inputFileName.Contains("TTWH") || inputFileName.Contains("TTWW") || inputFileName.Contains("TTWZ") || inputFileName.Contains("TTZH") || inputFileName.Contains("TTZZ"));
  isVV = (inputFileName.Contains( "WW_" ) || inputFileName.Contains( "WZ_" ) || inputFileName.Contains( "ZZ_" ));
  isMC = !( inputFileName.Contains("Single") || inputFileName.Contains("Data18") || inputFileName.Contains( "Egamma" ) );
  isSM = inputFileName.Contains("SingleMuon");
  isSE = (inputFileName.Contains("SingleElectron") || inputFileName.Contains("EGamma"));
          	  
  isTTSemilepIncHT0Njet0 = outputFileName.Contains("HT0Njet0");
  isTTSemilepIncHT500Njet9 = outputFileName.Contains("HT500Njet9");
  if(inputFileName.Contains("HT500Njet9")) isTTSemilepIncHT500Njet9 = false;
  outTTBB = outputFileName.Contains("_ttbb");
  outTT2B = outputFileName.Contains("_tt2b");
  outTT1B = outputFileName.Contains("_tt1b");
  outTTCC = outputFileName.Contains("_ttcc");
  outTTLF = outputFileName.Contains("_ttjj");
    
  std::cout << ">> Opening file: " << inputFileName <<std::endl;
  //Get the sample name from "inputFileName" for pileupWeights
  sample_ = inputFileName;
  Int_t slash = sample_.Last('/');
  sample_.Remove(0,slash+1);
  Int_t uscore = sample_.Last('_');
  Int_t thelength = sample_.Length();
  sample_.Remove(uscore,thelength);
  sample = (std::string)sample_;
  
  if(!(inputFile=TFile::Open(inputFileName))){
    std::cout<<"[WARN] File doesn't exist. Exiting..." << std::endl;
    exit(1);
  }
  
  outputFile = new TFile(outputFileName,"RECREATE");   
  
}

step1::~step1()
{
   if (!inputTree) return;
   delete inputTree->GetCurrentFile();
}

Int_t step1::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!inputTree) return 0;
   return inputTree->GetEntry(entry);
}
Long64_t step1::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!inputTree) return -5;
   Long64_t centry = inputTree->LoadTree(entry);
   if (centry <= 0) return centry;
   if (inputTree->GetTreeNumber() != fCurrent) {
      fCurrent = inputTree->GetTreeNumber();
      Notify();
   }
   return centry;
}

void step1::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   AK4JetBTag_MultiLepCalc = 0;
   AK4JetBTag_bSFdn_MultiLepCalc = 0;
   AK4JetBTag_bSFup_MultiLepCalc = 0;
   AK4JetBTag_lSFdn_MultiLepCalc = 0;
   AK4JetBTag_lSFup_MultiLepCalc = 0;
   HadronicVHtID_JetSubCalc = 0;
   allTopsID_TTbarMassCalc = 0;
   allTopsStatus_TTbarMassCalc = 0;
   elNumberOfMothers_MultiLepCalc = 0;
   genID_MultiLepCalc = 0;
   genIndex_MultiLepCalc = 0;
   genMotherID_MultiLepCalc = 0;
   genMotherIndex_MultiLepCalc = 0;
   genStatus_MultiLepCalc = 0;
   genTtbarIdCategory_TTbarMassCalc = 0;
   genTtbarId_TTbarMassCalc = 0;
   maxProb_JetSubCalc = 0;
   muMother_id_MultiLepCalc = 0;
   muNumberOfMothers_MultiLepCalc = 0;
   theJetAK8SDSubjetHFlav_JetSubCalc = 0;
   theJetAK8SDSubjetIndex_JetSubCalc = 0;
   theJetAK8SDSubjetNDeepCSVL_JetSubCalc = 0;
   theJetAK8SDSubjetNDeepCSVMSF_JetSubCalc = 0;
   theJetAK8SDSubjetSize_JetSubCalc = 0;
   theJetBTag_JetSubCalc = 0;
   theJetBTag_bSFdn_JetSubCalc = 0;
   theJetBTag_bSFup_JetSubCalc = 0;
   theJetBTag_lSFdn_JetSubCalc = 0;
   theJetBTag_lSFup_JetSubCalc = 0;
   theJetHFlav_JetSubCalc = 0;
   theJetPFlav_JetSubCalc = 0;
   topID_TTbarMassCalc = 0;
   topJet1Index_HOTTaggerCalc = 0;
   topJet2Index_HOTTaggerCalc = 0;
   topJet3Index_HOTTaggerCalc = 0;
   topWID_TTbarMassCalc = 0;
   topbID_TTbarMassCalc = 0;
   viSelMCTriggersEl_MultiLepCalc = 0;
   viSelMCTriggersHad_MultiLepCalc = 0;
   viSelMCTriggersMu_MultiLepCalc = 0;
   viSelTriggersEl_MultiLepCalc = 0;
   viSelTriggersHad_MultiLepCalc = 0;
   viSelTriggersMu_MultiLepCalc = 0;
   AK4JetDeepCSVb_MultiLepCalc = 0;
   AK4JetDeepCSVbb_MultiLepCalc = 0;
   AK4JetDeepCSVc_MultiLepCalc = 0;
   AK4JetDeepCSVudsg_MultiLepCalc = 0;
   AK4JetDeepFlavb_MultiLepCalc = 0;
   AK4JetDeepFlavbb_MultiLepCalc = 0;
   AK4JetDeepFlavc_MultiLepCalc = 0;
   AK4JetDeepFlavg_MultiLepCalc = 0;
   AK4JetDeepFlavlepb_MultiLepCalc = 0;
   AK4JetDeepFlavuds_MultiLepCalc = 0;
   HadronicVHtD0E_JetSubCalc = 0;
   HadronicVHtD0Eta_JetSubCalc = 0;
   HadronicVHtD0Phi_JetSubCalc = 0;
   HadronicVHtD0Pt_JetSubCalc = 0;
   HadronicVHtD1E_JetSubCalc = 0;
   HadronicVHtD1Eta_JetSubCalc = 0;
   HadronicVHtD1Phi_JetSubCalc = 0;
   HadronicVHtD1Pt_JetSubCalc = 0;
   HadronicVHtD2E_JetSubCalc = 0;
   HadronicVHtD2Eta_JetSubCalc = 0;
   HadronicVHtD2Phi_JetSubCalc = 0;
   HadronicVHtD2Pt_JetSubCalc = 0;
   HadronicVHtEnergy_JetSubCalc = 0;
   HadronicVHtEta_JetSubCalc = 0;
   HadronicVHtPhi_JetSubCalc = 0;
   HadronicVHtPt_JetSubCalc = 0;
   LHEweights_MultiLepCalc = 0;
   NewPDFweights_MultiLepCalc = 0;
   allTopsEnergy_TTbarMassCalc = 0;
   allTopsEta_TTbarMassCalc = 0;
   allTopsPhi_TTbarMassCalc = 0;
   allTopsPt_TTbarMassCalc = 0;
   elEnergy_MultiLepCalc = 0;
   elEta_MultiLepCalc = 0;
   elMother_id_MultiLepCalc = 0;
   elMiniIso_MultiLepCalc = 0;
   elPhi_MultiLepCalc = 0;
   elPt_MultiLepCalc = 0;
   elRelIso_MultiLepCalc = 0;
   evtWeightsMC_MultiLepCalc = 0;
   genEnergy_MultiLepCalc = 0;
   genEta_MultiLepCalc = 0;
   genJetEnergyNoClean_MultiLepCalc = 0;
   genJetEnergy_MultiLepCalc = 0;
   genJetEtaNoClean_MultiLepCalc = 0;
   genJetEta_MultiLepCalc = 0;
   genJetPhiNoClean_MultiLepCalc = 0;
   genJetPhi_MultiLepCalc = 0;
   genJetPtNoClean_MultiLepCalc = 0;
   genJetPt_MultiLepCalc = 0;
   genPhi_MultiLepCalc = 0;
   genPt_MultiLepCalc = 0;
   muEnergy_MultiLepCalc = 0;
   muEta_MultiLepCalc = 0;
   muMiniIso_MultiLepCalc = 0;
   muPhi_MultiLepCalc = 0;
   muPt_MultiLepCalc = 0;
   muRelIso_MultiLepCalc = 0;
   theJetAK8CHSPrunedMass_JetSubCalc = 0;
   theJetAK8CHSSoftDropMass_JetSubCalc = 0;
   theJetAK8CHSTau1_JetSubCalc = 0;
   theJetAK8CHSTau2_JetSubCalc = 0;
   theJetAK8CHSTau3_JetSubCalc = 0;
   theJetAK8DoubleB_JetSubCalc = 0;
   theJetAK8Energy_JetSubCalc = 0;
   theJetAK8Eta_JetSubCalc = 0;
   theJetAK8Mass_JetSubCalc = 0;
   theJetAK8NjettinessTau1_JetSubCalc = 0;
   theJetAK8NjettinessTau2_JetSubCalc = 0;
   theJetAK8NjettinessTau3_JetSubCalc = 0;
   theJetAK8Phi_JetSubCalc = 0;
   theJetAK8Pt_JetSubCalc = 0;
   theJetAK8SoftDropCorr_JetSubCalc = 0;
   theJetAK8SoftDropRaw_JetSubCalc = 0;
   theJetAK8SoftDrop_JMRdn_JetSubCalc = 0;
   theJetAK8SoftDrop_JMRup_JetSubCalc = 0;
   theJetAK8SoftDrop_JMSdn_JetSubCalc = 0;
   theJetAK8SoftDrop_JMSup_JetSubCalc = 0;
   theJetAK8SoftDrop_JetSubCalc = 0;
   theJetDeepFlavB_JetSubCalc = 0;
   theJetEnergy_JetSubCalc = 0;
   theJetEta_JetSubCalc = 0;
   theJetPhi_JetSubCalc = 0;
   theJetPt_JetSubCalc = 0;
   topBestGenEnergy_HOTTaggerCalc = 0;
   topBestGenEta_HOTTaggerCalc = 0;
   topBestGenPhi_HOTTaggerCalc = 0;
   topBestGenPt_HOTTaggerCalc = 0;
   topDRmax_HOTTaggerCalc = 0;
   topDThetaMax_HOTTaggerCalc = 0;
   topDThetaMin_HOTTaggerCalc = 0;
   topDiscriminator_HOTTaggerCalc = 0;
   topEnergy_TTbarMassCalc = 0;
   topEta_HOTTaggerCalc = 0;
   topEta_TTbarMassCalc = 0;
   topMass_HOTTaggerCalc = 0;
   topMass_TTbarMassCalc = 0;
   topNconstituents_HOTTaggerCalc = 0;
   topPhi_HOTTaggerCalc = 0;
   topPhi_TTbarMassCalc = 0;
   topPt_HOTTaggerCalc = 0;
   topPt_TTbarMassCalc = 0;
   topType_HOTTaggerCalc = 0;
   topWEnergy_TTbarMassCalc = 0;
   topWEta_TTbarMassCalc = 0;
   topWPhi_TTbarMassCalc = 0;
   topWPt_TTbarMassCalc = 0;
   topbEnergy_TTbarMassCalc = 0;
   topbEta_TTbarMassCalc = 0;
   topbPhi_TTbarMassCalc = 0;
   topbPt_TTbarMassCalc = 0;
   vsSelMCTriggersEl_MultiLepCalc = 0;
   vsSelMCTriggersHad_MultiLepCalc = 0;
   vsSelMCTriggersMu_MultiLepCalc = 0;
   vsSelTriggersEl_MultiLepCalc = 0;
   vsSelTriggersHad_MultiLepCalc = 0;
   vsSelTriggersMu_MultiLepCalc = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   inputTree = tree;
   fCurrent = -1;
   inputTree->SetMakeClass(1);
   
   // event info
   inputTree->SetBranchAddress("event_CommonCalc", &event_CommonCalc, &b_event_CommonCalc);
   inputTree->SetBranchAddress("lumi_CommonCalc", &lumi_CommonCalc, &b_lumi_CommonCalc);
   inputTree->SetBranchAddress("run_CommonCalc", &run_CommonCalc, &b_run_CommonCalc);
   inputTree->SetBranchAddress("nTrueInteractions_MultiLepCalc", &nTrueInteractions_MultiLepCalc, &b_nTrueInteractions_MultiLepCalc);
   inputTree->SetBranchAddress("MCWeight_MultiLepCalc", &MCWeight_MultiLepCalc, &b_MCWeight_MultiLepCalc);
   inputTree->SetBranchAddress("evtWeightsMC_MultiLepCalc", &evtWeightsMC_MultiLepCalc, &b_evtWeightsMC_MultiLepCalc);
   inputTree->SetBranchAddress("LHEweightids_MultiLepCalc", &LHEweightids_MultiLepCalc, &b_LHEweightids_MultiLepCalc);
   inputTree->SetBranchAddress("LHEweights_MultiLepCalc", &LHEweights_MultiLepCalc, &b_LHEweights_MultiLepCalc);
   inputTree->SetBranchAddress("NewPDFweights_MultiLepCalc", &NewPDFweights_MultiLepCalc, &b_NewPDFweights_MultiLepCalc);
   inputTree->SetBranchAddress("HTfromHEPUEP_MultiLepCalc", &HTfromHEPUEP_MultiLepCalc, &b_HTfromHEPUEP_MultiLepCalc);
   inputTree->SetBranchAddress("L1NonPrefiringProbDown_CommonCalc", &L1NonPrefiringProbDown_CommonCalc, &b_L1NonPrefiringProbDown_CommonCalc);
   inputTree->SetBranchAddress("L1NonPrefiringProbUp_CommonCalc", &L1NonPrefiringProbUp_CommonCalc, &b_L1NonPrefiringProbUp_CommonCalc);
   inputTree->SetBranchAddress("L1NonPrefiringProb_CommonCalc", &L1NonPrefiringProb_CommonCalc, &b_L1NonPrefiringProb_CommonCalc);
   
   // MC triggers 
   inputTree->SetBranchAddress("vsSelMCTriggersEl_MultiLepCalc", &vsSelMCTriggersEl_MultiLepCalc, &b_vsSelMCTriggersEl_MultiLepCalc);
   inputTree->SetBranchAddress("vsSelMCTriggersHad_MultiLepCalc", &vsSelMCTriggersHad_MultiLepCalc, &b_vsSelMCTriggersHad_MultiLepCalc);
   inputTree->SetBranchAddress("vsSelMCTriggersMu_MultiLepCalc", &vsSelMCTriggersMu_MultiLepCalc, &b_vsSelMCTriggersMu_MultiLepCalc);
   inputTree->SetBranchAddress("viSelMCTriggersEl_MultiLepCalc", &viSelMCTriggersEl_MultiLepCalc, &b_viSelMCTriggersEl_MultiLepCalc);
   inputTree->SetBranchAddress("viSelMCTriggersHad_MultiLepCalc", &viSelMCTriggersHad_MultiLepCalc, &b_viSelMCTriggersHad_MultiLepCalc);
   inputTree->SetBranchAddress("viSelMCTriggersMu_MultiLepCalc", &viSelMCTriggersMu_MultiLepCalc, &b_viSelMCTriggersMu_MultiLepCalc);
   
   // Data triggers
   inputTree->SetBranchAddress("vsSelTriggersEl_MultiLepCalc", &vsSelTriggersEl_MultiLepCalc, &b_vsSelTriggersEl_MultiLepCalc);
   inputTree->SetBranchAddress("vsSelTriggersHad_MultiLepCalc", &vsSelTriggersHad_MultiLepCalc, &b_vsSelTriggersHad_MultiLepCalc);
   inputTree->SetBranchAddress("vsSelTriggersMu_MultiLepCalc", &vsSelTriggersMu_MultiLepCalc, &b_vsSelTriggersMu_MultiLepCalc);
   inputTree->SetBranchAddress("viSelTriggersEl_MultiLepCalc", &viSelTriggersEl_MultiLepCalc, &b_viSelTriggersEl_MultiLepCalc);
   inputTree->SetBranchAddress("viSelTriggersHad_MultiLepCalc", &viSelTriggersHad_MultiLepCalc, &b_viSelTriggersHad_MultiLepCalc);
   inputTree->SetBranchAddress("viSelTriggersMu_MultiLepCalc", &viSelTriggersMu_MultiLepCalc, &b_viSelTriggersMu_MultiLepCalc);
   
   // electrons
   inputTree->SetBranchAddress("elPt_MultiLepCalc", &elPt_MultiLepCalc, &b_elPt_MultiLepCalc);
   inputTree->SetBranchAddress("elEta_MultiLepCalc", &elEta_MultiLepCalc, &b_elEta_MultiLepCalc);  
   inputTree->SetBranchAddress("elPhi_MultiLepCalc", &elPhi_MultiLepCalc, &b_elPhi_MultiLepCalc);
   inputTree->SetBranchAddress("elEnergy_MultiLepCalc", &elEnergy_MultiLepCalc, &b_elEnergy_MultiLepCalc);
   inputTree->SetBranchAddress("elMiniIso_MultiLepCalc", &elMiniIso_MultiLepCalc, &b_elMiniIso_MultiLepCalc);
   inputTree->SetBranchAddress("elRelIso_MultiLepCalc", &elRelIso_MultiLepCalc, &b_elRelIso_MultiLepCalc);
   inputTree->SetBranchAddress("elMother_id_MultiLepCalc", &elMother_id_MultiLepCalc, &b_elMother_id_MultiLepCalc);
   inputTree->SetBranchAddress("elNumberOfMothers_MultiLepCalc", &elNumberOfMothers_MultiLepCalc, &b_elNumberOfMothers_MultiLepCalc);
   
   // muons
   inputTree->SetBranchAddress("muEnergy_MultiLepCalc", &muEnergy_MultiLepCalc, &b_muEnergy_MultiLepCalc);
   inputTree->SetBranchAddress("muEta_MultiLepCalc", &muEta_MultiLepCalc, &b_muEta_MultiLepCalc);
   inputTree->SetBranchAddress("muMiniIso_MultiLepCalc", &muMiniIso_MultiLepCalc, &b_muMiniIso_MultiLepCalc);
   inputTree->SetBranchAddress("muPhi_MultiLepCalc", &muPhi_MultiLepCalc, &b_muPhi_MultiLepCalc);
   inputTree->SetBranchAddress("muPt_MultiLepCalc", &muPt_MultiLepCalc, &b_muPt_MultiLepCalc);
   inputTree->SetBranchAddress("muRelIso_MultiLepCalc", &muRelIso_MultiLepCalc, &b_muRelIso_MultiLepCalc);
   inputTree->SetBranchAddress("muMother_id_MultiLepCalc", &muMother_id_MultiLepCalc, &b_muMother_id_MultiLepCalc);
   inputTree->SetBranchAddress("muNumberOfMothers_MultiLepCalc", &muNumberOfMothers_MultiLepCalc, &b_muNumberOfMothers_MultiLepCalc);
   
   // met
   inputTree->SetBranchAddress("corr_met_MultiLepCalc", &corr_met_MultiLepCalc, &b_corr_met_MultiLepCalc);
   inputTree->SetBranchAddress("corr_met_phi_MultiLepCalc", &corr_met_phi_MultiLepCalc, &b_corr_met_phi_MultiLepCalc);
   inputTree->SetBranchAddress("corr_metmod_MultiLepCalc", &corr_metmod_MultiLepCalc, &b_corr_metmod_MultiLepCalc);
   inputTree->SetBranchAddress("corr_metmod_phi_MultiLepCalc", &corr_metmod_phi_MultiLepCalc, &b_corr_metmod_phi_MultiLepCalc);
   
   // boosted truth
   inputTree->SetBranchAddress("HadronicVHtD0E_JetSubCalc", &HadronicVHtD0E_JetSubCalc, &b_HadronicVHtD0E_JetSubCalc);
   inputTree->SetBranchAddress("HadronicVHtD0Eta_JetSubCalc", &HadronicVHtD0Eta_JetSubCalc, &b_HadronicVHtD0Eta_JetSubCalc);
   inputTree->SetBranchAddress("HadronicVHtD0Phi_JetSubCalc", &HadronicVHtD0Phi_JetSubCalc, &b_HadronicVHtD0Phi_JetSubCalc);
   inputTree->SetBranchAddress("HadronicVHtD0Pt_JetSubCalc", &HadronicVHtD0Pt_JetSubCalc, &b_HadronicVHtD0Pt_JetSubCalc);
   inputTree->SetBranchAddress("HadronicVHtD1E_JetSubCalc", &HadronicVHtD1E_JetSubCalc, &b_HadronicVHtD1E_JetSubCalc);
   inputTree->SetBranchAddress("HadronicVHtD1Eta_JetSubCalc", &HadronicVHtD1Eta_JetSubCalc, &b_HadronicVHtD1Eta_JetSubCalc);
   inputTree->SetBranchAddress("HadronicVHtD1Phi_JetSubCalc", &HadronicVHtD1Phi_JetSubCalc, &b_HadronicVHtD1Phi_JetSubCalc);
   inputTree->SetBranchAddress("HadronicVHtD1Pt_JetSubCalc", &HadronicVHtD1Pt_JetSubCalc, &b_HadronicVHtD1Pt_JetSubCalc);
   inputTree->SetBranchAddress("HadronicVHtD2E_JetSubCalc", &HadronicVHtD2E_JetSubCalc, &b_HadronicVHtD2E_JetSubCalc);
   inputTree->SetBranchAddress("HadronicVHtD2Eta_JetSubCalc", &HadronicVHtD2Eta_JetSubCalc, &b_HadronicVHtD2Eta_JetSubCalc);
   inputTree->SetBranchAddress("HadronicVHtD2Phi_JetSubCalc", &HadronicVHtD2Phi_JetSubCalc, &b_HadronicVHtD2Phi_JetSubCalc);
   inputTree->SetBranchAddress("HadronicVHtD2Pt_JetSubCalc", &HadronicVHtD2Pt_JetSubCalc, &b_HadronicVHtD2Pt_JetSubCalc);
   inputTree->SetBranchAddress("HadronicVHtEnergy_JetSubCalc", &HadronicVHtEnergy_JetSubCalc, &b_HadronicVHtEnergy_JetSubCalc);
   inputTree->SetBranchAddress("HadronicVHtEta_JetSubCalc", &HadronicVHtEta_JetSubCalc, &b_HadronicVHtEta_JetSubCalc);
   inputTree->SetBranchAddress("HadronicVHtPhi_JetSubCalc", &HadronicVHtPhi_JetSubCalc, &b_HadronicVHtPhi_JetSubCalc);
   inputTree->SetBranchAddress("HadronicVHtPt_JetSubCalc", &HadronicVHtPt_JetSubCalc, &b_HadronicVHtPt_JetSubCalc);
   inputTree->SetBranchAddress("HadronicVHtID_JetSubCalc", &HadronicVHtID_JetSubCalc, &b_HadronicVHtID_JetSubCalc);
   
   // gen particles
   inputTree->SetBranchAddress("genPt_MultiLepCalc", &genPt_MultiLepCalc, &b_genPt_MultiLepCalc);
   inputTree->SetBranchAddress("genEta_MultiLepCalc", &genEta_MultiLepCalc, &b_genEta_MultiLepCalc);
   inputTree->SetBranchAddress("genPhi_MultiLepCalc", &genPhi_MultiLepCalc, &b_genPhi_MultiLepCalc);
   inputTree->SetBranchAddress("genEnergy_MultiLepCalc", &genEnergy_MultiLepCalc, &b_genEnergy_MultiLepCalc);
   inputTree->SetBranchAddress("genStatus_MultiLepCalc", &genStatus_MultiLepCalc, &b_genStatus_MultiLepCalc);
   inputTree->SetBranchAddress("genID_MultiLepCalc", &genID_MultiLepCalc, &b_genID_MultiLepCalc);
   inputTree->SetBranchAddress("genIndex_MultiLepCalc", &genIndex_MultiLepCalc, &b_genIndex_MultiLepCalc);
   inputTree->SetBranchAddress("genMotherID_MultiLepCalc", &genMotherID_MultiLepCalc, &b_genMotherID_MultiLepCalc);
   inputTree->SetBranchAddress("genMotherIndex_MultiLepCalc", &genMotherIndex_MultiLepCalc, &b_genMotherIndex_MultiLepCalc);
   inputTree->SetBranchAddress("genJetPt_MultiLepCalc", &genJetPt_MultiLepCalc, &b_genJetPt_MultiLepCalc);
   inputTree->SetBranchAddress("genJetEta_MultiLepCalc", &genJetEta_MultiLepCalc, &b_genJetEta_MultiLepCalc);
   inputTree->SetBranchAddress("genJetPhi_MultiLepCalc", &genJetPhi_MultiLepCalc, &b_genJetPhi_MultiLepCalc);
   inputTree->SetBranchAddress("genJetEnergy_MultiLepCalc", &genJetEnergy_MultiLepCalc, &b_genJetEnergy_MultiLepCalc);
   inputTree->SetBranchAddress("genJetPtNoClean_MultiLepCalc", &genJetPtNoClean_MultiLepCalc, &b_genJetPtNoClean_MultiLepCalc);
   inputTree->SetBranchAddress("genJetEtaNoClean_MultiLepCalc", &genJetEtaNoClean_MultiLepCalc, &b_genJetEtaNoClean_MultiLepCalc);
   inputTree->SetBranchAddress("genJetPhiNoClean_MultiLepCalc", &genJetPhiNoClean_MultiLepCalc, &b_genJetPhiNoClean_MultiLepCalc);
   inputTree->SetBranchAddress("genJetEnergyNoClean_MultiLepCalc", &genJetEnergyNoClean_MultiLepCalc, &b_genJetEnergyNoClean_MultiLepCalc);
   inputTree->SetBranchAddress("genTtbarIdCategory_TTbarMassCalc", &genTtbarIdCategory_TTbarMassCalc, &b_genTtbarIdCategory_TTbarMassCalc);
   inputTree->SetBranchAddress("genTtbarId_TTbarMassCalc", &genTtbarId_TTbarMassCalc, &b_genTtbarId_TTbarMassCalc);

   // JetSubCalc -- AK8 Subjet
   inputTree->SetBranchAddress("theJetAK8SDSubjetNDeepCSVMSF_JetSubCalc", &theJetAK8SDSubjetNDeepCSVMSF_JetSubCalc, &b_theJetAK8SDSubjetNDeepCSVMSF_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8SDSubjetNDeepCSVL_JetSubCalc", &theJetAK8SDSubjetNDeepCSVL_JetSubCalc, &b_theJetAK8SDSubjetNDeepCSVL_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8SDSubjetHFlav_JetSubCalc", &theJetAK8SDSubjetHFlav_JetSubCalc, &b_theJetAK8SDSubjetHFlav_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8SDSubjetIndex_JetSubCalc", &theJetAK8SDSubjetIndex_JetSubCalc, &b_theJetAK8SDSubjetIndex_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8SDSubjetSize_JetSubCalc", &theJetAK8SDSubjetSize_JetSubCalc, &b_theJetAK8SDSubjetSize_JetSubCalc);
   
   // JetSubCalc -- AK8
   inputTree->SetBranchAddress("theJetAK8Pt_JetSubCalc", &theJetAK8Pt_JetSubCalc, &b_theJetAK8Pt_JetSubCalc); 
   inputTree->SetBranchAddress("theJetAK8Eta_JetSubCalc", &theJetAK8Eta_JetSubCalc, &b_theJetAK8Eta_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8Phi_JetSubCalc", &theJetAK8Phi_JetSubCalc, &b_theJetAK8Phi_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8Mass_JetSubCalc", &theJetAK8Mass_JetSubCalc, &b_theJetAK8Mass_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8Energy_JetSubCalc", &theJetAK8Energy_JetSubCalc, &b_theJetAK8Energy_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8DoubleB_JetSubCalc", &theJetAK8DoubleB_JetSubCalc, &b_theJetAK8DoubleB_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8NjettinessTau1_JetSubCalc", &theJetAK8NjettinessTau1_JetSubCalc, &b_theJetAK8NjettinessTau1_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8NjettinessTau2_JetSubCalc", &theJetAK8NjettinessTau2_JetSubCalc, &b_theJetAK8NjettinessTau2_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8NjettinessTau3_JetSubCalc", &theJetAK8NjettinessTau3_JetSubCalc, &b_theJetAK8NjettinessTau3_JetSubCalc);
   
   // JetSubCalc -- AK8 CHS
   inputTree->SetBranchAddress("theJetAK8CHSPrunedMass_JetSubCalc", &theJetAK8CHSPrunedMass_JetSubCalc, &b_theJetAK8CHSPrunedMass_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8CHSSoftDropMass_JetSubCalc", &theJetAK8CHSSoftDropMass_JetSubCalc, &b_theJetAK8CHSSoftDropMass_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8CHSTau1_JetSubCalc", &theJetAK8CHSTau1_JetSubCalc, &b_theJetAK8CHSTau1_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8CHSTau2_JetSubCalc", &theJetAK8CHSTau2_JetSubCalc, &b_theJetAK8CHSTau2_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8CHSTau3_JetSubCalc", &theJetAK8CHSTau3_JetSubCalc, &b_theJetAK8CHSTau3_JetSubCalc);
   
   // JetSubCalc -- AK8 Softdrop
   inputTree->SetBranchAddress("theJetAK8SoftDropCorr_JetSubCalc", &theJetAK8SoftDropCorr_JetSubCalc, &b_theJetAK8SoftDropCorr_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8SoftDropRaw_JetSubCalc", &theJetAK8SoftDropRaw_JetSubCalc, &b_theJetAK8SoftDropRaw_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8SoftDrop_JMRdn_JetSubCalc", &theJetAK8SoftDrop_JMRdn_JetSubCalc, &b_theJetAK8SoftDrop_JMRdn_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8SoftDrop_JMRup_JetSubCalc", &theJetAK8SoftDrop_JMRup_JetSubCalc, &b_theJetAK8SoftDrop_JMRup_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8SoftDrop_JMSdn_JetSubCalc", &theJetAK8SoftDrop_JMSdn_JetSubCalc, &b_theJetAK8SoftDrop_JMSdn_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8SoftDrop_JMSup_JetSubCalc", &theJetAK8SoftDrop_JMSup_JetSubCalc, &b_theJetAK8SoftDrop_JMSup_JetSubCalc);
   inputTree->SetBranchAddress("theJetAK8SoftDrop_JetSubCalc", &theJetAK8SoftDrop_JetSubCalc, &b_theJetAK8SoftDrop_JetSubCalc);
   
   // JetSubCalc -- BTag
   inputTree->SetBranchAddress("theJetBTag_JetSubCalc", &theJetBTag_JetSubCalc, &b_theJetBTag_JetSubCalc);
   inputTree->SetBranchAddress("theJetBTag_bSFdn_JetSubCalc", &theJetBTag_bSFdn_JetSubCalc, &b_theJetBTag_bSFdn_JetSubCalc);
   inputTree->SetBranchAddress("theJetBTag_bSFup_JetSubCalc", &theJetBTag_bSFup_JetSubCalc, &b_theJetBTag_bSFup_JetSubCalc);
   inputTree->SetBranchAddress("theJetBTag_lSFdn_JetSubCalc", &theJetBTag_lSFdn_JetSubCalc, &b_theJetBTag_lSFdn_JetSubCalc);
   inputTree->SetBranchAddress("theJetBTag_lSFup_JetSubCalc", &theJetBTag_lSFup_JetSubCalc, &b_theJetBTag_lSFup_JetSubCalc);
   
   // JetSubCalc -- theJet
   inputTree->SetBranchAddress("theJetHFlav_JetSubCalc", &theJetHFlav_JetSubCalc, &b_theJetHFlav_JetSubCalc);
   inputTree->SetBranchAddress("theJetPFlav_JetSubCalc", &theJetPFlav_JetSubCalc, &b_theJetPFlav_JetSubCalc);
   inputTree->SetBranchAddress("theJetEnergy_JetSubCalc", &theJetEnergy_JetSubCalc, &b_theJetEnergy_JetSubCalc);
   inputTree->SetBranchAddress("theJetEta_JetSubCalc", &theJetEta_JetSubCalc, &b_theJetEta_JetSubCalc);
   inputTree->SetBranchAddress("theJetPhi_JetSubCalc", &theJetPhi_JetSubCalc, &b_theJetPhi_JetSubCalc);
   inputTree->SetBranchAddress("theJetPt_JetSubCalc", &theJetPt_JetSubCalc, &b_theJetPt_JetSubCalc);
   inputTree->SetBranchAddress("theJetDeepFlavB_JetSubCalc", &theJetDeepFlavB_JetSubCalc, &b_theJetDeepFlavB_JetSubCalc);
   inputTree->SetBranchAddress("maxProb_JetSubCalc", &maxProb_JetSubCalc, &b_maxProb_JetSubCalc);
   
   // AK4Jet -- DeepCSV
   inputTree->SetBranchAddress("AK4JetDeepCSVb_MultiLepCalc", &AK4JetDeepCSVb_MultiLepCalc, &b_AK4JetDeepCSVb_MultiLepCalc);
   inputTree->SetBranchAddress("AK4JetDeepCSVbb_MultiLepCalc", &AK4JetDeepCSVbb_MultiLepCalc, &b_AK4JetDeepCSVbb_MultiLepCalc);
   inputTree->SetBranchAddress("AK4JetDeepCSVc_MultiLepCalc", &AK4JetDeepCSVc_MultiLepCalc, &b_AK4JetDeepCSVc_MultiLepCalc);
   inputTree->SetBranchAddress("AK4JetDeepCSVudsg_MultiLepCalc", &AK4JetDeepCSVudsg_MultiLepCalc, &b_AK4JetDeepCSVudsg_MultiLepCalc);
   
   // AK4Jet -- DeepFlav
   inputTree->SetBranchAddress("AK4JetDeepFlavb_MultiLepCalc", &AK4JetDeepFlavb_MultiLepCalc, &b_AK4JetDeepFlavb_MultiLepCalc);
   inputTree->SetBranchAddress("AK4JetDeepFlavbb_MultiLepCalc", &AK4JetDeepFlavbb_MultiLepCalc, &b_AK4JetDeepFlavbb_MultiLepCalc);
   inputTree->SetBranchAddress("AK4JetDeepFlavc_MultiLepCalc", &AK4JetDeepFlavc_MultiLepCalc, &b_AK4JetDeepFlavc_MultiLepCalc);
   inputTree->SetBranchAddress("AK4JetDeepFlavg_MultiLepCalc", &AK4JetDeepFlavg_MultiLepCalc, &b_AK4JetDeepFlavg_MultiLepCalc);
   inputTree->SetBranchAddress("AK4JetDeepFlavlepb_MultiLepCalc", &AK4JetDeepFlavlepb_MultiLepCalc, &b_AK4JetDeepFlavlepb_MultiLepCalc);
   inputTree->SetBranchAddress("AK4JetDeepFlavuds_MultiLepCalc", &AK4JetDeepFlavuds_MultiLepCalc, &b_AK4JetDeepFlavuds_MultiLepCalc);
   
   // AK4Jet -- BTag
   inputTree->SetBranchAddress("AK4JetBTag_MultiLepCalc", &AK4JetBTag_MultiLepCalc, &b_AK4JetBTag_MultiLepCalc);
   inputTree->SetBranchAddress("AK4JetBTag_bSFdn_MultiLepCalc", &AK4JetBTag_bSFdn_MultiLepCalc, &b_AK4JetBTag_bSFdn_MultiLepCalc);
   inputTree->SetBranchAddress("AK4JetBTag_bSFup_MultiLepCalc", &AK4JetBTag_bSFup_MultiLepCalc, &b_AK4JetBTag_bSFup_MultiLepCalc);
   inputTree->SetBranchAddress("AK4JetBTag_lSFdn_MultiLepCalc", &AK4JetBTag_lSFdn_MultiLepCalc, &b_AK4JetBTag_lSFdn_MultiLepCalc);
   inputTree->SetBranchAddress("AK4JetBTag_lSFup_MultiLepCalc", &AK4JetBTag_lSFup_MultiLepCalc, &b_AK4JetBTag_lSFup_MultiLepCalc);
   
   // TTbarMassCalc -- top
   inputTree->SetBranchAddress("ttbarMass_TTbarMassCalc", &ttbarMass_TTbarMassCalc, &b_ttbarMass_TTbarMassCalc);
   inputTree->SetBranchAddress("topEnergy_TTbarMassCalc", &topEnergy_TTbarMassCalc, &b_topEnergy_TTbarMassCalc);
   inputTree->SetBranchAddress("topEta_TTbarMassCalc", &topEta_TTbarMassCalc, &b_topEta_TTbarMassCalc);
   inputTree->SetBranchAddress("topMass_TTbarMassCalc", &topMass_TTbarMassCalc, &b_topMass_TTbarMassCalc);
   inputTree->SetBranchAddress("topPhi_TTbarMassCalc", &topPhi_TTbarMassCalc, &b_topPhi_TTbarMassCalc);
   inputTree->SetBranchAddress("topPt_TTbarMassCalc", &topPt_TTbarMassCalc, &b_topPt_TTbarMassCalc);
   inputTree->SetBranchAddress("topID_TTbarMassCalc", &topID_TTbarMassCalc, &b_topID_TTbarMassCalc);
   
   inputTree->SetBranchAddress("allTopsID_TTbarMassCalc", &allTopsID_TTbarMassCalc, &b_allTopsID_TTbarMassCalc);
   inputTree->SetBranchAddress("allTopsStatus_TTbarMassCalc", &allTopsStatus_TTbarMassCalc, &b_allTopsStatus_TTbarMassCalc);
   inputTree->SetBranchAddress("allTopsEnergy_TTbarMassCalc", &allTopsEnergy_TTbarMassCalc, &b_allTopsEnergy_TTbarMassCalc);
   inputTree->SetBranchAddress("allTopsEta_TTbarMassCalc", &allTopsEta_TTbarMassCalc, &b_allTopsEta_TTbarMassCalc);
   inputTree->SetBranchAddress("allTopsPhi_TTbarMassCalc", &allTopsPhi_TTbarMassCalc, &b_allTopsPhi_TTbarMassCalc);
   inputTree->SetBranchAddress("allTopsPt_TTbarMassCalc", &allTopsPt_TTbarMassCalc, &b_allTopsPt_TTbarMassCalc);
   
   // TTbarMassCalc -- W
   inputTree->SetBranchAddress("topWEnergy_TTbarMassCalc", &topWEnergy_TTbarMassCalc, &b_topWEnergy_TTbarMassCalc);
   inputTree->SetBranchAddress("topWEta_TTbarMassCalc", &topWEta_TTbarMassCalc, &b_topWEta_TTbarMassCalc);
   inputTree->SetBranchAddress("topWPhi_TTbarMassCalc", &topWPhi_TTbarMassCalc, &b_topWPhi_TTbarMassCalc);
   inputTree->SetBranchAddress("topWPt_TTbarMassCalc", &topWPt_TTbarMassCalc, &b_topWPt_TTbarMassCalc);
   inputTree->SetBranchAddress("topWID_TTbarMassCalc", &topWID_TTbarMassCalc, &b_topWID_TTbarMassCalc);
   
   // TTbarMassCalc -- b
   inputTree->SetBranchAddress("topbEnergy_TTbarMassCalc", &topbEnergy_TTbarMassCalc, &b_topbEnergy_TTbarMassCalc);
   inputTree->SetBranchAddress("topbEta_TTbarMassCalc", &topbEta_TTbarMassCalc, &b_topbEta_TTbarMassCalc);
   inputTree->SetBranchAddress("topbPhi_TTbarMassCalc", &topbPhi_TTbarMassCalc, &b_topbPhi_TTbarMassCalc);
   inputTree->SetBranchAddress("topbPt_TTbarMassCalc", &topbPt_TTbarMassCalc, &b_topbPt_TTbarMassCalc);
   inputTree->SetBranchAddress("topbID_TTbarMassCalc", &topbID_TTbarMassCalc, &b_topbID_TTbarMassCalc);
   
   // HOTTaggerCalc
   inputTree->SetBranchAddress("topJet1Index_HOTTaggerCalc", &topJet1Index_HOTTaggerCalc, &b_topJet1Index_HOTTaggerCalc);
   inputTree->SetBranchAddress("topJet2Index_HOTTaggerCalc", &topJet2Index_HOTTaggerCalc, &b_topJet2Index_HOTTaggerCalc);
   inputTree->SetBranchAddress("topJet3Index_HOTTaggerCalc", &topJet3Index_HOTTaggerCalc, &b_topJet3Index_HOTTaggerCalc);
   inputTree->SetBranchAddress("topNAK4_HOTTaggerCalc", &topNAK4_HOTTaggerCalc, &b_topNAK4_HOTTaggerCalc);
   inputTree->SetBranchAddress("topNtops_HOTTaggerCalc", &topNtops_HOTTaggerCalc, &b_topNtops_HOTTaggerCalc);
   inputTree->SetBranchAddress("topBestGenEnergy_HOTTaggerCalc", &topBestGenEnergy_HOTTaggerCalc, &b_topBestGenEnergy_HOTTaggerCalc);
   inputTree->SetBranchAddress("topBestGenEta_HOTTaggerCalc", &topBestGenEta_HOTTaggerCalc, &b_topBestGenEta_HOTTaggerCalc);
   inputTree->SetBranchAddress("topBestGenPhi_HOTTaggerCalc", &topBestGenPhi_HOTTaggerCalc, &b_topBestGenPhi_HOTTaggerCalc);
   inputTree->SetBranchAddress("topBestGenPt_HOTTaggerCalc", &topBestGenPt_HOTTaggerCalc, &b_topBestGenPt_HOTTaggerCalc); 
   inputTree->SetBranchAddress("topDRmax_HOTTaggerCalc", &topDRmax_HOTTaggerCalc, &b_topDRmax_HOTTaggerCalc);
   inputTree->SetBranchAddress("topDThetaMax_HOTTaggerCalc", &topDThetaMax_HOTTaggerCalc, &b_topDThetaMax_HOTTaggerCalc);
   inputTree->SetBranchAddress("topDThetaMin_HOTTaggerCalc", &topDThetaMin_HOTTaggerCalc, &b_topDThetaMin_HOTTaggerCalc);
   inputTree->SetBranchAddress("topDiscriminator_HOTTaggerCalc", &topDiscriminator_HOTTaggerCalc, &b_topDiscriminator_HOTTaggerCalc);
   inputTree->SetBranchAddress("topEta_HOTTaggerCalc", &topEta_HOTTaggerCalc, &b_topEta_HOTTaggerCalc);
   inputTree->SetBranchAddress("topMass_HOTTaggerCalc", &topMass_HOTTaggerCalc, &b_topMass_HOTTaggerCalc);
   inputTree->SetBranchAddress("topNconstituents_HOTTaggerCalc", &topNconstituents_HOTTaggerCalc, &b_topNconstituents_HOTTaggerCalc);
   inputTree->SetBranchAddress("topPhi_HOTTaggerCalc", &topPhi_HOTTaggerCalc, &b_topPhi_HOTTaggerCalc);
   inputTree->SetBranchAddress("topPt_HOTTaggerCalc", &topPt_HOTTaggerCalc, &b_topPt_HOTTaggerCalc);
   inputTree->SetBranchAddress("topType_HOTTaggerCalc", &topType_HOTTaggerCalc, &b_topType_HOTTaggerCalc);
   Notify();
}

Bool_t step1::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void step1::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!inputTree) return;
   inputTree->Show(entry);
}
Int_t step1::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}

#endif // #ifdef step1_cxx
