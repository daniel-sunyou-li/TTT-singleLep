#define S2HardcodedConditions_cxx

#include <cmath>
#include "S2HardcodedConditions.h"
#include <unordered_map>


using namespace std;

S2HardcodedConditions::S2HardcodedConditions() {

   if(!(tfile_HTNJ_SF=TFile::Open("HT_njets_SF_4tops_dcsv_djet.root"))){
    std::cout<<"WARNING! SF file doesn't exist! Exiting" << std::endl;
    exit(1);
   }

  hscale_tttt_dcsv    = (TH2F*)tfile_HTNJ_SF->Get("hscale_tttt_dcsv")->Clone();
  hscale_ttjj_dcsv    = (TH2F*)tfile_HTNJ_SF->Get("hscale_ttjj_dcsv")->Clone();
  hscale_ttbb_dcsv    = (TH2F*)tfile_HTNJ_SF->Get("hscale_ttbb_dcsv")->Clone();  
  hscale_ttcc_dcsv    = (TH2F*)tfile_HTNJ_SF->Get("hscale_ttcc_dcsv")->Clone();
  hscale_tt2b_dcsv    = (TH2F*)tfile_HTNJ_SF->Get("hscale_tt2b_dcsv")->Clone();
  hscale_tt1b_dcsv    = (TH2F*)tfile_HTNJ_SF->Get("hscale_tt1b_dcsv")->Clone();
  hscale_HT500Njet9_ttjj_dcsv    = (TH2F*)tfile_HTNJ_SF->Get("hscale_HT500Njet9_ttjj_dcsv")->Clone();
  hscale_HT500Njet9_ttbb_dcsv    = (TH2F*)tfile_HTNJ_SF->Get("hscale_HT500Njet9_ttbb_dcsv")->Clone();
  hscale_HT500Njet9_ttcc_dcsv    = (TH2F*)tfile_HTNJ_SF->Get("hscale_HT500Njet9_ttcc_dcsv")->Clone();
  hscale_HT500Njet9_tt2b_dcsv    = (TH2F*)tfile_HTNJ_SF->Get("hscale_HT500Njet9_tt2b_dcsv")->Clone();
  hscale_HT500Njet9_tt1b_dcsv    = (TH2F*)tfile_HTNJ_SF->Get("hscale_HT500Njet9_tt1b_dcsv")->Clone();
  hscale_STs_dcsv     = (TH2F*)tfile_HTNJ_SF->Get("hscale_STs_dcsv")->Clone();
  hscale_STtw_dcsv    = (TH2F*)tfile_HTNJ_SF->Get("hscale_STtw_dcsv")->Clone();
  hscale_STt_dcsv     = (TH2F*)tfile_HTNJ_SF->Get("hscale_STt_dcsv")->Clone();
  hscale_WJets_dcsv   = (TH2F*)tfile_HTNJ_SF->Get("hscale_WJets_dcsv")->Clone();

  hscale_tttt_djet    = (TH2F*)tfile_HTNJ_SF->Get("hscale_tttt_djet")->Clone();
  hscale_ttjj_djet    = (TH2F*)tfile_HTNJ_SF->Get("hscale_ttjj_djet")->Clone();
  hscale_ttbb_djet    = (TH2F*)tfile_HTNJ_SF->Get("hscale_ttbb_djet")->Clone();
  hscale_ttcc_djet    = (TH2F*)tfile_HTNJ_SF->Get("hscale_ttcc_djet")->Clone();
  hscale_tt2b_djet    = (TH2F*)tfile_HTNJ_SF->Get("hscale_tt2b_djet")->Clone();
  hscale_tt1b_djet    = (TH2F*)tfile_HTNJ_SF->Get("hscale_tt1b_djet")->Clone();
  hscale_HT500Njet9_ttjj_djet    = (TH2F*)tfile_HTNJ_SF->Get("hscale_HT500Njet9_ttjj_djet")->Clone();
  hscale_HT500Njet9_ttbb_djet    = (TH2F*)tfile_HTNJ_SF->Get("hscale_HT500Njet9_ttbb_djet")->Clone();
  hscale_HT500Njet9_ttcc_djet    = (TH2F*)tfile_HTNJ_SF->Get("hscale_HT500Njet9_ttcc_djet")->Clone();
  hscale_HT500Njet9_tt2b_djet    = (TH2F*)tfile_HTNJ_SF->Get("hscale_HT500Njet9_tt2b_djet")->Clone();
  hscale_HT500Njet9_tt1b_djet    = (TH2F*)tfile_HTNJ_SF->Get("hscale_HT500Njet9_tt1b_djet")->Clone();
  hscale_STs_djet     = (TH2F*)tfile_HTNJ_SF->Get("hscale_STs_djet")->Clone();
  hscale_STtw_djet    = (TH2F*)tfile_HTNJ_SF->Get("hscale_STtw_djet")->Clone();
  hscale_STt_djet     = (TH2F*)tfile_HTNJ_SF->Get("hscale_STt_djet")->Clone();
  hscale_WJets_djet   = (TH2F*)tfile_HTNJ_SF->Get("hscale_WJets_djet")->Clone();

}

S2HardcodedConditions::~S2HardcodedConditions() {
}

float S2HardcodedConditions::GetCSVRenorm2DSF_HTnj(float HT, int njets, std::string sampleType){

  int tmp_njets = njets;
  if(tmp_njets>6) tmp_njets=6;

  if (sampleType == "tttt"){
      return hscale_tttt_dcsv->GetBinContent(hscale_tttt_dcsv->FindBin(tmp_njets, HT));
  }

  if (sampleType == "ttjj"){
      return hscale_ttjj_dcsv->GetBinContent(hscale_ttjj_dcsv->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "ttcc"){
      return hscale_ttcc_dcsv->GetBinContent(hscale_ttcc_dcsv->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "ttbb"){
      return hscale_ttbb_dcsv->GetBinContent(hscale_ttbb_dcsv->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "tt2b"){
      return hscale_tt2b_dcsv->GetBinContent(hscale_tt2b_dcsv->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "tt1b"){
      return hscale_tt1b_dcsv->GetBinContent(hscale_tt1b_dcsv->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "HT500Njet9_ttjj"){
      return hscale_HT500Njet9_ttjj_dcsv->GetBinContent(hscale_HT500Njet9_ttjj_dcsv->FindBin(tmp_njets, HT));
  }

  if (sampleType == "HT500Njet9_ttcc"){
      return hscale_HT500Njet9_ttcc_dcsv->GetBinContent(hscale_HT500Njet9_ttcc_dcsv->FindBin(tmp_njets, HT));
  }

  if (sampleType == "HT500Njet9_ttbb"){
      return hscale_HT500Njet9_ttbb_dcsv->GetBinContent(hscale_HT500Njet9_ttbb_dcsv->FindBin(tmp_njets, HT));
  }

  if (sampleType == "HT500Njet9_tt2b"){
      return hscale_HT500Njet9_tt2b_dcsv->GetBinContent(hscale_HT500Njet9_tt2b_dcsv->FindBin(tmp_njets, HT));
  }

  if (sampleType == "HT500Njet9_tt1b"){
      return hscale_HT500Njet9_tt1b_dcsv->GetBinContent(hscale_HT500Njet9_tt1b_dcsv->FindBin(tmp_njets, HT));
  }

  if (sampleType == "STs"){
      return hscale_STs_dcsv->GetBinContent(hscale_STs_dcsv->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "STt"){
      return hscale_STt_dcsv->GetBinContent(hscale_STt_dcsv->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "STtw"){
      return hscale_STtw_dcsv->GetBinContent(hscale_STtw_dcsv->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "WJets"){
      return hscale_WJets_dcsv->GetBinContent(hscale_WJets_dcsv->FindBin(tmp_njets, HT));  
  }

  return 1.0;
}


float S2HardcodedConditions::GetDeepJetRenorm2DSF_HTnj(float HT, int njets, std::string sampleType){

  int tmp_njets = njets;
  if(tmp_njets>6) tmp_njets=6;

  if (sampleType == "tttt"){
      return hscale_tttt_djet->GetBinContent(hscale_tttt_djet->FindBin(tmp_njets, HT));
  }

  if (sampleType == "ttjj"){
      return hscale_ttjj_djet->GetBinContent(hscale_ttjj_djet->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "ttcc"){
      return hscale_ttcc_djet->GetBinContent(hscale_ttcc_djet->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "ttbb"){
      return hscale_ttbb_djet->GetBinContent(hscale_ttbb_djet->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "tt2b"){
      return hscale_tt2b_djet->GetBinContent(hscale_tt2b_djet->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "tt1b"){
      return hscale_tt1b_djet->GetBinContent(hscale_tt1b_djet->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "HT500Njet9_ttjj"){
      return hscale_HT500Njet9_ttjj_djet->GetBinContent(hscale_HT500Njet9_ttjj_djet->FindBin(tmp_njets, HT));
  }

  if (sampleType == "HT500Njet9_ttcc"){
      return hscale_HT500Njet9_ttcc_djet->GetBinContent(hscale_HT500Njet9_ttcc_djet->FindBin(tmp_njets, HT));
  }

  if (sampleType == "HT500Njet9_ttbb"){
      return hscale_HT500Njet9_ttbb_djet->GetBinContent(hscale_HT500Njet9_ttbb_djet->FindBin(tmp_njets, HT));
  }

  if (sampleType == "HT500Njet9_tt2b"){
      return hscale_HT500Njet9_tt2b_djet->GetBinContent(hscale_HT500Njet9_tt2b_djet->FindBin(tmp_njets, HT));
  }

  if (sampleType == "HT500Njet9_tt1b"){
      return hscale_HT500Njet9_tt1b_djet->GetBinContent(hscale_HT500Njet9_tt1b_djet->FindBin(tmp_njets, HT));
  }

  if (sampleType == "STs"){
      return hscale_STs_djet->GetBinContent(hscale_STs_djet->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "STt"){
      return hscale_STt_djet->GetBinContent(hscale_STt_djet->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "STtw"){
      return hscale_STtw_djet->GetBinContent(hscale_STtw_djet->FindBin(tmp_njets, HT));  
  }

  if (sampleType == "WJets"){
      return hscale_WJets_djet->GetBinContent(hscale_WJets_djet->FindBin(tmp_njets, HT));  
  }

  return 1.0;
}
