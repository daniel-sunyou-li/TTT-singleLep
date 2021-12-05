#ifndef HardcodedConditions_h
#define HardcodedConditions_h

#include <iostream>
#include <vector>
#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TH2.h>
#include <algorithm>

typedef std::map<std::string, TH2F*> SFmap;

class S2HardcodedConditions{
    
public:
    
    HardcodedConditions();
    ~HardcodedConditions();

    float GetCSVRenormSF(int year, int isE, intnjet, std::string sampleType);
    // float GetDeepJetRenorm2DSF(int nljet, int hjet, std::String sampleType);
    float GetDeepJetRenorm2DSF_HTnj(float HT, int njets, std::string sampleType);
    //float GetCSVRenorm2DSF_HTnj(float HT, int njets, std::string sampleType);

    TFile *tfile_HTNJ_SF;

    //SFmap hscale_tttt_dcsv;
    //SFmap hscale_ttjj_dcsv;
    //SFmap hscale_ttbb_dcsv;
    //SFmap hscale_ttcc_dcsv;
    //SFmap hscale_tt2b_dcsv;
    //SFmap hscale_tt1b_dcsv;
    //SFmap hscale_HT500Njet9_ttjj_dcsv;
    //SFmap hscale_HT500Njet9_ttbb_dcsv;
    //SFmap hscale_HT500Njet9_ttcc_dcsv;
    //SFmap hscale_HT500Njet9_tt2b_dcsv;
    //SFmap hscale_HT500Njet9_tt1b_dcsv;
    //SFmap hscale_STs_dcsv;
    //SFmap hscale_STt_dcsv;
    //SFmap hscale_STtw_dcsv;
    //SFmap hscale_WJets_dcsv;   

    SFmap hscale_tttt;
    SFmap hscale_ttjj;
    SFmap hscale_ttbb;
    SFmap hscale_ttcc;
    SFmap hscale_tt2b;
    SFmap hscale_tt1b;
    SFmap hscale_HT500Njet9_ttjj;
    SFmap hscale_HT500Njet9_ttbb;
    SFmap hscale_HT500Njet9_ttcc;
    SFmap hscale_HT500Njet9_tt2b;
    SFmap hscale_HT500Njet9_tt1b;
    SFmap hscale_STs;
    SFmap hscale_STt;
    SFmap hscale_STtw;
    SFmap hscale_WJets;

};


#endif
