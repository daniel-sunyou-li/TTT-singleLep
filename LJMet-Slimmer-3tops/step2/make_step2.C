#include "step2.cc"
#include "Davismt2.cc"
#include "HardcodedConditions.cc"

void make_step2(TString macroDir, TString inputFile, TString outputFile){

  gROOT->SetMacroPath(macroDir);

  gSystem->AddIncludePath("-I$CMSSW_BASE/src/");

  TString incl("-I");
  incl+=macroDir;
  gSystem->AddIncludePath(incl);

  std::cout << " start makeStep2.C "; 
  step2 t(inputFile,outputFile);
  std::cout << " End of constructor ";
  t.Loop();

}
