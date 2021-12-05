#define HardcodedConditions_cxx
      print("eos root://cmseos.fnal.gov mkdir -p {}".format( os.path.join( outputDir[ shift ], step1_sample ) )  )

#include <cmath>
#include "HardcodedConditions.h"
#include <unordered_map>


using namespace std;

HardcodedConditions::HardcodedConditions() {}

HardcodedConditions::HardcodedConditions(Int_t year) {

   TString sfFileName( "HT_njets_SF_3t_UL17.root" );
   
   if( year == 2018 ){
     sfFileName = "HT_njets_SF_3t_UL18.root";
   }
   else if( year == 2016 ){
     sfFileName = "HT_njets_SF_3t_UL16.root";
   }

   if(!(tfile_HTNJ_SF=TFile::Open("HT_njets_SF_3t.root"))){
    std::cout<<"WARNING! SF file doesn't exist! Exiting" << std::endl;
    exit(1);
   }

   cout << ">> Reading scale factor file: " << sfFileName << endl;
   if( !(tfile_HTNJ_SF = TFile::Open( sfFileName ) ) ){
     std::cout << "[WARN] SF file does not exist. Exiting..." << std::endl;
     exit(1);
   }

  std::string SYSs[19] = { {"", "_HFup", "_HFdn", "_LFup", "_LFdn", "_jesup", "_jesdn", "_hfstats1up", "_hfstats1dn", "_hfstats2up", "_hfstats2dn", "_cferr1up", "_cferr1dn", "_cferr2up", "_cferr2dn", "_lfstats1up", "_lfstats1dn", "_lfstats2up", "_lfstats2dn"};  

  for( size_t isys = 0; isys<19; isys++){
    hscale_tttt[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_tttt"+SYSs[isys]).c_str())->Clone();
    hscale_ttjj[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_ttjj"+SYSs[isys]).c_str())->Clone();
    hscale_ttbb[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_ttbb"+SYSs[isys]).c_str())->Clone();
    hscale_ttcc[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_ttcc"+SYSs[isys]).c_str())->Clone();
    hscale_tt2b[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_tt2b"+SYSs[isys]).c_str())->Clone();
    hscale_tt1b[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_tt1b"+SYSs[isys]).c_str())->Clone();
    hscale_HT500Njet9_ttjj[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_HT500Njet9_ttjj"+SYSs[isys]).c_str())->Clone();
    hscale_HT500Njet9_ttbb[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_HT500Njet9_ttbb"+SYSs[isys]).c_str())->Clone();
    hscale_HT500Njet9_ttcc[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_HT500Njet9_ttcc"+SYSs[isys]).c_str())->Clone();
    hscale_HT500Njet9_tt2b[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_HT500Njet9_tt2b"+SYSs[isys]).c_str())->Clone();
    hscale_HT500Njet9_tt1b[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_HT500Njet9_tt1b"+SYSs[isys]).c_str())->Clone();
    hscale_STs[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_STs"+SYSs[isys]).c_str())->Clone();
    hscale_STtw[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_STtw"+SYSs[isys]).c_str())->Clone();
    hscale_STt[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_STt"+SYSs[isys]).c_str())->Clone();
    hscale_WJets[SYSs[isys]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_WJets"+SYSs[isys]).c_str())->Clone();
  }
}


HardcodedConditions::~HardcodedConditions() {}

float HardcodedConditions::GetCSVRenormSF(int year, int isE, int njet, std::string sampleType){
  if( sampleType == "" ) return 1.0;

  std::unordered_map<string, std::vector<float>> wgt2017_E = { // { type, { nj4, nj5, nj6p}}
      {"tttt", {0.9226035838, 0.9340754278, 0.9178683544}},
      {"ttjj", {0.9952321401, 0.9678148547, 0.916412004}},//{1.0150106608, 1.0158690852, 0.9984062267}}, 
      {"ttcc", {0.9952321401, 0.9678148547, 0.916412004}}, 
      {"ttbb", {0.9586652314, 0.9435930048, 0.8944224401}}, 
      {"tt1b", {0.9952321401, 0.9678148547, 0.916412004}},
      {"tt2b", {0.9952321401, 0.9678148547, 0.916412004}}, 
      {"T",    {0.9933786006, 0.9646801108, 0.9143510121}},    
      {"TTV",  {0.9933786006, 0.9646801108, 0.9143510121}},   
      {"TTXY", {0.9649570916, 0.9760667136, 0.9668860438}},
      {"WJets", {0.8826404583, 0.8583431706, 0.8123368769}},
      {"ZJets", {0.8826404583, 0.8583431706, 0.8123368769}},   
      {"VV",   {0.8826404583, 0.8583431706, 0.8123368769}}, 
      {"qcd",  {0.9844800159, 0.8744057182, 0.7953136397}}  
  }; 
           
  std::unordered_map<string, std::vector<float>> wgt2017_M = {
      {"tttt", {0.9433598986, 0.9272944126, 0.9110504508}},
      {"ttjj", {0.9962244676, 0.9667166631, 0.9186391487}},
      {"ttcc", {0.9962244676, 0.9667166631, 0.9186391487}},    
      {"ttbb", {0.9595725455, 0.9438734429, 0.9030468218}},   
      {"tt1b", {0.9962244676, 0.9667166631, 0.9186391487}},   
      {"tt2b", {0.9962244676, 0.9667166631, 0.9186391487}},
      {"T",    {0.9942103098, 0.9613614481, 0.9144844627}},   
      {"TTV",  {0.9942103098, 0.9613614481, 0.9144844627}}, 
      {"TTXY", {0.9755792626, 0.9659806557, 0.9643891245}},
      {"WJets", {0.9044615563, 0.9076278828, 0.7916357948}},
      {"ZJets", {0.9044615563, 0.9076278828, 0.7916357948}},
      {"VV",   {0.9044615563, 0.9076278828, 0.7916357948}}, 
      {"qcd",  {0.940833989, 0.9788744589, 0.9195875563}} 
  };                       

  std::unordered_map<string, std::vector<float>> wgt2018_E = { // { type, { nj4, nj5, nj6p}}
      {"tttt", {0.9279750194, 0.9479727174, 0.9191942033}},
      {"ttjj", {0.9923480750, 1.0057580471, 1.0011944434}},
      {"ttcc", {1.0050957838, 1.0047475902, 0.9982370828}},    
      {"ttbb", {0.9666382033, 0.9559780476, 0.9556587079}},   
      {"tt1b", {0.9692647427, 0.9778219595, 0.9722511777}},   
      {"tt2b", {0.9956445718, 0.9975362672, 0.9905346602}},
      {"T",    {0.9779770577, 0.9856033892, 0.9726416567}},   
      {"TTV",  {0.9597092704, 0.9660527988, 0.9585140872}}, 
      {"TTXY", {0.9502030288, 0.9594360242, 0.9608876848}},
      {"WJets", {0.8720559924, 0.8777058190, 0.8538766506}},
      {"ZJets", {0.8274565677, 0.8184282280, 0.7902021407}},
      {"VV",   {0.9808907637, 0.8806614835, 0.9322116757}}, 
      {"qcd",  {0.9317167909, 0.9550869373, 0.7593072727}} 
  };  

  std::unordered_map<string, std::vector<float>> wgt2018_M = {
      {"tttt", {0.9598061229, 0.9385816479, 0.9242174919}},
      {"ttjj", {0.9943568547, 1.0037506677, 0.9982871601}},
      {"ttcc", {0.9967671200, 0.9995292499, 0.9998498201}},
      {"ttbb", {0.9569457644, 0.9636918215, 0.9661412214}},
      {"tt1b", {0.9715690171, 0.9751878298, 0.9663625408}},
      {"tt2b", {0.9873304461, 0.9937619408, 0.9917692476}},
      {"T",    {0.9813194258, 0.9931216192, 0.9812484650}},
      {"TTV",  {0.9556623113, 0.9660025586, 0.9641271023}},
      {"TTXY", {0.9472739920, 0.9562394387, 0.9650080939}},
      {"WJets", {0.8705578922, 0.8711052889, 0.8521469129}},
      {"ZJets", {0.8628752440, 0.8546751993, 0.8152587307}},
      {"VV",   {0.8593916158, 0.8730070208, 0.9085752620}},
      {"qcd",  {0.8931172211, 1.0248316102, 0.9197058065}}
  };

  if (wgt2017_E.find(sampleType) ==  wgt2017_E.end()) {
    cout << " GetCSVRenormSF() ---- CHECK sample process type! \n";
    return 1.0;
  }

  if (year == 2017) {

      if (isE == 1) {
        if (njet == 4) {
          return wgt2017_E.at(sampleType)[0];
        }
        if (njet == 5) {
          return wgt2017_E.at(sampleType)[1];
        }
        if (njet >= 6) {
          return wgt2017_E.at(sampleType)[2];
        }
      }

      else {
        if (njet == 4) {
          return wgt2017_M.at(sampleType)[0];
        }
        if (njet == 5) {
          return wgt2017_M.at(sampleType)[1];
        }
        if (njet >= 6) {
          return wgt2017_M.at(sampleType)[2];
        }
      }

  }
 
  else if (year == 2018) {

      if (isE == 1) {
        if (njet == 4) {
          return wgt2018_E.at(sampleType)[0];
        }
        if (njet == 5) {
          return wgt2018_E.at(sampleType)[1];
        }
        if (njet >= 6) {
          return wgt2018_E.at(sampleType)[2];
        }
      }

      else {
        if (njet == 4) {
          return wgt2018_M.at(sampleType)[0];
        }
        if (njet == 5) {
          return wgt2018_M.at(sampleType)[1];
        }
        if (njet >= 6) {
          return wgt2018_M.at(sampleType)[2];
        }
      }

  }

  return 1.0;

}

float HardcodedConditions::GetDeepJetRenorm2DSF_HTnj( float HT, int njets, std::string sampleType, std::string sysType ){

  if( hscale_ttjj.find( sysType ) == hscale_ttjj.end() ) return 1.0;
  if( sampleType == "" ) return 1.0;
  int njets_idx = njets;
  if( njets_idx > 6 ) njets_idx = 6;
  
  if( sampleType == "tttt" ){
    return hscale_tttt[ sysType ]->GetBinContent( hscale_tttt[ sysType ]->FindBin( njets_idx, HT ) );
  }

  if( sampleType == "ttjj" ){
    return hscale_ttjj[ sysType ]->GetBinContent( hscale_ttjj[ sysType ]->FindBin( njets_idx, HT ) );
  }  

  if( sampleType == "ttcc" ){
    return hscale_ttcc[ sysType ]->GetBinContent( hscale_ttcc[ sysType ]->FindBin( njets_idx, HT ) );
  }
  
  if( sampleType == "ttbb" ){
    return hscale_ttbb[ sysType ]->GetBinContent( hscale_ttbb[ sysType ]->FindBin( njets_idx, HT ) );
  }  

  if( sampleType == "tt2b" ){
    return hscale_tt2b[ sysType ]->GetBinContent( hscale_tt2b[ sysType ]->FindBin( njets_idx, HT ) );
  }  

  if( sampleType == "STs" ){
    return hscale_STs[ sysType ]->GetBinContent( hscale_STs[ sysType ]->FindBin( njets_idx, HT ) );
  } 
 
  if( sampleType == "STt" ){
    return hscale_STt[ sysType ]->GetBinContent( hscale_STt[ sysType ]->FindBin( njets_idx, HT ) );
  }
  
  if( sampleType == "STtW" ){
    return hscale_STtW[ sysType ]->GetBinContent( hscale_STtW[ sysType ]->FindBin( njets_idx, HT ) );
  }
  
  if( sampleType == "WJets" ){
    return hscale_WJets[ sysType ]->GetBinContent( hscale_WJets[ sysType ]->FindBin( njets_idx, HT ) );
  }

  return 1.0;  
} 













