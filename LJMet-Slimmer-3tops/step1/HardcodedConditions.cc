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

void HardcodedConditions::GetTtaggingSF2016APV(double pt, double *tau32sf, double *tau32sfup, double *tau32sfdn)
{
	// VALUES from the githup repository linked from https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetTopTagging#13_TeV_Working_Points_and_Scale
	// CORRESPONDING TO WP5 with tau32<0.80 and 105<mSD<220
    ptMins= {300,400,480,600,1100};
    tSFs   = {0.98376977,1.00090742,1.00348091,1.00204241,1.00204241};
    tSFsUp = {1.02300429,1.02958071,1.03640139,1.05011296,1.09818339};
    tSFsDn = {0.94453520,9.72234130,9.70560491,9.53971922,9.05901372};
    int bin = findBin(pt, ptMins);
    *tau32sf  =tSFs[bin];
    *tau32sfup=tSFsUp[bin];
    *tau32sfdn=tSFsDn[bin];
}

void HardcodedConditions::GetTtaggingSF2016(double pt, double *tau32sf, double *tau32sfup, double *tau32sfdn)
{
	// VALUES from the githup repository linked from https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetTopTagging#13_TeV_Working_Points_and_Scale
	// CORRESPONDING TO WP5 with tau32<0.80 and 105<mSD<220
    ptMins= {300,400,480,600,1100};
    tSFs   = {0.98376977,1.00090742,1.00348091,1.00204241,1.00204241};
    tSFsUp = {1.02300429,1.02958071,1.03640139,1.05011296,1.09818339};
    tSFsDn = {0.94453520,9.72234130,9.70560491,9.53971922,9.05901372};
    int bin = findBin(pt, ptMins);
    *tau32sf  =tSFs[bin];
    *tau32sfup=tSFsUp[bin];
    *tau32sfdn=tSFsDn[bin];
}

void HardcodedConditions::GetTtaggingSF2017(double pt, double *tau32sf, double *tau32sfup, double *tau32sfdn)
{
	// VALUES from the githup repository linked from https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetTopTagging#13_TeV_Working_Points_and_Scale
	// CORRESPONDING TO WP5 with tau32<0.80 and 105<mSD<220
    ptMins= {300,400,480,600,1100};
    tSFs   = {0.98331112,0.96821666,0.95967776,1.02111010,1.02111010};
    tSFsUp = {1.02416270,0.99713147,0.99533176,1.06593850,1.11076690};
    tSFsDn = {0.94245958,0.93930185,0.92402375,0.97628158,0.93145317};
    int bin = findBin(pt, ptMins);
    *tau32sf  =tSFs[bin];
    *tau32sfup=tSFsUp[bin];
    *tau32sfdn=tSFsDn[bin];
}

void HardcodedConditions::GetTtaggingSF2018(double pt, double *tau32sf, double *tau32sfup, double *tau32sfdn)
{
	// VALUES from the githup repository linked from https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetTopTagging#13_TeV_Working_Points_and_Scale
	// CORRESPONDING TO WP5 with tau32<0.80 and 105<mSD<220
    ptMins= {300,400,480,600};
    tSFs   = {0.99998647,1.00215673,0.99631429,0.97337210};
    tSFsUp = {1.02159548, 1.01967812, 1.01507819, 1.00174773};
    tSFsDn = {0.97837746, 0.98463523, 0.97755039, 0.94499648};
    int bin = findBin(pt, ptMins);
    *tau32sf  =tSFs[bin];
    *tau32sfup=tSFsUp[bin];
    *tau32sfdn=tSFsDn[bin];
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

void HardcodedConditions::GetTtaggingEff2016APV(double pt, double *eff, std::string sample, int massIndex)
{

	GetTtaggingEff2016(pt, eff, sample, massIndex);

}

void HardcodedConditions::GetTtaggingEff2016(double pt, double *eff, std::string sample, int massIndex)
{

	GetTtaggingEff2016(pt, eff, sample, massIndex);

}

void HardcodedConditions::GetTtaggingEff2017(double pt, double *eff, std::string sample, int massIndex)
{
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
	// Scale Factor 2: https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/tree/master/POG/EGM/2016preVFP_UL
	if ( pt < 20.0 ) {
		if ( eta < -2.0 ) return 1.023;
		else if ( eta < -1.566 ) return 1.012;
		else if ( eta < -1.444 ) return 1.000;
		else if ( eta < -1.0 ) return 1.003;
		else if ( eta < 0.0 ) return 1.003;
		else if ( eta < 1.0 ) return 0.970;
		else if ( eta < 1.444 ) return 1.021;
		else if ( eta < 1.566 ) return 1.000;
		else if ( eta < 2.0 ) return 1.007;
		else return 1.049; }
	else if ( pt < 35.0 )
	{
		if ( eta < -2.0 ) return 0.994;
		else if ( eta < -1.566 ) return 0.976;
		else if ( eta < -1.444 ) return 1.000;
		else if ( eta < -1.0 ) return 0.969;
		else if ( eta < 0.0 ) return 0.969;
		else if ( eta < 1.0 ) return 0.977;
		else if ( eta < 1.444 ) return 0.983;
		else if ( eta < 1.566 ) return 1.000;
		else if ( eta < 2.0 ) return 0.967;
		else return 0.992; }
	else if ( pt < 50.0 )
	{
		if ( eta < -2.0 ) return 0.995;
		else if ( eta < -1.566 ) return 0.985;
		else if ( eta < -1.444 ) return 1.000;
		else if ( eta < -1.0 ) return 0.979;
		else if ( eta < 0.0 ) return 0.979;
		else if ( eta < 1.0 ) return 0.976;
		else if ( eta < 1.444 ) return 0.985;
		else if ( eta < 1.566 ) return 1.000;
		else if ( eta < 2.0 ) return 0.984;
		else return 0.995; }
	else if ( pt < 100.0 )
	{
		if ( eta < -2.0 ) return 0.998;
		else if ( eta < -1.566 ) return 0.990;
		else if ( eta < -1.444 ) return 1.000;
		else if ( eta < -1.0 ) return 0.980;
		else if ( eta < 0.0 ) return 0.980;
		else if ( eta < 1.0 ) return 0.977;
		else if ( eta < 1.444 ) return 0.985;
		else if ( eta < 1.566 ) return 1.000;
		else if ( eta < 2.0 ) return 0.993;
		else return 0.995; }
	else
	{
		if ( eta < -2.0 ) return 1.015;
		else if ( eta < -1.566 ) return 1.002;
		else if ( eta < -1.444 ) return 1.000;
		else if ( eta < -1.0 ) return 0.992;
		else if ( eta < 0.0 ) return 0.992;
		else if ( eta < 1.0 ) return 0.991;
		else if ( eta < 1.444 ) return 0.995;
		else if ( eta < 1.566 ) return 1.000;
		else if ( eta < 2.0 ) return 0.987;
		else return 1.001; }
}

double HardcodedConditions::GetElectronIdSF2016(double pt, double eta){
	if ( pt < 20.0 ) {
		if ( eta < -2.0 ) return 1.021;
		else if ( eta < -1.566 ) return 0.986;
		else if ( eta < -1.444 ) return 1.000;
		else if ( eta < -1.0 ) return 0.981;
		else if ( eta < 0.0 ) return 0.981;
		else if ( eta < 1.0 ) return 0.974;
		else if ( eta < 1.444 ) return 0.984;
		else if ( eta < 1.566 ) return 1.000;
		else if ( eta < 2.0 ) return 0.980;
		else return 0.985; }
	else if ( pt < 35.0 )
	{
		if ( eta < -2.0 ) return 0.994;
		else if ( eta < -1.566 ) return 0.954;
		else if ( eta < -1.444 ) return 1.000;
		else if ( eta < -1.0 ) return 0.963;
		else if ( eta < 0.0 ) return 0.963;
		else if ( eta < 1.0 ) return 0.988;
		else if ( eta < 1.444 ) return 0.965;
		else if ( eta < 1.566 ) return 1.000;
		else if ( eta < 2.0 ) return 0.943;
		else return 0.956; }
	else if ( pt < 50.0 )
	{
		if ( eta < -2.0 ) return 1.000;
		else if ( eta < -1.566 ) return 0.968;
		else if ( eta < -1.444 ) return 1.000;
		else if ( eta < -1.0 ) return 0.969;
		else if ( eta < 0.0 ) return 0.969;
		else if ( eta < 1.0 ) return 0.992;
		else if ( eta < 1.444 ) return 0.977;
		else if ( eta < 1.566 ) return 1.000;
		else if ( eta < 2.0 ) return 0.961;
		else return 0.968; }
	else if ( pt < 100.0 )
	{
		if ( eta < -2.0 ) return 0.998;
		else if ( eta < -1.566 ) return 0.981;
		else if ( eta < -1.444 ) return 1.000;
		else if ( eta < -1.0 ) return 0.972;
		else if ( eta < 0.0 ) return 0.972;
		else if ( eta < 1.0 ) return 0.994;
		else if ( eta < 1.444 ) return 0.982;
		else if ( eta < 1.566 ) return 1.000;
		else if ( eta < 2.0 ) return 0.969;
		else return 0.978; }
	else
	{
		if ( eta < -2.0 ) return 1.069;
		else if ( eta < -1.566 ) return 1.003;
		else if ( eta < -1.444 ) return 1.000;
		else if ( eta < -1.0 ) return 1.023;
		else if ( eta < 0.0 ) return 1.023;
		else if ( eta < 1.0 ) return 1.016;
		else if ( eta < 1.444 ) return 1.000;
		else if ( eta < 1.566 ) return 1.000;
		else if ( eta < 2.0 ) return 0.986;
		else return 1.005; }
}
		
double HardcodedConditions::GetElectronIdSF2017(double pt, double eta){
	if ( pt < 20.0 ) {
		if ( eta < -2.0 ) return 0.995;
		else if ( eta < -1.566 ) return 0.961;
		else if ( eta < -1.444 ) return 1.000;
		else if ( eta < -1.0 ) return 0.987;
		else if ( eta < 0.0 ) return 0.987;
		else if ( eta < 1.0 ) return 0.977;
		else if ( eta < 1.444 ) return 0.990;
		else if ( eta < 1.566 ) return 1.000;
		else if ( eta < 2.0 ) return 0.958;
		else return 1.006; }
	else if ( pt < 35.0 )
	{
		if ( eta < -2.0 ) return 0.958;
		else if ( eta < -1.566 ) return 0.941;
		else if ( eta < -1.444 ) return 1.000;
		else if ( eta < -1.0 ) return 0.965;
		else if ( eta < 0.0 ) return 0.965;
		else if ( eta < 1.0 ) return 0.971;
		else if ( eta < 1.444 ) return 0.969;
		else if ( eta < 1.566 ) return 1.000;
		else if ( eta < 2.0 ) return 0.944;
		else return 0.959; }
	else if ( pt < 50.0 )
	{
		if ( eta < -2.0 ) return 0.973;
		else if ( eta < -1.566 ) return 0.968;
		else if ( eta < -1.444 ) return 1.000;
		else if ( eta < -1.0 ) return 0.975;
		else if ( eta < 0.0 ) return 0.975;
		else if ( eta < 1.0 ) return 0.978;
		else if ( eta < 1.444 ) return 0.977;
		else if ( eta < 1.566 ) return 1.000;
		else if ( eta < 2.0 ) return 0.970;
		else return 0.968; }
	else if ( pt < 100.0 )
	{
		if ( eta < -2.0 ) return 0.969;
		else if ( eta < -1.566 ) return 0.977;
		else if ( eta < -1.444 ) return 1.000;
		else if ( eta < -1.0 ) return 0.973;
		else if ( eta < 0.0 ) return 0.973;
		else if ( eta < 1.0 ) return 0.977;
		else if ( eta < 1.444 ) return 0.977;
		else if ( eta < 1.566 ) return 1.000;
		else if ( eta < 2.0 ) return 0.983;
		else return 0.971; }
	else
	{
		if ( eta < -2.0 ) return 0.977;
		else if ( eta < -1.566 ) return 0.979;
		else if ( eta < -1.444 ) return 1.000;
		else if ( eta < -1.0 ) return 1.003;
		else if ( eta < 0.0 ) return 1.003;
		else if ( eta < 1.0 ) return 0.991;
		else if ( eta < 1.444 ) return 0.984;
		else if ( eta < 1.566 ) return 1.000;
		else if ( eta < 2.0 ) return 0.976;
		else return 0.987; }
}

double HardcodedConditions::GetElectronIdSF2018(double pt, double eta){
if ( pt < 20.0 ) {
  if ( eta < -2.0 ) return 0.990;
  else if ( eta < -1.566 ) return 0.972;
  else if ( eta < -1.444 ) return 1.000;
  else if ( eta < -1.0 ) return 0.984;
  else if ( eta < 0.0 ) return 0.984;
  else if ( eta < 1.0 ) return 0.981;
  else if ( eta < 1.444 ) return 0.984;
  else if ( eta < 1.566 ) return 1.000;
  else if ( eta < 2.0 ) return 0.982;
  else return 0.962; }
else if ( pt < 35.0 ) {
  if ( eta < -2.0 ) return 0.959;
  else if ( eta < -1.566 ) return 0.950;
  else if ( eta < -1.444 ) return 1.000;
  else if ( eta < -1.0 ) return 0.951;
  else if ( eta < 0.0 ) return 0.951;
  else if ( eta < 1.0 ) return 0.972;
  else if ( eta < 1.444 ) return 0.953;
  else if ( eta < 1.566 ) return 1.000;
  else if ( eta < 2.0 ) return 0.944;
  else return 0.945; }
else if ( pt < 50.0 ) {
  if ( eta < -2.0 ) return 0.972;
  else if ( eta < -1.566 ) return 0.967;
  else if ( eta < -1.444 ) return 1.000;
  else if ( eta < -1.0 ) return 0.968;
  else if ( eta < 0.0 ) return 0.968;
  else if ( eta < 1.0 ) return 0.976;
  else if ( eta < 1.444 ) return 0.969;
  else if ( eta < 1.566 ) return 1.000;
  else if ( eta < 2.0 ) return 0.965;
  else return 0.961; }
else if ( pt < 100.0 ) {
  if ( eta < -2.0 ) return 0.971;
  else if ( eta < -1.566 ) return 0.975;
  else if ( eta < -1.444 ) return 1.000;
  else if ( eta < -1.0 ) return 0.968;
  else if ( eta < 0.0 ) return 0.968;
  else if ( eta < 1.0 ) return 0.975;
  else if ( eta < 1.444 ) return 0.968;
  else if ( eta < 1.566 ) return 1.000;
  else if ( eta < 2.0 ) return 0.972;
  else return 0.963; }
else {
  if ( eta < -2.0 ) return 0.998;
  else if ( eta < -1.566 ) return 0.992;
  else if ( eta < -1.444 ) return 1.000;
  else if ( eta < -1.0 ) return 0.991;
  else if ( eta < 0.0 ) return 0.991;
  else if ( eta < 1.0 ) return 0.986;
  else if ( eta < 1.444 ) return 0.988;
  else if ( eta < 1.566 ) return 1.000;
  else if ( eta < 2.0 ) return 0.984;
  else return 0.966; }
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

double HardcodedConditions::GetMuonIdSF2016(double pt, double eta)
{
	// Cut based tight id
	if (fabs(eta) < 2.10 && fabs(eta) > 1.20) {
	    if (pt < 25.0 && pt > 20.0) return 0.9924252719877384;
	    else if (pt < 60.0 && pt > 50.0) return 0.9906364222943529;
	    else if (pt < 30.0 && pt > 25.0) return 0.9890884461284933;
	    else if (pt < 120.0 && pt > 60.0) return 0.9920464322143979;
	    else if (pt < 40.0 && pt > 30.0) return 0.9946469069883841;
	    else if (pt < 50.0 && pt > 40.0) return 0.9926528825155183; }
	else if (fabs(eta) < 2.40 && pt > 2.10) {
	    if (pt < 25.0 && pt > 20.0) return 0.9758095839531763;
	    else if (pt < 60.0 && pt > 50.0) return 0.9673568416097894;
	    else if (pt < 30.0 && pt > 25.0) return 0.9745153594179884;
	    else if (pt < 120.0 && pt > 60.0) return 0.9766311856731202;
	    else if (pt < 40.0 && pt > 30.0) return 0.9787410500158746;
	    else if (pt < 50.0 && pt > 40.0) return 0.978189122919501; }
	else if (fabs(eta) < 1.20 && fabs(eta) > 0.90) {
	    if (pt < 25.0 && pt > 20.0) return 0.9927389275515244;
	    else if (pt < 60.0 && pt > 50.0) return 0.9839056384760008;
	    else if (pt < 30.0 && pt > 25.0) return 0.985063939762512;
	    else if (pt < 120.0 && pt > 60.0) return 0.984060403143468;
	    else if (pt < 40.0 && pt > 30.0) return 0.9865359464182247;
	    else if (pt < 50.0 && pt > 40.0) return 0.984913093101493; }
	else if (fabs(eta) < 0.90 && fabs(eta) > 0.0) {
	    if (pt < 25.0 && pt > 20.0) return 0.9910777627756951;
	    else if (pt < 60.0 && pt > 50.0) return 0.9855545160334763;
	    else if (pt < 30.0 && pt > 25.0) return 0.987410468262084;
	    else if (pt < 120.0 && pt > 60.0) return 0.9898057377093389;
	    else if (pt < 40.0 && pt > 30.0) return 0.9907753279135898;
	    else if (pt < 50.0 && pt > 40.0) return 0.9892483588952047; }
	else{
	  std::cerr << "The pt=" << pt << ",eta=" << eta << " range is not coded into GetMuonIdSF2016!" << std::endl;
	  return 0;}		    
}

double HardcodedConditions::GetMuonIdSF2017(double pt, double eta)
{
	// Cut based tight id
	// Scale Factor 3: https://twiki.cern.ch/twiki/pub/CMS/MuonReferenceEffs2017/RunBCDEF_SF_ID.json
	if (fabs(eta) < 0.90) {
            if(pt<20) return 0.988973745094469;
            else if(pt<25) return 0.9901639639283745;
            else if(pt<30) return 0.9894505622634719;
            else if(pt<40) return 0.9890587934386978;
            else if(pt<50) return 0.988569587464391;
            else if(pt<60) return 0.9881735800442727;
            else return 0.9871638011006827;}
	else if (fabs(eta) < 1.20) {
            if(pt<20) return 0.9838660835619908;  
            else if(pt<25) return 0.9820592893628324;
            else if(pt<30) return 0.9816256211978136;
            else if(pt<40) return 0.9826795261832795;
            else if(pt<50) return 0.9832114785473719;
            else if(pt<60) return 0.9824017821465342;
            else return 0.9826989601771537;}
	else if (fabs(eta) < 2.10) {
            if(pt<20) return 0.9897274594905875;
            else if(pt<25) return 0.9894166761673087;
            else if(pt<30) return 0.9908099250187937;
            else if(pt<40) return 0.9909172603300768;
            else if(pt<50) return 0.9913614742306379;
            else if(pt<60) return 0.9901265754533497;
            else return 0.9893528963937902;}
	else {
            if(pt<20) return 0.9729565235238601;
            else if(pt<25) return 0.9740614475300607;
            else if(pt<30) return 0.9760309076915114;
            else if(pt<40) return 0.9753358818465124;
            else if(pt<50) return 0.9752601512900863;
            else if(pt<60) return 0.970358299873981;
            else return 0.9677621936001002;}

}

double HardcodedConditions::GetMuonIdSF2018(double pt, double eta)
{
    //cut based tight id: https://gitlab.cern.ch/cms-muonPOG/MuonReferenceEfficiencies/blob/master/EfficienciesStudies/2018/jsonfiles/RunABCD_SF_ID.json
	if (fabs(eta) > 0.00 && fabs(eta) < 0.90) {
	    if (pt >20.00 && pt < 25.00) return 0.9913892461286353;
        else if (pt > 25.00 && pt < 30.00) return 0.991434774563006;
        else if (pt > 30.00 && pt < 40.00) return 0.99137555469275;
        else if (pt > 40.00 && pt < 50.00) return 0.9914412620030336;
        else if (pt > 50.00 && pt < 60.00) return 0.9916861853024751;
        else {return 0.9905799448514033;}  
        }
    else if (fabs(eta) > 0.90 && fabs(eta) < 1.20) {
        if (pt >20.00 && pt < 25.00) return 0.985987369423937;
        else if (pt > 25.00 && pt < 30.00) return 0.983987818122965;
        else if (pt > 30.00 && pt < 40.00) return 0.983823809537526;
        else if (pt > 40.00 && pt < 50.00) return 0.9842166496308641;
        else if (pt > 50.00 && pt < 60.00) return 0.9830003119378048;
        else {return 0.9816888807775153;}
        }
    else if (fabs(eta) > 1.20 && fabs(eta) < 2.10) {
        if (pt >20.00 && pt < 25.00) return 0.991472765372932;
        else if (pt > 25.00 && pt < 30.00) return 0.991184702552688;
        else if (pt > 30.00 && pt < 40.00) return 0.9907979966866818;
        else if (pt > 40.00 && pt < 50.00) return 0.98999331286624;
        else if (pt > 50.00 && pt < 60.00) return 0.9907796746368196;
        else {return 0.9886366722532979;}
        }
    else{
        if (pt >20.00 && pt < 25.00) return 0.9762336613870103;
        else if (pt > 25.00 && pt < 30.00) return 0.9735941110201962;
        else if (pt > 30.00 && pt < 40.00) return 0.973964994647057;
        else if (pt > 40.00 && pt < 50.00) return 0.9738877279555861;
        else if (pt > 50.00 && pt < 60.00) return 0.9737076412350453;
        else {return 0.9677501192438909;}
        }
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
  if      (year==2016) GetPileupWeight2016(nTrueInt, pileupweight, pileupweightup, pileupweightdn, sample);
  else if (year==2017) GetPileupWeight2017(nTrueInt, pileupweight, pileupweightup, pileupweightdn, sample);
  else if (year==2018) GetPileupWeight2018(nTrueInt, pileupweight, pileupweightup, pileupweightdn, sample);
}//end GetPileupWeight

void HardcodedConditions::GetPileupWeight2016(int nTrueInt, float *pileupweight, float *pileupweightup, float *pileupweightdn, std::string sample)
{
   // Pileup distributions -- ReReco Data vs Moriond17MC
   std::vector<float> pileupweights;
   std::vector<float> pileupweightsUp;
   std::vector<float> pileupweightsDn;
   pileupweights = {3.603e-01, 9.378e-01, 1.201e+00, 9.651e-01, 1.112e+00, 1.162e+00, 7.847e-01, 4.960e-01, 7.422e-01, 8.839e-01, 9.662e-01, 1.071e+00, 1.124e+00, 1.175e+00, 1.203e+00, 1.208e+00, 1.200e+00, 1.182e+00, 1.144e+00, 1.096e+00, 1.065e+00, 1.051e+00, 1.052e+00, 1.051e+00, 1.050e+00, 1.057e+00, 1.072e+00, 1.083e+00, 1.095e+00, 1.108e+00, 1.094e+00, 1.084e+00, 1.042e+00, 9.850e-01, 9.095e-01, 8.196e-01, 7.159e-01, 6.107e-01, 5.032e-01, 4.052e-01, 3.092e-01, 2.285e-01, 1.636e-01, 1.133e-01, 7.738e-02, 5.090e-02, 3.180e-02, 2.013e-02, 1.226e-02, 7.425e-03, 4.389e-03, 2.614e-03, 1.572e-03, 9.679e-04, 7.333e-04, 6.786e-04, 7.342e-04, 9.346e-04, 1.346e-03, 1.888e-03, 3.248e-03, 3.966e-03, 4.872e-03, 5.119e-03, 5.452e-03, 5.338e-03, 5.112e-03, 4.397e-03, 4.023e-03, 3.359e-03, 2.987e-03, 2.770e-03, 2.278e-03, 1.982e-03, 1.765e-03};
   pileupweightsDn = {3.733e-01, 1.197e+00, 1.263e+00, 1.102e+00, 1.240e+00, 1.278e+00, 9.076e-01, 7.680e-01, 1.093e+00, 1.345e+00, 1.489e+00, 1.526e+00, 1.496e+00, 1.500e+00, 1.498e+00, 1.445e+00, 1.367e+00, 1.298e+00, 1.228e+00, 1.165e+00, 1.125e+00, 1.091e+00, 1.065e+00, 1.041e+00, 1.019e+00, 1.005e+00, 9.973e-01, 9.851e-01, 9.722e-01, 9.567e-01, 9.141e-01, 8.732e-01, 8.075e-01, 7.337e-01, 6.501e-01, 5.605e-01, 4.658e-01, 3.750e-01, 2.886e-01, 2.147e-01, 1.498e-01, 1.001e-01, 6.433e-02, 3.962e-02, 2.392e-02, 1.382e-02, 7.544e-03, 4.163e-03, 2.215e-03, 1.187e-03, 6.441e-04, 3.850e-04, 2.739e-04, 2.425e-04, 2.913e-04, 3.993e-04, 5.467e-04, 7.711e-04, 1.143e-03, 1.598e-03, 2.706e-03, 3.234e-03, 3.878e-03, 3.973e-03, 4.121e-03, 3.928e-03, 3.659e-03, 3.059e-03, 2.719e-03, 2.203e-03, 1.901e-03, 1.709e-03, 1.362e-03, 1.147e-03, 9.884e-04};
   pileupweightsUp = {3.510e-01, 7.384e-01, 1.136e+00, 8.481e-01, 1.011e+00, 1.047e+00, 7.158e-01, 3.479e-01, 5.006e-01, 6.065e-01, 6.335e-01, 7.320e-01, 8.266e-01, 9.118e-01, 9.603e-01, 9.892e-01, 1.024e+00, 1.052e+00, 1.051e+00, 1.027e+00, 1.005e+00, 9.982e-01, 1.015e+00, 1.038e+00, 1.058e+00, 1.085e+00, 1.121e+00, 1.155e+00, 1.192e+00, 1.232e+00, 1.245e+00, 1.269e+00, 1.260e+00, 1.233e+00, 1.180e+00, 1.103e+00, 1.001e+00, 8.905e-01, 7.691e-01, 6.545e-01, 5.326e-01, 4.236e-01, 3.297e-01, 2.501e-01, 1.888e-01, 1.381e-01, 9.654e-02, 6.875e-02, 4.733e-02, 3.248e-02, 2.175e-02, 1.456e-02, 9.619e-03, 6.146e-03, 4.301e-03, 3.097e-03, 2.253e-03, 1.894e-03, 2.009e-03, 2.389e-03, 3.847e-03, 4.626e-03, 5.722e-03, 6.110e-03, 6.639e-03, 6.646e-03, 6.514e-03, 5.738e-03, 5.381e-03, 4.607e-03, 4.204e-03, 4.003e-03, 3.382e-03, 3.025e-03, 2.770e-03};
   *pileupweight = pileupweights[nTrueInt];
   *pileupweightup = pileupweightsUp[nTrueInt];
   *pileupweightdn = pileupweightsDn[nTrueInt];

}

void HardcodedConditions::GetPileupWeight2017(int nTrueInt, float *pileupweight, float *pileupweightup, float *pileupweightdn, std::string sample)
{
    // Pileup distributions -- 31Mar2018 Data vs RunIIFall17MC
    std::unordered_map<std::string, std::vector<float>> pileupweights = { // 69.2 mb
{"DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8",{5.202e-04, 1.732e-01, 6.524e-02, 1.051e-01, 7.782e-02, 7.074e-02, 5.636e-02, 1.578e-01, 1.041e-01, 2.976e-01, 4.844e-01, 8.430e-01, 6.433e-01, 6.391e-01, 6.185e-01, 6.598e-01, 7.822e-01, 9.093e-01, 1.069e+00, 1.086e+00, 1.211e+00, 1.252e+00, 1.298e+00, 1.322e+00, 1.355e+00, 1.372e+00, 1.174e+00, 1.383e+00, 1.413e+00, 1.396e+00, 1.341e+00, 1.287e+00, 1.197e+00, 1.112e+00, 1.062e+00, 1.003e+00, 9.522e-01, 9.235e-01, 8.274e-01, 8.367e-01, 7.672e-01, 8.866e-01, 9.070e-01, 1.072e+00, 1.230e+00, 1.408e+00, 1.541e+00, 1.679e+00, 1.737e+00, 1.642e+00, 1.427e+00, 1.265e+00, 1.031e+00, 8.213e-01, 6.221e-01, 4.057e-01, 3.109e-01, 2.122e-01, 1.497e-01, 9.110e-02, 7.505e-02, 5.398e-02, 4.104e-02, 2.899e-02, 2.612e-02, 1.903e-02, 1.301e-02, 1.146e-02, 1.055e-02, 1.017e-02, 9.379e-03, 7.285e-03, 1.100e-03, 8.660e-03, 4.736e-04, 6.339e-03, 5.531e-03, 5.185e-03, 2.455e-04, 1.158e-04, 9.824e-03, 1.564e-03, 7.432e-03, 2.421e-03, 1.253e-02, 4.023e-03, 0.000e+00, 3.241e-03, 1.472e-05, 0.000e+00, 7.774e-04, 0.000e+00, 0.000e+00, 1.716e-04, 0.000e+00, 0.000e+00, 3.470e-05, 1.996e-05, 0.000e+00, 1.942e-07, 0.000e+0}},
{"DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8",{1.768e-01, 4.107e+00, 3.478e+00, 2.368e+00, 1.552e+00, 1.556e+00, 1.295e+00, 1.254e+00, 6.272e-01, 1.463e+00, 1.473e+00, 1.480e+00, 1.325e+00, 1.167e+00, 1.079e+00, 1.053e+00, 1.087e+00, 1.126e+00, 1.163e+00, 1.189e+00, 1.209e+00, 1.236e+00, 1.262e+00, 1.271e+00, 1.275e+00, 1.273e+00, 1.272e+00, 1.265e+00, 1.274e+00, 1.250e+00, 1.225e+00, 1.171e+00, 1.109e+00, 1.040e+00, 9.681e-01, 9.124e-01, 8.668e-01, 8.337e-01, 7.864e-01, 7.501e-01, 7.585e-01, 7.938e-01, 8.590e-01, 9.606e-01, 1.090e+00, 1.254e+00, 1.419e+00, 1.496e+00, 1.530e+00, 1.464e+00, 1.337e+00, 1.156e+00, 9.501e-01, 7.507e-01, 5.714e-01, 4.116e-01, 2.893e-01, 1.983e-01, 1.380e-01, 9.645e-02, 6.933e-02, 5.061e-02, 3.844e-02, 3.011e-02, 2.407e-02, 1.715e-02, 1.241e-02, 1.070e-02, 9.663e-03, 8.949e-03, 8.231e-03, 8.094e-03, 7.946e-03, 7.974e-03, 6.490e-03, 5.392e-03, 5.367e-03, 5.789e-03, 5.517e-03, 6.496e-03, 6.447e-03, 6.003e-03, 7.472e-03, 5.167e-03, 4.724e-03, 6.645e-03, 3.867e-03, 6.246e-03, 5.034e-03, 5.474e-03, 1.348e-02, 4.113e-03, 9.943e-04, 2.976e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8",{2.500e-01, 3.492e+00, 4.860e+00, 4.056e+00, 1.567e+00, 1.494e+00, 1.133e+00, 1.246e+00, 7.152e-01, 1.517e+00, 1.398e+00, 1.490e+00, 1.296e+00, 1.144e+00, 1.087e+00, 1.079e+00, 1.105e+00, 1.119e+00, 1.147e+00, 1.176e+00, 1.207e+00, 1.223e+00, 1.251e+00, 1.276e+00, 1.283e+00, 1.282e+00, 1.271e+00, 1.286e+00, 1.273e+00, 1.237e+00, 1.246e+00, 1.154e+00, 1.122e+00, 1.047e+00, 9.742e-01, 9.220e-01, 8.832e-01, 8.296e-01, 7.859e-01, 7.315e-01, 7.527e-01, 7.973e-01, 8.528e-01, 9.597e-01, 1.111e+00, 1.247e+00, 1.429e+00, 1.496e+00, 1.505e+00, 1.470e+00, 1.311e+00, 1.135e+00, 9.619e-01, 7.553e-01, 5.713e-01, 4.166e-01, 2.828e-01, 1.963e-01, 1.396e-01, 9.582e-02, 6.930e-02, 5.052e-02, 3.820e-02, 3.023e-02, 2.362e-02, 1.661e-02, 1.264e-02, 1.092e-02, 9.747e-03, 8.866e-03, 8.610e-03, 8.709e-03, 8.045e-03, 7.947e-03, 6.080e-03, 4.973e-03, 4.198e-03, 4.600e-03, 4.225e-03, 6.136e-03, 6.391e-03, 4.917e-03, 6.447e-03, 3.150e-03, 2.717e-03, 0.000e+00, 3.336e-03, 2.109e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8",{1.927e-01, 5.011e+00, 3.624e+00, 2.585e+00, 1.535e+00, 1.512e+00, 1.265e+00, 1.241e+00, 6.101e-01, 1.460e+00, 1.474e+00, 1.481e+00, 1.338e+00, 1.168e+00, 1.077e+00, 1.056e+00, 1.087e+00, 1.126e+00, 1.165e+00, 1.187e+00, 1.210e+00, 1.238e+00, 1.257e+00, 1.270e+00, 1.271e+00, 1.270e+00, 1.271e+00, 1.263e+00, 1.275e+00, 1.253e+00, 1.224e+00, 1.170e+00, 1.112e+00, 1.039e+00, 9.682e-01, 9.138e-01, 8.670e-01, 8.355e-01, 7.879e-01, 7.524e-01, 7.599e-01, 7.932e-01, 8.584e-01, 9.590e-01, 1.097e+00, 1.263e+00, 1.421e+00, 1.479e+00, 1.529e+00, 1.465e+00, 1.335e+00, 1.150e+00, 9.494e-01, 7.483e-01, 5.690e-01, 4.105e-01, 2.896e-01, 2.000e-01, 1.376e-01, 9.723e-02, 6.903e-02, 5.082e-02, 3.845e-02, 2.976e-02, 2.415e-02, 1.709e-02, 1.252e-02, 1.073e-02, 9.586e-03, 8.949e-03, 8.293e-03, 7.967e-03, 8.087e-03, 8.015e-03, 6.300e-03, 5.234e-03, 5.574e-03, 5.610e-03, 5.790e-03, 5.574e-03, 5.847e-03, 6.031e-03, 6.626e-03, 5.603e-03, 4.217e-03, 4.281e-03, 6.041e-03, 4.455e-03, 4.189e-03, 3.470e-03, 2.564e-03, 1.956e-03, 1.576e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8",{2.036e-01, 3.719e+00, 3.315e+00, 2.794e+00, 1.757e+00, 1.489e+00, 1.262e+00, 1.287e+00, 6.035e-01, 1.444e+00, 1.509e+00, 1.485e+00, 1.336e+00, 1.165e+00, 1.081e+00, 1.048e+00, 1.081e+00, 1.126e+00, 1.165e+00, 1.194e+00, 1.217e+00, 1.240e+00, 1.263e+00, 1.265e+00, 1.272e+00, 1.269e+00, 1.272e+00, 1.263e+00, 1.270e+00, 1.250e+00, 1.225e+00, 1.169e+00, 1.110e+00, 1.041e+00, 9.702e-01, 9.123e-01, 8.658e-01, 8.345e-01, 7.881e-01, 7.513e-01, 7.580e-01, 7.945e-01, 8.608e-01, 9.598e-01, 1.097e+00, 1.258e+00, 1.421e+00, 1.495e+00, 1.527e+00, 1.456e+00, 1.334e+00, 1.154e+00, 9.500e-01, 7.479e-01, 5.703e-01, 4.109e-01, 2.894e-01, 1.988e-01, 1.375e-01, 9.674e-02, 6.941e-02, 5.087e-02, 3.824e-02, 2.989e-02, 2.419e-02, 1.714e-02, 1.251e-02, 1.072e-02, 9.610e-03, 8.944e-03, 8.300e-03, 8.145e-03, 7.606e-03, 7.887e-03, 6.196e-03, 5.502e-03, 5.342e-03, 5.697e-03, 6.310e-03, 5.414e-03, 6.132e-03, 7.429e-03, 6.981e-03, 4.787e-03, 3.756e-03, 4.929e-03, 4.250e-03, 3.806e-03, 5.725e-03, 3.557e-03, 1.095e-02, 6.682e-03, 4.039e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8",{1.925e-01, 6.204e+00, 4.276e+00, 2.532e+00, 1.764e+00, 1.482e+00, 1.395e+00, 1.478e+00, 6.245e-01, 1.488e+00, 1.518e+00, 1.483e+00, 1.299e+00, 1.175e+00, 1.079e+00, 1.047e+00, 1.069e+00, 1.132e+00, 1.165e+00, 1.186e+00, 1.214e+00, 1.235e+00, 1.261e+00, 1.275e+00, 1.276e+00, 1.270e+00, 1.272e+00, 1.256e+00, 1.276e+00, 1.256e+00, 1.220e+00, 1.168e+00, 1.111e+00, 1.042e+00, 9.694e-01, 9.133e-01, 8.702e-01, 8.306e-01, 7.877e-01, 7.505e-01, 7.537e-01, 8.003e-01, 8.602e-01, 9.598e-01, 1.098e+00, 1.255e+00, 1.421e+00, 1.484e+00, 1.528e+00, 1.457e+00, 1.349e+00, 1.157e+00, 9.466e-01, 7.544e-01, 5.640e-01, 4.091e-01, 2.895e-01, 2.006e-01, 1.374e-01, 9.694e-02, 6.937e-02, 5.080e-02, 3.882e-02, 2.971e-02, 2.425e-02, 1.701e-02, 1.242e-02, 1.096e-02, 9.670e-03, 8.692e-03, 8.242e-03, 8.000e-03, 8.012e-03, 8.072e-03, 5.896e-03, 5.085e-03, 5.798e-03, 5.538e-03, 5.657e-03, 5.095e-03, 6.150e-03, 5.407e-03, 7.090e-03, 5.105e-03, 2.728e-03, 3.664e-03, 8.561e-03, 5.411e-03, 5.088e-03, 6.323e-03, 3.893e-03, 7.918e-04, 7.179e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8",{1.957e-01, 4.016e+00, 3.198e+00, 2.581e+00, 1.609e+00, 1.488e+00, 1.311e+00, 1.285e+00, 6.157e-01, 1.497e+00, 1.491e+00, 1.485e+00, 1.332e+00, 1.162e+00, 1.082e+00, 1.050e+00, 1.082e+00, 1.129e+00, 1.164e+00, 1.188e+00, 1.211e+00, 1.238e+00, 1.259e+00, 1.273e+00, 1.270e+00, 1.266e+00, 1.273e+00, 1.267e+00, 1.274e+00, 1.253e+00, 1.224e+00, 1.167e+00, 1.111e+00, 1.039e+00, 9.689e-01, 9.114e-01, 8.672e-01, 8.349e-01, 7.884e-01, 7.513e-01, 7.584e-01, 7.940e-01, 8.597e-01, 9.612e-01, 1.096e+00, 1.257e+00, 1.422e+00, 1.502e+00, 1.528e+00, 1.468e+00, 1.335e+00, 1.156e+00, 9.493e-01, 7.492e-01, 5.713e-01, 4.111e-01, 2.901e-01, 1.981e-01, 1.378e-01, 9.664e-02, 6.912e-02, 5.065e-02, 3.833e-02, 2.985e-02, 2.404e-02, 1.705e-02, 1.252e-02, 1.077e-02, 9.567e-03, 8.751e-03, 8.326e-03, 7.909e-03, 7.754e-03, 7.791e-03, 6.346e-03, 5.424e-03, 5.444e-03, 5.321e-03, 6.079e-03, 5.542e-03, 6.050e-03, 6.164e-03, 6.122e-03, 4.578e-03, 4.423e-03, 4.051e-03, 4.979e-03, 4.005e-03, 4.603e-03, 3.813e-03, 2.642e-03, 6.447e-03, 1.559e-03, 4.665e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8",{1.749e-01, 4.172e+00, 3.462e+00, 2.677e+00, 1.657e+00, 1.475e+00, 1.255e+00, 1.247e+00, 6.001e-01, 1.423e+00, 1.498e+00, 1.492e+00, 1.325e+00, 1.164e+00, 1.082e+00, 1.052e+00, 1.083e+00, 1.127e+00, 1.163e+00, 1.191e+00, 1.212e+00, 1.241e+00, 1.255e+00, 1.270e+00, 1.274e+00, 1.273e+00, 1.272e+00, 1.268e+00, 1.278e+00, 1.250e+00, 1.223e+00, 1.171e+00, 1.111e+00, 1.036e+00, 9.706e-01, 9.105e-01, 8.681e-01, 8.332e-01, 7.863e-01, 7.510e-01, 7.603e-01, 7.926e-01, 8.584e-01, 9.578e-01, 1.096e+00, 1.256e+00, 1.416e+00, 1.494e+00, 1.526e+00, 1.468e+00, 1.336e+00, 1.152e+00, 9.529e-01, 7.485e-01, 5.702e-01, 4.122e-01, 2.880e-01, 1.984e-01, 1.374e-01, 9.694e-02, 6.917e-02, 5.072e-02, 3.858e-02, 2.990e-02, 2.407e-02, 1.711e-02, 1.255e-02, 1.081e-02, 9.625e-03, 8.906e-03, 8.153e-03, 8.132e-03, 7.846e-03, 7.748e-03, 6.233e-03, 5.267e-03, 5.609e-03, 6.071e-03, 6.121e-03, 6.164e-03, 6.168e-03, 6.767e-03, 6.302e-03, 3.970e-03, 5.435e-03, 5.004e-03, 3.543e-03, 5.497e-03, 4.211e-03, 2.944e-03, 3.626e-03, 2.949e-03, 5.348e-03, 3.201e-03, 9.489e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8",{1.673e-01, 4.002e+00, 3.617e+00, 2.548e+00, 1.509e+00, 1.493e+00, 1.296e+00, 1.240e+00, 6.044e-01, 1.455e+00, 1.499e+00, 1.488e+00, 1.340e+00, 1.174e+00, 1.086e+00, 1.052e+00, 1.083e+00, 1.128e+00, 1.168e+00, 1.181e+00, 1.205e+00, 1.236e+00, 1.259e+00, 1.272e+00, 1.271e+00, 1.272e+00, 1.271e+00, 1.267e+00, 1.278e+00, 1.251e+00, 1.219e+00, 1.164e+00, 1.109e+00, 1.038e+00, 9.690e-01, 9.157e-01, 8.645e-01, 8.360e-01, 7.876e-01, 7.518e-01, 7.621e-01, 7.940e-01, 8.594e-01, 9.634e-01, 1.096e+00, 1.255e+00, 1.424e+00, 1.511e+00, 1.535e+00, 1.457e+00, 1.342e+00, 1.153e+00, 9.464e-01, 7.538e-01, 5.673e-01, 4.094e-01, 2.882e-01, 1.995e-01, 1.377e-01, 9.630e-02, 6.900e-02, 5.090e-02, 3.856e-02, 2.996e-02, 2.428e-02, 1.692e-02, 1.250e-02, 1.082e-02, 9.818e-03, 8.680e-03, 8.325e-03, 8.296e-03, 7.673e-03, 7.873e-03, 6.039e-03, 5.129e-03, 5.625e-03, 5.495e-03, 6.660e-03, 5.474e-03, 5.696e-03, 6.031e-03, 5.399e-03, 4.689e-03, 3.380e-03, 4.749e-03, 6.917e-03, 1.020e-02, 2.398e-03, 2.980e-03, 2.447e-03, 4.479e-03, 1.353e-03, 5.401e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8",{1.809e-01, 4.000e+00, 3.698e+00, 2.549e+00, 1.633e+00, 1.551e+00, 1.271e+00, 1.249e+00, 6.178e-01, 1.456e+00, 1.491e+00, 1.487e+00, 1.335e+00, 1.167e+00, 1.080e+00, 1.055e+00, 1.082e+00, 1.129e+00, 1.166e+00, 1.189e+00, 1.212e+00, 1.239e+00, 1.260e+00, 1.270e+00, 1.273e+00, 1.271e+00, 1.270e+00, 1.266e+00, 1.274e+00, 1.253e+00, 1.225e+00, 1.171e+00, 1.110e+00, 1.038e+00, 9.680e-01, 9.116e-01, 8.658e-01, 8.344e-01, 7.895e-01, 7.502e-01, 7.581e-01, 7.934e-01, 8.596e-01, 9.603e-01, 1.094e+00, 1.256e+00, 1.420e+00, 1.494e+00, 1.527e+00, 1.463e+00, 1.340e+00, 1.153e+00, 9.533e-01, 7.507e-01, 5.701e-01, 4.092e-01, 2.900e-01, 1.986e-01, 1.377e-01, 9.651e-02, 6.932e-02, 5.073e-02, 3.841e-02, 2.995e-02, 2.408e-02, 1.705e-02, 1.251e-02, 1.072e-02, 9.619e-03, 8.788e-03, 8.250e-03, 7.996e-03, 7.891e-03, 7.873e-03, 6.430e-03, 5.389e-03, 5.500e-03, 5.553e-03, 5.844e-03, 6.347e-03, 6.023e-03, 5.760e-03, 6.569e-03, 4.950e-03, 4.052e-03, 4.399e-03, 4.184e-03, 4.983e-03, 5.131e-03, 4.617e-03, 5.154e-03, 2.959e-03, 1.789e-03, 6.067e-03, 1.079e-02, 1.056e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8",{1.857e-01, 4.045e+00, 3.641e+00, 2.530e+00, 1.581e+00, 1.497e+00, 1.295e+00, 1.279e+00, 6.177e-01, 1.454e+00, 1.500e+00, 1.481e+00, 1.327e+00, 1.166e+00, 1.076e+00, 1.055e+00, 1.082e+00, 1.128e+00, 1.165e+00, 1.188e+00, 1.212e+00, 1.239e+00, 1.261e+00, 1.269e+00, 1.272e+00, 1.271e+00, 1.272e+00, 1.266e+00, 1.275e+00, 1.252e+00, 1.221e+00, 1.170e+00, 1.110e+00, 1.037e+00, 9.681e-01, 9.120e-01, 8.670e-01, 8.341e-01, 7.886e-01, 7.513e-01, 7.581e-01, 7.927e-01, 8.606e-01, 9.609e-01, 1.093e+00, 1.258e+00, 1.421e+00, 1.493e+00, 1.528e+00, 1.463e+00, 1.337e+00, 1.152e+00, 9.533e-01, 7.506e-01, 5.696e-01, 4.108e-01, 2.902e-01, 1.987e-01, 1.375e-01, 9.668e-02, 6.935e-02, 5.089e-02, 3.841e-02, 2.998e-02, 2.406e-02, 1.712e-02, 1.249e-02, 1.072e-02, 9.597e-03, 8.794e-03, 8.246e-03, 8.079e-03, 7.878e-03, 7.878e-03, 6.210e-03, 5.385e-03, 5.520e-03, 5.676e-03, 5.731e-03, 5.892e-03, 6.284e-03, 6.447e-03, 6.131e-03, 4.915e-03, 4.189e-03, 4.261e-03, 3.924e-03, 5.040e-03, 4.146e-03, 3.989e-03, 2.456e-03, 2.904e-03, 1.652e-03, 2.101e-03, 9.965e-03, 2.925e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8",{1.834e-01, 3.830e+00, 3.431e+00, 2.566e+00, 1.607e+00, 1.516e+00, 1.322e+00, 1.286e+00, 6.178e-01, 1.451e+00, 1.510e+00, 1.489e+00, 1.334e+00, 1.166e+00, 1.079e+00, 1.051e+00, 1.080e+00, 1.129e+00, 1.168e+00, 1.188e+00, 1.212e+00, 1.236e+00, 1.259e+00, 1.270e+00, 1.275e+00, 1.273e+00, 1.272e+00, 1.266e+00, 1.275e+00, 1.251e+00, 1.222e+00, 1.170e+00, 1.108e+00, 1.038e+00, 9.692e-01, 9.114e-01, 8.675e-01, 8.339e-01, 7.873e-01, 7.504e-01, 7.585e-01, 7.925e-01, 8.606e-01, 9.600e-01, 1.097e+00, 1.258e+00, 1.417e+00, 1.495e+00, 1.532e+00, 1.461e+00, 1.339e+00, 1.155e+00, 9.511e-01, 7.497e-01, 5.697e-01, 4.110e-01, 2.903e-01, 1.985e-01, 1.376e-01, 9.636e-02, 6.920e-02, 5.083e-02, 3.837e-02, 2.997e-02, 2.407e-02, 1.708e-02, 1.248e-02, 1.079e-02, 9.597e-03, 8.774e-03, 8.342e-03, 8.039e-03, 7.871e-03, 7.898e-03, 6.371e-03, 5.334e-03, 5.530e-03, 5.678e-03, 5.844e-03, 6.165e-03, 6.247e-03, 6.308e-03, 6.138e-03, 5.205e-03, 4.022e-03, 4.512e-03, 3.981e-03, 4.461e-03, 3.549e-03, 3.699e-03, 3.210e-03, 3.590e-03, 2.367e-03, 1.732e-03, 4.620e-03, 2.712e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8",{1.879e-01, 3.816e+00, 3.218e+00, 2.454e+00, 1.641e+00, 1.494e+00, 1.304e+00, 1.240e+00, 6.218e-01, 1.457e+00, 1.500e+00, 1.489e+00, 1.328e+00, 1.166e+00, 1.081e+00, 1.054e+00, 1.079e+00, 1.130e+00, 1.166e+00, 1.190e+00, 1.211e+00, 1.241e+00, 1.258e+00, 1.270e+00, 1.270e+00, 1.272e+00, 1.273e+00, 1.266e+00, 1.275e+00, 1.250e+00, 1.221e+00, 1.170e+00, 1.110e+00, 1.038e+00, 9.694e-01, 9.114e-01, 8.672e-01, 8.367e-01, 7.879e-01, 7.498e-01, 7.579e-01, 7.935e-01, 8.617e-01, 9.591e-01, 1.097e+00, 1.255e+00, 1.422e+00, 1.495e+00, 1.530e+00, 1.462e+00, 1.341e+00, 1.155e+00, 9.510e-01, 7.488e-01, 5.689e-01, 4.108e-01, 2.892e-01, 1.990e-01, 1.375e-01, 9.631e-02, 6.932e-02, 5.092e-02, 3.836e-02, 2.995e-02, 2.401e-02, 1.709e-02, 1.245e-02, 1.070e-02, 9.656e-03, 8.801e-03, 8.344e-03, 8.060e-03, 7.939e-03, 7.699e-03, 6.254e-03, 5.278e-03, 5.482e-03, 5.668e-03, 5.810e-03, 6.086e-03, 6.095e-03, 6.078e-03, 6.937e-03, 5.137e-03, 4.083e-03, 4.345e-03, 3.657e-03, 4.376e-03, 4.655e-03, 3.409e-03, 2.351e-03, 2.758e-03, 1.445e-03, 1.081e-03, 2.564e-03, 1.505e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_s-channel_antitop_leptonDecays_13TeV-PSweights_powheg-pythia",{1.803e-01, 5.928e+00, 2.750e+00, 2.419e+00, 1.593e+00, 1.440e+00, 1.337e+00, 1.229e+00, 6.134e-01, 1.448e+00, 1.581e+00, 1.476e+00, 1.342e+00, 1.168e+00, 1.082e+00, 1.055e+00, 1.092e+00, 1.129e+00, 1.163e+00, 1.186e+00, 1.217e+00, 1.233e+00, 1.255e+00, 1.266e+00, 1.277e+00, 1.273e+00, 1.272e+00, 1.266e+00, 1.271e+00, 1.248e+00, 1.223e+00, 1.169e+00, 1.115e+00, 1.039e+00, 9.698e-01, 9.093e-01, 8.651e-01, 8.358e-01, 7.850e-01, 7.509e-01, 7.577e-01, 7.946e-01, 8.607e-01, 9.629e-01, 1.096e+00, 1.257e+00, 1.420e+00, 1.510e+00, 1.519e+00, 1.460e+00, 1.342e+00, 1.159e+00, 9.444e-01, 7.466e-01, 5.680e-01, 4.106e-01, 2.915e-01, 1.987e-01, 1.379e-01, 9.649e-02, 6.923e-02, 5.152e-02, 3.845e-02, 2.990e-02, 2.394e-02, 1.698e-02, 1.234e-02, 1.050e-02, 9.671e-03, 8.746e-03, 8.200e-03, 8.309e-03, 7.932e-03, 7.767e-03, 6.096e-03, 5.745e-03, 5.503e-03, 6.036e-03, 6.486e-03, 5.339e-03, 7.313e-03, 5.293e-03, 9.484e-03, 4.413e-03, 6.662e-03, 3.851e-03, 4.908e-03, 3.878e-03, 4.861e-03, 1.510e-03, 3.720e-03, 1.135e-03, 1.372e-03, 8.212e-04, 0.000e+00, 2.857e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_s-channel_top_leptonDecays_13TeV-PSweights_powheg-pythia",{1.746e-01, 3.830e+00, 3.553e+00, 2.403e+00, 1.599e+00, 1.559e+00, 1.322e+00, 1.260e+00, 6.069e-01, 1.461e+00, 1.501e+00, 1.472e+00, 1.320e+00, 1.158e+00, 1.080e+00, 1.055e+00, 1.084e+00, 1.121e+00, 1.171e+00, 1.191e+00, 1.209e+00, 1.237e+00, 1.260e+00, 1.273e+00, 1.272e+00, 1.267e+00, 1.272e+00, 1.269e+00, 1.271e+00, 1.252e+00, 1.223e+00, 1.171e+00, 1.111e+00, 1.044e+00, 9.695e-01, 9.127e-01, 8.670e-01, 8.365e-01, 7.866e-01, 7.524e-01, 7.567e-01, 7.963e-01, 8.596e-01, 9.551e-01, 1.093e+00, 1.260e+00, 1.425e+00, 1.487e+00, 1.521e+00, 1.463e+00, 1.343e+00, 1.156e+00, 9.445e-01, 7.558e-01, 5.707e-01, 4.089e-01, 2.878e-01, 1.986e-01, 1.374e-01, 9.582e-02, 6.921e-02, 5.063e-02, 3.820e-02, 3.022e-02, 2.411e-02, 1.709e-02, 1.256e-02, 1.082e-02, 9.682e-03, 8.739e-03, 8.479e-03, 8.119e-03, 8.084e-03, 7.948e-03, 6.203e-03, 5.410e-03, 5.892e-03, 5.502e-03, 5.216e-03, 5.742e-03, 6.863e-03, 6.583e-03, 7.384e-03, 6.367e-03, 4.829e-03, 4.283e-03, 3.582e-03, 5.176e-03, 3.785e-03, 2.822e-03, 8.689e-03, 2.651e-03, 3.204e-03, 9.591e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.852e-01, 3.872e+00, 3.527e+00, 2.555e+00, 1.599e+00, 1.529e+00, 1.308e+00, 1.270e+00, 6.120e-01, 1.461e+00, 1.499e+00, 1.481e+00, 1.335e+00, 1.168e+00, 1.079e+00, 1.051e+00, 1.078e+00, 1.128e+00, 1.167e+00, 1.190e+00, 1.212e+00, 1.238e+00, 1.260e+00, 1.272e+00, 1.272e+00, 1.271e+00, 1.270e+00, 1.267e+00, 1.278e+00, 1.253e+00, 1.222e+00, 1.170e+00, 1.109e+00, 1.038e+00, 9.688e-01, 9.125e-01, 8.665e-01, 8.339e-01, 7.873e-01, 7.505e-01, 7.585e-01, 7.922e-01, 8.598e-01, 9.591e-01, 1.096e+00, 1.256e+00, 1.419e+00, 1.497e+00, 1.529e+00, 1.464e+00, 1.338e+00, 1.158e+00, 9.496e-01, 7.484e-01, 5.695e-01, 4.107e-01, 2.897e-01, 1.987e-01, 1.375e-01, 9.643e-02, 6.918e-02, 5.080e-02, 3.835e-02, 3.004e-02, 2.410e-02, 1.712e-02, 1.248e-02, 1.078e-02, 9.636e-03, 8.782e-03, 8.289e-03, 8.057e-03, 7.851e-03, 7.971e-03, 6.259e-03, 5.394e-03, 5.467e-03, 5.733e-03, 5.734e-03, 5.922e-03, 6.267e-03, 6.286e-03, 6.323e-03, 4.593e-03, 3.965e-03, 4.804e-03, 4.310e-03, 4.481e-03, 4.186e-03, 3.790e-03, 2.723e-03, 2.931e-03, 1.882e-03, 2.003e-03, 1.069e-02, 8.963e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.825e-01, 3.909e+00, 3.371e+00, 2.523e+00, 1.643e+00, 1.508e+00, 1.285e+00, 1.257e+00, 6.197e-01, 1.460e+00, 1.502e+00, 1.487e+00, 1.334e+00, 1.168e+00, 1.080e+00, 1.053e+00, 1.081e+00, 1.128e+00, 1.166e+00, 1.189e+00, 1.214e+00, 1.238e+00, 1.260e+00, 1.270e+00, 1.273e+00, 1.272e+00, 1.271e+00, 1.267e+00, 1.275e+00, 1.252e+00, 1.221e+00, 1.170e+00, 1.109e+00, 1.038e+00, 9.690e-01, 9.118e-01, 8.668e-01, 8.344e-01, 7.886e-01, 7.506e-01, 7.584e-01, 7.925e-01, 8.602e-01, 9.579e-01, 1.094e+00, 1.256e+00, 1.420e+00, 1.496e+00, 1.530e+00, 1.462e+00, 1.337e+00, 1.153e+00, 9.504e-01, 7.509e-01, 5.697e-01, 4.111e-01, 2.900e-01, 1.986e-01, 1.377e-01, 9.650e-02, 6.921e-02, 5.083e-02, 3.841e-02, 3.001e-02, 2.415e-02, 1.713e-02, 1.248e-02, 1.077e-02, 9.577e-03, 8.775e-03, 8.270e-03, 8.056e-03, 7.813e-03, 7.842e-03, 6.354e-03, 5.325e-03, 5.540e-03, 5.616e-03, 5.825e-03, 6.069e-03, 6.155e-03, 6.495e-03, 6.770e-03, 4.718e-03, 4.354e-03, 4.733e-03, 4.094e-03, 4.475e-03, 3.960e-03, 4.563e-03, 2.711e-03, 2.947e-03, 1.628e-03, 1.795e-03, 6.741e-03, 1.696e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.923e-01, 3.858e+00, 3.294e+00, 2.403e+00, 1.686e+00, 1.567e+00, 1.329e+00, 1.244e+00, 6.014e-01, 1.447e+00, 1.506e+00, 1.487e+00, 1.325e+00, 1.173e+00, 1.079e+00, 1.053e+00, 1.079e+00, 1.127e+00, 1.171e+00, 1.188e+00, 1.213e+00, 1.238e+00, 1.255e+00, 1.271e+00, 1.274e+00, 1.271e+00, 1.271e+00, 1.267e+00, 1.271e+00, 1.255e+00, 1.224e+00, 1.167e+00, 1.110e+00, 1.039e+00, 9.678e-01, 9.130e-01, 8.656e-01, 8.348e-01, 7.886e-01, 7.502e-01, 7.614e-01, 7.936e-01, 8.597e-01, 9.614e-01, 1.090e+00, 1.261e+00, 1.414e+00, 1.498e+00, 1.524e+00, 1.460e+00, 1.328e+00, 1.158e+00, 9.470e-01, 7.491e-01, 5.716e-01, 4.128e-01, 2.892e-01, 1.986e-01, 1.370e-01, 9.649e-02, 6.938e-02, 5.098e-02, 3.854e-02, 3.016e-02, 2.394e-02, 1.713e-02, 1.252e-02, 1.078e-02, 9.578e-03, 8.740e-03, 8.257e-03, 7.846e-03, 7.829e-03, 8.136e-03, 6.325e-03, 5.530e-03, 5.481e-03, 5.873e-03, 5.533e-03, 6.041e-03, 6.394e-03, 6.647e-03, 6.734e-03, 5.885e-03, 4.336e-03, 4.177e-03, 3.758e-03, 6.731e-03, 4.219e-03, 2.621e-03, 2.421e-03, 5.909e-03, 1.190e-03, 2.138e-03, 0.000e+00, 3.720e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.706e-01, 4.036e+00, 4.062e+00, 2.813e+00, 1.666e+00, 1.506e+00, 1.243e+00, 1.212e+00, 6.098e-01, 1.456e+00, 1.456e+00, 1.476e+00, 1.333e+00, 1.172e+00, 1.073e+00, 1.053e+00, 1.082e+00, 1.124e+00, 1.171e+00, 1.194e+00, 1.215e+00, 1.233e+00, 1.264e+00, 1.270e+00, 1.273e+00, 1.275e+00, 1.272e+00, 1.266e+00, 1.273e+00, 1.249e+00, 1.221e+00, 1.168e+00, 1.105e+00, 1.037e+00, 9.676e-01, 9.107e-01, 8.676e-01, 8.343e-01, 7.912e-01, 7.511e-01, 7.582e-01, 7.948e-01, 8.562e-01, 9.601e-01, 1.099e+00, 1.257e+00, 1.423e+00, 1.487e+00, 1.521e+00, 1.465e+00, 1.342e+00, 1.157e+00, 9.496e-01, 7.494e-01, 5.700e-01, 4.126e-01, 2.901e-01, 1.984e-01, 1.380e-01, 9.621e-02, 6.949e-02, 5.070e-02, 3.833e-02, 3.015e-02, 2.417e-02, 1.718e-02, 1.252e-02, 1.094e-02, 9.618e-03, 8.845e-03, 8.205e-03, 7.989e-03, 7.797e-03, 7.889e-03, 6.438e-03, 5.379e-03, 5.799e-03, 5.502e-03, 6.000e-03, 5.766e-03, 6.608e-03, 6.037e-03, 5.066e-03, 4.670e-03, 5.930e-03, 5.713e-03, 4.681e-03, 5.178e-03, 3.246e-03, 3.227e-03, 1.656e-03, 6.062e-03, 9.159e-04, 2.193e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTHH_TuneCP5_13TeV-madgraph-pythia8",{1.196e-04, 5.204e-01, 4.023e-01, 2.879e-01, 2.163e-01, 1.576e-01, 1.475e-01, 1.344e-01, 6.983e-02, 3.851e-01, 5.166e-01, 5.361e-01, 7.230e-01, 3.607e-01, 7.524e-01, 7.334e-01, 7.852e-01, 9.504e-01, 8.686e-01, 1.200e+00, 1.238e+00, 1.309e+00, 1.392e+00, 1.441e+00, 1.436e+00, 1.369e+00, 1.420e+00, 1.404e+00, 1.421e+00, 1.387e+00, 1.349e+00, 1.289e+00, 1.261e+00, 1.153e+00, 1.115e+00, 1.035e+00, 9.963e-01, 9.319e-01, 8.792e-01, 8.314e-01, 8.832e-01, 8.983e-01, 9.666e-01, 1.054e+00, 1.235e+00, 1.399e+00, 1.609e+00, 1.718e+00, 1.716e+00, 1.680e+00, 1.450e+00, 1.254e+00, 1.053e+00, 8.634e-01, 6.589e-01, 4.735e-01, 3.268e-01, 2.292e-01, 1.535e-01, 1.054e-01, 7.915e-02, 5.845e-02, 3.508e-02, 3.221e-02, 2.534e-02, 2.050e-02, 1.364e-02, 1.160e-02, 1.077e-02, 1.017e-02, 8.554e-03, 9.067e-03, 1.006e-02, 8.524e-03, 7.597e-03, 5.249e-03, 6.624e-03, 5.027e-03, 1.259e-02, 1.677e-02, 5.556e-03, 4.885e-03, 9.607e-03, 2.086e-03, 0.000e+00, 2.600e-03, 1.657e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 5.607e-06, 0.000e+00, 0.000e+00, 1.479e-07, 0.000e+0}},
{"TTTJ_TuneCP5_13TeV-madgraph-pythia8",{1.374e-01, 0.000e+00, 4.808e+00, 2.580e+00, 3.231e+00, 1.756e+00, 1.468e+00, 1.089e+00, 6.318e-01, 1.449e+00, 1.492e+00, 1.421e+00, 1.218e+00, 1.156e+00, 1.103e+00, 1.046e+00, 1.100e+00, 1.149e+00, 1.178e+00, 1.214e+00, 1.215e+00, 1.226e+00, 1.255e+00, 1.278e+00, 1.249e+00, 1.262e+00, 1.260e+00, 1.258e+00, 1.278e+00, 1.257e+00, 1.224e+00, 1.172e+00, 1.109e+00, 1.027e+00, 9.588e-01, 9.063e-01, 8.598e-01, 8.457e-01, 8.045e-01, 7.557e-01, 7.739e-01, 7.953e-01, 8.771e-01, 9.409e-01, 1.128e+00, 1.215e+00, 1.418e+00, 1.511e+00, 1.522e+00, 1.437e+00, 1.357e+00, 1.172e+00, 9.472e-01, 7.288e-01, 5.542e-01, 4.123e-01, 2.807e-01, 2.046e-01, 1.358e-01, 9.633e-02, 7.233e-02, 5.112e-02, 3.930e-02, 2.868e-02, 2.438e-02, 1.681e-02, 1.328e-02, 1.063e-02, 9.811e-03, 7.983e-03, 8.093e-03, 8.161e-03, 8.634e-03, 9.577e-03, 5.548e-03, 4.920e-03, 5.340e-03, 5.776e-03, 4.560e-03, 4.174e-03, 5.533e-03, 0.000e+00, 9.568e-03, 2.078e-03, 0.000e+00, 0.000e+00, 1.650e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTTT_TuneCP5_13TeV-amcatnlo-pythia8",{1.503e-01, 2.250e+00, 2.922e+00, 2.287e+00, 1.841e+00, 9.179e-01, 7.874e-01, 8.202e-01, 9.332e-01, 1.343e+00, 1.293e+00, 1.631e+00, 1.278e+00, 1.115e+00, 1.072e+00, 1.053e+00, 1.066e+00, 1.161e+00, 1.218e+00, 1.171e+00, 1.245e+00, 1.187e+00, 1.233e+00, 1.250e+00, 1.289e+00, 1.233e+00, 1.278e+00, 1.275e+00, 1.248e+00, 1.274e+00, 1.187e+00, 1.165e+00, 1.094e+00, 1.052e+00, 9.833e-01, 9.331e-01, 8.964e-01, 8.474e-01, 7.690e-01, 7.452e-01, 7.399e-01, 7.868e-01, 8.684e-01, 9.558e-01, 1.101e+00, 1.326e+00, 1.447e+00, 1.501e+00, 1.613e+00, 1.487e+00, 1.324e+00, 1.155e+00, 9.510e-01, 7.847e-01, 5.405e-01, 4.072e-01, 3.035e-01, 1.982e-01, 1.431e-01, 9.851e-02, 6.585e-02, 4.937e-02, 3.788e-02, 3.128e-02, 2.360e-02, 1.687e-02, 1.200e-02, 9.873e-03, 9.357e-03, 8.688e-03, 8.214e-03, 7.563e-03, 6.484e-03, 6.005e-03, 5.620e-03, 7.475e-03, 4.868e-03, 6.167e-03, 8.022e-03, 2.537e-02, 5.173e-03, 3.167e-03, 4.153e-03, 4.735e-03, 2.450e-03, 0.000e+00, 1.254e-03, -7.925e-04, 0.000e+00, 0.000e+00, 0.000e+00, -4.638e-04, 0.000e+00, -8.391e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8",{2.302e-01, 7.396e+00, 2.287e+00, 2.090e+00, 1.407e+00, 1.191e+00, 1.419e+00, 1.101e+00, 6.714e-01, 1.540e+00, 1.523e+00, 1.458e+00, 1.346e+00, 1.134e+00, 1.051e+00, 1.061e+00, 1.077e+00, 1.147e+00, 1.164e+00, 1.193e+00, 1.202e+00, 1.227e+00, 1.266e+00, 1.289e+00, 1.250e+00, 1.293e+00, 1.261e+00, 1.261e+00, 1.275e+00, 1.256e+00, 1.210e+00, 1.156e+00, 1.110e+00, 1.041e+00, 9.645e-01, 9.088e-01, 8.708e-01, 8.399e-01, 7.916e-01, 7.479e-01, 7.467e-01, 8.111e-01, 8.647e-01, 9.552e-01, 1.106e+00, 1.269e+00, 1.422e+00, 1.530e+00, 1.525e+00, 1.467e+00, 1.330e+00, 1.147e+00, 9.393e-01, 7.665e-01, 5.674e-01, 4.013e-01, 2.870e-01, 2.045e-01, 1.386e-01, 9.738e-02, 6.968e-02, 5.167e-02, 3.840e-02, 2.991e-02, 2.409e-02, 1.688e-02, 1.212e-02, 1.001e-02, 9.246e-03, 8.900e-03, 8.941e-03, 8.093e-03, 7.877e-03, 7.762e-03, 7.078e-03, 5.385e-03, 4.949e-03, 5.953e-03, 8.948e-03, 5.718e-03, 6.317e-03, 5.680e-03, 5.120e-03, 4.447e-03, 2.877e-03, 5.543e-03, 0.000e+00, -4.466e-03, 1.400e-03, 0.000e+00, 1.071e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTTW_TuneCP5_13TeV-madgraph-pythia8",{1.822e-03, 4.739e-01, 5.690e-01, 2.711e-01, 2.349e-01, 1.976e-01, 1.814e-01, 1.785e-01, 9.210e-02, 1.979e-01, 5.709e-01, 6.113e-01, 6.835e-01, 1.001e+00, 1.049e+00, 1.019e+00, 1.057e+00, 9.561e-01, 1.063e+00, 1.097e+00, 1.129e+00, 1.175e+00, 1.246e+00, 1.283e+00, 1.280e+00, 1.309e+00, 1.316e+00, 1.270e+00, 1.314e+00, 1.319e+00, 1.259e+00, 1.227e+00, 1.110e+00, 1.084e+00, 1.037e+00, 9.790e-01, 8.646e-01, 8.969e-01, 8.425e-01, 8.139e-01, 8.230e-01, 8.539e-01, 9.129e-01, 1.061e+00, 1.152e+00, 1.363e+00, 1.531e+00, 1.673e+00, 1.684e+00, 1.584e+00, 1.396e+00, 1.236e+00, 8.211e-01, 7.984e-01, 6.256e-01, 4.464e-01, 3.063e-01, 1.624e-01, 1.482e-01, 1.041e-01, 7.243e-02, 5.495e-02, 4.163e-02, 3.149e-02, 2.467e-02, 1.878e-02, 1.324e-02, 1.179e-02, 9.596e-03, 9.792e-03, 9.045e-03, 8.131e-03, 1.065e-02, 6.261e-03, 5.979e-03, 6.232e-03, 5.937e-03, 6.294e-03, 3.604e-03, 3.015e-05, 7.420e-03, 1.468e-02, 9.623e-03, 2.090e-03, 4.056e-03, 2.605e-03, 4.150e-04, 1.778e-06, 6.577e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 1.123e-05, 0.000e+00, 0.000e+00, 4.148e-07, 0.000e+0}},
{"TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.788e-01, 3.918e+00, 3.422e+00, 2.558e+00, 1.640e+00, 1.547e+00, 1.294e+00, 1.245e+00, 6.140e-01, 1.462e+00, 1.487e+00, 1.493e+00, 1.332e+00, 1.172e+00, 1.079e+00, 1.054e+00, 1.082e+00, 1.126e+00, 1.165e+00, 1.190e+00, 1.212e+00, 1.238e+00, 1.260e+00, 1.269e+00, 1.271e+00, 1.272e+00, 1.271e+00, 1.266e+00, 1.275e+00, 1.251e+00, 1.223e+00, 1.171e+00, 1.110e+00, 1.039e+00, 9.682e-01, 9.119e-01, 8.664e-01, 8.355e-01, 7.881e-01, 7.501e-01, 7.599e-01, 7.924e-01, 8.597e-01, 9.594e-01, 1.094e+00, 1.259e+00, 1.422e+00, 1.495e+00, 1.531e+00, 1.461e+00, 1.339e+00, 1.156e+00, 9.484e-01, 7.504e-01, 5.701e-01, 4.114e-01, 2.895e-01, 1.988e-01, 1.375e-01, 9.635e-02, 6.927e-02, 5.070e-02, 3.840e-02, 3.003e-02, 2.402e-02, 1.707e-02, 1.246e-02, 1.077e-02, 9.651e-03, 8.821e-03, 8.296e-03, 8.108e-03, 7.676e-03, 7.829e-03, 6.228e-03, 5.362e-03, 5.526e-03, 5.500e-03, 5.669e-03, 5.859e-03, 6.026e-03, 6.557e-03, 6.010e-03, 4.681e-03, 4.003e-03, 4.407e-03, 3.879e-03, 4.291e-03, 3.963e-03, 3.509e-03, 3.201e-03, 3.102e-03, 2.125e-03, 2.120e-03, 5.656e-03, 2.213e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTTo2L2Nu_TuneCP5_erdON_13TeV-powheg-pythia8",{1.840e-01, 3.662e+00, 4.010e+00, 2.418e+00, 1.672e+00, 1.441e+00, 1.243e+00, 1.306e+00, 6.359e-01, 1.453e+00, 1.533e+00, 1.502e+00, 1.344e+00, 1.168e+00, 1.084e+00, 1.049e+00, 1.084e+00, 1.131e+00, 1.158e+00, 1.195e+00, 1.217e+00, 1.239e+00, 1.260e+00, 1.275e+00, 1.273e+00, 1.274e+00, 1.274e+00, 1.266e+00, 1.267e+00, 1.250e+00, 1.224e+00, 1.171e+00, 1.110e+00, 1.039e+00, 9.677e-01, 9.105e-01, 8.661e-01, 8.357e-01, 7.874e-01, 7.511e-01, 7.592e-01, 7.924e-01, 8.614e-01, 9.582e-01, 1.092e+00, 1.259e+00, 1.412e+00, 1.493e+00, 1.523e+00, 1.458e+00, 1.335e+00, 1.155e+00, 9.488e-01, 7.469e-01, 5.703e-01, 4.122e-01, 2.908e-01, 1.989e-01, 1.378e-01, 9.644e-02, 6.916e-02, 5.079e-02, 3.839e-02, 3.001e-02, 2.407e-02, 1.706e-02, 1.251e-02, 1.068e-02, 9.579e-03, 8.792e-03, 8.295e-03, 7.761e-03, 8.101e-03, 7.755e-03, 6.441e-03, 5.339e-03, 5.774e-03, 5.426e-03, 5.963e-03, 5.410e-03, 6.702e-03, 6.187e-03, 6.760e-03, 5.467e-03, 6.033e-03, 5.988e-03, 6.996e-03, 5.307e-03, 1.663e-02, 1.476e-03, 0.000e+00, 3.883e-03, 0.000e+00, 7.024e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8",{2.835e-04, 4.059e-02, 3.404e-02, 6.586e-02, 6.835e-02, 1.112e-01, 1.163e-01, 1.458e-01, 8.880e-02, 3.273e-01, 4.664e-01, 6.116e-01, 6.635e-01, 7.136e-01, 6.942e-01, 7.775e-01, 8.844e-01, 9.643e-01, 1.084e+00, 1.137e+00, 1.190e+00, 1.243e+00, 1.288e+00, 1.339e+00, 1.344e+00, 1.361e+00, 1.345e+00, 1.339e+00, 1.382e+00, 1.353e+00, 1.334e+00, 1.256e+00, 1.203e+00, 1.134e+00, 1.060e+00, 9.933e-01, 9.512e-01, 9.144e-01, 8.659e-01, 8.197e-01, 8.376e-01, 8.601e-01, 9.380e-01, 1.032e+00, 1.201e+00, 1.376e+00, 1.570e+00, 1.640e+00, 1.677e+00, 1.588e+00, 1.376e+00, 1.198e+00, 1.024e+00, 7.695e-01, 6.010e-01, 4.205e-01, 3.115e-01, 2.120e-01, 1.474e-01, 1.037e-01, 7.384e-02, 5.415e-02, 4.162e-02, 3.229e-02, 2.174e-02, 1.836e-02, 1.201e-02, 1.151e-02, 1.051e-02, 9.396e-03, 8.981e-03, 5.835e-03, 6.364e-03, 3.731e-03, 2.320e-03, 4.202e-03, 5.608e-03, 5.281e-03, 8.625e-04, 2.962e-04, 2.812e-04, 7.532e-03, 6.543e-03, 3.965e-03, 6.162e-04, 1.376e-04, 4.104e-03, 4.954e-05, 4.932e-06, 5.242e-05, 4.888e-05, 5.181e-06, 3.116e-05, 1.425e-05, 5.737e-07, 2.036e-07, 1.018e-05, 1.757e-05, 1.112e-05, 3.616e-07, 0.000e+0}},
{"TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8",{2.284e-04, 2.095e-02, 5.801e-02, 4.406e-02, 6.534e-02, 7.308e-02, 8.682e-02, 1.390e-01, 1.152e-01, 2.737e-01, 4.851e-01, 6.506e-01, 6.138e-01, 7.384e-01, 7.507e-01, 8.407e-01, 9.474e-01, 1.038e+00, 1.108e+00, 1.164e+00, 1.202e+00, 1.255e+00, 1.309e+00, 1.318e+00, 1.345e+00, 1.348e+00, 1.382e+00, 1.387e+00, 1.382e+00, 1.382e+00, 1.347e+00, 1.263e+00, 1.217e+00, 1.117e+00, 1.073e+00, 1.005e+00, 9.551e-01, 9.159e-01, 8.429e-01, 8.335e-01, 8.255e-01, 8.521e-01, 9.182e-01, 1.053e+00, 1.222e+00, 1.364e+00, 1.530e+00, 1.593e+00, 1.669e+00, 1.614e+00, 1.413e+00, 1.245e+00, 1.003e+00, 7.827e-01, 6.143e-01, 4.329e-01, 3.028e-01, 2.152e-01, 1.473e-01, 1.012e-01, 7.465e-02, 5.308e-02, 4.164e-02, 3.221e-02, 2.583e-02, 1.847e-02, 1.244e-02, 1.030e-02, 1.028e-02, 8.157e-03, 6.394e-03, 6.379e-03, 4.304e-03, 8.809e-03, 3.284e-03, 5.696e-03, 5.464e-03, 1.022e-03, 7.867e-04, 3.656e-04, 1.154e-04, 8.550e-05, 6.918e-03, 5.037e-03, 5.562e-05, 4.186e-03, 2.159e-03, 9.322e-06, 1.223e-05, 3.628e-06, 1.498e-05, 2.467e-05, 1.679e-05, 7.588e-04, 8.996e-04, 5.444e-06, 1.534e-05, 2.942e-05, 1.257e-05, 3.520e-07, 0.000e+0}},
{"TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8",{2.084e-04, 3.092e-02, 2.999e-02, 3.955e-02, 3.400e-02, 6.921e-02, 1.578e-01, 1.371e-01, 7.704e-02, 2.829e-01, 4.081e-01, 5.581e-01, 6.673e-01, 7.276e-01, 7.514e-01, 8.007e-01, 9.048e-01, 1.029e+00, 1.112e+00, 1.150e+00, 1.218e+00, 1.265e+00, 1.297e+00, 1.361e+00, 1.376e+00, 1.381e+00, 1.361e+00, 1.389e+00, 1.403e+00, 1.384e+00, 1.316e+00, 1.292e+00, 1.227e+00, 1.169e+00, 1.068e+00, 1.010e+00, 9.731e-01, 9.382e-01, 8.780e-01, 8.177e-01, 8.530e-01, 8.913e-01, 9.299e-01, 1.073e+00, 1.203e+00, 1.407e+00, 1.549e+00, 1.626e+00, 1.684e+00, 1.579e+00, 1.357e+00, 1.152e+00, 1.033e+00, 7.943e-01, 6.216e-01, 4.329e-01, 3.106e-01, 2.118e-01, 1.484e-01, 1.002e-01, 7.080e-02, 5.370e-02, 4.120e-02, 3.199e-02, 2.550e-02, 1.736e-02, 1.293e-02, 1.178e-02, 1.023e-02, 9.756e-03, 7.645e-03, 3.947e-03, 5.360e-03, 8.342e-03, 3.573e-03, 5.841e-03, 4.959e-03, 6.311e-04, 7.599e-04, 2.545e-04, 1.463e-04, 1.562e-03, 1.610e-04, 1.052e-04, 3.452e-05, 4.447e-05, 3.329e-03, 7.411e-06, 1.132e-05, 1.776e-03, 2.403e-05, 4.002e-03, 2.238e-06, 1.448e-03, 8.584e-04, 1.408e-06, 3.254e-05, 5.932e-07, 1.599e-05, 3.126e-07, 0.000e+0}},
{"TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8",{3.372e-04, 5.758e-02, 3.192e-02, 5.762e-02, 5.601e-02, 1.217e-01, 1.524e-01, 1.690e-01, 1.068e-01, 4.697e-01, 6.134e-01, 6.978e-01, 6.623e-01, 7.043e-01, 7.038e-01, 8.086e-01, 8.691e-01, 9.616e-01, 1.068e+00, 1.111e+00, 1.186e+00, 1.228e+00, 1.290e+00, 1.331e+00, 1.335e+00, 1.322e+00, 1.337e+00, 1.344e+00, 1.349e+00, 1.341e+00, 1.312e+00, 1.255e+00, 1.198e+00, 1.134e+00, 1.048e+00, 1.001e+00, 9.525e-01, 9.142e-01, 8.510e-01, 8.156e-01, 8.136e-01, 8.622e-01, 9.281e-01, 1.028e+00, 1.171e+00, 1.346e+00, 1.558e+00, 1.557e+00, 1.621e+00, 1.590e+00, 1.383e+00, 1.237e+00, 1.008e+00, 7.955e-01, 5.958e-01, 4.322e-01, 3.115e-01, 2.134e-01, 1.444e-01, 1.033e-01, 7.411e-02, 5.480e-02, 4.140e-02, 2.954e-02, 2.486e-02, 1.816e-02, 1.226e-02, 1.152e-02, 1.027e-02, 9.449e-03, 8.251e-03, 4.949e-03, 8.306e-03, 4.435e-03, 2.320e-03, 4.025e-03, 3.667e-03, 4.028e-03, 4.711e-04, 4.370e-04, 5.383e-04, 4.716e-03, 3.246e-03, 3.759e-03, 3.317e-03, 3.254e-05, 1.373e-05, 9.566e-05, 1.479e-03, 2.206e-03, 0.000e+00, 1.381e-03, 2.504e-03, 8.715e-06, 4.443e-04, 3.967e-07, 1.895e-05, 2.491e-05, 2.483e-05, 2.640e-07, 0.000e+0}},
{"TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.864e-01, 3.667e+00, 3.369e+00, 2.529e+00, 1.611e+00, 1.512e+00, 1.281e+00, 1.273e+00, 6.152e-01, 1.451e+00, 1.487e+00, 1.485e+00, 1.334e+00, 1.169e+00, 1.077e+00, 1.054e+00, 1.081e+00, 1.128e+00, 1.164e+00, 1.188e+00, 1.213e+00, 1.238e+00, 1.261e+00, 1.271e+00, 1.272e+00, 1.271e+00, 1.271e+00, 1.267e+00, 1.274e+00, 1.251e+00, 1.222e+00, 1.169e+00, 1.110e+00, 1.038e+00, 9.684e-01, 9.112e-01, 8.669e-01, 8.359e-01, 7.887e-01, 7.499e-01, 7.593e-01, 7.939e-01, 8.595e-01, 9.585e-01, 1.094e+00, 1.257e+00, 1.418e+00, 1.494e+00, 1.531e+00, 1.462e+00, 1.337e+00, 1.155e+00, 9.514e-01, 7.501e-01, 5.697e-01, 4.109e-01, 2.898e-01, 1.986e-01, 1.374e-01, 9.662e-02, 6.931e-02, 5.093e-02, 3.845e-02, 2.997e-02, 2.409e-02, 1.708e-02, 1.250e-02, 1.079e-02, 9.602e-03, 8.834e-03, 8.264e-03, 8.024e-03, 7.804e-03, 7.872e-03, 6.320e-03, 5.380e-03, 5.496e-03, 5.494e-03, 5.879e-03, 5.870e-03, 6.121e-03, 6.425e-03, 6.407e-03, 4.853e-03, 4.312e-03, 4.588e-03, 4.065e-03, 4.433e-03, 4.088e-03, 4.064e-03, 3.536e-03, 3.817e-03, 1.935e-03, 1.890e-03, 7.096e-03, 2.499e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToHadronic_TuneCP5_erdON_13TeV-powheg-pythia8",{1.838e-01, 4.220e+00, 3.464e+00, 2.629e+00, 1.652e+00, 1.509e+00, 1.312e+00, 1.245e+00, 6.033e-01, 1.456e+00, 1.484e+00, 1.489e+00, 1.319e+00, 1.162e+00, 1.078e+00, 1.054e+00, 1.078e+00, 1.128e+00, 1.166e+00, 1.187e+00, 1.212e+00, 1.237e+00, 1.263e+00, 1.274e+00, 1.273e+00, 1.271e+00, 1.273e+00, 1.269e+00, 1.275e+00, 1.251e+00, 1.224e+00, 1.168e+00, 1.111e+00, 1.038e+00, 9.686e-01, 9.118e-01, 8.665e-01, 8.344e-01, 7.888e-01, 7.495e-01, 7.594e-01, 7.929e-01, 8.602e-01, 9.571e-01, 1.094e+00, 1.258e+00, 1.419e+00, 1.497e+00, 1.529e+00, 1.463e+00, 1.341e+00, 1.151e+00, 9.504e-01, 7.482e-01, 5.709e-01, 4.117e-01, 2.895e-01, 1.983e-01, 1.377e-01, 9.671e-02, 6.920e-02, 5.077e-02, 3.839e-02, 2.984e-02, 2.403e-02, 1.710e-02, 1.252e-02, 1.077e-02, 9.581e-03, 8.802e-03, 8.204e-03, 8.140e-03, 7.652e-03, 8.057e-03, 6.318e-03, 5.458e-03, 5.507e-03, 5.832e-03, 5.668e-03, 6.364e-03, 6.273e-03, 6.052e-03, 5.565e-03, 4.626e-03, 3.429e-03, 4.093e-03, 3.959e-03, 4.122e-03, 3.820e-03, 4.963e-03, 2.101e-03, 3.418e-03, 1.549e-03, 1.060e-03, 2.199e-03, 2.582e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToHadronic_TuneCP5down_PSweights_13TeV-powheg-pythia8",{2.609e-04, 2.804e-02, 4.064e-02, 4.852e-02, 6.866e-02, 9.920e-02, 1.019e-01, 1.277e-01, 1.055e-01, 3.152e-01, 4.856e-01, 6.254e-01, 6.574e-01, 6.772e-01, 7.346e-01, 8.029e-01, 9.165e-01, 1.006e+00, 1.086e+00, 1.147e+00, 1.202e+00, 1.261e+00, 1.304e+00, 1.333e+00, 1.348e+00, 1.348e+00, 1.359e+00, 1.371e+00, 1.365e+00, 1.351e+00, 1.327e+00, 1.272e+00, 1.213e+00, 1.134e+00, 1.059e+00, 1.004e+00, 9.416e-01, 9.131e-01, 8.579e-01, 8.212e-01, 8.274e-01, 8.696e-01, 9.466e-01, 1.044e+00, 1.196e+00, 1.367e+00, 1.540e+00, 1.619e+00, 1.632e+00, 1.574e+00, 1.402e+00, 1.230e+00, 1.019e+00, 7.898e-01, 5.956e-01, 4.312e-01, 3.064e-01, 2.102e-01, 1.443e-01, 1.037e-01, 7.443e-02, 5.246e-02, 4.114e-02, 3.046e-02, 2.391e-02, 1.818e-02, 1.279e-02, 1.095e-02, 9.360e-03, 8.273e-03, 7.991e-03, 6.402e-03, 5.968e-03, 7.683e-03, 4.821e-03, 2.165e-03, 2.368e-03, 1.454e-03, 9.074e-04, 3.889e-04, 2.512e-04, 2.332e-04, 2.331e-04, 2.224e-04, 4.564e-05, 1.065e-04, 4.728e-05, 7.163e-05, 1.052e-05, 4.916e-05, 1.490e-05, 3.562e-04, 1.708e-05, 2.340e-06, 6.990e-06, 4.866e-07, 2.115e-05, 1.452e-06, 7.915e-07, 3.200e-07, 0.000e+0}},
{"TTToHadronic_TuneCP5up_PSweights_13TeV-powheg-pythia8",{2.888e-04, 2.817e-02, 5.308e-02, 6.337e-02, 6.926e-02, 1.117e-01, 1.251e-01, 1.569e-01, 1.070e-01, 3.411e-01, 4.488e-01, 5.971e-01, 6.965e-01, 7.326e-01, 7.523e-01, 7.993e-01, 9.111e-01, 9.892e-01, 1.087e+00, 1.145e+00, 1.196e+00, 1.247e+00, 1.303e+00, 1.324e+00, 1.351e+00, 1.346e+00, 1.347e+00, 1.352e+00, 1.363e+00, 1.358e+00, 1.322e+00, 1.259e+00, 1.198e+00, 1.130e+00, 1.056e+00, 9.969e-01, 9.457e-01, 9.032e-01, 8.601e-01, 8.214e-01, 8.217e-01, 8.651e-01, 9.343e-01, 1.047e+00, 1.186e+00, 1.364e+00, 1.544e+00, 1.594e+00, 1.629e+00, 1.557e+00, 1.380e+00, 1.219e+00, 9.916e-01, 7.796e-01, 5.990e-01, 4.323e-01, 3.033e-01, 2.076e-01, 1.470e-01, 1.018e-01, 7.312e-02, 5.280e-02, 4.074e-02, 3.043e-02, 2.455e-02, 1.775e-02, 1.264e-02, 1.117e-02, 9.201e-03, 8.824e-03, 7.958e-03, 6.434e-03, 5.568e-03, 4.569e-03, 5.131e-03, 2.311e-03, 1.791e-03, 3.172e-03, 1.105e-03, 6.431e-04, 4.632e-04, 2.538e-04, 5.729e-04, 7.287e-05, 1.447e-04, 2.043e-04, 1.107e-04, 5.545e-05, 1.081e-05, 6.730e-06, 6.586e-06, 6.816e-06, 2.964e-05, 1.430e-05, 1.241e-06, 7.765e-07, 1.419e-05, 3.119e-05, 1.629e-07, 2.908e-07, 0.000e+0}},
{"TTToHadronic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8",{2.704e-04, 3.131e-02, 3.541e-02, 5.619e-02, 7.172e-02, 1.094e-01, 1.419e-01, 1.458e-01, 1.052e-01, 3.173e-01, 4.570e-01, 6.421e-01, 6.947e-01, 7.235e-01, 7.266e-01, 7.792e-01, 9.228e-01, 9.958e-01, 1.104e+00, 1.151e+00, 1.208e+00, 1.263e+00, 1.300e+00, 1.321e+00, 1.350e+00, 1.344e+00, 1.361e+00, 1.356e+00, 1.378e+00, 1.362e+00, 1.324e+00, 1.268e+00, 1.202e+00, 1.134e+00, 1.049e+00, 9.949e-01, 9.492e-01, 9.122e-01, 8.580e-01, 8.203e-01, 8.260e-01, 8.582e-01, 9.403e-01, 1.047e+00, 1.186e+00, 1.354e+00, 1.552e+00, 1.632e+00, 1.637e+00, 1.582e+00, 1.425e+00, 1.197e+00, 1.017e+00, 7.956e-01, 5.884e-01, 4.294e-01, 3.048e-01, 2.119e-01, 1.467e-01, 1.028e-01, 7.335e-02, 5.321e-02, 4.055e-02, 3.014e-02, 2.396e-02, 1.777e-02, 1.226e-02, 1.036e-02, 9.859e-03, 9.499e-03, 6.261e-03, 7.061e-03, 5.395e-03, 5.715e-03, 5.573e-03, 3.774e-03, 2.893e-03, 2.765e-03, 8.642e-04, 4.058e-04, 1.288e-04, 2.187e-04, 2.190e-04, 4.815e-05, 1.529e-04, 2.207e-04, 6.845e-05, 1.395e-05, 1.534e-05, 1.228e-05, 1.460e-05, 3.194e-05, 1.007e-03, 7.544e-06, 1.526e-06, 4.805e-07, 1.434e-05, 3.027e-06, 2.445e-07, 2.575e-07, 0.000e+0}},
{"TTToHadronic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8",{2.716e-04, 4.038e-02, 4.414e-02, 5.114e-02, 7.165e-02, 1.075e-01, 1.036e-01, 1.560e-01, 1.127e-01, 3.029e-01, 4.606e-01, 6.063e-01, 7.042e-01, 7.185e-01, 7.373e-01, 8.090e-01, 9.058e-01, 1.000e+00, 1.089e+00, 1.141e+00, 1.191e+00, 1.254e+00, 1.296e+00, 1.326e+00, 1.344e+00, 1.349e+00, 1.353e+00, 1.364e+00, 1.364e+00, 1.355e+00, 1.323e+00, 1.255e+00, 1.195e+00, 1.135e+00, 1.065e+00, 1.003e+00, 9.513e-01, 9.122e-01, 8.648e-01, 8.228e-01, 8.233e-01, 8.582e-01, 9.430e-01, 1.048e+00, 1.201e+00, 1.365e+00, 1.538e+00, 1.618e+00, 1.627e+00, 1.520e+00, 1.412e+00, 1.236e+00, 1.005e+00, 7.939e-01, 5.949e-01, 4.332e-01, 3.075e-01, 2.124e-01, 1.450e-01, 1.038e-01, 7.309e-02, 5.469e-02, 4.125e-02, 3.087e-02, 2.501e-02, 1.766e-02, 1.266e-02, 1.112e-02, 9.956e-03, 8.286e-03, 6.547e-03, 6.001e-03, 4.888e-03, 6.360e-03, 4.477e-03, 2.132e-03, 3.887e-03, 1.505e-03, 9.198e-04, 4.122e-04, 1.741e-04, 2.351e-04, 1.896e-04, 6.166e-05, 7.784e-05, 6.334e-05, 5.165e-05, 2.669e-05, 1.120e-05, 3.057e-05, 1.171e-05, 1.711e-04, 8.492e-04, 2.974e-06, 4.116e-06, 3.936e-07, 1.999e-05, 9.409e-06, 1.336e-06, 2.616e-07, 0.000e+0}},
{"TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.811e-01, 3.462e+00, 3.211e+00, 2.535e+00, 1.791e+00, 1.512e+00, 1.317e+00, 1.248e+00, 6.201e-01, 1.475e+00, 1.504e+00, 1.491e+00, 1.319e+00, 1.162e+00, 1.075e+00, 1.048e+00, 1.080e+00, 1.129e+00, 1.169e+00, 1.189e+00, 1.214e+00, 1.238e+00, 1.259e+00, 1.275e+00, 1.272e+00, 1.274e+00, 1.273e+00, 1.264e+00, 1.278e+00, 1.253e+00, 1.220e+00, 1.170e+00, 1.109e+00, 1.039e+00, 9.645e-01, 9.131e-01, 8.659e-01, 8.357e-01, 7.867e-01, 7.525e-01, 7.610e-01, 7.934e-01, 8.610e-01, 9.587e-01, 1.097e+00, 1.252e+00, 1.421e+00, 1.496e+00, 1.528e+00, 1.464e+00, 1.340e+00, 1.153e+00, 9.468e-01, 7.495e-01, 5.696e-01, 4.099e-01, 2.905e-01, 1.983e-01, 1.372e-01, 9.646e-02, 6.899e-02, 5.074e-02, 3.830e-02, 2.981e-02, 2.427e-02, 1.683e-02, 1.256e-02, 1.085e-02, 9.632e-03, 8.763e-03, 8.381e-03, 7.930e-03, 7.709e-03, 8.051e-03, 6.293e-03, 5.565e-03, 5.650e-03, 5.678e-03, 5.556e-03, 6.456e-03, 5.985e-03, 6.993e-03, 7.668e-03, 4.995e-03, 3.950e-03, 3.567e-03, 7.275e-03, 4.181e-03, 9.608e-03, 2.559e-03, 2.757e-03, 0.000e+00, 4.519e-04, 1.217e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.802e-01, 3.818e+00, 3.486e+00, 2.560e+00, 1.644e+00, 1.521e+00, 1.281e+00, 1.246e+00, 6.131e-01, 1.454e+00, 1.494e+00, 1.485e+00, 1.335e+00, 1.169e+00, 1.078e+00, 1.054e+00, 1.081e+00, 1.128e+00, 1.166e+00, 1.189e+00, 1.212e+00, 1.238e+00, 1.260e+00, 1.271e+00, 1.273e+00, 1.272e+00, 1.271e+00, 1.267e+00, 1.275e+00, 1.252e+00, 1.222e+00, 1.170e+00, 1.111e+00, 1.037e+00, 9.690e-01, 9.110e-01, 8.666e-01, 8.345e-01, 7.878e-01, 7.509e-01, 7.581e-01, 7.934e-01, 8.582e-01, 9.589e-01, 1.096e+00, 1.258e+00, 1.420e+00, 1.496e+00, 1.530e+00, 1.462e+00, 1.337e+00, 1.155e+00, 9.500e-01, 7.497e-01, 5.697e-01, 4.111e-01, 2.902e-01, 1.988e-01, 1.375e-01, 9.667e-02, 6.919e-02, 5.097e-02, 3.840e-02, 3.001e-02, 2.409e-02, 1.705e-02, 1.247e-02, 1.077e-02, 9.649e-03, 8.840e-03, 8.295e-03, 8.003e-03, 7.891e-03, 7.831e-03, 6.270e-03, 5.289e-03, 5.419e-03, 5.406e-03, 5.901e-03, 5.930e-03, 6.144e-03, 6.537e-03, 6.476e-03, 4.929e-03, 4.254e-03, 4.667e-03, 3.827e-03, 4.901e-03, 4.923e-03, 4.466e-03, 3.354e-03, 4.661e-03, 1.636e-03, 1.786e-03, 4.499e-03, 3.521e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToSemiLeptonic_TuneCP5_erdON_13TeV-powheg-pythia8",{1.946e-01, 4.348e+00, 3.571e+00, 2.709e+00, 1.525e+00, 1.446e+00, 1.339e+00, 1.323e+00, 6.360e-01, 1.485e+00, 1.518e+00, 1.482e+00, 1.332e+00, 1.164e+00, 1.088e+00, 1.057e+00, 1.081e+00, 1.129e+00, 1.163e+00, 1.187e+00, 1.208e+00, 1.234e+00, 1.263e+00, 1.274e+00, 1.275e+00, 1.272e+00, 1.273e+00, 1.262e+00, 1.279e+00, 1.252e+00, 1.221e+00, 1.172e+00, 1.111e+00, 1.038e+00, 9.689e-01, 9.118e-01, 8.672e-01, 8.351e-01, 7.858e-01, 7.524e-01, 7.567e-01, 7.918e-01, 8.626e-01, 9.538e-01, 1.097e+00, 1.265e+00, 1.414e+00, 1.495e+00, 1.534e+00, 1.463e+00, 1.333e+00, 1.158e+00, 9.502e-01, 7.516e-01, 5.698e-01, 4.096e-01, 2.904e-01, 1.975e-01, 1.375e-01, 9.607e-02, 6.909e-02, 5.062e-02, 3.867e-02, 2.973e-02, 2.422e-02, 1.693e-02, 1.262e-02, 1.080e-02, 9.578e-03, 8.922e-03, 8.393e-03, 7.991e-03, 7.748e-03, 7.597e-03, 6.708e-03, 5.356e-03, 5.632e-03, 5.469e-03, 6.474e-03, 6.174e-03, 6.266e-03, 6.887e-03, 7.473e-03, 5.228e-03, 3.971e-03, 4.512e-03, 3.738e-03, 1.181e-02, 3.703e-03, 4.601e-03, 2.267e-03, 6.915e-03, 1.393e-03, 1.251e-03, 1.483e-03, 4.353e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToSemiLeptonic_TuneCP5down_PSweights_13TeV-powheg-pythia8",{2.596e-04, 3.384e-02, 3.817e-02, 5.049e-02, 5.790e-02, 9.713e-02, 1.520e-01, 1.377e-01, 1.041e-01, 3.098e-01, 4.510e-01, 6.723e-01, 6.955e-01, 7.315e-01, 7.483e-01, 7.984e-01, 8.970e-01, 1.006e+00, 1.063e+00, 1.147e+00, 1.209e+00, 1.256e+00, 1.300e+00, 1.335e+00, 1.353e+00, 1.355e+00, 1.357e+00, 1.376e+00, 1.378e+00, 1.358e+00, 1.329e+00, 1.266e+00, 1.214e+00, 1.147e+00, 1.064e+00, 1.003e+00, 9.545e-01, 9.146e-01, 8.618e-01, 8.187e-01, 8.312e-01, 8.578e-01, 9.479e-01, 1.038e+00, 1.207e+00, 1.356e+00, 1.559e+00, 1.595e+00, 1.642e+00, 1.597e+00, 1.408e+00, 1.219e+00, 9.906e-01, 7.923e-01, 6.123e-01, 4.248e-01, 3.090e-01, 2.131e-01, 1.468e-01, 1.040e-01, 7.401e-02, 5.237e-02, 4.120e-02, 3.030e-02, 2.445e-02, 1.669e-02, 1.292e-02, 1.120e-02, 9.822e-03, 8.268e-03, 9.143e-03, 7.237e-03, 3.889e-03, 6.575e-03, 4.670e-03, 3.075e-03, 2.800e-03, 2.654e-03, 4.637e-04, 2.912e-04, 1.689e-04, 1.395e-04, 1.741e-04, 5.394e-05, 9.565e-05, 4.141e-05, 6.405e-05, 1.236e-05, 2.504e-05, 2.385e-06, 1.424e-03, 1.365e-03, 1.155e-03, 1.356e-05, 1.354e-06, 3.189e-07, 2.185e-05, 1.034e-06, 6.858e-07, 3.566e-07, 0.000e+0}},
{"TTToSemiLeptonic_TuneCP5up_PSweights_13TeV-powheg-pythia8",{3.047e-04, 5.786e-02, 4.981e-02, 7.256e-02, 7.712e-02, 1.218e-01, 1.537e-01, 1.609e-01, 1.186e-01, 3.566e-01, 4.940e-01, 6.099e-01, 7.041e-01, 7.416e-01, 7.343e-01, 7.761e-01, 8.746e-01, 9.847e-01, 1.078e+00, 1.152e+00, 1.206e+00, 1.259e+00, 1.285e+00, 1.322e+00, 1.335e+00, 1.345e+00, 1.335e+00, 1.362e+00, 1.368e+00, 1.351e+00, 1.321e+00, 1.262e+00, 1.200e+00, 1.128e+00, 1.047e+00, 9.903e-01, 9.388e-01, 9.122e-01, 8.585e-01, 8.221e-01, 8.152e-01, 8.618e-01, 9.372e-01, 1.043e+00, 1.192e+00, 1.362e+00, 1.521e+00, 1.599e+00, 1.608e+00, 1.572e+00, 1.396e+00, 1.199e+00, 9.868e-01, 7.931e-01, 6.000e-01, 4.322e-01, 3.046e-01, 2.112e-01, 1.467e-01, 1.030e-01, 7.338e-02, 5.380e-02, 4.111e-02, 3.081e-02, 2.405e-02, 1.791e-02, 1.208e-02, 1.090e-02, 9.616e-03, 8.796e-03, 8.288e-03, 5.958e-03, 5.670e-03, 5.069e-03, 3.652e-03, 3.651e-03, 1.955e-03, 1.922e-03, 1.613e-03, 3.283e-04, 1.781e-04, 2.080e-04, 1.314e-04, 3.258e-04, 8.278e-05, 5.895e-05, 3.552e-05, 1.349e-05, 1.083e-05, 3.353e-05, 1.470e-05, 7.019e-04, 1.576e-05, 1.952e-06, 1.330e-06, 2.477e-07, 1.646e-05, 1.338e-06, 1.041e-06, 3.216e-07, 0.000e+0}},
{"TTToSemiLeptonic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.907e-01, 3.584e+00, 3.040e+00, 2.527e+00, 1.688e+00, 1.536e+00, 1.297e+00, 1.258e+00, 6.160e-01, 1.476e+00, 1.494e+00, 1.499e+00, 1.334e+00, 1.169e+00, 1.077e+00, 1.053e+00, 1.081e+00, 1.126e+00, 1.166e+00, 1.189e+00, 1.211e+00, 1.240e+00, 1.262e+00, 1.269e+00, 1.272e+00, 1.270e+00, 1.270e+00, 1.266e+00, 1.276e+00, 1.251e+00, 1.220e+00, 1.171e+00, 1.109e+00, 1.040e+00, 9.685e-01, 9.105e-01, 8.682e-01, 8.348e-01, 7.885e-01, 7.509e-01, 7.597e-01, 7.931e-01, 8.591e-01, 9.579e-01, 1.095e+00, 1.256e+00, 1.420e+00, 1.493e+00, 1.534e+00, 1.466e+00, 1.339e+00, 1.159e+00, 9.525e-01, 7.489e-01, 5.698e-01, 4.112e-01, 2.902e-01, 1.980e-01, 1.374e-01, 9.648e-02, 6.916e-02, 5.080e-02, 3.834e-02, 2.991e-02, 2.399e-02, 1.708e-02, 1.246e-02, 1.080e-02, 9.654e-03, 8.699e-03, 8.340e-03, 8.033e-03, 7.839e-03, 8.029e-03, 6.351e-03, 5.283e-03, 5.547e-03, 5.496e-03, 6.055e-03, 6.343e-03, 6.319e-03, 7.097e-03, 6.107e-03, 4.811e-03, 3.965e-03, 4.245e-03, 4.134e-03, 3.743e-03, 6.201e-03, 5.394e-03, 1.748e-03, 1.013e-02, 1.021e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToSemiLeptonic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8",{2.988e-04, 2.881e-02, 4.309e-02, 5.216e-02, 6.881e-02, 1.049e-01, 1.410e-01, 1.642e-01, 1.165e-01, 2.891e-01, 5.218e-01, 6.467e-01, 6.879e-01, 7.314e-01, 7.710e-01, 8.254e-01, 9.146e-01, 1.017e+00, 1.094e+00, 1.142e+00, 1.204e+00, 1.261e+00, 1.303e+00, 1.328e+00, 1.330e+00, 1.331e+00, 1.331e+00, 1.354e+00, 1.364e+00, 1.341e+00, 1.318e+00, 1.264e+00, 1.194e+00, 1.131e+00, 1.053e+00, 9.820e-01, 9.411e-01, 9.099e-01, 8.519e-01, 8.168e-01, 8.158e-01, 8.575e-01, 9.337e-01, 1.041e+00, 1.187e+00, 1.358e+00, 1.551e+00, 1.608e+00, 1.630e+00, 1.566e+00, 1.398e+00, 1.216e+00, 9.864e-01, 7.985e-01, 5.883e-01, 4.328e-01, 2.963e-01, 2.120e-01, 1.439e-01, 1.024e-01, 7.364e-02, 5.393e-02, 4.123e-02, 3.041e-02, 2.313e-02, 1.781e-02, 1.292e-02, 1.056e-02, 1.005e-02, 7.931e-03, 7.572e-03, 6.117e-03, 4.756e-03, 5.431e-03, 3.223e-03, 3.338e-03, 2.305e-03, 1.958e-03, 1.832e-03, 9.028e-04, 2.178e-04, 2.158e-04, 2.631e-04, 4.610e-04, 8.927e-05, 1.685e-04, 4.482e-05, 1.922e-05, 1.160e-05, 9.174e-06, 1.483e-03, 1.734e-03, 8.115e-05, 6.207e-06, 2.673e-05, 4.712e-07, 2.058e-05, 4.610e-05, 1.401e-06, 3.117e-07, 0.000e+0}},
{"TTWH_TuneCP5_13TeV-madgraph-pythia8",{2.554e-04, 3.020e-02, 4.190e-02, 2.967e-01, 2.159e-01, 1.828e-01, 1.515e-01, 1.461e-01, 7.338e-02, 1.834e-01, 5.735e-01, 7.585e-01, 7.385e-01, 6.286e-01, 6.018e-01, 3.906e-01, 7.894e-01, 1.070e+00, 1.173e+00, 1.229e+00, 1.229e+00, 1.193e+00, 1.307e+00, 1.321e+00, 1.359e+00, 1.415e+00, 1.433e+00, 1.368e+00, 1.461e+00, 1.425e+00, 1.353e+00, 1.288e+00, 1.243e+00, 1.157e+00, 1.070e+00, 1.026e+00, 9.708e-01, 8.998e-01, 8.974e-01, 8.384e-01, 8.284e-01, 8.681e-01, 1.006e+00, 1.074e+00, 1.263e+00, 1.383e+00, 1.542e+00, 1.628e+00, 1.672e+00, 1.617e+00, 1.381e+00, 1.176e+00, 6.075e-01, 8.045e-01, 6.090e-01, 4.314e-01, 3.180e-01, 2.192e-01, 1.486e-01, 1.036e-01, 7.456e-02, 5.292e-02, 4.359e-02, 3.150e-02, 2.504e-02, 1.768e-02, 1.322e-02, 1.147e-02, 1.005e-02, 4.843e-03, 8.162e-03, 8.592e-03, 4.017e-03, 2.241e-03, 8.628e-03, 4.299e-03, 3.406e-03, 2.595e-03, 5.586e-03, 1.673e-02, 1.109e-02, 1.463e-02, 4.794e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 6.553e-04, 0.000e+00, 0.000e+00, 0.000e+00, 9.246e-05, 0.000e+00, 0.000e+00, 0.000e+00, 5.596e-06, 6.439e-06, 3.667e-06, 2.296e-07, 0.000e+0}},
{"TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8",{1.942e-01, 2.753e+00, 2.952e+00, 2.626e+00, 1.424e+00, 1.487e+00, 1.406e+00, 1.178e+00, 6.317e-01, 1.473e+00, 1.549e+00, 1.461e+00, 1.353e+00, 1.154e+00, 1.081e+00, 1.066e+00, 1.091e+00, 1.125e+00, 1.170e+00, 1.181e+00, 1.214e+00, 1.239e+00, 1.253e+00, 1.261e+00, 1.275e+00, 1.270e+00, 1.285e+00, 1.263e+00, 1.280e+00, 1.263e+00, 1.226e+00, 1.162e+00, 1.111e+00, 1.044e+00, 9.655e-01, 9.063e-01, 8.640e-01, 8.284e-01, 7.845e-01, 7.472e-01, 7.625e-01, 7.901e-01, 8.609e-01, 9.676e-01, 1.097e+00, 1.249e+00, 1.414e+00, 1.494e+00, 1.527e+00, 1.456e+00, 1.341e+00, 1.145e+00, 9.444e-01, 7.433e-01, 5.678e-01, 4.124e-01, 2.912e-01, 2.001e-01, 1.415e-01, 9.657e-02, 6.951e-02, 5.019e-02, 3.902e-02, 3.056e-02, 2.366e-02, 1.696e-02, 1.266e-02, 1.087e-02, 9.641e-03, 8.947e-03, 8.189e-03, 7.520e-03, 7.446e-03, 7.509e-03, 6.657e-03, 5.850e-03, 5.653e-03, 4.963e-03, 5.588e-03, 9.609e-03, 4.931e-03, 7.466e-03, 6.293e-03, 1.076e-02, 6.962e-03, 3.974e-03, 3.256e-03, 7.205e-03, 3.011e-03, 1.403e-03, -3.456e-03, 0.000e+00, 0.000e+00, 3.814e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",{1.196e-01, 3.842e+00, 2.673e+00, 2.114e+00, 1.391e+00, 1.689e+00, 9.939e-01, 1.172e+00, 6.387e-01, 1.589e+00, 1.447e+00, 1.528e+00, 1.426e+00, 1.172e+00, 1.126e+00, 1.049e+00, 1.076e+00, 1.127e+00, 1.194e+00, 1.170e+00, 1.208e+00, 1.247e+00, 1.263e+00, 1.271e+00, 1.291e+00, 1.281e+00, 1.271e+00, 1.269e+00, 1.277e+00, 1.255e+00, 1.208e+00, 1.175e+00, 1.121e+00, 1.037e+00, 9.857e-01, 8.943e-01, 8.604e-01, 8.540e-01, 7.981e-01, 7.348e-01, 7.543e-01, 7.774e-01, 8.580e-01, 9.335e-01, 1.098e+00, 1.266e+00, 1.443e+00, 1.484e+00, 1.544e+00, 1.459e+00, 1.309e+00, 1.143e+00, 9.758e-01, 7.455e-01, 5.578e-01, 3.962e-01, 2.868e-01, 1.953e-01, 1.395e-01, 9.678e-02, 7.154e-02, 5.207e-02, 3.726e-02, 2.936e-02, 2.574e-02, 1.781e-02, 1.253e-02, 1.115e-02, 8.425e-03, 8.174e-03, 7.346e-03, 7.581e-03, 8.104e-03, 9.333e-03, 4.828e-03, 4.895e-03, 5.668e-03, 5.061e-03, 5.312e-03, 3.909e-03, 4.922e-03, 4.637e-03, 5.319e-03, 1.386e-02, 2.989e-03, 2.880e-03, 3.670e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTWW_TuneCP5_13TeV-madgraph-pythia8",{7.033e-04, 5.772e-01, 6.426e-01, 4.893e-01, 2.429e-01, 2.166e-01, 3.724e-01, 4.252e-01, 2.228e-01, 5.841e-01, 6.034e-01, 5.884e-01, 5.759e-01, 5.445e-01, 6.798e-01, 7.602e-01, 9.141e-01, 1.032e+00, 1.148e+00, 1.115e+00, 1.188e+00, 1.227e+00, 1.278e+00, 1.247e+00, 1.374e+00, 1.363e+00, 1.380e+00, 1.412e+00, 1.377e+00, 1.374e+00, 1.234e+00, 1.303e+00, 1.201e+00, 1.150e+00, 1.064e+00, 1.027e+00, 9.396e-01, 9.283e-01, 8.592e-01, 8.035e-01, 8.355e-01, 8.667e-01, 9.533e-01, 1.042e+00, 1.185e+00, 1.099e+00, 1.582e+00, 1.644e+00, 1.724e+00, 1.585e+00, 1.331e+00, 1.133e+00, 9.544e-01, 7.582e-01, 5.949e-01, 2.526e-01, 2.960e-01, 2.041e-01, 1.431e-01, 1.000e-01, 7.121e-02, 5.312e-02, 4.084e-02, 3.141e-02, 2.601e-02, 1.844e-02, 1.410e-02, 1.106e-02, 5.710e-03, 9.571e-03, 8.653e-03, 8.180e-03, 1.172e-02, 9.131e-03, 6.104e-03, 5.988e-03, 4.163e-03, 5.790e-03, 3.591e-03, 6.845e-05, 7.395e-03, 4.876e-03, 4.795e-03, 2.062e-05, 1.347e-03, 3.032e-06, 0.000e+00, 1.046e-03, 0.000e+00, 1.113e-06, 0.000e+00, 1.530e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 2.584e-07, 0.000e+0}},
{"TTWZ_TuneCP5_13TeV-madgraph-pythia8",{2.264e-03, 2.731e-01, 2.006e-01, 1.755e-01, 5.545e-01, 4.849e-01, 4.229e-01, 3.478e-01, 2.282e-01, 4.834e-01, 5.215e-01, 4.925e-01, 4.540e-01, 7.166e-01, 7.775e-01, 9.475e-01, 9.996e-01, 1.105e+00, 1.142e+00, 1.153e+00, 1.249e+00, 1.275e+00, 1.250e+00, 1.314e+00, 1.342e+00, 1.290e+00, 1.300e+00, 1.322e+00, 1.346e+00, 1.305e+00, 1.279e+00, 1.186e+00, 1.142e+00, 1.075e+00, 1.031e+00, 9.884e-01, 9.079e-01, 8.905e-01, 8.238e-01, 7.990e-01, 8.009e-01, 8.148e-01, 9.196e-01, 9.914e-01, 1.063e+00, 1.358e+00, 1.567e+00, 1.606e+00, 1.608e+00, 1.430e+00, 1.408e+00, 1.003e+00, 9.926e-01, 7.812e-01, 5.951e-01, 4.188e-01, 2.975e-01, 1.208e-01, 1.416e-01, 9.715e-02, 7.189e-02, 5.105e-02, 3.734e-02, 3.128e-02, 2.533e-02, 1.742e-02, 1.244e-02, 1.095e-02, 9.884e-03, 8.801e-03, 9.065e-03, 8.944e-03, 7.912e-03, 7.190e-03, 5.812e-03, 4.785e-03, 5.908e-03, 5.370e-03, 6.277e-03, 5.571e-03, 4.431e-03, 7.305e-03, 0.000e+00, 1.560e-03, 2.018e-03, 1.296e-03, 0.000e+00, 5.274e-06, 6.546e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 2.236e-06, 3.216e-06, 0.000e+00, 2.949e-07, 0.000e+0}},
{"TTZH_TuneCP5_13TeV-madgraph-pythia8",{2.303e-03, 1.734e+00, 1.379e+00, 1.066e+00, 6.949e-01, 9.400e-01, 8.145e-01, 7.805e-01, 3.441e-01, 1.176e+00, 1.171e+00, 1.287e+00, 1.034e+00, 9.583e-01, 8.984e-01, 8.627e-01, 8.913e-01, 9.552e-01, 9.954e-01, 1.079e+00, 1.126e+00, 1.123e+00, 1.206e+00, 1.221e+00, 1.314e+00, 1.291e+00, 1.258e+00, 1.278e+00, 1.361e+00, 1.328e+00, 1.222e+00, 1.221e+00, 1.164e+00, 1.115e+00, 1.043e+00, 9.468e-01, 9.185e-01, 8.947e-01, 8.459e-01, 8.025e-01, 8.345e-01, 8.395e-01, 9.202e-01, 7.704e-01, 1.183e+00, 1.414e+00, 1.535e+00, 1.615e+00, 1.651e+00, 1.586e+00, 1.400e+00, 7.774e-01, 9.911e-01, 7.694e-01, 6.107e-01, 4.293e-01, 2.968e-01, 2.113e-01, 1.419e-01, 1.032e-01, 7.320e-02, 5.125e-02, 3.969e-02, 3.295e-02, 2.468e-02, 1.727e-02, 1.441e-02, 1.095e-02, 1.048e-02, 8.983e-03, 9.487e-03, 7.220e-03, 8.047e-03, 8.520e-03, 6.265e-03, 6.458e-03, 5.360e-03, 5.384e-03, 6.294e-03, 8.379e-03, 4.347e-05, 3.662e-03, 4.802e-03, 2.085e-03, 2.024e-03, 0.000e+00, 0.000e+00, 1.047e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 1.121e-05, 2.150e-06, 0.000e+00, 2.957e-07, 0.000e+0}},
{"TTZToLLNuNu_M-10_TuneCP5_PSweights_13TeV-amcatnlo-pythia8",{1.909e-01, 3.419e+00, 3.339e+00, 2.336e+00, 1.564e+00, 1.778e+00, 1.310e+00, 1.249e+00, 6.491e-01, 1.471e+00, 1.485e+00, 1.484e+00, 1.312e+00, 1.177e+00, 1.075e+00, 1.056e+00, 1.089e+00, 1.131e+00, 1.162e+00, 1.192e+00, 1.216e+00, 1.246e+00, 1.259e+00, 1.280e+00, 1.274e+00, 1.277e+00, 1.267e+00, 1.269e+00, 1.268e+00, 1.254e+00, 1.224e+00, 1.172e+00, 1.107e+00, 1.035e+00, 9.686e-01, 9.117e-01, 8.680e-01, 8.377e-01, 7.833e-01, 7.461e-01, 7.584e-01, 7.940e-01, 8.556e-01, 9.610e-01, 1.104e+00, 1.255e+00, 1.416e+00, 1.495e+00, 1.523e+00, 1.457e+00, 1.317e+00, 1.148e+00, 9.458e-01, 7.459e-01, 5.699e-01, 4.125e-01, 2.889e-01, 1.985e-01, 1.372e-01, 9.581e-02, 6.918e-02, 5.162e-02, 3.844e-02, 3.025e-02, 2.414e-02, 1.708e-02, 1.244e-02, 1.111e-02, 9.695e-03, 8.772e-03, 8.088e-03, 8.092e-03, 7.848e-03, 7.564e-03, 6.635e-03, 5.332e-03, 6.230e-03, 5.662e-03, 6.334e-03, 6.250e-03, 7.893e-03, 5.664e-03, 6.824e-03, 4.217e-03, 3.433e-03, 5.257e-03, 4.839e-03, 3.059e-03, 4.314e-03, 2.680e-03, 1.320e-03, 0.000e+00, 2.435e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8",{4.022e-01, 0.000e+00, 3.127e+00, -1.174e+01, 2.101e+00, 1.661e+00, 1.114e+00, 1.327e+00, 5.752e-01, 2.339e+00, 1.836e+00, 1.476e+00, 1.367e+00, 1.151e+00, 1.006e+00, 1.045e+00, 1.143e+00, 1.113e+00, 1.144e+00, 1.172e+00, 1.201e+00, 1.242e+00, 1.242e+00, 1.320e+00, 1.265e+00, 1.262e+00, 1.361e+00, 1.284e+00, 1.268e+00, 1.259e+00, 1.210e+00, 1.139e+00, 1.100e+00, 1.045e+00, 9.528e-01, 9.223e-01, 8.820e-01, 8.160e-01, 7.886e-01, 7.253e-01, 7.725e-01, 7.989e-01, 8.619e-01, 9.514e-01, 1.118e+00, 1.248e+00, 1.376e+00, 1.434e+00, 1.494e+00, 1.467e+00, 1.338e+00, 1.069e+00, 9.879e-01, 8.642e-01, 5.838e-01, 3.875e-01, 2.948e-01, 2.024e-01, 1.346e-01, 1.018e-01, 7.046e-02, 4.719e-02, 4.026e-02, 2.827e-02, 2.311e-02, 1.658e-02, 1.230e-02, 1.002e-02, 9.193e-03, 9.473e-03, 7.944e-03, 1.346e-02, 7.765e-03, 8.674e-03, 6.013e-03, 6.399e-03, 0.000e+00, 5.426e-03, 2.718e-03, 7.239e-03, -1.439e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, -6.784e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTZZ_TuneCP5_13TeV-madgraph-pythia8",{2.030e-04, 3.061e-01, 1.637e-01, 1.486e-01, 9.636e-02, 1.621e-01, 2.382e-01, 3.280e-01, 1.991e-01, 4.761e-01, 5.700e-01, 5.404e-01, 5.790e-01, 9.805e-01, 8.808e-01, 6.118e-01, 9.211e-01, 9.485e-01, 9.354e-01, 1.038e+00, 1.148e+00, 1.239e+00, 1.182e+00, 1.331e+00, 1.325e+00, 1.320e+00, 1.295e+00, 1.306e+00, 1.407e+00, 1.386e+00, 1.393e+00, 1.302e+00, 1.254e+00, 1.167e+00, 1.096e+00, 1.044e+00, 9.903e-01, 7.137e-01, 8.838e-01, 8.566e-01, 8.420e-01, 9.136e-01, 1.001e+00, 8.963e-01, 1.243e+00, 1.398e+00, 1.678e+00, 1.758e+00, 1.775e+00, 1.709e+00, 1.076e+00, 1.311e+00, 1.081e+00, 8.328e-01, 6.199e-01, 4.474e-01, 3.084e-01, 2.273e-01, 1.529e-01, 1.060e-01, 7.840e-02, 5.577e-02, 4.271e-02, 3.296e-02, 2.693e-02, 1.881e-02, 1.053e-02, 1.166e-02, 1.014e-02, 1.012e-02, 7.739e-03, 8.971e-03, 9.089e-03, 6.945e-03, 5.571e-03, 4.666e-03, 6.256e-03, 5.800e-03, 3.875e-03, 3.726e-03, 7.408e-03, 7.327e-03, 9.607e-03, 2.086e-03, 2.024e-03, 1.734e-04, 1.657e-03, 1.048e-03, 0.000e+00, 0.000e+00, 0.000e+00, 1.533e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 5.607e-06, 0.000e+00, 0.000e+00, 3.451e-07, 0.000e+0}},
{"WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8",{1.878e-01, 4.700e+00, 3.198e+00, 2.393e+00, 1.807e+00, 1.486e+00, 1.327e+00, 1.211e+00, 6.100e-01, 1.495e+00, 1.517e+00, 1.479e+00, 1.319e+00, 1.164e+00, 1.076e+00, 1.050e+00, 1.080e+00, 1.130e+00, 1.165e+00, 1.189e+00, 1.212e+00, 1.237e+00, 1.259e+00, 1.271e+00, 1.271e+00, 1.272e+00, 1.272e+00, 1.268e+00, 1.276e+00, 1.253e+00, 1.221e+00, 1.169e+00, 1.110e+00, 1.039e+00, 9.690e-01, 9.132e-01, 8.658e-01, 8.373e-01, 7.900e-01, 7.510e-01, 7.588e-01, 7.925e-01, 8.575e-01, 9.589e-01, 1.093e+00, 1.257e+00, 1.420e+00, 1.494e+00, 1.528e+00, 1.462e+00, 1.338e+00, 1.155e+00, 9.496e-01, 7.493e-01, 5.704e-01, 4.108e-01, 2.901e-01, 1.994e-01, 1.375e-01, 9.653e-02, 6.896e-02, 5.074e-02, 3.839e-02, 3.000e-02, 2.413e-02, 1.700e-02, 1.244e-02, 1.072e-02, 9.636e-03, 8.831e-03, 8.326e-03, 8.101e-03, 7.730e-03, 7.915e-03, 6.286e-03, 5.303e-03, 5.503e-03, 5.776e-03, 5.860e-03, 6.285e-03, 6.690e-03, 6.442e-03, 6.628e-03, 4.505e-03, 3.409e-03, 3.690e-03, 4.449e-03, 6.122e-03, 3.433e-03, 1.930e-03, 3.565e-03, 5.076e-03, 3.068e-03, 1.102e-03, 0.000e+00, 1.917e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8",{1.913e-01, 4.255e+00, 3.444e+00, 2.481e+00, 1.640e+00, 1.532e+00, 1.288e+00, 1.270e+00, 5.997e-01, 1.442e+00, 1.477e+00, 1.476e+00, 1.330e+00, 1.169e+00, 1.083e+00, 1.051e+00, 1.078e+00, 1.126e+00, 1.166e+00, 1.188e+00, 1.211e+00, 1.239e+00, 1.256e+00, 1.271e+00, 1.274e+00, 1.274e+00, 1.271e+00, 1.267e+00, 1.274e+00, 1.254e+00, 1.220e+00, 1.167e+00, 1.113e+00, 1.037e+00, 9.689e-01, 9.130e-01, 8.681e-01, 8.336e-01, 7.865e-01, 7.516e-01, 7.577e-01, 7.949e-01, 8.594e-01, 9.562e-01, 1.097e+00, 1.258e+00, 1.421e+00, 1.493e+00, 1.534e+00, 1.461e+00, 1.341e+00, 1.156e+00, 9.519e-01, 7.507e-01, 5.693e-01, 4.101e-01, 2.896e-01, 1.981e-01, 1.374e-01, 9.659e-02, 6.938e-02, 5.074e-02, 3.867e-02, 2.989e-02, 2.413e-02, 1.713e-02, 1.251e-02, 1.076e-02, 9.503e-03, 8.768e-03, 8.259e-03, 8.064e-03, 7.856e-03, 7.777e-03, 6.306e-03, 5.442e-03, 5.529e-03, 5.516e-03, 6.169e-03, 5.712e-03, 6.266e-03, 7.418e-03, 7.192e-03, 4.264e-03, 4.179e-03, 5.316e-03, 3.595e-03, 6.186e-03, 2.908e-03, 3.336e-03, 3.338e-03, 5.431e-03, 1.969e-03, 1.179e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8",{1.893e-01, 4.111e+00, 3.265e+00, 2.650e+00, 1.614e+00, 1.489e+00, 1.286e+00, 1.242e+00, 6.233e-01, 1.437e+00, 1.485e+00, 1.483e+00, 1.338e+00, 1.164e+00, 1.076e+00, 1.050e+00, 1.080e+00, 1.130e+00, 1.168e+00, 1.188e+00, 1.213e+00, 1.239e+00, 1.262e+00, 1.272e+00, 1.272e+00, 1.269e+00, 1.273e+00, 1.266e+00, 1.276e+00, 1.250e+00, 1.221e+00, 1.171e+00, 1.110e+00, 1.038e+00, 9.688e-01, 9.133e-01, 8.687e-01, 8.352e-01, 7.870e-01, 7.480e-01, 7.603e-01, 7.925e-01, 8.593e-01, 9.609e-01, 1.091e+00, 1.256e+00, 1.416e+00, 1.495e+00, 1.528e+00, 1.461e+00, 1.340e+00, 1.154e+00, 9.491e-01, 7.498e-01, 5.704e-01, 4.106e-01, 2.895e-01, 1.986e-01, 1.373e-01, 9.674e-02, 6.937e-02, 5.068e-02, 3.836e-02, 3.009e-02, 2.404e-02, 1.719e-02, 1.254e-02, 1.088e-02, 9.526e-03, 8.853e-03, 8.373e-03, 8.004e-03, 7.929e-03, 7.867e-03, 6.149e-03, 5.388e-03, 5.507e-03, 5.840e-03, 5.703e-03, 6.378e-03, 6.406e-03, 6.041e-03, 6.583e-03, 5.059e-03, 4.319e-03, 4.639e-03, 5.043e-03, 5.162e-03, 3.576e-03, 1.055e-02, 5.199e-03, 3.965e-03, 3.195e-03, 1.913e-03, 3.402e-03, 6.656e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8",{1.899e-01, 3.953e+00, 3.873e+00, 2.681e+00, 1.643e+00, 1.482e+00, 1.303e+00, 1.283e+00, 6.122e-01, 1.433e+00, 1.499e+00, 1.483e+00, 1.326e+00, 1.166e+00, 1.080e+00, 1.051e+00, 1.074e+00, 1.126e+00, 1.163e+00, 1.187e+00, 1.212e+00, 1.238e+00, 1.261e+00, 1.268e+00, 1.274e+00, 1.274e+00, 1.270e+00, 1.269e+00, 1.277e+00, 1.252e+00, 1.224e+00, 1.171e+00, 1.110e+00, 1.038e+00, 9.698e-01, 9.114e-01, 8.653e-01, 8.348e-01, 7.896e-01, 7.499e-01, 7.574e-01, 7.922e-01, 8.594e-01, 9.566e-01, 1.096e+00, 1.260e+00, 1.419e+00, 1.496e+00, 1.534e+00, 1.466e+00, 1.340e+00, 1.157e+00, 9.516e-01, 7.506e-01, 5.693e-01, 4.110e-01, 2.895e-01, 1.974e-01, 1.380e-01, 9.661e-02, 6.949e-02, 5.089e-02, 3.837e-02, 2.965e-02, 2.417e-02, 1.699e-02, 1.248e-02, 1.080e-02, 9.541e-03, 8.778e-03, 8.269e-03, 8.060e-03, 7.843e-03, 7.899e-03, 6.202e-03, 5.430e-03, 5.553e-03, 5.352e-03, 5.700e-03, 6.046e-03, 5.834e-03, 6.622e-03, 6.070e-03, 4.560e-03, 4.739e-03, 6.189e-03, 3.287e-03, 4.675e-03, 2.605e-03, 5.826e-03, 4.484e-03, 3.648e-03, 6.615e-03, 1.320e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8",{1.899e-01, 3.543e+00, 3.520e+00, 2.642e+00, 1.581e+00, 1.495e+00, 1.296e+00, 1.289e+00, 6.150e-01, 1.486e+00, 1.474e+00, 1.479e+00, 1.324e+00, 1.167e+00, 1.074e+00, 1.054e+00, 1.080e+00, 1.133e+00, 1.165e+00, 1.186e+00, 1.215e+00, 1.238e+00, 1.261e+00, 1.271e+00, 1.273e+00, 1.274e+00, 1.268e+00, 1.265e+00, 1.275e+00, 1.254e+00, 1.223e+00, 1.171e+00, 1.109e+00, 1.036e+00, 9.683e-01, 9.107e-01, 8.671e-01, 8.344e-01, 7.894e-01, 7.523e-01, 7.561e-01, 7.949e-01, 8.589e-01, 9.589e-01, 1.095e+00, 1.253e+00, 1.420e+00, 1.494e+00, 1.534e+00, 1.461e+00, 1.336e+00, 1.154e+00, 9.528e-01, 7.531e-01, 5.698e-01, 4.117e-01, 2.903e-01, 1.985e-01, 1.375e-01, 9.617e-02, 6.911e-02, 5.079e-02, 3.843e-02, 2.984e-02, 2.402e-02, 1.707e-02, 1.242e-02, 1.086e-02, 9.660e-03, 8.759e-03, 8.298e-03, 8.004e-03, 7.673e-03, 7.920e-03, 6.424e-03, 5.314e-03, 5.516e-03, 5.349e-03, 5.832e-03, 5.663e-03, 5.797e-03, 6.295e-03, 7.324e-03, 5.018e-03, 4.021e-03, 5.118e-03, 4.375e-03, 3.544e-03, 3.741e-03, 3.680e-03, 3.885e-03, 2.074e-03, 2.006e-03, 1.501e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8",{1.711e-01, 3.594e+00, 3.093e+00, 2.601e+00, 1.589e+00, 1.441e+00, 1.296e+00, 1.252e+00, 6.094e-01, 1.446e+00, 1.500e+00, 1.471e+00, 1.332e+00, 1.165e+00, 1.075e+00, 1.055e+00, 1.081e+00, 1.127e+00, 1.166e+00, 1.190e+00, 1.212e+00, 1.240e+00, 1.261e+00, 1.271e+00, 1.275e+00, 1.275e+00, 1.271e+00, 1.265e+00, 1.274e+00, 1.250e+00, 1.222e+00, 1.170e+00, 1.106e+00, 1.039e+00, 9.693e-01, 9.130e-01, 8.675e-01, 8.347e-01, 7.890e-01, 7.505e-01, 7.590e-01, 7.920e-01, 8.588e-01, 9.599e-01, 1.092e+00, 1.260e+00, 1.418e+00, 1.489e+00, 1.528e+00, 1.462e+00, 1.335e+00, 1.156e+00, 9.475e-01, 7.490e-01, 5.692e-01, 4.120e-01, 2.903e-01, 1.986e-01, 1.383e-01, 9.633e-02, 6.924e-02, 5.100e-02, 3.853e-02, 2.984e-02, 2.411e-02, 1.705e-02, 1.249e-02, 1.076e-02, 9.660e-03, 8.825e-03, 8.295e-03, 7.969e-03, 7.927e-03, 8.048e-03, 6.381e-03, 5.146e-03, 5.648e-03, 5.484e-03, 5.505e-03, 6.079e-03, 6.374e-03, 5.975e-03, 6.869e-03, 4.352e-03, 4.725e-03, 4.714e-03, 4.314e-03, 4.431e-03, 3.030e-03, 4.142e-03, 2.834e-03, 3.890e-03, 3.135e-03, 0.000e+00, 1.669e-03, 1.959e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WW_TuneCP5_13TeV-pythia8",{1.747e-01, 3.754e+00, 3.329e+00, 2.355e+00, 1.696e+00, 1.497e+00, 1.243e+00, 1.161e+00, 6.304e-01, 1.463e+00, 1.500e+00, 1.485e+00, 1.340e+00, 1.163e+00, 1.075e+00, 1.056e+00, 1.083e+00, 1.133e+00, 1.161e+00, 1.192e+00, 1.211e+00, 1.240e+00, 1.261e+00, 1.273e+00, 1.272e+00, 1.270e+00, 1.272e+00, 1.263e+00, 1.272e+00, 1.254e+00, 1.220e+00, 1.169e+00, 1.111e+00, 1.037e+00, 9.708e-01, 9.098e-01, 8.665e-01, 8.359e-01, 7.902e-01, 7.517e-01, 7.575e-01, 7.910e-01, 8.594e-01, 9.547e-01, 1.092e+00, 1.255e+00, 1.425e+00, 1.496e+00, 1.535e+00, 1.463e+00, 1.344e+00, 1.154e+00, 9.460e-01, 7.464e-01, 5.712e-01, 4.131e-01, 2.907e-01, 1.988e-01, 1.374e-01, 9.660e-02, 6.931e-02, 5.074e-02, 3.861e-02, 2.972e-02, 2.417e-02, 1.708e-02, 1.251e-02, 1.077e-02, 9.748e-03, 8.891e-03, 8.086e-03, 8.099e-03, 7.509e-03, 7.948e-03, 6.661e-03, 5.426e-03, 5.356e-03, 5.449e-03, 5.574e-03, 5.704e-03, 5.771e-03, 5.596e-03, 5.198e-03, 4.780e-03, 5.257e-03, 6.753e-03, 3.397e-03, 4.534e-03, 8.525e-03, 3.973e-03, 3.262e-03, 5.971e-03, 9.021e-04, 7.201e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WZ_TuneCP5_13TeV-pythia8",{2.885e-04, 9.426e-03, 3.709e-02, 6.739e-02, 9.283e-02, 1.810e-01, 1.933e-01, 2.232e-01, 1.095e-01, 4.127e-01, 4.222e-01, 6.463e-01, 7.086e-01, 7.589e-01, 7.401e-01, 7.535e-01, 8.487e-01, 1.014e+00, 1.090e+00, 1.144e+00, 1.238e+00, 1.270e+00, 1.304e+00, 1.329e+00, 1.353e+00, 1.354e+00, 1.340e+00, 1.366e+00, 1.392e+00, 1.375e+00, 1.305e+00, 1.262e+00, 1.203e+00, 1.138e+00, 1.076e+00, 1.014e+00, 9.526e-01, 9.096e-01, 8.524e-01, 8.366e-01, 8.149e-01, 8.498e-01, 9.367e-01, 1.070e+00, 1.217e+00, 1.370e+00, 1.555e+00, 1.651e+00, 1.661e+00, 1.619e+00, 1.441e+00, 1.254e+00, 1.031e+00, 7.733e-01, 6.002e-01, 4.269e-01, 3.139e-01, 2.145e-01, 1.491e-01, 1.047e-01, 7.117e-02, 5.268e-02, 3.779e-02, 2.871e-02, 2.464e-02, 1.834e-02, 1.201e-02, 1.115e-02, 7.759e-03, 8.828e-03, 4.914e-03, 4.979e-03, 4.248e-03, 8.633e-03, 3.551e-03, 1.225e-03, 8.479e-04, 5.544e-03, 2.923e-04, 2.167e-04, 4.406e-04, 9.199e-05, 1.197e-04, 2.637e-05, 4.199e-03, 3.283e-05, 2.446e-05, 3.924e-05, 2.652e-06, 1.347e-05, 3.182e-06, 2.517e-04, 6.085e-04, 5.464e-04, 2.159e-04, 9.482e-07, 3.683e-05, 1.271e-04, 2.586e-07, 2.874e-07, 0.000e+0}},
{"ZZ_TuneCP5_13TeV-pythia8",{2.034e-01, 4.570e+00, 3.455e+00, 2.433e+00, 2.113e+00, 1.497e+00, 1.226e+00, 1.242e+00, 6.374e-01, 1.528e+00, 1.536e+00, 1.507e+00, 1.329e+00, 1.159e+00, 1.065e+00, 1.041e+00, 1.082e+00, 1.144e+00, 1.158e+00, 1.193e+00, 1.211e+00, 1.235e+00, 1.258e+00, 1.277e+00, 1.272e+00, 1.264e+00, 1.269e+00, 1.273e+00, 1.269e+00, 1.264e+00, 1.223e+00, 1.173e+00, 1.104e+00, 1.033e+00, 9.748e-01, 9.112e-01, 8.653e-01, 8.366e-01, 7.900e-01, 7.484e-01, 7.577e-01, 7.925e-01, 8.630e-01, 9.599e-01, 1.088e+00, 1.262e+00, 1.443e+00, 1.488e+00, 1.536e+00, 1.452e+00, 1.325e+00, 1.154e+00, 9.670e-01, 7.471e-01, 5.738e-01, 4.083e-01, 2.878e-01, 1.975e-01, 1.365e-01, 9.673e-02, 6.975e-02, 5.090e-02, 3.868e-02, 3.004e-02, 2.368e-02, 1.673e-02, 1.234e-02, 1.077e-02, 9.694e-03, 8.566e-03, 8.172e-03, 7.909e-03, 7.901e-03, 7.859e-03, 6.528e-03, 5.654e-03, 5.522e-03, 6.173e-03, 6.403e-03, 7.198e-03, 7.156e-03, 5.899e-03, 3.712e-03, 4.030e-03, 2.445e-03, 6.280e-03, 8.004e-03, 1.687e-03, 3.171e-03, 3.941e-03, 1.213e-03, 1.481e-03, 8.949e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8",{1.803e-01, 3.458e+00, 3.320e+00, 2.672e+00, 1.673e+00, 1.617e+00, 1.216e+00, 1.254e+00, 5.875e-01, 1.508e+00, 1.485e+00, 1.469e+00, 1.337e+00, 1.158e+00, 1.083e+00, 1.052e+00, 1.077e+00, 1.128e+00, 1.165e+00, 1.185e+00, 1.215e+00, 1.238e+00, 1.267e+00, 1.269e+00, 1.272e+00, 1.267e+00, 1.272e+00, 1.268e+00, 1.274e+00, 1.250e+00, 1.219e+00, 1.169e+00, 1.112e+00, 1.039e+00, 9.677e-01, 9.125e-01, 8.686e-01, 8.354e-01, 7.882e-01, 7.527e-01, 7.564e-01, 7.919e-01, 8.570e-01, 9.614e-01, 1.101e+00, 1.253e+00, 1.426e+00, 1.490e+00, 1.537e+00, 1.467e+00, 1.327e+00, 1.145e+00, 9.504e-01, 7.503e-01, 5.704e-01, 4.090e-01, 2.908e-01, 1.991e-01, 1.382e-01, 9.642e-02, 6.952e-02, 5.087e-02, 3.848e-02, 2.981e-02, 2.406e-02, 1.711e-02, 1.247e-02, 1.064e-02, 9.808e-03, 8.913e-03, 8.170e-03, 8.021e-03, 8.009e-03, 7.519e-03, 6.414e-03, 5.711e-03, 5.312e-03, 5.423e-03, 5.859e-03, 5.321e-03, 5.620e-03, 5.984e-03, 6.974e-03, 4.543e-03, 4.534e-03, 7.841e-03, 4.640e-03, 2.737e-03, 3.677e-03, 7.996e-03, 1.641e-03, 0.000e+00, 1.816e-03, 7.246e-04, 0.000e+00, 7.564e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8",{1.814e-01, 4.869e+00, 3.328e+00, 2.649e+00, 1.539e+00, 1.459e+00, 1.240e+00, 1.245e+00, 6.164e-01, 1.457e+00, 1.487e+00, 1.486e+00, 1.338e+00, 1.172e+00, 1.080e+00, 1.049e+00, 1.083e+00, 1.127e+00, 1.162e+00, 1.192e+00, 1.214e+00, 1.236e+00, 1.264e+00, 1.269e+00, 1.270e+00, 1.271e+00, 1.270e+00, 1.267e+00, 1.275e+00, 1.251e+00, 1.224e+00, 1.169e+00, 1.110e+00, 1.040e+00, 9.670e-01, 9.113e-01, 8.653e-01, 8.359e-01, 7.899e-01, 7.515e-01, 7.573e-01, 7.931e-01, 8.636e-01, 9.604e-01, 1.094e+00, 1.256e+00, 1.421e+00, 1.503e+00, 1.522e+00, 1.462e+00, 1.344e+00, 1.151e+00, 9.522e-01, 7.464e-01, 5.692e-01, 4.098e-01, 2.902e-01, 1.990e-01, 1.377e-01, 9.661e-02, 6.950e-02, 5.084e-02, 3.821e-02, 3.001e-02, 2.393e-02, 1.717e-02, 1.241e-02, 1.069e-02, 9.439e-03, 8.829e-03, 8.278e-03, 7.919e-03, 8.173e-03, 8.321e-03, 6.351e-03, 5.280e-03, 5.702e-03, 5.654e-03, 5.687e-03, 6.971e-03, 6.876e-03, 7.289e-03, 5.101e-03, 4.640e-03, 4.187e-03, 4.087e-03, 5.009e-03, 4.116e-03, 4.300e-03, 1.781e-03, 3.290e-03, 6.023e-03, 9.100e-04, 2.179e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}}
};

    std::unordered_map<std::string, std::vector<float>> pileupweightsDn = { // 69.2 - 4.6%
{"DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8",{5.442e-04, 1.917e-01, 8.522e-02, 1.016e-01, 8.975e-02, 7.892e-02, 5.881e-02, 1.769e-01, 1.507e-01, 4.431e-01, 7.086e-01, 1.173e+00, 8.420e-01, 8.414e-01, 8.254e-01, 8.910e-01, 1.038e+00, 1.155e+00, 1.307e+00, 1.285e+00, 1.392e+00, 1.404e+00, 1.433e+00, 1.450e+00, 1.482e+00, 1.490e+00, 1.257e+00, 1.452e+00, 1.450e+00, 1.402e+00, 1.319e+00, 1.238e+00, 1.125e+00, 1.023e+00, 9.612e-01, 8.986e-01, 8.495e-01, 8.262e-01, 7.515e-01, 7.846e-01, 7.553e-01, 9.243e-01, 9.966e-01, 1.218e+00, 1.403e+00, 1.561e+00, 1.610e+00, 1.611e+00, 1.502e+00, 1.262e+00, 9.683e-01, 7.556e-01, 5.432e-01, 3.836e-01, 2.596e-01, 1.528e-01, 1.069e-01, 6.729e-02, 4.427e-02, 2.538e-02, 1.990e-02, 1.376e-02, 1.016e-02, 7.047e-03, 6.298e-03, 4.594e-03, 3.170e-03, 2.830e-03, 2.643e-03, 2.578e-03, 2.397e-03, 1.865e-03, 2.800e-04, 2.177e-03, 1.168e-04, 1.525e-03, 1.291e-03, 1.170e-03, 5.334e-05, 2.415e-05, 1.960e-03, 2.975e-04, 1.345e-03, 4.157e-04, 2.037e-03, 6.177e-04, 0.000e+00, 4.410e-04, 1.880e-06, 0.000e+00, 8.695e-05, 0.000e+00, 0.000e+00, 1.554e-05, 0.000e+00, 0.000e+00, 2.511e-06, 1.336e-06, 0.000e+00, 1.109e-08, 0.000e+0}},
{"DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8",{1.849e-01, 4.546e+00, 4.543e+00, 2.289e+00, 1.790e+00, 1.736e+00, 1.351e+00, 1.406e+00, 9.077e-01, 2.178e+00, 2.154e+00, 2.059e+00, 1.735e+00, 1.537e+00, 1.440e+00, 1.422e+00, 1.442e+00, 1.430e+00, 1.421e+00, 1.408e+00, 1.390e+00, 1.387e+00, 1.394e+00, 1.394e+00, 1.394e+00, 1.383e+00, 1.362e+00, 1.328e+00, 1.308e+00, 1.255e+00, 1.205e+00, 1.126e+00, 1.042e+00, 9.563e-01, 8.764e-01, 8.178e-01, 7.734e-01, 7.459e-01, 7.142e-01, 7.034e-01, 7.467e-01, 8.275e-01, 9.439e-01, 1.091e+00, 1.244e+00, 1.390e+00, 1.483e+00, 1.436e+00, 1.323e+00, 1.126e+00, 9.070e-01, 6.905e-01, 5.005e-01, 3.506e-01, 2.385e-01, 1.551e-01, 9.946e-02, 6.288e-02, 4.082e-02, 2.687e-02, 1.838e-02, 1.290e-02, 9.519e-03, 7.319e-03, 5.804e-03, 4.141e-03, 3.024e-03, 2.641e-03, 2.421e-03, 2.270e-03, 2.104e-03, 2.072e-03, 2.022e-03, 2.004e-03, 1.600e-03, 1.297e-03, 1.253e-03, 1.307e-03, 1.199e-03, 1.355e-03, 1.286e-03, 1.142e-03, 1.352e-03, 8.874e-04, 7.679e-04, 1.020e-03, 5.594e-04, 8.497e-04, 6.427e-04, 6.547e-04, 1.508e-03, 4.294e-04, 9.676e-05, 2.695e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8",{2.615e-01, 3.865e+00, 6.348e+00, 3.921e+00, 1.808e+00, 1.667e+00, 1.183e+00, 1.396e+00, 1.035e+00, 2.259e+00, 2.045e+00, 2.073e+00, 1.697e+00, 1.506e+00, 1.451e+00, 1.457e+00, 1.465e+00, 1.422e+00, 1.401e+00, 1.392e+00, 1.387e+00, 1.372e+00, 1.381e+00, 1.399e+00, 1.403e+00, 1.392e+00, 1.361e+00, 1.350e+00, 1.307e+00, 1.242e+00, 1.225e+00, 1.110e+00, 1.055e+00, 9.634e-01, 8.820e-01, 8.264e-01, 7.880e-01, 7.423e-01, 7.137e-01, 6.859e-01, 7.409e-01, 8.312e-01, 9.370e-01, 1.090e+00, 1.267e+00, 1.383e+00, 1.493e+00, 1.436e+00, 1.301e+00, 1.130e+00, 8.897e-01, 6.779e-01, 5.067e-01, 3.527e-01, 2.385e-01, 1.569e-01, 9.719e-02, 6.225e-02, 4.128e-02, 2.670e-02, 1.838e-02, 1.288e-02, 9.458e-03, 7.347e-03, 5.697e-03, 4.012e-03, 3.080e-03, 2.696e-03, 2.442e-03, 2.249e-03, 2.201e-03, 2.229e-03, 2.048e-03, 1.997e-03, 1.499e-03, 1.196e-03, 9.802e-04, 1.038e-03, 9.181e-04, 1.280e-03, 1.275e-03, 9.355e-04, 1.167e-03, 5.409e-04, 4.417e-04, 0.000e+00, 4.826e-04, 2.869e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8",{2.015e-01, 5.547e+00, 4.734e+00, 2.499e+00, 1.771e+00, 1.687e+00, 1.320e+00, 1.391e+00, 8.830e-01, 2.174e+00, 2.157e+00, 2.061e+00, 1.752e+00, 1.538e+00, 1.437e+00, 1.426e+00, 1.442e+00, 1.430e+00, 1.424e+00, 1.406e+00, 1.391e+00, 1.388e+00, 1.388e+00, 1.392e+00, 1.390e+00, 1.379e+00, 1.360e+00, 1.325e+00, 1.309e+00, 1.258e+00, 1.203e+00, 1.125e+00, 1.045e+00, 9.559e-01, 8.765e-01, 8.190e-01, 7.735e-01, 7.475e-01, 7.156e-01, 7.055e-01, 7.481e-01, 8.270e-01, 9.431e-01, 1.089e+00, 1.252e+00, 1.400e+00, 1.485e+00, 1.419e+00, 1.322e+00, 1.126e+00, 9.058e-01, 6.869e-01, 5.001e-01, 3.495e-01, 2.375e-01, 1.547e-01, 9.955e-02, 6.342e-02, 4.070e-02, 2.709e-02, 1.830e-02, 1.295e-02, 9.521e-03, 7.234e-03, 5.824e-03, 4.128e-03, 3.050e-03, 2.650e-03, 2.401e-03, 2.270e-03, 2.120e-03, 2.039e-03, 2.059e-03, 2.015e-03, 1.553e-03, 1.259e-03, 1.302e-03, 1.266e-03, 1.258e-03, 1.162e-03, 1.166e-03, 1.148e-03, 1.199e-03, 9.624e-04, 6.856e-04, 6.572e-04, 8.739e-04, 6.061e-04, 5.348e-04, 4.151e-04, 2.868e-04, 2.042e-04, 1.534e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8",{2.129e-01, 4.117e+00, 4.330e+00, 2.700e+00, 2.026e+00, 1.661e+00, 1.316e+00, 1.443e+00, 8.735e-01, 2.150e+00, 2.207e+00, 2.067e+00, 1.749e+00, 1.534e+00, 1.442e+00, 1.416e+00, 1.433e+00, 1.431e+00, 1.424e+00, 1.414e+00, 1.398e+00, 1.392e+00, 1.394e+00, 1.387e+00, 1.391e+00, 1.379e+00, 1.362e+00, 1.326e+00, 1.304e+00, 1.255e+00, 1.205e+00, 1.124e+00, 1.043e+00, 9.580e-01, 8.783e-01, 8.177e-01, 7.725e-01, 7.466e-01, 7.158e-01, 7.045e-01, 7.462e-01, 8.283e-01, 9.458e-01, 1.090e+00, 1.251e+00, 1.395e+00, 1.485e+00, 1.435e+00, 1.320e+00, 1.119e+00, 9.050e-01, 6.895e-01, 5.004e-01, 3.493e-01, 2.380e-01, 1.548e-01, 9.949e-02, 6.305e-02, 4.065e-02, 2.695e-02, 1.841e-02, 1.297e-02, 9.470e-03, 7.265e-03, 5.832e-03, 4.139e-03, 3.047e-03, 2.647e-03, 2.407e-03, 2.269e-03, 2.121e-03, 2.085e-03, 1.936e-03, 1.982e-03, 1.528e-03, 1.324e-03, 1.247e-03, 1.286e-03, 1.371e-03, 1.129e-03, 1.223e-03, 1.413e-03, 1.263e-03, 8.221e-04, 6.106e-04, 7.567e-04, 6.148e-04, 5.177e-04, 7.310e-04, 4.255e-04, 1.225e-03, 6.977e-04, 3.930e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8",{2.014e-01, 6.867e+00, 5.585e+00, 2.447e+00, 2.035e+00, 1.653e+00, 1.456e+00, 1.656e+00, 9.039e-01, 2.215e+00, 2.221e+00, 2.063e+00, 1.700e+00, 1.547e+00, 1.440e+00, 1.414e+00, 1.418e+00, 1.439e+00, 1.424e+00, 1.404e+00, 1.395e+00, 1.386e+00, 1.393e+00, 1.398e+00, 1.396e+00, 1.379e+00, 1.362e+00, 1.318e+00, 1.310e+00, 1.261e+00, 1.200e+00, 1.123e+00, 1.044e+00, 9.583e-01, 8.776e-01, 8.186e-01, 7.764e-01, 7.431e-01, 7.154e-01, 7.037e-01, 7.419e-01, 8.343e-01, 9.451e-01, 1.090e+00, 1.252e+00, 1.391e+00, 1.485e+00, 1.424e+00, 1.321e+00, 1.120e+00, 9.150e-01, 6.909e-01, 4.986e-01, 3.523e-01, 2.354e-01, 1.541e-01, 9.951e-02, 6.362e-02, 4.062e-02, 2.701e-02, 1.840e-02, 1.295e-02, 9.612e-03, 7.223e-03, 5.847e-03, 4.108e-03, 3.025e-03, 2.707e-03, 2.422e-03, 2.205e-03, 2.107e-03, 2.048e-03, 2.039e-03, 2.029e-03, 1.454e-03, 1.223e-03, 1.354e-03, 1.250e-03, 1.229e-03, 1.062e-03, 1.227e-03, 1.029e-03, 1.283e-03, 8.767e-04, 4.435e-04, 5.625e-04, 1.238e-03, 7.362e-04, 6.496e-04, 7.562e-04, 4.355e-04, 8.268e-05, 6.986e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8",{2.047e-01, 4.445e+00, 4.178e+00, 2.495e+00, 1.855e+00, 1.660e+00, 1.368e+00, 1.440e+00, 8.912e-01, 2.230e+00, 2.181e+00, 2.066e+00, 1.744e+00, 1.530e+00, 1.444e+00, 1.418e+00, 1.435e+00, 1.434e+00, 1.422e+00, 1.406e+00, 1.393e+00, 1.389e+00, 1.390e+00, 1.395e+00, 1.390e+00, 1.375e+00, 1.362e+00, 1.330e+00, 1.307e+00, 1.258e+00, 1.203e+00, 1.123e+00, 1.044e+00, 9.555e-01, 8.772e-01, 8.168e-01, 7.737e-01, 7.470e-01, 7.161e-01, 7.045e-01, 7.466e-01, 8.278e-01, 9.446e-01, 1.092e+00, 1.251e+00, 1.394e+00, 1.486e+00, 1.442e+00, 1.321e+00, 1.128e+00, 9.060e-01, 6.908e-01, 5.000e-01, 3.499e-01, 2.385e-01, 1.549e-01, 9.973e-02, 6.280e-02, 4.075e-02, 2.693e-02, 1.833e-02, 1.291e-02, 9.491e-03, 7.256e-03, 5.796e-03, 4.117e-03, 3.050e-03, 2.660e-03, 2.397e-03, 2.220e-03, 2.128e-03, 2.024e-03, 1.974e-03, 1.958e-03, 1.565e-03, 1.305e-03, 1.271e-03, 1.201e-03, 1.321e-03, 1.156e-03, 1.207e-03, 1.173e-03, 1.108e-03, 7.862e-04, 7.191e-04, 6.219e-04, 7.202e-04, 5.449e-04, 5.877e-04, 4.561e-04, 2.955e-04, 6.731e-04, 1.517e-04, 4.225e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8",{1.829e-01, 4.618e+00, 4.523e+00, 2.588e+00, 1.911e+00, 1.646e+00, 1.310e+00, 1.398e+00, 8.685e-01, 2.119e+00, 2.192e+00, 2.076e+00, 1.735e+00, 1.532e+00, 1.443e+00, 1.420e+00, 1.437e+00, 1.432e+00, 1.421e+00, 1.410e+00, 1.394e+00, 1.392e+00, 1.385e+00, 1.393e+00, 1.394e+00, 1.383e+00, 1.362e+00, 1.330e+00, 1.312e+00, 1.256e+00, 1.202e+00, 1.126e+00, 1.044e+00, 9.529e-01, 8.787e-01, 8.160e-01, 7.746e-01, 7.455e-01, 7.141e-01, 7.043e-01, 7.484e-01, 8.263e-01, 9.432e-01, 1.088e+00, 1.250e+00, 1.393e+00, 1.479e+00, 1.433e+00, 1.319e+00, 1.129e+00, 9.066e-01, 6.883e-01, 5.019e-01, 3.495e-01, 2.380e-01, 1.553e-01, 9.900e-02, 6.291e-02, 4.064e-02, 2.701e-02, 1.834e-02, 1.293e-02, 9.552e-03, 7.268e-03, 5.805e-03, 4.131e-03, 3.057e-03, 2.669e-03, 2.411e-03, 2.259e-03, 2.084e-03, 2.082e-03, 1.997e-03, 1.948e-03, 1.537e-03, 1.267e-03, 1.310e-03, 1.370e-03, 1.330e-03, 1.285e-03, 1.230e-03, 1.288e-03, 1.141e-03, 6.818e-04, 8.836e-04, 7.682e-04, 5.126e-04, 7.479e-04, 5.377e-04, 3.521e-04, 4.055e-04, 3.079e-04, 5.204e-04, 2.899e-04, 7.985e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8",{1.750e-01, 4.429e+00, 4.725e+00, 2.462e+00, 1.740e+00, 1.666e+00, 1.353e+00, 1.390e+00, 8.748e-01, 2.167e+00, 2.192e+00, 2.071e+00, 1.754e+00, 1.546e+00, 1.449e+00, 1.421e+00, 1.437e+00, 1.433e+00, 1.428e+00, 1.399e+00, 1.385e+00, 1.386e+00, 1.391e+00, 1.395e+00, 1.390e+00, 1.382e+00, 1.361e+00, 1.329e+00, 1.312e+00, 1.256e+00, 1.198e+00, 1.119e+00, 1.042e+00, 9.544e-01, 8.772e-01, 8.207e-01, 7.713e-01, 7.479e-01, 7.153e-01, 7.050e-01, 7.503e-01, 8.277e-01, 9.443e-01, 1.095e+00, 1.250e+00, 1.392e+00, 1.487e+00, 1.450e+00, 1.327e+00, 1.120e+00, 9.107e-01, 6.889e-01, 4.985e-01, 3.520e-01, 2.368e-01, 1.542e-01, 9.906e-02, 6.327e-02, 4.071e-02, 2.683e-02, 1.830e-02, 1.298e-02, 9.548e-03, 7.284e-03, 5.854e-03, 4.086e-03, 3.046e-03, 2.670e-03, 2.459e-03, 2.202e-03, 2.128e-03, 2.124e-03, 1.953e-03, 1.979e-03, 1.489e-03, 1.234e-03, 1.313e-03, 1.240e-03, 1.447e-03, 1.141e-03, 1.136e-03, 1.148e-03, 9.771e-04, 8.053e-04, 5.495e-04, 7.291e-04, 1.001e-03, 1.388e-03, 3.062e-04, 3.565e-04, 2.737e-04, 4.676e-04, 1.317e-04, 4.892e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8",{1.893e-01, 4.428e+00, 4.831e+00, 2.464e+00, 1.884e+00, 1.731e+00, 1.326e+00, 1.400e+00, 8.941e-01, 2.168e+00, 2.181e+00, 2.069e+00, 1.748e+00, 1.537e+00, 1.442e+00, 1.425e+00, 1.435e+00, 1.434e+00, 1.424e+00, 1.408e+00, 1.394e+00, 1.390e+00, 1.392e+00, 1.393e+00, 1.392e+00, 1.381e+00, 1.360e+00, 1.328e+00, 1.307e+00, 1.258e+00, 1.204e+00, 1.126e+00, 1.043e+00, 9.545e-01, 8.763e-01, 8.170e-01, 7.725e-01, 7.465e-01, 7.171e-01, 7.035e-01, 7.463e-01, 8.272e-01, 9.445e-01, 1.091e+00, 1.248e+00, 1.392e+00, 1.484e+00, 1.434e+00, 1.320e+00, 1.124e+00, 9.090e-01, 6.888e-01, 5.021e-01, 3.506e-01, 2.380e-01, 1.542e-01, 9.967e-02, 6.297e-02, 4.072e-02, 2.689e-02, 1.838e-02, 1.293e-02, 9.511e-03, 7.280e-03, 5.806e-03, 4.118e-03, 3.047e-03, 2.647e-03, 2.410e-03, 2.229e-03, 2.109e-03, 2.047e-03, 2.009e-03, 1.979e-03, 1.586e-03, 1.296e-03, 1.284e-03, 1.253e-03, 1.270e-03, 1.323e-03, 1.202e-03, 1.096e-03, 1.189e-03, 8.501e-04, 6.587e-04, 6.754e-04, 6.053e-04, 6.779e-04, 6.551e-04, 5.523e-04, 5.764e-04, 3.090e-04, 1.741e-04, 5.495e-04, 9.080e-04, 8.242e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8",{1.942e-01, 4.477e+00, 4.756e+00, 2.445e+00, 1.824e+00, 1.670e+00, 1.351e+00, 1.434e+00, 8.940e-01, 2.165e+00, 2.194e+00, 2.061e+00, 1.737e+00, 1.536e+00, 1.436e+00, 1.425e+00, 1.435e+00, 1.433e+00, 1.424e+00, 1.406e+00, 1.393e+00, 1.390e+00, 1.393e+00, 1.392e+00, 1.391e+00, 1.380e+00, 1.362e+00, 1.329e+00, 1.309e+00, 1.257e+00, 1.201e+00, 1.125e+00, 1.043e+00, 9.541e-01, 8.764e-01, 8.174e-01, 7.735e-01, 7.463e-01, 7.162e-01, 7.046e-01, 7.463e-01, 8.264e-01, 9.456e-01, 1.092e+00, 1.247e+00, 1.395e+00, 1.485e+00, 1.433e+00, 1.321e+00, 1.124e+00, 9.072e-01, 6.883e-01, 5.021e-01, 3.505e-01, 2.378e-01, 1.548e-01, 9.974e-02, 6.302e-02, 4.066e-02, 2.694e-02, 1.839e-02, 1.297e-02, 9.510e-03, 7.288e-03, 5.802e-03, 4.133e-03, 3.043e-03, 2.647e-03, 2.404e-03, 2.231e-03, 2.108e-03, 2.068e-03, 2.005e-03, 1.980e-03, 1.531e-03, 1.295e-03, 1.289e-03, 1.281e-03, 1.245e-03, 1.229e-03, 1.254e-03, 1.227e-03, 1.110e-03, 8.441e-04, 6.810e-04, 6.541e-04, 5.677e-04, 6.857e-04, 5.294e-04, 4.771e-04, 2.747e-04, 3.032e-04, 1.608e-04, 1.903e-04, 8.386e-04, 2.284e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8",{1.918e-01, 4.239e+00, 4.483e+00, 2.480e+00, 1.854e+00, 1.692e+00, 1.379e+00, 1.441e+00, 8.941e-01, 2.161e+00, 2.208e+00, 2.072e+00, 1.746e+00, 1.535e+00, 1.440e+00, 1.419e+00, 1.432e+00, 1.434e+00, 1.428e+00, 1.407e+00, 1.393e+00, 1.387e+00, 1.390e+00, 1.393e+00, 1.395e+00, 1.383e+00, 1.361e+00, 1.329e+00, 1.309e+00, 1.256e+00, 1.201e+00, 1.126e+00, 1.041e+00, 9.551e-01, 8.774e-01, 8.169e-01, 7.739e-01, 7.461e-01, 7.151e-01, 7.037e-01, 7.467e-01, 8.262e-01, 9.456e-01, 1.091e+00, 1.251e+00, 1.395e+00, 1.480e+00, 1.435e+00, 1.325e+00, 1.123e+00, 9.082e-01, 6.897e-01, 5.010e-01, 3.501e-01, 2.378e-01, 1.548e-01, 9.977e-02, 6.294e-02, 4.068e-02, 2.685e-02, 1.835e-02, 1.296e-02, 9.501e-03, 7.286e-03, 5.804e-03, 4.125e-03, 3.039e-03, 2.665e-03, 2.404e-03, 2.226e-03, 2.132e-03, 2.058e-03, 2.003e-03, 1.985e-03, 1.571e-03, 1.283e-03, 1.291e-03, 1.281e-03, 1.270e-03, 1.285e-03, 1.246e-03, 1.200e-03, 1.111e-03, 8.939e-04, 6.538e-04, 6.927e-04, 5.760e-04, 6.069e-04, 4.532e-04, 4.425e-04, 3.590e-04, 3.749e-04, 2.304e-04, 1.569e-04, 3.888e-04, 2.118e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8",{1.966e-01, 4.224e+00, 4.203e+00, 2.372e+00, 1.893e+00, 1.666e+00, 1.360e+00, 1.390e+00, 8.999e-01, 2.170e+00, 2.194e+00, 2.073e+00, 1.738e+00, 1.535e+00, 1.442e+00, 1.423e+00, 1.431e+00, 1.436e+00, 1.425e+00, 1.409e+00, 1.393e+00, 1.393e+00, 1.389e+00, 1.392e+00, 1.389e+00, 1.381e+00, 1.363e+00, 1.329e+00, 1.308e+00, 1.255e+00, 1.201e+00, 1.125e+00, 1.043e+00, 9.549e-01, 8.776e-01, 8.168e-01, 7.737e-01, 7.485e-01, 7.156e-01, 7.031e-01, 7.461e-01, 8.273e-01, 9.468e-01, 1.090e+00, 1.252e+00, 1.391e+00, 1.486e+00, 1.435e+00, 1.322e+00, 1.124e+00, 9.096e-01, 6.901e-01, 5.010e-01, 3.497e-01, 2.375e-01, 1.548e-01, 9.942e-02, 6.312e-02, 4.066e-02, 2.684e-02, 1.838e-02, 1.298e-02, 9.500e-03, 7.280e-03, 5.790e-03, 4.127e-03, 3.032e-03, 2.641e-03, 2.419e-03, 2.232e-03, 2.133e-03, 2.063e-03, 2.021e-03, 1.935e-03, 1.542e-03, 1.270e-03, 1.280e-03, 1.279e-03, 1.263e-03, 1.269e-03, 1.216e-03, 1.157e-03, 1.256e-03, 8.823e-04, 6.637e-04, 6.671e-04, 5.291e-04, 5.953e-04, 5.943e-04, 4.077e-04, 2.629e-04, 2.880e-04, 1.406e-04, 9.791e-05, 2.157e-04, 1.175e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_s-channel_antitop_leptonDecays_13TeV-PSweights_powheg-pythia",{1.886e-01, 6.561e+00, 3.592e+00, 2.338e+00, 1.837e+00, 1.607e+00, 1.395e+00, 1.378e+00, 8.878e-01, 2.156e+00, 2.312e+00, 2.054e+00, 1.756e+00, 1.538e+00, 1.444e+00, 1.424e+00, 1.449e+00, 1.434e+00, 1.422e+00, 1.405e+00, 1.399e+00, 1.383e+00, 1.386e+00, 1.388e+00, 1.397e+00, 1.382e+00, 1.362e+00, 1.329e+00, 1.304e+00, 1.253e+00, 1.203e+00, 1.124e+00, 1.047e+00, 9.556e-01, 8.779e-01, 8.150e-01, 7.719e-01, 7.478e-01, 7.130e-01, 7.041e-01, 7.459e-01, 8.284e-01, 9.457e-01, 1.094e+00, 1.250e+00, 1.394e+00, 1.484e+00, 1.449e+00, 1.314e+00, 1.122e+00, 9.105e-01, 6.921e-01, 4.975e-01, 3.487e-01, 2.371e-01, 1.547e-01, 1.002e-01, 6.301e-02, 4.078e-02, 2.688e-02, 1.836e-02, 1.313e-02, 9.521e-03, 7.269e-03, 5.773e-03, 4.099e-03, 3.007e-03, 2.591e-03, 2.423e-03, 2.218e-03, 2.096e-03, 2.127e-03, 2.019e-03, 1.952e-03, 1.503e-03, 1.382e-03, 1.285e-03, 1.362e-03, 1.409e-03, 1.113e-03, 1.459e-03, 1.007e-03, 1.717e-03, 7.579e-04, 1.083e-03, 5.912e-04, 7.100e-04, 5.276e-04, 6.207e-04, 1.806e-04, 4.161e-04, 1.185e-04, 1.335e-04, 7.437e-05, 0.000e+00, 2.231e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_s-channel_top_leptonDecays_13TeV-PSweights_powheg-pythia",{1.827e-01, 4.239e+00, 4.641e+00, 2.323e+00, 1.844e+00, 1.739e+00, 1.380e+00, 1.413e+00, 8.784e-01, 2.175e+00, 2.196e+00, 2.049e+00, 1.728e+00, 1.525e+00, 1.442e+00, 1.424e+00, 1.439e+00, 1.425e+00, 1.431e+00, 1.411e+00, 1.390e+00, 1.388e+00, 1.391e+00, 1.395e+00, 1.391e+00, 1.377e+00, 1.362e+00, 1.331e+00, 1.304e+00, 1.257e+00, 1.202e+00, 1.126e+00, 1.044e+00, 9.607e-01, 8.777e-01, 8.180e-01, 7.735e-01, 7.484e-01, 7.144e-01, 7.056e-01, 7.449e-01, 8.301e-01, 9.445e-01, 1.085e+00, 1.247e+00, 1.396e+00, 1.489e+00, 1.427e+00, 1.315e+00, 1.125e+00, 9.113e-01, 6.905e-01, 4.975e-01, 3.530e-01, 2.382e-01, 1.540e-01, 9.892e-02, 6.298e-02, 4.062e-02, 2.670e-02, 1.835e-02, 1.291e-02, 9.459e-03, 7.347e-03, 5.813e-03, 4.126e-03, 3.059e-03, 2.672e-03, 2.425e-03, 2.216e-03, 2.167e-03, 2.078e-03, 2.058e-03, 1.998e-03, 1.530e-03, 1.301e-03, 1.376e-03, 1.242e-03, 1.133e-03, 1.197e-03, 1.369e-03, 1.252e-03, 1.337e-03, 1.093e-03, 7.851e-04, 6.575e-04, 5.183e-04, 7.042e-04, 4.833e-04, 3.376e-04, 9.719e-04, 2.768e-04, 3.118e-04, 8.686e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.937e-01, 4.285e+00, 4.608e+00, 2.469e+00, 1.844e+00, 1.705e+00, 1.365e+00, 1.423e+00, 8.858e-01, 2.176e+00, 2.193e+00, 2.060e+00, 1.747e+00, 1.538e+00, 1.440e+00, 1.420e+00, 1.430e+00, 1.433e+00, 1.426e+00, 1.409e+00, 1.393e+00, 1.389e+00, 1.392e+00, 1.394e+00, 1.392e+00, 1.381e+00, 1.360e+00, 1.329e+00, 1.311e+00, 1.258e+00, 1.201e+00, 1.125e+00, 1.042e+00, 9.546e-01, 8.770e-01, 8.178e-01, 7.731e-01, 7.461e-01, 7.151e-01, 7.038e-01, 7.467e-01, 8.259e-01, 9.447e-01, 1.090e+00, 1.251e+00, 1.393e+00, 1.483e+00, 1.436e+00, 1.322e+00, 1.126e+00, 9.080e-01, 6.916e-01, 5.002e-01, 3.495e-01, 2.377e-01, 1.547e-01, 9.960e-02, 6.302e-02, 4.066e-02, 2.687e-02, 1.834e-02, 1.295e-02, 9.497e-03, 7.302e-03, 5.810e-03, 4.134e-03, 3.040e-03, 2.661e-03, 2.414e-03, 2.228e-03, 2.119e-03, 2.062e-03, 1.998e-03, 2.004e-03, 1.543e-03, 1.298e-03, 1.277e-03, 1.294e-03, 1.246e-03, 1.235e-03, 1.250e-03, 1.196e-03, 1.144e-03, 7.888e-04, 6.446e-04, 7.375e-04, 6.236e-04, 6.096e-04, 5.344e-04, 4.533e-04, 3.045e-04, 3.061e-04, 1.832e-04, 1.814e-04, 8.995e-04, 6.998e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.909e-01, 4.326e+00, 4.404e+00, 2.438e+00, 1.895e+00, 1.683e+00, 1.341e+00, 1.409e+00, 8.969e-01, 2.174e+00, 2.197e+00, 2.069e+00, 1.746e+00, 1.538e+00, 1.441e+00, 1.422e+00, 1.434e+00, 1.433e+00, 1.424e+00, 1.407e+00, 1.395e+00, 1.389e+00, 1.392e+00, 1.393e+00, 1.392e+00, 1.381e+00, 1.361e+00, 1.329e+00, 1.308e+00, 1.257e+00, 1.201e+00, 1.126e+00, 1.042e+00, 9.550e-01, 8.772e-01, 8.172e-01, 7.734e-01, 7.465e-01, 7.162e-01, 7.039e-01, 7.466e-01, 8.262e-01, 9.452e-01, 1.088e+00, 1.248e+00, 1.393e+00, 1.483e+00, 1.436e+00, 1.323e+00, 1.124e+00, 9.072e-01, 6.888e-01, 5.006e-01, 3.507e-01, 2.378e-01, 1.549e-01, 9.968e-02, 6.299e-02, 4.072e-02, 2.689e-02, 1.835e-02, 1.296e-02, 9.511e-03, 7.295e-03, 5.823e-03, 4.136e-03, 3.040e-03, 2.658e-03, 2.399e-03, 2.226e-03, 2.114e-03, 2.062e-03, 1.989e-03, 1.971e-03, 1.567e-03, 1.281e-03, 1.294e-03, 1.268e-03, 1.266e-03, 1.265e-03, 1.228e-03, 1.236e-03, 1.225e-03, 8.103e-04, 7.079e-04, 7.266e-04, 5.923e-04, 6.088e-04, 5.056e-04, 5.458e-04, 3.032e-04, 3.077e-04, 1.585e-04, 1.626e-04, 5.673e-04, 1.324e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",{2.012e-01, 4.270e+00, 4.304e+00, 2.322e+00, 1.945e+00, 1.748e+00, 1.387e+00, 1.395e+00, 8.704e-01, 2.155e+00, 2.203e+00, 2.069e+00, 1.735e+00, 1.544e+00, 1.441e+00, 1.422e+00, 1.431e+00, 1.432e+00, 1.431e+00, 1.407e+00, 1.395e+00, 1.389e+00, 1.386e+00, 1.393e+00, 1.394e+00, 1.381e+00, 1.361e+00, 1.330e+00, 1.305e+00, 1.260e+00, 1.203e+00, 1.122e+00, 1.043e+00, 9.561e-01, 8.762e-01, 8.183e-01, 7.723e-01, 7.469e-01, 7.162e-01, 7.035e-01, 7.495e-01, 8.273e-01, 9.446e-01, 1.092e+00, 1.243e+00, 1.398e+00, 1.478e+00, 1.437e+00, 1.318e+00, 1.123e+00, 9.013e-01, 6.919e-01, 4.988e-01, 3.498e-01, 2.386e-01, 1.555e-01, 9.940e-02, 6.298e-02, 4.051e-02, 2.688e-02, 1.840e-02, 1.299e-02, 9.542e-03, 7.331e-03, 5.774e-03, 4.136e-03, 3.049e-03, 2.662e-03, 2.399e-03, 2.217e-03, 2.111e-03, 2.008e-03, 1.993e-03, 2.045e-03, 1.560e-03, 1.330e-03, 1.280e-03, 1.325e-03, 1.202e-03, 1.260e-03, 1.275e-03, 1.265e-03, 1.219e-03, 1.011e-03, 7.049e-04, 6.413e-04, 5.437e-04, 9.157e-04, 5.387e-04, 3.135e-04, 2.708e-04, 6.170e-04, 1.159e-04, 1.936e-04, 0.000e+00, 2.904e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.784e-01, 4.467e+00, 5.307e+00, 2.718e+00, 1.922e+00, 1.680e+00, 1.297e+00, 1.359e+00, 8.826e-01, 2.168e+00, 2.130e+00, 2.054e+00, 1.745e+00, 1.543e+00, 1.432e+00, 1.422e+00, 1.435e+00, 1.428e+00, 1.431e+00, 1.414e+00, 1.396e+00, 1.383e+00, 1.395e+00, 1.392e+00, 1.392e+00, 1.385e+00, 1.362e+00, 1.328e+00, 1.307e+00, 1.254e+00, 1.201e+00, 1.123e+00, 1.038e+00, 9.542e-01, 8.759e-01, 8.162e-01, 7.741e-01, 7.464e-01, 7.186e-01, 7.044e-01, 7.464e-01, 8.286e-01, 9.407e-01, 1.091e+00, 1.254e+00, 1.394e+00, 1.486e+00, 1.427e+00, 1.315e+00, 1.126e+00, 9.108e-01, 6.908e-01, 5.002e-01, 3.500e-01, 2.379e-01, 1.554e-01, 9.973e-02, 6.290e-02, 4.081e-02, 2.681e-02, 1.843e-02, 1.292e-02, 9.491e-03, 7.328e-03, 5.827e-03, 4.150e-03, 3.050e-03, 2.700e-03, 2.409e-03, 2.243e-03, 2.097e-03, 2.045e-03, 1.985e-03, 1.983e-03, 1.588e-03, 1.294e-03, 1.354e-03, 1.242e-03, 1.304e-03, 1.202e-03, 1.318e-03, 1.149e-03, 9.169e-04, 8.020e-04, 9.641e-04, 8.771e-04, 6.772e-04, 7.045e-04, 4.144e-04, 3.860e-04, 1.852e-04, 6.329e-04, 8.913e-05, 1.986e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTHH_TuneCP5_13TeV-madgraph-pythia8",{1.251e-04, 5.760e-01, 5.256e-01, 2.782e-01, 2.495e-01, 1.758e-01, 1.539e-01, 1.507e-01, 1.011e-01, 5.734e-01, 7.558e-01, 7.460e-01, 9.463e-01, 4.749e-01, 1.004e+00, 9.904e-01, 1.042e+00, 1.208e+00, 1.061e+00, 1.421e+00, 1.423e+00, 1.469e+00, 1.537e+00, 1.580e+00, 1.571e+00, 1.487e+00, 1.520e+00, 1.473e+00, 1.458e+00, 1.392e+00, 1.326e+00, 1.239e+00, 1.185e+00, 1.061e+00, 1.009e+00, 9.272e-01, 8.889e-01, 8.338e-01, 7.985e-01, 7.797e-01, 8.695e-01, 9.365e-01, 1.062e+00, 1.197e+00, 1.409e+00, 1.552e+00, 1.681e+00, 1.649e+00, 1.483e+00, 1.291e+00, 9.837e-01, 7.490e-01, 5.545e-01, 4.032e-01, 2.750e-01, 1.784e-01, 1.123e-01, 7.269e-02, 4.541e-02, 2.936e-02, 2.099e-02, 1.490e-02, 8.686e-03, 7.830e-03, 6.111e-03, 4.949e-03, 3.322e-03, 2.865e-03, 2.698e-03, 2.580e-03, 2.187e-03, 2.321e-03, 2.561e-03, 2.142e-03, 1.873e-03, 1.263e-03, 1.547e-03, 1.135e-03, 2.736e-03, 3.496e-03, 1.108e-03, 9.294e-04, 1.739e-03, 3.583e-04, 0.000e+00, 3.992e-04, 2.397e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 4.057e-07, 0.000e+00, 0.000e+00, 8.444e-09, 0.000e+0}},
{"TTTJ_TuneCP5_13TeV-madgraph-pythia8",{1.438e-01, 0.000e+00, 6.281e+00, 2.494e+00, 3.726e+00, 1.959e+00, 1.532e+00, 1.220e+00, 9.144e-01, 2.157e+00, 2.183e+00, 1.977e+00, 1.594e+00, 1.521e+00, 1.472e+00, 1.412e+00, 1.459e+00, 1.459e+00, 1.440e+00, 1.438e+00, 1.396e+00, 1.375e+00, 1.386e+00, 1.402e+00, 1.366e+00, 1.371e+00, 1.349e+00, 1.320e+00, 1.311e+00, 1.262e+00, 1.204e+00, 1.127e+00, 1.042e+00, 9.448e-01, 8.680e-01, 8.123e-01, 7.671e-01, 7.567e-01, 7.307e-01, 7.087e-01, 7.618e-01, 8.291e-01, 9.637e-01, 1.069e+00, 1.287e+00, 1.347e+00, 1.481e+00, 1.450e+00, 1.316e+00, 1.105e+00, 9.209e-01, 6.998e-01, 4.989e-01, 3.403e-01, 2.313e-01, 1.553e-01, 9.649e-02, 6.488e-02, 4.017e-02, 2.684e-02, 1.918e-02, 1.303e-02, 9.731e-03, 6.971e-03, 5.879e-03, 4.060e-03, 3.235e-03, 2.624e-03, 2.458e-03, 2.025e-03, 2.069e-03, 2.089e-03, 2.198e-03, 2.407e-03, 1.368e-03, 1.184e-03, 1.247e-03, 1.304e-03, 9.910e-04, 8.704e-04, 1.104e-03, 0.000e+00, 1.732e-03, 3.568e-04, 0.000e+00, 0.000e+00, 2.388e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTTT_TuneCP5_13TeV-amcatnlo-pythia8",{1.573e-01, 2.490e+00, 3.817e+00, 2.210e+00, 2.123e+00, 1.024e+00, 8.216e-01, 9.194e-01, 1.351e+00, 2.000e+00, 1.891e+00, 2.270e+00, 1.672e+00, 1.468e+00, 1.430e+00, 1.422e+00, 1.414e+00, 1.475e+00, 1.488e+00, 1.387e+00, 1.432e+00, 1.332e+00, 1.362e+00, 1.370e+00, 1.410e+00, 1.339e+00, 1.368e+00, 1.338e+00, 1.281e+00, 1.279e+00, 1.167e+00, 1.121e+00, 1.028e+00, 9.681e-01, 8.901e-01, 8.363e-01, 7.997e-01, 7.582e-01, 6.984e-01, 6.988e-01, 7.284e-01, 8.203e-01, 9.542e-01, 1.086e+00, 1.256e+00, 1.471e+00, 1.512e+00, 1.440e+00, 1.395e+00, 1.143e+00, 8.980e-01, 6.901e-01, 5.010e-01, 3.665e-01, 2.256e-01, 1.534e-01, 1.043e-01, 6.284e-02, 4.232e-02, 2.745e-02, 1.746e-02, 1.259e-02, 9.379e-03, 7.603e-03, 5.690e-03, 4.074e-03, 2.923e-03, 2.438e-03, 2.344e-03, 2.204e-03, 2.100e-03, 1.936e-03, 1.650e-03, 1.509e-03, 1.386e-03, 1.798e-03, 1.137e-03, 1.392e-03, 1.743e-03, 5.289e-03, 1.032e-03, 6.027e-04, 7.517e-04, 8.131e-04, 3.984e-04, 0.000e+00, 1.814e-04, -1.078e-04, 0.000e+00, 0.000e+00, 0.000e+00, -4.843e-05, 0.000e+00, -7.599e-06, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8",{2.408e-01, 8.186e+00, 2.988e+00, 2.020e+00, 1.622e+00, 1.328e+00, 1.481e+00, 1.234e+00, 9.717e-01, 2.293e+00, 2.229e+00, 2.029e+00, 1.762e+00, 1.493e+00, 1.402e+00, 1.433e+00, 1.429e+00, 1.458e+00, 1.423e+00, 1.412e+00, 1.381e+00, 1.377e+00, 1.398e+00, 1.413e+00, 1.367e+00, 1.404e+00, 1.350e+00, 1.324e+00, 1.309e+00, 1.261e+00, 1.189e+00, 1.112e+00, 1.043e+00, 9.572e-01, 8.731e-01, 8.145e-01, 7.769e-01, 7.514e-01, 7.189e-01, 7.013e-01, 7.351e-01, 8.456e-01, 9.501e-01, 1.085e+00, 1.261e+00, 1.407e+00, 1.486e+00, 1.469e+00, 1.319e+00, 1.128e+00, 9.022e-01, 6.850e-01, 4.948e-01, 3.579e-01, 2.368e-01, 1.512e-01, 9.866e-02, 6.485e-02, 4.098e-02, 2.713e-02, 1.848e-02, 1.317e-02, 9.509e-03, 7.271e-03, 5.810e-03, 4.075e-03, 2.952e-03, 2.472e-03, 2.316e-03, 2.257e-03, 2.285e-03, 2.071e-03, 2.005e-03, 1.951e-03, 1.745e-03, 1.295e-03, 1.156e-03, 1.344e-03, 1.944e-03, 1.192e-03, 1.260e-03, 1.081e-03, 9.267e-04, 7.637e-04, 4.677e-04, 8.510e-04, 0.000e+00, -6.076e-04, 1.787e-04, 0.000e+00, 1.198e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTTW_TuneCP5_13TeV-madgraph-pythia8",{1.905e-03, 5.245e-01, 7.432e-01, 2.621e-01, 2.709e-01, 2.205e-01, 1.893e-01, 2.001e-01, 1.333e-01, 2.948e-01, 8.352e-01, 8.506e-01, 8.946e-01, 1.317e+00, 1.400e+00, 1.377e+00, 1.402e+00, 1.215e+00, 1.299e+00, 1.299e+00, 1.298e+00, 1.318e+00, 1.376e+00, 1.407e+00, 1.399e+00, 1.422e+00, 1.409e+00, 1.332e+00, 1.348e+00, 1.325e+00, 1.238e+00, 1.180e+00, 1.043e+00, 9.976e-01, 9.392e-01, 8.775e-01, 7.714e-01, 8.024e-01, 7.652e-01, 7.632e-01, 8.102e-01, 8.902e-01, 1.003e+00, 1.205e+00, 1.314e+00, 1.511e+00, 1.600e+00, 1.606e+00, 1.456e+00, 1.217e+00, 9.474e-01, 7.386e-01, 4.325e-01, 3.729e-01, 2.611e-01, 1.682e-01, 1.053e-01, 5.149e-02, 4.383e-02, 2.900e-02, 1.921e-02, 1.401e-02, 1.031e-02, 7.654e-03, 5.949e-03, 4.535e-03, 3.226e-03, 2.911e-03, 2.404e-03, 2.484e-03, 2.312e-03, 2.081e-03, 2.711e-03, 1.574e-03, 1.474e-03, 1.499e-03, 1.386e-03, 1.420e-03, 7.831e-04, 6.287e-06, 1.480e-03, 2.793e-03, 1.742e-03, 3.589e-04, 6.593e-04, 3.999e-04, 6.003e-05, 2.419e-07, 8.397e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 8.127e-07, 0.000e+00, 0.000e+00, 2.368e-08, 0.000e+0}},
{"TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.870e-01, 4.337e+00, 4.470e+00, 2.473e+00, 1.891e+00, 1.726e+00, 1.350e+00, 1.395e+00, 8.887e-01, 2.177e+00, 2.175e+00, 2.077e+00, 1.744e+00, 1.544e+00, 1.439e+00, 1.423e+00, 1.436e+00, 1.431e+00, 1.423e+00, 1.409e+00, 1.393e+00, 1.389e+00, 1.392e+00, 1.392e+00, 1.390e+00, 1.382e+00, 1.361e+00, 1.329e+00, 1.308e+00, 1.256e+00, 1.202e+00, 1.126e+00, 1.043e+00, 9.555e-01, 8.765e-01, 8.173e-01, 7.730e-01, 7.475e-01, 7.158e-01, 7.034e-01, 7.481e-01, 8.260e-01, 9.445e-01, 1.090e+00, 1.249e+00, 1.396e+00, 1.486e+00, 1.435e+00, 1.324e+00, 1.123e+00, 9.082e-01, 6.907e-01, 4.996e-01, 3.504e-01, 2.379e-01, 1.550e-01, 9.952e-02, 6.304e-02, 4.067e-02, 2.685e-02, 1.837e-02, 1.293e-02, 9.508e-03, 7.300e-03, 5.792e-03, 4.121e-03, 3.035e-03, 2.660e-03, 2.418e-03, 2.237e-03, 2.121e-03, 2.075e-03, 1.954e-03, 1.968e-03, 1.536e-03, 1.290e-03, 1.290e-03, 1.241e-03, 1.232e-03, 1.222e-03, 1.202e-03, 1.248e-03, 1.088e-03, 8.040e-04, 6.508e-04, 6.766e-04, 5.611e-04, 5.837e-04, 5.060e-04, 4.197e-04, 3.581e-04, 3.239e-04, 2.068e-04, 1.920e-04, 4.759e-04, 1.728e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTTo2L2Nu_TuneCP5_erdON_13TeV-powheg-pythia8",{1.925e-01, 4.053e+00, 5.238e+00, 2.337e+00, 1.928e+00, 1.607e+00, 1.297e+00, 1.464e+00, 9.204e-01, 2.164e+00, 2.242e+00, 2.090e+00, 1.759e+00, 1.537e+00, 1.446e+00, 1.417e+00, 1.438e+00, 1.437e+00, 1.415e+00, 1.416e+00, 1.399e+00, 1.390e+00, 1.391e+00, 1.398e+00, 1.393e+00, 1.384e+00, 1.364e+00, 1.329e+00, 1.300e+00, 1.256e+00, 1.203e+00, 1.126e+00, 1.043e+00, 9.554e-01, 8.761e-01, 8.161e-01, 7.727e-01, 7.477e-01, 7.151e-01, 7.044e-01, 7.474e-01, 8.261e-01, 9.465e-01, 1.089e+00, 1.245e+00, 1.395e+00, 1.475e+00, 1.433e+00, 1.316e+00, 1.121e+00, 9.058e-01, 6.898e-01, 4.998e-01, 3.488e-01, 2.380e-01, 1.553e-01, 9.995e-02, 6.307e-02, 4.076e-02, 2.687e-02, 1.834e-02, 1.295e-02, 9.505e-03, 7.295e-03, 5.804e-03, 4.120e-03, 3.047e-03, 2.636e-03, 2.400e-03, 2.230e-03, 2.120e-03, 1.986e-03, 2.062e-03, 1.949e-03, 1.588e-03, 1.284e-03, 1.348e-03, 1.225e-03, 1.296e-03, 1.128e-03, 1.337e-03, 1.177e-03, 1.224e-03, 9.389e-04, 9.808e-04, 9.194e-04, 1.012e-03, 7.220e-04, 2.124e-03, 1.766e-04, 0.000e+00, 4.054e-04, 0.000e+00, 6.361e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8",{2.966e-04, 4.492e-02, 4.447e-02, 6.366e-02, 7.882e-02, 1.240e-01, 1.213e-01, 1.635e-01, 1.285e-01, 4.873e-01, 6.823e-01, 8.511e-01, 8.685e-01, 9.395e-01, 9.264e-01, 1.050e+00, 1.173e+00, 1.225e+00, 1.324e+00, 1.347e+00, 1.368e+00, 1.395e+00, 1.422e+00, 1.468e+00, 1.470e+00, 1.479e+00, 1.440e+00, 1.406e+00, 1.419e+00, 1.359e+00, 1.311e+00, 1.208e+00, 1.131e+00, 1.043e+00, 9.592e-01, 8.903e-01, 8.487e-01, 8.181e-01, 7.864e-01, 7.687e-01, 8.245e-01, 8.967e-01, 1.031e+00, 1.172e+00, 1.370e+00, 1.526e+00, 1.640e+00, 1.574e+00, 1.450e+00, 1.220e+00, 9.338e-01, 7.154e-01, 5.391e-01, 3.594e-01, 2.508e-01, 1.584e-01, 1.071e-01, 6.723e-02, 4.359e-02, 2.889e-02, 1.958e-02, 1.380e-02, 1.031e-02, 7.849e-03, 5.242e-03, 4.434e-03, 2.925e-03, 2.841e-03, 2.633e-03, 2.383e-03, 2.296e-03, 1.494e-03, 1.620e-03, 9.379e-04, 5.721e-04, 1.011e-03, 1.310e-03, 1.192e-03, 1.874e-04, 6.176e-05, 5.609e-05, 1.433e-03, 1.184e-03, 6.810e-04, 1.002e-04, 2.112e-05, 5.937e-04, 6.740e-06, 6.297e-07, 6.270e-06, 5.468e-06, 5.409e-07, 3.032e-06, 1.291e-06, 4.828e-08, 1.590e-08, 7.367e-07, 1.177e-06, 6.879e-07, 2.064e-08, 0.000e+0}},
{"TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8",{2.389e-04, 2.319e-02, 7.578e-02, 4.259e-02, 7.536e-02, 8.153e-02, 9.058e-02, 1.558e-01, 1.668e-01, 4.075e-01, 7.097e-01, 9.054e-01, 8.034e-01, 9.722e-01, 1.002e+00, 1.135e+00, 1.257e+00, 1.319e+00, 1.355e+00, 1.378e+00, 1.382e+00, 1.408e+00, 1.446e+00, 1.445e+00, 1.471e+00, 1.464e+00, 1.480e+00, 1.456e+00, 1.418e+00, 1.387e+00, 1.324e+00, 1.214e+00, 1.144e+00, 1.027e+00, 9.715e-01, 9.009e-01, 8.522e-01, 8.195e-01, 7.656e-01, 7.816e-01, 8.127e-01, 8.883e-01, 1.009e+00, 1.197e+00, 1.394e+00, 1.512e+00, 1.598e+00, 1.529e+00, 1.443e+00, 1.241e+00, 9.585e-01, 7.437e-01, 5.283e-01, 3.655e-01, 2.564e-01, 1.631e-01, 1.041e-01, 6.826e-02, 4.355e-02, 2.819e-02, 1.979e-02, 1.353e-02, 1.031e-02, 7.830e-03, 6.228e-03, 4.461e-03, 3.031e-03, 2.542e-03, 2.575e-03, 2.069e-03, 1.634e-03, 1.633e-03, 1.095e-03, 2.214e-03, 8.098e-04, 1.370e-03, 1.276e-03, 2.306e-04, 1.710e-04, 7.623e-05, 2.303e-05, 1.627e-05, 1.252e-03, 8.651e-04, 9.042e-06, 6.426e-04, 3.124e-04, 1.268e-06, 1.562e-06, 4.340e-07, 1.675e-06, 2.576e-06, 1.634e-06, 6.872e-05, 7.570e-05, 4.251e-07, 1.110e-06, 1.970e-06, 7.774e-07, 2.009e-08, 0.000e+0}},
{"TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8",{2.180e-04, 3.422e-02, 3.917e-02, 3.823e-02, 3.921e-02, 7.722e-02, 1.647e-01, 1.537e-01, 1.115e-01, 4.213e-01, 5.970e-01, 7.766e-01, 8.734e-01, 9.580e-01, 1.003e+00, 1.081e+00, 1.200e+00, 1.307e+00, 1.359e+00, 1.361e+00, 1.400e+00, 1.419e+00, 1.432e+00, 1.493e+00, 1.505e+00, 1.500e+00, 1.458e+00, 1.458e+00, 1.440e+00, 1.390e+00, 1.293e+00, 1.242e+00, 1.153e+00, 1.075e+00, 9.672e-01, 9.051e-01, 8.682e-01, 8.393e-01, 7.974e-01, 7.668e-01, 8.397e-01, 9.292e-01, 1.022e+00, 1.219e+00, 1.372e+00, 1.560e+00, 1.618e+00, 1.561e+00, 1.456e+00, 1.214e+00, 9.209e-01, 6.880e-01, 5.442e-01, 3.709e-01, 2.594e-01, 1.631e-01, 1.068e-01, 6.716e-02, 4.389e-02, 2.793e-02, 1.877e-02, 1.369e-02, 1.020e-02, 7.777e-03, 6.150e-03, 4.191e-03, 3.150e-03, 2.909e-03, 2.562e-03, 2.474e-03, 1.954e-03, 1.010e-03, 1.364e-03, 2.097e-03, 8.812e-04, 1.405e-03, 1.158e-03, 1.424e-04, 1.651e-04, 5.306e-05, 2.917e-05, 2.972e-04, 2.914e-05, 1.806e-05, 5.611e-06, 6.827e-06, 4.816e-04, 1.008e-06, 1.445e-06, 2.124e-04, 2.688e-06, 4.179e-04, 2.178e-07, 1.311e-04, 7.224e-05, 1.099e-07, 2.354e-06, 3.971e-08, 9.891e-07, 1.784e-08, 0.000e+0}},
{"TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8",{3.528e-04, 6.373e-02, 4.170e-02, 5.569e-02, 6.459e-02, 1.357e-01, 1.590e-01, 1.895e-01, 1.545e-01, 6.994e-01, 8.974e-01, 9.710e-01, 8.670e-01, 9.274e-01, 9.393e-01, 1.092e+00, 1.153e+00, 1.222e+00, 1.305e+00, 1.316e+00, 1.363e+00, 1.378e+00, 1.424e+00, 1.460e+00, 1.460e+00, 1.436e+00, 1.432e+00, 1.411e+00, 1.385e+00, 1.346e+00, 1.290e+00, 1.207e+00, 1.125e+00, 1.043e+00, 9.484e-01, 8.967e-01, 8.499e-01, 8.179e-01, 7.729e-01, 7.648e-01, 8.009e-01, 8.989e-01, 1.020e+00, 1.168e+00, 1.335e+00, 1.492e+00, 1.627e+00, 1.495e+00, 1.401e+00, 1.222e+00, 9.387e-01, 7.386e-01, 5.311e-01, 3.715e-01, 2.487e-01, 1.628e-01, 1.071e-01, 6.767e-02, 4.269e-02, 2.879e-02, 1.965e-02, 1.397e-02, 1.025e-02, 7.181e-03, 5.996e-03, 4.385e-03, 2.986e-03, 2.844e-03, 2.572e-03, 2.397e-03, 2.109e-03, 1.267e-03, 2.114e-03, 1.115e-03, 5.721e-04, 9.684e-04, 8.564e-04, 9.091e-04, 1.024e-04, 9.113e-05, 1.074e-04, 8.973e-04, 5.876e-04, 6.457e-04, 5.392e-04, 4.996e-06, 1.986e-06, 1.301e-05, 1.888e-04, 2.638e-04, 0.000e+00, 1.442e-04, 2.437e-04, 7.893e-07, 3.739e-05, 3.097e-08, 1.371e-06, 1.668e-06, 1.536e-06, 1.507e-08, 0.000e+0}},
{"TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.950e-01, 4.059e+00, 4.401e+00, 2.445e+00, 1.859e+00, 1.687e+00, 1.337e+00, 1.427e+00, 8.903e-01, 2.160e+00, 2.175e+00, 2.066e+00, 1.746e+00, 1.539e+00, 1.437e+00, 1.424e+00, 1.433e+00, 1.433e+00, 1.422e+00, 1.407e+00, 1.394e+00, 1.389e+00, 1.392e+00, 1.394e+00, 1.391e+00, 1.381e+00, 1.361e+00, 1.329e+00, 1.308e+00, 1.256e+00, 1.202e+00, 1.125e+00, 1.043e+00, 9.551e-01, 8.766e-01, 8.166e-01, 7.735e-01, 7.479e-01, 7.163e-01, 7.032e-01, 7.475e-01, 8.276e-01, 9.443e-01, 1.089e+00, 1.248e+00, 1.393e+00, 1.482e+00, 1.434e+00, 1.324e+00, 1.124e+00, 9.073e-01, 6.900e-01, 5.012e-01, 3.503e-01, 2.378e-01, 1.548e-01, 9.962e-02, 6.299e-02, 4.064e-02, 2.692e-02, 1.838e-02, 1.298e-02, 9.520e-03, 7.286e-03, 5.810e-03, 4.125e-03, 3.045e-03, 2.665e-03, 2.405e-03, 2.241e-03, 2.112e-03, 2.054e-03, 1.986e-03, 1.979e-03, 1.558e-03, 1.294e-03, 1.283e-03, 1.240e-03, 1.278e-03, 1.224e-03, 1.221e-03, 1.222e-03, 1.160e-03, 8.335e-04, 7.010e-04, 7.044e-04, 5.880e-04, 6.031e-04, 5.220e-04, 4.861e-04, 3.955e-04, 3.986e-04, 1.883e-04, 1.712e-04, 5.971e-04, 1.951e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToHadronic_TuneCP5_erdON_13TeV-powheg-pythia8",{1.923e-01, 4.671e+00, 4.525e+00, 2.541e+00, 1.905e+00, 1.684e+00, 1.369e+00, 1.395e+00, 8.732e-01, 2.168e+00, 2.171e+00, 2.073e+00, 1.727e+00, 1.530e+00, 1.438e+00, 1.423e+00, 1.430e+00, 1.433e+00, 1.424e+00, 1.405e+00, 1.393e+00, 1.388e+00, 1.395e+00, 1.397e+00, 1.392e+00, 1.381e+00, 1.362e+00, 1.331e+00, 1.309e+00, 1.256e+00, 1.203e+00, 1.123e+00, 1.044e+00, 9.545e-01, 8.769e-01, 8.172e-01, 7.731e-01, 7.465e-01, 7.164e-01, 7.028e-01, 7.476e-01, 8.267e-01, 9.452e-01, 1.087e+00, 1.248e+00, 1.395e+00, 1.483e+00, 1.437e+00, 1.322e+00, 1.125e+00, 9.100e-01, 6.874e-01, 5.006e-01, 3.494e-01, 2.383e-01, 1.551e-01, 9.950e-02, 6.287e-02, 4.072e-02, 2.695e-02, 1.835e-02, 1.294e-02, 9.505e-03, 7.253e-03, 5.794e-03, 4.130e-03, 3.049e-03, 2.659e-03, 2.400e-03, 2.232e-03, 2.097e-03, 2.084e-03, 1.948e-03, 2.025e-03, 1.558e-03, 1.313e-03, 1.286e-03, 1.316e-03, 1.232e-03, 1.327e-03, 1.251e-03, 1.151e-03, 1.007e-03, 7.946e-04, 5.574e-04, 6.284e-04, 5.728e-04, 5.608e-04, 4.877e-04, 5.935e-04, 2.350e-04, 3.569e-04, 1.508e-04, 9.600e-05, 1.851e-04, 2.016e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToHadronic_TuneCP5down_PSweights_13TeV-powheg-pythia8",{2.729e-04, 3.104e-02, 5.309e-02, 4.690e-02, 7.919e-02, 1.107e-01, 1.063e-01, 1.431e-01, 1.526e-01, 4.694e-01, 7.104e-01, 8.702e-01, 8.605e-01, 8.916e-01, 9.803e-01, 1.084e+00, 1.216e+00, 1.278e+00, 1.327e+00, 1.358e+00, 1.382e+00, 1.415e+00, 1.440e+00, 1.461e+00, 1.475e+00, 1.464e+00, 1.455e+00, 1.438e+00, 1.401e+00, 1.356e+00, 1.304e+00, 1.224e+00, 1.140e+00, 1.043e+00, 9.588e-01, 8.997e-01, 8.401e-01, 8.169e-01, 7.791e-01, 7.701e-01, 8.145e-01, 9.066e-01, 1.040e+00, 1.186e+00, 1.364e+00, 1.516e+00, 1.610e+00, 1.554e+00, 1.411e+00, 1.210e+00, 9.512e-01, 7.344e-01, 5.369e-01, 3.688e-01, 2.486e-01, 1.624e-01, 1.053e-01, 6.666e-02, 4.266e-02, 2.891e-02, 1.974e-02, 1.337e-02, 1.019e-02, 7.403e-03, 5.767e-03, 4.391e-03, 3.117e-03, 2.705e-03, 2.345e-03, 2.098e-03, 2.043e-03, 1.639e-03, 1.519e-03, 1.931e-03, 1.189e-03, 5.208e-04, 5.530e-04, 3.281e-04, 1.972e-04, 8.109e-05, 5.010e-05, 4.437e-05, 4.219e-05, 3.820e-05, 7.420e-06, 1.636e-05, 6.840e-06, 9.745e-06, 1.344e-06, 5.879e-06, 1.667e-06, 3.719e-05, 1.662e-06, 2.119e-07, 5.882e-07, 3.800e-08, 1.530e-06, 9.723e-08, 4.896e-08, 1.827e-08, 0.000e+0}},
{"TTToHadronic_TuneCP5up_PSweights_13TeV-powheg-pythia8",{3.021e-04, 3.117e-02, 6.934e-02, 6.125e-02, 7.988e-02, 1.246e-01, 1.305e-01, 1.759e-01, 1.548e-01, 5.079e-01, 6.565e-01, 8.309e-01, 9.117e-01, 9.646e-01, 1.004e+00, 1.079e+00, 1.209e+00, 1.257e+00, 1.329e+00, 1.356e+00, 1.374e+00, 1.399e+00, 1.439e+00, 1.451e+00, 1.477e+00, 1.462e+00, 1.442e+00, 1.418e+00, 1.399e+00, 1.364e+00, 1.300e+00, 1.210e+00, 1.126e+00, 1.040e+00, 9.561e-01, 8.935e-01, 8.438e-01, 8.081e-01, 7.811e-01, 7.703e-01, 8.089e-01, 9.019e-01, 1.027e+00, 1.190e+00, 1.353e+00, 1.512e+00, 1.613e+00, 1.530e+00, 1.408e+00, 1.197e+00, 9.363e-01, 7.280e-01, 5.223e-01, 3.641e-01, 2.500e-01, 1.629e-01, 1.043e-01, 6.583e-02, 4.346e-02, 2.836e-02, 1.939e-02, 1.346e-02, 1.009e-02, 7.398e-03, 5.919e-03, 4.285e-03, 3.078e-03, 2.757e-03, 2.305e-03, 2.238e-03, 2.034e-03, 1.647e-03, 1.417e-03, 1.148e-03, 1.265e-03, 5.559e-04, 4.182e-04, 7.158e-04, 2.401e-04, 1.341e-04, 9.239e-05, 4.829e-05, 1.037e-04, 1.252e-05, 2.352e-05, 3.136e-05, 1.602e-05, 7.544e-06, 1.381e-06, 8.050e-07, 7.367e-07, 7.117e-07, 2.885e-06, 1.295e-06, 1.044e-07, 6.063e-08, 1.026e-06, 2.088e-06, 1.008e-08, 1.660e-08, 0.000e+0}},
{"TTToHadronic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8",{2.829e-04, 3.465e-02, 4.626e-02, 5.431e-02, 8.272e-02, 1.221e-01, 1.481e-01, 1.634e-01, 1.523e-01, 4.725e-01, 6.685e-01, 8.936e-01, 9.093e-01, 9.525e-01, 9.696e-01, 1.052e+00, 1.224e+00, 1.265e+00, 1.349e+00, 1.363e+00, 1.388e+00, 1.418e+00, 1.435e+00, 1.449e+00, 1.477e+00, 1.460e+00, 1.457e+00, 1.423e+00, 1.414e+00, 1.367e+00, 1.302e+00, 1.220e+00, 1.129e+00, 1.043e+00, 9.500e-01, 8.917e-01, 8.469e-01, 8.161e-01, 7.792e-01, 7.693e-01, 8.132e-01, 8.946e-01, 1.033e+00, 1.190e+00, 1.353e+00, 1.501e+00, 1.622e+00, 1.566e+00, 1.416e+00, 1.216e+00, 9.669e-01, 7.148e-01, 5.358e-01, 3.715e-01, 2.456e-01, 1.618e-01, 1.048e-01, 6.718e-02, 4.339e-02, 2.863e-02, 1.945e-02, 1.357e-02, 1.004e-02, 7.325e-03, 5.777e-03, 4.291e-03, 2.986e-03, 2.558e-03, 2.470e-03, 2.409e-03, 1.600e-03, 1.807e-03, 1.373e-03, 1.436e-03, 1.374e-03, 9.078e-04, 6.755e-04, 6.239e-04, 1.878e-04, 8.462e-05, 2.569e-05, 4.162e-05, 3.964e-05, 8.270e-06, 2.485e-05, 3.388e-05, 9.903e-06, 1.898e-06, 1.959e-06, 1.469e-06, 1.633e-06, 3.335e-06, 9.801e-05, 6.832e-07, 1.284e-07, 3.752e-08, 1.038e-06, 2.027e-07, 1.513e-08, 1.470e-08, 0.000e+0}},
{"TTToHadronic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8",{2.841e-04, 4.469e-02, 5.766e-02, 4.942e-02, 8.264e-02, 1.200e-01, 1.081e-01, 1.749e-01, 1.630e-01, 4.510e-01, 6.739e-01, 8.436e-01, 9.218e-01, 9.460e-01, 9.839e-01, 1.093e+00, 1.201e+00, 1.271e+00, 1.331e+00, 1.351e+00, 1.369e+00, 1.406e+00, 1.431e+00, 1.453e+00, 1.470e+00, 1.465e+00, 1.448e+00, 1.431e+00, 1.400e+00, 1.361e+00, 1.301e+00, 1.207e+00, 1.123e+00, 1.045e+00, 9.638e-01, 8.990e-01, 8.487e-01, 8.162e-01, 7.854e-01, 7.716e-01, 8.104e-01, 8.947e-01, 1.036e+00, 1.191e+00, 1.370e+00, 1.513e+00, 1.607e+00, 1.553e+00, 1.406e+00, 1.168e+00, 9.581e-01, 7.382e-01, 5.292e-01, 3.708e-01, 2.483e-01, 1.632e-01, 1.057e-01, 6.734e-02, 4.289e-02, 2.893e-02, 1.938e-02, 1.394e-02, 1.021e-02, 7.504e-03, 6.031e-03, 4.265e-03, 3.083e-03, 2.745e-03, 2.494e-03, 2.102e-03, 1.674e-03, 1.536e-03, 1.244e-03, 1.599e-03, 1.104e-03, 5.129e-04, 9.076e-04, 3.397e-04, 1.999e-04, 8.595e-05, 3.472e-05, 4.473e-05, 3.432e-05, 1.059e-05, 1.265e-05, 9.724e-06, 7.472e-06, 3.631e-06, 1.430e-06, 3.656e-06, 1.309e-06, 1.786e-05, 8.265e-05, 2.694e-07, 3.464e-07, 3.073e-08, 1.446e-06, 6.299e-07, 8.263e-08, 1.493e-08, 0.000e+0}},
{"TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.895e-01, 3.831e+00, 4.195e+00, 2.451e+00, 2.066e+00, 1.687e+00, 1.374e+00, 1.398e+00, 8.974e-01, 2.196e+00, 2.201e+00, 2.075e+00, 1.727e+00, 1.531e+00, 1.435e+00, 1.415e+00, 1.433e+00, 1.435e+00, 1.428e+00, 1.408e+00, 1.396e+00, 1.389e+00, 1.390e+00, 1.398e+00, 1.392e+00, 1.384e+00, 1.362e+00, 1.326e+00, 1.311e+00, 1.258e+00, 1.200e+00, 1.125e+00, 1.042e+00, 9.555e-01, 8.732e-01, 8.184e-01, 7.726e-01, 7.477e-01, 7.145e-01, 7.056e-01, 7.492e-01, 8.272e-01, 9.460e-01, 1.089e+00, 1.252e+00, 1.388e+00, 1.485e+00, 1.436e+00, 1.321e+00, 1.125e+00, 9.091e-01, 6.889e-01, 4.987e-01, 3.500e-01, 2.378e-01, 1.544e-01, 9.984e-02, 6.290e-02, 4.057e-02, 2.688e-02, 1.829e-02, 1.294e-02, 9.484e-03, 7.247e-03, 5.852e-03, 4.065e-03, 3.059e-03, 2.678e-03, 2.413e-03, 2.223e-03, 2.142e-03, 2.030e-03, 1.962e-03, 2.024e-03, 1.552e-03, 1.339e-03, 1.319e-03, 1.281e-03, 1.207e-03, 1.346e-03, 1.194e-03, 1.330e-03, 1.388e-03, 8.579e-04, 6.421e-04, 5.477e-04, 1.052e-03, 5.687e-04, 1.227e-03, 3.060e-04, 3.084e-04, 0.000e+00, 4.397e-05, 1.102e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.885e-01, 4.226e+00, 4.554e+00, 2.475e+00, 1.896e+00, 1.697e+00, 1.336e+00, 1.397e+00, 8.874e-01, 2.165e+00, 2.186e+00, 2.067e+00, 1.748e+00, 1.540e+00, 1.439e+00, 1.423e+00, 1.433e+00, 1.433e+00, 1.425e+00, 1.408e+00, 1.393e+00, 1.389e+00, 1.391e+00, 1.393e+00, 1.392e+00, 1.382e+00, 1.361e+00, 1.330e+00, 1.309e+00, 1.257e+00, 1.201e+00, 1.125e+00, 1.044e+00, 9.542e-01, 8.772e-01, 8.165e-01, 7.732e-01, 7.466e-01, 7.155e-01, 7.042e-01, 7.463e-01, 8.271e-01, 9.429e-01, 1.089e+00, 1.250e+00, 1.394e+00, 1.484e+00, 1.436e+00, 1.323e+00, 1.123e+00, 9.069e-01, 6.897e-01, 5.004e-01, 3.501e-01, 2.378e-01, 1.549e-01, 9.976e-02, 6.303e-02, 4.067e-02, 2.693e-02, 1.835e-02, 1.299e-02, 9.509e-03, 7.294e-03, 5.808e-03, 4.118e-03, 3.039e-03, 2.659e-03, 2.417e-03, 2.242e-03, 2.120e-03, 2.049e-03, 2.009e-03, 1.968e-03, 1.546e-03, 1.272e-03, 1.265e-03, 1.220e-03, 1.282e-03, 1.237e-03, 1.225e-03, 1.244e-03, 1.172e-03, 8.465e-04, 6.915e-04, 7.164e-04, 5.537e-04, 6.667e-04, 6.286e-04, 5.342e-04, 3.751e-04, 4.867e-04, 1.592e-04, 1.617e-04, 3.786e-04, 2.749e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToSemiLeptonic_TuneCP5_erdON_13TeV-powheg-pythia8",{2.035e-01, 4.812e+00, 4.664e+00, 2.618e+00, 1.758e+00, 1.613e+00, 1.397e+00, 1.483e+00, 9.205e-01, 2.212e+00, 2.221e+00, 2.062e+00, 1.743e+00, 1.533e+00, 1.452e+00, 1.427e+00, 1.433e+00, 1.435e+00, 1.421e+00, 1.405e+00, 1.388e+00, 1.385e+00, 1.394e+00, 1.396e+00, 1.394e+00, 1.382e+00, 1.363e+00, 1.325e+00, 1.312e+00, 1.257e+00, 1.200e+00, 1.127e+00, 1.044e+00, 9.551e-01, 8.771e-01, 8.172e-01, 7.737e-01, 7.471e-01, 7.137e-01, 7.056e-01, 7.449e-01, 8.255e-01, 9.477e-01, 1.084e+00, 1.251e+00, 1.402e+00, 1.477e+00, 1.435e+00, 1.326e+00, 1.124e+00, 9.044e-01, 6.915e-01, 5.005e-01, 3.510e-01, 2.378e-01, 1.543e-01, 9.980e-02, 6.262e-02, 4.066e-02, 2.677e-02, 1.832e-02, 1.291e-02, 9.575e-03, 7.228e-03, 5.841e-03, 4.089e-03, 3.075e-03, 2.666e-03, 2.399e-03, 2.263e-03, 2.145e-03, 2.045e-03, 1.972e-03, 1.910e-03, 1.654e-03, 1.288e-03, 1.315e-03, 1.234e-03, 1.407e-03, 1.287e-03, 1.250e-03, 1.310e-03, 1.353e-03, 8.980e-04, 6.455e-04, 6.927e-04, 5.408e-04, 1.607e-03, 4.728e-04, 5.503e-04, 2.535e-04, 7.220e-04, 1.356e-04, 1.133e-04, 1.248e-04, 3.399e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToSemiLeptonic_TuneCP5down_PSweights_13TeV-powheg-pythia8",{2.715e-04, 3.745e-02, 4.987e-02, 4.880e-02, 6.678e-02, 1.084e-01, 1.586e-01, 1.543e-01, 1.506e-01, 4.613e-01, 6.597e-01, 9.356e-01, 9.103e-01, 9.631e-01, 9.986e-01, 1.078e+00, 1.190e+00, 1.278e+00, 1.299e+00, 1.359e+00, 1.390e+00, 1.409e+00, 1.436e+00, 1.463e+00, 1.480e+00, 1.472e+00, 1.453e+00, 1.444e+00, 1.414e+00, 1.363e+00, 1.306e+00, 1.217e+00, 1.141e+00, 1.056e+00, 9.636e-01, 8.985e-01, 8.516e-01, 8.183e-01, 7.828e-01, 7.678e-01, 8.183e-01, 8.943e-01, 1.042e+00, 1.179e+00, 1.377e+00, 1.503e+00, 1.629e+00, 1.531e+00, 1.420e+00, 1.227e+00, 9.552e-01, 7.283e-01, 5.218e-01, 3.700e-01, 2.556e-01, 1.600e-01, 1.062e-01, 6.757e-02, 4.341e-02, 2.896e-02, 1.963e-02, 1.335e-02, 1.020e-02, 7.365e-03, 5.895e-03, 4.031e-03, 3.147e-03, 2.764e-03, 2.460e-03, 2.097e-03, 2.337e-03, 1.853e-03, 9.900e-04, 1.653e-03, 1.152e-03, 7.397e-04, 6.539e-04, 5.991e-04, 1.008e-04, 6.072e-05, 3.368e-05, 2.654e-05, 3.151e-05, 9.265e-06, 1.555e-05, 6.358e-06, 9.266e-06, 1.681e-06, 3.197e-06, 2.852e-07, 1.593e-04, 1.425e-04, 1.124e-04, 1.228e-06, 1.139e-07, 2.490e-08, 1.581e-06, 6.922e-08, 4.242e-08, 2.036e-08, 0.000e+0}},
{"TTToSemiLeptonic_TuneCP5up_PSweights_13TeV-powheg-pythia8",{3.188e-04, 6.404e-02, 6.507e-02, 7.014e-02, 8.895e-02, 1.359e-01, 1.604e-01, 1.803e-01, 1.717e-01, 5.309e-01, 7.227e-01, 8.487e-01, 9.217e-01, 9.764e-01, 9.800e-01, 1.048e+00, 1.160e+00, 1.251e+00, 1.318e+00, 1.364e+00, 1.386e+00, 1.412e+00, 1.419e+00, 1.449e+00, 1.460e+00, 1.461e+00, 1.429e+00, 1.430e+00, 1.404e+00, 1.357e+00, 1.298e+00, 1.214e+00, 1.127e+00, 1.037e+00, 9.476e-01, 8.875e-01, 8.376e-01, 8.162e-01, 7.797e-01, 7.709e-01, 8.025e-01, 8.984e-01, 1.030e+00, 1.185e+00, 1.360e+00, 1.510e+00, 1.589e+00, 1.535e+00, 1.390e+00, 1.208e+00, 9.473e-01, 7.162e-01, 5.198e-01, 3.704e-01, 2.504e-01, 1.628e-01, 1.047e-01, 6.697e-02, 4.338e-02, 2.870e-02, 1.946e-02, 1.372e-02, 1.018e-02, 7.490e-03, 5.798e-03, 4.325e-03, 2.942e-03, 2.691e-03, 2.409e-03, 2.231e-03, 2.118e-03, 1.525e-03, 1.443e-03, 1.274e-03, 9.005e-04, 8.783e-04, 4.565e-04, 4.337e-04, 3.506e-04, 6.846e-05, 3.553e-05, 3.957e-05, 2.378e-05, 5.596e-05, 1.346e-05, 9.050e-06, 5.138e-06, 1.835e-06, 1.382e-06, 4.010e-06, 1.644e-06, 7.328e-05, 1.534e-06, 1.768e-07, 1.119e-07, 1.934e-08, 1.191e-06, 8.957e-08, 6.440e-08, 1.836e-08, 0.000e+0}},
{"TTToSemiLeptonic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.995e-01, 3.967e+00, 3.971e+00, 2.442e+00, 1.946e+00, 1.714e+00, 1.354e+00, 1.410e+00, 8.915e-01, 2.198e+00, 2.186e+00, 2.086e+00, 1.746e+00, 1.539e+00, 1.437e+00, 1.422e+00, 1.434e+00, 1.431e+00, 1.425e+00, 1.408e+00, 1.392e+00, 1.392e+00, 1.393e+00, 1.391e+00, 1.391e+00, 1.380e+00, 1.359e+00, 1.329e+00, 1.309e+00, 1.256e+00, 1.199e+00, 1.126e+00, 1.042e+00, 9.571e-01, 8.768e-01, 8.160e-01, 7.746e-01, 7.469e-01, 7.162e-01, 7.042e-01, 7.479e-01, 8.268e-01, 9.440e-01, 1.088e+00, 1.249e+00, 1.392e+00, 1.484e+00, 1.433e+00, 1.326e+00, 1.127e+00, 9.083e-01, 6.922e-01, 5.018e-01, 3.497e-01, 2.378e-01, 1.549e-01, 9.974e-02, 6.279e-02, 4.064e-02, 2.688e-02, 1.834e-02, 1.295e-02, 9.494e-03, 7.271e-03, 5.785e-03, 4.124e-03, 3.035e-03, 2.666e-03, 2.418e-03, 2.206e-03, 2.132e-03, 2.056e-03, 1.995e-03, 2.018e-03, 1.566e-03, 1.271e-03, 1.295e-03, 1.240e-03, 1.316e-03, 1.323e-03, 1.261e-03, 1.350e-03, 1.105e-03, 8.262e-04, 6.447e-04, 6.517e-04, 5.981e-04, 5.092e-04, 7.917e-04, 6.452e-04, 1.955e-04, 1.058e-03, 9.933e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToSemiLeptonic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8",{3.126e-04, 3.189e-02, 5.629e-02, 5.042e-02, 7.936e-02, 1.171e-01, 1.471e-01, 1.841e-01, 1.686e-01, 4.304e-01, 7.634e-01, 9.000e-01, 9.004e-01, 9.629e-01, 1.029e+00, 1.115e+00, 1.213e+00, 1.292e+00, 1.337e+00, 1.352e+00, 1.384e+00, 1.415e+00, 1.439e+00, 1.456e+00, 1.455e+00, 1.446e+00, 1.425e+00, 1.421e+00, 1.400e+00, 1.346e+00, 1.296e+00, 1.216e+00, 1.122e+00, 1.040e+00, 9.536e-01, 8.801e-01, 8.397e-01, 8.141e-01, 7.737e-01, 7.659e-01, 8.031e-01, 8.940e-01, 1.026e+00, 1.183e+00, 1.355e+00, 1.506e+00, 1.621e+00, 1.543e+00, 1.409e+00, 1.204e+00, 9.487e-01, 7.263e-01, 5.196e-01, 3.729e-01, 2.456e-01, 1.630e-01, 1.019e-01, 6.724e-02, 4.255e-02, 2.853e-02, 1.953e-02, 1.375e-02, 1.021e-02, 7.391e-03, 5.577e-03, 4.301e-03, 3.148e-03, 2.607e-03, 2.518e-03, 2.012e-03, 1.935e-03, 1.566e-03, 1.211e-03, 1.365e-03, 7.947e-04, 8.031e-04, 5.383e-04, 4.419e-04, 3.980e-04, 1.882e-04, 4.344e-05, 4.107e-05, 4.763e-05, 7.918e-05, 1.451e-05, 2.587e-05, 6.484e-06, 2.615e-06, 1.481e-06, 1.097e-06, 1.659e-04, 1.811e-04, 7.897e-06, 5.621e-07, 2.249e-06, 3.679e-08, 1.489e-06, 3.086e-06, 8.668e-08, 1.779e-08, 0.000e+0}},
{"TTWH_TuneCP5_13TeV-madgraph-pythia8",{2.671e-04, 3.342e-02, 5.474e-02, 2.868e-01, 2.490e-01, 2.040e-01, 1.581e-01, 1.638e-01, 1.062e-01, 2.731e-01, 8.390e-01, 1.055e+00, 9.666e-01, 8.276e-01, 8.032e-01, 5.275e-01, 1.047e+00, 1.360e+00, 1.433e+00, 1.456e+00, 1.413e+00, 1.339e+00, 1.444e+00, 1.448e+00, 1.486e+00, 1.537e+00, 1.534e+00, 1.436e+00, 1.500e+00, 1.431e+00, 1.330e+00, 1.239e+00, 1.168e+00, 1.064e+00, 9.688e-01, 9.196e-01, 8.662e-01, 8.051e-01, 8.150e-01, 7.862e-01, 8.155e-01, 9.051e-01, 1.106e+00, 1.221e+00, 1.440e+00, 1.534e+00, 1.611e+00, 1.562e+00, 1.445e+00, 1.243e+00, 9.372e-01, 7.025e-01, 3.200e-01, 3.757e-01, 2.542e-01, 1.625e-01, 1.093e-01, 6.953e-02, 4.395e-02, 2.885e-02, 1.977e-02, 1.349e-02, 1.079e-02, 7.656e-03, 6.038e-03, 4.270e-03, 3.220e-03, 2.833e-03, 2.519e-03, 1.228e-03, 2.086e-03, 2.199e-03, 1.023e-03, 5.633e-04, 2.128e-03, 1.034e-03, 7.952e-04, 5.857e-04, 1.214e-03, 3.489e-03, 2.212e-03, 2.783e-03, 8.678e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 8.367e-05, 0.000e+00, 0.000e+00, 0.000e+00, 8.998e-06, 0.000e+00, 0.000e+00, 0.000e+00, 4.049e-07, 4.311e-07, 2.268e-07, 1.311e-08, 0.000e+0}},
{"TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8",{2.031e-01, 3.047e+00, 3.856e+00, 2.538e+00, 1.643e+00, 1.659e+00, 1.467e+00, 1.320e+00, 9.143e-01, 2.194e+00, 2.266e+00, 2.033e+00, 1.771e+00, 1.520e+00, 1.442e+00, 1.440e+00, 1.447e+00, 1.429e+00, 1.430e+00, 1.398e+00, 1.396e+00, 1.390e+00, 1.384e+00, 1.383e+00, 1.394e+00, 1.380e+00, 1.375e+00, 1.326e+00, 1.313e+00, 1.268e+00, 1.205e+00, 1.117e+00, 1.044e+00, 9.606e-01, 8.740e-01, 8.123e-01, 7.709e-01, 7.412e-01, 7.125e-01, 7.007e-01, 7.506e-01, 8.236e-01, 9.460e-01, 1.099e+00, 1.252e+00, 1.384e+00, 1.477e+00, 1.434e+00, 1.320e+00, 1.119e+00, 9.096e-01, 6.837e-01, 4.975e-01, 3.471e-01, 2.370e-01, 1.554e-01, 1.001e-01, 6.346e-02, 4.185e-02, 2.691e-02, 1.843e-02, 1.280e-02, 9.662e-03, 7.430e-03, 5.706e-03, 4.096e-03, 3.084e-03, 2.683e-03, 2.415e-03, 2.269e-03, 2.093e-03, 1.925e-03, 1.895e-03, 1.887e-03, 1.642e-03, 1.407e-03, 1.320e-03, 1.120e-03, 1.214e-03, 2.004e-03, 9.836e-04, 1.421e-03, 1.139e-03, 1.848e-03, 1.132e-03, 6.102e-04, 4.711e-04, 9.801e-04, 3.844e-04, 1.678e-04, -3.865e-04, 0.000e+00, 0.000e+00, 3.454e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",{1.251e-01, 4.253e+00, 3.492e+00, 2.043e+00, 1.604e+00, 1.884e+00, 1.037e+00, 1.313e+00, 9.244e-01, 2.366e+00, 2.117e+00, 2.126e+00, 1.867e+00, 1.542e+00, 1.503e+00, 1.417e+00, 1.427e+00, 1.431e+00, 1.460e+00, 1.385e+00, 1.389e+00, 1.399e+00, 1.395e+00, 1.393e+00, 1.412e+00, 1.391e+00, 1.361e+00, 1.332e+00, 1.311e+00, 1.260e+00, 1.188e+00, 1.130e+00, 1.054e+00, 9.543e-01, 8.923e-01, 8.015e-01, 7.676e-01, 7.641e-01, 7.249e-01, 6.891e-01, 7.425e-01, 8.105e-01, 9.428e-01, 1.061e+00, 1.253e+00, 1.403e+00, 1.508e+00, 1.425e+00, 1.334e+00, 1.121e+00, 8.885e-01, 6.830e-01, 5.140e-01, 3.482e-01, 2.328e-01, 1.493e-01, 9.857e-02, 6.193e-02, 4.124e-02, 2.697e-02, 1.897e-02, 1.327e-02, 9.227e-03, 7.136e-03, 6.207e-03, 4.300e-03, 3.053e-03, 2.754e-03, 2.110e-03, 2.073e-03, 1.878e-03, 1.941e-03, 2.063e-03, 2.346e-03, 1.191e-03, 1.178e-03, 1.324e-03, 1.142e-03, 1.154e-03, 8.150e-04, 9.818e-04, 8.822e-04, 9.628e-04, 2.381e-03, 4.859e-04, 4.421e-04, 5.310e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTWW_TuneCP5_13TeV-madgraph-pythia8",{7.356e-04, 6.389e-01, 8.394e-01, 4.729e-01, 2.801e-01, 2.417e-01, 3.886e-01, 4.766e-01, 3.224e-01, 8.697e-01, 8.827e-01, 8.187e-01, 7.538e-01, 7.170e-01, 9.072e-01, 1.027e+00, 1.212e+00, 1.311e+00, 1.403e+00, 1.320e+00, 1.366e+00, 1.376e+00, 1.411e+00, 1.367e+00, 1.503e+00, 1.480e+00, 1.478e+00, 1.482e+00, 1.413e+00, 1.379e+00, 1.213e+00, 1.253e+00, 1.129e+00, 1.058e+00, 9.632e-01, 9.203e-01, 8.383e-01, 8.306e-01, 7.804e-01, 7.535e-01, 8.225e-01, 9.036e-01, 1.047e+00, 1.184e+00, 1.351e+00, 1.218e+00, 1.653e+00, 1.578e+00, 1.491e+00, 1.218e+00, 9.032e-01, 6.766e-01, 5.027e-01, 3.541e-01, 2.483e-01, 9.517e-02, 1.017e-01, 6.473e-02, 4.231e-02, 2.787e-02, 1.888e-02, 1.354e-02, 1.011e-02, 7.635e-03, 6.273e-03, 4.453e-03, 3.436e-03, 2.731e-03, 1.430e-03, 2.428e-03, 2.212e-03, 2.094e-03, 2.983e-03, 2.295e-03, 1.505e-03, 1.441e-03, 9.721e-04, 1.307e-03, 7.804e-04, 1.427e-05, 1.475e-03, 9.278e-04, 8.679e-04, 3.541e-06, 2.190e-04, 4.655e-07, 0.000e+00, 1.423e-04, 0.000e+00, 1.331e-07, 0.000e+00, 1.598e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 1.475e-08, 0.000e+0}},
{"TTWZ_TuneCP5_13TeV-madgraph-pythia8",{2.368e-03, 3.022e-01, 2.620e-01, 1.697e-01, 6.395e-01, 5.410e-01, 4.412e-01, 3.899e-01, 3.303e-01, 7.198e-01, 7.629e-01, 6.853e-01, 5.942e-01, 9.435e-01, 1.038e+00, 1.280e+00, 1.326e+00, 1.404e+00, 1.396e+00, 1.365e+00, 1.435e+00, 1.431e+00, 1.381e+00, 1.441e+00, 1.467e+00, 1.401e+00, 1.391e+00, 1.387e+00, 1.382e+00, 1.311e+00, 1.258e+00, 1.141e+00, 1.073e+00, 9.892e-01, 9.331e-01, 8.859e-01, 8.100e-01, 7.967e-01, 7.482e-01, 7.493e-01, 7.884e-01, 8.494e-01, 1.010e+00, 1.126e+00, 1.212e+00, 1.506e+00, 1.637e+00, 1.541e+00, 1.390e+00, 1.099e+00, 9.551e-01, 5.990e-01, 5.229e-01, 3.648e-01, 2.484e-01, 1.578e-01, 1.022e-01, 3.832e-02, 4.188e-02, 2.707e-02, 1.906e-02, 1.301e-02, 9.247e-03, 7.603e-03, 6.107e-03, 4.206e-03, 3.032e-03, 2.703e-03, 2.476e-03, 2.232e-03, 2.317e-03, 2.289e-03, 2.014e-03, 1.807e-03, 1.433e-03, 1.151e-03, 1.380e-03, 1.212e-03, 1.364e-03, 1.162e-03, 8.839e-04, 1.390e-03, 0.000e+00, 2.679e-04, 3.281e-04, 1.990e-04, 0.000e+00, 7.175e-07, 8.358e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 1.618e-07, 2.153e-07, 0.000e+00, 1.684e-08, 0.000e+0}},
{"TTZH_TuneCP5_13TeV-madgraph-pythia8",{2.409e-03, 1.919e+00, 1.801e+00, 1.031e+00, 8.015e-01, 1.049e+00, 8.499e-01, 8.749e-01, 4.980e-01, 1.752e+00, 1.714e+00, 1.791e+00, 1.354e+00, 1.262e+00, 1.199e+00, 1.165e+00, 1.182e+00, 1.214e+00, 1.216e+00, 1.277e+00, 1.295e+00, 1.260e+00, 1.332e+00, 1.339e+00, 1.437e+00, 1.402e+00, 1.346e+00, 1.342e+00, 1.397e+00, 1.333e+00, 1.202e+00, 1.175e+00, 1.094e+00, 1.026e+00, 9.439e-01, 8.486e-01, 8.195e-01, 8.004e-01, 7.682e-01, 7.525e-01, 8.215e-01, 8.752e-01, 1.011e+00, 8.753e-01, 1.350e+00, 1.567e+00, 1.603e+00, 1.550e+00, 1.427e+00, 1.219e+00, 9.499e-01, 4.644e-01, 5.221e-01, 3.593e-01, 2.549e-01, 1.617e-01, 1.020e-01, 6.699e-02, 4.198e-02, 2.875e-02, 1.941e-02, 1.306e-02, 9.827e-03, 8.009e-03, 5.952e-03, 4.170e-03, 3.510e-03, 2.704e-03, 2.624e-03, 2.278e-03, 2.425e-03, 1.848e-03, 2.048e-03, 2.141e-03, 1.545e-03, 1.554e-03, 1.252e-03, 1.215e-03, 1.368e-03, 1.747e-03, 8.672e-06, 6.968e-04, 8.691e-04, 3.581e-04, 3.290e-04, 0.000e+00, 0.000e+00, 1.424e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 8.110e-07, 1.439e-07, 0.000e+00, 1.688e-08, 0.000e+0}},
{"TTZToLLNuNu_M-10_TuneCP5_PSweights_13TeV-amcatnlo-pythia8",{1.997e-01, 3.784e+00, 4.362e+00, 2.258e+00, 1.804e+00, 1.983e+00, 1.367e+00, 1.400e+00, 9.395e-01, 2.191e+00, 2.173e+00, 2.065e+00, 1.718e+00, 1.550e+00, 1.435e+00, 1.426e+00, 1.445e+00, 1.437e+00, 1.420e+00, 1.411e+00, 1.397e+00, 1.397e+00, 1.391e+00, 1.403e+00, 1.393e+00, 1.387e+00, 1.357e+00, 1.332e+00, 1.302e+00, 1.259e+00, 1.204e+00, 1.128e+00, 1.041e+00, 9.517e-01, 8.769e-01, 8.171e-01, 7.745e-01, 7.495e-01, 7.114e-01, 6.997e-01, 7.466e-01, 8.277e-01, 9.401e-01, 1.092e+00, 1.259e+00, 1.392e+00, 1.480e+00, 1.435e+00, 1.316e+00, 1.120e+00, 8.938e-01, 6.857e-01, 4.982e-01, 3.483e-01, 2.379e-01, 1.554e-01, 9.930e-02, 6.293e-02, 4.058e-02, 2.670e-02, 1.834e-02, 1.316e-02, 9.518e-03, 7.353e-03, 5.821e-03, 4.125e-03, 3.031e-03, 2.742e-03, 2.429e-03, 2.225e-03, 2.067e-03, 2.071e-03, 1.998e-03, 1.901e-03, 1.636e-03, 1.283e-03, 1.455e-03, 1.278e-03, 1.376e-03, 1.303e-03, 1.574e-03, 1.078e-03, 1.235e-03, 7.243e-04, 5.580e-04, 8.071e-04, 7.001e-04, 4.161e-04, 5.508e-04, 3.206e-04, 1.477e-04, 0.000e+00, 2.369e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8",{4.207e-01, 0.000e+00, 4.085e+00, -1.135e+01, 2.423e+00, 1.853e+00, 1.162e+00, 1.488e+00, 8.325e-01, 3.483e+00, 2.685e+00, 2.055e+00, 1.789e+00, 1.516e+00, 1.343e+00, 1.412e+00, 1.516e+00, 1.415e+00, 1.398e+00, 1.388e+00, 1.381e+00, 1.393e+00, 1.371e+00, 1.447e+00, 1.384e+00, 1.370e+00, 1.457e+00, 1.348e+00, 1.301e+00, 1.264e+00, 1.190e+00, 1.096e+00, 1.033e+00, 9.617e-01, 8.626e-01, 8.266e-01, 7.869e-01, 7.300e-01, 7.163e-01, 6.802e-01, 7.604e-01, 8.329e-01, 9.470e-01, 1.081e+00, 1.275e+00, 1.384e+00, 1.438e+00, 1.377e+00, 1.291e+00, 1.128e+00, 9.077e-01, 6.383e-01, 5.204e-01, 4.036e-01, 2.436e-01, 1.460e-01, 1.013e-01, 6.420e-02, 3.982e-02, 2.836e-02, 1.868e-02, 1.203e-02, 9.969e-03, 6.872e-03, 5.573e-03, 4.003e-03, 2.997e-03, 2.474e-03, 2.303e-03, 2.403e-03, 2.031e-03, 3.446e-03, 1.976e-03, 2.180e-03, 1.483e-03, 1.539e-03, 0.000e+00, 1.225e-03, 5.907e-04, 1.509e-03, -2.871e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, -9.229e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTZZ_TuneCP5_13TeV-madgraph-pythia8",{2.123e-04, 3.388e-01, 2.138e-01, 1.437e-01, 1.111e-01, 1.809e-01, 2.485e-01, 3.676e-01, 2.882e-01, 7.089e-01, 8.338e-01, 7.520e-01, 7.579e-01, 1.291e+00, 1.175e+00, 8.262e-01, 1.222e+00, 1.205e+00, 1.143e+00, 1.230e+00, 1.319e+00, 1.390e+00, 1.305e+00, 1.460e+00, 1.450e+00, 1.434e+00, 1.387e+00, 1.371e+00, 1.444e+00, 1.391e+00, 1.370e+00, 1.252e+00, 1.178e+00, 1.074e+00, 9.918e-01, 9.355e-01, 8.835e-01, 6.386e-01, 8.027e-01, 8.032e-01, 8.288e-01, 9.525e-01, 1.099e+00, 1.018e+00, 1.419e+00, 1.550e+00, 1.753e+00, 1.688e+00, 1.535e+00, 1.314e+00, 7.303e-01, 7.831e-01, 5.692e-01, 3.889e-01, 2.587e-01, 1.686e-01, 1.060e-01, 7.208e-02, 4.521e-02, 2.952e-02, 2.079e-02, 1.422e-02, 1.058e-02, 8.012e-03, 6.494e-03, 4.541e-03, 2.566e-03, 2.878e-03, 2.540e-03, 2.567e-03, 1.978e-03, 2.296e-03, 2.313e-03, 1.746e-03, 1.374e-03, 1.122e-03, 1.461e-03, 1.309e-03, 8.420e-04, 7.769e-04, 1.478e-03, 1.394e-03, 1.739e-03, 3.583e-04, 3.291e-04, 2.661e-05, 2.397e-04, 1.425e-04, 0.000e+00, 0.000e+00, 0.000e+00, 1.600e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 4.057e-07, 0.000e+00, 0.000e+00, 1.970e-08, 0.000e+0}},
{"WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8",{1.965e-01, 5.202e+00, 4.177e+00, 2.313e+00, 2.084e+00, 1.658e+00, 1.385e+00, 1.358e+00, 8.829e-01, 2.226e+00, 2.219e+00, 2.058e+00, 1.727e+00, 1.532e+00, 1.436e+00, 1.417e+00, 1.433e+00, 1.436e+00, 1.423e+00, 1.408e+00, 1.393e+00, 1.387e+00, 1.390e+00, 1.393e+00, 1.391e+00, 1.382e+00, 1.362e+00, 1.331e+00, 1.310e+00, 1.258e+00, 1.200e+00, 1.124e+00, 1.043e+00, 9.556e-01, 8.772e-01, 8.185e-01, 7.725e-01, 7.491e-01, 7.175e-01, 7.042e-01, 7.470e-01, 8.261e-01, 9.421e-01, 1.089e+00, 1.247e+00, 1.394e+00, 1.484e+00, 1.434e+00, 1.321e+00, 1.124e+00, 9.079e-01, 6.900e-01, 5.002e-01, 3.499e-01, 2.381e-01, 1.548e-01, 9.972e-02, 6.322e-02, 4.067e-02, 2.690e-02, 1.829e-02, 1.293e-02, 9.505e-03, 7.294e-03, 5.818e-03, 4.106e-03, 3.032e-03, 2.647e-03, 2.414e-03, 2.240e-03, 2.128e-03, 2.074e-03, 1.968e-03, 1.989e-03, 1.550e-03, 1.276e-03, 1.285e-03, 1.303e-03, 1.273e-03, 1.311e-03, 1.335e-03, 1.226e-03, 1.200e-03, 7.738e-04, 5.542e-04, 5.666e-04, 6.437e-04, 8.328e-04, 4.383e-04, 2.308e-04, 3.988e-04, 5.300e-04, 2.985e-04, 9.979e-05, 0.000e+00, 1.497e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8",{2.002e-01, 4.710e+00, 4.499e+00, 2.398e+00, 1.891e+00, 1.709e+00, 1.344e+00, 1.424e+00, 8.680e-01, 2.147e+00, 2.161e+00, 2.054e+00, 1.741e+00, 1.539e+00, 1.446e+00, 1.420e+00, 1.430e+00, 1.431e+00, 1.425e+00, 1.407e+00, 1.392e+00, 1.390e+00, 1.387e+00, 1.393e+00, 1.393e+00, 1.384e+00, 1.361e+00, 1.330e+00, 1.307e+00, 1.260e+00, 1.200e+00, 1.123e+00, 1.046e+00, 9.542e-01, 8.771e-01, 8.183e-01, 7.745e-01, 7.458e-01, 7.144e-01, 7.048e-01, 7.459e-01, 8.286e-01, 9.442e-01, 1.086e+00, 1.251e+00, 1.395e+00, 1.485e+00, 1.432e+00, 1.327e+00, 1.123e+00, 9.097e-01, 6.906e-01, 5.014e-01, 3.506e-01, 2.376e-01, 1.545e-01, 9.954e-02, 6.282e-02, 4.064e-02, 2.691e-02, 1.840e-02, 1.294e-02, 9.575e-03, 7.267e-03, 5.819e-03, 4.135e-03, 3.046e-03, 2.656e-03, 2.380e-03, 2.224e-03, 2.111e-03, 2.064e-03, 2.000e-03, 1.955e-03, 1.555e-03, 1.309e-03, 1.291e-03, 1.245e-03, 1.340e-03, 1.191e-03, 1.250e-03, 1.411e-03, 1.302e-03, 7.324e-04, 6.793e-04, 8.161e-04, 5.201e-04, 8.416e-04, 3.713e-04, 3.990e-04, 3.733e-04, 5.671e-04, 1.917e-04, 1.068e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8",{1.980e-01, 4.550e+00, 4.265e+00, 2.562e+00, 1.861e+00, 1.661e+00, 1.342e+00, 1.392e+00, 9.020e-01, 2.140e+00, 2.172e+00, 2.063e+00, 1.752e+00, 1.533e+00, 1.435e+00, 1.418e+00, 1.433e+00, 1.435e+00, 1.427e+00, 1.407e+00, 1.394e+00, 1.390e+00, 1.394e+00, 1.394e+00, 1.392e+00, 1.378e+00, 1.363e+00, 1.329e+00, 1.309e+00, 1.256e+00, 1.201e+00, 1.126e+00, 1.043e+00, 9.545e-01, 8.770e-01, 8.185e-01, 7.750e-01, 7.473e-01, 7.148e-01, 7.015e-01, 7.485e-01, 8.262e-01, 9.442e-01, 1.092e+00, 1.244e+00, 1.393e+00, 1.480e+00, 1.435e+00, 1.321e+00, 1.123e+00, 9.089e-01, 6.890e-01, 4.999e-01, 3.502e-01, 2.381e-01, 1.547e-01, 9.950e-02, 6.297e-02, 4.061e-02, 2.695e-02, 1.839e-02, 1.292e-02, 9.498e-03, 7.314e-03, 5.797e-03, 4.151e-03, 3.056e-03, 2.686e-03, 2.386e-03, 2.245e-03, 2.140e-03, 2.049e-03, 2.018e-03, 1.977e-03, 1.516e-03, 1.296e-03, 1.286e-03, 1.318e-03, 1.239e-03, 1.330e-03, 1.278e-03, 1.149e-03, 1.192e-03, 8.689e-04, 7.022e-04, 7.122e-04, 7.296e-04, 7.022e-04, 4.566e-04, 1.262e-03, 5.815e-04, 4.140e-04, 3.110e-04, 1.732e-04, 2.863e-04, 5.197e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8",{1.986e-01, 4.375e+00, 5.060e+00, 2.591e+00, 1.895e+00, 1.654e+00, 1.359e+00, 1.438e+00, 8.861e-01, 2.134e+00, 2.192e+00, 2.063e+00, 1.736e+00, 1.535e+00, 1.441e+00, 1.420e+00, 1.425e+00, 1.430e+00, 1.422e+00, 1.405e+00, 1.393e+00, 1.389e+00, 1.392e+00, 1.391e+00, 1.394e+00, 1.383e+00, 1.360e+00, 1.332e+00, 1.311e+00, 1.257e+00, 1.203e+00, 1.127e+00, 1.043e+00, 9.544e-01, 8.780e-01, 8.169e-01, 7.720e-01, 7.469e-01, 7.172e-01, 7.032e-01, 7.456e-01, 8.258e-01, 9.443e-01, 1.087e+00, 1.250e+00, 1.397e+00, 1.483e+00, 1.436e+00, 1.326e+00, 1.127e+00, 9.090e-01, 6.912e-01, 5.013e-01, 3.505e-01, 2.376e-01, 1.548e-01, 9.950e-02, 6.260e-02, 4.080e-02, 2.692e-02, 1.843e-02, 1.297e-02, 9.502e-03, 7.208e-03, 5.828e-03, 4.103e-03, 3.041e-03, 2.666e-03, 2.390e-03, 2.226e-03, 2.114e-03, 2.063e-03, 1.996e-03, 1.985e-03, 1.530e-03, 1.306e-03, 1.297e-03, 1.208e-03, 1.239e-03, 1.261e-03, 1.164e-03, 1.260e-03, 1.099e-03, 7.831e-04, 7.705e-04, 9.502e-04, 4.755e-04, 6.359e-04, 3.325e-04, 6.968e-04, 5.016e-04, 3.809e-04, 6.437e-04, 1.195e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8",{1.987e-01, 3.922e+00, 4.598e+00, 2.554e+00, 1.823e+00, 1.668e+00, 1.352e+00, 1.445e+00, 8.901e-01, 2.212e+00, 2.157e+00, 2.058e+00, 1.733e+00, 1.536e+00, 1.433e+00, 1.423e+00, 1.433e+00, 1.440e+00, 1.424e+00, 1.404e+00, 1.397e+00, 1.389e+00, 1.393e+00, 1.394e+00, 1.392e+00, 1.384e+00, 1.357e+00, 1.328e+00, 1.308e+00, 1.259e+00, 1.203e+00, 1.126e+00, 1.042e+00, 9.533e-01, 8.766e-01, 8.162e-01, 7.737e-01, 7.465e-01, 7.170e-01, 7.055e-01, 7.443e-01, 8.287e-01, 9.437e-01, 1.089e+00, 1.249e+00, 1.389e+00, 1.484e+00, 1.434e+00, 1.326e+00, 1.123e+00, 9.064e-01, 6.894e-01, 5.019e-01, 3.517e-01, 2.378e-01, 1.551e-01, 9.978e-02, 6.294e-02, 4.066e-02, 2.680e-02, 1.833e-02, 1.295e-02, 9.515e-03, 7.253e-03, 5.793e-03, 4.122e-03, 3.027e-03, 2.681e-03, 2.420e-03, 2.222e-03, 2.121e-03, 2.049e-03, 1.953e-03, 1.991e-03, 1.584e-03, 1.278e-03, 1.288e-03, 1.207e-03, 1.267e-03, 1.181e-03, 1.156e-03, 1.198e-03, 1.326e-03, 8.619e-04, 6.537e-04, 7.858e-04, 6.330e-04, 4.821e-04, 4.776e-04, 4.402e-04, 4.345e-04, 2.166e-04, 1.952e-04, 1.359e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8",{1.790e-01, 3.978e+00, 4.040e+00, 2.514e+00, 1.832e+00, 1.607e+00, 1.352e+00, 1.403e+00, 8.819e-01, 2.153e+00, 2.194e+00, 2.047e+00, 1.743e+00, 1.534e+00, 1.435e+00, 1.424e+00, 1.433e+00, 1.432e+00, 1.425e+00, 1.409e+00, 1.393e+00, 1.391e+00, 1.392e+00, 1.393e+00, 1.395e+00, 1.385e+00, 1.361e+00, 1.328e+00, 1.308e+00, 1.255e+00, 1.202e+00, 1.125e+00, 1.040e+00, 9.554e-01, 8.775e-01, 8.183e-01, 7.740e-01, 7.468e-01, 7.166e-01, 7.038e-01, 7.472e-01, 8.257e-01, 9.436e-01, 1.090e+00, 1.246e+00, 1.397e+00, 1.481e+00, 1.429e+00, 1.321e+00, 1.124e+00, 9.056e-01, 6.905e-01, 4.991e-01, 3.498e-01, 2.376e-01, 1.552e-01, 9.979e-02, 6.298e-02, 4.089e-02, 2.684e-02, 1.836e-02, 1.300e-02, 9.542e-03, 7.253e-03, 5.813e-03, 4.117e-03, 3.043e-03, 2.657e-03, 2.420e-03, 2.238e-03, 2.120e-03, 2.040e-03, 2.018e-03, 2.023e-03, 1.573e-03, 1.238e-03, 1.319e-03, 1.238e-03, 1.196e-03, 1.268e-03, 1.271e-03, 1.137e-03, 1.243e-03, 7.474e-04, 7.681e-04, 7.238e-04, 6.241e-04, 6.028e-04, 3.869e-04, 4.954e-04, 3.170e-04, 4.062e-04, 3.051e-04, 0.000e+00, 1.404e-04, 1.530e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WW_TuneCP5_13TeV-pythia8",{1.827e-01, 4.155e+00, 4.348e+00, 2.276e+00, 1.956e+00, 1.670e+00, 1.297e+00, 1.302e+00, 9.124e-01, 2.178e+00, 2.194e+00, 2.067e+00, 1.753e+00, 1.531e+00, 1.434e+00, 1.426e+00, 1.436e+00, 1.439e+00, 1.418e+00, 1.411e+00, 1.392e+00, 1.391e+00, 1.393e+00, 1.395e+00, 1.392e+00, 1.379e+00, 1.362e+00, 1.326e+00, 1.306e+00, 1.259e+00, 1.199e+00, 1.124e+00, 1.044e+00, 9.542e-01, 8.789e-01, 8.155e-01, 7.731e-01, 7.479e-01, 7.177e-01, 7.049e-01, 7.457e-01, 8.246e-01, 9.442e-01, 1.085e+00, 1.245e+00, 1.392e+00, 1.488e+00, 1.435e+00, 1.327e+00, 1.125e+00, 9.117e-01, 6.896e-01, 4.983e-01, 3.486e-01, 2.384e-01, 1.556e-01, 9.993e-02, 6.303e-02, 4.062e-02, 2.692e-02, 1.838e-02, 1.294e-02, 9.562e-03, 7.224e-03, 5.827e-03, 4.125e-03, 3.048e-03, 2.660e-03, 2.442e-03, 2.255e-03, 2.067e-03, 2.073e-03, 1.911e-03, 1.998e-03, 1.643e-03, 1.305e-03, 1.251e-03, 1.230e-03, 1.211e-03, 1.189e-03, 1.151e-03, 1.065e-03, 9.408e-04, 8.209e-04, 8.546e-04, 1.037e-03, 4.915e-04, 6.168e-04, 1.089e-03, 4.752e-04, 3.648e-04, 6.234e-04, 8.779e-05, 6.521e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WZ_TuneCP5_13TeV-pythia8",{3.018e-04, 1.043e-02, 4.845e-02, 6.513e-02, 1.071e-01, 2.019e-01, 2.017e-01, 2.501e-01, 1.584e-01, 6.145e-01, 6.177e-01, 8.993e-01, 9.275e-01, 9.992e-01, 9.877e-01, 1.018e+00, 1.126e+00, 1.289e+00, 1.331e+00, 1.355e+00, 1.423e+00, 1.425e+00, 1.440e+00, 1.457e+00, 1.480e+00, 1.471e+00, 1.434e+00, 1.434e+00, 1.429e+00, 1.381e+00, 1.283e+00, 1.213e+00, 1.131e+00, 1.047e+00, 9.739e-01, 9.086e-01, 8.499e-01, 8.138e-01, 7.742e-01, 7.845e-01, 8.022e-01, 8.859e-01, 1.029e+00, 1.216e+00, 1.389e+00, 1.519e+00, 1.625e+00, 1.584e+00, 1.436e+00, 1.245e+00, 9.776e-01, 7.491e-01, 5.429e-01, 3.611e-01, 2.505e-01, 1.608e-01, 1.079e-01, 6.801e-02, 4.409e-02, 2.918e-02, 1.887e-02, 1.343e-02, 9.357e-03, 6.979e-03, 5.942e-03, 4.430e-03, 2.926e-03, 2.752e-03, 1.944e-03, 2.239e-03, 1.256e-03, 1.275e-03, 1.081e-03, 2.170e-03, 8.758e-04, 2.946e-04, 1.980e-04, 1.251e-03, 6.351e-05, 4.519e-05, 8.788e-05, 1.750e-05, 2.166e-05, 4.529e-06, 6.827e-04, 5.040e-06, 3.539e-06, 5.339e-06, 3.386e-07, 1.611e-06, 3.558e-07, 2.628e-05, 5.922e-05, 4.948e-05, 1.817e-05, 7.404e-08, 2.665e-06, 8.511e-06, 1.599e-08, 1.641e-08, 0.000e+0}},
{"ZZ_TuneCP5_13TeV-pythia8",{2.127e-01, 5.059e+00, 4.513e+00, 2.352e+00, 2.437e+00, 1.670e+00, 1.279e+00, 1.393e+00, 9.226e-01, 2.276e+00, 2.247e+00, 2.097e+00, 1.739e+00, 1.526e+00, 1.422e+00, 1.405e+00, 1.435e+00, 1.454e+00, 1.415e+00, 1.413e+00, 1.392e+00, 1.385e+00, 1.389e+00, 1.400e+00, 1.391e+00, 1.373e+00, 1.358e+00, 1.336e+00, 1.303e+00, 1.270e+00, 1.203e+00, 1.128e+00, 1.038e+00, 9.504e-01, 8.825e-01, 8.167e-01, 7.721e-01, 7.485e-01, 7.175e-01, 7.018e-01, 7.459e-01, 8.262e-01, 9.482e-01, 1.091e+00, 1.241e+00, 1.400e+00, 1.508e+00, 1.428e+00, 1.328e+00, 1.116e+00, 8.987e-01, 6.891e-01, 5.094e-01, 3.489e-01, 2.395e-01, 1.538e-01, 9.893e-02, 6.262e-02, 4.037e-02, 2.695e-02, 1.850e-02, 1.297e-02, 9.579e-03, 7.301e-03, 5.711e-03, 4.039e-03, 3.006e-03, 2.658e-03, 2.428e-03, 2.173e-03, 2.089e-03, 2.024e-03, 2.011e-03, 1.975e-03, 1.610e-03, 1.360e-03, 1.289e-03, 1.393e-03, 1.391e-03, 1.501e-03, 1.427e-03, 1.122e-03, 6.719e-04, 6.922e-04, 3.974e-04, 9.641e-04, 1.158e-03, 2.294e-04, 4.049e-04, 4.714e-04, 1.357e-04, 1.546e-04, 8.709e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8",{1.886e-01, 3.827e+00, 4.337e+00, 2.583e+00, 1.930e+00, 1.804e+00, 1.269e+00, 1.406e+00, 8.503e-01, 2.245e+00, 2.172e+00, 2.044e+00, 1.751e+00, 1.525e+00, 1.445e+00, 1.421e+00, 1.429e+00, 1.433e+00, 1.424e+00, 1.403e+00, 1.397e+00, 1.389e+00, 1.399e+00, 1.392e+00, 1.391e+00, 1.377e+00, 1.362e+00, 1.331e+00, 1.308e+00, 1.255e+00, 1.199e+00, 1.124e+00, 1.044e+00, 9.561e-01, 8.761e-01, 8.178e-01, 7.750e-01, 7.474e-01, 7.159e-01, 7.058e-01, 7.446e-01, 8.256e-01, 9.417e-01, 1.092e+00, 1.257e+00, 1.390e+00, 1.490e+00, 1.430e+00, 1.329e+00, 1.128e+00, 9.002e-01, 6.841e-01, 5.006e-01, 3.504e-01, 2.381e-01, 1.541e-01, 9.996e-02, 6.314e-02, 4.088e-02, 2.686e-02, 1.844e-02, 1.297e-02, 9.528e-03, 7.247e-03, 5.801e-03, 4.132e-03, 3.039e-03, 2.626e-03, 2.457e-03, 2.261e-03, 2.088e-03, 2.053e-03, 2.039e-03, 1.890e-03, 1.582e-03, 1.374e-03, 1.240e-03, 1.224e-03, 1.273e-03, 1.110e-03, 1.121e-03, 1.138e-03, 1.262e-03, 7.802e-04, 7.372e-04, 1.204e-03, 6.712e-04, 3.724e-04, 4.694e-04, 9.564e-04, 1.836e-04, 0.000e+00, 1.767e-04, 6.562e-05, 0.000e+00, 5.906e-05, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8",{1.898e-01, 5.389e+00, 4.348e+00, 2.560e+00, 1.775e+00, 1.627e+00, 1.294e+00, 1.396e+00, 8.921e-01, 2.170e+00, 2.176e+00, 2.068e+00, 1.751e+00, 1.543e+00, 1.442e+00, 1.417e+00, 1.437e+00, 1.432e+00, 1.420e+00, 1.412e+00, 1.395e+00, 1.386e+00, 1.396e+00, 1.391e+00, 1.389e+00, 1.380e+00, 1.359e+00, 1.330e+00, 1.308e+00, 1.256e+00, 1.203e+00, 1.124e+00, 1.043e+00, 9.569e-01, 8.754e-01, 8.168e-01, 7.720e-01, 7.478e-01, 7.174e-01, 7.047e-01, 7.455e-01, 8.268e-01, 9.489e-01, 1.091e+00, 1.248e+00, 1.392e+00, 1.485e+00, 1.443e+00, 1.316e+00, 1.124e+00, 9.119e-01, 6.876e-01, 5.016e-01, 3.486e-01, 2.376e-01, 1.544e-01, 9.974e-02, 6.310e-02, 4.072e-02, 2.692e-02, 1.843e-02, 1.296e-02, 9.461e-03, 7.294e-03, 5.771e-03, 4.147e-03, 3.024e-03, 2.640e-03, 2.364e-03, 2.239e-03, 2.116e-03, 2.027e-03, 2.080e-03, 2.091e-03, 1.566e-03, 1.270e-03, 1.331e-03, 1.276e-03, 1.236e-03, 1.454e-03, 1.372e-03, 1.387e-03, 9.233e-04, 7.969e-04, 6.806e-04, 6.275e-04, 7.246e-04, 5.600e-04, 5.490e-04, 2.130e-04, 3.680e-04, 6.289e-04, 8.856e-05, 1.973e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}}
};

    std::unordered_map<std::string, std::vector<float>> pileupweightsUp = { // 69.2 + 4.6%
{"DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8",{5.039e-04, 1.494e-01, 5.339e-02, 1.056e-01, 6.698e-02, 6.264e-02, 5.444e-02, 1.444e-01, 8.380e-02, 1.927e-01, 3.448e-01, 5.859e-01, 4.878e-01, 4.942e-01, 4.739e-01, 4.986e-01, 5.874e-01, 6.995e-01, 8.566e-01, 8.998e-01, 1.033e+00, 1.097e+00, 1.162e+00, 1.202e+00, 1.241e+00, 1.259e+00, 1.083e+00, 1.291e+00, 1.341e+00, 1.352e+00, 1.326e+00, 1.297e+00, 1.230e+00, 1.166e+00, 1.137e+00, 1.093e+00, 1.051e+00, 1.027e+00, 9.228e-01, 9.289e-01, 8.380e-01, 9.384e-01, 9.171e-01, 1.028e+00, 1.125e+00, 1.247e+00, 1.356e+00, 1.511e+00, 1.643e+00, 1.671e+00, 1.591e+00, 1.566e+00, 1.428e+00, 1.277e+00, 1.086e+00, 7.924e-01, 6.757e-01, 5.091e-01, 3.928e-01, 2.590e-01, 2.290e-01, 1.752e-01, 1.403e-01, 1.036e-01, 9.661e-02, 7.223e-02, 5.024e-02, 4.459e-02, 4.100e-02, 3.921e-02, 3.575e-02, 2.740e-02, 4.088e-03, 3.190e-02, 1.739e-03, 2.333e-02, 2.054e-02, 1.954e-02, 9.435e-04, 4.563e-04, 3.984e-02, 6.548e-03, 3.225e-02, 1.091e-02, 5.885e-02, 1.974e-02, 0.000e+00, 1.747e-02, 8.341e-05, 0.000e+00, 4.898e-03, 0.000e+00, 0.000e+00, 1.285e-03, 0.000e+00, 0.000e+00, 3.131e-04, 1.923e-04, 0.000e+00, 2.138e-06, 0.000e+0}},
{"DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8",{1.713e-01, 3.545e+00, 2.846e+00, 2.380e+00, 1.336e+00, 1.378e+00, 1.251e+00, 1.148e+00, 5.048e-01, 9.470e-01, 1.048e+00, 1.028e+00, 1.005e+00, 9.025e-01, 8.265e-01, 7.959e-01, 8.164e-01, 8.660e-01, 9.318e-01, 9.855e-01, 1.031e+00, 1.083e+00, 1.131e+00, 1.155e+00, 1.167e+00, 1.168e+00, 1.173e+00, 1.180e+00, 1.210e+00, 1.211e+00, 1.211e+00, 1.180e+00, 1.139e+00, 1.091e+00, 1.037e+00, 9.949e-01, 9.570e-01, 9.275e-01, 8.771e-01, 8.328e-01, 8.285e-01, 8.401e-01, 8.685e-01, 9.214e-01, 9.967e-01, 1.111e+00, 1.249e+00, 1.347e+00, 1.448e+00, 1.490e+00, 1.491e+00, 1.431e+00, 1.315e+00, 1.167e+00, 9.974e-01, 8.041e-01, 6.288e-01, 4.757e-01, 3.622e-01, 2.742e-01, 2.116e-01, 1.642e-01, 1.314e-01, 1.076e-01, 8.905e-02, 6.510e-02, 4.791e-02, 4.161e-02, 3.756e-02, 3.452e-02, 3.138e-02, 3.044e-02, 2.952e-02, 2.937e-02, 2.383e-02, 1.984e-02, 1.993e-02, 2.181e-02, 2.121e-02, 2.560e-02, 2.614e-02, 2.514e-02, 3.242e-02, 2.330e-02, 2.219e-02, 3.260e-02, 1.986e-02, 3.366e-02, 2.852e-02, 3.267e-02, 8.494e-02, 2.740e-02, 7.017e-03, 2.228e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8",{2.422e-01, 3.014e+00, 3.977e+00, 4.078e+00, 1.349e+00, 1.323e+00, 1.095e+00, 1.140e+00, 5.757e-01, 9.821e-01, 9.954e-01, 1.035e+00, 9.831e-01, 8.844e-01, 8.331e-01, 8.155e-01, 8.296e-01, 8.611e-01, 9.186e-01, 9.746e-01, 1.029e+00, 1.071e+00, 1.120e+00, 1.160e+00, 1.175e+00, 1.176e+00, 1.172e+00, 1.200e+00, 1.209e+00, 1.198e+00, 1.231e+00, 1.163e+00, 1.153e+00, 1.099e+00, 1.044e+00, 1.005e+00, 9.751e-01, 9.229e-01, 8.765e-01, 8.121e-01, 8.221e-01, 8.438e-01, 8.623e-01, 9.205e-01, 1.016e+00, 1.105e+00, 1.258e+00, 1.347e+00, 1.424e+00, 1.495e+00, 1.462e+00, 1.405e+00, 1.332e+00, 1.174e+00, 9.972e-01, 8.138e-01, 6.145e-01, 4.709e-01, 3.664e-01, 2.725e-01, 2.115e-01, 1.639e-01, 1.306e-01, 1.080e-01, 8.739e-02, 6.307e-02, 4.881e-02, 4.247e-02, 3.788e-02, 3.420e-02, 3.282e-02, 3.276e-02, 2.989e-02, 2.927e-02, 2.232e-02, 1.830e-02, 1.559e-02, 1.733e-02, 1.624e-02, 2.418e-02, 2.592e-02, 2.059e-02, 2.797e-02, 1.420e-02, 1.276e-02, 0.000e+00, 1.713e-02, 1.136e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8",{1.866e-01, 4.325e+00, 2.965e+00, 2.599e+00, 1.322e+00, 1.339e+00, 1.222e+00, 1.135e+00, 4.911e-01, 9.451e-01, 1.050e+00, 1.029e+00, 1.015e+00, 9.035e-01, 8.252e-01, 7.978e-01, 8.163e-01, 8.662e-01, 9.333e-01, 9.841e-01, 1.032e+00, 1.084e+00, 1.126e+00, 1.155e+00, 1.163e+00, 1.165e+00, 1.172e+00, 1.179e+00, 1.211e+00, 1.214e+00, 1.210e+00, 1.179e+00, 1.143e+00, 1.090e+00, 1.037e+00, 9.964e-01, 9.572e-01, 9.294e-01, 8.787e-01, 8.353e-01, 8.300e-01, 8.395e-01, 8.679e-01, 9.199e-01, 1.003e+00, 1.119e+00, 1.251e+00, 1.331e+00, 1.447e+00, 1.491e+00, 1.488e+00, 1.423e+00, 1.314e+00, 1.163e+00, 9.932e-01, 8.020e-01, 6.294e-01, 4.798e-01, 3.612e-01, 2.765e-01, 2.107e-01, 1.649e-01, 1.315e-01, 1.063e-01, 8.934e-02, 6.489e-02, 4.832e-02, 4.175e-02, 3.726e-02, 3.452e-02, 3.161e-02, 2.996e-02, 3.005e-02, 2.953e-02, 2.313e-02, 1.926e-02, 2.070e-02, 2.114e-02, 2.226e-02, 2.196e-02, 2.371e-02, 2.526e-02, 2.875e-02, 2.526e-02, 1.981e-02, 2.100e-02, 3.103e-02, 2.401e-02, 2.373e-02, 2.071e-02, 1.616e-02, 1.303e-02, 1.112e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8",{1.972e-01, 3.210e+00, 2.712e+00, 2.808e+00, 1.512e+00, 1.318e+00, 1.219e+00, 1.177e+00, 4.858e-01, 9.347e-01, 1.074e+00, 1.032e+00, 1.013e+00, 9.009e-01, 8.281e-01, 7.922e-01, 8.116e-01, 8.663e-01, 9.334e-01, 9.899e-01, 1.037e+00, 1.087e+00, 1.131e+00, 1.150e+00, 1.164e+00, 1.165e+00, 1.173e+00, 1.179e+00, 1.206e+00, 1.210e+00, 1.211e+00, 1.178e+00, 1.140e+00, 1.093e+00, 1.039e+00, 9.948e-01, 9.559e-01, 9.283e-01, 8.790e-01, 8.341e-01, 8.279e-01, 8.408e-01, 8.703e-01, 9.206e-01, 1.003e+00, 1.115e+00, 1.251e+00, 1.346e+00, 1.445e+00, 1.481e+00, 1.487e+00, 1.429e+00, 1.315e+00, 1.162e+00, 9.954e-01, 8.026e-01, 6.291e-01, 4.770e-01, 3.608e-01, 2.751e-01, 2.118e-01, 1.650e-01, 1.308e-01, 1.068e-01, 8.947e-02, 6.508e-02, 4.828e-02, 4.171e-02, 3.735e-02, 3.450e-02, 3.164e-02, 3.064e-02, 2.826e-02, 2.905e-02, 2.275e-02, 2.025e-02, 1.984e-02, 2.147e-02, 2.426e-02, 2.133e-02, 2.486e-02, 3.111e-02, 3.029e-02, 2.158e-02, 1.764e-02, 2.418e-02, 2.183e-02, 2.051e-02, 3.244e-02, 2.123e-02, 6.900e-02, 4.452e-02, 2.850e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8",{1.865e-01, 5.354e+00, 3.499e+00, 2.545e+00, 1.518e+00, 1.312e+00, 1.347e+00, 1.352e+00, 5.027e-01, 9.633e-01, 1.081e+00, 1.030e+00, 9.848e-01, 9.086e-01, 8.266e-01, 7.914e-01, 8.031e-01, 8.712e-01, 9.336e-01, 9.830e-01, 1.035e+00, 1.082e+00, 1.130e+00, 1.159e+00, 1.168e+00, 1.165e+00, 1.173e+00, 1.172e+00, 1.212e+00, 1.216e+00, 1.206e+00, 1.177e+00, 1.141e+00, 1.093e+00, 1.038e+00, 9.959e-01, 9.608e-01, 9.240e-01, 8.785e-01, 8.332e-01, 8.232e-01, 8.469e-01, 8.697e-01, 9.207e-01, 1.003e+00, 1.112e+00, 1.251e+00, 1.336e+00, 1.446e+00, 1.483e+00, 1.504e+00, 1.431e+00, 1.310e+00, 1.173e+00, 9.843e-01, 7.992e-01, 6.291e-01, 4.813e-01, 3.605e-01, 2.756e-01, 2.117e-01, 1.648e-01, 1.327e-01, 1.061e-01, 8.969e-02, 6.459e-02, 4.793e-02, 4.264e-02, 3.758e-02, 3.353e-02, 3.142e-02, 3.009e-02, 2.977e-02, 2.974e-02, 2.164e-02, 1.871e-02, 2.153e-02, 2.087e-02, 2.174e-02, 2.007e-02, 2.494e-02, 2.265e-02, 3.076e-02, 2.302e-02, 1.282e-02, 1.797e-02, 4.397e-02, 2.916e-02, 2.883e-02, 3.774e-02, 2.453e-02, 5.275e-03, 5.066e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8",{1.895e-01, 3.466e+00, 2.617e+00, 2.595e+00, 1.384e+00, 1.317e+00, 1.266e+00, 1.175e+00, 4.957e-01, 9.695e-01, 1.061e+00, 1.032e+00, 1.010e+00, 8.984e-01, 8.290e-01, 7.935e-01, 8.126e-01, 8.684e-01, 9.323e-01, 9.843e-01, 1.033e+00, 1.085e+00, 1.128e+00, 1.157e+00, 1.163e+00, 1.161e+00, 1.174e+00, 1.183e+00, 1.209e+00, 1.213e+00, 1.209e+00, 1.177e+00, 1.142e+00, 1.090e+00, 1.038e+00, 9.938e-01, 9.574e-01, 9.288e-01, 8.794e-01, 8.341e-01, 8.284e-01, 8.403e-01, 8.692e-01, 9.220e-01, 1.002e+00, 1.114e+00, 1.252e+00, 1.352e+00, 1.446e+00, 1.494e+00, 1.489e+00, 1.431e+00, 1.314e+00, 1.164e+00, 9.972e-01, 8.030e-01, 6.306e-01, 4.751e-01, 3.616e-01, 2.748e-01, 2.109e-01, 1.643e-01, 1.311e-01, 1.066e-01, 8.892e-02, 6.473e-02, 4.833e-02, 4.190e-02, 3.718e-02, 3.376e-02, 3.174e-02, 2.975e-02, 2.881e-02, 2.870e-02, 2.330e-02, 1.997e-02, 2.021e-02, 2.005e-02, 2.337e-02, 2.183e-02, 2.453e-02, 2.581e-02, 2.657e-02, 2.064e-02, 2.078e-02, 1.987e-02, 2.557e-02, 2.158e-02, 2.608e-02, 2.276e-02, 1.664e-02, 4.295e-02, 1.100e-02, 3.493e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8",{1.694e-01, 3.601e+00, 2.833e+00, 2.691e+00, 1.426e+00, 1.306e+00, 1.212e+00, 1.141e+00, 4.830e-01, 9.215e-01, 1.067e+00, 1.037e+00, 1.005e+00, 9.000e-01, 8.288e-01, 7.948e-01, 8.136e-01, 8.674e-01, 9.318e-01, 9.872e-01, 1.034e+00, 1.087e+00, 1.124e+00, 1.155e+00, 1.167e+00, 1.168e+00, 1.173e+00, 1.183e+00, 1.213e+00, 1.211e+00, 1.209e+00, 1.180e+00, 1.142e+00, 1.087e+00, 1.040e+00, 9.928e-01, 9.585e-01, 9.269e-01, 8.769e-01, 8.338e-01, 8.304e-01, 8.389e-01, 8.680e-01, 9.187e-01, 1.002e+00, 1.113e+00, 1.246e+00, 1.345e+00, 1.444e+00, 1.494e+00, 1.490e+00, 1.426e+00, 1.319e+00, 1.163e+00, 9.951e-01, 8.053e-01, 6.260e-01, 4.760e-01, 3.607e-01, 2.757e-01, 2.111e-01, 1.646e-01, 1.319e-01, 1.068e-01, 8.906e-02, 6.495e-02, 4.843e-02, 4.205e-02, 3.741e-02, 3.436e-02, 3.108e-02, 3.059e-02, 2.915e-02, 2.854e-02, 2.288e-02, 1.939e-02, 2.083e-02, 2.287e-02, 2.353e-02, 2.429e-02, 2.501e-02, 2.834e-02, 2.735e-02, 1.790e-02, 2.553e-02, 2.455e-02, 1.820e-02, 2.962e-02, 2.386e-02, 1.757e-02, 2.284e-02, 1.965e-02, 3.774e-02, 2.397e-02, 7.550e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8",{1.620e-01, 3.454e+00, 2.960e+00, 2.561e+00, 1.299e+00, 1.322e+00, 1.252e+00, 1.134e+00, 4.865e-01, 9.423e-01, 1.067e+00, 1.034e+00, 1.016e+00, 9.080e-01, 8.318e-01, 7.951e-01, 8.135e-01, 8.676e-01, 9.358e-01, 9.792e-01, 1.028e+00, 1.083e+00, 1.128e+00, 1.156e+00, 1.163e+00, 1.167e+00, 1.172e+00, 1.182e+00, 1.214e+00, 1.212e+00, 1.205e+00, 1.173e+00, 1.140e+00, 1.089e+00, 1.038e+00, 9.985e-01, 9.545e-01, 9.299e-01, 8.784e-01, 8.347e-01, 8.324e-01, 8.403e-01, 8.690e-01, 9.242e-01, 1.002e+00, 1.112e+00, 1.253e+00, 1.360e+00, 1.452e+00, 1.483e+00, 1.497e+00, 1.427e+00, 1.310e+00, 1.172e+00, 9.902e-01, 7.997e-01, 6.263e-01, 4.786e-01, 3.613e-01, 2.738e-01, 2.106e-01, 1.652e-01, 1.318e-01, 1.070e-01, 8.981e-02, 6.424e-02, 4.827e-02, 4.207e-02, 3.816e-02, 3.348e-02, 3.173e-02, 3.120e-02, 2.851e-02, 2.900e-02, 2.217e-02, 1.888e-02, 2.088e-02, 2.070e-02, 2.560e-02, 2.157e-02, 2.310e-02, 2.526e-02, 2.343e-02, 2.114e-02, 1.588e-02, 2.330e-02, 3.553e-02, 5.498e-02, 1.359e-02, 1.779e-02, 1.542e-02, 2.984e-02, 9.552e-03, 4.044e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8",{1.753e-01, 3.453e+00, 3.026e+00, 2.563e+00, 1.406e+00, 1.374e+00, 1.227e+00, 1.143e+00, 4.973e-01, 9.426e-01, 1.062e+00, 1.033e+00, 1.013e+00, 9.025e-01, 8.279e-01, 7.973e-01, 8.126e-01, 8.686e-01, 9.337e-01, 9.855e-01, 1.034e+00, 1.085e+00, 1.129e+00, 1.155e+00, 1.165e+00, 1.167e+00, 1.171e+00, 1.181e+00, 1.209e+00, 1.213e+00, 1.210e+00, 1.180e+00, 1.140e+00, 1.089e+00, 1.037e+00, 9.940e-01, 9.560e-01, 9.282e-01, 8.806e-01, 8.329e-01, 8.281e-01, 8.397e-01, 8.691e-01, 9.211e-01, 9.999e-01, 1.113e+00, 1.250e+00, 1.345e+00, 1.444e+00, 1.488e+00, 1.494e+00, 1.427e+00, 1.320e+00, 1.167e+00, 9.951e-01, 7.993e-01, 6.302e-01, 4.764e-01, 3.614e-01, 2.744e-01, 2.115e-01, 1.646e-01, 1.313e-01, 1.070e-01, 8.906e-02, 6.474e-02, 4.829e-02, 4.170e-02, 3.739e-02, 3.390e-02, 3.145e-02, 3.008e-02, 2.932e-02, 2.900e-02, 2.360e-02, 1.983e-02, 2.042e-02, 2.092e-02, 2.246e-02, 2.501e-02, 2.442e-02, 2.412e-02, 2.851e-02, 2.232e-02, 1.903e-02, 2.158e-02, 2.149e-02, 2.685e-02, 2.907e-02, 2.756e-02, 3.247e-02, 1.972e-02, 1.262e-02, 4.543e-02, 8.585e-02, 8.938e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8",{1.798e-01, 3.491e+00, 2.979e+00, 2.543e+00, 1.361e+00, 1.325e+00, 1.251e+00, 1.170e+00, 4.972e-01, 9.413e-01, 1.068e+00, 1.030e+00, 1.006e+00, 9.020e-01, 8.245e-01, 7.976e-01, 8.126e-01, 8.677e-01, 9.334e-01, 9.843e-01, 1.034e+00, 1.086e+00, 1.130e+00, 1.154e+00, 1.165e+00, 1.166e+00, 1.173e+00, 1.181e+00, 1.211e+00, 1.212e+00, 1.207e+00, 1.179e+00, 1.141e+00, 1.088e+00, 1.037e+00, 9.944e-01, 9.572e-01, 9.279e-01, 8.795e-01, 8.341e-01, 8.280e-01, 8.390e-01, 8.702e-01, 9.218e-01, 9.992e-01, 1.114e+00, 1.251e+00, 1.344e+00, 1.446e+00, 1.488e+00, 1.491e+00, 1.426e+00, 1.320e+00, 1.167e+00, 9.943e-01, 8.025e-01, 6.306e-01, 4.768e-01, 3.609e-01, 2.749e-01, 2.116e-01, 1.651e-01, 1.313e-01, 1.071e-01, 8.901e-02, 6.498e-02, 4.822e-02, 4.169e-02, 3.730e-02, 3.392e-02, 3.143e-02, 3.039e-02, 2.927e-02, 2.902e-02, 2.280e-02, 1.982e-02, 2.050e-02, 2.139e-02, 2.203e-02, 2.322e-02, 2.548e-02, 2.700e-02, 2.660e-02, 2.216e-02, 1.968e-02, 2.090e-02, 2.016e-02, 2.716e-02, 2.349e-02, 2.381e-02, 1.548e-02, 1.935e-02, 1.166e-02, 1.573e-02, 7.929e-02, 2.476e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8",{1.776e-01, 3.305e+00, 2.808e+00, 2.579e+00, 1.384e+00, 1.343e+00, 1.277e+00, 1.176e+00, 4.973e-01, 9.395e-01, 1.075e+00, 1.035e+00, 1.011e+00, 9.015e-01, 8.271e-01, 7.941e-01, 8.110e-01, 8.684e-01, 9.360e-01, 9.846e-01, 1.034e+00, 1.083e+00, 1.128e+00, 1.155e+00, 1.168e+00, 1.168e+00, 1.173e+00, 1.181e+00, 1.211e+00, 1.212e+00, 1.208e+00, 1.179e+00, 1.138e+00, 1.089e+00, 1.038e+00, 9.938e-01, 9.578e-01, 9.277e-01, 8.782e-01, 8.331e-01, 8.284e-01, 8.388e-01, 8.702e-01, 9.208e-01, 1.003e+00, 1.115e+00, 1.247e+00, 1.346e+00, 1.450e+00, 1.487e+00, 1.492e+00, 1.429e+00, 1.317e+00, 1.165e+00, 9.944e-01, 8.028e-01, 6.308e-01, 4.762e-01, 3.610e-01, 2.740e-01, 2.112e-01, 1.649e-01, 1.312e-01, 1.071e-01, 8.903e-02, 6.484e-02, 4.816e-02, 4.199e-02, 3.730e-02, 3.385e-02, 3.180e-02, 3.024e-02, 2.925e-02, 2.910e-02, 2.339e-02, 1.963e-02, 2.053e-02, 2.139e-02, 2.246e-02, 2.429e-02, 2.533e-02, 2.642e-02, 2.663e-02, 2.347e-02, 1.889e-02, 2.214e-02, 2.045e-02, 2.404e-02, 2.011e-02, 2.208e-02, 2.022e-02, 2.392e-02, 1.671e-02, 1.297e-02, 3.676e-02, 2.297e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8",{1.821e-01, 3.294e+00, 2.633e+00, 2.467e+00, 1.412e+00, 1.323e+00, 1.259e+00, 1.134e+00, 5.005e-01, 9.435e-01, 1.068e+00, 1.035e+00, 1.007e+00, 9.015e-01, 8.280e-01, 7.965e-01, 8.102e-01, 8.695e-01, 9.340e-01, 9.863e-01, 1.033e+00, 1.088e+00, 1.127e+00, 1.154e+00, 1.163e+00, 1.167e+00, 1.174e+00, 1.181e+00, 1.210e+00, 1.211e+00, 1.207e+00, 1.179e+00, 1.141e+00, 1.089e+00, 1.039e+00, 9.938e-01, 9.575e-01, 9.307e-01, 8.787e-01, 8.325e-01, 8.278e-01, 8.398e-01, 8.713e-01, 9.200e-01, 1.003e+00, 1.112e+00, 1.252e+00, 1.346e+00, 1.447e+00, 1.488e+00, 1.495e+00, 1.430e+00, 1.317e+00, 1.164e+00, 9.930e-01, 8.024e-01, 6.286e-01, 4.775e-01, 3.609e-01, 2.739e-01, 2.115e-01, 1.652e-01, 1.312e-01, 1.070e-01, 8.883e-02, 6.489e-02, 4.804e-02, 4.161e-02, 3.753e-02, 3.395e-02, 3.181e-02, 3.032e-02, 2.950e-02, 2.836e-02, 2.296e-02, 1.943e-02, 2.036e-02, 2.136e-02, 2.234e-02, 2.398e-02, 2.471e-02, 2.546e-02, 3.010e-02, 2.316e-02, 1.918e-02, 2.132e-02, 1.878e-02, 2.358e-02, 2.637e-02, 2.035e-02, 1.481e-02, 1.838e-02, 1.020e-02, 8.095e-03, 2.040e-02, 1.274e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_s-channel_antitop_leptonDecays_13TeV-PSweights_powheg-pythia",{1.747e-01, 5.116e+00, 2.250e+00, 2.432e+00, 1.371e+00, 1.276e+00, 1.291e+00, 1.125e+00, 4.938e-01, 9.376e-01, 1.125e+00, 1.026e+00, 1.018e+00, 9.031e-01, 8.293e-01, 7.971e-01, 8.202e-01, 8.686e-01, 9.318e-01, 9.833e-01, 1.038e+00, 1.080e+00, 1.124e+00, 1.151e+00, 1.169e+00, 1.168e+00, 1.173e+00, 1.182e+00, 1.207e+00, 1.209e+00, 1.209e+00, 1.178e+00, 1.145e+00, 1.090e+00, 1.039e+00, 9.915e-01, 9.552e-01, 9.298e-01, 8.755e-01, 8.336e-01, 8.276e-01, 8.410e-01, 8.703e-01, 9.237e-01, 1.002e+00, 1.114e+00, 1.250e+00, 1.359e+00, 1.437e+00, 1.486e+00, 1.496e+00, 1.434e+00, 1.307e+00, 1.160e+00, 9.914e-01, 8.021e-01, 6.335e-01, 4.767e-01, 3.619e-01, 2.744e-01, 2.113e-01, 1.672e-01, 1.315e-01, 1.068e-01, 8.856e-02, 6.445e-02, 4.765e-02, 4.082e-02, 3.759e-02, 3.374e-02, 3.126e-02, 3.125e-02, 2.947e-02, 2.861e-02, 2.238e-02, 2.114e-02, 2.043e-02, 2.274e-02, 2.493e-02, 2.104e-02, 2.965e-02, 2.217e-02, 4.115e-02, 1.990e-02, 3.129e-02, 1.889e-02, 2.521e-02, 2.090e-02, 2.754e-02, 9.015e-03, 2.344e-02, 7.561e-03, 9.681e-03, 6.149e-03, 0.000e+00, 2.420e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_s-channel_top_leptonDecays_13TeV-PSweights_powheg-pythia",{1.692e-01, 3.305e+00, 2.908e+00, 2.416e+00, 1.376e+00, 1.380e+00, 1.277e+00, 1.153e+00, 4.885e-01, 9.458e-01, 1.069e+00, 1.023e+00, 1.001e+00, 8.954e-01, 8.278e-01, 7.969e-01, 8.144e-01, 8.628e-01, 9.383e-01, 9.874e-01, 1.031e+00, 1.084e+00, 1.129e+00, 1.157e+00, 1.165e+00, 1.163e+00, 1.173e+00, 1.184e+00, 1.206e+00, 1.212e+00, 1.208e+00, 1.180e+00, 1.142e+00, 1.096e+00, 1.039e+00, 9.952e-01, 9.573e-01, 9.305e-01, 8.773e-01, 8.353e-01, 8.265e-01, 8.427e-01, 8.691e-01, 9.161e-01, 9.991e-01, 1.116e+00, 1.254e+00, 1.339e+00, 1.439e+00, 1.489e+00, 1.498e+00, 1.431e+00, 1.307e+00, 1.175e+00, 9.960e-01, 7.987e-01, 6.254e-01, 4.765e-01, 3.605e-01, 2.725e-01, 2.112e-01, 1.643e-01, 1.306e-01, 1.080e-01, 8.918e-02, 6.487e-02, 4.847e-02, 4.210e-02, 3.763e-02, 3.371e-02, 3.232e-02, 3.054e-02, 3.004e-02, 2.928e-02, 2.277e-02, 1.991e-02, 2.188e-02, 2.073e-02, 2.005e-02, 2.262e-02, 2.783e-02, 2.757e-02, 3.204e-02, 2.871e-02, 2.268e-02, 2.101e-02, 1.840e-02, 2.789e-02, 2.144e-02, 1.685e-02, 5.475e-02, 1.766e-02, 2.261e-02, 7.181e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.793e-01, 3.342e+00, 2.887e+00, 2.568e+00, 1.376e+00, 1.354e+00, 1.263e+00, 1.162e+00, 4.927e-01, 9.461e-01, 1.067e+00, 1.029e+00, 1.012e+00, 9.031e-01, 8.271e-01, 7.946e-01, 8.098e-01, 8.675e-01, 9.350e-01, 9.860e-01, 1.034e+00, 1.085e+00, 1.129e+00, 1.156e+00, 1.165e+00, 1.166e+00, 1.171e+00, 1.182e+00, 1.213e+00, 1.213e+00, 1.208e+00, 1.179e+00, 1.140e+00, 1.089e+00, 1.038e+00, 9.950e-01, 9.567e-01, 9.276e-01, 8.781e-01, 8.332e-01, 8.285e-01, 8.384e-01, 8.694e-01, 9.200e-01, 1.002e+00, 1.113e+00, 1.249e+00, 1.347e+00, 1.446e+00, 1.490e+00, 1.492e+00, 1.433e+00, 1.315e+00, 1.163e+00, 9.939e-01, 8.023e-01, 6.297e-01, 4.768e-01, 3.608e-01, 2.742e-01, 2.111e-01, 1.648e-01, 1.311e-01, 1.073e-01, 8.913e-02, 6.499e-02, 4.818e-02, 4.192e-02, 3.745e-02, 3.388e-02, 3.160e-02, 3.030e-02, 2.917e-02, 2.937e-02, 2.298e-02, 1.985e-02, 2.030e-02, 2.160e-02, 2.204e-02, 2.333e-02, 2.541e-02, 2.632e-02, 2.744e-02, 2.071e-02, 1.863e-02, 2.357e-02, 2.214e-02, 2.415e-02, 2.372e-02, 2.262e-02, 1.715e-02, 1.953e-02, 1.328e-02, 1.500e-02, 8.504e-02, 7.589e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.768e-01, 3.374e+00, 2.759e+00, 2.536e+00, 1.414e+00, 1.336e+00, 1.241e+00, 1.150e+00, 4.988e-01, 9.453e-01, 1.069e+00, 1.033e+00, 1.012e+00, 9.035e-01, 8.272e-01, 7.957e-01, 8.121e-01, 8.678e-01, 9.337e-01, 9.853e-01, 1.035e+00, 1.084e+00, 1.129e+00, 1.155e+00, 1.165e+00, 1.167e+00, 1.172e+00, 1.182e+00, 1.210e+00, 1.212e+00, 1.207e+00, 1.179e+00, 1.140e+00, 1.089e+00, 1.038e+00, 9.942e-01, 9.570e-01, 9.282e-01, 8.796e-01, 8.334e-01, 8.283e-01, 8.387e-01, 8.698e-01, 9.188e-01, 1.000e+00, 1.113e+00, 1.250e+00, 1.347e+00, 1.447e+00, 1.488e+00, 1.491e+00, 1.427e+00, 1.316e+00, 1.167e+00, 9.943e-01, 8.031e-01, 6.303e-01, 4.766e-01, 3.613e-01, 2.744e-01, 2.112e-01, 1.649e-01, 1.313e-01, 1.072e-01, 8.932e-02, 6.502e-02, 4.817e-02, 4.188e-02, 3.722e-02, 3.385e-02, 3.153e-02, 3.030e-02, 2.903e-02, 2.889e-02, 2.333e-02, 1.960e-02, 2.057e-02, 2.116e-02, 2.239e-02, 2.391e-02, 2.496e-02, 2.720e-02, 2.937e-02, 2.127e-02, 2.045e-02, 2.322e-02, 2.103e-02, 2.411e-02, 2.244e-02, 2.724e-02, 1.708e-02, 1.963e-02, 1.149e-02, 1.344e-02, 5.363e-02, 1.436e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.863e-01, 3.330e+00, 2.696e+00, 2.415e+00, 1.451e+00, 1.388e+00, 1.284e+00, 1.138e+00, 4.841e-01, 9.371e-01, 1.072e+00, 1.033e+00, 1.005e+00, 9.067e-01, 8.271e-01, 7.960e-01, 8.104e-01, 8.670e-01, 9.379e-01, 9.847e-01, 1.035e+00, 1.085e+00, 1.124e+00, 1.155e+00, 1.167e+00, 1.166e+00, 1.172e+00, 1.183e+00, 1.207e+00, 1.215e+00, 1.210e+00, 1.176e+00, 1.141e+00, 1.090e+00, 1.037e+00, 9.956e-01, 9.558e-01, 9.287e-01, 8.795e-01, 8.329e-01, 8.316e-01, 8.399e-01, 8.692e-01, 9.222e-01, 9.963e-01, 1.117e+00, 1.245e+00, 1.348e+00, 1.442e+00, 1.486e+00, 1.481e+00, 1.433e+00, 1.311e+00, 1.164e+00, 9.976e-01, 8.064e-01, 6.285e-01, 4.764e-01, 3.595e-01, 2.744e-01, 2.117e-01, 1.654e-01, 1.318e-01, 1.077e-01, 8.857e-02, 6.503e-02, 4.831e-02, 4.194e-02, 3.723e-02, 3.371e-02, 3.148e-02, 2.951e-02, 2.909e-02, 2.997e-02, 2.322e-02, 2.036e-02, 2.035e-02, 2.213e-02, 2.127e-02, 2.380e-02, 2.593e-02, 2.784e-02, 2.922e-02, 2.653e-02, 2.037e-02, 2.049e-02, 1.930e-02, 3.627e-02, 2.390e-02, 1.565e-02, 1.525e-02, 3.937e-02, 8.401e-03, 1.601e-02, 0.000e+00, 3.150e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.652e-01, 3.483e+00, 3.324e+00, 2.827e+00, 1.434e+00, 1.333e+00, 1.201e+00, 1.109e+00, 4.909e-01, 9.427e-01, 1.037e+00, 1.026e+00, 1.011e+00, 9.062e-01, 8.225e-01, 7.959e-01, 8.123e-01, 8.647e-01, 9.383e-01, 9.896e-01, 1.036e+00, 1.080e+00, 1.132e+00, 1.154e+00, 1.165e+00, 1.170e+00, 1.173e+00, 1.181e+00, 1.209e+00, 1.209e+00, 1.207e+00, 1.177e+00, 1.135e+00, 1.088e+00, 1.037e+00, 9.930e-01, 9.579e-01, 9.280e-01, 8.824e-01, 8.339e-01, 8.281e-01, 8.412e-01, 8.657e-01, 9.209e-01, 1.005e+00, 1.113e+00, 1.252e+00, 1.338e+00, 1.439e+00, 1.491e+00, 1.497e+00, 1.431e+00, 1.315e+00, 1.165e+00, 9.948e-01, 8.060e-01, 6.306e-01, 4.759e-01, 3.622e-01, 2.736e-01, 2.121e-01, 1.645e-01, 1.311e-01, 1.077e-01, 8.939e-02, 6.524e-02, 4.833e-02, 4.253e-02, 3.738e-02, 3.412e-02, 3.128e-02, 3.005e-02, 2.897e-02, 2.906e-02, 2.363e-02, 1.980e-02, 2.153e-02, 2.073e-02, 2.306e-02, 2.272e-02, 2.680e-02, 2.528e-02, 2.198e-02, 2.106e-02, 2.786e-02, 2.803e-02, 2.404e-02, 2.790e-02, 1.839e-02, 1.926e-02, 1.043e-02, 4.038e-02, 6.464e-03, 1.642e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTHH_TuneCP5_13TeV-madgraph-pythia8",{1.158e-04, 4.492e-01, 3.292e-01, 2.894e-01, 1.862e-01, 1.396e-01, 1.424e-01, 1.230e-01, 5.621e-02, 2.493e-01, 3.678e-01, 3.726e-01, 5.482e-01, 2.789e-01, 5.765e-01, 5.542e-01, 5.897e-01, 7.312e-01, 6.958e-01, 9.945e-01, 1.056e+00, 1.147e+00, 1.246e+00, 1.310e+00, 1.315e+00, 1.256e+00, 1.310e+00, 1.310e+00, 1.349e+00, 1.343e+00, 1.333e+00, 1.299e+00, 1.295e+00, 1.210e+00, 1.194e+00, 1.128e+00, 1.100e+00, 1.037e+00, 9.806e-01, 9.231e-01, 9.647e-01, 9.507e-01, 9.773e-01, 1.011e+00, 1.129e+00, 1.240e+00, 1.416e+00, 1.547e+00, 1.623e+00, 1.710e+00, 1.617e+00, 1.552e+00, 1.457e+00, 1.342e+00, 1.150e+00, 9.249e-01, 7.102e-01, 5.499e-01, 4.030e-01, 2.997e-01, 2.415e-01, 1.897e-01, 1.199e-01, 1.151e-01, 9.375e-02, 7.781e-02, 5.264e-02, 4.514e-02, 4.185e-02, 3.924e-02, 3.261e-02, 3.410e-02, 3.739e-02, 3.140e-02, 2.789e-02, 1.932e-02, 2.460e-02, 1.894e-02, 4.841e-02, 6.606e-02, 2.253e-02, 2.046e-02, 4.169e-02, 9.406e-03, 0.000e+00, 1.276e-02, 8.511e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 5.060e-05, 0.000e+00, 0.000e+00, 1.629e-06, 0.000e+0}},
{"TTTJ_TuneCP5_13TeV-madgraph-pythia8",{1.331e-01, 0.000e+00, 3.935e+00, 2.594e+00, 2.781e+00, 1.555e+00, 1.418e+00, 9.959e-01, 5.086e-01, 9.380e-01, 1.062e+00, 9.876e-01, 9.237e-01, 8.936e-01, 8.450e-01, 7.904e-01, 8.260e-01, 8.837e-01, 9.439e-01, 1.007e+00, 1.036e+00, 1.074e+00, 1.124e+00, 1.162e+00, 1.144e+00, 1.158e+00, 1.162e+00, 1.174e+00, 1.213e+00, 1.217e+00, 1.210e+00, 1.181e+00, 1.139e+00, 1.078e+00, 1.027e+00, 9.883e-01, 9.493e-01, 9.408e-01, 8.973e-01, 8.390e-01, 8.453e-01, 8.416e-01, 8.868e-01, 9.026e-01, 1.031e+00, 1.076e+00, 1.248e+00, 1.360e+00, 1.440e+00, 1.463e+00, 1.513e+00, 1.450e+00, 1.311e+00, 1.133e+00, 9.673e-01, 8.053e-01, 6.101e-01, 4.908e-01, 3.565e-01, 2.739e-01, 2.207e-01, 1.659e-01, 1.344e-01, 1.024e-01, 9.019e-02, 6.383e-02, 5.126e-02, 4.134e-02, 3.813e-02, 3.079e-02, 3.085e-02, 3.070e-02, 3.208e-02, 3.528e-02, 2.037e-02, 1.811e-02, 1.983e-02, 2.177e-02, 1.753e-02, 1.645e-02, 2.244e-02, 0.000e+00, 4.152e-02, 9.367e-03, 0.000e+00, 0.000e+00, 8.476e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTTT_TuneCP5_13TeV-amcatnlo-pythia8",{1.456e-01, 1.942e+00, 2.391e+00, 2.299e+00, 1.584e+00, 8.128e-01, 7.605e-01, 7.503e-01, 7.512e-01, 8.695e-01, 9.203e-01, 1.133e+00, 9.687e-01, 8.623e-01, 8.210e-01, 7.956e-01, 8.005e-01, 8.931e-01, 9.754e-01, 9.708e-01, 1.062e+00, 1.040e+00, 1.105e+00, 1.136e+00, 1.180e+00, 1.131e+00, 1.179e+00, 1.190e+00, 1.185e+00, 1.233e+00, 1.173e+00, 1.174e+00, 1.124e+00, 1.104e+00, 1.053e+00, 1.017e+00, 9.897e-01, 9.427e-01, 8.577e-01, 8.273e-01, 8.081e-01, 8.327e-01, 8.781e-01, 9.168e-01, 1.007e+00, 1.175e+00, 1.274e+00, 1.351e+00, 1.526e+00, 1.513e+00, 1.476e+00, 1.430e+00, 1.317e+00, 1.220e+00, 9.433e-01, 7.954e-01, 6.596e-01, 4.754e-01, 3.756e-01, 2.801e-01, 2.010e-01, 1.602e-01, 1.295e-01, 1.117e-01, 8.730e-02, 6.405e-02, 4.631e-02, 3.840e-02, 3.637e-02, 3.351e-02, 3.131e-02, 2.845e-02, 2.409e-02, 2.212e-02, 2.063e-02, 2.751e-02, 1.808e-02, 2.324e-02, 3.084e-02, 9.995e-02, 2.098e-02, 1.327e-02, 1.802e-02, 2.135e-02, 1.151e-02, 0.000e+00, 6.439e-03, -4.270e-03, 0.000e+00, 0.000e+00, 0.000e+00, -3.090e-03, 0.000e+00, -6.282e-04, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8",{2.230e-01, 6.383e+00, 1.872e+00, 2.101e+00, 1.211e+00, 1.054e+00, 1.371e+00, 1.007e+00, 5.404e-01, 9.969e-01, 1.085e+00, 1.013e+00, 1.021e+00, 8.771e-01, 8.050e-01, 8.020e-01, 8.090e-01, 8.828e-01, 9.325e-01, 9.885e-01, 1.025e+00, 1.075e+00, 1.134e+00, 1.172e+00, 1.144e+00, 1.186e+00, 1.163e+00, 1.177e+00, 1.210e+00, 1.216e+00, 1.196e+00, 1.165e+00, 1.140e+00, 1.092e+00, 1.033e+00, 9.909e-01, 9.614e-01, 9.343e-01, 8.828e-01, 8.303e-01, 8.156e-01, 8.584e-01, 8.743e-01, 9.163e-01, 1.011e+00, 1.124e+00, 1.252e+00, 1.378e+00, 1.443e+00, 1.493e+00, 1.483e+00, 1.419e+00, 1.300e+00, 1.191e+00, 9.903e-01, 7.838e-01, 6.238e-01, 4.906e-01, 3.637e-01, 2.769e-01, 2.126e-01, 1.676e-01, 1.313e-01, 1.068e-01, 8.913e-02, 6.407e-02, 4.677e-02, 3.894e-02, 3.594e-02, 3.433e-02, 3.408e-02, 3.044e-02, 2.927e-02, 2.859e-02, 2.599e-02, 1.982e-02, 1.838e-02, 2.243e-02, 3.440e-02, 2.253e-02, 2.561e-02, 2.379e-02, 2.222e-02, 2.005e-02, 1.351e-02, 2.719e-02, 0.000e+00, -2.407e-02, 7.930e-03, 0.000e+00, 6.748e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTTW_TuneCP5_13TeV-madgraph-pythia8",{1.764e-03, 4.090e-01, 4.656e-01, 2.725e-01, 2.022e-01, 1.750e-01, 1.752e-01, 1.633e-01, 7.414e-02, 1.282e-01, 4.065e-01, 4.248e-01, 5.183e-01, 7.738e-01, 8.040e-01, 7.703e-01, 7.935e-01, 7.356e-01, 8.513e-01, 9.095e-01, 9.632e-01, 1.029e+00, 1.116e+00, 1.167e+00, 1.172e+00, 1.201e+00, 1.214e+00, 1.185e+00, 1.247e+00, 1.278e+00, 1.244e+00, 1.236e+00, 1.140e+00, 1.138e+00, 1.111e+00, 1.068e+00, 9.546e-01, 9.977e-01, 9.396e-01, 9.036e-01, 8.989e-01, 9.037e-01, 9.230e-01, 1.018e+00, 1.053e+00, 1.207e+00, 1.348e+00, 1.506e+00, 1.593e+00, 1.612e+00, 1.557e+00, 1.530e+00, 1.137e+00, 1.241e+00, 1.092e+00, 8.721e-01, 6.657e-01, 3.895e-01, 3.889e-01, 2.960e-01, 2.210e-01, 1.783e-01, 1.423e-01, 1.125e-01, 9.127e-02, 7.130e-02, 5.112e-02, 4.586e-02, 3.729e-02, 3.777e-02, 3.448e-02, 3.058e-02, 3.957e-02, 2.306e-02, 2.195e-02, 2.294e-02, 2.204e-02, 2.372e-02, 1.385e-02, 1.188e-04, 3.009e-02, 6.147e-02, 4.176e-02, 9.422e-03, 1.905e-02, 1.278e-02, 2.131e-03, 9.583e-06, 3.726e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 1.014e-04, 0.000e+00, 0.000e+00, 4.568e-06, 0.000e+0}},
{"TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.732e-01, 3.382e+00, 2.800e+00, 2.572e+00, 1.412e+00, 1.370e+00, 1.250e+00, 1.138e+00, 4.943e-01, 9.468e-01, 1.058e+00, 1.037e+00, 1.010e+00, 9.067e-01, 8.265e-01, 7.962e-01, 8.128e-01, 8.662e-01, 9.331e-01, 9.862e-01, 1.034e+00, 1.085e+00, 1.129e+00, 1.154e+00, 1.163e+00, 1.167e+00, 1.173e+00, 1.182e+00, 1.210e+00, 1.211e+00, 1.208e+00, 1.180e+00, 1.140e+00, 1.090e+00, 1.037e+00, 9.944e-01, 9.566e-01, 9.294e-01, 8.790e-01, 8.327e-01, 8.300e-01, 8.386e-01, 8.692e-01, 9.203e-01, 1.001e+00, 1.115e+00, 1.252e+00, 1.346e+00, 1.449e+00, 1.487e+00, 1.492e+00, 1.431e+00, 1.313e+00, 1.166e+00, 9.950e-01, 8.037e-01, 6.292e-01, 4.769e-01, 3.609e-01, 2.740e-01, 2.114e-01, 1.645e-01, 1.313e-01, 1.073e-01, 8.885e-02, 6.479e-02, 4.809e-02, 4.190e-02, 3.751e-02, 3.403e-02, 3.162e-02, 3.050e-02, 2.852e-02, 2.884e-02, 2.286e-02, 1.974e-02, 2.052e-02, 2.072e-02, 2.179e-02, 2.309e-02, 2.443e-02, 2.746e-02, 2.608e-02, 2.111e-02, 1.880e-02, 2.162e-02, 1.992e-02, 2.312e-02, 2.246e-02, 2.095e-02, 2.017e-02, 2.067e-02, 1.500e-02, 1.587e-02, 4.500e-02, 1.874e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTTo2L2Nu_TuneCP5_erdON_13TeV-powheg-pythia8",{1.782e-01, 3.161e+00, 3.281e+00, 2.431e+00, 1.439e+00, 1.276e+00, 1.201e+00, 1.195e+00, 5.119e-01, 9.408e-01, 1.091e+00, 1.044e+00, 1.019e+00, 9.030e-01, 8.304e-01, 7.928e-01, 8.143e-01, 8.705e-01, 9.275e-01, 9.909e-01, 1.038e+00, 1.086e+00, 1.128e+00, 1.159e+00, 1.166e+00, 1.169e+00, 1.175e+00, 1.181e+00, 1.203e+00, 1.211e+00, 1.209e+00, 1.180e+00, 1.140e+00, 1.090e+00, 1.037e+00, 9.928e-01, 9.563e-01, 9.297e-01, 8.782e-01, 8.339e-01, 8.292e-01, 8.386e-01, 8.710e-01, 9.191e-01, 9.980e-01, 1.115e+00, 1.243e+00, 1.344e+00, 1.441e+00, 1.484e+00, 1.489e+00, 1.429e+00, 1.314e+00, 1.161e+00, 9.954e-01, 8.051e-01, 6.319e-01, 4.772e-01, 3.617e-01, 2.742e-01, 2.110e-01, 1.648e-01, 1.313e-01, 1.072e-01, 8.903e-02, 6.478e-02, 4.829e-02, 4.152e-02, 3.723e-02, 3.392e-02, 3.162e-02, 2.919e-02, 3.010e-02, 2.857e-02, 2.365e-02, 1.965e-02, 2.144e-02, 2.045e-02, 2.292e-02, 2.132e-02, 2.718e-02, 2.591e-02, 2.933e-02, 2.465e-02, 2.834e-02, 2.938e-02, 3.593e-02, 2.860e-02, 9.423e-02, 8.812e-03, 0.000e+00, 2.587e-02, 0.000e+00, 5.259e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8",{2.746e-04, 3.503e-02, 2.786e-02, 6.621e-02, 5.882e-02, 9.843e-02, 1.123e-01, 1.334e-01, 7.149e-02, 2.119e-01, 3.321e-01, 4.250e-01, 5.031e-01, 5.518e-01, 5.319e-01, 5.875e-01, 6.642e-01, 7.419e-01, 8.681e-01, 9.427e-01, 1.015e+00, 1.089e+00, 1.154e+00, 1.217e+00, 1.230e+00, 1.249e+00, 1.240e+00, 1.250e+00, 1.312e+00, 1.310e+00, 1.318e+00, 1.265e+00, 1.236e+00, 1.190e+00, 1.135e+00, 1.083e+00, 1.050e+00, 1.017e+00, 9.657e-01, 9.100e-01, 9.148e-01, 9.103e-01, 9.484e-01, 9.897e-01, 1.098e+00, 1.219e+00, 1.382e+00, 1.476e+00, 1.587e+00, 1.616e+00, 1.535e+00, 1.482e+00, 1.417e+00, 1.196e+00, 1.049e+00, 8.213e-01, 6.770e-01, 5.086e-01, 3.869e-01, 2.948e-01, 2.253e-01, 1.757e-01, 1.423e-01, 1.153e-01, 8.042e-02, 6.972e-02, 4.634e-02, 4.476e-02, 4.085e-02, 3.625e-02, 3.424e-02, 2.195e-02, 2.365e-02, 1.375e-02, 8.516e-03, 1.547e-02, 2.082e-02, 1.990e-02, 3.315e-03, 1.167e-03, 1.140e-03, 3.155e-02, 2.839e-02, 1.788e-02, 2.895e-03, 6.748e-04, 2.108e-02, 2.670e-04, 2.794e-05, 3.129e-04, 3.080e-04, 3.451e-05, 2.199e-04, 1.067e-04, 4.565e-06, 1.724e-06, 9.190e-05, 1.693e-04, 1.144e-04, 3.982e-06, 0.000e+0}},
{"TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8",{2.212e-04, 1.808e-02, 4.747e-02, 4.429e-02, 5.624e-02, 6.472e-02, 8.385e-02, 1.272e-01, 9.275e-02, 1.772e-01, 3.454e-01, 4.522e-01, 4.654e-01, 5.710e-01, 5.752e-01, 6.353e-01, 7.115e-01, 7.985e-01, 8.879e-01, 9.646e-01, 1.025e+00, 1.099e+00, 1.173e+00, 1.198e+00, 1.231e+00, 1.237e+00, 1.275e+00, 1.294e+00, 1.312e+00, 1.338e+00, 1.331e+00, 1.272e+00, 1.250e+00, 1.172e+00, 1.150e+00, 1.096e+00, 1.055e+00, 1.019e+00, 9.401e-01, 9.254e-01, 9.017e-01, 9.018e-01, 9.283e-01, 1.010e+00, 1.117e+00, 1.208e+00, 1.347e+00, 1.434e+00, 1.579e+00, 1.643e+00, 1.575e+00, 1.541e+00, 1.388e+00, 1.217e+00, 1.072e+00, 8.456e-01, 6.582e-01, 5.164e-01, 3.865e-01, 2.877e-01, 2.278e-01, 1.722e-01, 1.424e-01, 1.151e-01, 9.554e-02, 7.014e-02, 4.803e-02, 4.005e-02, 3.995e-02, 3.147e-02, 2.437e-02, 2.399e-02, 1.599e-02, 3.245e-02, 1.206e-02, 2.097e-02, 2.029e-02, 3.851e-03, 3.024e-03, 1.440e-03, 4.681e-04, 3.581e-04, 3.002e-02, 2.271e-02, 2.613e-04, 2.054e-02, 1.109e-02, 5.023e-05, 6.930e-05, 2.166e-05, 9.436e-05, 1.644e-04, 1.185e-04, 5.681e-03, 7.158e-03, 4.610e-05, 1.385e-04, 2.834e-04, 1.293e-04, 3.876e-06, 0.000e+0}},
{"TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8",{2.019e-04, 2.669e-02, 2.454e-02, 3.976e-02, 2.926e-02, 6.129e-02, 1.524e-01, 1.254e-01, 6.201e-02, 1.832e-01, 2.905e-01, 3.878e-01, 5.060e-01, 5.627e-01, 5.758e-01, 6.051e-01, 6.795e-01, 7.917e-01, 8.907e-01, 9.530e-01, 1.039e+00, 1.108e+00, 1.162e+00, 1.238e+00, 1.260e+00, 1.267e+00, 1.256e+00, 1.296e+00, 1.332e+00, 1.341e+00, 1.300e+00, 1.302e+00, 1.261e+00, 1.227e+00, 1.145e+00, 1.101e+00, 1.074e+00, 1.044e+00, 9.793e-01, 9.078e-01, 9.317e-01, 9.433e-01, 9.403e-01, 1.029e+00, 1.099e+00, 1.246e+00, 1.363e+00, 1.464e+00, 1.593e+00, 1.607e+00, 1.513e+00, 1.425e+00, 1.430e+00, 1.235e+00, 1.085e+00, 8.457e-01, 6.750e-01, 5.081e-01, 3.895e-01, 2.850e-01, 2.161e-01, 1.742e-01, 1.409e-01, 1.143e-01, 9.435e-02, 6.589e-02, 4.991e-02, 4.583e-02, 3.974e-02, 3.763e-02, 2.914e-02, 1.484e-02, 1.992e-02, 3.073e-02, 1.312e-02, 2.150e-02, 1.841e-02, 2.378e-03, 2.921e-03, 1.003e-03, 5.930e-04, 6.541e-03, 6.987e-04, 4.742e-04, 1.621e-04, 2.182e-04, 1.710e-02, 3.993e-05, 6.412e-05, 1.060e-02, 1.514e-04, 2.666e-02, 1.579e-05, 1.084e-02, 6.830e-03, 1.192e-05, 2.936e-04, 5.713e-06, 1.646e-04, 3.442e-06, 0.000e+0}},
{"TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8",{3.267e-04, 4.970e-02, 2.612e-02, 5.792e-02, 4.821e-02, 1.077e-01, 1.472e-01, 1.546e-01, 8.595e-02, 3.041e-01, 4.367e-01, 4.849e-01, 5.023e-01, 5.447e-01, 5.393e-01, 6.110e-01, 6.527e-01, 7.398e-01, 8.557e-01, 9.211e-01, 1.011e+00, 1.076e+00, 1.155e+00, 1.210e+00, 1.223e+00, 1.213e+00, 1.233e+00, 1.254e+00, 1.281e+00, 1.298e+00, 1.297e+00, 1.264e+00, 1.231e+00, 1.190e+00, 1.122e+00, 1.091e+00, 1.052e+00, 1.017e+00, 9.491e-01, 9.055e-01, 8.887e-01, 9.125e-01, 9.384e-01, 9.860e-01, 1.070e+00, 1.192e+00, 1.371e+00, 1.402e+00, 1.533e+00, 1.618e+00, 1.543e+00, 1.530e+00, 1.396e+00, 1.237e+00, 1.040e+00, 8.443e-01, 6.770e-01, 5.119e-01, 3.788e-01, 2.939e-01, 2.261e-01, 1.778e-01, 1.416e-01, 1.055e-01, 9.198e-02, 6.894e-02, 4.732e-02, 4.480e-02, 3.991e-02, 3.645e-02, 3.145e-02, 1.862e-02, 3.086e-02, 1.634e-02, 8.517e-03, 1.482e-02, 1.362e-02, 1.518e-02, 1.811e-03, 1.722e-03, 2.183e-03, 1.975e-02, 1.409e-02, 1.695e-02, 1.558e-02, 1.597e-04, 7.051e-05, 5.155e-04, 8.380e-03, 1.317e-02, 0.000e+00, 9.201e-03, 1.767e-02, 6.526e-05, 3.535e-03, 3.359e-06, 1.710e-04, 2.399e-04, 2.555e-04, 2.907e-06, 0.000e+0}},
{"TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.806e-01, 3.165e+00, 2.757e+00, 2.542e+00, 1.387e+00, 1.339e+00, 1.237e+00, 1.164e+00, 4.952e-01, 9.393e-01, 1.058e+00, 1.032e+00, 1.011e+00, 9.039e-01, 8.250e-01, 7.967e-01, 8.115e-01, 8.675e-01, 9.322e-01, 9.849e-01, 1.034e+00, 1.085e+00, 1.129e+00, 1.155e+00, 1.165e+00, 1.167e+00, 1.172e+00, 1.182e+00, 1.210e+00, 1.212e+00, 1.208e+00, 1.178e+00, 1.141e+00, 1.089e+00, 1.037e+00, 9.935e-01, 9.572e-01, 9.299e-01, 8.797e-01, 8.326e-01, 8.294e-01, 8.402e-01, 8.690e-01, 9.194e-01, 1.000e+00, 1.113e+00, 1.248e+00, 1.345e+00, 1.448e+00, 1.488e+00, 1.491e+00, 1.430e+00, 1.317e+00, 1.166e+00, 9.943e-01, 8.027e-01, 6.298e-01, 4.765e-01, 3.607e-01, 2.748e-01, 2.115e-01, 1.653e-01, 1.315e-01, 1.071e-01, 8.913e-02, 6.485e-02, 4.825e-02, 4.198e-02, 3.732e-02, 3.408e-02, 3.150e-02, 3.018e-02, 2.900e-02, 2.900e-02, 2.320e-02, 1.980e-02, 2.041e-02, 2.070e-02, 2.260e-02, 2.313e-02, 2.482e-02, 2.691e-02, 2.780e-02, 2.188e-02, 2.026e-02, 2.251e-02, 2.088e-02, 2.389e-02, 2.316e-02, 2.426e-02, 2.228e-02, 2.543e-02, 1.366e-02, 1.415e-02, 5.646e-02, 2.116e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToHadronic_TuneCP5_erdON_13TeV-powheg-pythia8",{1.781e-01, 3.642e+00, 2.834e+00, 2.643e+00, 1.422e+00, 1.336e+00, 1.268e+00, 1.138e+00, 4.856e-01, 9.428e-01, 1.057e+00, 1.035e+00, 1.001e+00, 8.984e-01, 8.259e-01, 7.963e-01, 8.093e-01, 8.676e-01, 9.337e-01, 9.838e-01, 1.033e+00, 1.084e+00, 1.132e+00, 1.158e+00, 1.166e+00, 1.166e+00, 1.174e+00, 1.184e+00, 1.211e+00, 1.212e+00, 1.209e+00, 1.177e+00, 1.142e+00, 1.089e+00, 1.038e+00, 9.942e-01, 9.567e-01, 9.282e-01, 8.798e-01, 8.321e-01, 8.294e-01, 8.392e-01, 8.698e-01, 9.181e-01, 9.998e-01, 1.115e+00, 1.249e+00, 1.348e+00, 1.446e+00, 1.489e+00, 1.495e+00, 1.424e+00, 1.316e+00, 1.163e+00, 9.964e-01, 8.043e-01, 6.291e-01, 4.756e-01, 3.613e-01, 2.750e-01, 2.112e-01, 1.647e-01, 1.313e-01, 1.066e-01, 8.889e-02, 6.492e-02, 4.832e-02, 4.189e-02, 3.724e-02, 3.395e-02, 3.127e-02, 3.062e-02, 2.843e-02, 2.968e-02, 2.320e-02, 2.009e-02, 2.045e-02, 2.197e-02, 2.179e-02, 2.507e-02, 2.544e-02, 2.534e-02, 2.415e-02, 2.086e-02, 1.611e-02, 2.008e-02, 2.034e-02, 2.221e-02, 2.164e-02, 2.962e-02, 1.324e-02, 2.277e-02, 1.093e-02, 7.937e-03, 1.750e-02, 2.186e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToHadronic_TuneCP5down_PSweights_13TeV-powheg-pythia8",{2.527e-04, 2.420e-02, 3.326e-02, 4.878e-02, 5.910e-02, 8.784e-02, 9.845e-02, 1.168e-01, 8.490e-02, 2.041e-01, 3.457e-01, 4.346e-01, 4.985e-01, 5.237e-01, 5.629e-01, 6.068e-01, 6.882e-01, 7.736e-01, 8.701e-01, 9.508e-01, 1.025e+00, 1.105e+00, 1.168e+00, 1.212e+00, 1.235e+00, 1.237e+00, 1.253e+00, 1.279e+00, 1.296e+00, 1.308e+00, 1.311e+00, 1.282e+00, 1.246e+00, 1.190e+00, 1.135e+00, 1.095e+00, 1.040e+00, 1.016e+00, 9.568e-01, 9.118e-01, 9.038e-01, 9.204e-01, 9.570e-01, 1.001e+00, 1.093e+00, 1.211e+00, 1.356e+00, 1.457e+00, 1.544e+00, 1.602e+00, 1.563e+00, 1.522e+00, 1.411e+00, 1.228e+00, 1.040e+00, 8.423e-01, 6.658e-01, 5.043e-01, 3.786e-01, 2.950e-01, 2.271e-01, 1.702e-01, 1.407e-01, 1.088e-01, 8.847e-02, 6.903e-02, 4.939e-02, 4.261e-02, 3.638e-02, 3.191e-02, 3.046e-02, 2.408e-02, 2.218e-02, 2.830e-02, 1.770e-02, 7.968e-03, 8.793e-03, 5.477e-03, 3.488e-03, 1.532e-03, 1.018e-03, 9.767e-04, 1.011e-03, 1.003e-03, 2.144e-04, 5.227e-04, 2.428e-04, 3.860e-04, 5.962e-05, 2.934e-04, 9.388e-05, 2.373e-03, 1.205e-04, 1.752e-05, 5.562e-05, 4.121e-06, 1.909e-04, 1.399e-05, 8.146e-06, 3.524e-06, 0.000e+0}},
{"TTToHadronic_TuneCP5up_PSweights_13TeV-powheg-pythia8",{2.798e-04, 2.431e-02, 4.344e-02, 6.370e-02, 5.961e-02, 9.892e-02, 1.208e-01, 1.435e-01, 8.612e-02, 2.208e-01, 3.195e-01, 4.150e-01, 5.281e-01, 5.666e-01, 5.764e-01, 6.040e-01, 6.842e-01, 7.610e-01, 8.710e-01, 9.491e-01, 1.020e+00, 1.092e+00, 1.167e+00, 1.203e+00, 1.237e+00, 1.235e+00, 1.242e+00, 1.261e+00, 1.294e+00, 1.315e+00, 1.307e+00, 1.268e+00, 1.231e+00, 1.186e+00, 1.131e+00, 1.087e+00, 1.044e+00, 1.005e+00, 9.593e-01, 9.119e-01, 8.975e-01, 9.155e-01, 9.447e-01, 1.005e+00, 1.084e+00, 1.208e+00, 1.359e+00, 1.435e+00, 1.541e+00, 1.585e+00, 1.539e+00, 1.508e+00, 1.373e+00, 1.212e+00, 1.046e+00, 8.444e-01, 6.593e-01, 4.980e-01, 3.857e-01, 2.894e-01, 2.232e-01, 1.713e-01, 1.393e-01, 1.087e-01, 9.081e-02, 6.737e-02, 4.878e-02, 4.343e-02, 3.576e-02, 3.404e-02, 3.034e-02, 2.420e-02, 2.069e-02, 1.683e-02, 1.884e-02, 8.506e-03, 6.650e-03, 1.195e-02, 4.247e-03, 2.534e-03, 1.878e-03, 1.063e-03, 2.486e-03, 3.286e-04, 6.796e-04, 1.002e-03, 5.686e-04, 2.988e-04, 6.127e-05, 4.017e-05, 4.150e-05, 4.541e-05, 2.092e-04, 1.071e-04, 9.873e-06, 6.575e-06, 1.280e-04, 3.004e-04, 1.677e-06, 3.202e-06, 0.000e+0}},
{"TTToHadronic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8",{2.619e-04, 2.702e-02, 2.898e-02, 5.648e-02, 6.173e-02, 9.688e-02, 1.371e-01, 1.333e-01, 8.471e-02, 2.055e-01, 3.254e-01, 4.463e-01, 5.268e-01, 5.595e-01, 5.567e-01, 5.888e-01, 6.930e-01, 7.661e-01, 8.842e-01, 9.543e-01, 1.030e+00, 1.107e+00, 1.164e+00, 1.201e+00, 1.236e+00, 1.233e+00, 1.255e+00, 1.266e+00, 1.308e+00, 1.319e+00, 1.308e+00, 1.278e+00, 1.235e+00, 1.190e+00, 1.124e+00, 1.085e+00, 1.048e+00, 1.015e+00, 9.569e-01, 9.108e-01, 9.022e-01, 9.082e-01, 9.507e-01, 1.005e+00, 1.084e+00, 1.199e+00, 1.367e+00, 1.469e+00, 1.549e+00, 1.610e+00, 1.589e+00, 1.481e+00, 1.408e+00, 1.237e+00, 1.027e+00, 8.388e-01, 6.624e-01, 5.082e-01, 3.851e-01, 2.922e-01, 2.238e-01, 1.727e-01, 1.387e-01, 1.076e-01, 8.863e-02, 6.746e-02, 4.732e-02, 4.030e-02, 3.832e-02, 3.664e-02, 2.387e-02, 2.656e-02, 2.005e-02, 2.105e-02, 2.046e-02, 1.389e-02, 1.074e-02, 1.042e-02, 3.322e-03, 1.599e-03, 5.222e-04, 9.160e-04, 9.502e-04, 2.171e-04, 7.181e-04, 1.083e-03, 3.516e-04, 7.519e-05, 8.691e-05, 7.330e-05, 9.201e-05, 2.128e-04, 7.107e-03, 5.648e-05, 1.214e-05, 4.069e-06, 1.294e-04, 2.916e-05, 2.517e-06, 2.836e-06, 0.000e+0}},
{"TTToHadronic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8",{2.630e-04, 3.485e-02, 3.612e-02, 5.140e-02, 6.167e-02, 9.522e-02, 1.001e-01, 1.427e-01, 9.068e-02, 1.961e-01, 3.279e-01, 4.213e-01, 5.340e-01, 5.556e-01, 5.650e-01, 6.114e-01, 6.802e-01, 7.694e-01, 8.722e-01, 9.455e-01, 1.015e+00, 1.098e+00, 1.160e+00, 1.205e+00, 1.231e+00, 1.238e+00, 1.248e+00, 1.273e+00, 1.295e+00, 1.312e+00, 1.308e+00, 1.265e+00, 1.228e+00, 1.191e+00, 1.141e+00, 1.094e+00, 1.050e+00, 1.015e+00, 9.645e-01, 9.135e-01, 8.992e-01, 9.083e-01, 9.535e-01, 1.005e+00, 1.098e+00, 1.209e+00, 1.354e+00, 1.456e+00, 1.539e+00, 1.547e+00, 1.574e+00, 1.529e+00, 1.391e+00, 1.234e+00, 1.038e+00, 8.462e-01, 6.683e-01, 5.095e-01, 3.807e-01, 2.952e-01, 2.231e-01, 1.775e-01, 1.411e-01, 1.103e-01, 9.253e-02, 6.706e-02, 4.885e-02, 4.325e-02, 3.869e-02, 3.196e-02, 2.496e-02, 2.257e-02, 1.816e-02, 2.343e-02, 1.643e-02, 7.847e-03, 1.443e-02, 5.671e-03, 3.536e-03, 1.624e-03, 7.058e-04, 9.845e-04, 8.227e-04, 2.780e-04, 3.656e-04, 3.107e-04, 2.653e-04, 1.438e-04, 6.345e-05, 1.824e-04, 7.376e-05, 1.140e-03, 5.993e-03, 2.227e-05, 3.275e-05, 3.333e-06, 1.804e-04, 9.061e-05, 1.375e-05, 2.880e-06, 0.000e+0}},
{"TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.755e-01, 2.988e+00, 2.628e+00, 2.549e+00, 1.542e+00, 1.339e+00, 1.272e+00, 1.141e+00, 4.991e-01, 9.551e-01, 1.071e+00, 1.036e+00, 1.000e+00, 8.989e-01, 8.239e-01, 7.918e-01, 8.111e-01, 8.688e-01, 9.363e-01, 9.858e-01, 1.035e+00, 1.085e+00, 1.127e+00, 1.159e+00, 1.165e+00, 1.169e+00, 1.174e+00, 1.179e+00, 1.213e+00, 1.214e+00, 1.206e+00, 1.179e+00, 1.140e+00, 1.090e+00, 1.033e+00, 9.956e-01, 9.561e-01, 9.297e-01, 8.775e-01, 8.354e-01, 8.312e-01, 8.397e-01, 8.706e-01, 9.196e-01, 1.003e+00, 1.109e+00, 1.251e+00, 1.347e+00, 1.445e+00, 1.489e+00, 1.494e+00, 1.427e+00, 1.311e+00, 1.165e+00, 9.942e-01, 8.007e-01, 6.313e-01, 4.758e-01, 3.601e-01, 2.743e-01, 2.105e-01, 1.646e-01, 1.310e-01, 1.065e-01, 8.977e-02, 6.391e-02, 4.847e-02, 4.219e-02, 3.743e-02, 3.380e-02, 3.195e-02, 2.983e-02, 2.864e-02, 2.966e-02, 2.310e-02, 2.048e-02, 2.098e-02, 2.139e-02, 2.136e-02, 2.544e-02, 2.427e-02, 2.928e-02, 3.327e-02, 2.252e-02, 1.855e-02, 1.750e-02, 3.736e-02, 2.253e-02, 5.444e-02, 1.527e-02, 1.737e-02, 0.000e+00, 3.189e-03, 9.114e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.746e-01, 3.296e+00, 2.853e+00, 2.574e+00, 1.415e+00, 1.347e+00, 1.237e+00, 1.140e+00, 4.936e-01, 9.416e-01, 1.064e+00, 1.032e+00, 1.013e+00, 9.043e-01, 8.262e-01, 7.965e-01, 8.115e-01, 8.675e-01, 9.341e-01, 9.858e-01, 1.034e+00, 1.084e+00, 1.128e+00, 1.155e+00, 1.165e+00, 1.168e+00, 1.172e+00, 1.182e+00, 1.210e+00, 1.212e+00, 1.208e+00, 1.179e+00, 1.141e+00, 1.088e+00, 1.038e+00, 9.934e-01, 9.568e-01, 9.283e-01, 8.787e-01, 8.337e-01, 8.280e-01, 8.396e-01, 8.677e-01, 9.198e-01, 1.002e+00, 1.114e+00, 1.250e+00, 1.347e+00, 1.447e+00, 1.487e+00, 1.490e+00, 1.429e+00, 1.315e+00, 1.165e+00, 9.943e-01, 8.030e-01, 6.307e-01, 4.768e-01, 3.609e-01, 2.749e-01, 2.111e-01, 1.654e-01, 1.313e-01, 1.072e-01, 8.910e-02, 6.473e-02, 4.815e-02, 4.188e-02, 3.750e-02, 3.410e-02, 3.162e-02, 3.010e-02, 2.932e-02, 2.885e-02, 2.302e-02, 1.947e-02, 2.012e-02, 2.037e-02, 2.268e-02, 2.336e-02, 2.491e-02, 2.738e-02, 2.810e-02, 2.222e-02, 1.998e-02, 2.289e-02, 1.966e-02, 2.641e-02, 2.789e-02, 2.666e-02, 2.113e-02, 3.105e-02, 1.154e-02, 1.337e-02, 3.579e-02, 2.981e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTJets_TuneCP5_13TeV-madgraphMLM-pythia8",{1.746e-01, 3.296e+00, 2.853e+00, 2.574e+00, 1.415e+00, 1.347e+00, 1.237e+00, 1.140e+00, 4.936e-01, 9.416e-01, 1.064e+00, 1.032e+00, 1.013e+00, 9.043e-01, 8.262e-01, 7.965e-01, 8.115e-01, 8.675e-01, 9.341e-01, 9.858e-01, 1.034e+00, 1.084e+00, 1.128e+00, 1.155e+00, 1.165e+00, 1.168e+00, 1.172e+00, 1.182e+00, 1.210e+00, 1.212e+00, 1.208e+00, 1.179e+00, 1.141e+00, 1.088e+00, 1.038e+00, 9.934e-01, 9.568e-01, 9.283e-01, 8.787e-01, 8.337e-01, 8.280e-01, 8.396e-01, 8.677e-01, 9.198e-01, 1.002e+00, 1.114e+00, 1.250e+00, 1.347e+00, 1.447e+00, 1.487e+00, 1.490e+00, 1.429e+00, 1.315e+00, 1.165e+00, 9.943e-01, 8.030e-01, 6.307e-01, 4.768e-01, 3.609e-01, 2.749e-01, 2.111e-01, 1.654e-01, 1.313e-01, 1.072e-01, 8.910e-02, 6.473e-02, 4.815e-02, 4.188e-02, 3.750e-02, 3.410e-02, 3.162e-02, 3.010e-02, 2.932e-02, 2.885e-02, 2.302e-02, 1.947e-02, 2.012e-02, 2.037e-02, 2.268e-02, 2.336e-02, 2.491e-02, 2.738e-02, 2.810e-02, 2.222e-02, 1.998e-02, 2.289e-02, 1.966e-02, 2.641e-02, 2.789e-02, 2.666e-02, 2.113e-02, 3.105e-02, 1.154e-02, 1.337e-02, 3.579e-02, 2.981e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToSemiLeptonic_TuneCP5_erdON_13TeV-powheg-pythia8",{1.885e-01, 3.752e+00, 2.922e+00, 2.723e+00, 1.312e+00, 1.281e+00, 1.294e+00, 1.211e+00, 5.120e-01, 9.618e-01, 1.081e+00, 1.030e+00, 1.010e+00, 9.005e-01, 8.337e-01, 7.988e-01, 8.115e-01, 8.689e-01, 9.316e-01, 9.835e-01, 1.030e+00, 1.081e+00, 1.131e+00, 1.158e+00, 1.167e+00, 1.168e+00, 1.174e+00, 1.178e+00, 1.214e+00, 1.212e+00, 1.207e+00, 1.181e+00, 1.142e+00, 1.089e+00, 1.038e+00, 9.942e-01, 9.575e-01, 9.290e-01, 8.764e-01, 8.353e-01, 8.265e-01, 8.380e-01, 8.721e-01, 9.149e-01, 1.003e+00, 1.121e+00, 1.244e+00, 1.346e+00, 1.451e+00, 1.488e+00, 1.486e+00, 1.433e+00, 1.315e+00, 1.168e+00, 9.945e-01, 8.001e-01, 6.310e-01, 4.738e-01, 3.608e-01, 2.732e-01, 2.108e-01, 1.643e-01, 1.322e-01, 1.062e-01, 8.960e-02, 6.429e-02, 4.873e-02, 4.201e-02, 3.722e-02, 3.442e-02, 3.200e-02, 3.005e-02, 2.879e-02, 2.799e-02, 2.463e-02, 1.971e-02, 2.091e-02, 2.061e-02, 2.489e-02, 2.433e-02, 2.541e-02, 2.884e-02, 3.243e-02, 2.357e-02, 1.865e-02, 2.214e-02, 1.920e-02, 6.366e-02, 2.098e-02, 2.746e-02, 1.428e-02, 4.607e-02, 9.831e-03, 9.366e-03, 1.180e-02, 3.686e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToSemiLeptonic_TuneCP5down_PSweights_13TeV-powheg-pythia8",{2.514e-04, 2.920e-02, 3.124e-02, 5.076e-02, 4.984e-02, 8.601e-02, 1.468e-01, 1.259e-01, 8.378e-02, 2.006e-01, 3.211e-01, 4.673e-01, 5.274e-01, 5.657e-01, 5.734e-01, 6.033e-01, 6.736e-01, 7.740e-01, 8.515e-01, 9.511e-01, 1.031e+00, 1.101e+00, 1.164e+00, 1.213e+00, 1.239e+00, 1.244e+00, 1.251e+00, 1.284e+00, 1.308e+00, 1.315e+00, 1.313e+00, 1.275e+00, 1.248e+00, 1.204e+00, 1.140e+00, 1.093e+00, 1.054e+00, 1.017e+00, 9.612e-01, 9.090e-01, 9.079e-01, 9.078e-01, 9.584e-01, 9.955e-01, 1.103e+00, 1.201e+00, 1.373e+00, 1.436e+00, 1.554e+00, 1.625e+00, 1.570e+00, 1.509e+00, 1.371e+00, 1.232e+00, 1.069e+00, 8.298e-01, 6.715e-01, 5.112e-01, 3.853e-01, 2.956e-01, 2.259e-01, 1.699e-01, 1.409e-01, 1.082e-01, 9.043e-02, 6.338e-02, 4.987e-02, 4.355e-02, 3.817e-02, 3.189e-02, 3.486e-02, 2.722e-02, 1.445e-02, 2.422e-02, 1.714e-02, 1.132e-02, 1.040e-02, 1.000e-02, 1.783e-03, 1.147e-03, 6.847e-04, 5.842e-04, 7.553e-04, 2.432e-04, 4.493e-04, 2.032e-04, 3.290e-04, 6.659e-05, 1.419e-04, 1.423e-05, 8.971e-03, 9.095e-03, 8.152e-03, 1.015e-04, 1.077e-05, 2.700e-06, 1.972e-04, 9.958e-06, 7.058e-06, 3.927e-06, 0.000e+0}},
{"TTToSemiLeptonic_TuneCP5up_PSweights_13TeV-powheg-pythia8",{2.952e-04, 4.994e-02, 4.076e-02, 7.295e-02, 6.638e-02, 1.079e-01, 1.485e-01, 1.471e-01, 9.547e-02, 2.309e-01, 3.517e-01, 4.239e-01, 5.339e-01, 5.735e-01, 5.627e-01, 5.865e-01, 6.568e-01, 7.576e-01, 8.639e-01, 9.548e-01, 1.028e+00, 1.103e+00, 1.151e+00, 1.202e+00, 1.223e+00, 1.235e+00, 1.231e+00, 1.271e+00, 1.299e+00, 1.309e+00, 1.305e+00, 1.272e+00, 1.233e+00, 1.183e+00, 1.121e+00, 1.080e+00, 1.036e+00, 1.015e+00, 9.575e-01, 9.127e-01, 8.904e-01, 9.120e-01, 9.476e-01, 1.000e+00, 1.090e+00, 1.206e+00, 1.339e+00, 1.439e+00, 1.521e+00, 1.600e+00, 1.557e+00, 1.484e+00, 1.366e+00, 1.233e+00, 1.047e+00, 8.443e-01, 6.619e-01, 5.066e-01, 3.850e-01, 2.929e-01, 2.239e-01, 1.746e-01, 1.406e-01, 1.101e-01, 8.895e-02, 6.800e-02, 4.662e-02, 4.239e-02, 3.737e-02, 3.393e-02, 3.159e-02, 2.241e-02, 2.107e-02, 1.867e-02, 1.341e-02, 1.344e-02, 7.259e-03, 7.241e-03, 6.202e-03, 1.294e-03, 7.222e-04, 8.709e-04, 5.701e-04, 1.469e-03, 3.889e-04, 2.892e-04, 1.824e-04, 7.269e-05, 6.134e-05, 2.001e-04, 9.263e-05, 4.676e-03, 1.112e-04, 1.462e-05, 1.058e-05, 2.097e-06, 1.485e-04, 1.289e-05, 1.071e-05, 3.542e-06, 0.000e+0}},
{"TTToSemiLeptonic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8",{1.848e-01, 3.093e+00, 2.488e+00, 2.540e+00, 1.453e+00, 1.360e+00, 1.253e+00, 1.150e+00, 4.959e-01, 9.556e-01, 1.064e+00, 1.042e+00, 1.011e+00, 9.040e-01, 8.254e-01, 7.957e-01, 8.119e-01, 8.664e-01, 9.341e-01, 9.859e-01, 1.033e+00, 1.087e+00, 1.130e+00, 1.153e+00, 1.165e+00, 1.166e+00, 1.171e+00, 1.182e+00, 1.211e+00, 1.211e+00, 1.206e+00, 1.180e+00, 1.140e+00, 1.092e+00, 1.038e+00, 9.928e-01, 9.586e-01, 9.286e-01, 8.795e-01, 8.337e-01, 8.298e-01, 8.394e-01, 8.687e-01, 9.189e-01, 1.001e+00, 1.112e+00, 1.250e+00, 1.344e+00, 1.451e+00, 1.492e+00, 1.493e+00, 1.434e+00, 1.319e+00, 1.164e+00, 9.945e-01, 8.033e-01, 6.306e-01, 4.750e-01, 3.607e-01, 2.743e-01, 2.111e-01, 1.648e-01, 1.311e-01, 1.069e-01, 8.875e-02, 6.484e-02, 4.809e-02, 4.200e-02, 3.752e-02, 3.355e-02, 3.179e-02, 3.021e-02, 2.913e-02, 2.958e-02, 2.332e-02, 1.945e-02, 2.060e-02, 2.071e-02, 2.327e-02, 2.499e-02, 2.562e-02, 2.972e-02, 2.650e-02, 2.169e-02, 1.863e-02, 2.082e-02, 2.123e-02, 2.017e-02, 3.513e-02, 3.220e-02, 1.101e-02, 6.751e-02, 7.203e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTToSemiLeptonic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8",{2.894e-04, 2.487e-02, 3.526e-02, 5.244e-02, 5.922e-02, 9.293e-02, 1.362e-01, 1.502e-01, 9.376e-02, 1.872e-01, 3.715e-01, 4.495e-01, 5.216e-01, 5.656e-01, 5.908e-01, 6.237e-01, 6.869e-01, 7.822e-01, 8.762e-01, 9.465e-01, 1.027e+00, 1.105e+00, 1.167e+00, 1.207e+00, 1.218e+00, 1.221e+00, 1.228e+00, 1.263e+00, 1.295e+00, 1.298e+00, 1.302e+00, 1.274e+00, 1.227e+00, 1.187e+00, 1.128e+00, 1.071e+00, 1.039e+00, 1.012e+00, 9.501e-01, 9.068e-01, 8.910e-01, 9.075e-01, 9.441e-01, 9.985e-01, 1.086e+00, 1.203e+00, 1.365e+00, 1.447e+00, 1.542e+00, 1.594e+00, 1.559e+00, 1.505e+00, 1.366e+00, 1.241e+00, 1.027e+00, 8.454e-01, 6.440e-01, 5.087e-01, 3.776e-01, 2.912e-01, 2.247e-01, 1.750e-01, 1.410e-01, 1.086e-01, 8.556e-02, 6.762e-02, 4.988e-02, 4.107e-02, 3.906e-02, 3.059e-02, 2.886e-02, 2.301e-02, 1.767e-02, 2.001e-02, 1.183e-02, 1.229e-02, 8.560e-03, 7.377e-03, 7.040e-03, 3.557e-03, 8.830e-04, 9.039e-04, 1.142e-03, 2.079e-03, 4.193e-04, 8.268e-04, 2.302e-04, 1.036e-04, 6.574e-05, 5.476e-05, 9.343e-03, 1.155e-02, 5.727e-04, 4.648e-05, 2.127e-04, 3.990e-06, 1.857e-04, 4.440e-04, 1.442e-05, 3.432e-06, 0.000e+0}},
{"TTWH_TuneCP5_13TeV-madgraph-pythia8",{2.474e-04, 2.606e-02, 3.429e-02, 2.983e-01, 1.858e-01, 1.619e-01, 1.463e-01, 1.337e-01, 5.907e-02, 1.187e-01, 4.083e-01, 5.271e-01, 5.600e-01, 4.861e-01, 4.612e-01, 2.952e-01, 5.928e-01, 8.235e-01, 9.393e-01, 1.019e+00, 1.048e+00, 1.046e+00, 1.171e+00, 1.201e+00, 1.244e+00, 1.298e+00, 1.321e+00, 1.277e+00, 1.387e+00, 1.380e+00, 1.337e+00, 1.298e+00, 1.277e+00, 1.214e+00, 1.146e+00, 1.119e+00, 1.072e+00, 1.001e+00, 1.001e+00, 9.308e-01, 9.048e-01, 9.188e-01, 1.018e+00, 1.031e+00, 1.154e+00, 1.226e+00, 1.357e+00, 1.465e+00, 1.581e+00, 1.646e+00, 1.540e+00, 1.455e+00, 8.410e-01, 1.250e+00, 1.063e+00, 8.427e-01, 6.911e-01, 5.260e-01, 3.901e-01, 2.945e-01, 2.275e-01, 1.717e-01, 1.490e-01, 1.125e-01, 9.263e-02, 6.713e-02, 5.102e-02, 4.463e-02, 3.908e-02, 1.868e-02, 3.111e-02, 3.232e-02, 1.493e-02, 8.257e-03, 3.167e-02, 1.582e-02, 1.265e-02, 9.778e-03, 2.147e-02, 6.593e-02, 4.497e-02, 6.125e-02, 2.080e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 3.713e-03, 0.000e+00, 0.000e+00, 0.000e+00, 6.525e-04, 0.000e+00, 0.000e+00, 0.000e+00, 5.050e-05, 6.201e-05, 3.774e-05, 2.529e-06, 0.000e+0}},
{"TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8",{1.881e-01, 2.376e+00, 2.415e+00, 2.640e+00, 1.226e+00, 1.317e+00, 1.358e+00, 1.078e+00, 5.085e-01, 9.538e-01, 1.103e+00, 1.015e+00, 1.026e+00, 8.925e-01, 8.281e-01, 8.059e-01, 8.194e-01, 8.652e-01, 9.376e-01, 9.786e-01, 1.035e+00, 1.085e+00, 1.122e+00, 1.147e+00, 1.167e+00, 1.165e+00, 1.185e+00, 1.179e+00, 1.215e+00, 1.223e+00, 1.211e+00, 1.171e+00, 1.142e+00, 1.096e+00, 1.034e+00, 9.883e-01, 9.540e-01, 9.215e-01, 8.750e-01, 8.295e-01, 8.328e-01, 8.361e-01, 8.705e-01, 9.281e-01, 1.003e+00, 1.106e+00, 1.244e+00, 1.345e+00, 1.444e+00, 1.481e+00, 1.495e+00, 1.416e+00, 1.307e+00, 1.155e+00, 9.911e-01, 8.056e-01, 6.329e-01, 4.801e-01, 3.714e-01, 2.746e-01, 2.121e-01, 1.629e-01, 1.334e-01, 1.092e-01, 8.754e-02, 6.440e-02, 4.887e-02, 4.226e-02, 3.747e-02, 3.451e-02, 3.122e-02, 2.829e-02, 2.767e-02, 2.766e-02, 2.444e-02, 2.153e-02, 2.099e-02, 1.870e-02, 2.148e-02, 3.786e-02, 1.999e-02, 3.127e-02, 2.731e-02, 4.852e-02, 3.270e-02, 1.950e-02, 1.673e-02, 3.882e-02, 1.706e-02, 8.374e-03, -2.177e-02, 0.000e+00, 0.000e+00, 2.856e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",{1.159e-01, 3.316e+00, 2.188e+00, 2.125e+00, 1.197e+00, 1.495e+00, 9.600e-01, 1.072e+00, 5.141e-01, 1.029e+00, 1.030e+00, 1.062e+00, 1.082e+00, 9.059e-01, 8.631e-01, 7.931e-01, 8.078e-01, 8.667e-01, 9.568e-01, 9.698e-01, 1.030e+00, 1.093e+00, 1.132e+00, 1.155e+00, 1.182e+00, 1.175e+00, 1.172e+00, 1.185e+00, 1.212e+00, 1.215e+00, 1.194e+00, 1.184e+00, 1.152e+00, 1.088e+00, 1.056e+00, 9.751e-01, 9.499e-01, 9.500e-01, 8.902e-01, 8.158e-01, 8.238e-01, 8.228e-01, 8.676e-01, 8.954e-01, 1.004e+00, 1.121e+00, 1.270e+00, 1.336e+00, 1.460e+00, 1.484e+00, 1.460e+00, 1.415e+00, 1.351e+00, 1.159e+00, 9.735e-01, 7.739e-01, 6.232e-01, 4.685e-01, 3.660e-01, 2.752e-01, 2.183e-01, 1.689e-01, 1.274e-01, 1.049e-01, 9.521e-02, 6.761e-02, 4.838e-02, 4.338e-02, 3.274e-02, 3.153e-02, 2.801e-02, 2.851e-02, 3.011e-02, 3.438e-02, 1.773e-02, 1.802e-02, 2.105e-02, 1.907e-02, 2.042e-02, 1.540e-02, 1.996e-02, 1.942e-02, 2.308e-02, 6.250e-02, 1.404e-02, 1.413e-02, 1.885e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTWW_TuneCP5_13TeV-madgraph-pythia8",{6.812e-04, 4.982e-01, 5.258e-01, 4.918e-01, 2.091e-01, 1.918e-01, 3.597e-01, 3.889e-01, 1.793e-01, 3.782e-01, 4.296e-01, 4.089e-01, 4.367e-01, 4.211e-01, 5.209e-01, 5.745e-01, 6.864e-01, 7.936e-01, 9.198e-01, 9.240e-01, 1.013e+00, 1.075e+00, 1.144e+00, 1.134e+00, 1.258e+00, 1.251e+00, 1.273e+00, 1.317e+00, 1.307e+00, 1.330e+00, 1.219e+00, 1.313e+00, 1.235e+00, 1.206e+00, 1.140e+00, 1.120e+00, 1.037e+00, 1.033e+00, 9.583e-01, 8.921e-01, 9.126e-01, 9.173e-01, 9.638e-01, 9.997e-01, 1.083e+00, 9.733e-01, 1.392e+00, 1.480e+00, 1.631e+00, 1.613e+00, 1.484e+00, 1.402e+00, 1.321e+00, 1.179e+00, 1.038e+00, 4.935e-01, 6.432e-01, 4.897e-01, 3.755e-01, 2.844e-01, 2.173e-01, 1.724e-01, 1.396e-01, 1.122e-01, 9.623e-02, 7.001e-02, 5.444e-02, 4.302e-02, 2.219e-02, 3.692e-02, 3.298e-02, 3.077e-02, 4.354e-02, 3.364e-02, 2.241e-02, 2.204e-02, 1.546e-02, 2.182e-02, 1.381e-02, 2.697e-04, 2.998e-02, 2.042e-02, 2.081e-02, 9.296e-05, 6.328e-03, 1.488e-05, 0.000e+00, 5.635e-03, 0.000e+00, 6.641e-06, 0.000e+00, 1.019e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 2.845e-06, 0.000e+0}},
{"TTWZ_TuneCP5_13TeV-madgraph-pythia8",{2.193e-03, 2.357e-01, 1.641e-01, 1.765e-01, 4.772e-01, 4.294e-01, 4.084e-01, 3.182e-01, 1.837e-01, 3.130e-01, 3.712e-01, 3.423e-01, 3.443e-01, 5.542e-01, 5.957e-01, 7.160e-01, 7.507e-01, 8.501e-01, 9.148e-01, 9.556e-01, 1.065e+00, 1.117e+00, 1.120e+00, 1.194e+00, 1.228e+00, 1.183e+00, 1.199e+00, 1.233e+00, 1.278e+00, 1.264e+00, 1.264e+00, 1.195e+00, 1.174e+00, 1.128e+00, 1.104e+00, 1.078e+00, 1.002e+00, 9.906e-01, 9.188e-01, 8.871e-01, 8.747e-01, 8.623e-01, 9.298e-01, 9.510e-01, 9.716e-01, 1.203e+00, 1.379e+00, 1.446e+00, 1.521e+00, 1.455e+00, 1.569e+00, 1.241e+00, 1.374e+00, 1.214e+00, 1.039e+00, 8.182e-01, 6.465e-01, 2.899e-01, 3.717e-01, 2.762e-01, 2.194e-01, 1.656e-01, 1.277e-01, 1.117e-01, 9.369e-02, 6.612e-02, 4.804e-02, 4.259e-02, 3.841e-02, 3.395e-02, 3.456e-02, 3.364e-02, 2.940e-02, 2.649e-02, 2.134e-02, 1.761e-02, 2.194e-02, 2.023e-02, 2.413e-02, 2.195e-02, 1.797e-02, 3.059e-02, 0.000e+00, 7.033e-03, 9.481e-03, 6.359e-03, 0.000e+00, 2.842e-05, 3.709e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 2.018e-05, 3.097e-05, 0.000e+00, 3.248e-06, 0.000e+0}},
{"TTZH_TuneCP5_13TeV-madgraph-pythia8",{2.231e-03, 1.497e+00, 1.128e+00, 1.072e+00, 5.981e-01, 8.323e-01, 7.867e-01, 7.140e-01, 2.770e-01, 7.616e-01, 8.339e-01, 8.947e-01, 7.843e-01, 7.411e-01, 6.884e-01, 6.519e-01, 6.694e-01, 7.349e-01, 7.974e-01, 8.940e-01, 9.605e-01, 9.842e-01, 1.080e+00, 1.110e+00, 1.203e+00, 1.185e+00, 1.160e+00, 1.193e+00, 1.292e+00, 1.286e+00, 1.208e+00, 1.231e+00, 1.196e+00, 1.170e+00, 1.117e+00, 1.032e+00, 1.014e+00, 9.952e-01, 9.434e-01, 8.909e-01, 9.115e-01, 8.885e-01, 9.305e-01, 7.390e-01, 1.081e+00, 1.252e+00, 1.351e+00, 1.454e+00, 1.562e+00, 1.614e+00, 1.561e+00, 9.621e-01, 1.372e+00, 1.196e+00, 1.066e+00, 8.387e-01, 6.449e-01, 5.068e-01, 3.725e-01, 2.934e-01, 2.234e-01, 1.663e-01, 1.357e-01, 1.177e-01, 9.130e-02, 6.557e-02, 5.562e-02, 4.260e-02, 4.071e-02, 3.465e-02, 3.617e-02, 2.716e-02, 2.990e-02, 3.139e-02, 2.300e-02, 2.377e-02, 1.990e-02, 2.029e-02, 2.419e-02, 3.301e-02, 1.763e-04, 1.534e-02, 2.084e-02, 9.402e-03, 9.506e-03, 0.000e+00, 0.000e+00, 5.642e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 1.012e-04, 2.070e-05, 0.000e+00, 3.256e-06, 0.000e+0}},
{"TTZToLLNuNu_M-10_TuneCP5_PSweights_13TeV-amcatnlo-pythia8",{1.849e-01, 2.951e+00, 2.732e+00, 2.349e+00, 1.347e+00, 1.574e+00, 1.266e+00, 1.143e+00, 5.225e-01, 9.525e-01, 1.058e+00, 1.031e+00, 9.952e-01, 9.102e-01, 8.238e-01, 7.977e-01, 8.181e-01, 8.702e-01, 9.308e-01, 9.879e-01, 1.037e+00, 1.091e+00, 1.128e+00, 1.163e+00, 1.166e+00, 1.172e+00, 1.169e+00, 1.184e+00, 1.204e+00, 1.214e+00, 1.210e+00, 1.182e+00, 1.138e+00, 1.085e+00, 1.038e+00, 9.941e-01, 9.584e-01, 9.318e-01, 8.736e-01, 8.283e-01, 8.283e-01, 8.403e-01, 8.651e-01, 9.219e-01, 1.009e+00, 1.112e+00, 1.247e+00, 1.346e+00, 1.441e+00, 1.482e+00, 1.469e+00, 1.421e+00, 1.309e+00, 1.159e+00, 9.946e-01, 8.058e-01, 6.278e-01, 4.761e-01, 3.601e-01, 2.725e-01, 2.111e-01, 1.675e-01, 1.314e-01, 1.080e-01, 8.931e-02, 6.485e-02, 4.803e-02, 4.320e-02, 3.768e-02, 3.384e-02, 3.083e-02, 3.044e-02, 2.916e-02, 2.786e-02, 2.436e-02, 1.962e-02, 2.313e-02, 2.133e-02, 2.435e-02, 2.462e-02, 3.200e-02, 2.372e-02, 2.961e-02, 1.901e-02, 1.612e-02, 2.579e-02, 2.485e-02, 1.648e-02, 2.444e-02, 1.600e-02, 8.319e-03, 0.000e+00, 1.718e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8",{3.896e-01, 0.000e+00, 2.559e+00, -1.181e+01, 1.808e+00, 1.471e+00, 1.076e+00, 1.214e+00, 4.630e-01, 1.514e+00, 1.307e+00, 1.026e+00, 1.037e+00, 8.905e-01, 7.712e-01, 7.898e-01, 8.582e-01, 8.567e-01, 9.164e-01, 9.717e-01, 1.024e+00, 1.088e+00, 1.112e+00, 1.200e+00, 1.158e+00, 1.158e+00, 1.255e+00, 1.198e+00, 1.203e+00, 1.219e+00, 1.196e+00, 1.148e+00, 1.130e+00, 1.097e+00, 1.021e+00, 1.006e+00, 9.738e-01, 9.077e-01, 8.796e-01, 8.053e-01, 8.437e-01, 8.455e-01, 8.714e-01, 9.126e-01, 1.022e+00, 1.105e+00, 1.211e+00, 1.291e+00, 1.413e+00, 1.493e+00, 1.492e+00, 1.322e+00, 1.368e+00, 1.343e+00, 1.019e+00, 7.570e-01, 6.408e-01, 4.857e-01, 3.534e-01, 2.895e-01, 2.150e-01, 1.531e-01, 1.377e-01, 1.010e-01, 8.549e-02, 6.294e-02, 4.749e-02, 3.897e-02, 3.573e-02, 3.654e-02, 3.028e-02, 5.064e-02, 2.885e-02, 3.195e-02, 2.208e-02, 2.355e-02, 0.000e+00, 2.044e-02, 1.045e-02, 2.852e-02, -5.836e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, -3.656e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"TTZZ_TuneCP5_13TeV-madgraph-pythia8",{1.966e-04, 2.642e-01, 1.339e-01, 1.494e-01, 8.294e-02, 1.436e-01, 2.301e-01, 3.000e-01, 1.603e-01, 3.082e-01, 4.058e-01, 3.756e-01, 4.391e-01, 7.582e-01, 6.749e-01, 4.623e-01, 6.917e-01, 7.297e-01, 7.493e-01, 8.607e-01, 9.787e-01, 1.086e+00, 1.059e+00, 1.210e+00, 1.214e+00, 1.211e+00, 1.194e+00, 1.219e+00, 1.336e+00, 1.342e+00, 1.377e+00, 1.312e+00, 1.288e+00, 1.225e+00, 1.174e+00, 1.138e+00, 1.093e+00, 7.940e-01, 9.857e-01, 9.510e-01, 9.196e-01, 9.669e-01, 1.012e+00, 8.598e-01, 1.137e+00, 1.239e+00, 1.477e+00, 1.583e+00, 1.680e+00, 1.739e+00, 1.200e+00, 1.622e+00, 1.496e+00, 1.294e+00, 1.082e+00, 8.740e-01, 6.703e-01, 5.453e-01, 4.012e-01, 3.013e-01, 2.393e-01, 1.809e-01, 1.460e-01, 1.177e-01, 9.962e-02, 7.139e-02, 4.066e-02, 4.535e-02, 3.941e-02, 3.904e-02, 2.950e-02, 3.374e-02, 3.377e-02, 2.558e-02, 2.045e-02, 1.717e-02, 2.323e-02, 2.185e-02, 1.489e-02, 1.468e-02, 3.004e-02, 3.069e-02, 4.169e-02, 9.406e-03, 9.510e-03, 8.505e-04, 8.511e-03, 5.645e-03, 0.000e+00, 0.000e+00, 0.000e+00, 1.021e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 5.060e-05, 0.000e+00, 0.000e+00, 3.800e-06, 0.000e+0}},
{"WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8",{1.819e-01, 4.056e+00, 2.617e+00, 2.405e+00, 1.556e+00, 1.316e+00, 1.282e+00, 1.108e+00, 4.911e-01, 9.681e-01, 1.080e+00, 1.028e+00, 1.000e+00, 8.999e-01, 8.246e-01, 7.932e-01, 8.111e-01, 8.694e-01, 9.329e-01, 9.856e-01, 1.033e+00, 1.083e+00, 1.127e+00, 1.155e+00, 1.164e+00, 1.167e+00, 1.173e+00, 1.184e+00, 1.212e+00, 1.214e+00, 1.207e+00, 1.178e+00, 1.140e+00, 1.090e+00, 1.038e+00, 9.958e-01, 9.560e-01, 9.314e-01, 8.812e-01, 8.337e-01, 8.288e-01, 8.387e-01, 8.670e-01, 9.198e-01, 9.993e-01, 1.113e+00, 1.250e+00, 1.345e+00, 1.445e+00, 1.488e+00, 1.492e+00, 1.430e+00, 1.315e+00, 1.165e+00, 9.955e-01, 8.024e-01, 6.305e-01, 4.783e-01, 3.609e-01, 2.745e-01, 2.105e-01, 1.646e-01, 1.313e-01, 1.072e-01, 8.925e-02, 6.455e-02, 4.804e-02, 4.171e-02, 3.745e-02, 3.407e-02, 3.174e-02, 3.047e-02, 2.872e-02, 2.916e-02, 2.308e-02, 1.952e-02, 2.043e-02, 2.176e-02, 2.252e-02, 2.476e-02, 2.713e-02, 2.698e-02, 2.876e-02, 2.031e-02, 1.601e-02, 1.811e-02, 2.285e-02, 3.299e-02, 1.945e-02, 1.152e-02, 2.246e-02, 3.382e-02, 2.165e-02, 8.250e-03, 0.000e+00, 1.623e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8",{1.853e-01, 3.673e+00, 2.819e+00, 2.494e+00, 1.411e+00, 1.356e+00, 1.244e+00, 1.162e+00, 4.828e-01, 9.335e-01, 1.052e+00, 1.026e+00, 1.009e+00, 9.039e-01, 8.301e-01, 7.946e-01, 8.098e-01, 8.666e-01, 9.340e-01, 9.849e-01, 1.033e+00, 1.085e+00, 1.125e+00, 1.155e+00, 1.166e+00, 1.169e+00, 1.173e+00, 1.183e+00, 1.209e+00, 1.215e+00, 1.206e+00, 1.176e+00, 1.143e+00, 1.088e+00, 1.038e+00, 9.955e-01, 9.585e-01, 9.273e-01, 8.773e-01, 8.345e-01, 8.276e-01, 8.412e-01, 8.689e-01, 9.172e-01, 1.003e+00, 1.114e+00, 1.251e+00, 1.344e+00, 1.452e+00, 1.487e+00, 1.495e+00, 1.431e+00, 1.318e+00, 1.167e+00, 9.937e-01, 8.011e-01, 6.293e-01, 4.753e-01, 3.607e-01, 2.747e-01, 2.117e-01, 1.646e-01, 1.322e-01, 1.068e-01, 8.927e-02, 6.502e-02, 4.827e-02, 4.185e-02, 3.693e-02, 3.382e-02, 3.148e-02, 3.033e-02, 2.919e-02, 2.865e-02, 2.315e-02, 2.003e-02, 2.053e-02, 2.079e-02, 2.371e-02, 2.251e-02, 2.541e-02, 3.107e-02, 3.121e-02, 1.923e-02, 1.963e-02, 2.608e-02, 1.846e-02, 3.333e-02, 1.648e-02, 1.991e-02, 2.103e-02, 3.618e-02, 1.390e-02, 8.827e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8",{1.833e-01, 3.548e+00, 2.672e+00, 2.664e+00, 1.389e+00, 1.318e+00, 1.242e+00, 1.136e+00, 5.017e-01, 9.307e-01, 1.057e+00, 1.030e+00, 1.015e+00, 9.003e-01, 8.242e-01, 7.936e-01, 8.110e-01, 8.690e-01, 9.355e-01, 9.848e-01, 1.034e+00, 1.086e+00, 1.130e+00, 1.156e+00, 1.165e+00, 1.164e+00, 1.174e+00, 1.182e+00, 1.211e+00, 1.211e+00, 1.207e+00, 1.180e+00, 1.140e+00, 1.089e+00, 1.038e+00, 9.958e-01, 9.591e-01, 9.291e-01, 8.777e-01, 8.305e-01, 8.305e-01, 8.387e-01, 8.688e-01, 9.217e-01, 9.970e-01, 1.113e+00, 1.247e+00, 1.346e+00, 1.446e+00, 1.486e+00, 1.494e+00, 1.428e+00, 1.314e+00, 1.165e+00, 9.955e-01, 8.020e-01, 6.291e-01, 4.764e-01, 3.604e-01, 2.751e-01, 2.117e-01, 1.644e-01, 1.312e-01, 1.075e-01, 8.893e-02, 6.525e-02, 4.842e-02, 4.231e-02, 3.702e-02, 3.415e-02, 3.192e-02, 3.011e-02, 2.946e-02, 2.898e-02, 2.257e-02, 1.983e-02, 2.045e-02, 2.201e-02, 2.192e-02, 2.513e-02, 2.597e-02, 2.530e-02, 2.857e-02, 2.281e-02, 2.029e-02, 2.276e-02, 2.590e-02, 2.781e-02, 2.026e-02, 6.299e-02, 3.276e-02, 2.642e-02, 2.255e-02, 1.432e-02, 2.707e-02, 5.636e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8",{1.839e-01, 3.412e+00, 3.170e+00, 2.695e+00, 1.414e+00, 1.312e+00, 1.258e+00, 1.174e+00, 4.928e-01, 9.279e-01, 1.067e+00, 1.030e+00, 1.006e+00, 9.016e-01, 8.276e-01, 7.945e-01, 8.067e-01, 8.662e-01, 9.320e-01, 9.837e-01, 1.033e+00, 1.085e+00, 1.129e+00, 1.153e+00, 1.167e+00, 1.169e+00, 1.172e+00, 1.184e+00, 1.212e+00, 1.213e+00, 1.209e+00, 1.181e+00, 1.141e+00, 1.089e+00, 1.039e+00, 9.938e-01, 9.553e-01, 9.286e-01, 8.807e-01, 8.325e-01, 8.272e-01, 8.384e-01, 8.690e-01, 9.176e-01, 1.002e+00, 1.116e+00, 1.250e+00, 1.346e+00, 1.451e+00, 1.492e+00, 1.494e+00, 1.432e+00, 1.317e+00, 1.167e+00, 9.937e-01, 8.028e-01, 6.291e-01, 4.736e-01, 3.621e-01, 2.747e-01, 2.120e-01, 1.651e-01, 1.312e-01, 1.059e-01, 8.941e-02, 6.451e-02, 4.819e-02, 4.201e-02, 3.708e-02, 3.386e-02, 3.152e-02, 3.032e-02, 2.914e-02, 2.910e-02, 2.277e-02, 1.998e-02, 2.062e-02, 2.017e-02, 2.191e-02, 2.382e-02, 2.366e-02, 2.773e-02, 2.634e-02, 2.056e-02, 2.226e-02, 3.036e-02, 1.688e-02, 2.519e-02, 1.476e-02, 3.477e-02, 2.825e-02, 2.430e-02, 4.668e-02, 9.882e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8",{1.840e-01, 3.058e+00, 2.880e+00, 2.656e+00, 1.361e+00, 1.324e+00, 1.251e+00, 1.179e+00, 4.951e-01, 9.619e-01, 1.050e+00, 1.028e+00, 1.004e+00, 9.024e-01, 8.226e-01, 7.965e-01, 8.113e-01, 8.720e-01, 9.336e-01, 9.831e-01, 1.037e+00, 1.085e+00, 1.130e+00, 1.156e+00, 1.165e+00, 1.169e+00, 1.169e+00, 1.181e+00, 1.210e+00, 1.214e+00, 1.209e+00, 1.180e+00, 1.140e+00, 1.087e+00, 1.037e+00, 9.930e-01, 9.574e-01, 9.281e-01, 8.805e-01, 8.352e-01, 8.259e-01, 8.413e-01, 8.684e-01, 9.198e-01, 1.001e+00, 1.110e+00, 1.250e+00, 1.345e+00, 1.451e+00, 1.487e+00, 1.490e+00, 1.428e+00, 1.319e+00, 1.171e+00, 9.945e-01, 8.043e-01, 6.309e-01, 4.762e-01, 3.609e-01, 2.735e-01, 2.109e-01, 1.648e-01, 1.314e-01, 1.066e-01, 8.887e-02, 6.481e-02, 4.796e-02, 4.223e-02, 3.754e-02, 3.379e-02, 3.163e-02, 3.010e-02, 2.851e-02, 2.918e-02, 2.358e-02, 1.956e-02, 2.048e-02, 2.016e-02, 2.242e-02, 2.231e-02, 2.351e-02, 2.636e-02, 3.178e-02, 2.263e-02, 1.889e-02, 2.511e-02, 2.247e-02, 1.910e-02, 2.120e-02, 2.197e-02, 2.448e-02, 1.382e-02, 1.415e-02, 1.124e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8",{1.657e-01, 3.102e+00, 2.531e+00, 2.614e+00, 1.367e+00, 1.276e+00, 1.252e+00, 1.145e+00, 4.905e-01, 9.360e-01, 1.068e+00, 1.022e+00, 1.010e+00, 9.010e-01, 8.237e-01, 7.969e-01, 8.116e-01, 8.674e-01, 9.339e-01, 9.865e-01, 1.033e+00, 1.086e+00, 1.129e+00, 1.155e+00, 1.167e+00, 1.170e+00, 1.172e+00, 1.181e+00, 1.210e+00, 1.210e+00, 1.208e+00, 1.179e+00, 1.137e+00, 1.090e+00, 1.038e+00, 9.956e-01, 9.578e-01, 9.285e-01, 8.800e-01, 8.333e-01, 8.291e-01, 8.382e-01, 8.683e-01, 9.207e-01, 9.987e-01, 1.116e+00, 1.248e+00, 1.341e+00, 1.445e+00, 1.488e+00, 1.488e+00, 1.431e+00, 1.312e+00, 1.164e+00, 9.935e-01, 8.048e-01, 6.309e-01, 4.764e-01, 3.629e-01, 2.739e-01, 2.113e-01, 1.655e-01, 1.318e-01, 1.066e-01, 8.918e-02, 6.473e-02, 4.822e-02, 4.186e-02, 3.754e-02, 3.404e-02, 3.162e-02, 2.997e-02, 2.946e-02, 2.965e-02, 2.342e-02, 1.894e-02, 2.097e-02, 2.066e-02, 2.116e-02, 2.395e-02, 2.584e-02, 2.502e-02, 2.981e-02, 1.962e-02, 2.220e-02, 2.313e-02, 2.216e-02, 2.388e-02, 1.717e-02, 2.472e-02, 1.785e-02, 2.592e-02, 2.212e-02, 0.000e+00, 1.328e-02, 1.659e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WW_TuneCP5_13TeV-pythia8",{1.692e-01, 3.240e+00, 2.724e+00, 2.367e+00, 1.460e+00, 1.326e+00, 1.201e+00, 1.062e+00, 5.075e-01, 9.471e-01, 1.068e+00, 1.032e+00, 1.016e+00, 8.993e-01, 8.235e-01, 7.977e-01, 8.132e-01, 8.716e-01, 9.297e-01, 9.878e-01, 1.033e+00, 1.086e+00, 1.130e+00, 1.157e+00, 1.165e+00, 1.165e+00, 1.173e+00, 1.179e+00, 1.208e+00, 1.214e+00, 1.206e+00, 1.178e+00, 1.141e+00, 1.088e+00, 1.040e+00, 9.921e-01, 9.568e-01, 9.299e-01, 8.814e-01, 8.345e-01, 8.274e-01, 8.371e-01, 8.689e-01, 9.158e-01, 9.980e-01, 1.112e+00, 1.254e+00, 1.346e+00, 1.452e+00, 1.489e+00, 1.498e+00, 1.429e+00, 1.310e+00, 1.160e+00, 9.970e-01, 8.069e-01, 6.318e-01, 4.768e-01, 3.605e-01, 2.747e-01, 2.115e-01, 1.646e-01, 1.320e-01, 1.062e-01, 8.940e-02, 6.485e-02, 4.829e-02, 4.191e-02, 3.788e-02, 3.430e-02, 3.082e-02, 3.046e-02, 2.790e-02, 2.928e-02, 2.445e-02, 1.997e-02, 1.989e-02, 2.053e-02, 2.143e-02, 2.247e-02, 2.340e-02, 2.344e-02, 2.255e-02, 2.155e-02, 2.470e-02, 3.313e-02, 1.745e-02, 2.443e-02, 4.830e-02, 2.371e-02, 2.055e-02, 3.978e-02, 6.366e-03, 5.391e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"WZ_TuneCP5_13TeV-pythia8",{2.795e-04, 8.136e-03, 3.035e-02, 6.774e-02, 7.990e-02, 1.602e-01, 1.867e-01, 2.041e-01, 8.812e-02, 2.672e-01, 3.006e-01, 4.491e-01, 5.373e-01, 5.869e-01, 5.671e-01, 5.694e-01, 6.374e-01, 7.804e-01, 8.728e-01, 9.482e-01, 1.056e+00, 1.113e+00, 1.168e+00, 1.208e+00, 1.239e+00, 1.243e+00, 1.236e+00, 1.275e+00, 1.322e+00, 1.332e+00, 1.290e+00, 1.272e+00, 1.237e+00, 1.194e+00, 1.153e+00, 1.105e+00, 1.052e+00, 1.012e+00, 9.507e-01, 9.288e-01, 8.900e-01, 8.994e-01, 9.471e-01, 1.026e+00, 1.113e+00, 1.214e+00, 1.369e+00, 1.486e+00, 1.571e+00, 1.648e+00, 1.606e+00, 1.552e+00, 1.427e+00, 1.202e+00, 1.048e+00, 8.340e-01, 6.822e-01, 5.145e-01, 3.913e-01, 2.978e-01, 2.172e-01, 1.709e-01, 1.292e-01, 1.026e-01, 9.116e-02, 6.964e-02, 4.636e-02, 4.335e-02, 3.016e-02, 3.406e-02, 1.873e-02, 1.873e-02, 1.578e-02, 3.180e-02, 1.304e-02, 4.507e-03, 3.148e-03, 2.089e-02, 1.124e-03, 8.538e-04, 1.786e-03, 3.853e-04, 5.193e-04, 1.189e-04, 1.973e-02, 1.610e-04, 1.256e-04, 2.115e-04, 1.502e-05, 8.038e-05, 2.004e-05, 1.677e-03, 4.294e-03, 4.091e-03, 1.718e-03, 8.029e-06, 3.324e-04, 1.224e-03, 2.661e-06, 3.164e-06, 0.000e+0}},
{"ZZ_TuneCP5_13TeV-pythia8",{1.970e-01, 3.944e+00, 2.827e+00, 2.446e+00, 1.819e+00, 1.326e+00, 1.184e+00, 1.137e+00, 5.131e-01, 9.896e-01, 1.094e+00, 1.047e+00, 1.008e+00, 8.963e-01, 8.164e-01, 7.864e-01, 8.124e-01, 8.802e-01, 9.277e-01, 9.891e-01, 1.033e+00, 1.082e+00, 1.126e+00, 1.161e+00, 1.164e+00, 1.160e+00, 1.170e+00, 1.188e+00, 1.205e+00, 1.224e+00, 1.209e+00, 1.182e+00, 1.135e+00, 1.084e+00, 1.044e+00, 9.936e-01, 9.554e-01, 9.307e-01, 8.811e-01, 8.309e-01, 8.276e-01, 8.387e-01, 8.725e-01, 9.208e-01, 9.946e-01, 1.118e+00, 1.270e+00, 1.340e+00, 1.453e+00, 1.478e+00, 1.477e+00, 1.428e+00, 1.339e+00, 1.161e+00, 1.002e+00, 7.975e-01, 6.255e-01, 4.737e-01, 3.583e-01, 2.751e-01, 2.129e-01, 1.651e-01, 1.323e-01, 1.073e-01, 8.761e-02, 6.351e-02, 4.763e-02, 4.187e-02, 3.768e-02, 3.304e-02, 3.115e-02, 2.975e-02, 2.936e-02, 2.895e-02, 2.396e-02, 2.081e-02, 2.050e-02, 2.326e-02, 2.461e-02, 2.836e-02, 2.902e-02, 2.470e-02, 1.611e-02, 1.817e-02, 1.148e-02, 3.081e-02, 4.111e-02, 9.088e-03, 1.797e-02, 2.352e-02, 7.645e-03, 9.865e-03, 6.315e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8",{1.747e-01, 2.984e+00, 2.717e+00, 2.686e+00, 1.440e+00, 1.432e+00, 1.175e+00, 1.147e+00, 4.729e-01, 9.762e-01, 1.057e+00, 1.021e+00, 1.014e+00, 8.959e-01, 8.300e-01, 7.950e-01, 8.088e-01, 8.677e-01, 9.335e-01, 9.819e-01, 1.036e+00, 1.085e+00, 1.134e+00, 1.154e+00, 1.165e+00, 1.163e+00, 1.174e+00, 1.183e+00, 1.209e+00, 1.211e+00, 1.205e+00, 1.178e+00, 1.142e+00, 1.090e+00, 1.037e+00, 9.950e-01, 9.591e-01, 9.293e-01, 8.791e-01, 8.356e-01, 8.262e-01, 8.381e-01, 8.665e-01, 9.222e-01, 1.007e+00, 1.110e+00, 1.255e+00, 1.342e+00, 1.454e+00, 1.493e+00, 1.479e+00, 1.417e+00, 1.316e+00, 1.166e+00, 9.955e-01, 7.989e-01, 6.320e-01, 4.777e-01, 3.628e-01, 2.742e-01, 2.122e-01, 1.651e-01, 1.316e-01, 1.065e-01, 8.899e-02, 6.496e-02, 4.815e-02, 4.137e-02, 3.812e-02, 3.438e-02, 3.115e-02, 3.017e-02, 2.976e-02, 2.770e-02, 2.355e-02, 2.102e-02, 1.972e-02, 2.043e-02, 2.252e-02, 2.097e-02, 2.279e-02, 2.506e-02, 3.026e-02, 2.048e-02, 2.130e-02, 3.847e-02, 2.383e-02, 1.475e-02, 2.083e-02, 4.773e-02, 1.034e-02, 0.000e+00, 1.281e-02, 5.425e-03, 0.000e+00, 6.405e-03, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}},
{"ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8",{1.757e-01, 4.202e+00, 2.724e+00, 2.663e+00, 1.325e+00, 1.292e+00, 1.198e+00, 1.139e+00, 4.962e-01, 9.436e-01, 1.059e+00, 1.033e+00, 1.014e+00, 9.063e-01, 8.277e-01, 7.931e-01, 8.135e-01, 8.669e-01, 9.307e-01, 9.881e-01, 1.035e+00, 1.082e+00, 1.132e+00, 1.153e+00, 1.163e+00, 1.166e+00, 1.171e+00, 1.182e+00, 1.210e+00, 1.211e+00, 1.210e+00, 1.178e+00, 1.141e+00, 1.091e+00, 1.036e+00, 9.937e-01, 9.554e-01, 9.298e-01, 8.810e-01, 8.343e-01, 8.271e-01, 8.393e-01, 8.732e-01, 9.213e-01, 1.000e+00, 1.113e+00, 1.251e+00, 1.353e+00, 1.440e+00, 1.488e+00, 1.498e+00, 1.425e+00, 1.318e+00, 1.160e+00, 9.935e-01, 8.006e-01, 6.306e-01, 4.774e-01, 3.614e-01, 2.747e-01, 2.121e-01, 1.650e-01, 1.306e-01, 1.072e-01, 8.853e-02, 6.520e-02, 4.792e-02, 4.159e-02, 3.668e-02, 3.406e-02, 3.156e-02, 2.979e-02, 3.037e-02, 3.065e-02, 2.332e-02, 1.944e-02, 2.117e-02, 2.131e-02, 2.186e-02, 2.747e-02, 2.788e-02, 3.053e-02, 2.214e-02, 2.092e-02, 1.967e-02, 2.005e-02, 2.573e-02, 2.218e-02, 2.436e-02, 1.063e-02, 2.073e-02, 4.012e-02, 6.422e-03, 1.632e-02, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+0}}
};

	*pileupweight = pileupweights.at(sample)[nTrueInt];
	*pileupweightup = pileupweightsUp.at(sample)[nTrueInt];
	*pileupweightdn = pileupweightsDn.at(sample)[nTrueInt];

}

void HardcodedConditions::GetPileupWeight2018(int nTrueInt, float *pileupweight, float *pileupweightup, float *pileupweightdn, std::string sample)
{
   // Pileup distributions -- Centrally-stored data PU hists 2018 vs 2018 TTToSemiLeptonic
   std::vector<float> pileupweights;
   std::vector<float> pileupweightsUp;
   std::vector<float> pileupweightsDn;

   pileupweights = { 0.000e+00,  1.250e+01,  5.025e+01,  1.900e+01,  1.197e+01,  9.118e+00,  6.647e+00,  4.832e+00,  3.633e+00,  2.747e+00,  
		    2.238e+00,  1.904e+00,  1.694e+00,  1.572e+00,  1.502e+00,  1.468e+00,  1.451e+00,  1.452e+00,  1.461e+00,  1.467e+00,  
		    1.458e+00,  1.436e+00,  1.401e+00,  1.352e+00,  1.302e+00,  1.250e+00,  1.205e+00,  1.167e+00,  1.138e+00,  1.116e+00,  
		    1.100e+00,  1.089e+00,  1.081e+00,  1.077e+00,  1.074e+00,  1.069e+00,  1.063e+00,  1.052e+00,  1.035e+00,  1.012e+00,  
		    9.794e-01,  9.367e-01,  8.867e-01,  8.272e-01,  7.609e-01,  6.925e-01,  6.209e-01,  5.505e-01,  4.824e-01,  4.193e-01,  
		    3.621e-01,  3.103e-01,  2.658e-01,  2.276e-01,  1.948e-01,  1.679e-01,  1.455e-01,  1.262e-01,  1.098e-01,  9.584e-02,  
		    8.398e-02,  7.342e-02,  6.469e-02,  5.654e-02,  4.900e-02,  4.233e-02,  3.634e-02,  3.081e-02,  2.661e-02,  2.266e-02,  
		    1.889e-02,  1.652e-02,  1.344e-02,  1.173e-02,  9.423e-03,  8.155e-03,  6.671e-03,  5.637e-03,  4.504e-03,  3.920e-03,  
		    3.007e-03,  2.567e-03,  1.909e-03,  1.425e-03,  1.084e-03,  8.974e-04,  8.267e-04,  4.805e-04,  2.814e-04,  1.588e-04,  
		    1.206e-04,  6.816e-05,  2.870e-05,  1.436e-05,  7.136e-06,  4.702e-06,  1.107e-06,  1.723e-06,  1.079e-06,  1.269e-07,  0.000e+00,  }; // TTToSemiLeptonic
   pileupweightsUp = { 0.000e+00,  1.447e+01,  5.931e+01,  2.226e+01,  1.397e+01,  1.063e+01,  7.865e+00,  5.773e+00,  4.367e+00,  3.362e+00,  
			2.793e+00,  2.408e+00,  2.153e+00,  1.999e+00,  1.907e+00,  1.857e+00,  1.824e+00,  1.805e+00,  1.789e+00,  1.761e+00,  
			1.710e+00,  1.645e+00,  1.572e+00,  1.493e+00,  1.423e+00,  1.358e+00,  1.306e+00,  1.264e+00,  1.232e+00,  1.206e+00,  
			1.185e+00,  1.166e+00,  1.148e+00,  1.131e+00,  1.111e+00,  1.085e+00,  1.054e+00,  1.014e+00,  9.643e-01,  9.065e-01,  
			8.402e-01,  7.663e-01,  6.892e-01,  6.091e-01,  5.296e-01,  4.550e-01,  3.850e-01,  3.223e-01,  2.671e-01,  2.202e-01,  
			1.810e-01,  1.482e-01,  1.217e-01,  1.003e-01,  8.289e-02,  6.902e-02,  5.780e-02,  4.834e-02,  4.046e-02,  3.384e-02,  
			2.830e-02,  2.351e-02,  1.962e-02,  1.619e-02,  1.322e-02,  1.075e-02,  8.680e-03,  6.919e-03,  5.624e-03,  4.508e-03,  
			3.538e-03,  2.915e-03,  2.233e-03,  1.832e-03,  1.382e-03,  1.121e-03,  8.562e-04,  6.734e-04,  4.991e-04,  4.012e-04,  
			2.833e-04,  2.218e-04,  1.506e-04,  1.023e-04,  7.060e-05,  5.282e-05,  4.385e-05,  2.290e-05,  1.202e-05,  6.059e-06,  
			4.098e-06,  2.061e-06,  7.699e-07,  3.418e-07,  1.507e-07,  8.865e-08,  1.895e-08,  2.792e-08,  1.816e-08,  2.615e-09,  0.000e+00,  }; // TTToSemiLeptonic
   pileupweightsDn = { 0.000e+00,  1.091e+01,  4.288e+01,  1.632e+01,  1.032e+01,  7.892e+00,  5.683e+00,  4.086e+00,  3.057e+00,  2.285e+00,  
		      1.826e+00,  1.531e+00,  1.349e+00,  1.249e+00,  1.194e+00,  1.169e+00,  1.161e+00,  1.169e+00,  1.188e+00,  1.211e+00,  
		      1.226e+00,  1.233e+00,  1.230e+00,  1.210e+00,  1.183e+00,  1.147e+00,  1.112e+00,  1.080e+00,  1.053e+00,  1.034e+00,  
		      1.020e+00,  1.013e+00,  1.010e+00,  1.013e+00,  1.018e+00,  1.026e+00,  1.035e+00,  1.044e+00,  1.051e+00,  1.055e+00,  
		      1.054e+00,  1.045e+00,  1.030e+00,  1.004e+00,  9.672e-01,  9.247e-01,  8.727e-01,  8.155e-01,  7.534e-01,  6.903e-01,  
		      6.275e-01,  5.648e-01,  5.067e-01,  4.529e-01,  4.034e-01,  3.604e-01,  3.231e-01,  2.891e-01,  2.595e-01,  2.338e-01,  
		      2.119e-01,  1.921e-01,  1.761e-01,  1.607e-01,  1.459e-01,  1.325e-01,  1.199e-01,  1.073e-01,  9.796e-02,  8.821e-02,  
		      7.775e-02,  7.190e-02,  6.182e-02,  5.697e-02,  4.835e-02,  4.420e-02,  3.822e-02,  3.417e-02,  2.895e-02,  2.677e-02,  
		      2.188e-02,  1.996e-02,  1.591e-02,  1.278e-02,  1.049e-02,  9.408e-03,  9.417e-03,  5.965e-03,  3.820e-03,  2.364e-03,  
		      1.972e-03,  1.229e-03,  5.718e-04,  3.170e-04,  1.748e-04,  1.282e-04,  3.363e-05,  5.837e-05,  4.079e-05,  5.342e-06,  0.000e+00,  }; // TTToSemiLeptonic

	*pileupweight = pileupweights[nTrueInt];
	*pileupweightup = pileupweightsUp[nTrueInt];
	*pileupweightdn = pileupweightsDn[nTrueInt];

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
