#define HardcodedConditions_cxx
#include <cmath>
#include "HardcodedConditions.h"
#include <unordered_map>


using namespace std;

HardcodedConditions::HardcodedConditions() {}

HardcodedConditions::HardcodedConditions( Int_t year ) {

  TString sfFileName( "HT_njets_SF_3t_UL17_sys.root" );
  if( year == 2018 ){
    sfFileName = "HT_njets_SF_3t_UL18_sys.root"; 
  }
  else if( year == 2016 ){
    sfFileName = "renorm/HT_njets_SF_3t_UL16_sys.root"; 
  }

  cout << ">> Reading scale factor file: " << sfFileName << endl;
  if( !( tfile_HTNJ_SF = TFile::Open( sfFileName ) ) ){
    std::cout << "[WARN] File does not exist. Exiting..." << std::endl;
    exit(1);  
  }

  std::string SYSs[19] = { "", "_HFup", "_HFdn", "_LFup", "_LFdn", "_jesup", "_jesdn", "_hfstats1up", "_hfstats1dn", "_hfstats2up", "_hfstats2dn", "_cferr1up", "_cferr1dn", "_cferr2up", "_cferr2dn", "_lfstats1up", "_lfstats1dn", "_lfstats2up", "_lfstats2dn" };  
  for( size_t i = 0; i < 19; i++ ){
    hscale_tttw[SYSs[i]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_TTTW"+SYSs[i]).c_str())->Clone();
    hscale_tttj[SYSs[i]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_TTTJ"+SYSs[i]).c_str())->Clone();   // hscale_tttt[SYSs[i]]   =(TH2F*)tfile_HTNJ_SF->Get(("hscale_tttt"+SYSs[i]).c_str())->Clone();
    // hscale_tttt[SYSs[i]]   =(TH2F*)tfile_HTNJ_SF->Get(("hscale_tttt"+SYSs[i]).c_str())->Clone();
    // hscale_ttjj[SYSs[i]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_ttjj"+SYSs[i]).c_str())->Clone();
    // hscale_ttbb[SYSs[i]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_ttbb"+SYSs[i]).c_str())->Clone();
    // hscale_ttcc[SYSs[i]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_ttcc"+SYSs[i]).c_str())->Clone();
    // hscale_tt2b[SYSs[i]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_tt2b"+SYSs[i]).c_str())->Clone();
    // hscale_tt1b[SYSs[i]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_tt1b"+SYSs[i]).c_str())->Clone();
    // hscale_HT500Njet9_ttjj[SYSs[i]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_HT500Njet9_ttjj"+SYSs[i]).c_str())->Clone();
    // hscale_HT500Njet9_ttbb[SYSs[i]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_HT500Njet9_ttbb"+SYSs[i]).c_str())->Clone();
    // hscale_HT500Njet9_ttcc[SYSs[i]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_HT500Njet9_ttcc"+SYSs[i]).c_str())->Clone();
    // hscale_HT500Njet9_tt2b[SYSs[i]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_HT500Njet9_tt2b"+SYSs[i]).c_str())->Clone();
    // hscale_HT500Njet9_tt1b[SYSs[i]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_HT500Njet9_tt1b"+SYSs[i]).c_str())->Clone();
    // hscale_STs[SYSs[i]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_STs"+SYSs[i]).c_str())->Clone();
    // hscale_STtw[SYSs[i]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_STtw"+SYSs[i]).c_str())->Clone();
    // hscale_STt[SYSs[i]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_STt"+SYSs[i]).c_str())->Clone();
    // hscale_WJets[SYSs[i]]    = (TH2F*)tfile_HTNJ_SF->Get(("hscale_WJets"+SYSs[i]).c_str())->Clone();
  }
}

HardcodedConditions::~HardcodedConditions() {}

float HardcodedConditions::GetDeepJetRenorm2DSF_HTnj( float HT, int njets, std::string sampleType, std::string sysType ){
  //if( hscale_ttjj.find( sysType ) == hscale_ttjj.end() ) return 1.0;
  if( sampleType == "" ) return 1.0;
  int njets_idx = njets;
  if( njets_idx > 8 ) njets_idx = 8;

  if( sampleType == "tttw" ){
    return hscale_tttw[ sysType ]->GetBinContent( hscale_tttw[ sysType ]->FindBin( njets_idx, HT ) );
  }

  if( sampleType == "tttj" ){
    return hscale_tttj[ sysType ]->GetBinContent( hscale_tttj[ sysType ]->FindBin( njets_idx, HT ) );
  }  

//  if( sampleType == "tttt" ){
//    return hscale_tttt[ sysType ]->GetBinContent( hscale_tttt[ sysType ]->FindBin( njets_idx, HT ) );
//  }  

//if( sampleType == "ttjj" ){
//    return hscale_ttjj[ sysType ]->GetBinContent( hscale_ttjj[ sysType ]->FindBin( njets_idx, HT ) );
//  }  

//  if( sampleType == "ttcc" ){
//    return hscale_ttcc[ sysType ]->GetBinContent( hscale_ttcc[ sysType ]->FindBin( njets_idx, HT ) );
//  }

//  if( sampleType == "ttbb" ){
//    return hscale_ttbb[ sysType ]->GetBinContent( hscale_ttbb[ sysType ]->FindBin( njets_idx, HT ) );
//  }  

//  if( sampleType == "tt2b" ){
//    return hscale_tt2b[ sysType ]->GetBinContent( hscale_tt2b[ sysType ]->FindBin( njets_idx, HT ) );
//  }  

//  if( sampleType == "STs" ){
//    return hscale_STs[ sysType ]->GetBinContent( hscale_STs[ sysType ]->FindBin( njets_idx, HT ) );
//  } 

//  if( sampleType == "STt" ){
//    return hscale_STt[ sysType ]->GetBinContent( hscale_STt[ sysType ]->FindBin( njets_idx, HT ) );
//  }

//  if( sampleType == "STtW" ){
//    return hscale_STtW[ sysType ]->GetBinContent( hscale_STtW[ sysType ]->FindBin( njets_idx, HT ) );
//  }

//  if( sampleType == "WJets" ){
//    return hscale_WJets[ sysType ]->GetBinContent( hscale_WJets[ sysType ]->FindBin( njets_idx, HT ) );
//  }

  return 1.0;  
} 

float HardcodedConditions::GetCrossSectionEfficiency( TString inputFileName, int Year ){
  if( Year == 2016 ){
    return 1.0; // hasn't been implemented yet 
  }
  else if( Year == 2017 ){
    if( inputFileName.Contains( "TTToSemiLeptonic_TuneCP5" ) && inputFileName.Contains( "HT0Njet0" ) ) return 1;
    else if( inputFileName.Contains( "TTToSemiLepton_HT500Njet9_TuneCP5" ) ) return 1;
    else if( inputFileName.Contains( "TTToSemiLeptonic_TuneCP5" ) && inputFileName.Contains( "HT500Njet9" ) ) return 1;
    else if( inputFileName.Contains( "TTToHadronic_TuneCP5" ) ) return 1;
    else if( inputFileName.Contains( "TTTo2L2Nu_TuneCP5" ) ) return 1;
    else if( inputFileName.Contains( "TTTT" ) ) return 1;
    else if( inputFileName.Contains( "TTTW" ) ) return 1;
    else if( inputFileName.Contains( "TTTJ" ) ) return 1;
    else return 1;
  }
  else if( Year == 2018 ){
    return 1.0; // hasn't been implemented yet 
  }
  else return 1.0;
}

float HardcodedConditions::GetBTagWP( int Year, std::string tagger ){
  if( tagger == "deepJet" ){
    if( Year == 2017 ) return 0.3040;
    else if( Year == 2018 ) return 0.2783;
    else if( Year == 2016 ) return 0.2489;
    else return 1.0;
  }
  else if( tagger == "deepCSV" ){
    if( Year == 2017 ) return 0.4506;
    else if( Year == 2018 ) return 0.4168;
    else if( Year == 2016 ) return 0.5847;
    else return 1.0;
  }
  else return 1.0;
}

