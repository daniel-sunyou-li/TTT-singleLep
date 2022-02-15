// -*- C++ -*-
//
// Helper class, provides jet tagging eff, scale factors, etc.
// 
// Inspired from BtagHardcodedConditions in LJMET
// 
// by
//
// Sinan Sagir, November 2019
//

#include <cmath>
#include "HardcodedConditions.h"
#include <unordered_map>

using namespace std;

HardcodedConditions::HardcodedConditions() {
}

HardcodedConditions::~HardcodedConditions() {
}

/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|           B TAGGING SCALE FACTOR SECTION            |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

void HardcodedConditions::GetBtaggingSF(double pt, double eta, double *btagsf, double *btagsfunc, std::string tagger, int jetHFlav, std::string year)
{
  //The main getter for GetBtaggingSF Scale Factors
  *btagsf   = 1.000;
  *btagsfunc = 0.000;
  if( year=="2016APV" ){
  	if      (jetHFlav==5) GetBtaggingSF2016APV(pt, eta, btagsf, btagsfunc, tagger);
  	else if (jetHFlav==4) GetCtaggingSF2016APV(pt, eta, btagsf, btagsfunc, tagger);
  	else                  GetLtaggingSF2016APV(pt, eta, btagsf, btagsfunc, tagger);
  	}
  else if(year=="2016"){
  	if      (jetHFlav==5) GetBtaggingSF2016(pt, eta, btagsf, btagsfunc, tagger);
  	else if (jetHFlav==4) GetCtaggingSF2016(pt, eta, btagsf, btagsfunc, tagger);
  	else                  GetLtaggingSF2016(pt, eta, btagsf, btagsfunc, tagger);
  	}
  else if(year=="2017"){
  	if      (jetHFlav==5) GetBtaggingSF2017(pt, eta, btagsf, btagsfunc, tagger);
  	else if (jetHFlav==4) GetCtaggingSF2017(pt, eta, btagsf, btagsfunc, tagger);
  	else                  GetLtaggingSF2017(pt, eta, btagsf, btagsfunc, tagger);
  	}
  else if(year=="2018"){
  	if      (jetHFlav==5) GetBtaggingSF2018(pt, eta, btagsf, btagsfunc, tagger);
  	else if (jetHFlav==4) GetCtaggingSF2018(pt, eta, btagsf, btagsfunc, tagger);
  	else                  GetLtaggingSF2018(pt, eta, btagsf, btagsfunc, tagger);
  	}
  else{ std::cerr << "Year " << year << " not coded into HardcodedConditions::GetBtaggingSF! Aborting ..." << std::endl; std::abort();}
} //end GetBtaggingSF

// placeholder
void HardcodedConditions::GetBtaggingSF2016APV(double pt, double eta, double *btagsf, double *btagsfunc, std::string tagger)
{
  double pt_ = pt;
	if( tagger == "DeepCSVMEDIUM"){ 
      *btagsf = 1.0;
      *btagsfunc = 0.0;
  }
  else if( tagger == "DeepJetMEDIUM") { 
    *btagsf = 1.0;
    *btagsfunc = 0.0;
  }
  else{ 
    std::cerr << tagger << " not coded into HardcodedConditions::GetBtaggingSF2016APV! Aborting ..." << std::endl; std::abort();
  }
}

void HardcodedConditions::GetBtaggingSF2016(double pt, double eta, double *btagsf, double *btagsfunc, std::string tagger)
{
	double pt_ = pt;
	if(pt > 1000.) pt_ = 1000.;
    if(tagger == "DeepCSVMEDIUM"){ // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation2016Legacy/DeepCSV_2016LegacySF_WP_V1.csv
      *btagsf = 0.653526*((1.+(0.220245*pt_))/(1.+(0.14383*pt_)));
      if(pt < 30)        *btagsfunc = 0.043795019388198853;
      else if(pt < 50)   *btagsfunc = 0.015845479443669319;
      else if(pt < 70)   *btagsfunc = 0.014174085110425949;
      else if(pt < 100)  *btagsfunc = 0.013200919143855572;
      else if(pt < 140)  *btagsfunc = 0.012912030331790447;
      else if(pt < 200)  *btagsfunc = 0.019475525245070457;
      else if(pt < 300)  *btagsfunc = 0.01628459244966507;
      else if(pt < 600)  *btagsfunc = 0.034840557724237442;
      else               *btagsfunc = 0.049875054508447647;
    }
    else if( tagger == "DeepJetMEDIUM") { // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation2016Legacy/DeepJet_2016LegacySF_WP_V1.csv
      *btagsf = 0.922748*((1.+(0.0241884*pt_))/(1.+(0.0223119*pt_)));
      if(pt < 30)        *btagsfunc = 0.046558864414691925;
      else if(pt < 50)   *btagsfunc = 0.016374086961150169;
      else if(pt < 70)   *btagsfunc = 0.014532930217683315;
      else if(pt < 100)  *btagsfunc = 0.012927571311593056;
      else if(pt < 140)  *btagsfunc = 0.012316481210291386;
      else if(pt < 200)  *btagsfunc = 0.014507872052490711;
      else if(pt < 300)  *btagsfunc = 0.016649365425109863;
      else if(pt < 600)  *btagsfunc = 0.030278874561190605;
      else               *btagsfunc = 0.053674362599849701;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetBtaggingSF2016! Aborting ..." << std::endl; std::abort();}

    if(pt > 1000){*btagsfunc *= 2.0;}
    
    if(fabs(eta) > 2.5 or pt < 20.) {*btagsf = 1.0; *btagsfunc = 0.0;}
}

// placeholder
void HardcodedConditions::GetCtaggingSF2016APV(double pt, double eta, double *btagsf, double *btagsfunc, std::string tagger)
{
  double pt_ = pt;
	if( tagger == "DeepCSVMEDIUM"){ 
      *btagsf = 1.0;
      *btagsfunc = 0.0;
  }
  else if( tagger == "DeepJetMEDIUM") { 
    *btagsf = 1.0;
    *btagsfunc = 0.0;
  }
  else{ 
    std::cerr << tagger << " not coded into HardcodedConditions::GetBtaggingSF2016APV! Aborting ..." << std::endl; std::abort();
  }
}

void HardcodedConditions::GetCtaggingSF2016(double pt, double eta, double *btagsf, double *btagsfunc, std::string tagger)
{
	double pt_ = pt;
	if(pt > 1000.) pt_ = 1000.;
    if(tagger == "DeepCSVMEDIUM"){ // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation2016Legacy/DeepCSV_2016LegacySF_WP_V1.csv
      *btagsf = 0.653526*((1.+(0.220245*pt_))/(1.+(0.14383*pt_)));
      if(pt < 30)        *btagsfunc = 0.13138505816459656;
      else if(pt < 50)   *btagsfunc = 0.047536440193653107;
      else if(pt < 70)   *btagsfunc = 0.042522255331277847;
      else if(pt < 100)  *btagsfunc = 0.039602756500244141;
      else if(pt < 140)  *btagsfunc = 0.038736090064048767;
      else if(pt < 200)  *btagsfunc = 0.058426573872566223;
      else if(pt < 300)  *btagsfunc = 0.048853777348995209;
      else if(pt < 600)  *btagsfunc = 0.10452167689800262;
      else               *btagsfunc = 0.14962516725063324;
    }
    else if( tagger == "DeepJetMEDIUM") { // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation2016Legacy/DeepJet_2016LegacySF_WP_V1.csv
      *btagsf = 0.922748*((1.+(0.0241884*pt_))/(1.+(0.0223119*pt_)));
      if(pt < 30)        *btagsfunc = 0.13967660069465637;
      else if(pt < 50)   *btagsfunc = 0.049122259020805359;
      else if(pt < 70)   *btagsfunc = 0.043598789721727371;
      else if(pt < 100)  *btagsfunc = 0.038782715797424316;
      else if(pt < 140)  *btagsfunc = 0.036949444562196732;
      else if(pt < 200)  *btagsfunc = 0.043523617088794708;
      else if(pt < 300)  *btagsfunc = 0.04994809627532959;
      else if(pt < 600)  *btagsfunc = 0.090836621820926666;
      else               *btagsfunc = 0.16102308034896851;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetCtaggingSF2016! Aborting ..." << std::endl; std::abort();}

    if(pt > 1000){*btagsfunc *= 2.0;}
    
    if(fabs(eta) > 2.5 or pt < 20.) {*btagsf = 1.0; *btagsfunc = 0.0;}
}


// placeholder
void HardcodedConditions::GetLtaggingSF2016APV(double pt, double eta, double *btagsf, double *btagsfunc, std::string tagger)
{
  double pt_ = pt;
	if( tagger == "DeepCSVMEDIUM"){ 
      *btagsf = 1.0;
      *btagsfunc = 0.0;
  }
  else if( tagger == "DeepJetMEDIUM") { 
    *btagsf = 1.0;
    *btagsfunc = 0.0;
  }
  else{ 
    std::cerr << tagger << " not coded into HardcodedConditions::GetLtaggingSF2016APV! Aborting ..." << std::endl; std::abort();
  }
}

void HardcodedConditions::GetLtaggingSF2016(double pt, double eta, double *btagsf, double *btagsfunc, std::string tagger)
{
	double pt_ = pt;
	if(pt > 1000.) pt_ = 1000.;
    if(tagger == "DeepCSVMEDIUM"){ // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation2016Legacy/DeepCSV_2016LegacySF_WP_V1.csv
      *btagsf = 1.09286+-0.00052597*pt_+1.88225e-06*pt_*pt_+-1.27417e-09*pt_*pt_*pt_;
      *btagsfunc = 0.101915+0.000192134*pt_+-1.94974e-07*pt_*pt_;
    }
    else if( tagger == "DeepJetMEDIUM") { // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation2016Legacy/DeepJet_2016LegacySF_WP_V1.csv
      *btagsf = 1.09149+3.31851e-05*pt_+2.34826e-07*pt_*pt_+-0.888846/pt_;
      *btagsfunc = 0.127379+0.000199537*pt_+-2.43111e-07*pt_*pt_;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetLtaggingSF2016! Aborting ..." << std::endl; std::abort();}

    if(pt > 1000){*btagsfunc *= 2.0;}
    
    if(fabs(eta) > 2.5 or pt < 20.) {*btagsf = 1.0; *btagsfunc = 0.0;}
}

void HardcodedConditions::GetBtaggingSF2017(double pt, double eta, double *btagsf, double *btagsfunc, std::string tagger)
{
	double pt_ = pt;
	if(pt > 1000.) pt_ = 1000.;
    if(tagger == "DeepCSVMEDIUM"){ //DeepCSV_106XUL17SF_WPonly.csv 
      *btagsf = 0.934639+(5.3539e-06*(log(pt_+19)*(log(pt_+18)*(3-(-(45.0991*log(pt_+18)))))));//2.22144*((1.+(0.540134*pt_))/(1.+(1.30246*pt_)));
      if(pt < 30)        *btagsfunc = 0.036777336150407791;//0.038731977343559265;
      else if(pt < 50)   *btagsfunc = 0.011289253830909729;//0.015137125737965107;
      else if(pt < 70)   *btagsfunc = 0.014985882677137852;//0.013977443799376488;
      else if(pt < 100)  *btagsfunc = 0.011643307283520699;//0.012607076205313206;
      else if(pt < 140)  *btagsfunc = 0.010223580524325371;//0.013979751616716385;
      else if(pt < 200)  *btagsfunc = 0.011323201470077038;//0.015011214651167393;
      else if(pt < 300)  *btagsfunc = 0.026883697137236595;//0.034551065415143967;
      else if(pt < 600)  *btagsfunc = 0.069629497826099396;//0.040168888866901398;
      else               *btagsfunc = 0.088828794658184052;//0.054684814065694809;
    }
    else if( tagger == "DeepJetMEDIUM") { //DeepJet_106XUL17SF_WPonly 
      *btagsf = 0.938414+(1.64274e-05*(log(pt_+19)*(log(pt_+18)*(3-(-(13.223*log(pt_+18)))))));//0.991757*((1.+(0.0209615*pt_))/(1.+(0.0234962*pt_)));
      if(pt < 30)        *btagsfunc = 0.032288491725921631;//0.076275914907455444;
      else if(pt < 50)   *btagsfunc = 0.0099225323647260666;//0.026398291811347008;
      else if(pt < 70)   *btagsfunc = 0.014409177005290985;//0.02534114383161068;
      else if(pt < 100)  *btagsfunc = 0.011234057135879993;//0.02437339723110199;
      else if(pt < 140)  *btagsfunc = 0.0091218706220388412;//0.026176376268267632;
      else if(pt < 200)  *btagsfunc = 0.0090840766206383705;//0.02870459109544754;
      else if(pt < 300)  *btagsfunc = 0.018635481595993042;//0.037160992622375488;
      else if(pt < 600)  *btagsfunc = 0.061456717550754547;//0.036622315645217896;
      else               *btagsfunc = 0.079311750829219818;//0.04215230792760849;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetBtaggingSF2017! Aborting ..." << std::endl; std::abort();}

    if(pt > 1000){*btagsfunc *= 2.0;}
    
    if(fabs(eta) > 2.5 or pt < 20.) {*btagsf = 1.0; *btagsfunc = 0.0;}
}

void HardcodedConditions::GetCtaggingSF2017(double pt, double eta, double *btagsf, double *btagsfunc, std::string tagger)
{
	double pt_ = pt;
	if(pt > 1000.) pt_ = 1000.;
    if(tagger == "DeepCSVMEDIUM"){ //DeepCSV_106XUL17SF_WPonly.csv  
      *btagsf = 0.934639+(5.3539e-06*(log(pt_+19)*(log(pt_+18)*(3-(-(45.0991*log(pt_+18)))))));//2.22144*((1.+(0.540134*pt_))/(1.+(1.30246*pt_)));
      if(pt < 30)        *btagsfunc = 0.11033201217651367;//0.1161959320306778;
      else if(pt < 50)   *btagsfunc = 0.033867761492729187;//0.045411378145217896;
      else if(pt < 70)   *btagsfunc = 0.04495764896273613;//0.041932329535484314;
      else if(pt < 100)  *btagsfunc = 0.034929923713207245;//0.037821229547262192;
      else if(pt < 140)  *btagsfunc = 0.030670741572976112;//0.041939254850149155;
      else if(pt < 200)  *btagsfunc = 0.033969603478908539;//0.045033644884824753;
      else if(pt < 300)  *btagsfunc = 0.080651089549064636;//0.1036531925201416;
      else if(pt < 600)  *btagsfunc = 0.20888850092887878;//0.12050666660070419;
      else               *btagsfunc = 0.26648637652397156;//0.16405443847179413;
    }
    else if( tagger == "DeepJetMEDIUM") { //DeepJet_106XUL17SF_WPonly  
      *btagsf = 0.938414+(1.64274e-05*(log(pt_+19)*(log(pt_+18)*(3-(-(13.223*log(pt_+18))))))); 
      if(pt < 30)        *btagsfunc = 0.096865475177764893;//0.22882774472236633;
      else if(pt < 50)   *btagsfunc = 0.0297675970941782;//0.079194873571395874;
      else if(pt < 70)   *btagsfunc = 0.043227531015872955;//0.07602342963218689;
      else if(pt < 100)  *btagsfunc = 0.033702172338962555;//0.073120191693305969;
      else if(pt < 140)  *btagsfunc = 0.027365611866116524;//0.078529126942157745;
      else if(pt < 200)  *btagsfunc = 0.027252230793237686;//0.086113773286342621;
      else if(pt < 300)  *btagsfunc = 0.055906444787979126;//0.11148297786712646;
      else if(pt < 600)  *btagsfunc = 0.18437016010284424;//0.10986694693565369;
      else               *btagsfunc = 0.23793524503707886;//0.12645691633224487;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetCtaggingSF2017! Aborting ..." << std::endl; std::abort();}

    if(pt > 1000){*btagsfunc *= 2.0;}
    
    if(fabs(eta) > 2.5 or pt < 20.) {*btagsf = 1.0; *btagsfunc = 0.0;}
}

void HardcodedConditions::GetLtaggingSF2017(double pt, double eta, double *btagsf, double *btagsfunc, std::string tagger)
{
	double pt_ = pt;
	if(pt > 1000.) pt_ = 1000.;
    if(tagger == "DeepCSVMEDIUM"){  //DeepCSV_106XUL17SF_WPonly.csv
      *btagsf = 1.09411+-0.000277731*pt_+2.47948e-07*pt_*pt_+-0.65943/pt_;//0.972902+0.000201811*pt_+3.96396e-08*pt_*pt_+-4.53965e-10*pt_*pt_*pt_;
      *btagsfunc = 1-(0.079916+0.000250233*pt_+-2.41117e-07*pt_*pt_);//0.101236+0.000212696*pt_+-1.71672e-07*pt_*pt_;
    }
    else if( tagger == "DeepJetMEDIUM") { //DeepJet_106XUL17SF_WPonly 
      *btagsf = 1.35875+-0.000916722*pt_+6.33425e-07*pt_*pt_+-2.07301/pt_;//1.40779+-0.00094558*pt_+8.74982e-07*pt_*pt_+-4.67814/pt_;
      *btagsfunc = 1-(0.117907+0.000250773*pt_+-3.04922e-07*pt_*pt_);//0.100661+0.000294578*pt_+-3.2739e-07*pt_*pt_;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetLtaggingSF2017! Aborting ..." << std::endl; std::abort();}

    if(pt > 1000){*btagsfunc *= 2.0;}
    
    if(fabs(eta) > 2.5 or pt < 20.) {*btagsf = 1.0; *btagsfunc = 0.0;}
}

void HardcodedConditions::GetBtaggingSF2018(double pt, double eta, double *btagsf, double *btagsfunc, std::string tagger)
{
	double pt_ = pt;
	if(pt > 1000.) pt_ = 1000.;
    if(tagger == "DeepCSVMEDIUM"){ // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation102X/DeepCSV_102XSF_WP_V1.csv
      *btagsf = 0.909339+(0.00354*(log(pt_+19)*(log(pt_+18)*(3-(0.471623*log(pt_+18))))));
      if(pt < 30)        *btagsfunc = 0.065904870629310608;
      else if(pt < 50)   *btagsfunc = 0.015055687166750431;
      else if(pt < 70)   *btagsfunc = 0.013506759889423847;
      else if(pt < 100)  *btagsfunc = 0.015106724575161934;
      else if(pt < 140)  *btagsfunc = 0.014620178379118443;
      else if(pt < 200)  *btagsfunc = 0.012161554768681526;
      else if(pt < 300)  *btagsfunc = 0.016239689663052559;
      else if(pt < 600)  *btagsfunc = 0.039990410208702087;
      else               *btagsfunc = 0.068454340100288391;
    }
    else if( tagger == "DeepJetMEDIUM") { // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation102X/DeepJet_102XSF_WP_V1.csv
      *btagsf = 1.0097+(-(2.89663e-06*(log(pt_+19)*(log(pt_+18)*(3-(-(110.381*log(pt_+18))))))));
      if(pt < 30)        *btagsfunc = 0.064865283668041229;
      else if(pt < 50)   *btagsfunc = 0.015645328909158707;
      else if(pt < 70)   *btagsfunc = 0.013825654052197933;
      else if(pt < 100)  *btagsfunc = 0.012404476292431355;
      else if(pt < 140)  *btagsfunc = 0.011260545812547207;
      else if(pt < 200)  *btagsfunc = 0.011756212450563908;
      else if(pt < 300)  *btagsfunc = 0.01450541615486145;
      else if(pt < 600)  *btagsfunc = 0.034563884139060974;
      else               *btagsfunc = 0.099752180278301239;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetBtaggingSF2018! Aborting ..." << std::endl; std::abort();}

    if(pt > 1000){*btagsfunc *= 2.0;}
    
    if(fabs(eta) > 2.5 or pt < 20.) {*btagsf = 1.0; *btagsfunc = 0.0;}
}

void HardcodedConditions::GetCtaggingSF2018(double pt, double eta, double *btagsf, double *btagsfunc, std::string tagger)
{
	double pt_ = pt;
	if(pt > 1000.) pt_ = 1000.;
    if(tagger == "DeepCSVMEDIUM"){ // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation102X/DeepCSV_102XSF_WP_V1.csv
      *btagsf = 0.909339+(0.00354*(log(pt_+19)*(log(pt_+18)*(3-(0.471623*log(pt_+18))))));
      if(pt < 30)        *btagsfunc = 0.19771461188793182;
      else if(pt < 50)   *btagsfunc = 0.045167062431573868;
      else if(pt < 70)   *btagsfunc = 0.040520280599594116;
      else if(pt < 100)  *btagsfunc = 0.045320175588130951;
      else if(pt < 140)  *btagsfunc = 0.043860536068677902;
      else if(pt < 200)  *btagsfunc = 0.036484666168689728;
      else if(pt < 300)  *btagsfunc = 0.048719070851802826;
      else if(pt < 600)  *btagsfunc = 0.11997123062610626;
      else               *btagsfunc = 0.20536302030086517;
    }
    else if( tagger == "DeepJetMEDIUM") { // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation102X/DeepJet_102XSF_WP_V1.csv
      *btagsf = 1.0097+(-(2.89663e-06*(log(pt_+19)*(log(pt_+18)*(3-(-(110.381*log(pt_+18))))))));
      if(pt < 30)        *btagsfunc = 0.19459584355354309;
      else if(pt < 50)   *btagsfunc = 0.04693598672747612;
      else if(pt < 70)   *btagsfunc = 0.041476961225271225;
      else if(pt < 100)  *btagsfunc = 0.037213429808616638;
      else if(pt < 140)  *btagsfunc = 0.033781636506319046;
      else if(pt < 200)  *btagsfunc = 0.035268638283014297;
      else if(pt < 300)  *btagsfunc = 0.043516248464584351;
      else if(pt < 600)  *btagsfunc = 0.10369165241718292;
      else               *btagsfunc = 0.29925653338432312;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetCtaggingSF2018! Aborting ..." << std::endl; std::abort();}

    if(pt > 1000){*btagsfunc *= 2.0;}
    
    if(fabs(eta) > 2.5 or pt < 20.) {*btagsf = 1.0; *btagsfunc = 0.0;}
}

void HardcodedConditions::GetLtaggingSF2018(double pt, double eta, double *btagsf, double *btagsfunc, std::string tagger)
{
	double pt_ = pt;
	if(pt > 1000.) pt_ = 1000.;
    if(tagger == "DeepCSVMEDIUM"){ // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation102X/DeepCSV_102XSF_WP_V1.csv
      *btagsf = 1.6329+-0.00160255*pt_+1.9899e-06*pt_*pt_+-6.72613e-10*pt_*pt_*pt_;
      *btagsfunc = 0.122811+0.000162564*pt_+-1.66422e-07*pt_*pt_;
    }
    else if( tagger == "DeepJetMEDIUM") { // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation102X/DeepJet_102XSF_WP_V1.csv
      *btagsf = 1.59373+-0.00113028*pt_+8.66631e-07*pt_*pt_+-1.10505/pt_;
      *btagsfunc = 0.142253+0.000227323*pt_+-2.71704e-07*pt_*pt_;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetLtaggingSF2018! Aborting ..." << std::endl; std::abort();}

    if(pt > 1000){*btagsfunc *= 2.0;}
    
    if(fabs(eta) > 2.5 or pt < 20.) {*btagsf = 1.0; *btagsfunc = 0.0;}
}


/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|            B TAGGING EFFICIENCY SECTION            |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

void HardcodedConditions::GetBtaggingEff(double pt, double *eff, std::string tagger, int jetHFlav, std::string year)
{
  //The main getter for GetBtaggingEff Efficiencies
  *eff = 1.000;
  if(year=="2016APV"){
  	if      (jetHFlav==5) GetBtaggingEff2016APV(pt, eff, tagger);
  	else if (jetHFlav==4) GetCtaggingEff2016APV(pt, eff, tagger);
  	else                  GetLtaggingEff2016APV(pt, eff, tagger);
  	}
  else if(year=="2016"){
  	if      (jetHFlav==5) GetBtaggingEff2016(pt, eff, tagger);
  	else if (jetHFlav==4) GetCtaggingEff2016(pt, eff, tagger);
  	else                  GetLtaggingEff2016(pt, eff, tagger);
  	}
  else if(year=="2017"){
  	if      (jetHFlav==5) GetBtaggingEff2017(pt, eff, tagger);
  	else if (jetHFlav==4) GetCtaggingEff2017(pt, eff, tagger);
  	else                  GetLtaggingEff2017(pt, eff, tagger);
  	}
  else if(year=="2018"){
  	if      (jetHFlav==5) GetBtaggingEff2018(pt, eff, tagger);
  	else if (jetHFlav==4) GetCtaggingEff2018(pt, eff, tagger);
  	else                  GetLtaggingEff2018(pt, eff, tagger);
  	}
  else{ std::cerr << "Year " << year << " not coded into HardcodedConditions::GetBtaggingEff! Aborting ..." << std::endl; std::abort();}
}//end GetBtaggingEff

// placeholder
void HardcodedConditions::GetBtaggingEff2016APV(double pt, double *eff, std::string tagger)
{
  *eff = 1.0;
}

void HardcodedConditions::GetBtaggingEff2016(double pt, double *eff, std::string tagger)
{
	// ***** DEEPCSV VALUES ARE REALLY FOR 2017!!!!! ******
    if(tagger == "DeepCSVMEDIUM" or tagger == "SJDeepCSVMEDIUM"){
      if(pt < 30)        *eff = 0.447390;
      else if(pt < 50)   *eff = 0.652679;
      else if(pt < 70)   *eff = 0.704724;
      else if(pt < 100)  *eff = 0.727924;
      else if(pt < 140)  *eff = 0.737712;
      else if(pt < 200)  *eff = 0.731578;
      else if(pt < 300)  *eff = 0.689644;
      else if(pt < 400)  *eff = 0.615546;
      else if(pt < 500)  *eff = 0.552437;
      else if(pt < 600)  *eff = 0.501756;
      else if(pt < 800)  *eff = 0.433998;
      else if(pt < 1000) *eff = 0.318242;
      else if(pt < 1200) *eff = 0.220351;
      else               *eff = 0.140777;
    }
    else if( tagger == "DeepCSVLOOSE" or tagger == "SJDeepCSVLOOSE") {
      if(pt < 30)        *eff = 0.665838;
      else if(pt < 50)   *eff = 0.818215;
      else if(pt < 70)   *eff = 0.856991;
      else if(pt < 100)  *eff = 0.878542;
      else if(pt < 140)  *eff = 0.892642;
      else if(pt < 200)  *eff = 0.898174;
      else if(pt < 300)  *eff = 0.888097;
      else if(pt < 400)  *eff = 0.866256;
      else if(pt < 500)  *eff = 0.850732;
      else if(pt < 600)  *eff = 0.837788;
      else if(pt < 800)  *eff = 0.819362;
      else if(pt < 1000) *eff = 0.769139;
      else if(pt < 1200) *eff = 0.702670;
      else               *eff = 0.609493;
    } // ***** DEEPJET VALUES ARE REAL ****** 
    else if( tagger == "DeepJetLOOSE") {
      if(pt < 30)        *eff = 0.759402;
      else if(pt < 50)   *eff = 0.824510;
      else if(pt < 70)   *eff = 0.855261;
      else if(pt < 100)  *eff = 0.875164;
      else if(pt < 140)  *eff = 0.889594;
      else if(pt < 200)  *eff = 0.903509;
      else if(pt < 300)  *eff = 0.913996;
      else if(pt < 400)  *eff = 0.920554;
      else if(pt < 500)  *eff = 0.919814;
      else if(pt < 600)  *eff = 0.921714;
      else if(pt < 800)  *eff = 0.925330;
      else if(pt < 1000) *eff = 0.918149;
      else if(pt < 1200) *eff = 0.919149;
      else if(pt < 1600) *eff = 0.931211;
      else				 *eff = 0.929134;
    }
    else if( tagger == "DeepJetMEDIUM") {
      if(pt < 30)        *eff = 0.471181;
      else if(pt < 50)   *eff = 0.657978;
      else if(pt < 70)   *eff = 0.712938;
      else if(pt < 100)  *eff = 0.744385;
      else if(pt < 140)  *eff = 0.765768;
      else if(pt < 200)  *eff = 0.783068;
      else if(pt < 300)  *eff = 0.787322;
      else if(pt < 400)  *eff = 0.777034;
      else if(pt < 500)  *eff = 0.760514;
      else if(pt < 600)  *eff = 0.745978;
      else if(pt < 800)  *eff = 0.730742;
      else if(pt < 1000) *eff = 0.697064;
      else if(pt < 1200) *eff = 0.672727;
      else if(pt < 1600) *eff = 0.598563;
      else				 *eff = 0.464567;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetBtaggingEff2016! Aborting ..." << std::endl; std::abort();}
}

void HardcodedConditions::GetCtaggingEff2016APV(double pt, double *eff, std::string tagger)
{
  *eff = 1.0;
}

void HardcodedConditions::GetCtaggingEff2016(double pt, double *eff, std::string tagger)
{
	// ***** DEEPCSV VALUES ARE REALLY FOR 2017!!!!! ******
    if(tagger == "DeepCSVMEDIUM" or tagger == "SJDeepCSVMEDIUM"){
      if(pt < 30)        *eff = 0.070384; //0.057985;
      else if(pt < 50)   *eff = 0.107334; //0.111536;
      else if(pt < 70)   *eff = 0.111125; //0.112216;
      else if(pt < 100)  *eff = 0.119346; //0.120075;
      else if(pt < 140)  *eff = 0.128583; //0.128499;
      else if(pt < 200)  *eff = 0.134354; //0.132918;
      else if(pt < 300)  *eff = 0.127251; //0.126724;
      else if(pt < 400)  *eff = 0.107927; //0.126281;
      else if(pt < 500)  *eff = 0.099135; //0.123026;
      else if(pt < 600)  *eff = 0.081601; //0.124840;
      else if(pt < 800)  *eff = 0.056054; //0.130060;
      else if(pt < 1000) *eff = 0.032320; //0.128022;
      else if(pt < 1200) *eff = 0.014388; //0.134100;
      else               *eff = 0.012887; //0.125348;
    }
    else if( tagger == "DeepCSVLOOSE" or tagger == "SJDeepCSVLOOSE") {
      if(pt < 30)        *eff = 0.288516; //0.206192;
      else if(pt < 50)   *eff = 0.408332; //0.338902;
      else if(pt < 70)   *eff = 0.422585; //0.353516;
      else if(pt < 100)  *eff = 0.438211; //0.366214;
      else if(pt < 140)  *eff = 0.454386; //0.371430;
      else if(pt < 200)  *eff = 0.464604; //0.381838;
      else if(pt < 300)  *eff = 0.453372; //0.374189;
      else if(pt < 400)  *eff = 0.434347; //0.379317;
      else if(pt < 500)  *eff = 0.443035; //0.393696;
      else if(pt < 600)  *eff = 0.419901; //0.404215;
      else if(pt < 800)  *eff = 0.390432; //0.417190;
      else if(pt < 1000) *eff = 0.337017; //0.422815;
      else if(pt < 1200) *eff = 0.267386; //0.402299;
      else               *eff = 0.275773; //0.401114;
    }
    else if( tagger == "DeepJetLOOSE") {
      if(pt < 30)        *eff = 0.477140;
      else if(pt < 50)   *eff = 0.419867;
      else if(pt < 70)   *eff = 0.411881;
      else if(pt < 100)  *eff = 0.412006;
      else if(pt < 140)  *eff = 0.417465;
      else if(pt < 200)  *eff = 0.437310;
      else if(pt < 300)  *eff = 0.474103;
      else if(pt < 400)  *eff = 0.527105;
      else if(pt < 500)  *eff = 0.574946;
      else if(pt < 600)  *eff = 0.590475;
      else if(pt < 800)  *eff = 0.595066;
      else if(pt < 1000) *eff = 0.622047;
      else if(pt < 1200) *eff = 0.638436;
      else if(pt < 1600) *eff = 0.698039;
      else				 *eff = 0.900000;
    }
    else if( tagger == "DeepJetMEDIUM") {
      if(pt < 30)        *eff = 0.109560;
      else if(pt < 50)   *eff = 0.138032;
      else if(pt < 70)   *eff = 0.132161;
      else if(pt < 100)  *eff = 0.132031;
      else if(pt < 140)  *eff = 0.135244;
      else if(pt < 200)  *eff = 0.145503;
      else if(pt < 300)  *eff = 0.166384;
      else if(pt < 400)  *eff = 0.192547;
      else if(pt < 500)  *eff = 0.216578;
      else if(pt < 600)  *eff = 0.221702;
      else if(pt < 800)  *eff = 0.226893;
      else if(pt < 1000) *eff = 0.230419;
      else if(pt < 1200) *eff = 0.206840;
      else if(pt < 1600) *eff = 0.203922;
      else               *eff = 0.400000;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetCtaggingEff2016! Aborting ..." << std::endl; std::abort();}
}

void HardcodedConditions::GetLtaggingEff2016APV(double pt, double *eff, std::string tagger)
{
  *eff = 1.0;
}

void HardcodedConditions::GetLtaggingEff2016(double pt, double *eff, std::string tagger)
{
	// ***** DEEPCSV VALUES ARE REALLY FOR 2017!!!!! ******
    if(tagger == "DeepCSVMEDIUM" || tagger == "SJDeepCSVMEDIUM"){
      if(pt < 30)        *eff = 0.004377;
      else if(pt < 50)   *eff = 0.010659;
      else if(pt < 70)   *eff = 0.009622;
      else if(pt < 100)  *eff = 0.009726;
      else if(pt < 140)  *eff = 0.010565;
      else if(pt < 200)  *eff = 0.011395;
      else if(pt < 300)  *eff = 0.011618;
      else if(pt < 400)  *eff = 0.011412;
      else if(pt < 500)  *eff = 0.011566;
      else if(pt < 600)  *eff = 0.010326;
      else if(pt < 800)  *eff = 0.007474;
      else if(pt < 1000) *eff = 0.005215;
      else if(pt < 1200) *eff = 0.001746;
      else               *eff = 0.001182;
    }
    else if( tagger == "DeepCSVLOOSE" || tagger == "SJDeepCSVLOOSE") {
      if(pt < 30)        *eff = 0.076955;
      else if(pt < 50)   *eff = 0.104639;
      else if(pt < 70)   *eff = 0.099754;
      else if(pt < 100)  *eff = 0.103881;
      else if(pt < 140)  *eff = 0.113770;
      else if(pt < 200)  *eff = 0.126487;
      else if(pt < 300)  *eff = 0.139755;
      else if(pt < 400)  *eff = 0.149181;
      else if(pt < 500)  *eff = 0.158620;
      else if(pt < 600)  *eff = 0.161799;
      else if(pt < 800)  *eff = 0.161169;
      else if(pt < 1000) *eff = 0.159885;
      else if(pt < 1200) *eff = 0.143730;
      else               *eff = 0.131501;
    }
    else if( tagger == "DeepJetLOOSE") {
      if(pt < 30)        *eff = 0.446756;
      else if(pt < 50)   *eff = 0.158561;
      else if(pt < 70)   *eff = 0.109936;
      else if(pt < 100)  *eff = 0.098146;
      else if(pt < 140)  *eff = 0.096993;
      else if(pt < 200)  *eff = 0.108170;
      else if(pt < 300)  *eff = 0.137391;
      else if(pt < 400)  *eff = 0.186428;
      else if(pt < 500)  *eff = 0.233441;
      else if(pt < 600)  *eff = 0.270899;
      else if(pt < 800)  *eff = 0.313911;
      else if(pt < 1000) *eff = 0.396140;
      else if(pt < 1200) *eff = 0.461929;
      else if(pt < 1600) *eff = 0.552249;
      else               *eff = 0.682292;
    }
    else if( tagger == "DeepJetMEDIUM") {
      if(pt < 30)        *eff = 0.013025;
      else if(pt < 50)   *eff = 0.015275;
      else if(pt < 70)   *eff = 0.010233;
      else if(pt < 100)  *eff = 0.009397;
      else if(pt < 140)  *eff = 0.009666;
      else if(pt < 200)  *eff = 0.011638;
      else if(pt < 300)  *eff = 0.016291;
      else if(pt < 400)  *eff = 0.025791;
      else if(pt < 500)  *eff = 0.037945;
      else if(pt < 600)  *eff = 0.049457;
      else if(pt < 800)  *eff = 0.065214;
      else if(pt < 1000) *eff = 0.091311;
      else if(pt < 1200) *eff = 0.100395;
      else if(pt < 1600) *eff = 0.122354;
      else				 *eff = 0.156250;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetLtaggingEff2016! Aborting ..." << std::endl; std::abort();}
}

void HardcodedConditions::GetBtaggingEff2017(double pt, double *eff, std::string tagger)
{
    if(tagger == "DeepCSVMEDIUM" or tagger == "SJDeepCSVMEDIUM"){
      if(pt < 30)        *eff = 0.447390;
      else if(pt < 50)   *eff = 0.652679;
      else if(pt < 70)   *eff = 0.704724;
      else if(pt < 100)  *eff = 0.727924;
      else if(pt < 140)  *eff = 0.737712;
      else if(pt < 200)  *eff = 0.731578;
      else if(pt < 300)  *eff = 0.689644;
      else if(pt < 400)  *eff = 0.615546;
      else if(pt < 500)  *eff = 0.552437;
      else if(pt < 600)  *eff = 0.501756;
      else if(pt < 800)  *eff = 0.433998;
      else if(pt < 1000) *eff = 0.318242;
      else if(pt < 1200) *eff = 0.220351;
      else               *eff = 0.140777;
    }
    else if( tagger == "DeepCSVLOOSE" or tagger == "SJDeepCSVLOOSE") {
      if(pt < 30)        *eff = 0.665838;
      else if(pt < 50)   *eff = 0.818215;
      else if(pt < 70)   *eff = 0.856991;
      else if(pt < 100)  *eff = 0.878542;
      else if(pt < 140)  *eff = 0.892642;
      else if(pt < 200)  *eff = 0.898174;
      else if(pt < 300)  *eff = 0.888097;
      else if(pt < 400)  *eff = 0.866256;
      else if(pt < 500)  *eff = 0.850732;
      else if(pt < 600)  *eff = 0.837788;
      else if(pt < 800)  *eff = 0.819362;
      else if(pt < 1000) *eff = 0.769139;
      else if(pt < 1200) *eff = 0.702670;
      else               *eff = 0.609493;
    }
    else if( tagger == "DeepJetLOOSE") {
      if(pt < 30)        *eff = 0.851718;
      else if(pt < 50)   *eff = 0.884214;
      else if(pt < 70)   *eff = 0.907905;
      else if(pt < 100)  *eff = 0.922352;
      else if(pt < 140)  *eff = 0.932389;
      else if(pt < 200)  *eff = 0.940210;
      else if(pt < 300)  *eff = 0.944604;
      else if(pt < 400)  *eff = 0.946136;
      else if(pt < 500)  *eff = 0.946462;
      else if(pt < 600)  *eff = 0.945494;
      else if(pt < 800)  *eff = 0.946109;
      else if(pt < 1000) *eff = 0.948120;
      else if(pt < 1200) *eff = 0.936282;
      else if(pt < 1600) *eff = 0.938925;
      else               *eff = 0.948529;
    }
    else if( tagger == "DeepJetMEDIUM") {
      if(pt < 30)        *eff = 0.575387;
      else if(pt < 50)   *eff = 0.741632;
      else if(pt < 70)   *eff = 0.786534;
      else if(pt < 100)  *eff = 0.811308;
      else if(pt < 140)  *eff = 0.828136;
      else if(pt < 200)  *eff = 0.840061;
      else if(pt < 300)  *eff = 0.841153;
      else if(pt < 400)  *eff = 0.829102;
      else if(pt < 500)  *eff = 0.814186;
      else if(pt < 600)  *eff = 0.800483;
      else if(pt < 800)  *eff = 0.783784;
      else if(pt < 1000) *eff = 0.757304;
      else if(pt < 1200) *eff = 0.726879;
      else if(pt < 1600) *eff = 0.697068;
      else				 *eff = 0.588235;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetBtaggingEff2017! Aborting ..." << std::endl; std::abort();}
}

void HardcodedConditions::GetCtaggingEff2017(double pt, double *eff, std::string tagger)
{
    if(tagger == "DeepCSVMEDIUM" or tagger == "SJDeepCSVMEDIUM"){
      if(pt < 30)        *eff = 0.070384;
      else if(pt < 50)   *eff = 0.107334;
      else if(pt < 70)   *eff = 0.111125;
      else if(pt < 100)  *eff = 0.119346;
      else if(pt < 140)  *eff = 0.128583;
      else if(pt < 200)  *eff = 0.134354;
      else if(pt < 300)  *eff = 0.127251;
      else if(pt < 400)  *eff = 0.107927;
      else if(pt < 500)  *eff = 0.099135;
      else if(pt < 600)  *eff = 0.081601;
      else if(pt < 800)  *eff = 0.056054;
      else if(pt < 1000) *eff = 0.032320;
      else if(pt < 1200) *eff = 0.014388;
      else               *eff = 0.012887;
    }
    else if( tagger == "DeepCSVLOOSE" or tagger == "SJDeepCSVLOOSE") {
      if(pt < 30)        *eff = 0.288516;
      else if(pt < 50)   *eff = 0.408332;
      else if(pt < 70)   *eff = 0.422585;
      else if(pt < 100)  *eff = 0.438211;
      else if(pt < 140)  *eff = 0.454386;
      else if(pt < 200)  *eff = 0.464604;
      else if(pt < 300)  *eff = 0.453372;
      else if(pt < 400)  *eff = 0.434347;
      else if(pt < 500)  *eff = 0.443035;
      else if(pt < 600)  *eff = 0.419901;
      else if(pt < 800)  *eff = 0.390432;
      else if(pt < 1000) *eff = 0.337017;
      else if(pt < 1200) *eff = 0.267386;
      else               *eff = 0.275773;
    }
    else if( tagger == "DeepJetLOOSE") {
      if(pt < 30)        *eff = 0.606140;
      else if(pt < 50)   *eff = 0.506422;
      else if(pt < 70)   *eff = 0.487623;
      else if(pt < 100)  *eff = 0.478236;
      else if(pt < 140)  *eff = 0.476632;
      else if(pt < 200)  *eff = 0.489872;
      else if(pt < 300)  *eff = 0.516671;
      else if(pt < 400)  *eff = 0.561243;
      else if(pt < 500)  *eff = 0.608884;
      else if(pt < 600)  *eff = 0.618029;
      else if(pt < 800)  *eff = 0.615539;
      else if(pt < 1000) *eff = 0.638375;
      else if(pt < 1200) *eff = 0.632394;
      else if(pt < 1600) *eff = 0.719745;
      else				 *eff = 0.771429;
    }
    else if( tagger == "DeepJetMEDIUM") {
      if(pt < 30)        *eff = 0.138400;
      else if(pt < 50)   *eff = 0.164792;
      else if(pt < 70)   *eff = 0.147040;
      else if(pt < 100)  *eff = 0.143868;
      else if(pt < 140)  *eff = 0.145936;
      else if(pt < 200)  *eff = 0.155583;
      else if(pt < 300)  *eff = 0.174800;
      else if(pt < 400)  *eff = 0.203433;
      else if(pt < 500)  *eff = 0.229636;
      else if(pt < 600)  *eff = 0.231657;
      else if(pt < 800)  *eff = 0.233721;
      else if(pt < 1000) *eff = 0.224901;
      else if(pt < 1200) *eff = 0.214085;
      else if(pt < 1600) *eff = 0.270701;
      else				 *eff = 0.228571;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetCtaggingEff2017! Aborting ..." << std::endl; std::abort();}
}

void HardcodedConditions::GetLtaggingEff2017(double pt, double *eff, std::string tagger)
{
    if(tagger == "DeepCSVMEDIUM" || tagger == "SJDeepCSVMEDIUM"){
      if(pt < 30)        *eff = 0.004377;
      else if(pt < 50)   *eff = 0.010659;
      else if(pt < 70)   *eff = 0.009622;
      else if(pt < 100)  *eff = 0.009726;
      else if(pt < 140)  *eff = 0.010565;
      else if(pt < 200)  *eff = 0.011395;
      else if(pt < 300)  *eff = 0.011618;
      else if(pt < 400)  *eff = 0.011412;
      else if(pt < 500)  *eff = 0.011566;
      else if(pt < 600)  *eff = 0.010326;
      else if(pt < 800)  *eff = 0.007474;
      else if(pt < 1000) *eff = 0.005215;
      else if(pt < 1200) *eff = 0.001746;
      else               *eff = 0.001182;
    }
    else if( tagger == "DeepCSVLOOSE" || tagger == "SJDeepCSVLOOSE") {
      if(pt < 30)        *eff = 0.076955;
      else if(pt < 50)   *eff = 0.104639;
      else if(pt < 70)   *eff = 0.099754;
      else if(pt < 100)  *eff = 0.103881;
      else if(pt < 140)  *eff = 0.113770;
      else if(pt < 200)  *eff = 0.126487;
      else if(pt < 300)  *eff = 0.139755;
      else if(pt < 400)  *eff = 0.149181;
      else if(pt < 500)  *eff = 0.158620;
      else if(pt < 600)  *eff = 0.161799;
      else if(pt < 800)  *eff = 0.161169;
      else if(pt < 1000) *eff = 0.159885;
      else if(pt < 1200) *eff = 0.143730;
      else               *eff = 0.131501;
    }
    else if( tagger == "DeepJetLOOSE") {
      if(pt < 30)        *eff = 0.651013;
      else if(pt < 50)   *eff = 0.210108;
      else if(pt < 70)   *eff = 0.134127;
      else if(pt < 100)  *eff = 0.112109;
      else if(pt < 140)  *eff = 0.106110;
      else if(pt < 200)  *eff = 0.111936;
      else if(pt < 300)  *eff = 0.133864;
      else if(pt < 400)  *eff = 0.167843;
      else if(pt < 500)  *eff = 0.202058;
      else if(pt < 600)  *eff = 0.227584;
      else if(pt < 800)  *eff = 0.263326;
      else if(pt < 1000) *eff = 0.329590;
      else if(pt < 1200) *eff = 0.400291;
      else if(pt < 1600) *eff = 0.486617;
      else				 *eff = 0.646341;
    }
    else if( tagger == "DeepJetMEDIUM") {
      if(pt < 30)        *eff = 0.015401;
      else if(pt < 50)   *eff = 0.022976;
      else if(pt < 70)   *eff = 0.012974;
      else if(pt < 100)  *eff = 0.010330;
      else if(pt < 140)  *eff = 0.009675;
      else if(pt < 200)  *eff = 0.010583;
      else if(pt < 300)  *eff = 0.013391;
      else if(pt < 400)  *eff = 0.018188;
      else if(pt < 500)  *eff = 0.024087;
      else if(pt < 600)  *eff = 0.029274;
      else if(pt < 800)  *eff = 0.036472;
      else if(pt < 1000) *eff = 0.048173;
      else if(pt < 1200) *eff = 0.053652;
      else if(pt < 1600) *eff = 0.069888;
      else				 *eff = 0.060976;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetLtaggingEff2017! Aborting ..." << std::endl; std::abort();}
}

void HardcodedConditions::GetBtaggingEff2018(double pt, double *eff, std::string tagger)
{
    if(tagger == "DeepCSVMEDIUM" or tagger == "SJDeepCSVMEDIUM"){
      if(pt < 30)        *eff = 0.403823;
      else if(pt < 50)   *eff = 0.618852;
      else if(pt < 70)   *eff = 0.679287;
      else if(pt < 100)  *eff = 0.706293;
      else if(pt < 140)  *eff = 0.717887;
      else if(pt < 200)  *eff = 0.713093;
      else if(pt < 300)  *eff = 0.670051;
      else if(pt < 400)  *eff = 0.59587; 
      else if(pt < 500)  *eff = 0.531372;
      else if(pt < 600)  *eff = 0.483849;
      else if(pt < 800)  *eff = 0.417429;
      else if(pt < 1000) *eff = 0.30052; 
      else if(pt < 1200) *eff = 0.20051; 
      else               *eff = 0.124058;
    }
    else if( tagger == "DeepCSVLOOSE" or tagger == "SJDeepCSVLOOSE") {
      if(pt < 30)        *eff = 0.628235;
      else if(pt < 50)   *eff = 0.794337;
      else if(pt < 70)   *eff = 0.839644;
      else if(pt < 100)  *eff = 0.863855;
      else if(pt < 140)  *eff = 0.878786;
      else if(pt < 200)  *eff = 0.88415;
      else if(pt < 300)  *eff = 0.872817;
      else if(pt < 400)  *eff = 0.850809;
      else if(pt < 500)  *eff = 0.834119;
      else if(pt < 600)  *eff = 0.824796;
      else if(pt < 800)  *eff = 0.802984;
      else if(pt < 1000) *eff = 0.751513;
      else if(pt < 1200) *eff = 0.684949;
      else               *eff = 0.598841;
    }
    else if( tagger == "DeepJetLOOSE") {
      if(pt < 30)        *eff = 0.851020;
      else if(pt < 50)   *eff = 0.876084;
      else if(pt < 70)   *eff = 0.900523;
      else if(pt < 100)  *eff = 0.915644;
      else if(pt < 140)  *eff = 0.925711;
      else if(pt < 200)  *eff = 0.933620;
      else if(pt < 300)  *eff = 0.938040;
      else if(pt < 400)  *eff = 0.940265;
      else if(pt < 500)  *eff = 0.939513;
      else if(pt < 600)  *eff = 0.941458;
      else if(pt < 800)  *eff = 0.941525;
      else if(pt < 1000) *eff = 0.942361;
      else if(pt < 1200) *eff = 0.942157;
      else if(pt < 1600) *eff = 0.942434;
      else				 *eff = 0.971631;
    } else if( tagger == "DeepJetMEDIUM") {
      if(pt < 30)        *eff = 0.550569;
      else if(pt < 50)   *eff = 0.729405;
      else if(pt < 70)   *eff = 0.779659;
      else if(pt < 100)  *eff = 0.806085;
      else if(pt < 140)  *eff = 0.823140;
      else if(pt < 200)  *eff = 0.835408;
      else if(pt < 300)  *eff = 0.835926;
      else if(pt < 400)  *eff = 0.824441;
      else if(pt < 500)  *eff = 0.809940;
      else if(pt < 600)  *eff = 0.798645;
      else if(pt < 800)  *eff = 0.777866;
      else if(pt < 1000) *eff = 0.762113;
      else if(pt < 1200) *eff = 0.724929;
      else if(pt < 1600) *eff = 0.671053;
      else               *eff = 0.638298;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetBtaggingEff2018! Aborting ..." << std::endl; std::abort();}
}

void HardcodedConditions::GetCtaggingEff2018(double pt, double *eff, std::string tagger)
{
    if(tagger == "DeepCSVMEDIUM" or tagger == "SJDeepCSVMEDIUM"){
      if(pt < 30)        *eff = 0.055637;
      else if(pt < 50)   *eff = 0.089934;
      else if(pt < 70)   *eff = 0.09309;
      else if(pt < 100)  *eff = 0.099994;
      else if(pt < 140)  *eff = 0.108785;
      else if(pt < 200)  *eff = 0.114926;
      else if(pt < 300)  *eff = 0.110015;
      else if(pt < 400)  *eff = 0.093696;
      else if(pt < 500)  *eff = 0.087263;
      else if(pt < 600)  *eff = 0.068838;
      else if(pt < 800)  *eff = 0.047241;
      else if(pt < 1000) *eff = 0.022655;
      else if(pt < 1200) *eff = 0.015532;
      else               *eff = 0.008043;
    }
    else if( tagger == "DeepCSVLOOSE" or tagger == "SJDeepCSVLOOSE") {
      if(pt < 30)        *eff = 0.255572;
      else if(pt < 50)   *eff = 0.362164;
      else if(pt < 70)   *eff = 0.376513;
      else if(pt < 100)  *eff = 0.392257;
      else if(pt < 140)  *eff = 0.408828;
      else if(pt < 200)  *eff = 0.419713;
      else if(pt < 300)  *eff = 0.410212;
      else if(pt < 400)  *eff = 0.39379;
      else if(pt < 500)  *eff = 0.408445;
      else if(pt < 600)  *eff = 0.391614;
      else if(pt < 800)  *eff = 0.354956;
      else if(pt < 1000) *eff = 0.318908;
      else if(pt < 1200) *eff = 0.27957;
      else               *eff = 0.243968;
    }
    else if( tagger == "DeepJetLOOSE") {
      if(pt < 30)        *eff = 0.623290;
      else if(pt < 50)   *eff = 0.487405;
      else if(pt < 70)   *eff = 0.466320;
      else if(pt < 100)  *eff = 0.457424;
      else if(pt < 140)  *eff = 0.455686;
      else if(pt < 200)  *eff = 0.467629;
      else if(pt < 300)  *eff = 0.496279;
      else if(pt < 400)  *eff = 0.542364;
      else if(pt < 500)  *eff = 0.592628;
      else if(pt < 600)  *eff = 0.599028;
      else if(pt < 800)  *eff = 0.607188;
      else if(pt < 1000) *eff = 0.619593;
      else if(pt < 1200) *eff = 0.632199;
      else if(pt < 1600) *eff = 0.729814;
      else				 *eff = 0.758621;
    }
    else if( tagger == "DeepJetMEDIUM") {
      if(pt < 30)        *eff = 0.129218;
      else if(pt < 50)   *eff = 0.167245;
      else if(pt < 70)   *eff = 0.150488;
      else if(pt < 100)  *eff = 0.145313;
      else if(pt < 140)  *eff = 0.146303;
      else if(pt < 200)  *eff = 0.154596;
      else if(pt < 300)  *eff = 0.174328;
      else if(pt < 400)  *eff = 0.201489;
      else if(pt < 500)  *eff = 0.223132;
      else if(pt < 600)  *eff = 0.224519;
      else if(pt < 800)  *eff = 0.228117;
      else if(pt < 1000) *eff = 0.223919;
      else if(pt < 1200) *eff = 0.200262;
      else if(pt < 1600) *eff = 0.267081;
      else               *eff = 0.137931;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetCtaggingEff2018! Aborting ..." << std::endl; std::abort();}
}

void HardcodedConditions::GetLtaggingEff2018(double pt, double *eff, std::string tagger)
{
    if(tagger == "DeepCSVMEDIUM" || tagger == "SJDeepCSVMEDIUM"){
      if(pt < 30)        *eff = 0.00308;
      else if(pt < 50)   *eff = 0.007497;
      else if(pt < 70)   *eff = 0.006558;
      else if(pt < 100)  *eff = 0.006771;
      else if(pt < 140)  *eff = 0.00761;
      else if(pt < 200)  *eff = 0.008422;
      else if(pt < 300)  *eff = 0.009002;
      else if(pt < 400)  *eff = 0.00957;
      else if(pt < 500)  *eff = 0.010041;
      else if(pt < 600)  *eff = 0.00947;
      else if(pt < 800)  *eff = 0.007225;
      else if(pt < 1000) *eff = 0.00395;
      else if(pt < 1200) *eff = 0.002117;
      else               *eff = 0.001617;
    }
    else if( tagger == "DeepCSVLOOSE" || tagger == "SJDeepCSVLOOSE") {
      if(pt < 30)        *eff = 0.086838;
      else if(pt < 50)   *eff = 0.090621;
      else if(pt < 70)   *eff = 0.078963;
      else if(pt < 100)  *eff = 0.081875;
      else if(pt < 140)  *eff = 0.091066;
      else if(pt < 200)  *eff = 0.102062;
      else if(pt < 300)  *eff = 0.114996;
      else if(pt < 400)  *eff = 0.127951;
      else if(pt < 500)  *eff = 0.142193;
      else if(pt < 600)  *eff = 0.149584;
      else if(pt < 800)  *eff = 0.153378;
      else if(pt < 1000) *eff = 0.152735;
      else if(pt < 1200) *eff = 0.141539;
      else               *eff = 0.124475;
    }
    else if( tagger == "DeepJetLOOSE") {
      if(pt < 30)        *eff = 0.711314;
      else if(pt < 50)   *eff = 0.218544;
      else if(pt < 70)   *eff = 0.126203;
      else if(pt < 100)  *eff = 0.101815;
      else if(pt < 140)  *eff = 0.094655;
      else if(pt < 200)  *eff = 0.098919;
      else if(pt < 300)  *eff = 0.119787;
      else if(pt < 400)  *eff = 0.156960;
      else if(pt < 500)  *eff = 0.194404;
      else if(pt < 600)  *eff = 0.224125;
      else if(pt < 800)  *eff = 0.267105;
      else if(pt < 1000) *eff = 0.341202;
      else if(pt < 1200) *eff = 0.433265;
      else if(pt < 1600) *eff = 0.529856;
      else				 *eff = 0.677054;
    }
    else if( tagger == "DeepJetMEDIUM") {
      if(pt < 30)        *eff = 0.016255;
      else if(pt < 50)   *eff = 0.022813;
      else if(pt < 70)   *eff = 0.012405;
      else if(pt < 100)  *eff = 0.009765;
      else if(pt < 140)  *eff = 0.009090;
      else if(pt < 200)  *eff = 0.009873;
      else if(pt < 300)  *eff = 0.012624;
      else if(pt < 400)  *eff = 0.018061;
      else if(pt < 500)  *eff = 0.024528;
      else if(pt < 600)  *eff = 0.029325;
      else if(pt < 800)  *eff = 0.037422;
      else if(pt < 1000) *eff = 0.048407;
      else if(pt < 1200) *eff = 0.064141;
      else if(pt < 1600) *eff = 0.066138;
      else				 *eff = 0.082153;
    }else{ std::cerr << "Tagger " << tagger << " not coded into HardcodedConditions::GetLtaggingEff2018! Aborting ..." << std::endl; std::abort();}
}



/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|           HOT TAGGER SCALE FACTOR SECTION           |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

void HardcodedConditions::GetHOTtaggingSF(double pt, int njet, double *hotsf, double *hotstatunc, double *hotcspurunc, double *hotclosureunc, std::string year, bool isGenMatched, std::string workingpoint)
{
  //The main getter for GetHOTtaggingSF Scale Factors
  *hotsf   = 1.000;
  *hotstatunc = 0.000;
  *hotcspurunc = 0.000;
  *hotclosureunc = 0.000;
  if(isGenMatched){
  	if      (year=="2016APV") GetHOTtaggingSF2016APV(pt, njet, hotsf, hotstatunc, hotcspurunc, hotclosureunc, workingpoint);
    else if (year=="2016") GetHOTtaggingSF2016(pt, njet, hotsf, hotstatunc, hotcspurunc, hotclosureunc, workingpoint);
  	else if (year=="2017") GetHOTtaggingSF2017(pt, njet, hotsf, hotstatunc, hotcspurunc, hotclosureunc, workingpoint);
  	else if (year=="2018") GetHOTtaggingSF2018(pt, njet, hotsf, hotstatunc, hotcspurunc, hotclosureunc, workingpoint);
  	}
  else{
  	if      (year=="2016APV") GetHOTmistagSF2016APV(pt, njet, hotsf, hotstatunc, hotcspurunc, hotclosureunc, workingpoint);
  	else if (year=="2016") GetHOTmistagSF2016(pt, njet, hotsf, hotstatunc, hotcspurunc, hotclosureunc, workingpoint);
  	else if (year=="2017") GetHOTmistagSF2017(pt, njet, hotsf, hotstatunc, hotcspurunc, hotclosureunc, workingpoint);
  	else if (year=="2018") GetHOTmistagSF2018(pt, njet, hotsf, hotstatunc, hotcspurunc, hotclosureunc, workingpoint);
  	}
}//end GetHOTtaggingSF


void HardcodedConditions::GetHOTtaggingSF2016APV(double pt, int njet, double *hotsf, double *hotstatunc, double *hotcspurunc, double *hotclosureunc, std::string workingpoint)
{
	// VALUES from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSYHOTGroup
	ptMins = {0,150,250,300,350,400,450,500,600};
	njetMins = {4,5,6,7,8,9,10};
	if (workingpoint=="1pfake"){
		*hotsf = 1.0234;
		*hotstatunc = 0.0193;
		hotCSpurUncs = {0.0356,0.0011,0.0015,0.002,0.0025,0.0051,0.0077,0.0037,0.0487};
		int bin = findBin(pt, ptMins);
		*hotcspurunc = hotCSpurUncs[bin];
		hotClosureUncs = {0.3032,0.0464,0.0461,0.0515,0.0808,0.1396,0.1744};
		bin = findBin(njet, njetMins);
		*hotclosureunc = hotClosureUncs[bin];
		}
	else if (workingpoint=="2pfake"){
		*hotsf = 1.0470;
		*hotstatunc = 0.0176;
		hotCSpurUncs = {0.0376,0.0007,0.0017,0.002,0.003,0.0042,0.0065,0.0033,0.046};
		int bin = findBin(pt, ptMins);
		*hotcspurunc = hotCSpurUncs[bin];
		hotClosureUncs = {0.0282,0.0282,0.084,0.0561,0.0619,0.0903,0.1053};
		bin = findBin(njet, njetMins);
		*hotclosureunc = hotClosureUncs[bin];
		}
	else if (workingpoint=="5pfake"){
		*hotsf = 1.0055;
		*hotstatunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotcspurunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotclosureunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		}
	else if (workingpoint=="10pfake"){
		*hotsf = 1.0093;
		*hotstatunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotcspurunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotclosureunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		}
	else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingSF2016! Aborting ..." << std::endl; std::abort();}
}

void HardcodedConditions::GetHOTtaggingSF2016(double pt, int njet, double *hotsf, double *hotstatunc, double *hotcspurunc, double *hotclosureunc, std::string workingpoint)
{
	// VALUES from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSYHOTGroup
	ptMins = {0,150,250,300,350,400,450,500,600};
	njetMins = {4,5,6,7,8,9,10};
	if (workingpoint=="1pfake"){
		*hotsf = 1.0234;
		*hotstatunc = 0.0193;
		hotCSpurUncs = {0.0356,0.0011,0.0015,0.002,0.0025,0.0051,0.0077,0.0037,0.0487};
		int bin = findBin(pt, ptMins);
		*hotcspurunc = hotCSpurUncs[bin];
		hotClosureUncs = {0.3032,0.0464,0.0461,0.0515,0.0808,0.1396,0.1744};
		bin = findBin(njet, njetMins);
		*hotclosureunc = hotClosureUncs[bin];
		}
	else if (workingpoint=="2pfake"){
		*hotsf = 1.0470;
		*hotstatunc = 0.0176;
		hotCSpurUncs = {0.0376,0.0007,0.0017,0.002,0.003,0.0042,0.0065,0.0033,0.046};
		int bin = findBin(pt, ptMins);
		*hotcspurunc = hotCSpurUncs[bin];
		hotClosureUncs = {0.0282,0.0282,0.084,0.0561,0.0619,0.0903,0.1053};
		bin = findBin(njet, njetMins);
		*hotclosureunc = hotClosureUncs[bin];
		}
	else if (workingpoint=="5pfake"){
		*hotsf = 1.0055;
		*hotstatunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotcspurunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotclosureunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		}
	else if (workingpoint=="10pfake"){
		*hotsf = 1.0093;
		*hotstatunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotcspurunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotclosureunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		}
	else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingSF2016! Aborting ..." << std::endl; std::abort();}
}

void HardcodedConditions::GetHOTmistagSF2016APV(double pt, int njet, double *hotsf, double *hotstatunc, double *hotcspurunc, double *hotclosureunc, std::string workingpoint)
{
	// VALUES from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSYHOTGroup
	ptMins = {0,150,250,300,350,400,450,500,600};
	njetMins = {4,5,6,7,8,9,10};
	if (workingpoint=="1pfake"){
		*hotsf = 0.9071;
		*hotstatunc = 0.0070;
		hotCSpurUncs = {0.0278,0.0311,0.0342,0.0376,0.0403,0.0405,0.0375,0.0439,0.0648};
		int bin = findBin(pt, ptMins);
		*hotcspurunc = hotCSpurUncs[bin];
		hotClosureUncs = {0.0531,0.0821,0.0154,0.0779,0.211,0.2536,0.2935};
		bin = findBin(njet, njetMins);
		*hotclosureunc = hotClosureUncs[bin];
		}
	else if (workingpoint=="2pfake"){
		*hotsf = 0.9126;
		*hotstatunc = 0.0053;
		hotCSpurUncs = {0.0168,0.0199,0.0231,0.0262,0.0286,0.0289,0.0268,0.0313,0.0467};
		int bin = findBin(pt, ptMins);
		*hotcspurunc = hotCSpurUncs[bin];
		hotClosureUncs = {0.0306,0.0555,0.0047,0.0758,0.1999,0.2308,0.3003};
		bin = findBin(njet, njetMins);
		*hotclosureunc = hotClosureUncs[bin];
		}
	else if (workingpoint=="5pfake"){
		*hotsf = 0.9298;
		*hotstatunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotcspurunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotclosureunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		}
	else if (workingpoint=="10pfake"){
		*hotsf = 0.9194;
		*hotstatunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotcspurunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotclosureunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		}
	else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTmistagSF2016! Aborting ..." << std::endl; std::abort();}
}

void HardcodedConditions::GetHOTmistagSF2016(double pt, int njet, double *hotsf, double *hotstatunc, double *hotcspurunc, double *hotclosureunc, std::string workingpoint)
{
	// VALUES from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSYHOTGroup
	ptMins = {0,150,250,300,350,400,450,500,600};
	njetMins = {4,5,6,7,8,9,10};
	if (workingpoint=="1pfake"){
		*hotsf = 0.9071;
		*hotstatunc = 0.0070;
		hotCSpurUncs = {0.0278,0.0311,0.0342,0.0376,0.0403,0.0405,0.0375,0.0439,0.0648};
		int bin = findBin(pt, ptMins);
		*hotcspurunc = hotCSpurUncs[bin];
		hotClosureUncs = {0.0531,0.0821,0.0154,0.0779,0.211,0.2536,0.2935};
		bin = findBin(njet, njetMins);
		*hotclosureunc = hotClosureUncs[bin];
		}
	else if (workingpoint=="2pfake"){
		*hotsf = 0.9126;
		*hotstatunc = 0.0053;
		hotCSpurUncs = {0.0168,0.0199,0.0231,0.0262,0.0286,0.0289,0.0268,0.0313,0.0467};
		int bin = findBin(pt, ptMins);
		*hotcspurunc = hotCSpurUncs[bin];
		hotClosureUncs = {0.0306,0.0555,0.0047,0.0758,0.1999,0.2308,0.3003};
		bin = findBin(njet, njetMins);
		*hotclosureunc = hotClosureUncs[bin];
		}
	else if (workingpoint=="5pfake"){
		*hotsf = 0.9298;
		*hotstatunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotcspurunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotclosureunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		}
	else if (workingpoint=="10pfake"){
		*hotsf = 0.9194;
		*hotstatunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotcspurunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotclosureunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		}
	else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTmistagSF2016! Aborting ..." << std::endl; std::abort();}
}

void HardcodedConditions::GetHOTtaggingSF2017(double pt, int njet, double *hotsf, double *hotstatunc, double *hotcspurunc, double *hotclosureunc, std::string workingpoint)
{
	// VALUES from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSYHOTGroup
	ptMins = {0,150,250,300,350,400,450,500,600};
	njetMins = {4,5,6,7,8,9,10};
	if (workingpoint=="1pfake"){
		*hotsf = 0.9570;
		*hotstatunc = 0.0237;
		hotCSpurUncs = {0.0825,0.0256,0.0276,0.0075,0.0244,0.0265,0.0343,0.0652,0.0095};
		int bin = findBin(pt, ptMins);
		*hotcspurunc = hotCSpurUncs[bin];
		hotClosureUncs = {0.0412,0.0412,0.0865,0.082,0.0375,0.1117,0.0808};
		bin = findBin(njet, njetMins);
		*hotclosureunc = hotClosureUncs[bin];
		}
	else if (workingpoint=="2pfake"){
		*hotsf = 0.9604;
		*hotstatunc = 0.0219;
		hotCSpurUncs = {0.0463,0.026,0.0208,0.0104,0.0247,0.0253,0.0328,0.0486,0.0036};
		int bin = findBin(pt, ptMins);
		*hotcspurunc = hotCSpurUncs[bin];
		hotClosureUncs = {0.0558,0.0558,0.0322,0.0203,0.0548,0.0403,0.0924};
		bin = findBin(njet, njetMins);
		*hotclosureunc = hotClosureUncs[bin];
		}
	else if (workingpoint=="5pfake"){
		*hotsf = 0.9874;
		*hotstatunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotcspurunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotclosureunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		}
	else if (workingpoint=="10pfake"){
		*hotsf = 1.0067;
		*hotstatunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotcspurunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotclosureunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		}
	else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingSF2017! Aborting ..." << std::endl; std::abort();}
}

void HardcodedConditions::GetHOTmistagSF2017(double pt, int njet, double *hotsf, double *hotstatunc, double *hotcspurunc, double *hotclosureunc, std::string workingpoint)
{
	// VALUES from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSYHOTGroup
	ptMins = {0,150,250,300,350,400,450,500,600};
	njetMins = {4,5,6,7,8,9,10};
	if (workingpoint=="1pfake"){
		*hotsf = 0.9921;
		*hotstatunc = 0.0099;
		hotCSpurUncs = {0.0303,0.0367,0.0406,0.0431,0.0499,0.0548,0.0623,0.0594,0.0571};
		int bin = findBin(pt, ptMins);
		*hotcspurunc = hotCSpurUncs[bin];
		hotClosureUncs = {0.0369,0.0377,0.0384,0.0986,0.1768,0.2546,0.257};
		bin = findBin(njet, njetMins);
		*hotclosureunc = hotClosureUncs[bin];
		}
	else if (workingpoint=="2pfake"){
		*hotsf = 1.0140;
		*hotstatunc = 0.0074;
		hotCSpurUncs = {0.0189,0.0236,0.0276,0.0309,0.0355,0.0396,0.0459,0.0448,0.0427};
		int bin = findBin(pt, ptMins);
		*hotcspurunc = hotCSpurUncs[bin];
		hotClosureUncs = {0.0875,0.0309,0.064,0.1179,0.1828,0.2453,0.2146};
		bin = findBin(njet, njetMins);
		*hotclosureunc = hotClosureUncs[bin];
		}
	else if (workingpoint=="5pfake"){
		*hotsf = 1.0119;
		*hotstatunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotcspurunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotclosureunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		}
	else if (workingpoint=="10pfake"){
		*hotsf = 1.0012;
		*hotstatunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotcspurunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotclosureunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		}
	else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTmistagSF2017! Aborting ..." << std::endl; std::abort();}
}

void HardcodedConditions::GetHOTtaggingSF2018(double pt, int njet, double *hotsf, double *hotstatunc, double *hotcspurunc, double *hotclosureunc, std::string workingpoint)
{
	// VALUES from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSYHOTGroup
	ptMins = {0,150,250,300,350,400,450,500,600};
	njetMins = {4,5,6,7,8,9,10};
	if (workingpoint=="1pfake"){
		*hotsf = 0.9359;
		*hotstatunc = 0.0239;
		hotCSpurUncs = {0.0641,0.1004,0.0416,0.0583,0.0695,0.0457,0.0255,0.0553,0.03};
		int bin = findBin(pt, ptMins);
		*hotcspurunc = hotCSpurUncs[bin];
		hotClosureUncs = {0.0693,0.0693,0.1077,0.1884,0.1159,0.2002,0.0862};
		bin = findBin(njet, njetMins);
		*hotclosureunc = hotClosureUncs[bin];
		}
	else if (workingpoint=="2pfake"){
		*hotsf = 0.9483;
		*hotstatunc = 0.0222;
		hotCSpurUncs = {0.0644,0.0445,0.0437,0.0466,0.0694,0.0415,0.0269,0.0544,0.0133};
		int bin = findBin(pt, ptMins);
		*hotcspurunc = hotCSpurUncs[bin];
		hotClosureUncs = {0.0342,0.0342,0.0356,0.0222,0.1118,0.0935,0.1934};
		bin = findBin(njet, njetMins);
		*hotclosureunc = hotClosureUncs[bin];
		}
	else if (workingpoint=="5pfake"){
		*hotsf = 0.9769;
		*hotstatunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotcspurunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotclosureunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		}
	else if (workingpoint=="10pfake"){
		*hotsf = 0.9922;
		*hotstatunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotcspurunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotclosureunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		}
	else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingSF2018! Aborting ..." << std::endl; std::abort();}
}

void HardcodedConditions::GetHOTmistagSF2018(double pt, int njet, double *hotsf, double *hotstatunc, double *hotcspurunc, double *hotclosureunc, std::string workingpoint)
{
	// VALUES from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSYHOTGroup
	ptMins = {0,150,250,300,350,400,450,500,600};
	njetMins = {4,5,6,7,8,9,10};
	if (workingpoint=="1pfake"){
		*hotsf = 0.9036;
		*hotstatunc = 0.0128;
		hotCSpurUncs = {0.0544,0.0523,0.0568,0.0608,0.0667,0.0769,0.0784,0.0732,0.0714};
		int bin = findBin(pt, ptMins);
		*hotcspurunc = hotCSpurUncs[bin];
		hotClosureUncs = {0.0774,0.0179,0.0762,0.1097,0.254,0.3018,0.4417};
		bin = findBin(njet, njetMins);
		*hotclosureunc = hotClosureUncs[bin];
		}
	else if (workingpoint=="2pfake"){
		*hotsf = 0.9532;
		*hotstatunc = 0.0096;
		hotCSpurUncs = {0.032,0.0348,0.0413,0.0439,0.0486,0.0569,0.0586,0.0553,0.0543};
		int bin = findBin(pt, ptMins);
		*hotcspurunc = hotCSpurUncs[bin];
		hotClosureUncs = {0.111,0.0466,0.1185,0.1579,0.3102,0.3314,0.4543};
		bin = findBin(njet, njetMins);
		*hotclosureunc = hotClosureUncs[bin];
		}
	else if (workingpoint=="5pfake"){
		*hotsf = 0.9753;
		*hotstatunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotcspurunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotclosureunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		}
	else if (workingpoint=="10pfake"){
		*hotsf = 0.9703;
		*hotstatunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotcspurunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		*hotclosureunc = 0.0; //NOT PROVIDED in TWIKI, NOV 2019
		}
	else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTmistagSF2018! Aborting ..." << std::endl; std::abort();}
}


/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|            HOT TAGGER EFFICIENCY SECTION            |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

void HardcodedConditions::GetHOTtaggingEff(double pt, double *eff, std::string year, std::string sample, bool isGenMatched, std::string workingpoint, int massIndex)
{
  //The main getter for GetHOTtaggingEff Efficiencies
  *eff = 1.000;
  if(isGenMatched){
  	if      (year=="2016APV") GetHOTtaggingEff2016APV(pt, eff, sample, workingpoint, massIndex);
    else if (year=="2016") GetHOTtaggingEff2016(pt, eff, sample, workingpoint, massIndex);
  	else if (year=="2017") GetHOTtaggingEff2017(pt, eff, sample, workingpoint, massIndex);
  	else if (year=="2018") GetHOTtaggingEff2018(pt, eff, sample, workingpoint, massIndex);
  	}
  else{
  	if      (year=="2016APV") GetHOTmistagEff2016APV(pt, eff, sample, workingpoint, massIndex);
    else if (year=="2016") GetHOTmistagEff2016(pt, eff, sample, workingpoint, massIndex);
  	else if (year=="2017") GetHOTmistagEff2017(pt, eff, sample, workingpoint, massIndex);
  	else if (year=="2018") GetHOTmistagEff2018(pt, eff, sample, workingpoint, massIndex);
  	}
}//end GetHOTtaggingEff

void HardcodedConditions::GetHOTtaggingEff2016APV(double pt, double *eff, std::string sample, std::string workingpoint, int massIndex)
{
	if(sample=="singletop"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.205348668416,0.314370717634,0.409574468085,0.44616639478,0.499124343257,0.472885032538,0.375634517766};
		hotEffs2p = {0.33733459885,0.435088351965,0.522606382979,0.551386623165,0.583187390543,0.58568329718,0.472081218274};
		hotEffs5p = {0.52297470828,0.592679408583,0.65469858156,0.677814029364,0.709281961471,0.720173535792,0.583756345178};
		hotEffs10p= {0.664787002401,0.717634331049,0.754875886525,0.783849918434,0.791593695271,0.798264642082,0.654822335025};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="TTVV"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.305842391304,0.399267399267,0.477281055332,0.493034055728,0.537331701346,0.531803542673,0.418008784773};
		hotEffs2p = {0.464266304348,0.535256410256,0.587761084646,0.609907120743,0.645042839657,0.625603864734,0.513909224012};
		hotEffs5p = {0.650815217391,0.6903998779,0.725357273727,0.731682146543,0.74949000408,0.739935587762,0.635431918009};
		hotEffs10p= {0.768614130435,0.791361416361,0.813484792964,0.818885448916,0.825785393717,0.815217391304,0.714494875549};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="TTTX"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.306924101198,0.39515630792,0.47762962963,0.52101910828,0.53066850448,0.537334263782,0.394946808511};
		hotEffs2p = {0.466932978251,0.531199802298,0.59762962963,0.635668789809,0.644383184011,0.630146545708,0.496010638298};
		hotEffs5p = {0.648024855748,0.684047942667,0.733037037037,0.750318471338,0.762232942798,0.738311235171,0.644946808511};
		hotEffs10p= {0.770972037284,0.785617200049,0.815111111111,0.832696390658,0.840799448656,0.813677599442,0.716755319149};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttbarHT500Njet9"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.407909294843,0.487360654607,0.554943124203,0.585792903693,0.607100158595,0.624351331646,0.610264067903,0.570180155956,0.529164477141,0.417211703959};
		hotEffs2p = {0.568257255093,0.618534948399,0.665471923536,0.685199131064,0.698426253507,0.708109962688,0.696007544797,0.66415703146,0.621650026274,0.499139414802};
		hotEffs5p = {0.736228265173,0.755602546717,0.781532684758,0.791745112238,0.799609613273,0.804949178711,0.792675259352,0.767410594246,0.723068838676,0.618244406196};
		hotEffs10p= {0.834972644315,0.840545199623,0.854462214994,0.860637219406,0.867268512871,0.87095252391,0.857041810751,0.837859639688,0.800840777719,0.702925989673};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttbar"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.252959824309,0.361397414942,0.459087366036,0.504119254456,0.534357717034,0.550922369278,0.535451420581,0.492177755604,0.438544880534,0.298526640397};
		hotEffs2p = {0.39900220362,0.493794233602,0.574189819563,0.608677624155,0.631207830733,0.641467233281,0.624997572486,0.58401339938,0.523498600847,0.380589343841};
		hotEffs5p = {0.588466684642,0.652158801147,0.707418016666,0.730327047958,0.745084736246,0.749944084098,0.732041248325,0.69227753822,0.632991318074,0.48338187425};
		hotEffs10p= {0.721765531851,0.763493052893,0.801389053122,0.815564800087,0.823962905082,0.823869769432,0.80799331948,0.771996721428,0.718160292746,0.574610244989};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttVjets"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.25058416855,0.337887212073,0.411016797393,0.443887827299,0.467403702729,0.474528168015,0.454567022539,0.411171171171,0.368152866242,0.247029393371};
		hotEffs2p = {0.395882818686,0.471008737093,0.528383653881,0.553943087332,0.570150039484,0.56903646942,0.539264531435,0.495135135135,0.452229299363,0.330206378987};
		hotEffs5p = {0.582893999961,0.633783425999,0.669388632212,0.683313536126,0.691936474511,0.690506598553,0.664294187426,0.607207207207,0.579617834395,0.430268918074};
		hotEffs10p= {0.715350597686,0.747603918454,0.769958096057,0.777668749677,0.780994998684,0.78288633461,0.749466192171,0.707747747748,0.675796178344,0.522826766729};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttHToNonbb"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.283254772173,0.370313194136,0.441448382126,0.485894673548,0.5044754744,0.51778614773,0.402069297401};
		hotEffs2p = {0.438354561562,0.511728120835,0.561922187982,0.595279851681,0.607948442535,0.61581920904,0.491578440808};
		hotEffs5p = {0.629559054592,0.672112394491,0.70531587057,0.721250688981,0.727980665951,0.726197949362,0.615736284889};
		hotEffs10p= {0.756560692675,0.781452687694,0.800783256292,0.809640727564,0.808628714644,0.80989746809,0.700433108758};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttHTobb"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.306951814618,0.400615427169,0.481797844214,0.522922404017,0.541345583877,0.54735152488,0.417312661499};
		hotEffs2p = {0.468254179889,0.544082564049,0.607585926378,0.636886440953,0.652934202727,0.639200998752,0.502153316107};
		hotEffs5p = {0.662009013093,0.708830342634,0.748525523693,0.759274258869,0.766597510373,0.752452291778,0.617571059432};
		hotEffs10p= {0.786299032026,0.81291705563,0.833384177344,0.84318807711,0.838470657973,0.820581416087,0.699827734711};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="tttt"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.311329828161,0.390131583914,0.447922957643,0.479768786127,0.503408790045,0.50556497774,0.495245245245,0.459487179487,0.408713227038,0.294583883752};
		hotEffs2p = {0.462714798666,0.528502298755,0.5714845344,0.594583600942,0.609445326979,0.607536569854,0.591257924591,0.557307692308,0.505501908826,0.386393659181};
		hotEffs5p = {0.646111182354,0.686146320104,0.71145025708,0.72575465639,0.731135822081,0.725991096036,0.708375041708,0.674871794872,0.632158095666,0.503302509908};
		hotEffs10p= {0.763352782765,0.788031374799,0.80355831225,0.811025476343,0.811854646545,0.807504769981,0.787287287287,0.762564102564,0.719514933753,0.594671950683};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else{ std::cerr << "The sample " << sample << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}

}

void HardcodedConditions::GetHOTtaggingEff2016APV(double pt, double *eff, std::string sample, std::string workingpoint, int massIndex)
{
	if(sample=="singletop"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.205348668416,0.314370717634,0.409574468085,0.44616639478,0.499124343257,0.472885032538,0.375634517766};
		hotEffs2p = {0.33733459885,0.435088351965,0.522606382979,0.551386623165,0.583187390543,0.58568329718,0.472081218274};
		hotEffs5p = {0.52297470828,0.592679408583,0.65469858156,0.677814029364,0.709281961471,0.720173535792,0.583756345178};
		hotEffs10p= {0.664787002401,0.717634331049,0.754875886525,0.783849918434,0.791593695271,0.798264642082,0.654822335025};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="TTVV"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.305842391304,0.399267399267,0.477281055332,0.493034055728,0.537331701346,0.531803542673,0.418008784773};
		hotEffs2p = {0.464266304348,0.535256410256,0.587761084646,0.609907120743,0.645042839657,0.625603864734,0.513909224012};
		hotEffs5p = {0.650815217391,0.6903998779,0.725357273727,0.731682146543,0.74949000408,0.739935587762,0.635431918009};
		hotEffs10p= {0.768614130435,0.791361416361,0.813484792964,0.818885448916,0.825785393717,0.815217391304,0.714494875549};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="TTTX"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.306924101198,0.39515630792,0.47762962963,0.52101910828,0.53066850448,0.537334263782,0.394946808511};
		hotEffs2p = {0.466932978251,0.531199802298,0.59762962963,0.635668789809,0.644383184011,0.630146545708,0.496010638298};
		hotEffs5p = {0.648024855748,0.684047942667,0.733037037037,0.750318471338,0.762232942798,0.738311235171,0.644946808511};
		hotEffs10p= {0.770972037284,0.785617200049,0.815111111111,0.832696390658,0.840799448656,0.813677599442,0.716755319149};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttbarHT500Njet9"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.407909294843,0.487360654607,0.554943124203,0.585792903693,0.607100158595,0.624351331646,0.610264067903,0.570180155956,0.529164477141,0.417211703959};
		hotEffs2p = {0.568257255093,0.618534948399,0.665471923536,0.685199131064,0.698426253507,0.708109962688,0.696007544797,0.66415703146,0.621650026274,0.499139414802};
		hotEffs5p = {0.736228265173,0.755602546717,0.781532684758,0.791745112238,0.799609613273,0.804949178711,0.792675259352,0.767410594246,0.723068838676,0.618244406196};
		hotEffs10p= {0.834972644315,0.840545199623,0.854462214994,0.860637219406,0.867268512871,0.87095252391,0.857041810751,0.837859639688,0.800840777719,0.702925989673};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttbar"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.252959824309,0.361397414942,0.459087366036,0.504119254456,0.534357717034,0.550922369278,0.535451420581,0.492177755604,0.438544880534,0.298526640397};
		hotEffs2p = {0.39900220362,0.493794233602,0.574189819563,0.608677624155,0.631207830733,0.641467233281,0.624997572486,0.58401339938,0.523498600847,0.380589343841};
		hotEffs5p = {0.588466684642,0.652158801147,0.707418016666,0.730327047958,0.745084736246,0.749944084098,0.732041248325,0.69227753822,0.632991318074,0.48338187425};
		hotEffs10p= {0.721765531851,0.763493052893,0.801389053122,0.815564800087,0.823962905082,0.823869769432,0.80799331948,0.771996721428,0.718160292746,0.574610244989};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttVjets"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.25058416855,0.337887212073,0.411016797393,0.443887827299,0.467403702729,0.474528168015,0.454567022539,0.411171171171,0.368152866242,0.247029393371};
		hotEffs2p = {0.395882818686,0.471008737093,0.528383653881,0.553943087332,0.570150039484,0.56903646942,0.539264531435,0.495135135135,0.452229299363,0.330206378987};
		hotEffs5p = {0.582893999961,0.633783425999,0.669388632212,0.683313536126,0.691936474511,0.690506598553,0.664294187426,0.607207207207,0.579617834395,0.430268918074};
		hotEffs10p= {0.715350597686,0.747603918454,0.769958096057,0.777668749677,0.780994998684,0.78288633461,0.749466192171,0.707747747748,0.675796178344,0.522826766729};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttHToNonbb"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.283254772173,0.370313194136,0.441448382126,0.485894673548,0.5044754744,0.51778614773,0.402069297401};
		hotEffs2p = {0.438354561562,0.511728120835,0.561922187982,0.595279851681,0.607948442535,0.61581920904,0.491578440808};
		hotEffs5p = {0.629559054592,0.672112394491,0.70531587057,0.721250688981,0.727980665951,0.726197949362,0.615736284889};
		hotEffs10p= {0.756560692675,0.781452687694,0.800783256292,0.809640727564,0.808628714644,0.80989746809,0.700433108758};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttHTobb"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.306951814618,0.400615427169,0.481797844214,0.522922404017,0.541345583877,0.54735152488,0.417312661499};
		hotEffs2p = {0.468254179889,0.544082564049,0.607585926378,0.636886440953,0.652934202727,0.639200998752,0.502153316107};
		hotEffs5p = {0.662009013093,0.708830342634,0.748525523693,0.759274258869,0.766597510373,0.752452291778,0.617571059432};
		hotEffs10p= {0.786299032026,0.81291705563,0.833384177344,0.84318807711,0.838470657973,0.820581416087,0.699827734711};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="tttt"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.311329828161,0.390131583914,0.447922957643,0.479768786127,0.503408790045,0.50556497774,0.495245245245,0.459487179487,0.408713227038,0.294583883752};
		hotEffs2p = {0.462714798666,0.528502298755,0.5714845344,0.594583600942,0.609445326979,0.607536569854,0.591257924591,0.557307692308,0.505501908826,0.386393659181};
		hotEffs5p = {0.646111182354,0.686146320104,0.71145025708,0.72575465639,0.731135822081,0.725991096036,0.708375041708,0.674871794872,0.632158095666,0.503302509908};
		hotEffs10p= {0.763352782765,0.788031374799,0.80355831225,0.811025476343,0.811854646545,0.807504769981,0.787287287287,0.762564102564,0.719514933753,0.594671950683};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else{ std::cerr << "The sample " << sample << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}

}

void HardcodedConditions::GetHOTtaggingEff2016(double pt, double *eff, std::string sample, std::string workingpoint, int massIndex)
{
	if(sample=="singletop"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.205348668416,0.314370717634,0.409574468085,0.44616639478,0.499124343257,0.472885032538,0.375634517766};
		hotEffs2p = {0.33733459885,0.435088351965,0.522606382979,0.551386623165,0.583187390543,0.58568329718,0.472081218274};
		hotEffs5p = {0.52297470828,0.592679408583,0.65469858156,0.677814029364,0.709281961471,0.720173535792,0.583756345178};
		hotEffs10p= {0.664787002401,0.717634331049,0.754875886525,0.783849918434,0.791593695271,0.798264642082,0.654822335025};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="TTVV"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.305842391304,0.399267399267,0.477281055332,0.493034055728,0.537331701346,0.531803542673,0.418008784773};
		hotEffs2p = {0.464266304348,0.535256410256,0.587761084646,0.609907120743,0.645042839657,0.625603864734,0.513909224012};
		hotEffs5p = {0.650815217391,0.6903998779,0.725357273727,0.731682146543,0.74949000408,0.739935587762,0.635431918009};
		hotEffs10p= {0.768614130435,0.791361416361,0.813484792964,0.818885448916,0.825785393717,0.815217391304,0.714494875549};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="TTTX"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.306924101198,0.39515630792,0.47762962963,0.52101910828,0.53066850448,0.537334263782,0.394946808511};
		hotEffs2p = {0.466932978251,0.531199802298,0.59762962963,0.635668789809,0.644383184011,0.630146545708,0.496010638298};
		hotEffs5p = {0.648024855748,0.684047942667,0.733037037037,0.750318471338,0.762232942798,0.738311235171,0.644946808511};
		hotEffs10p= {0.770972037284,0.785617200049,0.815111111111,0.832696390658,0.840799448656,0.813677599442,0.716755319149};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttbarHT500Njet9"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.407909294843,0.487360654607,0.554943124203,0.585792903693,0.607100158595,0.624351331646,0.610264067903,0.570180155956,0.529164477141,0.417211703959};
		hotEffs2p = {0.568257255093,0.618534948399,0.665471923536,0.685199131064,0.698426253507,0.708109962688,0.696007544797,0.66415703146,0.621650026274,0.499139414802};
		hotEffs5p = {0.736228265173,0.755602546717,0.781532684758,0.791745112238,0.799609613273,0.804949178711,0.792675259352,0.767410594246,0.723068838676,0.618244406196};
		hotEffs10p= {0.834972644315,0.840545199623,0.854462214994,0.860637219406,0.867268512871,0.87095252391,0.857041810751,0.837859639688,0.800840777719,0.702925989673};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttbar"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.252959824309,0.361397414942,0.459087366036,0.504119254456,0.534357717034,0.550922369278,0.535451420581,0.492177755604,0.438544880534,0.298526640397};
		hotEffs2p = {0.39900220362,0.493794233602,0.574189819563,0.608677624155,0.631207830733,0.641467233281,0.624997572486,0.58401339938,0.523498600847,0.380589343841};
		hotEffs5p = {0.588466684642,0.652158801147,0.707418016666,0.730327047958,0.745084736246,0.749944084098,0.732041248325,0.69227753822,0.632991318074,0.48338187425};
		hotEffs10p= {0.721765531851,0.763493052893,0.801389053122,0.815564800087,0.823962905082,0.823869769432,0.80799331948,0.771996721428,0.718160292746,0.574610244989};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttVjets"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.25058416855,0.337887212073,0.411016797393,0.443887827299,0.467403702729,0.474528168015,0.454567022539,0.411171171171,0.368152866242,0.247029393371};
		hotEffs2p = {0.395882818686,0.471008737093,0.528383653881,0.553943087332,0.570150039484,0.56903646942,0.539264531435,0.495135135135,0.452229299363,0.330206378987};
		hotEffs5p = {0.582893999961,0.633783425999,0.669388632212,0.683313536126,0.691936474511,0.690506598553,0.664294187426,0.607207207207,0.579617834395,0.430268918074};
		hotEffs10p= {0.715350597686,0.747603918454,0.769958096057,0.777668749677,0.780994998684,0.78288633461,0.749466192171,0.707747747748,0.675796178344,0.522826766729};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttHToNonbb"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.283254772173,0.370313194136,0.441448382126,0.485894673548,0.5044754744,0.51778614773,0.402069297401};
		hotEffs2p = {0.438354561562,0.511728120835,0.561922187982,0.595279851681,0.607948442535,0.61581920904,0.491578440808};
		hotEffs5p = {0.629559054592,0.672112394491,0.70531587057,0.721250688981,0.727980665951,0.726197949362,0.615736284889};
		hotEffs10p= {0.756560692675,0.781452687694,0.800783256292,0.809640727564,0.808628714644,0.80989746809,0.700433108758};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttHTobb"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.306951814618,0.400615427169,0.481797844214,0.522922404017,0.541345583877,0.54735152488,0.417312661499};
		hotEffs2p = {0.468254179889,0.544082564049,0.607585926378,0.636886440953,0.652934202727,0.639200998752,0.502153316107};
		hotEffs5p = {0.662009013093,0.708830342634,0.748525523693,0.759274258869,0.766597510373,0.752452291778,0.617571059432};
		hotEffs10p= {0.786299032026,0.81291705563,0.833384177344,0.84318807711,0.838470657973,0.820581416087,0.699827734711};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="tttt"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.311329828161,0.390131583914,0.447922957643,0.479768786127,0.503408790045,0.50556497774,0.495245245245,0.459487179487,0.408713227038,0.294583883752};
		hotEffs2p = {0.462714798666,0.528502298755,0.5714845344,0.594583600942,0.609445326979,0.607536569854,0.591257924591,0.557307692308,0.505501908826,0.386393659181};
		hotEffs5p = {0.646111182354,0.686146320104,0.71145025708,0.72575465639,0.731135822081,0.725991096036,0.708375041708,0.674871794872,0.632158095666,0.503302509908};
		hotEffs10p= {0.763352782765,0.788031374799,0.80355831225,0.811025476343,0.811854646545,0.807504769981,0.787287287287,0.762564102564,0.719514933753,0.594671950683};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else{ std::cerr << "The sample " << sample << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}

}

void HardcodedConditions::GetHOTmistagEff2016APV(double pt, double *eff, std::string sample, std::string workingpoint, int massIndex)
{
	// VALUES from Slide 20 in https://indico.cern.ch/event/828647/contributions/3468595/attachments/1863710/3063888/ResolvedTopTagger_HOT2.pdf
	ptMins = {0,150,250,300,350,400,450,500,600};
	hotEffs = {0.0015,0.005,0.0095,0.0135,0.0155,0.016,0.0145,0.0115,0.005};
	int bin = findBin(pt, ptMins);
	*eff = hotEffs[bin];
}

void HardcodedConditions::GetHOTmistagEff2016(double pt, double *eff, std::string sample, std::string workingpoint, int massIndex)
{
	// VALUES from Slide 20 in https://indico.cern.ch/event/828647/contributions/3468595/attachments/1863710/3063888/ResolvedTopTagger_HOT2.pdf
	ptMins = {0,150,250,300,350,400,450,500,600};
	hotEffs = {0.0015,0.005,0.0095,0.0135,0.0155,0.016,0.0145,0.0115,0.005};
	int bin = findBin(pt, ptMins);
	*eff = hotEffs[bin];
}

void HardcodedConditions::GetHOTtaggingEff2017(double pt, double *eff, std::string sample, std::string workingpoint, int massIndex)
{
	if(sample=="singletop"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.238703480146,0.344134347664,0.434589800443,0.475746268657,0.518656716418,0.507683863886,0.394703656999};
		hotEffs2p = {0.368731908044,0.464867471993,0.537324464154,0.574419568823,0.607794361526,0.594401756312,0.471626733922};
		hotEffs5p = {0.54382958838,0.612588516432,0.670467743638,0.697968490879,0.713515754561,0.708562019759,0.566204287516};
		hotEffs10p= {0.671183976531,0.722995637209,0.76665610812,0.781301824212,0.790215588723,0.783754116356,0.645649432535};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="TTVV"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.349224166392,0.427451708767,0.499334221039,0.520619877049,0.558111860373,0.56627719581,0.438589981447};
		hotEffs2p = {0.499438758666,0.557317979198,0.607723035952,0.62487192623,0.656287187624,0.656124093473,0.525788497217};
		hotEffs5p = {0.664443710796,0.702674591382,0.731025299601,0.737320696721,0.755850852836,0.757655116841,0.640074211503};
		hotEffs10p= {0.770287223506,0.797288261516,0.814824678207,0.815573770492,0.83141610472,0.818291700242,0.714285714286};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="TTTX"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.354968471407,0.433300637567,0.507690054197,0.538025210084,0.567065073041,0.558911384003,0.447599729547};
		hotEffs2p = {0.501304631442,0.561611083865,0.623553537425,0.64243697479,0.666002656042,0.647195486226,0.540229885057};
		hotEffs5p = {0.670580560992,0.705983325159,0.748498608466,0.754201680672,0.762284196547,0.74709591769,0.651115618661};
		hotEffs10p= {0.775277234181,0.798369298676,0.826717445437,0.829411764706,0.831673306773,0.814802522403,0.73968897904};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttbar"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.269151562867,0.371040944242,0.46093357409,0.500559342772,0.529478935766,0.537946286717,0.52057549505,0.472972972973,0.420305878017,0.276479750779};
		hotEffs2p = {0.409420532838,0.495800937276,0.567888124784,0.597745149449,0.618724849018,0.621770021734,0.604450288779,0.557548928239,0.499907868067,0.350689808634};
		hotEffs5p = {0.587507414481,0.64446661573,0.694030504437,0.714070966614,0.728097654509,0.725256428181,0.705548679868,0.662488350419,0.602634973282,0.453604806409};
		hotEffs10p= {0.713205263769,0.750500206068,0.784037803988,0.797203286139,0.805845103535,0.799979663688,0.782152433993,0.742684063374,0.683618942325,0.537939474855};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttbarHT500Njet9"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.420852331885,0.49926498383,0.564610559123,0.591745991624,0.615611535924,0.626310934991,0.615721617224,0.574397250711,0.528376963351,0.407833470282};
		hotEffs2p = {0.581325769815,0.630417434401,0.675020226295,0.692950658632,0.706585025036,0.712875345882,0.700431843785,0.666809858777,0.621465968586,0.492467817036};
		hotEffs5p = {0.747017077753,0.765742585467,0.789658484483,0.799216420697,0.808368590614,0.809209852082,0.796689197647,0.77076733072,0.732251308901,0.610928512736};
		hotEffs10p= {0.842857541777,0.848382142668,0.861767718434,0.866446835523,0.873704537515,0.874150240836,0.861622230567,0.839392149493,0.810261780105,0.699808271706};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttVjets"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.288452231149,0.373458612278,0.449154067675,0.486258527123,0.509460431655,0.520363614616,0.49159748937,0.45743846998,0.393109061313,0.249461786868};
		hotEffs2p = {0.428064401639,0.49869671282,0.558195344372,0.587842991958,0.599064748201,0.607439746427,0.576331241142,0.543815645085,0.476125881715,0.318622174381};
		hotEffs5p = {0.602006904785,0.646202087487,0.685520158387,0.704814419284,0.709748201439,0.713952514802,0.685260174124,0.654021006427,0.591427021161,0.414962325081};
		hotEffs10p= {0.722776110735,0.751445312065,0.777447804176,0.790576030338,0.789928057554,0.796064828659,0.766045758251,0.734127606208,0.675529028757,0.497039827772};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttHToNonbb"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.322708874232,0.407453342783,0.475704187558,0.514392259134,0.539779313898,0.537583014691,0.427537922987};
		hotEffs2p = {0.470150457177,0.537347249962,0.586948188356,0.615564600648,0.633978790091,0.623717045683,0.508518086348};
		hotEffs5p = {0.646441760333,0.68446513326,0.715626293758,0.730337078652,0.742089219012,0.731183336687,0.613302217036};
		hotEffs10p= {0.760219960975,0.78353521036,0.802904150758,0.811450437495,0.817397277919,0.804789696116,0.697549591599};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttHTobb"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.349631239811,0.446789663388,0.523204501703,0.554238073182,0.572679367653,0.573949497904,0.453166226913};
		hotEffs2p = {0.50534896359,0.580202415134,0.635213978972,0.658452987494,0.667936765302,0.659744564688,0.539797713281};
		hotEffs5p = {0.683611520845,0.726871932718,0.756759958537,0.771607225567,0.771139035266,0.762796139222,0.647317502199};
		hotEffs10p= {0.794689853272,0.818254016739,0.835628609507,0.843584993052,0.841183623835,0.830067271132,0.728671943712};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="tttt"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.352514194404,0.430878952682,0.49099243151,0.515815708562,0.532235793946,0.536272793993,0.516997674003,0.493587033122,0.429605416764,0.316731141199};
		hotEffs2p = {0.495189202054,0.558040511935,0.602814198913,0.620469579801,0.627792529651,0.625134082312,0.605832886026,0.580408738548,0.519495680598,0.392408123791};
		hotEffs5p = {0.65894332438,0.700410329892,0.727498845184,0.733369048728,0.739281288724,0.730028792412,0.712918232242,0.68245243129,0.623161335512,0.488636363636};
		hotEffs10p= {0.767653758542,0.793288175335,0.809952741357,0.811702226777,0.812143742255,0.805961723028,0.787618536411,0.76067653277,0.704646275975,0.575435203095};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else{ std::cerr << "The sample " << sample << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
}

void HardcodedConditions::GetHOTmistagEff2017(double pt, double *eff, std::string sample, std::string workingpoint, int massIndex)
{
	// VALUES from Slide 24 in https://indico.cern.ch/event/828647/contributions/3468595/attachments/1863710/3063888/ResolvedTopTagger_HOT2.pdf
	ptMins = {0,150,250,300,350,400,450,500,600};
	hotEffs = {0.001,0.004,0.008,0.0115,0.013,0.013,0.0125,0.0085,0.0035};
	int bin = findBin(pt, ptMins);
	*eff = hotEffs[bin];
}

void HardcodedConditions::GetHOTtaggingEff2018(double pt, double *eff, std::string sample, std::string workingpoint, int massIndex)
{
	if(sample=="singletop"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.212296119533,0.315031032999,0.406236058097,0.45123586894,0.482085987261,0.467056323061,0.377334993773};
		hotEffs2p = {0.339097202454,0.433202236834,0.510682595549,0.548380915884,0.587579617834,0.550743889479,0.452054794521};
		hotEffs5p = {0.507791822372,0.580153219034,0.640608734447,0.665453151945,0.700835987261,0.664984059511,0.564757160648};
		hotEffs10p= {0.639292830797,0.693213707778,0.738611014723,0.760682123012,0.78523089172,0.751062699256,0.658779576588};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="TTVV"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.306757547592,0.388706280631,0.457114122887,0.484619395203,0.519713261649,0.516032171582,0.406852649317};
		hotEffs2p = {0.446968914593,0.510106875037,0.567166323452,0.588373305527,0.611954459203,0.603217158177,0.492229919491};
		hotEffs5p = {0.6178181693,0.655854508237,0.693022364829,0.711222627737,0.720851781573,0.70981233244,0.600074892342};
		hotEffs10p= {0.729319425798,0.756411518098,0.784588860687,0.796532846715,0.798545224541,0.788632707775,0.680022467703};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="TTTX"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.320480258601,0.40133316564,0.479001825928,0.507153534059,0.526281208936,0.531127712558,0.443624161074};
		hotEffs2p = {0.460978988686,0.5288642938,0.592818015825,0.609438394192,0.624835742444,0.624332977588,0.518791946309};
		hotEffs5p = {0.626876010159,0.670230159728,0.720328667072,0.730728165706,0.727003942181,0.731412308787,0.61610738255};
		hotEffs10p= {0.742438235973,0.76895987926,0.798843578819,0.806747811232,0.799605781866,0.797936677339,0.695302013423};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttbar"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.239645560484,0.339776636222,0.431088672755,0.472410045883,0.500610192316,0.508911240515,0.495590310442,0.453230420467,0.390272209327,0.257381258023};
		hotEffs2p = {0.373344786383,0.461458384312,0.53720713172,0.569649038075,0.590771367252,0.595406152579,0.577404750706,0.537323905651,0.469086305128,0.332092426187};
		hotEffs5p = {0.550542735949,0.611085074492,0.664600193036,0.688434087311,0.70022023033,0.701194047409,0.683060912512,0.642953527285,0.574382781177,0.424133504493};
		hotEffs10p= {0.680216158719,0.720677490343,0.759026901279,0.774571359575,0.783206385277,0.78032174578,0.762582314205,0.724564149619,0.668917493142,0.512836970475};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttbarHT500Njet9"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.382883189333,0.463774763516,0.530534334919,0.564121055076,0.585513888459,0.595023744476,0.582740745664,0.55169669755,0.508245382586,0.387973402718};
		hotEffs2p = {0.541805565004,0.59518344389,0.641367700136,0.664696751167,0.679590004026,0.685399438934,0.671130457899,0.642983004604,0.600043975374,0.476293726511};
		hotEffs5p = {0.711693822709,0.735689977202,0.762616536367,0.775344073142,0.786775255731,0.785309594969,0.771549146009,0.747967941795,0.712401055409,0.592223185892};
		hotEffs10p= {0.814625994966,0.824408134231,0.841727352727,0.848803383284,0.856109167105,0.856488017749,0.843523625972,0.820042062184,0.791886543536,0.68545822492};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttVjets"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.248203555141,0.336000706936,0.410729173126,0.448669593355,0.469720348827,0.480485326639,0.454306244307,0.427374526706,0.360325061675,0.238377129656};
		hotEffs2p = {0.381978758931,0.457716400911,0.519888105721,0.549423937014,0.563393956206,0.568047337278,0.544023884222,0.50938532184,0.447395153098,0.309558186543};
		hotEffs5p = {0.556277269744,0.607370787841,0.652259589216,0.670757847441,0.677837687893,0.681130834977,0.655399251088,0.614919842101,0.557248585111,0.41264799307};
		hotEffs10p= {0.682254559552,0.716801017202,0.748003610382,0.762206558256,0.764697723608,0.764837726376,0.739904867928,0.700072504632,0.650848933391,0.498123014727};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttHToNonbb"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.287911917634,0.372938377432,0.444955418438,0.479304265453,0.503111984651,0.511731658956,0.394968553459};
		hotEffs2p = {0.431923831824,0.500676886208,0.555987494003,0.58108570376,0.599653703964,0.601454064772,0.477106918239};
		hotEffs5p = {0.609810268241,0.652403090058,0.68518304081,0.701576191353,0.709906874444,0.712161269002,0.58679245283};
		hotEffs10p= {0.730054061499,0.755174579034,0.776794428545,0.787464147567,0.793766671346,0.791749283983,0.669685534591};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="ttHTobb"){
		ptMins = {0,150,250,300,350,400,500};
		hotEffs1p = {0.318843650941,0.416048224125,0.492033415169,0.52523214609,0.546462416046,0.548041732671,0.441785091};
		hotEffs2p = {0.473585688679,0.549666357685,0.602642895981,0.62854038954,0.641043334253,0.637242584804,0.526427324857};
		hotEffs5p = {0.653722197204,0.69979676318,0.728575900875,0.744988489692,0.750805041862,0.741628885126,0.631388681127};
		hotEffs10p= {0.771326145886,0.796325616475,0.812805852598,0.82023227542,0.823902842948,0.814606434697,0.71540762902};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else if(sample=="tttt"){
		ptMins = {0,150,250,300,350,400,450,500,550,600};
		hotEffs1p = {0.320831918231,0.3982520778,0.461573343186,0.482859420675,0.502006407014,0.500831411254,0.495233142659,0.45651048408,0.412305671119,0.289095332891};
		hotEffs2p = {0.463894684068,0.525030962526,0.572251519936,0.588138896271,0.601315123925,0.594861342059,0.585283411336,0.549055138493,0.501423253777,0.371156823712};
		hotEffs5p = {0.631604483043,0.670621042055,0.698431359377,0.708920187793,0.715528578655,0.704446709221,0.693534408043,0.660367589956,0.616816290782,0.47401017474};
		hotEffs10p= {0.743712904113,0.767403276186,0.785529542172,0.792209230224,0.794267408531,0.784959502226,0.770150806032,0.746311157132,0.695423691701,0.555629285556};
		int bin = findBin(pt, ptMins);
		if(workingpoint=="1pfake"){*eff = hotEffs1p[bin];}
		else if(workingpoint=="2pfake"){*eff = hotEffs2p[bin];}
		else if(workingpoint=="5pfake"){*eff = hotEffs5p[bin];}
		else if(workingpoint=="10pfake"){*eff = hotEffs10p[bin];}
		else{ std::cerr << "Working Point " << workingpoint << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
		}
	else{ std::cerr << "The sample " << sample << " not coded into HardcodedConditions::GetHOTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
}

void HardcodedConditions::GetHOTmistagEff2018(double pt, double *eff, std::string sample, std::string workingpoint, int massIndex)
{
	// VALUES from Slide 28 in https://indico.cern.ch/event/828647/contributions/3468595/attachments/1863710/3063888/ResolvedTopTagger_HOT2.pdf
	ptMins = {0,150,250,300,350,400,450,500,600};
	hotEffs = {0.001,0.003,0.007,0.009,0.0115,0.012,0.0095,0.008,0.0025};
	int bin = findBin(pt, ptMins);
	*eff = hotEffs[bin];
}
      


/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|           T TAGGING SCALE FACTOR SECTION            |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

void HardcodedConditions::GetTtaggingSF(double pt, double *tau32sf, double *tau32sfup, double *tau32sfdn, std::string year)
{
  //The main getter for GetTtaggingSF Scale Factors
  *tau32sf   = 1.000;
  *tau32sfup = 1.000;
  *tau32sfdn = 1.000;
  if      (year=="2016APV") GetTtaggingSF2016APV(pt, tau32sf, tau32sfup, tau32sfdn);
  else if (year=="2016") GetTtaggingSF2016(pt, tau32sf, tau32sfup, tau32sfdn);
  else if (year=="2017") GetTtaggingSF2017(pt, tau32sf, tau32sfup, tau32sfdn);
  else if (year=="2018") GetTtaggingSF2018(pt, tau32sf, tau32sfup, tau32sfdn);
}//end GetTtaggingSF

void HardcodedConditions::GetTtaggingSF2016APV(double pt, double *tau32sf, double *tau32sfup, double *tau32sfdn) {
// copy from 2017, 2016APV in production
  GetTtaggingSF2017( pt, *tau32sf, *tau32sfup, *tau32sfdn )
}

void HardcodedConditions::GetTtaggingSF2016(double pt, double *tau32sf, double *tau32sfup, double *tau32sfdn)
{
// copy from 2017, 2016 in production
  GetTtaggingSF2017( pt, *tau32sf, *tau32sfup, *tau32sfdn )
}

void HardcodedConditions::GetTtaggingSF2017(double pt, double *tau32sf, double *tau32sfup, double *tau32sfdn) {
// Will be replaced by RunIISummer20UL version
  if ( pt < 400.0 ) {
    *tau32sf   = 1.10981;
    *tau32sfUp = 1.14199;
    *tau32sfDn = 1.07812; }
  else {
    *tau32sf   = 1.13264;
    *tau32sfUp = 1.18365;
    *tau32sfDn = 1.08415; }
}

void HardcodedConditions::GetTtaggingSF2018(double pt, double *tau32sf, double *tau32sfup, double *tau32sfdn) {
// will be replaced by RunIISummer20UL version
if ( pt < 400.0 ) {
  *tau32sf   = 1.13869;
  *tau32sfUp = 1.17326;
  *tau32sfDn = 1.10527; }
else {
  *tau32sf   = 1.12333;
  *tau32sfUp = 1.16340;
  *tau32sfDn = 1.08492; }
}


/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|            T TAGGING EFFICIENCY SECTION             |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

void HardcodedConditions::GetTtaggingEff(double pt, double *eff, std::string year, std::string sample, int massIndex)
{
  //The main getter for GetTtaggingEff Efficiencies
  *eff = 1.000;
  if      (year=="2016APV") GetTtaggingEff2016APV(pt, eff, sample, massIndex);
  else if (year=="2016") GetTtaggingEff2016(pt, eff, sample, massIndex);
  else if (year=="2017") GetTtaggingEff2017(pt, eff, sample, massIndex);
  else if (year=="2018") GetTtaggingEff2018(pt, eff, sample, massIndex);
}//end GetTtaggingEff

void HardcodedConditions::GetTtaggingEff2016APV(double pt, double *eff, std::string sample, int massIndex){
	GetTtaggingEff2017(pt, eff, sample, massIndex);
}

void HardcodedConditions::GetTtaggingEff2016(double pt, double *eff, std::string sample, int massIndex){
	GetTtaggingEff2017(pt, eff, sample, massIndex);
}

void HardcodedConditions::GetTtaggingEff2017(double pt, double *eff, std::string sample, int massIndex){
    // Top tagging efficiencies updated
    const int Nbin = 9;
    double ptMins[Nbin] = {400,450,500,550,600,700,800,1000,1200};
    double ttbarEff[Nbin] = {0.553, 0.761, 0.812, 0.815, 0.794, 0.762, 0.726, 0.694, 0.672};
    double STEff[Nbin] = {0.546, 0.760, 0.810, 0.820, 0.805, 0.774, 0.742, 0.734, 0.715};
    double ttttEff[Nbin] = {0.515, 0.657, 0.715, 0.724, 0.702, 0.674, 0.685, 0.650, 0.688};
    double x53x53Eff[12][Nbin] = {//X53X53
     {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//700
     {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//800
     {0.513, 0.685, 0.742, 0.743, 0.738, 0.734, 0.715, 0.710, 0.710},//900R
     {0.491, 0.653, 0.714, 0.729, 0.724, 0.718, 0.711, 0.701, 0.678},//1000R
     {0.461, 0.631, 0.687, 0.703, 0.705, 0.696, 0.698, 0.691, 0.701},//1100R
     {0.454, 0.608, 0.666, 0.680, 0.689, 0.677, 0.678, 0.689, 0.699},//1200R
     {0.440, 0.594, 0.642, 0.656, 0.659, 0.665, 0.659, 0.666, 0.693},//1300R
     {0.423, 0.578, 0.627, 0.646, 0.646, 0.649, 0.645, 0.652, 0.663},//1400R
     {0.404, 0.553, 0.595, 0.618, 0.618, 0.622, 0.633, 0.641, 0.650},//1500R
     {0.413, 0.549, 0.599, 0.599, 0.612, 0.620, 0.623, 0.631, 0.655},//1600R
     {0.418, 0.550, 0.586, 0.596, 0.595, 0.603, 0.610, 0.614, 0.638},//1700R
     {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//1800
     };

    for(int ibin = Nbin-1; ibin >= 0; ibin--){
    	if (pt > ptMins[ibin]){
    		if (sample=="tttt") {*eff=ttttEff[ibin];}
    		else if (sample=="ttbar") {*eff=ttbarEff[ibin];}
    		else if (sample=="singletop") {*eff=STEff[ibin];}
    		else if (sample=="x53x53") {*eff=x53x53Eff[massIndex][ibin];}
    		else{ std::cerr << "The sample " << sample << " not coded into HardcodedConditions::GetTtaggingEff2017! Aborting ..." << std::endl; std::abort();}
    		break;
    		}
    	}
   
}

void HardcodedConditions::GetTtaggingEff2018(double pt, double *eff, std::string sample, int massIndex)
{
    // CURRENTLY USING 2017 SFs WHILE WAITING FOR 2018 RECOMMENDATIONS!!!!!
    // Top tagging efficiencies updated
    const int Nbin = 9;
    double ptMins[Nbin] = {400,450,500,550,600,700,800,1000,1200};
    double ttbarEff[Nbin] = {0.561, 0.770, 0.820, 0.820, 0.800, 0.763, 0.729, 0.697, 0.672};
    double STEff[Nbin] = {0.556, 0.768, 0.813, 0.820, 0.798, 0.774, 0.728, 0.716, 0.657};
    double ttttEff[Nbin] = {0.519, 0.685, 0.723, 0.733, 0.725, 0.689, 0.703, 0.658, 0.619};
    double x53x53Eff[12][Nbin] = {//X53X53
     {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//700
     {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//800
     {0.518, 0.693, 0.742, 0.755, 0.749, 0.741, 0.732, 0.704, 0.713},//900R
     {0.490, 0.667, 0.721, 0.735, 0.732, 0.722, 0.720, 0.712, 0.691},//1000R
     {0.471, 0.641, 0.695, 0.709, 0.710, 0.699, 0.696, 0.698, 0.693},//1100R
     {0.446, 0.626, 0.671, 0.685, 0.692, 0.686, 0.687, 0.674, 0.680},//1200R
     {0.457, 0.606, 0.650, 0.670, 0.671, 0.669, 0.671, 0.671, 0.687},//1300R
     {0.430, 0.594, 0.631, 0.644, 0.659, 0.650, 0.654, 0.659, 0.684},//1400R
     {0.428, 0.572, 0.616, 0.628, 0.639, 0.641, 0.642, 0.634, 0.677},//1500R
     {0.422, 0.549, 0.608, 0.614, 0.620, 0.627, 0.627, 0.634, 0.664},//1600R
     {0.428, 0.562, 0.599, 0.607, 0.601, 0.605, 0.617, 0.619, 0.657},//1700R
     {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//1800
     };

    for(int ibin = Nbin-1; ibin >= 0; ibin--){
    	if (pt > ptMins[ibin]){
    		if (sample=="tttt") {*eff=ttttEff[ibin];}
    		else if (sample=="ttbar") {*eff=ttbarEff[ibin];}
    		else if (sample=="singletop") {*eff=STEff[ibin];}
    		else if (sample=="x53x53") {*eff=x53x53Eff[massIndex][ibin];}
    		else{ std::cerr << "The sample " << sample << " not coded into HardcodedConditions::GetTtaggingEff2018! Aborting ..." << std::endl; std::abort();}
    		break;
    		}
    	}
 
}


/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|           W TAGGING SCALE FACTOR SECTION            |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

void HardcodedConditions::GetWtaggingSF(double pt, double *tau21sf, double *tau21sfup, double *tau21sfdn, double *tau21ptsfup, double *tau21ptsfdn, std::string year)
{
  //The main getter for GetWtaggingSF Scale Factors
  *tau21sf   = 1.000;
  *tau21sfup = 1.000;
  *tau21sfdn = 1.000;
  *tau21ptsfup = 1.000;
  *tau21ptsfdn = 1.000;
  if      (year=="2016APV") GetWtaggingSF2016APV(pt, tau21sf, tau21sfup, tau21sfdn, tau21ptsfup, tau21ptsfdn);
  else if (year=="2016") GetWtaggingSF2017(pt, tau21sf, tau21sfup, tau21sfdn, tau21ptsfup, tau21ptsfdn);
  else if (year=="2017") GetWtaggingSF2017(pt, tau21sf, tau21sfup, tau21sfdn, tau21ptsfup, tau21ptsfdn);
  else if (year=="2018") GetWtaggingSF2018(pt, tau21sf, tau21sfup, tau21sfdn, tau21ptsfup, tau21ptsfdn);
}//end GetWtaggingSF

void HardcodedConditions::GetWtaggingSF2016(double pt, double *tau21sf, double *tau21sfup, double *tau21sfdn, double *tau21ptsfup, double *tau21ptsfdn)
{
	// VALUES from https://twiki.cern.ch/twiki/bin/view/CMS/JetWtagging#2016_scale_factors_and_correctio
	// CORRESPONDING TO tau21<0.55 and 65<mSD<105
	*tau21sf = 1.03;
	*tau21sfup = 1.03+0.14;
	*tau21sfdn = 1.03-0.14;
	*tau21ptsfup = 1.03+0.041*log(pt/200);
	*tau21ptsfdn = 1.03-0.041*log(pt/200);

}

void HardcodedConditions::GetWtaggingSF2017(double pt, double *tau21sf, double *tau21sfup, double *tau21sfdn, double *tau21ptsfup, double *tau21ptsfdn)
{
	// VALUES from https://twiki.cern.ch/twiki/bin/view/CMS/JetWtagging#2017_scale_factors_and_correctio
	// CORRESPONDING TO tau21<0.45 and 65<mSD<105
	*tau21sf = 0.97;
	*tau21sfup = 0.97+0.06;
	*tau21sfdn = 0.97-0.06;
	*tau21ptsfup = 0.97+0.041*log(pt/200);
	*tau21ptsfdn = 0.97-0.041*log(pt/200);
	if(pt > 600){
		*tau21sfup = 1.00;
		*tau21sfdn = 1.00;
		*tau21ptsfup = 0.97+0.041*log(pt/200);
		*tau21ptsfdn = 0.97-0.041*log(pt/200);
		}
	else if(pt > 350){
		*tau21sfup = 0.90+0.13;
		*tau21sfdn = 0.90-0.13;
		*tau21ptsfup = 1.00;
		*tau21ptsfdn = 1.00;
		}
	else if(pt > 300){
		*tau21sfup = 1.00+0.09;
		*tau21sfdn = 1.00-0.09;
		*tau21ptsfup = 1.00;
		*tau21ptsfdn = 1.00;
		}
	else if(pt > 250){
		*tau21sfup = 1.06+0.06;
		*tau21sfdn = 1.06-0.06;
		*tau21ptsfup = 1.00;
		*tau21ptsfdn = 1.00;
		}
	else if(pt > 200){
		*tau21sfup = 1.02+0.07;
		*tau21sfdn = 1.02-0.07;
		*tau21ptsfup = 1.00;
		*tau21ptsfdn = 1.00;
		}
	else{
		*tau21sfup = 1.00;
		*tau21sfdn = 1.00;
		*tau21ptsfup = 1.00;
		*tau21ptsfdn = 1.00;
		}
   
}

void HardcodedConditions::GetWtaggingSF2018(double pt, double *tau21sf, double *tau21sfup, double *tau21sfdn, double *tau21ptsfup, double *tau21ptsfdn)
{
	// VALUES from https://twiki.cern.ch/twiki/bin/view/CMS/JetWtagging#2018_scale_factors_and_correctio
	// CORRESPONDING TO tau21<0.45 and 65<mSD<105
	*tau21sf = 0.98;
	*tau21sfup = 0.98+0.03;
	*tau21sfdn = 0.98-0.03;
	*tau21ptsfup = 0.98+0.041*log(pt/200);
	*tau21ptsfdn = 0.98-0.041*log(pt/200);

}


/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|            W TAGGING EFFICIENCY SECTION             |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

void HardcodedConditions::GetWtaggingEff(double pt, double *eff, int year, std::string sample, int massIndex)
{
  //The main getter for GetTtaggingEff Efficiencies
  *eff = 1.000;
  if      (year==2016) GetWtaggingEff2016(pt, eff, sample, massIndex);
  else if (year==2017) GetWtaggingEff2017(pt, eff, sample, massIndex);
  else if (year==2018) GetWtaggingEff2018(pt, eff, sample, massIndex);
}//end GetTtaggingEff

void HardcodedConditions::GetWtaggingEff2016(double pt, double *eff, std::string sample, int massIndex)
{
	// TO-BE-IMPLEMENTED!!!!!!!
	// CURRENTLY SET TO 2017 EFFICIENCIES !!!!
	GetWtaggingEff2017(pt, eff, sample, massIndex);

}

void HardcodedConditions::GetWtaggingEff2017(double pt, double *eff, std::string sample, int massIndex)
{
    // W TAGGING EFFICIENCIES UPDATED
    // W tagging efficiencies. Assumes each signal mass uses the same pT bins but has unique values.
    const int NbinB = 12;
    const int NbinS = 14;
    double ptMinsB[NbinB] = {175,200,250,300,350,400,450,500,550,600,700,800};
    double ptMinsS[NbinS] = {175,200,250,300,350,400,450,500,550,600,700,800,1000,1200};
    double ttbarEff[NbinB]= {0.721, 0.851, 0.860, 0.837, 0.815, 0.793, 0.773, 0.753, 0.735, 0.716, 0.685, 0.657}; // ttbar
    double STtEff[NbinB]  = {0.726, 0.854, 0.863, 0.837, 0.815, 0.783, 0.767, 0.743, 0.722, 0.698, 0.717, 0.583}; // single top (s and t channel had 0 boosted tops)
    double STtWEff[NbinB] = {0.718, 0.857, 0.873, 0.857, 0.847, 0.834, 0.828, 0.821, 0.814, 0.811, 0.805, 0.777}; // single top (s and t channel had 0 boosted tops)
    double WVEff[NbinB]   = {0.744, 0.865, 0.874, 0.853, 0.836, 0.832, 0.818, 0.809, 0.804, 0.784, 0.787, 0.720}; // WW, WZ, etc. 
    double ttttEff[NbinB] = {0.591, 0.768, 0.785, 0.763, 0.728, 0.705, 0.706, 0.622, 0.679, 0.652, 0.509, 0.549}; // tttt

    double x53x53Eff[12][NbinS] = {//X53X53
       {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//700
       {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//800
       {0.731, 0.859, 0.867, 0.855, 0.843, 0.831, 0.822, 0.812, 0.804, 0.796, 0.775, 0.759, 0.718, 0.680},//900R
       {0.730, 0.866, 0.869, 0.856, 0.844, 0.835, 0.825, 0.823, 0.817, 0.804, 0.790, 0.763, 0.733, 0.721},//1000R
       {0.721, 0.863, 0.867, 0.855, 0.843, 0.838, 0.828, 0.817, 0.816, 0.804, 0.787, 0.770, 0.752, 0.712},//1100R
       {0.756, 0.866, 0.868, 0.853, 0.844, 0.835, 0.829, 0.823, 0.817, 0.809, 0.795, 0.778, 0.758, 0.724},//1200R
       {0.756, 0.865, 0.871, 0.857, 0.843, 0.825, 0.826, 0.826, 0.820, 0.807, 0.796, 0.773, 0.762, 0.737},//1300R
       {0.767, 0.873, 0.871, 0.859, 0.847, 0.838, 0.826, 0.817, 0.817, 0.810, 0.801, 0.778, 0.766, 0.758},//1400R
       {0.753, 0.856, 0.857, 0.833, 0.818, 0.818, 0.803, 0.795, 0.794, 0.793, 0.780, 0.763, 0.740, 0.734},//1500R
       {0.759, 0.876, 0.882, 0.853, 0.845, 0.838, 0.818, 0.821, 0.818, 0.811, 0.800, 0.786, 0.769, 0.758},//1600R
       {0.760, 0.866, 0.871, 0.856, 0.849, 0.836, 0.829, 0.807, 0.813, 0.813, 0.800, 0.792, 0.774, 0.771},//1700R
       {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//1800

      };     
    double TpTpEff[12][NbinS] = {//TpTp
       {0.710, 0.850, 0.855, 0.834, 0.818, 0.805, 0.799, 0.784, 0.787, 0.775, 0.760, 0.737, 0.724, 0.724},//700 
       {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//800
       {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//900
       {0.710, 0.851, 0.857, 0.837, 0.820, 0.807, 0.802, 0.785, 0.773, 0.770, 0.756, 0.746, 0.719, 0.695},//1000
       {0.705, 0.858, 0.853, 0.831, 0.818, 0.808, 0.798, 0.792, 0.782, 0.770, 0.763, 0.751, 0.729, 0.691},//1100
       {0.732, 0.858, 0.858, 0.837, 0.824, 0.808, 0.794, 0.784, 0.784, 0.775, 0.762, 0.752, 0.731, 0.719},//1200
       {0.727, 0.854, 0.856, 0.835, 0.819, 0.804, 0.798, 0.787, 0.778, 0.777, 0.765, 0.745, 0.727, 0.728},//1300
       {0.715, 0.861, 0.855, 0.831, 0.824, 0.806, 0.794, 0.789, 0.779, 0.776, 0.761, 0.746, 0.726, 0.715},//1400
       {0.694, 0.871, 0.866, 0.834, 0.820, 0.811, 0.794, 0.784, 0.789, 0.779, 0.766, 0.746, 0.727, 0.731},//1500
       {0.796, 0.867, 0.851, 0.841, 0.813, 0.804, 0.802, 0.787, 0.779, 0.777, 0.764, 0.751, 0.733, 0.729},//1600
       {0.672, 0.865, 0.856, 0.843, 0.821, 0.793, 0.788, 0.786, 0.775, 0.779, 0.767, 0.750, 0.737, 0.729},//1700
       {0.807, 0.867, 0.858, 0.839, 0.828, 0.812, 0.788, 0.774, 0.773, 0.770, 0.761, 0.757, 0.735, 0.729},//1800

       };
    double BpBpEff[12][NbinS] = {//BpBp
       {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//700
       {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//800
       {0.696, 0.859, 0.859, 0.843, 0.826, 0.818, 0.802, 0.796, 0.785, 0.777, 0.756, 0.733, 0.691, 0.619},//900 
       {0.706, 0.857, 0.865, 0.848, 0.833, 0.816, 0.809, 0.797, 0.784, 0.780, 0.767, 0.750, 0.700, 0.667},//1000
       {0.725, 0.859, 0.862, 0.850, 0.830, 0.817, 0.808, 0.794, 0.794, 0.784, 0.771, 0.750, 0.711, 0.709},//1100
       {0.751, 0.857, 0.865, 0.846, 0.829, 0.819, 0.806, 0.806, 0.792, 0.783, 0.772, 0.753, 0.737, 0.711},//1200
       {0.738, 0.863, 0.857, 0.846, 0.833, 0.816, 0.804, 0.805, 0.794, 0.786, 0.771, 0.761, 0.740, 0.708},//1300
       {0.738, 0.864, 0.860, 0.839, 0.835, 0.817, 0.811, 0.793, 0.796, 0.792, 0.774, 0.756, 0.737, 0.715},//1400
       {0.762, 0.873, 0.850, 0.844, 0.824, 0.821, 0.805, 0.802, 0.791, 0.786, 0.778, 0.765, 0.743, 0.738},//1500
       {0.795, 0.878, 0.857, 0.834, 0.830, 0.807, 0.811, 0.797, 0.788, 0.786, 0.780, 0.764, 0.745, 0.729},//1600
       {0.791, 0.881, 0.863, 0.850, 0.815, 0.813, 0.791, 0.798, 0.794, 0.785, 0.776, 0.768, 0.749, 0.740},//1700
       {0.795, 0.900, 0.862, 0.843, 0.826, 0.795, 0.800, 0.795, 0.788, 0.784, 0.780, 0.763, 0.754, 0.736},//1800

            };

    if(sample=="x53x53" || sample=="TpTp" || sample=="BpBp"){
    	for(int ibin = NbinS-1; ibin >= 0; ibin--){
    		if(pt > ptMinsS[ibin]){
    			if(sample=="x53x53") {*eff=x53x53Eff[massIndex][ibin];}
    			else if(sample=="TpTp") {*eff=TpTpEff[massIndex][ibin];}
    			else if(sample=="BpBp") {*eff=BpBpEff[massIndex][ibin];}
    			else{ std::cerr << "The sample " << sample << " not coded into HardcodedConditions::GetWtaggingEff2017! Aborting ..." << std::endl; std::abort();}
    			break;
    			}
    		}
    	}
    else{
    	for(int ibin = NbinB-1; ibin >= 0; ibin--){
    		if(pt > ptMinsB[ibin]){
    			if(sample=="tttt") {*eff=ttttEff[ibin];}
    			else if(sample=="ttbar") {*eff=ttbarEff[ibin];}
    			else if(sample=="singletopt") {*eff=STtEff[ibin];}
    			else if(sample=="singletoptW") {*eff=STtWEff[ibin];}
    			else if(sample=="WV") {*eff=WVEff[ibin];}
    			else{ std::cerr << "The sample " << sample << " not coded into HardcodedConditions::GetWtaggingEff2017! Aborting ..." << std::endl; std::abort();}
    			break;
    			}
    		}
    	}
   
}

void HardcodedConditions::GetWtaggingEff2018(double pt, double *eff, std::string sample, int massIndex)
{
    // W TAGGING EFFICIENCIES UPDATED
    // W tagging efficiencies. Assumes each signal mass uses the same pT bins but has unique values.
    const int NbinB = 12;
    const int NbinS = 14;
    double ptMinsB[NbinB] = {175,200,250,300,350,400,450,500,550,600,700,800};
    double ptMinsS[NbinS] = {175,200,250,300,350,400,450,500,550,600,700,800,1000,1200};
    double ttbarEff[NbinB]= {0.707, 0.828, 0.829, 0.808, 0.785, 0.761, 0.745, 0.728, 0.709, 0.689, 0.668, 0.636}; // ttbar
    double STtEff[NbinB]  = {0.710, 0.834, 0.835, 0.808, 0.782, 0.755, 0.735, 0.721, 0.682, 0.674, 0.659, 0.500}; // single top (s and t channel had 0 boosted tops)
    double STtWEff[NbinB] = {0.704, 0.839, 0.848, 0.835, 0.821, 0.812, 0.806, 0.802, 0.795, 0.789, 0.782, 0.763}; // single top (s and t channel had 0 boosted tops)
    double WVEff[NbinB]   = {0.730, 0.849, 0.852, 0.826, 0.818, 0.794, 0.774, 0.773, 0.775, 0.749, 0.759, 0.720}; // WW, WZ, etc. 
    double ttttEff[NbinB] = {0.570, 0.719, 0.728, 0.709, 0.682, 0.670, 0.645, 0.607, 0.605, 0.591, 0.594, 0.562}; // tttt

    double x53x53Eff[12][NbinS] = {//X53X53
       {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//700
       {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//800
       {0.668, 0.814, 0.823, 0.815, 0.808, 0.800, 0.792, 0.788, 0.781, 0.768, 0.759, 0.743, 0.698, 0.630},//900R
       {0.682, 0.819, 0.828, 0.818, 0.811, 0.803, 0.795, 0.793, 0.788, 0.775, 0.765, 0.743, 0.720, 0.678},//1000R
       {0.667, 0.824, 0.825, 0.817, 0.812, 0.806, 0.800, 0.794, 0.793, 0.778, 0.770, 0.755, 0.726, 0.728},//1100R
       {0.687, 0.829, 0.828, 0.815, 0.808, 0.809, 0.803, 0.797, 0.792, 0.788, 0.773, 0.755, 0.731, 0.720},//1200R
       {0.689, 0.827, 0.832, 0.819, 0.813, 0.807, 0.802, 0.796, 0.793, 0.787, 0.774, 0.763, 0.744, 0.731},//1300R
       {0.713, 0.833, 0.824, 0.821, 0.812, 0.797, 0.800, 0.792, 0.788, 0.788, 0.781, 0.762, 0.746, 0.749},//1400R
       {0.691, 0.842, 0.839, 0.817, 0.810, 0.803, 0.796, 0.799, 0.787, 0.788, 0.778, 0.769, 0.749, 0.746},//1500R
       {0.724, 0.831, 0.845, 0.814, 0.800, 0.800, 0.786, 0.789, 0.791, 0.788, 0.779, 0.769, 0.746, 0.762},//1600R
       {0.724, 0.856, 0.830, 0.821, 0.817, 0.807, 0.788, 0.791, 0.780, 0.788, 0.782, 0.774, 0.753, 0.758},//1700R
       {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//1800

      };     
    double TpTpEff[12][NbinS] = {//TpTp
       {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//700
       {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//800
       {0.654, 0.802, 0.812, 0.797, 0.783, 0.773, 0.763, 0.759, 0.754, 0.742, 0.736, 0.720, 0.701, 0.685},//900
       {0.679, 0.813, 0.812, 0.799, 0.784, 0.777, 0.769, 0.762, 0.751, 0.745, 0.736, 0.723, 0.705, 0.703},//1000
       {0.687, 0.809, 0.815, 0.797, 0.784, 0.774, 0.765, 0.758, 0.749, 0.743, 0.734, 0.726, 0.704, 0.706},//1100
       {0.654, 0.815, 0.817, 0.798, 0.785, 0.774, 0.768, 0.759, 0.751, 0.748, 0.735, 0.726, 0.713, 0.698},//1200
       {0.668, 0.823, 0.813, 0.799, 0.784, 0.774, 0.766, 0.756, 0.761, 0.751, 0.743, 0.725, 0.715, 0.716},//1300
       {0.696, 0.829, 0.817, 0.794, 0.783, 0.769, 0.764, 0.759, 0.754, 0.745, 0.742, 0.731, 0.706, 0.719},//1400
       {0.758, 0.818, 0.815, 0.797, 0.776, 0.767, 0.757, 0.756, 0.755, 0.756, 0.742, 0.734, 0.712, 0.719},//1500
       {0.706, 0.840, 0.806, 0.802, 0.781, 0.772, 0.756, 0.758, 0.749, 0.751, 0.748, 0.731, 0.713, 0.717},//1600
       {0.742, 0.829, 0.827, 0.796, 0.779, 0.772, 0.756, 0.752, 0.751, 0.750, 0.747, 0.739, 0.723, 0.726},//1700
       {0.689, 0.831, 0.815, 0.801, 0.779, 0.768, 0.745, 0.758, 0.748, 0.743, 0.748, 0.732, 0.731, 0.748},//1800

       };
    double BpBpEff[12][NbinS] = {//BpBp
       {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//700
       {1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000},//800
       {0.678, 0.817, 0.828, 0.806, 0.795, 0.787, 0.776, 0.765, 0.758, 0.750, 0.732, 0.717, 0.655, 0.652},//900
       {0.657, 0.820, 0.821, 0.813, 0.794, 0.786, 0.781, 0.772, 0.769, 0.754, 0.749, 0.726, 0.685, 0.639},//1000
       {0.671, 0.815, 0.822, 0.811, 0.796, 0.786, 0.779, 0.778, 0.765, 0.762, 0.744, 0.732, 0.704, 0.694},//1100
       {0.688, 0.827, 0.822, 0.808, 0.796, 0.789, 0.782, 0.773, 0.769, 0.759, 0.751, 0.733, 0.714, 0.703},//1200
       {0.661, 0.826, 0.822, 0.808, 0.796, 0.779, 0.780, 0.771, 0.770, 0.759, 0.750, 0.737, 0.716, 0.706},//1300
       {0.711, 0.825, 0.826, 0.802, 0.800, 0.778, 0.778, 0.769, 0.771, 0.763, 0.752, 0.737, 0.723, 0.711},//1400
       {0.762, 0.839, 0.828, 0.807, 0.790, 0.786, 0.778, 0.773, 0.772, 0.767, 0.754, 0.743, 0.722, 0.723},//1500
       {0.699, 0.837, 0.830, 0.799, 0.789, 0.784, 0.771, 0.763, 0.772, 0.766, 0.758, 0.744, 0.728, 0.737},//1600
       {0.690, 0.854, 0.839, 0.803, 0.792, 0.770, 0.773, 0.777, 0.764, 0.760, 0.752, 0.744, 0.724, 0.733},//1700
       {0.768, 0.835, 0.829, 0.807, 0.784, 0.780, 0.766, 0.761, 0.756, 0.760, 0.764, 0.747, 0.737, 0.755},//1800

            };

    if(sample=="x53x53" || sample=="TpTp" || sample=="BpBp"){
    	for(int ibin = NbinS-1; ibin >= 0; ibin--){
    		if(pt > ptMinsS[ibin]){
    			if(sample=="x53x53") {*eff=x53x53Eff[massIndex][ibin];}
    			else if(sample=="TpTp") {*eff=TpTpEff[massIndex][ibin];}
    			else if(sample=="BpBp") {*eff=BpBpEff[massIndex][ibin];}
    			else{ std::cerr << "The sample " << sample << " not coded into HardcodedConditions::GetWtaggingEff2018! Aborting ..." << std::endl; std::abort();}
    			break;
    			}
    		}
    	}
    else{
    	for(int ibin = NbinB-1; ibin >= 0; ibin--){
    		if(pt > ptMinsB[ibin]){
    			if(sample=="tttt") {*eff=ttttEff[ibin];}
    			else if(sample=="ttbar") {*eff=ttbarEff[ibin];}
    			else if(sample=="singletopt") {*eff=STtEff[ibin];}
    			else if(sample=="singletoptW") {*eff=STtWEff[ibin];}
    			else if(sample=="WV") {*eff=WVEff[ibin];}
    			else{ std::cerr << "The sample " << sample << " not coded into HardcodedConditions::GetWtaggingEff2018! Aborting ..." << std::endl; std::abort();}
    			break;
    			}
    		}
    	}

}


/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|           EGammaGsf SCALE FACTOR SECTION            |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

double HardcodedConditions::GetEGammaGsfSF(double pt, double eta, int year)
{
  //The main getter for EGammaGsf Scale Factors
  if      (year==2016) return GetEGammaGsfSF2016(pt, eta);
  else if (year==2017) return GetEGammaGsfSF2017(pt, eta);
  else if (year==2018) return GetEGammaGsfSF2018(pt, eta);
  else return 0.;
}//end GetEGammaGsfSF

double HardcodedConditions::GetEGammaGsfSF2016(double pt, double eta)
{
	// Gsf Tracking scale factor: http://fcouderc.web.cern.ch/fcouderc/EGamma/scaleFactors/Moriond17/approval/RECO/passingRECO/egammaEffi.txt_egammaPlots.pdf
	if (pt < 45) {
		if (eta < -2.0) return 0.977;
		else if (eta < -1.566) return 0.982;
		else if (eta < -1.442) return 0.948;
		else if (eta < -1.0) return 0.969;
		else if (eta < -0.5) return 0.977;
		else if (eta < 0.5) return 0.970;
		else if (eta < 1.0) return 0.972;
		else if (eta < 1.442) return 0.970;
		else if (eta < 1.566) return 0.958;
		else return 0.980; }
	else if (pt < 75) {
		if (eta < -2.0) return 0.984;
		else if (eta < -1.566) return 0.982;
		else if (eta < -1.442) return 0.971;
		else if (eta < -1.0) return 0.976;
		else if (eta < 0.0) return 0.980;
		else if (eta < 0.5) return 0.978;
		else if (eta < 1.0) return 0.979;
		else if (eta < 1.442) return 0.977;
		else if (eta < 1.566) return 0.964;
		else if (eta < 2.0) return 0.983;
		else return 0.984; }
	else if (pt < 100) {
		if (eta < -1.566) return 0.997;
		else if (eta < -1.442) return 1.003;
		else if (eta < -1.0) return 0.996;
		else if (eta < 1.0) return 0.992;
		else if (eta < 1.442) return 0.996;
		else if (eta < 1.566) return 1.003;
		else return 0.997; }
	else {
		if (eta < -1.566) return 0.990;
		else if (eta < -1.442) return 1.010;
		else if (eta < -1.0) return 0.985;
		else if (eta < -0.5) return 0.988;
		else if (eta < 0.5) return 0.994;
		else if (eta < 1.0) return 0.988;
		else if (eta < 1.442) return 0.985;
		else if (eta < 1.566) return 1.010;
		else return 0.990; }

}

double HardcodedConditions::GetEGammaGsfSF2017(double pt, double eta)
{
	// Gsf Tracking scale factor: http://fcouderc.web.cern.ch/fcouderc/EGamma/scaleFactors/Moriond17/approval/RECO/passingRECO/egammaEffi.txt_egammaPlots.pdf
	if (pt < 45) {
	    if (eta < -2.0) return 0.977;
	    else if (eta < -1.566) return 0.982;
	    else if (eta < -1.442) return 0.948;
	    else if (eta < -1.0) return 0.969;
	    else if (eta < -0.5) return 0.977;
	    else if (eta < 0.5) return 0.970;
	    else if (eta < 1.0) return 0.972;
	    else if (eta < 1.442) return 0.970;
	    else if (eta < 1.566) return 0.958;
	    else return 0.980; }
	else if (pt < 75) {
	    if (eta < -2.0) return 0.984;
	    else if (eta < -1.566) return 0.982;
	    else if (eta < -1.442) return 0.971;
	    else if (eta < -1.0) return 0.976;
	    else if (eta < 0.0) return 0.980;
	    else if (eta < 0.5) return 0.978;
	    else if (eta < 1.0) return 0.979;
	    else if (eta < 1.442) return 0.977;
	    else if (eta < 1.566) return 0.964;
	    else if (eta < 2.0) return 0.983;
	    else return 0.984; }
	else if (pt < 100) {
	    if (eta < -1.566) return 0.997;
	    else if (eta < -1.442) return 1.003;
	    else if (eta < -1.0) return 0.996;
	    else if (eta < 1.0) return 0.992;
	    else if (eta < 1.442) return 0.996;
	    else if (eta < 1.566) return 1.003;
	    else return 0.997; }
	else {
	    if (eta < -1.566) return 0.990;
	    else if (eta < -1.442) return 1.010;
	    else if (eta < -1.0) return 0.985;
	    else if (eta < -0.5) return 0.988;
	    else if (eta < 0.5) return 0.994;
	    else if (eta < 1.0) return 0.988;
	    else if (eta < 1.442) return 0.985;
	    else if (eta < 1.566) return 1.010;
	    else return 0.990; }

}

double HardcodedConditions::GetEGammaGsfSF2018(double pt, double eta)
{
	// Gsf Tracking scale factor: https://twiki.cern.ch/twiki/pub/CMS/EgammaIDRecipesRun2/egammaEffi.txt_egammaPlots.pdf
	if (pt < 45) {
	    if (eta < -2.0) return 0.989;
	    else if (eta < -1.566) return 0.991;
	    else if (eta < -1.442) return 0.982;
	    else if (eta < -1.0) return 0.988;
	    else if (eta < -0.5) return 0.990;
        else if (eta < 0.0) return 0.986;
	    else if (eta < 0.5) return 0.983;
	    else if (eta < 1.0) return 0.987;
	    else if (eta < 1.442) return 0.984;
	    else if (eta < 1.556) return 0.985;
	    else if (eta < 2.0) return 0.989;
	    else return 0.992; }
	else if (pt < 75) {
	    if (eta < -2.0) return 0.985;
	    else if (eta < -1.556) return 0.991;
	    else if (eta < -1.442) return 0.959;
	    else if (eta < -1.0) return 0.989;
        else if (eta < -0.5) return 0.991;
	    else if (eta < 0.0) return 0.989;
	    else if (eta < 0.5) return 0.987;
	    else if (eta < 1.0) return 0.989;
	    else if (eta < 1.442) return 0.982;
	    else if (eta < 1.566) return 0.973;
	    else if (eta < 2.0) return 0.991;
	    else return 0.986; }
	else if (pt < 100) {
        if (eta < -2.0) return 1.001;
	    else if (eta < -1.566) return 1.006;
	    else if (eta < -1.442) return 1.047;
	    else if (eta < -1.0) return 1.005;
        else if (eta < -0.5) return 1.002;
        else if (eta < 0.0) return 1.006;
        else if (eta < 0.5) return 1.006;
	    else if (eta < 1.0) return 1.002;
	    else if (eta < 1.442) return 1.005;
	    else if (eta < 1.566) return 1.047;
        else if (eta < 2.0) return 1.006;
	    else return 1.001; }
	else {
        if (eta < -2.0) return 1.007;
	    else if (eta < -1.566) return 0.992;
	    else if (eta < -1.442) return 0.984;
	    else if (eta < -1.0) return 1.001;
	    else if (eta < -0.5) return 1.001;
        else if (eta < 0.0) return 0.987;
	    else if (eta < 0.5) return 0.987;
	    else if (eta < 1.0) return 1.001;
	    else if (eta < 1.442) return 1.001;
	    else if (eta < 1.566) return 0.984;
	    else if (eta < 2.0) return 0.992;
	    else return 1.007; }
}

/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|          ELECTRON ID SCALE FACTOR SECTION           |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

double HardcodedConditions::GetElectronIdSF(double pt, double eta, std::string year)
{
  //The main getter for Electron Id Scale Factors
  if      (year=="2016APV") return GetElectronIdSF2016APV(pt, eta);
  else if (year=="2016") return GetElectronIdSF2016(pt, eta);
  else if (year=="2017") return GetElectronIdSF2017(pt, eta);
  else if (year=="2018") return GetElectronIdSF2018(pt, eta);
  else return 0.;
}//end GetElectronIdSF

double HardcodedConditions::GetElectronIdSF2016APV(double pt, double eta){
if ( pt < 20.0 ) {
  if ( eta < -2.0 ) return 1.02326;
  else if ( eta < -1.566 ) return 1.01186;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 1.00253;
  else if ( eta < 0.0 ) return 0.95517;
  else if ( eta < 0.8 ) return 0.97037;
  else if ( eta < 1.444 ) return 1.02059;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 1.00658;
  else return 1.04868; }
else if ( pt < 35.0 ) {
  if ( eta < -2.0 ) return 0.99368;
  else if ( eta < -1.566 ) return 0.97646;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 0.96936;
  else if ( eta < 0.0 ) return 0.96038;
  else if ( eta < 0.8 ) return 0.97741;
  else if ( eta < 1.444 ) return 0.98276;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.96650;
  else return 0.99230; }
else if ( pt < 50.0 ) {
  if ( eta < -2.0 ) return 0.99526;
  else if ( eta < -1.566 ) return 0.98497;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 0.97919;
  else if ( eta < 0.0 ) return 0.96686;
  else if ( eta < 0.8 ) return 0.97619;
  else if ( eta < 1.444 ) return 0.98497;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.98385;
  else return 0.99520; }
else if ( pt < 100.0 ) {
  if ( eta < -2.0 ) return 0.99766;
  else if ( eta < -1.566 ) return 0.98994;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 0.98048;
  else if ( eta < 0.0 ) return 0.96481;
  else if ( eta < 0.8 ) return 0.97748;
  else if ( eta < 1.444 ) return 0.98511;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.99329;
  else return 0.99527; }
else {
  if ( eta < -2.0 ) return 1.01458;
  else if ( eta < -1.566 ) return 1.00219;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 0.99195;
  else if ( eta < 0.0 ) return 0.97506;
  else if ( eta < 0.8 ) return 0.99092;
  else if ( eta < 1.444 ) return 0.99543;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.98701;
  else return 1.00119; }
}

double HardcodedConditions::GetElectronIdSF2016(double pt, double eta){
if ( pt < 20.0 ) {
  if ( eta < -2.0 ) return 1.02086;
  else if ( eta < -1.566 ) return 0.98577;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 0.98113;
  else if ( eta < 0.0 ) return 0.97311;
  else if ( eta < 0.8 ) return 0.97445;
  else if ( eta < 1.444 ) return 0.98367;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.97951;
  else return 0.98520; }
else if ( pt < 35.0 ) {
  if ( eta < -2.0 ) return 0.99359;
  else if ( eta < -1.566 ) return 0.95360;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 0.96252;
  else if ( eta < 0.0 ) return 0.96956;
  else if ( eta < 0.8 ) return 0.98824;
  else if ( eta < 1.444 ) return 0.96493;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.94310;
  else return 0.95614; }
else if ( pt < 50.0 ) {
  if ( eta < -2.0 ) return 1.00000;
  else if ( eta < -1.566 ) return 0.96800;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 0.96928;
  else if ( eta < 0.0 ) return 0.97770;
  else if ( eta < 0.8 ) return 0.99213;
  else if ( eta < 1.444 ) return 0.97717;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.96149;
  else return 0.96820; }
else if ( pt < 100.0 ) {
  if ( eta < -2.0 ) return 0.99764;
  else if ( eta < -1.566 ) return 0.98115;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 0.97182;
  else if ( eta < 0.0 ) return 0.98009;
  else if ( eta < 0.8 ) return 0.99442;
  else if ( eta < 1.444 ) return 0.98188;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.96916;
  else return 0.97778; }
else {
  if ( eta < -2.0 ) return 1.06901;
  else if ( eta < -1.566 ) return 1.00327;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 1.02273;
  else if ( eta < 0.0 ) return 1.00333;
  else if ( eta < 0.8 ) return 1.01577;
  else if ( eta < 1.444 ) return 1.00000;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.98598;
  else return 1.00465; }
}
		
double HardcodedConditions::GetElectronIdSF2017(double pt, double eta){
if ( pt < 20.0 ) {
  if ( eta < -2.0 ) return 0.99501;
  else if ( eta < -1.566 ) return 0.96127;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 0.98659;
  else if ( eta < 0.0 ) return 0.98027;
  else if ( eta < 0.8 ) return 0.97672;
  else if ( eta < 1.444 ) return 0.99009;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.95765;
  else return 1.00628; }
else if ( pt < 35.0 ) {
  if ( eta < -2.0 ) return 0.95848;
  else if ( eta < -1.566 ) return 0.94091;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 0.96508;
  else if ( eta < 0.0 ) return 0.96744;
  else if ( eta < 0.8 ) return 0.97113;
  else if ( eta < 1.444 ) return 0.96938;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.94388;
  else return 0.95935; }
else if ( pt < 50.0 ) {
  if ( eta < -2.0 ) return 0.97256;
  else if ( eta < -1.566 ) return 0.96798;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 0.97456;
  else if ( eta < 0.0 ) return 0.97577;
  else if ( eta < 0.8 ) return 0.97807;
  else if ( eta < 1.444 ) return 0.97669;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.97005;
  else return 0.96803; }
else if ( pt < 100.0 ) {
  if ( eta < -2.0 ) return 0.96851;
  else if ( eta < -1.566 ) return 0.97692;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 0.97271;
  else if ( eta < 0.0 ) return 0.97503;
  else if ( eta < 0.8 ) return 0.97727;
  else if ( eta < 1.444 ) return 0.97697;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.98310;
  else return 0.97056; }
else {
  if ( eta < -2.0 ) return 0.97677;
  else if ( eta < -1.566 ) return 0.97927;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 1.00331;
  else if ( eta < 0.0 ) return 0.98592;
  else if ( eta < 0.8 ) return 0.99134;
  else if ( eta < 1.444 ) return 0.98366;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.97617;
  else return 0.98664; }
}

double HardcodedConditions::GetElectronIdSF2018(double pt, double eta){
if ( pt < 20.0 ) {
  if ( eta < -2.0 ) return 0.98977;
  else if ( eta < -1.566 ) return 0.97193;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 0.98375;
  else if ( eta < 0.0 ) return 0.96348;
  else if ( eta < 0.8 ) return 0.98120;
  else if ( eta < 1.444 ) return 0.98365;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.98242;
  else return 0.96169; }
else if ( pt < 35.0 ) {
  if ( eta < -2.0 ) return 0.95916;
  else if ( eta < -1.566 ) return 0.95000;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 0.95088;
  else if ( eta < 0.0 ) return 0.96503;
  else if ( eta < 0.8 ) return 0.97209;
  else if ( eta < 1.444 ) return 0.95283;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.94413;
  else return 0.94496; }
else if ( pt < 50.0 ) {
  if ( eta < -2.0 ) return 0.97250;
  else if ( eta < -1.566 ) return 0.96706;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 0.96792;
  else if ( eta < 0.0 ) return 0.97247;
  else if ( eta < 0.8 ) return 0.97574;
  else if ( eta < 1.444 ) return 0.96882;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.96489;
  else return 0.96137; }
else if ( pt < 100.0 ) {
  if ( eta < -2.0 ) return 0.97059;
  else if ( eta < -1.566 ) return 0.97484;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 0.96824;
  else if ( eta < 0.0 ) return 0.97388;
  else if ( eta < 0.8 ) return 0.97495;
  else if ( eta < 1.444 ) return 0.96806;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.97170;
  else return 0.96280; }
else {
  if ( eta < -2.0 ) return 0.99777;
  else if ( eta < -1.566 ) return 0.99162;
  else if ( eta < -1.444 ) return 1.00000;
  else if ( eta < -0.8 ) return 0.99126;
  else if ( eta < 0.0 ) return 0.98060;
  else if ( eta < 0.8 ) return 0.98598;
  else if ( eta < 1.444 ) return 0.98794;
  else if ( eta < 1.566 ) return 1.00000;
  else if ( eta < 2.0 ) return 0.98428;
  else return 0.96563; }
}

/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|          ELECTRON ISO SCALE FACTOR SECTION          |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

double HardcodedConditions::GetElectronIsoSF(double pt, double eta, int year)
{
  //The main getter for Electron Iso Scale Factors
  if      (year==2016) return GetElectronIsoSF2016(pt, eta);
  else if (year==2017) return GetElectronIsoSF2017(pt, eta);
  else if (year==2018) return GetElectronIsoSF2018(pt, eta);
  else return 0.;
}//end GetElectronIsoSF

double HardcodedConditions::GetElectronIsoSF2016(double pt, double eta)
{
	// TO-BE-IMPLEMENTED!!!!!!!
	return 1.000;

}

double HardcodedConditions::GetElectronIsoSF2017(double pt, double eta)
{
	// mini isolation scale factors: https://wiwong.web.cern.ch/wiwong/Ele_Eff_Plots/2017passingMiniIsoTight/
	if (pt < 50){
            if (fabs(eta) < 0.8) return 0.997;
            else if (fabs(eta) < 1.442) return 0.999;
            else if (fabs(eta) < 1.566) return 1.009;
            else if (fabs(eta) < 2) return 0.998;
            else return 0.997;}
	else if (pt < 60){
            if (fabs(eta) < 0.8) return 0.998;
            else if (fabs(eta) < 1.442) return 0.999;
            else if (fabs(eta) < 1.566) return 1.022;
            else if (fabs(eta) < 2) return 0.999;
            else return 1.000;}
	else if (pt < 100){
            if (fabs(eta) < 0.8) return 0.998;
            else if (fabs(eta) < 1.442) return 1.001;
            else if (fabs(eta) < 1.566) return 1.024;
            else if (fabs(eta) < 2) return 1.001;
            else return 1.001;}
	else if (pt < 200){
            if (fabs(eta) < 0.8) return 0.999;
            else if (fabs(eta) < 1.442) return 1.001;
            else if (fabs(eta) < 1.566) return 1.021;
            else if (fabs(eta) < 2) return 1.003;
            else return 1.000;}
	else{
            if (fabs(eta) < 0.8) return 1.000;
            else if (fabs(eta) < 1.442) return 1.001;
            else if (fabs(eta) < 1.566) return 1.008;
            else if (fabs(eta) < 2) return 1.000;
            else return 0.999;}
            
}

double HardcodedConditions::GetElectronIsoSF2018(double pt, double eta)
{
	// mini isolation scale factors: https://wiwong.web.cern.ch/wiwong/Ele_Eff_Plots/2018passingMiniIsoTight_updated/egammaEffi.txt_egammaPlots.pdf
	if (pt < 20){
            if (fabs(eta) < -2.0) return 1.039;
            else if (fabs(eta) < -1.566) return 1.026;
            else if (fabs(eta) < -1.442) return 1.115;
            else if (fabs(eta) < -0.8) return 0.998;
            else if (fabs(eta) < 0.0) return 0.996;
            else if (fabs(eta) < 0.8) return 0.996;
            else if (fabs(eta) < 1.442) return 0.998;
            else if (fabs(eta) < 1.566) return 1.115;
            else if (fabs(eta) < 2.0) return 1.026;
            else return 1.039;}
    else if (pt < 40){
            if (fabs(eta) < -2.0) return 1.019;
            else if (fabs(eta) < -1.566) return 1.011;
            else if (fabs(eta) < -1.442) return 1.045;
            else if (fabs(eta) < -0.8) return 1.000;
            else if (fabs(eta) < 0.0) return 0.997;
            else if (fabs(eta) < 0.8) return 0.997;
            else if (fabs(eta) < 1.442) return 1.000;
            else if (fabs(eta) < 1.566) return 1.045;
            else if (fabs(eta) < 2.0) return 1.011;
            else return 1.019;}
    else if (pt < 50){
            if (fabs(eta) < -2.0) return 1.010;
            else if (fabs(eta) < -1.566) return 1.006;
            else if (fabs(eta) < -1.442) return 1.024;
            else if (fabs(eta) < -0.8) return 0.998;
            else if (fabs(eta) < 0.0) return 0.998;
            else if (fabs(eta) < 0.8) return 0.998;
            else if (fabs(eta) < 1.442) return 0.998;
            else if (fabs(eta) < 1.566) return 1.024;
            else if (fabs(eta) < 2.0) return 1.006;
            else return 1.010;}
    else if (pt < 60){
            if (fabs(eta) < -2.0) return 1.008;
            else if (fabs(eta) < -1.566) return 1.003;
            else if (fabs(eta) < -1.442) return 1.035;
            else if (fabs(eta) < -0.8) return 0.999;
            else if (fabs(eta) < 0.0) return 0.999;
            else if (fabs(eta) < 0.8) return 0.999;
            else if (fabs(eta) < 1.442) return 0.999;
            else if (fabs(eta) < 1.566) return 1.035;
            else if (fabs(eta) < 2.0) return 1.003;
            else return 1.008;}
    else if (pt < 100){
            if (fabs(eta) < -2.0) return 1.001;
            else if (fabs(eta) < -1.566) return 1.000;
            else if (fabs(eta) < -1.442) return 1.032;
            else if (fabs(eta) < -0.8) return 1.000;
            else if (fabs(eta) < 0.0) return 1.000;
            else if (fabs(eta) < 0.8) return 1.000;
            else if (fabs(eta) < 1.442) return 1.000;
            else if (fabs(eta) < 1.566) return 1.032;
            else if (fabs(eta) < 2.0) return 1.000;
            else return 1.001;}
    else if (pt < 200){
            if (fabs(eta) < -2.0) return 1.003;
            else if (fabs(eta) < -1.566) return 1.001;
            else if (fabs(eta) < -1.442) return 1.018;
            else if (fabs(eta) < -0.8) return 1.002;
            else if (fabs(eta) < 0.0) return 1.001;
            else if (fabs(eta) < 0.8) return 1.001;
            else if (fabs(eta) < 1.442) return 1.002;
            else if (fabs(eta) < 1.566) return 1.018;
            else if (fabs(eta) < 2.0) return 1.001;
            else return 1.003;}
    else{
            if (fabs(eta) < -2.0) return 1.003;
            else if (fabs(eta) < -1.566) return 1.001;
            else if (fabs(eta) < -1.442) return 0.999;
            else if (fabs(eta) < -0.8) return 0.999;
            else if (fabs(eta) < 0.0) return 1.000;
            else if (fabs(eta) < 0.8) return 1.000;
            else if (fabs(eta) < 1.442) return 0.999;
            else if (fabs(eta) < 1.566) return 0.999;
            else if (fabs(eta) < 2) return 1.001;
            else return 1.003;}

}

/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|        ELECTRON TRIGGER SCALE FACTOR SECTION        |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

double HardcodedConditions::GetElectronTriggerSF(double pt, double eta, int year)
{
  //The main getter for Electron Trigger Scale Factors
  if      (year==2016) return GetElectronTriggerSF2016(pt, eta);
  else if (year==2017) return GetElectronTriggerSF2017(pt, eta);
  else if (year==2018) return GetElectronTriggerSF2018(pt, eta);
  else return 0.;
}//end GetElectronTriggerSF

double HardcodedConditions::GetElectronTriggerSF2016(double pt, double eta)
{
	// TO-BE-IMPLEMENTED!!!!!!!
	return 1.000;

}

double HardcodedConditions::GetElectronTriggerSF2017(double pt, double eta)
{
	// Trigger Scale Factors, SF2017B_Bkg_LepPtEta_EOR.png & SF2017CDEF_Bkg_LepPtEta_EOR.png
	float triggerSFB = 1.0;
	float triggerSFC = 1.0;
	float triggerSFDEF = 1.0;
	float triggerSFBunc = 0.0;
	float triggerSFCunc = 0.0;
	float triggerSFDEFunc = 0.0;

	if (eta > 0.0 && eta <= 0.8){
	    if(pt >30.0 && pt <= 35.0){triggerSFDEF=0.910508894879; triggerSFDEFunc=0.0252630974566; }
	    else if(pt > 35.0 && pt <= 40.0){triggerSFB=1.19235377821; triggerSFBunc=0.00972352951004; triggerSFC=0.961432584122; triggerSFCunc=0.0206050210328;triggerSFDEF=0.953531146324; triggerSFDEFunc=0.00966443825252;}
	    else if(pt > 40.0 && pt <= 45.0){triggerSFB=1.15582596391; triggerSFBunc=0.0101490597149; triggerSFC=0.957629044796; triggerSFCunc=0.0156301400464;triggerSFDEF=0.969037828674; triggerSFDEFunc=0.00902253599794;}
	    else if(pt > 45.0 && pt <= 50.0){triggerSFB=1.14242389742; triggerSFBunc=0.00549159903045; triggerSFC=0.952084569431; triggerSFCunc=0.0156343831136;triggerSFDEF=0.972670135935; triggerSFDEFunc=0.00874302598399;}
	    else if(pt > 50.0 && pt <= 60.0){triggerSFB=1.13798058665; triggerSFBunc=0.00440646655911; triggerSFC=0.972836208578; triggerSFCunc=0.0109869570181;triggerSFDEF=0.97354484058; triggerSFDEFunc=0.00662049424611;}
	    else if(pt > 60.0 && pt >= 100.0){triggerSFB=1.11927898325; triggerSFBunc=0.00270996230892; triggerSFC=0.97878084945; triggerSFCunc=0.00639206054071;triggerSFDEF=0.978742705794; triggerSFDEFunc=0.00393049250046;}
	    else if(pt > 100.0 && pt >= 200.0){triggerSFB=1.08208421955; triggerSFBunc=0.00263577695243;triggerSFC=0.97205414899; triggerSFCunc=0.00666655373504;triggerSFDEF=0.976656543342; triggerSFDEFunc=0.00402836298722;}
	    else if(pt >200.0 && pt >= 300.0){triggerSFB=1.05681427994; triggerSFBunc=0.00197390294288;triggerSFC=0.988668281842; triggerSFCunc=0.0108354482413;triggerSFDEF=0.980285171661; triggerSFDEFunc=0.00719412375919;}
	}
	else if (eta > 0.8 && eta <= 1.442){
	    if(pt >30.0 && pt <= 35.0){triggerSFDEF=0.751761888491; triggerSFDEFunc=0.0392563144486;}
	    else if(pt > 35.0 && pt <= 40.0){triggerSFB=1.15822014397; triggerSFBunc=0.0366899788708; triggerSFC=0.860499625902; triggerSFCunc=0.0338474227491;triggerSFDEF=0.919657299703; triggerSFDEFunc=0.0145884627614;}
	    else if(pt > 40.0 && pt <= 45.0){triggerSFB=1.21616929374; triggerSFBunc=0.0075355308975; triggerSFC=0.954195822579; triggerSFCunc=0.0216774946301;triggerSFDEF=0.9416298044; triggerSFDEFunc=0.0135284523691;}
	    else if(pt > 45.0 && pt <= 50.0){triggerSFB=1.17221728706; triggerSFBunc=0.00598476735072;triggerSFC=0.95883629846; triggerSFCunc=0.0208809133241; triggerSFDEF=0.967038221562; triggerSFDEFunc=0.012176898146;}
	    else if(pt > 50.0 && pt <= 60.0){triggerSFB=1.19498750549; triggerSFBunc=0.0178876420601; triggerSFC=0.954662162504; triggerSFCunc=0.0160626737532;triggerSFDEF=0.975886529118; triggerSFDEFunc=0.00901597488231;}
	    else if(pt > 60.0 && pt >= 100.0){triggerSFB=1.14500756907; triggerSFBunc=0.00769191207143; triggerSFC=0.973404630486; triggerSFCunc=0.00863116494001;triggerSFDEF=0.981893775663; triggerSFDEFunc=0.00516090030148;}
	    else if(pt > 100.0 && pt >= 200.0){triggerSFB=1.08473672928; triggerSFBunc=0.00377953565311;triggerSFC=0.982716650785; triggerSFCunc=0.00847325191329;triggerSFDEF=0.978950786067; triggerSFDEFunc=0.0052715751246;}
	    else if(pt >200.0 && pt >= 300.0){triggerSFB=1.04804436988; triggerSFBunc=0.00275314759171;triggerSFC=0.962029353635; triggerSFCunc=0.0169198961547; triggerSFDEF=0.979265291494; triggerSFDEFunc=0.0093553710705;}
	}
	else if (eta > 1.442 && eta <= 2.0){
	    if(pt >30.0 && pt <= 35.0){triggerSFDEF=0.61359340781; triggerSFDEFunc=0.0720651614296; }
	    else if(pt > 35.0 && pt <= 40.0){triggerSFB=0.979837673172; triggerSFBunc=0.0996061772208;triggerSFC=0.834393494481; triggerSFCunc=0.0545242814001;triggerSFDEF=0.865218488115; triggerSFDEFunc=0.0255203774749;}
	    else if(pt > 40.0 && pt <= 45.0){triggerSFB=1.09592474113; triggerSFBunc=0.0388939927352; triggerSFC=0.934846351249; triggerSFCunc=0.0336441519287; triggerSFDEF=0.92564191376; triggerSFDEFunc=0.0228158658932; }
	    else if(pt > 45.0 && pt <= 50.0){triggerSFB=1.14329944654; triggerSFBunc=0.0390830761738; triggerSFC=0.962071721753; triggerSFCunc=0.0323504865487;triggerSFDEF=0.910259293332; triggerSFDEFunc=0.023206491402; }
	    else if(pt > 50.0 && pt <= 60.0){triggerSFB=1.12458617216; triggerSFBunc=0.0207787584607; triggerSFC=0.939378108547; triggerSFCunc=0.0246293245522; triggerSFDEF=0.951179859384; triggerSFDEFunc=0.0150226105676;}
	    else if(pt > 60.0 && pt >= 100.0){triggerSFB=1.12172511077; triggerSFBunc=0.0220454574283; triggerSFC=0.987642127321; triggerSFCunc=0.0210337676182; triggerSFDEF=0.968589861037; triggerSFDEFunc=0.0173841185589;}
	    else if(pt > 100.0 && pt >= 200.0){triggerSFB=1.09052141074; triggerSFBunc=0.0140524818938; triggerSFC=0.985970344843; triggerSFCunc=0.0167420341634; triggerSFDEF=0.967442726925; triggerSFDEFunc=0.0115473116236;}
	    else if(pt >200.0 && pt >= 300.0){triggerSFB=1.08883369326; triggerSFBunc=0.0193992275579;  triggerSFC=0.893843409369; triggerSFCunc=0.0558133858133; triggerSFDEF=0.958624277634; triggerSFDEFunc=0.0308831433403;}
	}
	else if (eta > 2.0 && eta <= 2.4){
	    if(pt >30.0 && pt <= 35.0){triggerSFDEF=1.34938101512; triggerSFDEFunc=0.897934586653;}
	    else if(pt > 35.0 && pt <= 40.0){triggerSFB=0.852743087035; triggerSFBunc=0.177423039542;triggerSFC=0.682868604737; triggerSFCunc=0.144437037161; triggerSFDEF=0.809342108762; triggerSFDEFunc=0.0630935824021;}
	    else if(pt > 40.0 && pt <= 45.0){triggerSFB=1.1679917664; triggerSFBunc=0.0167310627084; triggerSFC=1.0519398793; triggerSFCunc=0.0583624743679; triggerSFDEF=0.929952818205; triggerSFDEFunc=0.0555593489689;}
	    else if(pt > 45.0 && pt <= 50.0){triggerSFB=1.19320302369; triggerSFBunc=0.0205220242409;triggerSFC=0.983854619602; triggerSFCunc=0.0710158704718;triggerSFDEF=0.996331036879; triggerSFDEFunc=0.0509581507824;}
	    else if(pt > 50.0 && pt <= 60.0){triggerSFB=1.08557256937; triggerSFBunc=0.117006664089; triggerSFC=0.996753585332; triggerSFCunc=0.0684326387008;triggerSFDEF=0.926442474712; triggerSFDEFunc=0.0458155559586;}
	    else if(pt > 60.0 && pt >= 100.0){triggerSFB=1.18448651178; triggerSFBunc=0.0697531410082;triggerSFC=1.02919877827; triggerSFCunc=0.0716198040658; triggerSFDEF=1.03147014466; triggerSFDEFunc=0.058149906159;}
	    else if(pt > 100.0 && pt >= 200.0){triggerSFB=1.06393762562; triggerSFBunc=0.0624111781463;triggerSFC=1.01898572985; triggerSFCunc=0.0416570105471;triggerSFDEF=0.976709670734; triggerSFDEFunc=0.0321444698532;}
	    else if(pt >200.0 && pt >= 300.0){triggerSFB=1.07201980973; triggerSFBunc=0.0236270951373;triggerSFC=1.06465564707; triggerSFCunc=0.0231736721195;triggerSFDEF=0.958190082361; triggerSFDEFunc=0.103132973757; }
	}


	/*if (ht > 500.0 && ht < 750.0){
	  if (pt > 20.0 && pt < 50.0){triggerSFB = 0.907;triggerSFC = 0.931;triggerSFDEF = 0.967;}
	  else if (pt >=50.0 && pt <= 300.0){triggerSFB = 0.997;triggerSFC = 0.999;triggerSFDEF = 0.999;}
	}
	else if (ht >= 750.0 && ht < 3000.0){
	    if (pt > 20.0 && pt < 50.0){triggerSFB = 0.888;triggerSFC = 0.923;triggerSFDEF = 0.963;}
	    else if (pt >=50.0 && pt <= 300.0){triggerSFB = 0.996;triggerSFC = 1.000;triggerSFDEF = 0.999;}
	}*/
	return (4.823*triggerSFB+ 9.664*triggerSFC + 27.07*triggerSFDEF)/41.557;

}

double HardcodedConditions::GetElectronTriggerSF2018(double pt, double eta)
{
  float triggerSFABCD = 1.0;
  float triggerSFABCDunc = 0.0;
  if (eta > 0.0 && eta <= 0.8){
	    if(pt >30.0 && pt <= 35.0){triggerSFABCD=0.913692057441; triggerSFABCDunc=0.0154464370968;}
	    else if(pt > 35.0 && pt <= 40.0){triggerSFABCD=0.971695502732; triggerSFABCDunc=0.00613023548779;}
	    else if(pt > 40.0 && pt <= 45.0){triggerSFABCD=0.973472902604; triggerSFABCDunc=0.00581754877102;}
	    else if(pt > 45.0 && pt <= 50.0){triggerSFABCD=0.975870251002; triggerSFABCDunc=0.00591952371387;}
	    else if(pt > 50.0 && pt <= 60.0){triggerSFABCD=0.972260692149; triggerSFABCDunc=0.00426073436109;}
	    else if(pt > 60.0 && pt >= 100.0){triggerSFABCD=0.978462954775; triggerSFABCDunc=0.00251528166842;}
	    else if(pt > 100.0 && pt >= 200.0){triggerSFABCD=0.982340801275; triggerSFABCDunc=0.00249892269699;}
	    else if(pt >200.0 && pt >= 300.0){triggerSFABCD=0.988277803553; triggerSFABCDunc=0.00408553511306;}
	}
	else if (eta > 0.8 && eta <= 1.442){
	    if(pt >30.0 && pt <= 35.0){triggerSFABCD=0.79130810157; triggerSFABCDunc=0.0257604488845;}
	    else if(pt > 35.0 && pt <= 40.0){triggerSFABCD=0.95794335208; triggerSFABCDunc=0.0200823014694;}
	    else if(pt > 40.0 && pt <= 45.0){triggerSFABCD=0.98584588097; triggerSFABCDunc=0.0077862661467;}
	    else if(pt > 45.0 && pt <= 50.0){triggerSFABCD=0.986921685202; triggerSFABCDunc=0.0127837800598; }
	    else if(pt > 50.0 && pt <= 60.0){triggerSFABCD=1.01257881296; triggerSFABCDunc=0.0160565199922;}
	    else if(pt > 60.0 && pt >= 100.0){triggerSFABCD=0.985749736854; triggerSFABCDunc=0.00366472974788;}
	    else if(pt > 100.0 && pt >= 200.0){triggerSFABCD=0.993225266785; triggerSFABCDunc=0.00626714108618;}
	    else if(pt >200.0 && pt >= 300.0){triggerSFABCD=1.0017169042; triggerSFABCDunc=0.00833637183928;}
	}
	else if (eta > 1.442 && eta <= 2.0){
	    if(pt >30.0 && pt <= 35.0){triggerSFABCD=0.784488053273; triggerSFABCDunc=0.0399543285185;}
	    else if(pt > 35.0 && pt <= 40.0){triggerSFABCD=0.923642602884; triggerSFABCDunc=0.0250525652842;}
	    else if(pt > 40.0 && pt <= 45.0){triggerSFABCD=0.949818783052; triggerSFABCDunc=0.0160756054522;}
	    else if(pt > 45.0 && pt <= 50.0){triggerSFABCD=0.994631635079; triggerSFABCDunc=0.0190307120158;}
	    else if(pt > 50.0 && pt <= 60.0){triggerSFABCD=0.971684494245; triggerSFABCDunc=0.0170379153418;}
	    else if(pt > 60.0 && pt >= 100.0){triggerSFABCD=0.975080347642; triggerSFABCDunc=0.00914101473342;}
	    else if(pt > 100.0 && pt >= 200.0){triggerSFABCD=0.945571234252; triggerSFABCDunc=0.00842362907735;}
	    else if(pt >200.0 && pt >= 300.0){triggerSFABCD=0.917539801421; triggerSFABCDunc=0.0223619496622;}
	}
	else if (eta > 2.0 && eta <= 2.4){
	    if(pt >30.0 && pt <= 35.0){triggerSFABCD=0.771792545521; triggerSFABCDunc=0.0822918878152;}
	    else if(pt > 35.0 && pt <= 40.0){triggerSFABCD=0.877438998912; triggerSFABCDunc=0.035306995628;}
	    else if(pt > 40.0 && pt <= 45.0){triggerSFABCD=1.05068262187; triggerSFABCDunc=0.0582042341467;}
	    else if(pt > 45.0 && pt <= 50.0){triggerSFABCD=0.963750775537; triggerSFABCDunc=0.0331998840585;}
	    else if(pt > 50.0 && pt <= 60.0){triggerSFABCD=0.944876225901; triggerSFABCDunc=0.0237164780054;}
	    else if(pt > 60.0 && pt >= 100.0){ triggerSFABCD=0.954494360964; triggerSFABCDunc=0.0153518496535;}
	    else if(pt > 100.0 && pt >= 200.0){triggerSFABCD=0.940644961626; triggerSFABCDunc=0.0308095483653;}
	    else if(pt >200.0 && pt >= 300.0){triggerSFABCD=0.795593538315; triggerSFABCDunc=0.0538805201514;}
	}
  /*if (ht > 500.0 && ht < 750.0){
    if (pt > 20.0 && pt < 50.0){triggerSFAB = 0.970;triggerSFCD = 0.981;}
    else if (pt >=50.0 && pt <= 300.0){triggerSFAB = 0.999;triggerSFCD = 1.000;}
  }
  else if (ht >= 750.0 && ht < 3000.0){
    if (pt > 20.0 && pt < 50.0){triggerSFAB = 0.959;triggerSFCD = 0.990;}
    else if (pt >=50.0 && pt <= 300.0){triggerSFAB = 0.998;triggerSFCD = 0.999;}
  }*/
  return triggerSFABCD;
}

/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|         HADRON TRIGGER SCALE FACTOR SECTION         |\  | |/|
 | `---' |               (For Electron Channel)                | `---' |
 |       |                                                     |       |
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

double HardcodedConditions::GetIsEHadronTriggerSF(double njets, double ht, int year)
{
  //The main getter for Electron Trigger Scale Factors
  if      (year==2016) return GetIsEHadronTriggerSF2016(njets, ht);
  else if (year==2017) return GetIsEHadronTriggerSF2017(njets, ht);
  else if (year==2018) return GetIsEHadronTriggerSF2018(njets, ht);
  else return 0.;
}//end GetElectronTriggerSF

double HardcodedConditions::GetIsEHadronTriggerSF2016(double njets, double ht)
{
	// TO-BE-IMPLEMENTED!!!!!!!
	return 1.000;

}

double HardcodedConditions::GetIsEHadronTriggerSF2017(double njets, double ht)
{
	// Trigger Scale Factors, SF2017B_Bkg_LepPtEta_EOR.png & SF2017CDEF_Bkg_LepPtEta_EOR.png
	float triggerSFB = 1.0;
	float triggerSFC = 1.0;
	float triggerSFDEF = 1.0;
	float triggerSFBunc = 0.0;
	float triggerSFCunc = 0.0;
	float triggerSFDEFunc = 0.0;
	if (njets == 6){
	    if(ht > 500.0 && ht < 675.0){triggerSFB=0.7131034814; triggerSFBunc=0.039195159067;triggerSFC=1.06442916822; triggerSFCunc=0.0191310183113;triggerSFDEF=0.983282002779; triggerSFDEFunc=0.010945804749;}
	    else if(ht > 675.0 && ht < 850.0){triggerSFB=0.685182848626; triggerSFBunc=0.0550213486042;triggerSFC=0.933509202021; triggerSFCunc=0.0319571469815;triggerSFDEF=0.983282002779; triggerSFDEFunc=0.010945804749;}
	    else if(ht > 850.0 && ht < 1025.0){triggerSFB=0.703597186532; triggerSFBunc=0.0769206267945;triggerSFC=0.874125512276; triggerSFCunc=0.0491865692362; triggerSFDEF=0.951081570599; triggerSFDEFunc=0.0240807046522;}
	    else if(ht > 1025.0 ){triggerSFB=0.579846773226; triggerSFBunc=0.0975503616381;triggerSFC=0.884721020286; triggerSFCunc=0.0576515836494;triggerSFDEF=0.93196872246; triggerSFDEFunc=0.0290876876954;}
	}
	else if (njets == 7){
	    if(ht > 500.0 && ht < 675.0){triggerSFB=0.714231771966; triggerSFBunc=0.0460677631312; triggerSFC=1.04926653189; triggerSFCunc=0.0225797076839;triggerSFDEF=0.975633819631; triggerSFDEFunc=0.0133871357773;}
	    else if(ht > 675.0 && ht < 850.0){triggerSFB=0.74233748692; triggerSFBunc=0.0586519596923;triggerSFC=1.02591177026; triggerSFCunc=0.0304834579974;triggerSFDEF=0.973476673028; triggerSFDEFunc=0.016479213933;}
	    else if(ht > 850.0 && ht < 1025.0){triggerSFB=0.773750907604; triggerSFBunc=0.0760274269242;triggerSFC=0.968495646173; triggerSFCunc=0.043898355643;triggerSFDEF=0.943797434532; triggerSFDEFunc=0.0245958881885;}
	    else if(ht > 1025.0 ){triggerSFB=0.605305982369; triggerSFBunc=0.0708403379341;triggerSFC=0.884721020286; triggerSFCunc=0.0576515836494;triggerSFDEF=0.922137473976; triggerSFDEFunc=0.0268627574623;}
	}
	else if (njets == 8){
	    if(ht > 500.0 && ht < 675.0){triggerSFB=0.868823440272; triggerSFBunc=0.0687865318818;triggerSFC=1.04680148615; triggerSFCunc=0.0398178950336;triggerSFDEF=1.00682464403; triggerSFDEFunc=0.0206251589061;}
	    else if(ht > 675.0 && ht < 850.0){triggerSFB=0.748859059586; triggerSFBunc=0.0719696975787;triggerSFC=0.998869999542; triggerSFCunc=0.042632745896;triggerSFDEF=1.00934080574; triggerSFDEFunc=0.0214975217054;}
	    else if(ht > 850.0 && ht < 1025.0){triggerSFB=0.716921132745; triggerSFBunc=0.102970006749;triggerSFC=1.07367474404; triggerSFCunc=0.0508483052736;triggerSFDEF=0.98914773359; triggerSFDEFunc=0.0294991158576;}
	    else if(ht > 1025.0 ){triggerSFB=0.929517173615; triggerSFBunc=0.0875474821156;triggerSFC=0.778086332171; triggerSFCunc=0.0613585387112;triggerSFDEF=0.97651228934; triggerSFDEFunc=0.0286692152279; }
	}
	else if (njets >= 9){
	    if(ht > 500.0 && ht < 675.0){triggerSFB=0.719549247523; triggerSFBunc=0.145657165847;triggerSFC=1.08558687247; triggerSFCunc=0.0722757558896;triggerSFDEF=1.10004232982; triggerSFDEFunc=0.0330874214131;}
	    else if(ht > 675.0 && ht < 850.0){triggerSFB=0.820454121314; triggerSFBunc=0.115674062744;triggerSFC=1.01446464003; triggerSFCunc=0.0586710035419;triggerSFDEF=0.926273529637; triggerSFDEFunc=0.037549725576;}
	    else if(ht > 850.0 && ht < 1025.0){triggerSFB=0.752958758053; triggerSFBunc=0.125944437336;triggerSFC=0.873179063961; triggerSFCunc=0.0790579410256;triggerSFDEF=0.96662076276; triggerSFDEFunc=0.0350181506312;}
	    else if(ht > 1025.0 ){triggerSFB=0.455386650193; triggerSFBunc=0.0929742397607;triggerSFC=0.824568420102; triggerSFCunc=0.0630836384892; triggerSFDEF=0.979846128538; triggerSFDEFunc=0.0282249900232; }
	}
    float triggerSFUncert = sqrt( pow(4.823*triggerSFBunc/41.557,2) + pow(9.664*triggerSFCunc/41.557,2) + pow(27.07*triggerSFDEFunc/41.557,2) );
    float triggerSF = (4.823*triggerSFB+ 9.664*triggerSFC + 27.07*triggerSFDEF)/41.557;
	return triggerSF;

}

double HardcodedConditions::GetIsEHadronTriggerSF2018(double njets, double ht)
{
  float triggerSFAB = 1.0;
  float triggerSFCD = 1.0;
  float triggerSFABunc = 0.0;
  float triggerSFCDunc = 0.0;
  	if (njets == 6){
	    if(ht > 500.0 && ht < 675.0){triggerSFAB=0.968206089897; triggerSFABunc=0.0106829897362;triggerSFCD=0.977498593923; triggerSFCDunc=0.00724064739296;}
	    else if(ht > 675.0 && ht < 850.0){triggerSFAB=0.914475149322; triggerSFABunc=0.0158449037699;triggerSFCD=0.945512917623; triggerSFCDunc=0.01076706752;}
	    else if(ht > 850.0 && ht < 1025.0){triggerSFAB=0.8484487443; triggerSFABunc=0.0252864251284;triggerSFCD=0.916218285147; triggerSFCDunc=0.0166078728847;}
	    else if(ht > 1025.0 ){triggerSFAB=0.818129424017; triggerSFABunc=0.0295842407636;triggerSFCD=0.939086980165; triggerSFCDunc=0.0195738591402;}
	}
	else if (njets == 7){
	    if(ht > 500.0 && ht < 675.0){triggerSFAB=1.01435872808; triggerSFABunc=0.0136379664791;triggerSFCD=1.00499926004; triggerSFCDunc=0.00952767390448;}
	    else if(ht > 675.0 && ht < 850.0){triggerSFAB=0.91466472422; triggerSFABunc=0.0185173799717; triggerSFCD=0.955491528449; triggerSFCDunc=0.0121519124267;}
	    else if(ht > 850.0 && ht < 1025.0){triggerSFAB=0.968666143174; triggerSFABunc=0.0256979612464;triggerSFCD=0.974986701913; triggerSFCDunc=0.0177384315466;}
	    else if(ht > 1025.0 ){triggerSFAB=0.980046623746; triggerSFABunc=0.0280524922159;triggerSFCD=0.926004632606; triggerSFCDunc=0.0210110167572;}
	}
	else if (njets == 8){
	    if(ht > 500.0 && ht < 675.0){triggerSFAB=0.936955128853; triggerSFABunc=0.0254944260805;triggerSFCD=1.02490624383; triggerSFCDunc=0.015907478007;}
	    else if(ht > 675.0 && ht < 850.0){triggerSFAB=0.955910518012; triggerSFABunc=0.0279235614579;triggerSFCD=0.984275349326; triggerSFCDunc=0.0193980004758;}
	    else if(ht > 850.0 && ht < 1025.0){triggerSFAB=0.972082585397; triggerSFABunc=0.0356773916792;triggerSFCD=1.02092784075; triggerSFCDunc=0.0225048536722;}
	    else if(ht > 1025.0 ){triggerSFAB=0.916637786296; triggerSFABunc=0.036359451647;triggerSFCD=0.96864371249; triggerSFCDunc=0.0236041629142;}

	}
	else if (njets >= 9){
	    if(ht > 500.0 && ht < 675.0){triggerSFAB=1.01413203446; triggerSFABunc=0.0464563918487;triggerSFCD=0.95110722084; triggerSFCDunc=0.0331533447237;}
	    else if(ht > 675.0 && ht < 850.0){triggerSFAB=0.970133496757; triggerSFABunc=0.0368586768362;triggerSFCD=0.996098288346; triggerSFCDunc=0.0253552087868;}
	    else if(ht > 850.0 && ht < 1025.0){triggerSFAB=0.942926718587; triggerSFABunc=0.0445291095114;triggerSFCD=0.991907263195; triggerSFCDunc=0.028699822645;}
	    else if(ht > 1025.0 ){triggerSFAB=0.931569605971; triggerSFABunc=0.0348688784615;triggerSFCD=0.942471490068; triggerSFCDunc=0.0255418143576;}
	}
  float triggerSFUncert = sqrt( pow(21.10*triggerSFABunc/59.97,2) + pow(38.87*triggerSFCDunc/59.97,2) );
  float triggerSF = (21.10*triggerSFAB+ 38.87*triggerSFCD)/59.97;
  return triggerSF;
}


/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|        ELECTRON TRIGGER SCALE FACTOR SECTION        |\  | |/|
 | `---' |           (using cross triggers from VLQ)           | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

double HardcodedConditions::GetElectronTriggerVlqXSF(double pt, double eta, int year)
{
  //The main getter for Electron Trigger Scale Factors
  if      (year==2016) return GetElectronTriggerVlqXSF2016(pt, eta);
  else if (year==2017) return GetElectronTriggerVlqXSF2017(pt, eta);
  else if (year==2018) return GetElectronTriggerVlqXSF2018(pt, eta);
  else return 0.;
}//end GetElectronTriggerVlqXSF

double HardcodedConditions::GetElectronTriggerVlqXSF2016(double pt, double eta)
{
	// TO-BE-IMPLEMENTED!!!!!!!
	return 1.000;

}

double HardcodedConditions::GetElectronTriggerVlqXSF2017(double leppt, double lepeta)
{
	  // Trigger Scale Factors, SF2017B_Bkg_LepPtEta_EOR.png & SF2017CDEF_Bkg_LepPtEta_EOR.png
	  float trigSFB = 1.0;
	  float trigSFCDEF = 1.0;
	  float trigSFBunc = 0.0;
	  float trigSFCDEFunc = 0.0;
	  if (fabs(lepeta) < 0.8){
	    if (leppt < 50) {trigSFB = 0.697; trigSFBunc = 0.075; trigSFCDEF = 1.051; trigSFCDEFunc = 0.018;}
	    else if (leppt < 60) {trigSFB = 0.818; trigSFBunc = 0.069; trigSFCDEF = 1.029; trigSFCDEFunc = 0.016;}
	    else if (leppt < 70) {trigSFB = 0.761; trigSFBunc = 0.081;  trigSFCDEF = 0.988; trigSFCDEFunc = 0.019;}
	    else if (leppt < 100) {trigSFB = 0.693; trigSFBunc = 0.053;  trigSFCDEF = 0.972; trigSFCDEFunc = 0.012;}
	    else if (leppt < 200) {trigSFB = 0.679; trigSFBunc = 0.050;  trigSFCDEF = 0.972; trigSFCDEFunc = 0.009;}
	    else {trigSFB = 0.953; trigSFBunc = 0.066;  trigSFCDEF = 0.964; trigSFCDEFunc = 0.019;}
	  }else if (fabs(lepeta) < 1.442){
            if (leppt < 50) {trigSFB = 0.793; trigSFBunc = 0.142;  trigSFCDEF = 1.020; trigSFCDEFunc = 0.029;}
            else if (leppt < 60) {trigSFB = 0.853; trigSFBunc = 0.112;  trigSFCDEF = 1.063; trigSFCDEFunc = 0.024;}
            else if (leppt < 70) {trigSFB = 0.721; trigSFBunc = 0.116;  trigSFCDEF = 0.962; trigSFCDEFunc = 0.031;}
            else if (leppt < 100) {trigSFB = 0.731; trigSFBunc = 0.075;  trigSFCDEF = 0.923; trigSFCDEFunc = 0.020;}
            else if (leppt < 200) {trigSFB = 0.815; trigSFBunc = 0.060;  trigSFCDEF = 0.957; trigSFCDEFunc = 0.015;}
            else {trigSFB = 0.801; trigSFBunc = 0.143;  trigSFCDEF = 1.015; trigSFCDEFunc = 0.015;}
	  }else if (fabs(lepeta) < 1.566) {trigSFB = 1.0; trigSFCDEF = 1.0;}
	  else if (fabs(lepeta) < 2.0){
            if (leppt < 50) {trigSFB = 1.024; trigSFBunc = 0.157;  trigSFCDEF = 1.060; trigSFCDEFunc = 0.059;}
            else if (leppt < 60) {trigSFB = 0.695; trigSFBunc = 0.228;  trigSFCDEF = 1.109; trigSFCDEFunc = 0.045;}
            else if (leppt < 70) {trigSFB = 0.675; trigSFBunc = 0.202;  trigSFCDEF = 1.061; trigSFCDEFunc = 0.054;}
            else if (leppt < 100) {trigSFB = 0.752; trigSFBunc = 0.124;  trigSFCDEF = 0.996; trigSFCDEFunc = 0.035;}
            else if (leppt < 200) {trigSFB = 0.672; trigSFBunc = 0.174;  trigSFCDEF = 0.960; trigSFCDEFunc = 0.039;}
            else {trigSFB = 1.108; trigSFBunc = 0.022;  trigSFCDEF = 0.924; trigSFCDEFunc = 0.099;}
	  }else {
            if (leppt < 50) {trigSFB = 1.026; trigSFBunc = 0.297;  trigSFCDEF = 1.007; trigSFCDEFunc = 0.087;}
            else if (leppt < 60) {trigSFB = 1.216; trigSFBunc = 0.024;  trigSFCDEF = 0.903; trigSFCDEFunc = 0.092;}
            else if (leppt < 70) {trigSFB = 1.000; trigSFBunc = 0.050;  trigSFCDEF = 1.037; trigSFCDEFunc = 0.077;}
            else if (leppt < 100) {trigSFB = 0.977; trigSFBunc = 0.151;  trigSFCDEF = 1.027; trigSFCDEFunc = 0.045;}
            else if (leppt < 200) {trigSFB = 0.366; trigSFBunc = 0.299;  trigSFCDEF = 0.910; trigSFCDEFunc = 0.071;}
            else {trigSFB = 1.000; trigSFBunc = 0.050;  trigSFCDEF = 0.440; trigSFCDEFunc = 0.242;}
	  }
	  float triggerSF = (4.823*trigSFB + 36.734*trigSFCDEF)/41.557;
	  float triggerSFUncert = sqrt( pow(4.823*trigSFBunc/41.557,2) + pow(36.734*trigSFCDEFunc/41.557,2) );

	return triggerSF;

}

double HardcodedConditions::GetElectronTriggerVlqXSF2018(double leppt, double lepeta)
{
	  //Trigger SF calculated by JHogan, HT > 430, ttbar tag/probe, Id+iso applied
	float triggSF = 1.0;
	float triggSFUncert = 1.0;
	  if (fabs(lepeta) < 0.8){
	if (leppt < 30) {triggSF = 0.924; triggSFUncert = 0.025;}
	else if (leppt < 40) {triggSF = 1.030; triggSFUncert = 0.018;}
		else if (leppt < 50) {triggSF = 1.033; triggSFUncert = 0.015;}
		else if (leppt < 60) {triggSF = 1.029; triggSFUncert = 0.014;}
		else if (leppt < 70) {triggSF = 1.001; triggSFUncert = 0.014;}
		else if (leppt < 100) {triggSF = 1.001; triggSFUncert = 0.010;}
		else if (leppt < 200) {triggSF = 0.980; triggSFUncert = 0.010;}
		else {triggSF = 0.983; triggSFUncert = 0.013;}
  }
	  else if (fabs(lepeta) < 1.442){
	if (leppt < 30) {triggSF = 0.929; triggSFUncert = 0.037;}
		else if (leppt < 40) {triggSF = 1.057; triggSFUncert = 0.025;}
		else if (leppt < 50) {triggSF = 1.076; triggSFUncert = 0.023;}
		else if (leppt < 60) {triggSF = 1.035; triggSFUncert = 0.020;}
		else if (leppt < 70) {triggSF = 1.023; triggSFUncert = 0.021;}
		else if (leppt < 100) {triggSF = 1.010; triggSFUncert = 0.013;}
		else if (leppt < 200) {triggSF = 1.002; triggSFUncert = 0.010;}
		else {triggSF = 0.982; triggSFUncert = 0.021;}
	  }
	  else if (fabs(lepeta) < 1.556) {
	if (leppt < 30) {triggSF = 0.673; triggSFUncert = 0.171;}
		else if (leppt < 40) {triggSF = 1.197; triggSFUncert = 0.116;}
		else if (leppt < 50) {triggSF = 1.143; triggSFUncert = 0.087;}
		else if (leppt < 60) {triggSF = 0.928; triggSFUncert = 0.092;}
		else if (leppt < 70) {triggSF = 1.082; triggSFUncert = 0.076;}
		else if (leppt < 100) {triggSF = 0.951; triggSFUncert = 0.054;}
		else if (leppt < 200) {triggSF = 1.016; triggSFUncert = 0.029;}
		else {triggSF = 0.978; triggSFUncert = 0.062;}
  }
	  else if (fabs(lepeta) < 2.0){ 
	if (leppt < 30) {triggSF = 0.827; triggSFUncert = 0.073;}
		else if (leppt < 40) {triggSF = 0.976; triggSFUncert = 0.052;}
		else if (leppt < 50) {triggSF = 1.114; triggSFUncert = 0.042;}
		else if (leppt < 60) {triggSF = 1.099; triggSFUncert = 0.041;}
		else if (leppt < 70) {triggSF = 1.030; triggSFUncert = 0.040;}
		else if (leppt < 100) {triggSF = 0.990; triggSFUncert = 0.032;}
		else if (leppt < 200) {triggSF = 1.028; triggSFUncert = 0.022;}
		else {triggSF = 0.948; triggSFUncert = 0.058;}
	  }	  
	  else{ 
		if (leppt < 30) {triggSF = 1.047; triggSFUncert = 0.093;}
		else if (leppt < 40) {triggSF = 1.150; triggSFUncert = 0.080;}
		else if (leppt < 50) {triggSF = 1.094; triggSFUncert = 0.061;}
		else if (leppt < 60) {triggSF = 1.063; triggSFUncert = 0.060;}
		else if (leppt < 70) {triggSF = 1.073; triggSFUncert = 0.058;}
		else if (leppt < 100) {triggSF = 1.005; triggSFUncert = 0.039;}
		else if (leppt < 200) {triggSF = 0.978; triggSFUncert = 0.041;}
		else {triggSF = 1.103; triggSFUncert = 0.035;}
	 }

  return triggSF;
}


/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|      ELECTRON X-TRIGGER SCALE FACTOR SECTION        |\  | |/|
 | `---' |                    (from Nikos)                     | `---' |
 |       |                                                     |       |
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

double HardcodedConditions::GetElectronTriggerXSF(double pt, double eta, int year)
{
  //The main getter for Electron Trigger Scale Factors
  if      (year==2016) return GetElectronTriggerXSF2016(pt, eta);
  else if (year==2017) return GetElectronTriggerXSF2017(pt, eta);
  else if (year==2018) return GetElectronTriggerXSF2018(pt, eta);
  else return 0. ;
}//end GetElectronTriggerXSF

double HardcodedConditions::GetElectronTriggerXSF2016(double pt, double eta)
{
	// TO-BE-IMPLEMENTED!!!!!!!
	return 1.000 ;

}

double HardcodedConditions::GetElectronTriggerXSF2017(double leppt, double lepeta)
{
	  // Trigger Scale Factors, SF2017B_Bkg_LepPtEta_EOR.png & SF2017CDEF_Bkg_LepPtEta_EOR.png
	  float trigSFB = 1.0;
	  float trigSFCDEF = 1.0;
	  float trigSFBunc = 0.0;
	  float trigSFCDEFunc = 0.0;
	  float triggerSF;
	  float triggerSFUncert;
	  if (fabs(lepeta) < 0.8){
        if (leppt >=20.0 &&  leppt< 25.0 ) {
            trigSFB=0.0; trigSFBunc=-1;
            trigSFCDEF=1.08552840991; trigSFCDEFunc=0.00887273637568;
            }
        else if (leppt >=25.0 &&  leppt< 30.0 ) {
            trigSFB=0.0; trigSFBunc=-1;
            trigSFCDEF=1.07082446672; trigSFCDEFunc=0.00381687027718;
            }
        else if (leppt >=30.0 &&  leppt< 35.0 ) {
            trigSFB=0.0156991498666; trigSFBunc=0.00899912206167;
            trigSFCDEF=1.04732309472; trigSFCDEFunc=0.00912405345717;
            }
        else if (leppt >=35.0 &&  leppt< 40.0 ) {
            trigSFB=0.853055863294; trigSFBunc=0.0280478272024;
            trigSFCDEF=1.04001604765; trigSFCDEFunc=0.00398221313048;
            }
        else if (leppt >=40.0 &&  leppt< 45.0 ) {
            trigSFB=1.05266545066; trigSFBunc=0.0125523044299;
            trigSFCDEF=1.0474195663; trigSFCDEFunc=0.00945736440857;
            }
        else if (leppt >=45.0 &&  leppt< 50.0 ) {
            trigSFB=1.0446917778; trigSFBunc=0.00443218948007;
            trigSFCDEF=1.04057499109; trigSFCDEFunc=0.00254763009755;
            }
        else if (leppt >=50.0 &&  leppt< 60.0 ) {
            trigSFB=1.04499711786; trigSFBunc=0.00370247485863;
            trigSFCDEF=1.01884743033; trigSFCDEFunc=0.00313913252463;
            }
        else if (leppt >=60.0 &&  leppt< 70.0 ) {
            trigSFB=1.03288832639; trigSFBunc=0.00550597705563;
            trigSFCDEF=1.01753508381; trigSFCDEFunc=0.00308512823087;
            }
        else if (leppt >=70.0 &&  leppt< 100.0 ) {
            trigSFB=1.02883916576; trigSFBunc=0.00213991694503;
            trigSFCDEF=1.01383390053; trigSFCDEFunc=0.00173857940949;
            }
        else if (leppt >=100.0 &&  leppt< 200.0 ) {
            trigSFB=1.01507401909; trigSFBunc=0.00226096652583;
            trigSFCDEF=1.00616018347; trigSFCDEFunc=0.0013878685792;
            }
        else{
            trigSFB=1.0102603482; trigSFBunc=0.000747218314445;
            trigSFCDEF=1.00479357143; trigSFCDEFunc=0.00187741895;
            }
	  }
	  else if (fabs(lepeta) < 1.442){
        if (leppt >=20.0 &&  leppt< 25.0 ) {
            trigSFB=0.760119797875; trigSFBunc=0.310337896775;
            trigSFCDEF=1.13746928549; trigSFCDEFunc=0.00553544345872;
            }
        else if (leppt >=25.0 &&  leppt< 30.0 ) {
            trigSFB=0.0; trigSFBunc=-1;
            trigSFCDEF=1.12676244222; trigSFCDEFunc=0.015444776283;
            }
        else if (leppt >=30.0 &&  leppt< 35.0 ) {
            trigSFB=0.0; trigSFBunc=-1;
            trigSFCDEF=1.07272481048; trigSFCDEFunc=0.00661657111514;
            }
        else if (leppt >=35.0 &&  leppt< 40.0 ) {
            trigSFB=0.790278711561; trigSFBunc=0.0411165609489;
            trigSFCDEF=1.05882334456; trigSFCDEFunc=0.00511065558603;
            }
        else if (leppt >=40.0 &&  leppt< 45.0 ) {
            trigSFB=1.06945574436; trigSFBunc=0.00290318383937;
            trigSFCDEF=1.05540570753; trigSFCDEFunc=0.00443484967063;
            }
        else if (leppt >=45.0 &&  leppt< 50.0 ) {
            trigSFB=1.06334514688; trigSFBunc=0.0023530829504;
            trigSFCDEF=1.05453532794; trigSFCDEFunc=0.00362527515816;
            }
        else if (leppt >=50.0 &&  leppt< 60.0 ) {
            trigSFB=1.06349511204; trigSFBunc=0.0049802813825;
            trigSFCDEF=1.03133914935; trigSFCDEFunc=0.00474770949689;
            }
        else if (leppt >=60.0 &&  leppt< 70.0 ) {
            trigSFB=1.06692865386; trigSFBunc=0.0181708799599;
            trigSFCDEF=1.05458294543; trigSFCDEFunc=0.0157703426718;
            }
        else if (leppt >=70.0 &&  leppt< 100.0 ) {
            trigSFB=1.04105444789; trigSFBunc=0.00123767565196;
            trigSFCDEF=1.0184760525; trigSFCDEFunc=0.00273402347531;
            }
        else if (leppt >=100.0 &&  leppt< 200.0 ) {
            trigSFB=1.02152635173; trigSFBunc=0.00313051739258;
            trigSFCDEF=1.01085198147; trigSFCDEFunc=0.00205741257245;
            }
        else{
            trigSFB=1.01376673793; trigSFBunc=0.00130427393468;
            trigSFCDEF=1.00697812138; trigSFCDEFunc=0.00305088102889;
            }
	  }
	  else if (fabs(lepeta) < 1.566) {trigSFB = 1.0; trigSFCDEF = 1.0;}
	  else if (fabs(lepeta) < 2.0){
         if (leppt >=20.0 &&  leppt< 25.0 ) {
            trigSFB=0.0; trigSFBunc=-1;
            trigSFCDEF=1.19909358081; trigSFCDEFunc=0.0353376191772;
            }
         else if (leppt >=25.0 &&  leppt< 30.0 ) {
            trigSFB=0.0; trigSFBunc=-1;
            trigSFCDEF=1.09481419439; trigSFCDEFunc=0.0304477030337;
            }
         else if (leppt >=30.0 &&  leppt< 35.0 ) {
            trigSFB=0.0514234061329; trigSFBunc=0.0356155490968;
            trigSFCDEF=1.1072593802; trigSFCDEFunc=0.0368965723703;
            }
         else if (leppt >=35.0 &&  leppt< 40.0 ) {
            trigSFB=0.664907397575; trigSFBunc=0.0860296378044;
            trigSFCDEF=1.05256406493; trigSFCDEFunc=0.0138144332818;
            }
         else if (leppt >=40.0 &&  leppt< 45.0 ) {
            trigSFB=1.05025561699; trigSFBunc=0.0215543893492;
            trigSFCDEF=1.05848583952; trigSFCDEFunc=0.00658000222521;
            }
         else if (leppt >=45.0 &&  leppt< 50.0 ) {
            trigSFB=1.10222475298; trigSFBunc=0.0124495163302;
            trigSFCDEF=1.09740101227; trigSFCDEFunc=0.0128537992993;
            }
         else if (leppt >=50.0 &&  leppt< 60.0 ) {
            trigSFB=1.07732214728; trigSFBunc=0.0055355236644;
            trigSFCDEF=1.04684439896; trigSFCDEFunc=0.008256931132;
            }
         else if (leppt >=60.0 &&  leppt< 70.0 ) {
            trigSFB=1.056582036; trigSFBunc=0.00344137348184;
            trigSFCDEF=1.00469631102; trigSFCDEFunc=0.00939584806876;
            }
         else if (leppt >=70.0 &&  leppt< 100.0 ) {
            trigSFB=1.06256856682; trigSFBunc=0.00470393138296;
            trigSFCDEF=1.0342999195; trigSFCDEFunc=0.00662143745353;
            }
         else if (leppt >=100.0 &&  leppt< 200.0 ) {
            trigSFB=1.05522146539; trigSFBunc=0.0161323213105;
            trigSFCDEF=1.01830159313; trigSFCDEFunc=0.0165211825975;
            }
         else {
            trigSFB=1.0461007528; trigSFBunc=0.0149238889107;
            trigSFCDEF=1.01904642299; trigSFCDEFunc=0.0181710170484;
            }
	  }
	  else {
        if (leppt >=20.0 &&  leppt< 25.0 ) {
            trigSFB=0.0; trigSFBunc=-1;
            trigSFCDEF=1.19647528076; trigSFCDEFunc=0.0279497916168;
            }
        else if (leppt >=25.0 &&  leppt< 30.0 ) {
            trigSFB=0.0; trigSFBunc=-1;
            trigSFCDEF=1.16882475468; trigSFCDEFunc=0.0195107691178;
            }
        else if (leppt >=30.0 &&  leppt< 35.0 ) {
            trigSFB=0.0; trigSFBunc=-1;
            trigSFCDEF=1.17514382045; trigSFCDEFunc=0.169165525113;
            }
        else if (leppt >=35.0 &&  leppt< 40.0 ) {
            trigSFB=0.543989860379; trigSFBunc=0.14547991002;
            trigSFCDEF=1.05250212117; trigSFCDEFunc=0.0225076340631;
            }
        else if (leppt >=40.0 &&  leppt< 45.0 ) {
            trigSFB=1.05739184941; trigSFBunc=0.00789047727968;
            trigSFCDEF=1.04347879876; trigSFCDEFunc=0.0158637311148;
            }
        else if (leppt >=45.0 &&  leppt< 50.0 ) {
            trigSFB=1.07552884368; trigSFBunc=0.0106829876111;
            trigSFCDEF=1.07552884368; trigSFCDEFunc=0.0106829876111;
            }
        else if (leppt >=50.0 &&  leppt< 60.0 ) {
            trigSFB=1.06785906602; trigSFBunc=0.0077301392061;
            trigSFCDEF=1.04047806433; trigSFCDEFunc=0.0173271041498;
            }
        else if (leppt >=60.0 &&  leppt< 70.0 ) {
            trigSFB=1.05894469804; trigSFBunc=0.00771611811371;
            trigSFCDEF=1.02868913524; trigSFCDEFunc=0.0187776415751;
            }
        else if (leppt >=70.0 &&  leppt< 100.0 ) {
            trigSFB=1.03854075672; trigSFBunc=0.00552514353362;
            trigSFCDEF=1.0033359853; trigSFCDEFunc=0.0151014297158;
            }
        else if (leppt >=100.0 &&  leppt< 200.0 ) {
            trigSFB=1.03658177237; trigSFBunc=0.00528984872319;
            trigSFCDEF=1.03075827927; trigSFCDEFunc=0.00783527418978;
            }
        else {
            trigSFB=1.01020550365; trigSFBunc=0.00779170145734;
            trigSFCDEF=1.01020550365; trigSFCDEFunc=0.00779170145733;
            }
	  }
	  if (trigSFB < 0.1){
	  triggerSF = trigSFCDEF;
	  triggerSFUncert = trigSFCDEFunc;
	  }
	  else{
	  triggerSF = (4.823*trigSFB + 36.734*trigSFCDEF)/41.557;
	  triggerSFUncert = sqrt( pow(4.823*trigSFBunc/41.557,2) + pow(36.734*trigSFCDEFunc/41.557,2) );
	  }


	return triggerSF;

}

double HardcodedConditions::GetElectronTriggerXSF2018(double leppt, double lepeta)
{
	  //Trigger SF calculated by JHogan, HT >= 430, ttbar tag/probe, Id+iso applied
	float triggerSF18 = 1.0;
	float triggSF18Uncert = 1.0;
	  if (fabs(lepeta) < 0.8){
        if (leppt >=20.0 &&  leppt< 25.0 ) {triggerSF18=1.0670314856; triggSF18Uncert=0.00875315267781; }
        else if (leppt >=25.0 &&  leppt< 30.0 ) {triggerSF18=1.0499128083; triggSF18Uncert=0.0031247165944; }
        else if (leppt >=30.0 &&  leppt< 35.0 ) {triggerSF18=1.00621041046; triggSF18Uncert=0.0042497979947; }
        else if (leppt >=35.0 &&  leppt< 40.0 ) {triggerSF18=1.02422795836; triggSF18Uncert=0.00310166286402; }
        else if (leppt >=40.0 &&  leppt< 45.0 ) {triggerSF18=1.03558904355; triggSF18Uncert=0.00263344920681; }
        else if (leppt >=45.0 &&  leppt< 50.0 ) {triggerSF18=1.03474716309; triggSF18Uncert=0.0027799671747; }
        else if (leppt >=50.0 &&  leppt< 60.0 ) {triggerSF18=1.01260027831; triggSF18Uncert=0.00271688757315; }
        else if (leppt >=60.0 &&  leppt< 70.0 ) {triggerSF18=1.01212305341; triggSF18Uncert=0.0062052448711; }
        else if (leppt >=70.0 &&  leppt< 100.0 ) {triggerSF18=1.00340088961; triggSF18Uncert=0.00176541102064; }
        else if (leppt >=100.0 &&  leppt< 200.0 ) {triggerSF18=0.997574205522; triggSF18Uncert=0.00134545610057; }
        else  {triggerSF18=0.992697058409; triggSF18Uncert=0.00253795050908; }

        }
	  else if (fabs(lepeta) < 1.442){
        if (leppt >=20.0 &&  leppt< 25.0 ) {triggerSF18=1.12437681739; triggSF18Uncert=0.0075932996865; }
        else if (leppt >=25.0 &&  leppt< 30.0 ) {triggerSF18=1.07550983066; triggSF18Uncert=0.00476577651126; }
        else if (leppt >=30.0 &&  leppt< 35.0 ) {triggerSF18=1.03084039204; triggSF18Uncert=0.00668735845147; }
        else if (leppt >=35.0 &&  leppt< 40.0 ) {triggerSF18=1.04138824358; triggSF18Uncert=0.00538137691034; }
        else if (leppt >=40.0 &&  leppt< 45.0 ) {triggerSF18=1.05097643048; triggSF18Uncert=0.00372239498395; }
        else if (leppt >=45.0 &&  leppt< 50.0 ) {triggerSF18=1.04234383328; triggSF18Uncert=0.00366667742861; }
        else if (leppt >=50.0 &&  leppt< 60.0 ) {triggerSF18=1.04143606614; triggSF18Uncert=0.00970715361379; }
        else if (leppt >=60.0 &&  leppt< 70.0 ) {triggerSF18=1.01722246158; triggSF18Uncert=0.00392759954486; }
        else if (leppt >=70.0 &&  leppt< 100.0 ) {triggerSF18=1.0104522892; triggSF18Uncert=0.00236855031138; }
        else if (leppt >=100.0 &&  leppt< 200.0 ) {triggerSF18=0.999831753333; triggSF18Uncert=0.00195210024845; }
        else  {triggerSF18=0.994175176655; triggSF18Uncert=0.00377857034203; }
	  }
	  else if (fabs(lepeta) < 1.556) {
        if (leppt >20.0 &&  leppt< 25.0 ) {triggerSF18=1.10295078323; triggSF18Uncert=0.0488865333795; }
        else if (leppt >25.0 &&  leppt< 30.0 ) {triggerSF18=0.966520520194; triggSF18Uncert=0.120705655633; }
        else if (leppt >30.0 &&  leppt< 35.0 ) {triggerSF18=1.17938320259; triggSF18Uncert=0.0718021261304; }
        else if (leppt >35.0 &&  leppt< 40.0 ) {triggerSF18=1.20616437001; triggSF18Uncert=0.0833560551485; }
        else if (leppt >40.0 &&  leppt< 45.0 ) {triggerSF18=1.00507840459; triggSF18Uncert=0.00274864693113; }
        else if (leppt >45.0 &&  leppt< 50.0 ) {triggerSF18=1.06623280502; triggSF18Uncert=0.0402149474372; }
        else if (leppt >50.0 &&  leppt< 60.0 ) {triggerSF18=1.04420037013; triggSF18Uncert=0.0733326506729; }
        else if (leppt >60.0 &&  leppt< 70.0 ) {triggerSF18=1.01462540061; triggSF18Uncert=0.102066537958; }
        else if (leppt >70.0 &&  leppt< 100.0 ) {triggerSF18=1.01012931644; triggSF18Uncert=0.0048494662106; }
        else if (leppt >100.0 &&  leppt< 200.0 ) {triggerSF18=1.01360957744; triggSF18Uncert=0.0100629574181; }
        else {triggerSF18=1.04274527761; triggSF18Uncert=0.044572436364;}
	  }
	  else if (fabs(lepeta) < 2.0){
        if (leppt >=20.0 &&  leppt< 25.0 ) {triggerSF18=1.15666001871; triggSF18Uncert=0.015073354568; }
        else if (leppt >=25.0 &&  leppt< 30.0 ) {triggerSF18=1.1338916502; triggSF18Uncert=0.0321732752939; }
        else if (leppt >=30.0 &&  leppt< 35.0 ) {triggerSF18=1.07908854656; triggSF18Uncert=0.0424636253445; }
        else if (leppt >=35.0 &&  leppt< 40.0 ) {triggerSF18=1.04624854566; triggSF18Uncert=0.00917693729306; }
        else if (leppt >=40.0 &&  leppt< 45.0 ) {triggerSF18=1.04936439127; triggSF18Uncert=0.00551224232629; }
        else if (leppt >=45.0 &&  leppt< 50.0 ) {triggerSF18=1.04541518191; triggSF18Uncert=0.0059241055789; }
        else if (leppt >=50.0 &&  leppt< 60.0 ) {triggerSF18=1.05091611938; triggSF18Uncert=0.023416971145; }
        else if (leppt >=60.0 &&  leppt< 70.0 ) {triggerSF18=1.00314941274; triggSF18Uncert=0.00735793260239; }
        else if (leppt >=70.0 &&  leppt< 100.0 ) {triggerSF18=1.0014071838; triggSF18Uncert=0.00613007877119; }
        else if (leppt >=100.0 &&  leppt< 200.0 ) {triggerSF18=1.0195049775; triggSF18Uncert=0.0154470471865; }
        else  {triggerSF18=0.995298816473; triggSF18Uncert=0.0179251546103; }
        }
	  else{
        if (leppt >=20.0 &&  leppt< 25.0 ) {triggerSF18=1.09987049201; triggSF18Uncert=0.00562440298325; }
        else if (leppt >=25.0 &&  leppt< 30.0 ) {triggerSF18=1.07122500883; triggSF18Uncert=0.00484044388043; }
        else if (leppt >=30.0 &&  leppt< 35.0 ) {triggerSF18=1.02429081991; triggSF18Uncert=0.00647104843698; }
        else if (leppt >=35.0 &&  leppt< 40.0 ) {triggerSF18=1.03217586081; triggSF18Uncert=0.00266548321738; }
        else if (leppt >=40.0 &&  leppt< 45.0 ) {triggerSF18=1.04681708088; triggSF18Uncert=0.00494532195691; }
        else if (leppt >=45.0 &&  leppt< 50.0 ) {triggerSF18=1.03886408622; triggSF18Uncert=0.00204087554649; }
        else if (leppt >=50.0 &&  leppt< 60.0 ) {triggerSF18=1.02608538098; triggSF18Uncert=0.00435004675606; }
        else if (leppt >=60.0 &&  leppt< 70.0 ) {triggerSF18=1.01291470554; triggSF18Uncert=0.00379132821594; }
        else if (leppt >=70.0 &&  leppt< 100.0 ) {triggerSF18=1.00525339733; triggSF18Uncert=0.00141842634418; }
        else if (leppt >=100.0 &&  leppt< 200.0 ) {triggerSF18=1.00016819985; triggSF18Uncert=0.00175247967539; }
        else {triggerSF18=0.993999916871; triggSF18Uncert=0.00260426298855; }
	 }

  return triggerSF18;
}


/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|            MUON ID SCALE FACTOR SECTION             |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

double HardcodedConditions::GetMuonIdSF(double pt, double eta, int year)
{
  //The main getter for Muon Id Scale Factors
  if      (year==2016) return GetMuonIdSF2016(pt, eta);
  else if (year==2017) return GetMuonIdSF2017(pt, eta);
  else if (year==2018) return GetMuonIdSF2018(pt, eta);
  else return 0.;
}//end GetMuonIdSF

double HardcodedConditions::GetMuonIdSF2016APV(double pt, double eta)
{
  if ( pt < 20.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.98775;
    else if ( fabs(eta) < 1.2 ) return 0.98230;
    else if ( fabs(eta) < 2.1 ) return 0.98923;
    else return 0.97500; }
  else if ( pt < 25.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.99042;
    else if ( fabs(eta) < 1.2 ) return 0.98039;
    else if ( fabs(eta) < 2.1 ) return 0.98965;
    else return 0.97554; }
  else if ( pt < 30.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.98907;
    else if ( fabs(eta) < 1.2 ) return 0.97903;
    else if ( fabs(eta) < 2.1 ) return 0.98953;
    else return 0.97582; }
  else if ( pt < 40.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.98784;
    else if ( fabs(eta) < 1.2 ) return 0.98102;
    else if ( fabs(eta) < 2.1 ) return 0.99051;
    else return 0.97562; }
  else if ( pt < 50.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.98805;
    else if ( fabs(eta) < 1.2 ) return 0.97988;
    else if ( fabs(eta) < 2.1 ) return 0.99091;
    else return 0.97397; }
  else if ( pt < 60.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.98710;
    else if ( fabs(eta) < 1.2 ) return 0.97994;
    else if ( fabs(eta) < 2.1 ) return 0.98991;
    else return 0.97316; }
  else {
    if ( fabs(eta) < 0.9 ) return 0.98642;
    else if ( fabs(eta) < 1.2 ) return 0.97912;
    else if ( fabs(eta) < 2.1 ) return 0.98955;
    else return 0.96618; }	    
}

double HardcodedConditions::GetMuonIdSF2016( double pt, double eta ){
  if ( pt < 20.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.98943;
    else if ( fabs(eta) < 1.2 ) return 0.97899;
    else if ( fabs(eta) < 2.1 ) return 0.99012;
    else return 0.97577; }
  else if ( pt < 25.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.98763;
    else if ( fabs(eta) < 1.2 ) return 0.97658;
    else if ( fabs(eta) < 2.1 ) return 0.98945;
    else return 0.97531; }
  else if ( pt < 30.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.98792;
    else if ( fabs(eta) < 1.2 ) return 0.98151;
    else if ( fabs(eta) < 2.1 ) return 0.99097;
    else return 0.97610; }
  else if ( pt < 40.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.98650;
    else if ( fabs(eta) < 1.2 ) return 0.97872;
    else if ( fabs(eta) < 2.1 ) return 0.99050;
    else return 0.97594; }
  else if ( pt < 50.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.98673;
    else if ( fabs(eta) < 1.2 ) return 0.97925;
    else if ( fabs(eta) < 2.1 ) return 0.99152;
    else return 0.97642; }
  else if ( pt < 60.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.98517;
    else if ( fabs(eta) < 1.2 ) return 0.97903;
    else if ( fabs(eta) < 2.1 ) return 0.99063;
    else return 0.97201; }
  else {
    if ( fabs(eta) < 0.9 ) return 0.98463;
    else if ( fabs(eta) < 1.2 ) return 0.97832;
    else if ( fabs(eta) < 2.1 ) return 0.99049;
    else return 0.96955; } 
}

double HardcodedConditions::GetMuonIdSF2017(double pt, double eta)
{
if ( pt < 20.0 ) {
  if ( fabs(eta) < 0.9 ) return 0.98897;
  else if ( fabs(eta) < 1.2 ) return 0.98387;
  else if ( fabs(eta) < 2.1 ) return 0.98973;
  else return 0.97296; }
else if ( pt < 25.0 ) {
  if ( fabs(eta) < 0.9 ) return 0.99016;
  else if ( fabs(eta) < 1.2 ) return 0.98206;
  else if ( fabs(eta) < 2.1 ) return 0.98942;
  else return 0.97406; }
else if ( pt < 30.0 ) {
  if ( fabs(eta) < 0.9 ) return 0.98945;
  else if ( fabs(eta) < 1.2 ) return 0.98163;
  else if ( fabs(eta) < 2.1 ) return 0.99081;
  else return 0.97603; }
else if ( pt < 40.0 ) {
  if ( fabs(eta) < 0.9 ) return 0.98906;
  else if ( fabs(eta) < 1.2 ) return 0.98268;
  else if ( fabs(eta) < 2.1 ) return 0.99092;
  else return 0.97534; }
else if ( pt < 50.0 ) {
  if ( fabs(eta) < 0.9 ) return 0.98857;
  else if ( fabs(eta) < 1.2 ) return 0.98321;
  else if ( fabs(eta) < 2.1 ) return 0.99136;
  else return 0.97526; }
else if ( pt < 60.0 ) {
  if ( fabs(eta) < 0.9 ) return 0.98817;
  else if ( fabs(eta) < 1.2 ) return 0.98240;
  else if ( fabs(eta) < 2.1 ) return 0.99013;
  else return 0.97036; }
else {
  if ( fabs(eta) < 0.9 ) return 0.98716;
  else if ( fabs(eta) < 1.2 ) return 0.98270;
  else if ( fabs(eta) < 2.1 ) return 0.98935;
  else return 0.96776; }
}

double HardcodedConditions::GetMuonIdSF2018(double pt, double eta)
{
  if ( pt < 20.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.99159;
    else if ( fabs(eta) < 1.2 ) return 0.98433;
    else if ( fabs(eta) < 2.1 ) return 0.99002;
    else return 0.97497; }
  else if ( pt < 25.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.99339;
    else if ( fabs(eta) < 1.2 ) return 0.98319;
    else if ( fabs(eta) < 2.1 ) return 0.99000;
    else return 0.97239; }
  else if ( pt < 30.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.99251;
    else if ( fabs(eta) < 1.2 ) return 0.98308;
    else if ( fabs(eta) < 2.1 ) return 0.98982;
    else return 0.97306; }
  else if ( pt < 40.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.99233;
    else if ( fabs(eta) < 1.2 ) return 0.98436;
    else if ( fabs(eta) < 2.1 ) return 0.99000;
    else return 0.97180; }
  else if ( pt < 50.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.99195;
    else if ( fabs(eta) < 1.2 ) return 0.98399;
    else if ( fabs(eta) < 2.1 ) return 0.99039;
    else return 0.97227; }
  else if ( pt < 60.0 ) {
    if ( fabs(eta) < 0.9 ) return 0.99151;
    else if ( fabs(eta) < 1.2 ) return 0.98317;
    else if ( fabs(eta) < 2.1 ) return 0.98974;
    else return 0.96830; }
  else {
    if ( fabs(eta) < 0.9 ) return 0.99101;
    else if ( fabs(eta) < 1.2 ) return 0.98234;
    else if ( fabs(eta) < 2.1 ) return 0.98867;
    else return 0.96598; }
}

/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|            MUON ISO SCALE FACTOR SECTION            |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

double HardcodedConditions::GetMuonIsoSF(double pt, double eta, int year)
{
  //The main getter for Muon Iso Scale Factors
  if      (year==2016) return GetMuonIsoSF2016(pt, eta);
  else if (year==2017) return GetMuonIsoSF2017(pt, eta);
  else if (year==2018) return GetMuonIsoSF2018(pt, eta);
  else return 0.;
}//end GetMuonIsoSF

double HardcodedConditions::GetMuonIsoSF2016(double pt, double eta)
{
	// TO-BE-IMPLEMENTED!!!!!!!
	return 1.000;

}

double HardcodedConditions::GetMuonIsoSF2017(double pt, double eta)
{
	// MiniIsoTight/Tight
	// Jess Wong, approved in MUO 8/26/19, slide 37 upper left
	if(pt < 30){
        if(fabs(eta) < 0.9) return 0.9961;
        else if(fabs(eta) <  1.2) return 0.9921;
        else if(fabs(eta) <  2.1) return 0.9973;
        else if(fabs(eta) <  2.4) return 0.9990;
		else{ std::cerr << "The eta = " << eta << " not coded into HardcodedConditions::GetMuonIsoSF2017! Aborting ..." << std::endl; std::abort();}
		}
    else if(pt < 40){
        if(fabs(eta) < 0.9) return 0.9968;
        else if(fabs(eta) <  1.2) return 0.9962;
        else if(fabs(eta) <  2.1) return 0.9978;
        else if(fabs(eta) <  2.4) return 0.9988;
		else{ std::cerr << "The eta = " << eta << " not coded into HardcodedConditions::GetMuonIsoSF2017! Aborting ..." << std::endl; std::abort();}
		}
    else if(pt < 50){
        if(fabs(eta) < 0.9) return 0.9984;
        else if(fabs(eta) <  1.2) return 0.9976;
        else if(fabs(eta) <  2.1) return 0.9984;
        else if(fabs(eta) <  2.4) return 0.9996;
		else{ std::cerr << "The eta = " << eta << " not coded into HardcodedConditions::GetMuonIsoSF2017! Aborting ..." << std::endl; std::abort();}
		}
    else if(pt < 60){
        if(fabs(eta) < 0.9) return 0.9992;
        else if(fabs(eta) <  1.2) return 0.9989;
        else if(fabs(eta) <  2.1) return 0.9993;
        else if(fabs(eta) <  2.4) return 0.9988;
		else{ std::cerr << "The eta = " << eta << " not coded into HardcodedConditions::GetMuonIsoSF2017! Aborting ..." << std::endl; std::abort();}
		}
    else if(pt < 120){
        if(fabs(eta) < 0.9) return 0.9996;
        else if(fabs(eta) <  1.2) return 1.0000;
        else if(fabs(eta) <  2.1) return 1.0004;
        else if(fabs(eta) <  2.4) return 0.9987;
		else{ std::cerr << "The eta = " << eta << " not coded into HardcodedConditions::GetMuonIsoSF2017! Aborting ..." << std::endl; std::abort();}
		}
	else{ // ignoring the 200-300, low stats, using 120+
	    if(fabs(eta) < 0.9) return 0.9999;
        else if(fabs(eta) <  1.2) return 0.9992;
        else if(fabs(eta) <  2.1) return 1.0005;
        else if(fabs(eta) <  2.4) return 0.9964;
		else{ std::cerr << "The eta = " << eta << " not coded into HardcodedConditions::GetMuonIsoSF2017! Aborting ..." << std::endl; std::abort();}
		}
}

double HardcodedConditions::GetMuonIsoSF2018(double pt, double eta)
{
	//Miniisolation SF, Jess Wong approved in MUO 8/26/19, slide 38 upper left
    if(pt < 30){ // 25-30
        if(fabs(eta) < 0.9) return 0.9925;
        else if(fabs(eta) <  1.2) return 0.9932;
        else if(fabs(eta) <  2.1) return 1.0124;
        else return 1.0202;}
    else if(pt < 40){
        if(fabs(eta) < 0.9) return 0.9959;
        else if(fabs(eta) <  1.2) return 0.9957;
        else if(fabs(eta) <  2.1) return 1.0076;
        else return 1.0101;}
    else if(pt < 50){
        if(fabs(eta) < 0.9) return 0.9981;
        else if(fabs(eta) <  1.2) return 0.9978;
        else if(fabs(eta) <  2.1) return 1.0040;
        else return 1.0059;}
    else if(pt < 60){
        if(fabs(eta) < 0.9) return 0.9989;
        else if(fabs(eta) <  1.2) return 0.9982;
        else if(fabs(eta) <  2.1) return 1.0019;
        else return 1.0029;}
    else if(pt < 120){
        if(fabs(eta) < 0.9) return 0.9997;
        else if(fabs(eta) <  1.2) return 0.9995;
        else if(fabs(eta) <  2.1) return 1.0001;
        else return 1.0003;}
    else{ //120-200, ignoring 200-300 for low stats
        if(fabs(eta) < 0.9) return 1.0000;
        else if(fabs(eta) <  1.2) return 1.0016;
        else if(fabs(eta) <  2.1) return 0.9983;
        else return 1.0000;}

}

/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|          MUON TRIGGER SCALE FACTOR SECTION          |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

double HardcodedConditions::GetMuonTriggerSF(double pt, double eta, int year)
{
  //The main getter for Muon Trigger Scale Factors
  if      (year==2016) return GetMuonTriggerSF2016(pt, eta);
  else if (year==2017) return GetMuonTriggerSF2017(pt, eta);
  else if (year==2018) return GetMuonTriggerSF2018(pt, eta);
  else return 0.;
}//end GetMuonTriggerSF

double HardcodedConditions::GetMuonTriggerSF2016(double pt, double eta)
{
	// TO-BE-IMPLEMENTED!!!!!!!
	return 1.000;

}

double HardcodedConditions::GetMuonTriggerSF2017(double pt, double eta)
{
	float trigSFB = 1.0;
	float triggerSFCDEF = 1.0;
	float trigSFBunc = 0.0;
	float triggerSFCDEFunc = 0.0;
	if (eta > 0.0 && eta <= 0.8){
	    if(pt >30.0 && pt <= 35.0){trigSFB=1.10019349994; trigSFBunc=0.00547206712151;triggerSFCDEF=0.978804954631; triggerSFCDEFunc=0.00648538520448;}
	    else if(pt > 35.0 && pt <= 40.0){trigSFB=1.09211088948; trigSFBunc=0.00204401887493;triggerSFCDEF=0.984698671039; triggerSFCDEFunc=0.00602193913522;}
	    else if(pt > 40.0 && pt <= 45.0){trigSFB=1.07808450861; trigSFBunc=0.00464941695873;triggerSFCDEF=0.995559844257; triggerSFCDEFunc=0.00567940378055;}
	    else if(pt > 45.0 && pt <= 50.0){trigSFB=1.07193586473; trigSFBunc=0.00391132533692;triggerSFCDEF=0.988591733802; triggerSFCDEFunc=0.00579494608742;}
	    else if(pt > 50.0 && pt <= 60.0){trigSFB=1.01367573178; trigSFBunc=0.00984912438091;triggerSFCDEF=0.990844343111; triggerSFCDEFunc=0.00401810293322;}
	    else if(pt > 60.0 && pt >= 100.0){trigSFB=1.02371459077; trigSFBunc=0.00453347155488;triggerSFCDEF=0.9899251109; triggerSFCDEFunc=0.00222019796691;}
	    else if(pt > 100.0 && pt >= 200.0){trigSFB=1.01917413639; trigSFBunc=0.00428822026176;triggerSFCDEF=0.989816219066; triggerSFCDEFunc=0.00213658604325;}
	    else if(pt >200.0 && pt >= 300.0){trigSFB=1.03021004051; trigSFBunc=0.0047931519218;triggerSFCDEF=0.993698209245; triggerSFCDEFunc=0.00407479066069;}
	}
    else if (eta > 0.8 && eta <= 1.442){
	    if(pt >30.0 && pt <= 35.0){trigSFB=1.12077327256; trigSFBunc=0.0113246985811;triggerSFCDEF=0.965099847017; triggerSFCDEFunc=0.00969574453469;}
	    else if(pt > 35.0 && pt <=40.0){trigSFB=1.11606710619; trigSFBunc=0.00305398442218;triggerSFCDEF=0.974018899838; triggerSFCDEFunc=0.00871241069532;}
	    else if(pt >40.0 && pt<=45.0){trigSFB=1.10646659029; trigSFBunc=0.00302169373442;triggerSFCDEF=1.00039705989; triggerSFCDEFunc=0.00799929230775;}
	    else if(pt >45.0 && pt <=50.0){trigSFB=1.08923843408; trigSFBunc=0.00285057860769;triggerSFCDEF=0.979438599873; triggerSFCDEFunc=0.00829713158194;}
	    else if(pt > 50.0 && pt <= 60.0){trigSFB=1.0428344034; trigSFBunc=0.0107394273425;triggerSFCDEF=0.987897428252; triggerSFCDEFunc=0.0057226921376;}
	    else if(pt > 60.0 && pt >= 100.0){trigSFB=1.04106960725; trigSFBunc=0.00590548911614;triggerSFCDEF=0.984113306672; triggerSFCDEFunc=0.00341488478406;}
	    else if(pt > 100.0 && pt >= 200.0){trigSFB=1.03213107411; trigSFBunc=0.00600579292185;triggerSFCDEF=0.976053564253; triggerSFCDEFunc=0.00376853102255;}
	    else if(pt >200.0 && pt >= 300.0){trigSFB=1.04783653937; trigSFBunc=0.00247601879159;triggerSFCDEF=0.978883600082; triggerSFCDEFunc=0.00805752356996;}
	}
	else if (eta > 1.442 && eta <= 2.0){
	    if(pt >30.0 && pt <= 35.0){trigSFB=1.22434938101; trigSFBunc=0.0218235518324;triggerSFCDEF=0.986556201882; triggerSFCDEFunc=0.0215042582357;}
	    else if(pt > 35.0 && pt <=40.0){trigSFB=1.231305767; trigSFBunc=0.0357351749146;triggerSFCDEF=1.01780514621; triggerSFCDEFunc=0.0334931969651;}
	    else if(pt >40.0 && pt<=45.0){trigSFB=1.17997761091; trigSFBunc=0.040152142672;triggerSFCDEF=1.01890545164; triggerSFCDEFunc=0.0353809067738;}
	    else if(pt >45.0 && pt <=50.0){trigSFB=1.17228284782; trigSFBunc=0.0101568501078;triggerSFCDEF=1.02366913264; triggerSFCDEFunc=0.0159136035832;}
	    else if(pt > 50.0 && pt <= 60.0){trigSFB=1.10280648865; trigSFBunc=0.0136560295169;triggerSFCDEF=0.987117193306; triggerSFCDEFunc=0.0100560754841;}
	    else if(pt > 60.0 && pt >= 100.0){trigSFB=1.1679117327; trigSFBunc=0.0741698407372;triggerSFCDEF=1.0680856167; triggerSFCDEFunc=0.068623275864;}
	    else if(pt > 100.0 && pt >= 200.0){trigSFB=1.07915769032; trigSFBunc=0.0109413337715;triggerSFCDEF=0.994679822421; triggerSFCDEFunc=0.00762790132034;}
	    else if(pt >200.0 && pt >= 300.0){trigSFB=1.08679975819; trigSFBunc=0.00620436693934;triggerSFCDEF=1.00717797389; triggerSFCDEFunc=0.0151510689245;}
	}
	else if (eta > 2.0 && eta <= 2.4){
	    if(pt >30.0 && pt <= 35.0){trigSFB=1.22370728989; trigSFBunc=0.0285118014412;triggerSFCDEF=1.00353720864; triggerSFCDEFunc=0.0453772901758;}
	    else if(pt > 35.0 && pt <=40.0){trigSFB=1.18312757909; trigSFBunc=0.015933227322;triggerSFCDEF=0.935607479429; triggerSFCDEFunc=0.045376726802;}
	    else if(pt >40.0 && pt<=45.0){trigSFB=1.24146385007; trigSFBunc=0.0551921513212;triggerSFCDEF=1.00575925128; triggerSFCDEFunc=0.0652837869259;}
	    else if(pt >45.0 && pt <=50.0){trigSFB=1.01577521883; trigSFBunc=0.136561805823;triggerSFCDEF=0.950742260548; triggerSFCDEFunc=0.0437089261971;}
	    else if(pt > 50.0 && pt <= 60.0){trigSFB=1.12059750687; trigSFBunc=0.0109156647416;triggerSFCDEF=0.936123755289; triggerSFCDEFunc=0.0349139266772;}
	    else if(pt > 60.0 && pt >= 100.0){trigSFB=1.06117478026; trigSFBunc=0.0360468039116;triggerSFCDEF=0.911047525283; triggerSFCDEFunc=0.0239852531794;}
	    else if(pt > 100.0 && pt >= 200.0){trigSFB=1.03333258161; trigSFBunc=0.0596440436066;triggerSFCDEF=0.995804840183; triggerSFCDEFunc=0.0219341652245;}
	    else if(pt >200.0 && pt >= 300.0){trigSFB=0.552600867674; trigSFBunc=0.39096055356;triggerSFCDEF=0.989342189114; triggerSFCDEFunc=0.0887423004862;}
	}
	/*if (ht > 500.0 && ht < 750.0){
	  if (pt > 20.0 && pt < 50.0){trigSFB = 0.907;triggerSFC = 0.968;triggerSFDEF = 0.970;}
	  else if (pt >=50.0 && pt <= 300.0){trigSFB = 0.904;triggerSFC = 0.997;triggerSFDEF = 0.998;}
	}
	else if (ht >= 750.0 && ht < 3000.0){
	    if (pt > 20.0 && pt < 50.0){trigSFB = 0.882;triggerSFC = 0.992;triggerSFDEF = 0.930;}
	    else if (pt >=50.0 && pt <= 300.0){trigSFB = 0.891;triggerSFC = 0.983;triggerSFDEF = 0.983;}
	}*/
	float triggerSFUncert = sqrt( pow(4.823*trigSFBunc/41.557,2) + pow(36.734*triggerSFCDEFunc/41.557,2) );
	float triggerSF = (4.823*trigSFB + 36.734*triggerSFCDEF)/41.557;
	return triggerSF;

}

double HardcodedConditions::GetMuonTriggerSF2018(double pt, double eta)
{
	float triggerSFABCD = 1.0;
	float triggerSFABCDunc = 0.0;
	if (eta > 0.0 && eta <= 0.8){
	    if(pt >25.0 && pt <= 30.0){triggerSFABCD=0.94767883255; triggerSFABCDunc=0.00682250481374;}
	    else if(pt >30.0 && pt <= 35.0){triggerSFABCD=0.975343471352; triggerSFABCDunc=0.00521575836242;}
	    else if(pt > 35.0 && pt <= 40.0){triggerSFABCD=0.979786994807; triggerSFABCDunc=0.00494941444298;}
	    else if(pt > 40.0 && pt <= 45.0){triggerSFABCD=0.982749255218; triggerSFABCDunc=0.00465578298111;}
	    else if(pt > 45.0 && pt <= 50.0){triggerSFABCD=0.984508302475; triggerSFABCDunc=0.00453720177682;}
	    else if(pt > 50.0 && pt <= 60.0){triggerSFABCD=0.984211706209; triggerSFABCDunc=0.00317949601845;}
	    else if(pt > 60.0 && pt >= 100.0){triggerSFABCD=0.985833185857; triggerSFABCDunc=0.00175732224141;}
	    else if(pt > 100.0 && pt >= 200.0){triggerSFABCD=0.9894052249; triggerSFABCDunc=0.00162976487427;}
	    else if(pt >200.0 && pt >= 300.0){triggerSFABCD=0.98573388878; triggerSFABCDunc=0.00344224738942;}
	}
	else if (eta > 0.8 && eta <= 1.442){
	    if(pt >25.0 && pt <= 30.0){triggerSFABCD=0.940534308542; triggerSFABCDunc=0.00945493136507;}
	    else if(pt >30.0 && pt <= 35.0){triggerSFABCD=0.977250612414; triggerSFABCDunc=0.00720613736371;}
	    else if(pt > 35.0 && pt <= 40.0){triggerSFABCD=0.978939288095; triggerSFABCDunc=0.00691089368913;}
	    else if(pt > 40.0 && pt <= 45.0){triggerSFABCD=1.00221553593; triggerSFABCDunc=0.0060361955257;}
	    else if(pt > 45.0 && pt <= 50.0){triggerSFABCD=0.98279079978; triggerSFABCDunc=0.00628465006595;}
	    else if(pt > 50.0 && pt <= 60.0){triggerSFABCD=0.982680516659; triggerSFABCDunc=0.00452110678634;}
	    else if(pt > 60.0 && pt >= 100.0){triggerSFABCD=0.983137416465; triggerSFABCDunc=0.00257052834567;}
	    else if(pt > 100.0 && pt >= 200.0){triggerSFABCD=0.983626984691; triggerSFABCDunc=0.00275793170224;}
	    else if(pt >200.0 && pt >= 300.0){triggerSFABCD=0.977732187568; triggerSFABCDunc=0.00592051551757;}
	}
	else if (eta > 1.442 && eta <= 2.0){
	    if(pt >25.0 && pt <= 30.0){triggerSFABCD=0.984935935005; triggerSFABCDunc=0.0274745597906;}
	    else if(pt >30.0 && pt <= 35.0){triggerSFABCD=0.993393945563; triggerSFABCDunc=0.0224931800147;}
	    else if(pt > 35.0 && pt <= 40.0){triggerSFABCD=0.969211890199; triggerSFABCDunc=0.0126944223266;}
	    else if(pt > 40.0 && pt <= 45.0){triggerSFABCD=1.01711048762; triggerSFABCDunc=0.0237901621894;}
	    else if(pt > 45.0 && pt <= 50.0){triggerSFABCD=1.00678501376; triggerSFABCDunc=0.0111245808153;}
	    else if(pt > 50.0 && pt <= 60.0){triggerSFABCD=1.02287293295; triggerSFABCDunc=0.0182139340892;}
	    else if(pt > 60.0 && pt >= 100.0){triggerSFABCD=1.00718248827; triggerSFABCDunc=0.00559986702137;}
	    else if(pt > 100.0 && pt >= 200.0){triggerSFABCD=1.01037269188; triggerSFABCDunc=0.00556910617477;}
	    else if(pt >200.0 && pt >= 300.0){triggerSFABCD=1.0257553878; triggerSFABCDunc=0.0105437651897;}
	}
	else if (eta > 2.0 && eta <= 2.4){
	    if(pt >25.0 && pt <= 30.0){triggerSFABCD=0.88440469579; triggerSFABCDunc=0.0414085800527;}
	    else if(pt >30.0 && pt <= 35.0){triggerSFABCD=0.969619810729; triggerSFABCDunc=0.0356664367863;}
	    else if(pt > 35.0 && pt <= 40.0){triggerSFABCD=1.01974116338; triggerSFABCDunc=0.031654361893;}
	    else if(pt > 40.0 && pt <= 45.0){triggerSFABCD=1.02253219101; triggerSFABCDunc=0.0290017650303;}
	    else if(pt > 45.0 && pt <= 50.0){triggerSFABCD=1.0096846675; triggerSFABCDunc=0.0315634676889;}
	    else if(pt > 50.0 && pt <= 60.0){triggerSFABCD=1.04752858664; triggerSFABCDunc=0.0214622072212;}
	    else if(pt > 60.0 && pt >= 100.0){triggerSFABCD=0.995781529538; triggerSFABCDunc=0.0175074289416;}
	    else if(pt > 100.0 && pt >= 200.0){triggerSFABCD=1.03167948671; triggerSFABCDunc=0.0188983168656;}
	    else if(pt >200.0 && pt >= 300.0){triggerSFABCD=0.980451308225; triggerSFABCDunc=0.0530839815221;}
	}

	/*if (ht > 500.0 && ht < 750.0){
	  if (pt > 20.0 && pt < 50.0){triggerSFAB = 0.938;triggerSFCD = 0.948;}
	  else if (pt >=50.0 && pt <= 300.0){triggerSFAB = 0.985;triggerSFCD = 0.996;}
	}
	else if (ht >= 750.0 && ht < 3000.0){
	    if (pt > 20.0 && pt < 50.0){triggerSFAB = 0.921;triggerSFCD = 0.941;}
	    else if (pt >=50.0 && pt <= 300.0){triggerSFAB = 0.974;triggerSFCD = 0.984;}
	}*/
	return triggerSFABCD;
}



/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|         HADRON TRIGGER SCALE FACTOR SECTION         |\  | |/|
 | `---' |                  (For Muon Channel)                 | `---' |
 |       |                                                     |       |
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

double HardcodedConditions::GetIsMHadronTriggerSF(double njets, double ht, int year)
{
  //The main getter for Electron Trigger Scale Factors
  if      (year==2016) return GetIsMHadronTriggerSF2016(njets, ht);
  else if (year==2017) return GetIsMHadronTriggerSF2017(njets, ht);
  else if (year==2018) return GetIsMHadronTriggerSF2018(njets, ht);
  else return 0.;
}//end GetElectronTriggerSF

double HardcodedConditions::GetIsMHadronTriggerSF2016(double njets, double ht)
{
	// TO-BE-IMPLEMENTED!!!!!!!
	return 1.000;

}

double HardcodedConditions::GetIsMHadronTriggerSF2017(double njets, double ht)
{
	// Trigger Scale Factors, SF2017B_Bkg_LepPtEta_EOR.png & SF2017CDEF_Bkg_LepPtEta_EOR.png
	float triggerSFB = 1.0;
	float triggerSFC = 1.0;
	float triggerSFDEF = 1.0;
	float triggerSFBunc = 0.0;
	float triggerSFCunc = 0.0;
	float triggerSFDEFunc = 0.0;
	if (njets == 6){
	    if(ht > 500.0 && ht < 675.0){triggerSFB=0.901326599437; triggerSFBunc=0.0354950845149;triggerSFC=1.19172560657; triggerSFCunc=0.0164392192176;triggerSFDEF=1.09823276295; triggerSFDEFunc=0.0100095399407;}
	    else if(ht > 675.0 && ht < 850.0){triggerSFB=0.830153048387; triggerSFBunc=0.0514163341268;triggerSFC=1.06853722984; triggerSFCunc=0.0265488363692;triggerSFDEF=0.992368364074; triggerSFDEFunc=0.0153680492905;}
	    else if(ht > 850.0 && ht < 1025.0){triggerSFB=0.602324618842; triggerSFBunc=0.0744577774499;triggerSFC=0.968021708854; triggerSFCunc=0.0426049999959;triggerSFDEF=0.900528683477; triggerSFDEFunc=0.0246781298394;}
	    else if(ht > 1025.0 ){triggerSFB=0.592984765997; triggerSFBunc=0.0753255460925;triggerSFC=0.877662462006; triggerSFCunc=0.0498138245222;triggerSFDEF=0.900231158951; triggerSFDEFunc=0.0284134132168;}
	}
	else if (njets == 7){
	    if(ht > 500.0 && ht < 675.0){triggerSFB=0.888523145227; triggerSFBunc=0.0376657314246;triggerSFC=1.10996776087; triggerSFCunc=0.0183378530547;triggerSFDEF=1.05633176475; triggerSFDEFunc=0.0108103768438;}
	    else if(ht > 675.0 && ht < 850.0){triggerSFB=0.77942085976; triggerSFBunc=0.0465047067053;triggerSFC=1.06057015809; triggerSFCunc=0.0262271488879;triggerSFDEF=0.983397354665; triggerSFDEFunc=0.0141916490162;}
	    else if(ht > 850.0 && ht < 1025.0){triggerSFB=0.635882535413; triggerSFBunc=0.0636807224067;triggerSFC=1.06057015809; triggerSFCunc=0.0262271488879;triggerSFDEF=0.933675813752; triggerSFDEFunc=0.0209332819546;}
	    else if(ht > 1025.0 ){triggerSFB=0.56315405395; triggerSFBunc=0.0636124824921;triggerSFC=0.935923640798; triggerSFCunc=0.045168726139;triggerSFDEF=0.913210566682; triggerSFDEFunc=0.023095010078;}
	}
	else if (njets == 8){
	    if(ht > 500.0 && ht < 675.0){triggerSFB=0.809731948392; triggerSFBunc=0.0557441511507;triggerSFC=1.09717908007; triggerSFCunc=0.0310553042709;triggerSFDEF=1.02895141685; triggerSFDEFunc=0.0176679617243;}
	    else if(ht > 675.0 && ht < 850.0){triggerSFB=0.729024126758; triggerSFBunc=0.0597441485766;triggerSFC=1.0882040809; triggerSFCunc=0.0307231379301;triggerSFDEF=0.997978447484; triggerSFDEFunc=0.0189183840341;}
	    else if(ht > 850.0 && ht < 1025.0){triggerSFB=0.653313124493; triggerSFBunc=0.0711705888524;triggerSFC=0.975303164422; triggerSFCunc=0.0456403600603;triggerSFDEF=0.945354592444; triggerSFDEFunc=0.0256551175158;}
	    else if(ht > 1025.0 ){triggerSFB=0.550424290651; triggerSFBunc=0.0674178254638;triggerSFC=0.748619204416; triggerSFCunc=0.0536522406822;triggerSFDEF=0.919439957568; triggerSFDEFunc=0.0252186935352; }
	}
	else if (njets >= 9){
	    if(ht > 500.0 && ht < 675.0){triggerSFB=0.814496992569; triggerSFBunc=0.118371956733;triggerSFC=1.085125801; triggerSFCunc=0.0692566389692;triggerSFDEF=1.02280353055; triggerSFDEFunc=0.0354297237006;}
	    else if(ht > 675.0 && ht < 850.0){triggerSFB=0.782492896323; triggerSFBunc=0.101728714292;triggerSFC=0.956428401548; triggerSFCunc=0.0581483146783;triggerSFDEF=1.00011547977; triggerSFDEFunc=0.0276193784769;}
	    else if(ht > 850.0 && ht < 1025.0){triggerSFB=0.752102032105; triggerSFBunc=0.100055276209;triggerSFC=0.949406721047; triggerSFCunc=0.0619238063511;triggerSFDEF=0.966483491257; triggerSFDEFunc=0.0331239016439;}
	    else if(ht > 1025.0 ){triggerSFB=0.666638798389; triggerSFBunc=0.073370227875;triggerSFC=0.84948067102; triggerSFCunc=0.0531191922696;triggerSFDEF=0.891699501211; triggerSFDEFunc=0.027118923292;}
	}
    float triggerSFUncert = sqrt( pow(4.823*triggerSFBunc/41.557,2) + pow(9.664*triggerSFCunc/41.557,2) + pow(27.07*triggerSFDEFunc/41.557,2) );
    float triggerSF = (4.823*triggerSFB+ 9.664*triggerSFC + 27.07*triggerSFDEF)/41.557;
	return triggerSF;

}

double HardcodedConditions::GetIsMHadronTriggerSF2018(double njets, double ht)
{
  float triggerSFAB = 1.0;
  float triggerSFCD = 1.0;
  float triggerSFABunc = 0.0;
  float triggerSFCDunc = 0.0;
  	if (njets == 6){
	    if(ht > 500.0 && ht < 675.0){triggerSFAB=0.917992750326; triggerSFABunc=0.0122463316509;triggerSFCD=0.939923153561; triggerSFCDunc=0.0082356257948;}
	    else if(ht > 675.0 && ht < 850.0){triggerSFAB=0.846308380222; triggerSFABunc=0.0167618650341;triggerSFCD=0.867127741783; triggerSFCDunc=0.0114937087304;}
	    else if(ht > 850.0 && ht < 1025.0){triggerSFAB=0.756647287925; triggerSFABunc=0.0250683495324;triggerSFCD=0.786170997991; triggerSFCDunc=0.0166227550308;}
	    else if(ht > 1025.0 ){triggerSFAB=0.769110750518; triggerSFABunc=0.0304131337995;triggerSFCD=0.834480666716; triggerSFCDunc=0.0195823674297;}
	}
	else if (njets == 7){
	    if(ht > 500.0 && ht < 675.0){triggerSFAB=1.00833408459; triggerSFABunc=0.0128092215587; triggerSFCD=0.999895538188; triggerSFCDunc=0.00891742484208;}
	    else if(ht > 675.0 && ht < 850.0){triggerSFAB=0.928336995294; triggerSFABunc=0.0171104567865;triggerSFCD=0.959939380589; triggerSFCDunc=0.0110178993694;}
	    else if(ht > 850.0 && ht < 1025.0){triggerSFAB=0.893208371203; triggerSFABunc=0.0245150164125;triggerSFCD=0.9330397495; triggerSFCDunc=0.016043807924;}
	    else if(ht > 1025.0 ){triggerSFAB=0.8453263973; triggerSFABunc=0.0282535064794;triggerSFCD=0.949429540887; triggerSFCDunc=0.0175244609096;}
	}
	else if (njets == 8){
	    if(ht > 500.0 && ht < 675.0){triggerSFAB=1.01216041006; triggerSFABunc=0.0202893598503;triggerSFCD=1.04087019648; triggerSFCDunc=0.013779196679;}
	    else if(ht > 675.0 && ht < 850.0){triggerSFAB=0.97574520943; triggerSFABunc=0.0220361148103;triggerSFCD=0.970238811026; triggerSFCDunc=0.0145427369355;}
	    else if(ht > 850.0 && ht < 1025.0){triggerSFAB=0.923862342232; triggerSFABunc=0.028935592128;triggerSFCD=0.96157918255; triggerSFCDunc=0.018875465188;}
	    else if(ht > 1025.0 ){triggerSFAB=0.938040650652; triggerSFABunc=0.0288231271496;triggerSFCD=0.96422449985; triggerSFCDunc=0.0195199213706;}

	}
	else if (njets >= 9){
	    if(ht > 500.0 && ht < 675.0){triggerSFAB=1.10805831835; triggerSFABunc=0.0366536540938;triggerSFCD=1.04315580609; triggerSFCDunc=0.0265880677639;}
	    else if(ht > 675.0 && ht < 850.0){triggerSFAB=0.973928026964; triggerSFABunc=0.0322303705451;triggerSFCD=1.01979486697; triggerSFCDunc=0.0212305462838;}
	    else if(ht > 850.0 && ht < 1025.0){triggerSFAB=0.952334087619; triggerSFABunc=0.0367099921666;triggerSFCD=1.00054905845; triggerSFCDunc=0.0232230442621;}
	    else if(ht > 1025.0 ){triggerSFAB=0.884807946965; triggerSFABunc=0.0337246901529;triggerSFCD=1.00428267929; triggerSFCDunc=0.0190601862132;}
	}
  float triggerSFUncert = sqrt( pow(21.10*triggerSFABunc/59.97,2) + pow(38.87*triggerSFCDunc/59.97,2) );
  float triggerSF = (21.10*triggerSFAB+ 38.87*triggerSFCD)/59.97;
  return triggerSF;
}




/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|          MUON TRIGGER SCALE FACTOR SECTION          |\  | |/|
 | `---' |           (using cross triggers from VLQ)           | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

double HardcodedConditions::GetMuonTriggerVlqXSF(double pt, double eta, int year)
{
  //The main getter for Muon Trigger Scale Factors
  if      (year==2016) return GetMuonTriggerVlqXSF2016(pt, eta);
  else if (year==2017) return GetMuonTriggerVlqXSF2017(pt, eta);
  else if (year==2018) return GetMuonTriggerVlqXSF2018(pt, eta);
  else return 0.;
}//end GetMuonTriggerVlqXSF

double HardcodedConditions::GetMuonTriggerVlqXSF2016(double pt, double eta)
{
	// TO-BE-IMPLEMENTED!!!!!!!
	return 1.000;

}

double HardcodedConditions::GetMuonTriggerVlqXSF2017(double leppt, double lepeta)
{
	  float triggerSFB = 1.0;
	  float triggerSFCDEF = 1.0;
	  float triggerSFBunc = 0.0;
	  float triggerSFCDEFunc = 0.0;
	  if (fabs(lepeta) < 0.90){
		if (leppt < 50.0){
		  triggerSFB = 1.0; triggerSFBunc = 0.0;
		  triggerSFCDEF = 1.034; triggerSFCDEFunc = 0.014;
		}
		else if (leppt < 60.0){
		  triggerSFB = 0.905; triggerSFBunc = 0.057;
		  triggerSFCDEF = 0.980;  triggerSFCDEFunc = 0.015;
		}
		else if (leppt < 70.0){
		  triggerSFB = 0.978; triggerSFBunc = 0.050;
		  triggerSFCDEF = 0.983;  triggerSFCDEFunc = 0.016;
		}
		else if (leppt < 100){
		  triggerSFB = 0.924; triggerSFBunc = 0.039;
		  triggerSFCDEF = 1.006;  triggerSFCDEFunc = 0.008;
		}
		else if (leppt < 200){
		  triggerSFB = 0.972; triggerSFBunc = 0.028;
		  triggerSFCDEF = 0.971;  triggerSFCDEFunc = 0.010;
		}
		else{
		  triggerSFB = 0.976; triggerSFBunc = 0.063;
		  triggerSFCDEF = 0.976;  triggerSFCDEFunc = 0.024;
		}
	  }
	  else if (fabs(lepeta) < 1.20){
		if (leppt < 50.0){
		  triggerSFB = 1.0; triggerSFBunc = 0.0;
		  triggerSFCDEF = 1.005; triggerSFCDEFunc = 0.028;
		}
		else if (leppt < 60.0){
		  triggerSFB = 0.931; triggerSFBunc = 0.125;
		  triggerSFCDEF = 1.030;  triggerSFCDEFunc = 0.021;
		}
		else if (leppt < 70.0){
		  triggerSFB = 1.051; triggerSFBunc = 0.008;
		  triggerSFCDEF = 0.976;  triggerSFCDEFunc = 0.033;
		}
		else if (leppt < 100){
		  triggerSFB = 0.978; triggerSFBunc = 0.048;
		  triggerSFCDEF = 0.953;  triggerSFCDEFunc = 0.022;
		}
		else if (leppt < 200){
		  triggerSFB = 0.982; triggerSFBunc = 0.044;
		  triggerSFCDEF = 0.954;  triggerSFCDEFunc = 0.022;
		}
		else{
		  triggerSFB = 1.047; triggerSFBunc = 0.010;
		  triggerSFCDEF = 1.012;  triggerSFCDEFunc = 0.036;
		}
	  }
	  else if (fabs(lepeta) < 2.10){
		if (leppt < 50.0){
		  triggerSFB = 0.047; triggerSFBunc = 0.046;
		  triggerSFCDEF = 1.086; triggerSFCDEFunc = 0.027;
		}
		else if (leppt < 60.0){
		  triggerSFB = 0.803; triggerSFBunc = 0.110;
		  triggerSFCDEF = 1.065;  triggerSFCDEFunc = 0.017;
		}
		else if (leppt < 70.0){
		  triggerSFB = 1.027; triggerSFBunc = 0.056;
		  triggerSFCDEF = 1.031;  triggerSFCDEFunc = 0.024;
		}
		else if (leppt < 100){
		  triggerSFB = 0.928; triggerSFBunc = 0.053;
		  triggerSFCDEF = 1.012;  triggerSFCDEFunc = 0.015;
		}
		else if (leppt < 200){
		  triggerSFB = 0.977; triggerSFBunc = 0.018;
		  triggerSFCDEF = 0.974;  triggerSFCDEFunc = 0.021;
		}
		else{
		  triggerSFB = 0.524; triggerSFBunc = 0.370;
		  triggerSFCDEF = 1.047;  triggerSFCDEFunc = 0.009;
		}
	  }
	  else{
		if (leppt < 50.0){
		  triggerSFB = 1.0; triggerSFBunc = 0.0;
		  triggerSFCDEF = 1.166; triggerSFCDEFunc = 0.033;
		}
		else if (leppt < 60.0){
		  triggerSFB = 1.126; triggerSFBunc = 0.029;
		  triggerSFCDEF = 1.126;  triggerSFCDEFunc = 0.029;
		}
		else if (leppt < 70.0){
		  triggerSFB = 0.726; triggerSFBunc = 0.297;
		  triggerSFCDEF = 0.953;  triggerSFCDEFunc = 0.092;
		}
		else if (leppt < 100){
		  triggerSFB = 1.075; triggerSFBunc = 0.016;
		  triggerSFCDEF = 1.032;  triggerSFCDEFunc = 0.045;
		}
		else if (leppt < 200){
		  triggerSFB = 1.059; triggerSFBunc = 0.014;
		  triggerSFCDEF = 0.934;  triggerSFCDEFunc = 0.084;
		}
		else{
		  triggerSFB = 1.00; triggerSFBunc = 0.050;
		  triggerSFCDEF = 1.006;  triggerSFCDEFunc = 0.04;
		}
	  }
	  float triggerSF = (4.823*triggerSFB+36.734*triggerSFCDEF)/41.557;
	  float triggerSFUncert = sqrt( pow(4.823*triggerSFBunc/41.557,2) + pow(36.734*triggerSFCDEFunc/41.557,2) );

	return triggerSF;

}

double HardcodedConditions::GetMuonTriggerVlqXSF2018(double leppt, double lepeta)
{
	float triggSF = 1.0;
	float triggSFUncert = 1.0;
	if (fabs(lepeta) < 0.9){
		if (leppt < 30) {triggSF = 0.995; triggSFUncert = 0.014;}
		else if (leppt < 40) {triggSF = 1.047; triggSFUncert = 0.013;} 
		else if (leppt < 50) {triggSF = 1.050; triggSFUncert = 0.012;}
		else if (leppt < 60) {triggSF = 1.019; triggSFUncert = 0.009;}
		else if (leppt < 70) {triggSF = 1.035; triggSFUncert = 0.007;}
		else if (leppt < 100) {triggSF = 0.997; triggSFUncert = 0.007;}
		else if (leppt < 200) {triggSF = 0.989; triggSFUncert = 0.007;}
		else {triggSF = 0.960; triggSFUncert = 0.021;}
	  }	  
	else if (fabs(lepeta) < 1.2){ 
		if (leppt < 30) {triggSF = 0.944; triggSFUncert = 0.030;}
		else if (leppt < 40) {triggSF = 1.017; triggSFUncert = 0.022;}
		else if (leppt < 50) {triggSF = 0.986; triggSFUncert = 0.024;}
		else if (leppt < 60) {triggSF = 0.987; triggSFUncert = 0.016;}
		else if (leppt < 70) {triggSF = 0.988; triggSFUncert = 0.018;}
		else if (leppt < 100) {triggSF = 0.982; triggSFUncert = 0.013;}
		else if (leppt < 200) {triggSF = 0.983; triggSFUncert = 0.012;}
		else {triggSF = 0.997; triggSFUncert = 0.021;}
	  }
	else if (fabs(lepeta) < 2.1){ 
		if (leppt < 30) {triggSF = 0.989; triggSFUncert = 0.021;}
		else if (leppt < 40) {triggSF = 1.041; triggSFUncert = 0.018;}
		else if (leppt < 50) {triggSF = 1.050; triggSFUncert = 0.020;}
		else if (leppt < 60) {triggSF = 1.033; triggSFUncert = 0.012;}
		else if (leppt < 70) {triggSF = 0.981; triggSFUncert = 0.018;}
		else if (leppt < 100) {triggSF = 1.008; triggSFUncert = 0.009;}
		else if (leppt < 200) {triggSF = 1.001; triggSFUncert = 0.010;}
		else {triggSF = 0.938; triggSFUncert = 0.045;}
	  }	  
	else{
		if (leppt < 30) {triggSF = 0.964; triggSFUncert = 0.078;}
		else if (leppt < 40) {triggSF = 1.069; triggSFUncert = 0.066;}
		else if (leppt < 50) {triggSF = 1.088; triggSFUncert = 0.053;}
		else if (leppt < 60) {triggSF = 1.067; triggSFUncert = 0.055;}
		else if (leppt < 70) {triggSF = 1.017; triggSFUncert = 0.055;}
		else if (leppt < 100) {triggSF = 1.128; triggSFUncert = 0.020;}
		else if (leppt < 200) {triggSF = 0.958; triggSFUncert = 0.067;}
		else {triggSF = 1.066; triggSFUncert = 0.042;}
	 }	  

	return triggSF;
}


/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|          MUON TRIGGER SCALE FACTOR SECTION          |\  | |/|
 | `---' |                    (from Nikos)                     | `---' |
 |       |                                                     |       |
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

double HardcodedConditions::GetMuonTriggerXSF(double pt, double eta, int year)
{
  //The main getter for Muon Trigger Scale Factors
  if      (year==2016) return GetMuonTriggerXSF2016(pt, eta);
  else if (year==2017) return GetMuonTriggerXSF2017(pt, eta);
  else if (year==2018) return GetMuonTriggerXSF2018(pt, eta);
  else return 0. ;
}//end GetMuonTriggerXSF

double HardcodedConditions::GetMuonTriggerXSF2016(double pt, double eta)
{
	// TO-BE-IMPLEMENTED!!!!!!!
	return 1.000 ;

}

double HardcodedConditions::GetMuonTriggerXSF2017(double leppt, double lepeta)
{
	  float triggerSFB = 1.0;
	  float triggerSFCDEF = 1.0;
	  float triggerSFBunc = 0.0;
	  float triggerSFCDEFunc = 0.0;
	  float triggerSF;
	  float triggerSFUncert;
	  if (fabs(lepeta) < 0.90){
		if (leppt >=20.0 &&  leppt< 25.0 ) {
		    triggerSFB=0.10901424368; triggerSFBunc=0.0297520484758;
            triggerSFCDEF=1.0052069587; triggerSFCDEFunc=0.0026600686695;
		    }
        else if (leppt >=25.0 &&  leppt< 30.0 ) {
            triggerSFB=0.0210210903521; triggerSFBunc=0.00735762154869;
            triggerSFCDEF=0.960995864882; triggerSFCDEFunc=0.00500791874781;
            }
        else if (leppt >=30.0 &&  leppt< 35.0 ) {
            triggerSFB=0.0242333358365; triggerSFBunc=0.00757259539495;
            triggerSFCDEF=0.974505384769; triggerSFCDEFunc=0.003957690118;
            }
        else if (leppt >=35.0 &&  leppt< 40.0 ) {
            triggerSFB=0.0364588464917; triggerSFBunc=0.00924488272953;
            triggerSFCDEF=0.983399145478; triggerSFCDEFunc=0.0036271475697;
            }
        else if (leppt >=40.0 &&  leppt< 45.0 ) {
            triggerSFB=0.0155568004374; triggerSFBunc=0.00630250726765;
            triggerSFCDEF=0.988333635773; triggerSFCDEFunc=0.0033581107186;
            }
        else if (leppt >=45.0 &&  leppt< 50.0 ) {
            triggerSFB=0.0601735535178; triggerSFBunc=0.0127378687507;
            triggerSFCDEF=0.992949384645; triggerSFCDEFunc=0.00318012878697;
            }
        else if (leppt >=50.0 &&  leppt< 60.0 ) {
            triggerSFB=0.957992262221; triggerSFBunc=0.00904323273559;
            triggerSFCDEF=1.01031349539; triggerSFCDEFunc=0.000642798495817;
            }
        else if (leppt >=60.0 &&  leppt< 70.0 ) {
            triggerSFB=1.01130851753; triggerSFBunc=0.000512750896517;
            triggerSFCDEF=1.01130851753; triggerSFCDEFunc=0.000512750896517;
            }
        else if (leppt >=70.0 &&  leppt< 100.0 ) {
            triggerSFB=1.00991777123; triggerSFBunc=0.000970190328605;
            triggerSFCDEF=1.01036170337; triggerSFCDEFunc=0.000413700942763;
            }
        else if (leppt >=100.0 &&  leppt< 200.0 ) {
            triggerSFB=1.0108606672; triggerSFBunc=0.000911109504948;
            triggerSFCDEF=1.00777390206; triggerSFCDEFunc=0.000720296322595;
            }
        else {
            triggerSFB=1.01283446282; triggerSFBunc=0.000745881092977;
            triggerSFCDEF=1.00696862616; triggerSFCDEFunc=0.00184408341266;
            }
	  }
	  else if (fabs(lepeta) < 1.20){
	    if (leppt >=20.0 &&  leppt< 25.0 ) {
	        triggerSFB=0.0662842747267; triggerSFBunc=0.0453330771566;
            triggerSFCDEF=1.01637074529; triggerSFCDEFunc=0.00393276265789;
	        }
        else if (leppt >=25.0 &&  leppt< 30.0 ) {
            triggerSFB=0.0226119816607; triggerSFBunc=0.0158144284011;
            triggerSFCDEF=0.975331610131; triggerSFCDEFunc=0.00818431789788;
            }
        else if (leppt >=30.0 &&  leppt< 35.0 ) {
            triggerSFB=0.0690721943662; triggerSFBunc=0.0252132107011;
            triggerSFCDEF=0.969696033218; triggerSFCDEFunc=0.00786836176121;
            }
        else if (leppt >=35.0 &&  leppt< 40.0 ) {
            triggerSFB=0.0184541200508; triggerSFBunc=0.0129309814826;
            triggerSFCDEF=0.999875784844; triggerSFCDEFunc=0.00565894518267;
            }
        else if (leppt >=40.0 &&  leppt< 45.0 ) {
            triggerSFB=0.00987116596908; triggerSFBunc=0.00982314053155;
            triggerSFCDEF=0.972470985489; triggerSFCDEFunc=0.00734148819756;
            }
        else if (leppt >=45.0 &&  leppt< 50.0 ) {
            triggerSFB=0.0912843448139; triggerSFBunc=0.0329179690396;
            triggerSFCDEF=0.995205263009; triggerSFCDEFunc=0.00563888825035;
            }
        else if (leppt >=50.0 &&  leppt< 60.0 ) {
            triggerSFB=0.931375691137; triggerSFBunc=0.0213959361471;
            triggerSFCDEF=1.0060230931; triggerSFCDEFunc=0.00160633294093;
            }
        else if (leppt >=60.0 &&  leppt< 70.0 ) {
            triggerSFB=0.987840495689; triggerSFBunc=0.0121230178352;
            triggerSFCDEF=1.00900850631; triggerSFCDEFunc=0.000878347086976;
            }
        else if (leppt >=70.0 &&  leppt< 100.0 ) {
            triggerSFB=0.997989070224; triggerSFBunc=0.00729585751033;
            triggerSFCDEF=1.00992616194; triggerSFCDEFunc=0.00164676851791;
            }
        else if (leppt >=100.0 &&  leppt< 200.0 ) {
            triggerSFB=0.987291487084; triggerSFBunc=0.00865733825407;
            triggerSFCDEF=0.997323789347; triggerSFCDEFunc=0.00229167095156;
            }
        else {
            triggerSFB=1.01043951474; triggerSFBunc=0.00142459194722;
            triggerSFCDEF=1.01043951474; triggerSFCDEFunc=0.00142459194722;
            }
	  }
	  else if (fabs(lepeta) < 2.0){
	    if (leppt >=20.0 &&  leppt< 25.0 ) {
	        triggerSFB=0.121788408593; triggerSFBunc=0.0404492057733;
            triggerSFCDEF=1.00901933462; triggerSFCDEFunc=0.00522124464452;
	        }
        else if (leppt >=25.0 &&  leppt< 30.0 ) {
            triggerSFB=0.0212654325135; triggerSFBunc=0.010525396768;
            triggerSFCDEF=0.981013066271; triggerSFCDEFunc=0.00655696986969;
            }
        else if (leppt >=30.0 &&  leppt< 35.0 ) {
            triggerSFB=0.0283166962203; triggerSFBunc=0.0124904631503;
            triggerSFCDEF=0.98580551783; triggerSFCDEFunc=0.0058122300255;
            }
        else if (leppt >=35.0 &&  leppt< 40.0 ) {
            triggerSFB=0.0205248452988; triggerSFBunc=0.0101603667217;
            triggerSFCDEF=1.00222957851; triggerSFCDEFunc=0.00489449557235;
            }
        else if (leppt >=40.0 &&  leppt< 45.0 ) {
            triggerSFB=0.0243099947572; triggerSFBunc=0.0120112097715;
            triggerSFCDEF=0.995440124982; triggerSFCDEFunc=0.0054771344018;
            }
        else if (leppt >=45.0 &&  leppt< 50.0 ) {
            triggerSFB=0.131546794772; triggerSFBunc=0.025617977044;
            triggerSFCDEF=1.00512489719; triggerSFCDEFunc=0.00475681380405;
            }
        else if (leppt >=50.0 &&  leppt< 60.0 ) {
            triggerSFB=0.935871664822; triggerSFBunc=0.0169195527249;
            triggerSFCDEF=1.01761118339; triggerSFCDEFunc=0.00113936544648;
            }
        else if (leppt >=60.0 &&  leppt< 70.0 ) {
            triggerSFB=0.999506866986; triggerSFBunc=0.00838698960941;
            triggerSFCDEF=1.0134981693; triggerSFCDEFunc=0.00103420313813;
            }
        else if (leppt >=70.0 &&  leppt< 100.0 ) {
            triggerSFB=1.00763676579; triggerSFBunc=0.00382256649265;
            triggerSFCDEF=1.01163709462; triggerSFCDEFunc=0.00114370618974;
            }
        else if (leppt >=100.0 &&  leppt< 200.0 ) {
            triggerSFB=1.00830247462; triggerSFBunc=0.00383384346238;
            triggerSFCDEF=1.00495678228; triggerSFCDEFunc=0.00175352328092;
            }
        else {
            triggerSFB=0.997308629862; triggerSFBunc=0.0155221884374;
            triggerSFCDEF=1.00620582422; triggerSFCDEFunc=0.00360278358703;
            }
	  }
	  else{
         if (leppt >=20.0 &&  leppt< 25.0 ) {
            triggerSFB=0.121788408593; triggerSFBunc=0.0404492057733;
            triggerSFCDEF=1.00901933462; triggerSFCDEFunc=0.00522124464452;
            }
         else if (leppt >=25.0 &&  leppt< 30.0 ) {
            triggerSFB=0.0212654325135; triggerSFBunc=0.010525396768;
            triggerSFCDEF=0.981013066271; triggerSFCDEFunc=0.00655696986969;
            }
         else if (leppt >=30.0 &&  leppt< 35.0 ) {
            triggerSFB=0.0283166962203; triggerSFBunc=0.0124904631503;
            triggerSFCDEF=0.98580551783; triggerSFCDEFunc=0.0058122300255;
            }
         else if (leppt >=35.0 &&  leppt< 40.0 ) {
            triggerSFB=0.0205248452988; triggerSFBunc=0.0101603667217;
            triggerSFCDEF=1.00222957851; triggerSFCDEFunc=0.00489449557235;
            }
         else if (leppt >=40.0 &&  leppt< 45.0 ) {
            triggerSFB=0.0243099947572; triggerSFBunc=0.0120112097715;
            triggerSFCDEF=0.995440124982; triggerSFCDEFunc=0.0054771344018;
            }
         else if (leppt >=45.0 &&  leppt< 50.0 ) {
            triggerSFB=0.131546794772; triggerSFBunc=0.025617977044;
            triggerSFCDEF=1.00512489719; triggerSFCDEFunc=0.00475681380405;
            }
         else if (leppt >=50.0 &&  leppt< 60.0 ) {
            triggerSFB=0.935871664822; triggerSFBunc=0.0169195527249;
            triggerSFCDEF=1.01761118339; triggerSFCDEFunc=0.00113936544648;
            }
         else if (leppt >=60.0 &&  leppt< 70.0 ) {
            triggerSFB=0.999506866986; triggerSFBunc=0.00838698960941;
            triggerSFCDEF=1.0134981693; triggerSFCDEFunc=0.00103420313813;
            }
         else if (leppt >=70.0 &&  leppt< 100.0 ) {
            triggerSFB=1.00763676579; triggerSFBunc=0.00382256649265;
            triggerSFCDEF=1.01163709462; triggerSFCDEFunc=0.00114370618974;
            }
         else if (leppt >=100.0 &&  leppt< 200.0 ) {
            triggerSFB=1.00830247462; triggerSFBunc=0.00383384346238;
            triggerSFCDEF=1.00495678228; triggerSFCDEFunc=0.00175352328092;
            }
         else {
            triggerSFB=0.997308629862; triggerSFBunc=0.0155221884374;
            triggerSFCDEF=1.00620582422; triggerSFCDEFunc=0.00360278358703;
            }
	  }
	  if (triggerSFB < 0.1){
	  triggerSF = triggerSFCDEF;
	  triggerSFUncert = triggerSFCDEFunc;
	  }
	  else{
	  triggerSF = (4.823*triggerSFB + 36.734*triggerSFCDEF)/41.557;
	  triggerSFUncert = sqrt( pow(4.823*triggerSFBunc/41.557,2) + pow(36.734*triggerSFCDEFunc/41.557,2) );
	  }

	return triggerSF;

}

double HardcodedConditions::GetMuonTriggerXSF2018(double leppt, double lepeta)
{
	float triggerSF18 = 1.0;
	float triggerSF18Uncert = 1.0;
	if (fabs(lepeta) < 0.9){
		if (leppt >=20.0 &&  leppt< 25.0 ) {triggerSF18=0.987417939948; triggerSF18Uncert=0.00251362731945; }
        else if (leppt >=25.0 &&  leppt< 30.0 ) {triggerSF18=0.917141370412; triggerSF18Uncert=0.00429435321593; }
        else if (leppt >=30.0 &&  leppt< 35.0 ) {triggerSF18=0.946444021444; triggerSF18Uncert=0.00340050502629; }
        else if (leppt >=35.0 &&  leppt< 40.0 ) {triggerSF18=0.966553376455; triggerSF18Uncert=0.002971455577; }
        else if (leppt >=40.0 &&  leppt< 45.0 ) {triggerSF18=0.970691584144; triggerSF18Uncert=0.00293105430144; }
        else if (leppt >=45.0 &&  leppt< 50.0 ) {triggerSF18=0.983126243357; triggerSF18Uncert=0.00260347852603; }
        else if (leppt >=50.0 &&  leppt< 60.0 ) {triggerSF18=1.00830171939; triggerSF18Uncert=0.000553130869919; }
        else if (leppt >=60.0 &&  leppt< 70.0 ) {triggerSF18=1.00797984647; triggerSF18Uncert=0.000683459180841; }
        else if (leppt >=70.0 &&  leppt< 100.0 ) {triggerSF18=1.00823278299; triggerSF18Uncert=0.00044400015482; }
        else if (leppt >=100.0 &&  leppt< 200.0 ) {triggerSF18=1.0056714938; triggerSF18Uncert=0.00057478904892; }
        else {triggerSF18=1.00711097369; triggerSF18Uncert=0.0013107920744; }
	  }
	else if (fabs(lepeta) < 1.2){
        if (leppt >=20.0 &&  leppt< 25.0 ) {triggerSF18=0.976441901891; triggerSF18Uncert=0.00490331927403; }
        else if (leppt >=25.0 &&  leppt< 30.0 ) {triggerSF18=0.946751382153; triggerSF18Uncert=0.00670382249721; }
        else if (leppt >=30.0 &&  leppt< 35.0 ) {triggerSF18=0.962123712952; triggerSF18Uncert=0.00561105901647; }
        else if (leppt >=35.0 &&  leppt< 40.0 ) {triggerSF18=0.969840528002; triggerSF18Uncert=0.00527517900409; }
        else if (leppt >=40.0 &&  leppt< 45.0 ) {triggerSF18=0.963741770557; triggerSF18Uncert=0.00575801824799; }
        else if (leppt >=45.0 &&  leppt< 50.0 ) {triggerSF18=0.974243421361; triggerSF18Uncert=0.00494357669008; }
        else if (leppt >=50.0 &&  leppt< 60.0 ) {triggerSF18=1.00335772265; triggerSF18Uncert=0.000818561291688; }
        else if (leppt >=60.0 &&  leppt< 70.0 ) {triggerSF18=1.00459639791; triggerSF18Uncert=0.000851333503311; }
        else if (leppt >=70.0 &&  leppt< 100.0 ) {triggerSF18=1.00353653555; triggerSF18Uncert=0.00046503525718; }
        else if (leppt >=100.0 &&  leppt< 200.0 ) {triggerSF18=1.00304760188; triggerSF18Uncert=0.000778596944384; }
        else  {triggerSF18=0.999234385181; triggerSF18Uncert=0.00273653748279; }
	  }
	else if (fabs(lepeta) < 2.0){
	    if (leppt >=20.0 &&  leppt< 25.0 ) {triggerSF18=0.991590058833; triggerSF18Uncert=0.00351725974429; }
        else if (leppt >=25.0 &&  leppt< 30.0 ) {triggerSF18=0.916031418308; triggerSF18Uncert=0.00543097323382; }
        else if (leppt >=30.0 &&  leppt< 35.0 ) {triggerSF18=0.958609376918; triggerSF18Uncert=0.00439944564197; }
        else if (leppt >=35.0 &&  leppt< 40.0 ) {triggerSF18=0.97337282064; triggerSF18Uncert=0.00398436515741; }
        else if (leppt >=40.0 &&  leppt< 45.0 ) {triggerSF18=0.97295186263; triggerSF18Uncert=0.00417315471136; }
        else if (leppt >=45.0 &&  leppt< 50.0 ) {triggerSF18=0.98893432467; triggerSF18Uncert=0.00351110170968; }
        else if (leppt >=50.0 &&  leppt< 60.0 ) {triggerSF18=1.00830673332; triggerSF18Uncert=0.000720108711652; }
        else if (leppt >=60.0 &&  leppt< 70.0 ) {triggerSF18=1.00640337992; triggerSF18Uncert=0.000926568415299; }
        else if (leppt >=70.0 &&  leppt< 100.0 ) {triggerSF18=1.00928008959; triggerSF18Uncert=0.00136812990457; }
        else if (leppt >=100.0 &&  leppt< 200.0 ) {triggerSF18=1.00704811071; triggerSF18Uncert=0.000851600138819; }
        else  {triggerSF18=1.00360554222; triggerSF18Uncert=0.00159942722987; }
	  }
	else{
        if (leppt >=20.0 &&  leppt< 25.0 ) {triggerSF18=0.991590058833; triggerSF18Uncert=0.00351725974429; }
        else if (leppt >=25.0 &&  leppt< 30.0 ) {triggerSF18=0.916031418308; triggerSF18Uncert=0.00543097323382; }
        else if (leppt >=30.0 &&  leppt< 35.0 ) {triggerSF18=0.958609376918; triggerSF18Uncert=0.00439944564197; }
        else if (leppt >=35.0 &&  leppt< 40.0 ) {triggerSF18=0.97337282064; triggerSF18Uncert=0.00398436515741; }
        else if (leppt >=40.0 &&  leppt< 45.0 ) {triggerSF18=0.97295186263; triggerSF18Uncert=0.00417315471136; }
        else if (leppt >=45.0 &&  leppt< 50.0 ) {triggerSF18=0.98893432467; triggerSF18Uncert=0.00351110170968; }
        else if (leppt >=50.0 &&  leppt< 60.0 ) {triggerSF18=1.00830673332; triggerSF18Uncert=0.000720108711652; }
        else if (leppt >=60.0 &&  leppt< 70.0 ) {triggerSF18=1.00640337992; triggerSF18Uncert=0.000926568415299; }
        else if (leppt >=70.0 &&  leppt< 100.0 ) {triggerSF18=1.00928008959; triggerSF18Uncert=0.00136812990457; }
        else if (leppt >=100.0 &&  leppt< 200.0 ) {triggerSF18=1.00704811071; triggerSF18Uncert=0.000851600138819; }
        else {triggerSF18=1.00360554222; triggerSF18Uncert=0.00159942722987; }
	 }

	return triggerSF18;
}




/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|                PILEUP WEIGHT SECTION                |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

void HardcodedConditions::GetPileupWeight(int nTrueInt, float *pileupweight, float *pileupweightup, float *pileupweightdn, int year, std::string sample)
{
  //The main getter for Pileup Weight Factors
  *pileupweight   = 1.000;
  *pileupweightup = 1.000;
  *pileupweightdn = 1.000;
  if      (year=="2016APV") GetPileupWeight2016APV(nTrueInt, pileupweight, pileupweightup, pileupweightdn);
  else if (year=="2016") GetPileupWeight2016(nTrueInt, pileupweight, pileupweightup, pileupweightdn);
  else if (year=="2017") GetPileupWeight2017(nTrueInt, pileupweight, pileupweightup, pileupweightdn);
  else if (year=="2018") GetPileupWeight2018(nTrueInt, pileupweight, pileupweightup, pileupweightdn);
}//end GetPileupWeight

void HardcodedConditions::GetPileupWeight2016APV(int nTrueInt, float *pileupweight, float *pileupweightup, float *pileupweightdn){
  std::vector<float> puWeights;
  std::vector<float> puWeightsUP;
  std::vector<float> puWeightsDN;
  puWeights = { 2.397e-013.821e-01, 8.494e-01, 9.920e-01, 1.410e+00, 1.914e+00, 1.843e+00, 1.394e+00, 1.224e+00, 1.179e+00, 1.148e+00, 1.106e+00, 1.074e+00, 1.061e+00, 1.064e+00, 1.080e+00, 1.095e+00, 1.108e+00, 1.113e+00, 1.108e+00, 1.093e+00, 1.076e+00, 1.060e+00, 1.043e+00, 1.022e+00, 9.931e-01, 9.562e-01, 9.136e-01, 8.692e-01, 8.256e-01, 7.834e-01, 7.458e-01, 7.153e-01, 6.907e-01, 6.691e-01, 6.482e-01, 6.306e-01, 6.133e-01, 5.994e-01, 5.878e-01, 5.787e-01, 5.755e-01, 5.819e-01, 5.995e-01, 6.315e-01, 6.620e-01, 7.046e-01, 7.595e-01, 7.931e-01, 8.048e-01, 7.812e-01, 7.440e-01, 6.529e-01, 5.750e-01, 4.733e-01, 3.377e-01, 2.626e-01, 1.636e-01, 1.399e-01, 1.056e-01, 7.550e-02, 6.081e-02, 5.766e-02, 4.566e-02, 2.463e-02, 1.594e-02, 2.412e-02, 1.644e-02, 1.071e-02, 3.100e-02, 4.764e-02, 4.368e-03, 4.237e-03, 2.459e-02, 8.440e-03, 6.855e-04, 4.173e-03, 1.446e-03, 1.000e+00, 2.368e-04, 2.251e-05, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00,  };
  puWeightsUP = { 0.2093.285e-01, 7.532e-01, 8.673e-01, 1.122e+00, 1.371e+00, 1.464e+00, 1.148e+00, 9.557e-01, 9.038e-01, 8.933e-01, 8.800e-01, 8.663e-01, 8.626e-01, 8.745e-01, 9.101e-01, 9.563e-01, 9.991e-01, 1.031e+00, 1.051e+00, 1.057e+00, 1.057e+00, 1.057e+00, 1.061e+00, 1.063e+00, 1.061e+00, 1.052e+00, 1.036e+00, 1.015e+00, 9.911e-01, 9.651e-01, 9.417e-01, 9.261e-01, 9.194e-01, 9.194e-01, 9.243e-01, 9.381e-01, 9.566e-01, 9.843e-01, 1.020e+00, 1.063e+00, 1.123e+00, 1.207e+00, 1.323e+00, 1.484e+00, 1.658e+00, 1.883e+00, 2.166e+00, 2.415e+00, 2.618e+00, 2.715e+00, 2.762e+00, 2.587e+00, 2.425e+00, 2.117e+00, 1.590e+00, 1.290e+00, 8.276e-01, 7.187e-01, 5.420e-01, 3.820e-01, 3.005e-01, 2.773e-01, 2.144e-01, 1.138e-01, 7.318e-02, 1.113e-01, 7.708e-02, 5.143e-02, 1.533e-01, 2.440e-01, 2.326e-02, 2.351e-02, 1.425e-01, 5.120e-02, 4.361e-03, 2.790e-02, 1.018e-02, 1.000e+00, 1.860e-03, 1.874e-04, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00,  };
  puWeightsDN = { 0.2774.471e-01, 9.617e-01, 1.150e+00, 1.867e+00, 2.665e+00, 2.280e+00, 1.741e+00, 1.608e+00, 1.551e+00, 1.476e+00, 1.393e+00, 1.339e+00, 1.310e+00, 1.285e+00, 1.256e+00, 1.228e+00, 1.206e+00, 1.180e+00, 1.150e+00, 1.115e+00, 1.078e+00, 1.040e+00, 9.982e-01, 9.488e-01, 8.930e-01, 8.319e-01, 7.699e-01, 7.110e-01, 6.568e-01, 6.067e-01, 5.612e-01, 5.210e-01, 4.844e-01, 4.489e-01, 4.137e-01, 3.808e-01, 3.490e-01, 3.204e-01, 2.944e-01, 2.711e-01, 2.518e-01, 2.376e-01, 2.282e-01, 2.240e-01, 2.186e-01, 2.165e-01, 2.171e-01, 2.108e-01, 1.990e-01, 1.800e-01, 1.604e-01, 1.324e-01, 1.107e-01, 8.767e-02, 6.112e-02, 4.728e-02, 2.979e-02, 2.609e-02, 2.027e-02, 1.489e-02, 1.223e-02, 1.168e-02, 9.196e-03, 4.876e-03, 3.073e-03, 4.496e-03, 2.948e-03, 1.840e-03, 5.084e-03, 7.444e-03, 6.488e-04, 5.967e-04, 3.276e-03, 1.062e-03, 8.119e-05, 4.642e-04, 1.507e-04, 1.000e+00, 2.149e-05, 1.899e-06, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00,  };
  *pileupweight = puWeights[nTrueInt];
  *pileupweightup = puWeightsUP[nTrueInt];
  *pileupweightdn = puWeightsDN[nTrueInt];
}

void HardcodedConditions::GetPileupWeight2016(int nTrueInt, float *pilieupweight, float *pileupweightup, float *pileupweightdn){
  std::vector<float> puWeights;
  std::vector<float> puWeightsUP;
  std::vector<float> puWeightsDN;
  puWeights = { 2.777e-013.416e-01, 9.148e-01, 6.970e-01, 6.332e-01, 3.420e-01, 1.601e-01, 1.107e-01, 1.110e-01, 1.298e-01, 2.317e-01, 3.666e-01, 4.856e-01, 5.667e-01, 6.208e-01, 6.691e-01, 7.154e-01, 7.568e-01, 7.916e-01, 8.241e-01, 8.593e-01, 9.024e-01, 9.530e-01, 1.007e+00, 1.061e+00, 1.119e+00, 1.182e+00, 1.252e+00, 1.327e+00, 1.406e+00, 1.483e+00, 1.559e+00, 1.637e+00, 1.719e+00, 1.799e+00, 1.874e+00, 1.952e+00, 2.023e+00, 2.094e+00, 2.158e+00, 2.209e+00, 2.254e+00, 2.302e+00, 2.353e+00, 2.414e+00, 2.414e+00, 2.403e+00, 2.376e+00, 2.236e+00, 2.016e+00, 1.721e+00, 1.440e+00, 1.119e+00, 8.937e-01, 6.946e-01, 4.945e-01, 4.086e-01, 2.864e-01, 2.870e-01, 2.588e-01, 2.213e-01, 2.108e-01, 2.322e-01, 2.096e-01, 1.267e-01, 9.046e-02, 1.493e-01, 1.101e-01, 7.696e-02, 2.375e-01, 3.877e-01, 3.761e-02, 3.847e-02, 2.349e-01, 8.472e-02, 7.223e-03, 4.613e-02, 1.677e-02, 1.000e+00, 3.035e-03, 3.042e-04, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00,  };
  puWeightsUP = { 0.2442.895e-01, 8.507e-01, 6.287e-01, 5.801e-01, 3.108e-01, 1.482e-01, 8.596e-02, 8.725e-02, 8.356e-02, 1.354e-01, 2.315e-01, 3.370e-01, 4.227e-01, 4.849e-01, 5.420e-01, 6.015e-01, 6.600e-01, 7.097e-01, 7.512e-01, 7.898e-01, 8.330e-01, 8.872e-01, 9.515e-01, 1.020e+00, 1.091e+00, 1.168e+00, 1.254e+00, 1.353e+00, 1.464e+00, 1.583e+00, 1.711e+00, 1.856e+00, 2.017e+00, 2.192e+00, 2.381e+00, 2.596e+00, 2.833e+00, 3.107e+00, 3.415e+00, 3.757e+00, 4.151e+00, 4.624e+00, 5.188e+00, 5.872e+00, 6.512e+00, 7.209e+00, 7.941e+00, 8.324e+00, 8.334e+00, 7.850e+00, 7.154e+00, 5.939e+00, 4.916e+00, 3.802e+00, 2.572e+00, 1.935e+00, 1.204e+00, 1.071e+00, 8.760e-01, 7.022e-01, 6.477e-01, 7.100e-01, 6.503e-01, 4.040e-01, 2.992e-01, 5.151e-01, 3.973e-01, 2.913e-01, 9.443e-01, 1.620e+00, 1.653e-01, 1.779e-01, 1.143e+00, 4.338e-01, 3.892e-02, 2.616e-01, 1.001e-01, 1.000e+00, 2.006e-02, 2.116e-03, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00,  };
  puWeightsDN = { 0.3184.258e-01, 9.716e-01, 7.741e-01, 6.967e-01, 3.742e-01, 1.778e-01, 1.522e-01, 1.457e-01, 2.259e-01, 3.930e-01, 5.612e-01, 6.782e-01, 7.453e-01, 7.832e-01, 8.108e-01, 8.320e-01, 8.521e-01, 8.736e-01, 9.006e-01, 9.345e-01, 9.723e-01, 1.010e+00, 1.048e+00, 1.087e+00, 1.130e+00, 1.175e+00, 1.219e+00, 1.261e+00, 1.298e+00, 1.325e+00, 1.344e+00, 1.357e+00, 1.363e+00, 1.359e+00, 1.341e+00, 1.313e+00, 1.270e+00, 1.217e+00, 1.151e+00, 1.072e+00, 9.884e-01, 9.062e-01, 8.273e-01, 7.549e-01, 6.707e-01, 5.935e-01, 5.237e-01, 4.440e-01, 3.665e-01, 2.944e-01, 2.409e-01, 1.926e-01, 1.668e-01, 1.463e-01, 1.189e-01, 1.104e-01, 8.405e-02, 8.803e-02, 8.028e-02, 6.778e-02, 6.272e-02, 6.644e-02, 5.730e-02, 3.293e-02, 2.232e-02, 3.492e-02, 2.436e-02, 1.612e-02, 4.705e-02, 7.261e-02, 6.661e-03, 6.443e-03, 3.720e-02, 1.269e-02, 1.022e-03, 6.173e-03, 2.121e-03, 1.000e+00, 3.426e-04, 3.240e-05, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00,  };
  *pileupweight = puWeights[nTrueInt];
  *pileupweightup = puWeightsUP[nTrueInt];
  *pileupweightdn = puWeightsDN[nTrueInt]; 
}

void HardcodedConditions::GetPileupWeight2017(int nTrueInt, float *pileupweight, float *pileupweightup, float *pileupweightdn){
  std::vector<float> puWeights;
  std::vector<float> puWeightsUP;
  std::vector<float> puWeightsDN;
  puWeights = { 5.606e-017.357e-01, 5.379e-01, 1.218e+00, 8.023e-01, 9.163e-01, 1.004e+00, 9.252e-01, 6.847e-01, 7.132e-01, 7.505e-01, 8.165e-01, 8.377e-01, 8.464e-01, 8.440e-01, 8.439e-01, 8.666e-01, 8.930e-01, 9.180e-01, 9.358e-01, 9.556e-01, 9.721e-01, 9.812e-01, 9.832e-01, 9.781e-01, 9.760e-01, 9.766e-01, 9.827e-01, 9.904e-01, 9.981e-01, 1.008e+00, 1.019e+00, 1.030e+00, 1.044e+00, 1.053e+00, 1.061e+00, 1.068e+00, 1.071e+00, 1.070e+00, 1.061e+00, 1.043e+00, 1.029e+00, 1.011e+00, 9.898e-01, 9.667e-01, 9.597e-01, 9.605e-01, 9.726e-01, 9.860e-01, 1.020e+00, 1.080e+00, 1.131e+00, 1.175e+00, 1.206e+00, 1.189e+00, 1.175e+00, 1.153e+00, 1.139e+00, 1.149e+00, 1.186e+00, 1.230e+00, 1.284e+00, 1.348e+00, 1.415e+00, 1.489e+00, 1.564e+00, 1.761e+00, 2.497e+00, 3.605e+00, 3.510e+00, 5.546e+00, 1.647e+01, 3.021e+01, 1.596e+02, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00,  };
  puWeightsUP = { 0.5286.444e-01, 4.356e-01, 1.233e+00, 6.813e-01, 8.174e-01, 9.700e-01, 8.474e-01, 5.507e-01, 4.611e-01, 5.343e-01, 5.670e-01, 6.342e-01, 6.532e-01, 6.458e-01, 6.380e-01, 6.526e-01, 6.895e-01, 7.374e-01, 7.766e-01, 8.149e-01, 8.511e-01, 8.780e-01, 8.934e-01, 8.957e-01, 8.962e-01, 9.014e-01, 9.178e-01, 9.408e-01, 9.671e-01, 9.964e-01, 1.027e+00, 1.058e+00, 1.094e+00, 1.127e+00, 1.155e+00, 1.177e+00, 1.190e+00, 1.193e+00, 1.177e+00, 1.139e+00, 1.090e+00, 1.023e+00, 9.496e-01, 8.837e-01, 8.498e-01, 8.451e-01, 8.750e-01, 9.323e-01, 1.038e+00, 1.204e+00, 1.400e+00, 1.628e+00, 1.877e+00, 2.078e+00, 2.299e+00, 2.510e+00, 2.738e+00, 3.021e+00, 3.379e+00, 3.761e+00, 4.178e+00, 4.621e+00, 5.073e+00, 5.533e+00, 5.970e+00, 6.840e+00, 9.786e+00, 1.413e+01, 1.366e+01, 2.133e+01, 6.250e+01, 1.131e+02, 5.917e+02, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00,  };
  puWeightsDN = { 0.5988.077e-01, 7.068e-01, 1.168e+00, 9.349e-01, 1.015e+00, 1.047e+00, 1.035e+00, 9.934e-01, 1.062e+00, 1.098e+00, 1.138e+00, 1.099e+00, 1.116e+00, 1.127e+00, 1.137e+00, 1.145e+00, 1.131e+00, 1.120e+00, 1.108e+00, 1.099e+00, 1.092e+00, 1.084e+00, 1.078e+00, 1.069e+00, 1.059e+00, 1.045e+00, 1.031e+00, 1.016e+00, 1.002e+00, 9.908e-01, 9.804e-01, 9.691e-01, 9.613e-01, 9.547e-01, 9.521e-01, 9.538e-01, 9.587e-01, 9.719e-01, 9.945e-01, 1.026e+00, 1.073e+00, 1.111e+00, 1.125e+00, 1.103e+00, 1.065e+00, 1.004e+00, 9.338e-01, 8.524e-01, 7.841e-01, 7.322e-01, 6.749e-01, 6.183e-01, 5.626e-01, 4.956e-01, 4.420e-01, 3.956e-01, 3.605e-01, 3.390e-01, 3.295e-01, 3.249e-01, 3.259e-01, 3.318e-01, 3.417e-01, 3.562e-01, 3.744e-01, 4.249e-01, 6.109e-01, 8.951e-01, 8.834e-01, 1.409e+00, 4.197e+00, 7.666e+00, 4.005e+01, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00,  };
  *pileupweight = puWeights[nTrueInt];
  *pileupweightup = puWeightsUP[nTrueInt];
  *pileupweightdn = puWeightsDN[nTrueInt];
}

void HardcodedConditions::GetPileupWeight2018(int nTrueInt, float *pileupweight, float *pileupweightup, float *pileupweightdn){
  std::vector<float> puWeights;
  std::vector<float> puWeightsUP;
  std::vector<float> puWeightsDN;
  puWeights = { 4.760e+001.081e+00, 1.217e+00, 8.809e-01, 7.662e-01, 1.012e+00, 1.323e+00, 1.340e+00, 1.105e+00, 9.124e-01, 8.241e-01, 8.004e-01, 7.908e-01, 8.068e-01, 8.324e-01, 8.564e-01, 8.725e-01, 8.821e-01, 8.947e-01, 9.187e-01, 9.464e-01, 9.664e-01, 9.802e-01, 9.908e-01, 9.926e-01, 9.874e-01, 9.798e-01, 9.813e-01, 9.869e-01, 9.929e-01, 9.982e-01, 1.002e+00, 1.003e+00, 1.005e+00, 1.007e+00, 1.009e+00, 1.012e+00, 1.016e+00, 1.021e+00, 1.028e+00, 1.037e+00, 1.047e+00, 1.058e+00, 1.071e+00, 1.082e+00, 1.095e+00, 1.110e+00, 1.126e+00, 1.142e+00, 1.155e+00, 1.168e+00, 1.177e+00, 1.183e+00, 1.200e+00, 1.197e+00, 1.195e+00, 1.192e+00, 1.209e+00, 1.219e+00, 1.240e+00, 1.253e+00, 1.239e+00, 1.171e+00, 1.082e+00, 1.007e+00, 9.125e-01, 8.601e-01, 7.821e-01, 6.576e-01, 6.309e-01, 5.988e-01, 7.141e-01, 7.152e-01, 5.360e-01, 4.091e-01, 4.283e-01, 4.417e-01, 4.424e-01, 1.035e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00,  };
  puWeightsUP = { 4.4279.470e-01, 1.017e+00, 7.567e-01, 6.606e-01, 8.755e-01, 1.131e+00, 1.133e+00, 9.294e-01, 7.589e-01, 6.725e-01, 6.433e-01, 6.301e-01, 6.411e-01, 6.618e-01, 6.823e-01, 6.979e-01, 7.103e-01, 7.279e-01, 7.584e-01, 7.959e-01, 8.300e-01, 8.601e-01, 8.864e-01, 9.013e-01, 9.056e-01, 9.037e-01, 9.074e-01, 9.134e-01, 9.195e-01, 9.259e-01, 9.319e-01, 9.379e-01, 9.458e-01, 9.556e-01, 9.688e-01, 9.859e-01, 1.009e+00, 1.037e+00, 1.073e+00, 1.117e+00, 1.169e+00, 1.230e+00, 1.299e+00, 1.375e+00, 1.462e+00, 1.560e+00, 1.668e+00, 1.784e+00, 1.901e+00, 2.024e+00, 2.142e+00, 2.255e+00, 2.387e+00, 2.479e+00, 2.566e+00, 2.645e+00, 2.772e+00, 2.881e+00, 3.024e+00, 3.161e+00, 3.242e+00, 3.188e+00, 3.074e+00, 2.998e+00, 2.856e+00, 2.837e+00, 2.724e+00, 2.420e+00, 2.456e+00, 2.465e+00, 3.108e+00, 3.289e+00, 2.604e+00, 2.099e+00, 2.321e+00, 2.530e+00, 2.682e+00, 6.654e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00,  };
  puWeightsDN = { 5.1431.252e+00, 1.460e+00, 1.031e+00, 8.940e-01, 1.180e+00, 1.566e+00, 1.600e+00, 1.328e+00, 1.116e+00, 1.029e+00, 1.012e+00, 1.005e+00, 1.026e+00, 1.057e+00, 1.084e+00, 1.097e+00, 1.097e+00, 1.096e+00, 1.103e+00, 1.111e+00, 1.108e+00, 1.100e+00, 1.095e+00, 1.085e+00, 1.074e+00, 1.063e+00, 1.064e+00, 1.069e+00, 1.073e+00, 1.075e+00, 1.072e+00, 1.064e+00, 1.054e+00, 1.040e+00, 1.023e+00, 1.002e+00, 9.783e-01, 9.505e-01, 9.210e-01, 8.897e-01, 8.566e-01, 8.227e-01, 7.887e-01, 7.530e-01, 7.195e-01, 6.880e-01, 6.591e-01, 6.326e-01, 6.064e-01, 5.838e-01, 5.620e-01, 5.418e-01, 5.288e-01, 5.093e-01, 4.913e-01, 4.733e-01, 4.634e-01, 4.491e-01, 4.377e-01, 4.222e-01, 3.969e-01, 3.552e-01, 3.098e-01, 2.717e-01, 2.317e-01, 2.054e-01, 1.757e-01, 1.390e-01, 1.255e-01, 1.122e-01, 1.260e-01, 1.188e-01, 8.375e-02, 6.001e-02, 5.885e-02, 5.669e-02, 5.284e-02, 1.147e-01, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00,  };
  *pileupweight = puWeights[nTrueInt];
  *pileupweightup = puWeightsUP[nTrueInt];
  *pileupweightdn = puWeightsDN[nTrueInt];
}

/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|           Njet SF                                   |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/


float HardcodedConditions::GetNjetSF(int njet, int year, std::string variation, bool isTT)
{

if (!isTT) return 1.0;

// std::vector<float> njetSF17 =
// {1.080253774511706, 1.0623482253077383, 1.09355645604317};

// std::vector<float> njetSF17_err=
// {0.053333477794045514, 0.059333729746614994, 0.07534116157915727};

// std::vector<float> njetSF18=
// {1.04092777146488, 1.0100261031168394, 1.0108970084304671};

// std::vector<float> njetSF18_err=
// {0.0399403283162989, 0.042349665797684066, 0.04820757262016162};

std::vector<float> njetSF17 =
{1.1277934660274982, 1.102242245629874, 1.0756662016868377, 1.1090459291002919, 1.2170530772239552, 1.2377932283035988};

std::vector<float> njetSF17_err=
{0.04248003388593857, 0.046819986960960236, 0.051728530026750486, 0.0587524161035573, 0.06621128896622785, 0.08004381685037298};

std::vector<float> njetSF18=
{1.0425553892507844, 1.0136971948990172, 0.9844805605506629, 1.044627678877207, 1.0901388862059715, 1.200088823203118};

std::vector<float> njetSF18_err=
{0.03851850164109316, 0.040849713078698224, 0.04423838722090512, 0.04809850651350733, 0.05383229997672667, 0.062264381354622644};

std::vector<float> njetSF;
std::vector<float> njetSF_err;

if (year==2017){
  njetSF=njetSF17;
  njetSF_err=njetSF17_err;
} else if  (year==2018){
  njetSF=njetSF18;
  njetSF_err=njetSF18_err;
}

unsigned int iSF=0;
if (njet==4){
  iSF=0;
} else if(njet==5) {
  iSF=1;
} else if(njet==6) {
  iSF=2;
} else if(njet==7) {
  iSF=3;
} else if(njet==8) {
  iSF=4;
} else if(njet>=9) {
  iSF=5;
} else return 1.0;

if (variation=="up"){
  return njetSF[iSF]+njetSF_err[iSF];
} else if (variation=="down"){
  return njetSF[iSF]-njetSF_err[iSF];
} else {
  return njetSF[iSF];
}

}

/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|           ttHF SF                                   |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/

float HardcodedConditions::GetTtHfSF(bool isTT, bool isTTHF, bool isTTLF)
{

  if (isTT)
  {
    if (isTTHF) return 4.7/3.9; 
    if (isTTLF) return 0.989;
  }
  return 1.0;

}

/*.-----------------------------------------------------------------.
  /  .-.                                                         .-.  \
 |  /   \                                                       /   \  |
 | |\_.  |                                                     |    /| |
 |\|  | /|           btag CSV re-normalization                 |\  | |/|
 | `---' |                                                     | `---' |
 |       |                                                     |       | 
 |       |-----------------------------------------------------|       |
 \       |                                                     |       /
  \     /                                                       \     /
   `---'                                                         `---'*/


float HardcodedConditions::GetCSVRenormSF(int year, int isE, int njet, std::string sampleType) {

  if (sampleType == "")
    return 1.0;

  std::unordered_map<string, std::vector<float>> wgt2017_E = { // { type, { nj4, nj5, nj6p}}
      {"tttt", {0.9226035838, 0.9340754278, 0.9178683544}},
      {"ttjj", {1.0150106608, 1.0158690852, 0.9984062267}}, 
      {"ttcc", {1.0136943000, 1.0140899115, 0.9942071628}}, 
      {"ttbb", {0.9631111820, 0.9515052984, 0.9379830806}}, 
      {"tt1b", {0.9759196469, 0.9682610124, 0.9515214699}},
      {"tt2b", {1.0003494683, 0.9993383880, 0.9785378387}}, 
      {"T",    {0.9942575377, 0.9937236824, 0.9766816381}},    
      {"TTV",  {0.9812181248, 0.9825636826, 0.9692906190}},   
      {"TTXY", {0.9649570916, 0.9760667136, 0.9668860438}},
      {"WJets", {0.9466788783, 0.9314807852, 0.8977387072}},
      {"ZJets", {0.9238401519, 0.9142555237, 0.8754396906}},   
      {"VV",   {0.9479513385, 0.9228753647, 0.9351743323}}, 
      {"qcd",  {0.9347835971, 0.8894844256, 0.8726583653}}  
  }; 
           
  std::unordered_map<string, std::vector<float>> wgt2017_M = {
      {"tttt", {0.9433598986, 0.9272944126, 0.9110504508}},
      {"ttjj", {1.0132655222, 1.0155523211, 0.9985696550}},
      {"ttcc", {1.0136957889, 1.0156561190, 0.9926861551}},    
      {"ttbb", {0.9384948843, 0.9600479008, 0.9402875736}},   
      {"tt1b", {0.9686391123, 0.9678715509, 0.9516217613}},   
      {"tt2b", {1.0022929930, 0.9926428694, 0.9793777439}},
      {"T",    {0.9949107816, 0.9979611538, 0.9694816215}},   
      {"TTV",  {0.9845427478, 0.9879892539, 0.9598517712}}, 
      {"TTXY", {0.9755792626, 0.9659806557, 0.9643891245}},
      {"WJets", {0.9424065786, 0.9325232695, 0.9041351457}},
      {"ZJets", {0.9369363260, 0.9113343464, 0.8893352320}},
      {"VV",   {0.8981562513, 0.9607905859, 0.9578045041}}, 
      {"qcd",  {0.9525539727, 0.9176432861, 0.8539381306}} 
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
