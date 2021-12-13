#include "step1_test.cc"
#include "BTagCalibForLJMet.cpp"
#include "HardcodedConditions.cc"
#include<vector>
#include<string>
using namespace std;

void make_step1(TString macroDir, TString inputFile, TString outputFile, string systematics, Int_t Year){

  gROOT->SetMacroPath(macroDir);

  gSystem->AddIncludePath("-I$CMSSW_BASE/src/");

  TString incl("-I");
  incl+=macroDir;
  gSystem->AddIncludePath(incl);

  if ( inputFile.Contains("Run2017") || inputFile.Contains("Run2018") || inputFile.Contains("Single") || inputFile.Contains("Double") || inputFile.Contains("MuonEG") || inputFile.Contains("EGamma") ){ 
    step1_test t( inputFile, outputFile.ReplaceAll(".root","nominal.root"), Year );
      t.Loop("ljmet", "ljmet"); 
  } 
  else {
    vector<TString> shifts = { "nominal" };
    if( systematics == "true" ) vector<TString> shifts = { "JECup", "JECdown", "JERup", "JERdown" };
    for ( size_t i =0; i < shifts.size(); ++i) {
        cout << endl << ">> Running shift " << shifts[i] << endl;
        TString tName = "ljmet";
        if( !shifts[i].Contains("nominal") ){ 
          tName.Append("_"); 
          tName.Append(shifts[i]); 
        }
        step1_test t( inputFile, outputFile.ReplaceAll( ".root",shifts[i].Append(".root") ), Year ); 
        t.saveHistograms();
        t.Loop(tName, "ljmet");
        outputFile.ReplaceAll(shifts[i],".root"); //Change outputFile back to its original name.
    }
  }
}


void make_step1(TString macroDir, string filelist, string systematics, Int_t Year){

  gROOT->SetMacroPath(macroDir);

  gSystem->AddIncludePath("-I$CMSSW_BASE/src/");

  TString incl("-I");
  incl+=macroDir;
  gSystem->AddIncludePath(incl);

  string line;
  ifstream myfile ( filelist );
  vector< pair<string,string> > Files;
  if ( myfile.is_open() ){
    while ( getline ( myfile, line ) ){
      auto pos = line.find(",");
      Files.emplace_back( line.substr( 0, pos ), line.substr( pos + 1 ) );
    }
    myfile.close();

    std::string btagcsvfile("DeepCSV_106XUL17SF.csv");
    std::string btagdjcsvfile("DeepJet_106XUL17SF.csv");
    cout << ">> CSV reshaping file: " << btagcsvfile << endl;
    cout << ">> Deep Jet reshaping file: "<<btagdjcsvfile<< endl;
    auto calib = new const BTagCalibrationForLJMet( "DeepCSV", btagcsvfile ); 
    auto dj_calib = new const BTagCalibrationForLJMet( "DeepJet", btagdjcsvfile );
    for ( auto f : Files ){
      TString inputFile( f.first );
      TString outputFile( f.second );
      if( inputFile.Contains("Run2017") || inputFile.Contains("Run2018") || inputFile.Contains("Single") || inputFile.Contains("Double") || inputFile.Contains("MuonEG") || inputFile.Contains("EGamma") ){ 
        step1_test t( inputFile, outputFile.ReplaceAll( ".root", "nominal.root" ), Year );
        t.Loop( "ljmet", "ljmet", calib, dj_calib );
      } else {
        vector<TString> shifts = { "nominal" }; 
        if( systematics == "true" ) shifts = { "nominal", "JECup", "JECdown", "JERup", "JERdown" };
        for( size_t i = 0; i<shifts.size(); ++i ){
          cout << endl << ">> Running shift " << shifts[i] << endl;
          TString tName = "ljmet";
          if( !shifts[i].Contains("nominal") ){ 
            tName.Append("_"); 
            tName.Append(shifts[i]);
          }
          step1_test t( inputFile, outputFile.ReplaceAll( ".root",shifts[i].Append(".root") ), Year); 
          t.saveHistograms();
          t.Loop( tName, "ljmet", calib, dj_calib );
          outputFile.ReplaceAll(shifts[i],".root"); 
        }
      }
    }
  }
  else cout << "[ERR] Unable to open filelist"; 
}
