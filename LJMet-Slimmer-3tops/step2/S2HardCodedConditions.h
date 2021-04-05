#ifndef S2HardcodedConditions_h
#define S2HardcodedConditions_h

#include <iostream>
#include <vector>
#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TH2.h>
#include <algorithm>


class S2HardcodedConditions{
    
public:
    
    S2HardcodedConditions();
    ~S2HardcodedConditions();

    float GetDeepJetRenorm2DSF_HTnj(float HT, int njets, std::string sampleType);
    float GetCSVRenorm2DSF_HTnj(float HT, int njets, std::string sampleType);

    TFile *tfile_HTNJ_SF;

    TH2F* hscale_tttt_dcsv;
    TH2F* hscale_ttjj_dcsv;
    TH2F* hscale_ttbb_dcsv;
    TH2F* hscale_ttcc_dcsv;
    TH2F* hscale_tt2b_dcsv;
    TH2F* hscale_tt1b_dcsv;
    TH2F* hscale_HT500Njet9_ttjj_dcsv;
    TH2F* hscale_HT500Njet9_ttbb_dcsv;
    TH2F* hscale_HT500Njet9_ttcc_dcsv;
    TH2F* hscale_HT500Njet9_tt2b_dcsv;
    TH2F* hscale_HT500Njet9_tt1b_dcsv;
    TH2F* hscale_STs_dcsv;
    TH2F* hscale_STt_dcsv;
    TH2F* hscale_STtw_dcsv;
    TH2F* hscale_WJets_dcsv;   

    TH2F* hscale_tttt_djet;
    TH2F* hscale_ttjj_djet;
    TH2F* hscale_ttbb_djet;
    TH2F* hscale_ttcc_djet;
    TH2F* hscale_tt2b_djet;
    TH2F* hscale_tt1b_djet;
    TH2F* hscale_HT500Njet9_ttjj_djet;
    TH2F* hscale_HT500Njet9_ttbb_djet;
    TH2F* hscale_HT500Njet9_ttcc_djet;
    TH2F* hscale_HT500Njet9_tt2b_djet;
    TH2F* hscale_HT500Njet9_tt1b_djet;
    TH2F* hscale_STs_djet;
    TH2F* hscale_STt_djet;
    TH2F* hscale_STtw_djet;
    TH2F* hscale_WJets_djet;

};


#endif
