/*************************************************************
Class Usage:
This class should only be used for upgrading and downgrading 
if a single operating point is used in an analysis. 
bool isBTagged = b-tag flag for jet
int pdgIdPart = parton id
float Btag_SF = MC/data scale factor for b/c-tagging efficiency
float Btag_eff = b/c-tagging efficiency in data
float Bmistag_SF = MC/data scale factor for mistag efficiency
float Bmistag_eff = mistag efficiency in data
Author: Michael Segala
Contact: michael.segala@gmail.com
Updated: Ulrich Heintz 12/23/2011
Updated: Gena Kukartsev 10/30/2012 
Updated: Daniel Li 11/29/2021
v 1.2
Comments (09/07/2021):
- Updated to use deepJet instead of deepCSV for b-tagging
- Update subjet WP for UL 
*************************************************************/


#include "FWLJMET/LJMET/interface/BTagSFUtil.h"



BTagSFUtil::BTagSFUtil() {
}



BTagSFUtil::BTagSFUtil(int seed) {
  SetSeed(seed);
}



BTagSFUtil::~BTagSFUtil() {

}


void BTagSFUtil::Initialize(const edm::ParameterSet& iConfig){

	
    //BTAG parameter initialization
    std::cout << mLegend << "Initializing BTagSFUtil object." << std::endl;

    debug              = iConfig.getParameter<bool>("debug");

    bdisc_min          = iConfig.getParameter<double>("bdisc_min");
    DeepJetfile        = iConfig.getParameter<edm::FileInPath>("DeepJetfile").fullPath();
    DeepCSVSubjetfile  = iConfig.getParameter<edm::FileInPath>("DeepCSVSubjetfile").fullPath();   
    btagOP             = iConfig.getParameter<std::string>("btagOP");
    applyBtagSF        = iConfig.getParameter<bool>("applyBtagSF");
    BTagUncertUp       = iConfig.getParameter<bool>("BTagUncertUp");
    BTagUncertDown     = iConfig.getParameter<bool>("BTagUncertDown");
    MistagUncertUp     = iConfig.getParameter<bool>("MistagUncertUp");
    MistagUncertDown   = iConfig.getParameter<bool>("MistagUncertDown");

    if(DeepJetfile.find("2016Legacy") != std::string::npos) year = 2016;
    else if(DeepJetfile.find("UL17") != std::string::npos) year = 2017;
    else year = 2018;

    std::cout << mLegend << "b-tag check: DeepJet "<<btagOP<<" > "<<bdisc_min<<std::endl;
    std::cout << mLegend << "b-tag files: " << DeepJetfile << ", " << DeepCSVSubjetfile << std::endl;
    std::cout << mLegend << "b-tag year: " << year << std::endl;
    calib   = BTagCalibration("deepcsv",DeepJetfile);
    calibsj = BTagCalibration("deepcsvsj",DeepCSVSubjetfile);
    if(btagOP == "LOOSE"){
      reader   = BTagCalibrationReader(BTagEntry::OP_LOOSE, "central", {"up","down"});
      readerSJ = BTagCalibrationReader(BTagEntry::OP_LOOSE, "central", {"up","down"});
    }else if(btagOP == "TIGHT"){
      reader   = BTagCalibrationReader(BTagEntry::OP_TIGHT, "central", {"up","down"});
    }else{
      reader   = BTagCalibrationReader(BTagEntry::OP_MEDIUM, "central", {"up","down"});
      readerSJ = BTagCalibrationReader(BTagEntry::OP_MEDIUM, "central", {"up","down"});
    }
    reader.load(calib, BTagEntry::FLAV_B, "comb");
    reader.load(calib, BTagEntry::FLAV_C, "comb");
    reader.load(calib, BTagEntry::FLAV_UDSG, "incl");
    readerSJ.load(calibsj, BTagEntry::FLAV_B, "lt");
    readerSJ.load(calibsj, BTagEntry::FLAV_C, "lt");
    readerSJ.load(calibsj, BTagEntry::FLAV_UDSG, "incl");

    // Set Subjet WPs manually since we need DeepCSV instead of DeepJet
    if(btagOP == "LOOSE"){	      
      if (year == 2016) bdisc_sj = 0.2217; // need to update for UL
      else if(year == 2017) bdisc_sj = 0.1355;
      else bdisc_sj = 0.1241; # need to update
    }else{ // medium, only loose & medium for subjets
      if (year == 2016) bdisc_sj = 0.6321; // need to update
      else if(year == 2017) bdisc_sj = 0.4506;
      else bdisc_sj = 0.4184; # need to update
    }

}

void BTagSFUtil::SetSeed( int seed ) {

  rand_ . SetSeed(seed);

}



void BTagSFUtil::modifyBTagsWithSF(bool& isBTagged, 
                                   int pdgIdPart,
                                   float Btag_SF, 
                                   float Btag_eff,
                                   float Bmistag_SF, 
                                   float Bmistag_eff)
{

  bool newBTag = isBTagged;

  // b quarks and c quarks:
  if( abs( pdgIdPart ) == 5 ||  abs( pdgIdPart ) == 4) { 

    // Commented out Feb 2017 -- adding exact charm effs/SFs to HardcodedConditions and passing in "Btag" arguments
    //double bctag_eff = Btag_eff;
    //if ( abs(pdgIdPart)==4 )  bctag_eff = Btag_eff/5.0; // take ctag eff as one 5th of Btag eff
    newBTag = applySF(isBTagged, Btag_SF, Btag_eff);

  // light quarks:
  } else { // need 0's with hadronFlavor

    newBTag = applySF(isBTagged, Bmistag_SF, Bmistag_eff);
    
  }

  isBTagged = newBTag;
  
}


bool BTagSFUtil::applySF(bool& isBTagged, float Btag_SF, float Btag_eff){
  
  bool newBTag = isBTagged;

  if (Btag_SF == 1) return newBTag; //no correction needed 

  //throw die
  float coin = rand_.Uniform(1.);    
  
  if(Btag_SF > 1){  // use this if SF>1

    if( !isBTagged ) {

      //fraction of jets that need to be upgraded
      float mistagPercent = (1.0 - Btag_SF) / (1.0 - (Btag_SF/Btag_eff) );

      //upgrade to tagged
      if( coin < mistagPercent ) {newBTag = true;}
    }

  }else{  // use this if SF<1
      
    //downgrade tagged to untagged
    if( isBTagged && coin > Btag_SF ) {newBTag = false;}

  }

  return newBTag;
}



bool BTagSFUtil::isJetTagged(const pat::Jet & jet,
                                        TLorentzVector correctedJet_lv,
                                        edm::Event const & event,
                                        bool isMc,
                                        int shiftflag,
                                        bool subjetflag)
{
    bool _isTagged = false;

    if (jet.bDiscriminator("pfDeepFlavourJetTags:probb")+jet.bDiscriminator("pfDeepFlavourJetTags:probbb")+jet.bDiscriminator("pfDeepFlavourJetTags:problepb") > bdisc_min) _isTagged = true;
    if (subjetflag){
      	if (jet.bDiscriminator("pfDeepCSVJetTags:probb")+jet.bDiscriminator("pfDeepCSVJetTags:probbb") > bdisc_sj) _isTagged = true;
    }

    if (isMc && applyBtagSF){

      //TLorentzVector lvjet = correctJet(jet, event);
      TLorentzVector lvjet = correctedJet_lv;

      int _jetFlavor = abs(jet.hadronFlavour());
      double _heavySf = 1.0;
      double _heavyEff = 1.0;
      double _lightSf = 1.0;
      double _lightEff = 1.0;

      if(!subjetflag){

	_heavySf = reader.eval_auto_bounds("central",BTagEntry::FLAV_B,fabs(lvjet.Eta()),lvjet.Pt());
	if (shiftflag == 1 ||  BTagUncertUp ) _heavySf = reader.eval_auto_bounds("up",BTagEntry::FLAV_B,fabs(lvjet.Eta()),lvjet.Pt());
	else if (shiftflag == 2 ||  BTagUncertDown ) _heavySf = reader.eval_auto_bounds("down",BTagEntry::FLAV_B,fabs(lvjet.Eta()),lvjet.Pt());
	_heavyEff = mBtagCond.GetBtagEfficiency(lvjet.Et(), fabs(lvjet.Eta()), "DeepJet"+btagOP, year);
	
	if(_jetFlavor == 4){
	  _heavySf = reader.eval_auto_bounds("central",BTagEntry::FLAV_C,fabs(lvjet.Eta()),lvjet.Pt());
	  if (shiftflag == 1 ||  BTagUncertUp ) _heavySf = reader.eval_auto_bounds("up",BTagEntry::FLAV_C,fabs(lvjet.Eta()),lvjet.Pt());
	  else if (shiftflag == 2 ||  BTagUncertDown ) _heavySf = reader.eval_auto_bounds("down",BTagEntry::FLAV_C,fabs(lvjet.Eta()),lvjet.Pt());
	  _heavyEff = mBtagCond.GetCtagEfficiency(lvjet.Et(), fabs(lvjet.Eta()), "DeepJet"+btagOP, year);
	}
	
	_lightSf = reader.eval_auto_bounds("central",BTagEntry::FLAV_UDSG,fabs(lvjet.Eta()),lvjet.Pt());
	if (shiftflag == 3 || MistagUncertUp ) _lightSf = reader.eval_auto_bounds("up",BTagEntry::FLAV_UDSG,fabs(lvjet.Eta()),lvjet.Pt());
	else if (shiftflag == 4 ||  MistagUncertDown ) _lightSf = reader.eval_auto_bounds("down",BTagEntry::FLAV_UDSG,fabs(lvjet.Eta()),lvjet.Pt());
	_lightEff = mBtagCond.GetMistagRate(lvjet.Et(), fabs(lvjet.Eta()), "DeepJet"+btagOP, year);
	
      }
      else{
	
      	_heavySf = readerSJ.eval_auto_bounds("central",BTagEntry::FLAV_B,fabs(lvjet.Eta()),lvjet.Pt());
      	if (shiftflag == 1 ||  BTagUncertUp ) _heavySf = readerSJ.eval_auto_bounds("up",BTagEntry::FLAV_B,fabs(lvjet.Eta()),lvjet.Pt());
      	else if (shiftflag == 2 ||  BTagUncertDown ) _heavySf = readerSJ.eval_auto_bounds("down",BTagEntry::FLAV_B,fabs(lvjet.Eta()),lvjet.Pt());
      	_heavyEff = mBtagCond.GetBtagEfficiency(lvjet.Et(), fabs(lvjet.Eta()), "SJDeepCSV"+btagOP, year);

      	if(_jetFlavor == 4){
      	  _heavySf = readerSJ.eval_auto_bounds("central",BTagEntry::FLAV_C,fabs(lvjet.Eta()),lvjet.Pt());
      	  if (shiftflag == 1 ||  BTagUncertUp ) _heavySf = readerSJ.eval_auto_bounds("up",BTagEntry::FLAV_C,fabs(lvjet.Eta()),lvjet.Pt());
      	  else if (shiftflag == 2 ||  BTagUncertDown ) _heavySf = readerSJ.eval_auto_bounds("down",BTagEntry::FLAV_C,fabs(lvjet.Eta()),lvjet.Pt());
      	  _heavyEff = mBtagCond.GetCtagEfficiency(lvjet.Et(), fabs(lvjet.Eta()), "SJDeepCSV"+btagOP, year);
      	}

      	_lightSf = readerSJ.eval_auto_bounds("central",BTagEntry::FLAV_UDSG,fabs(lvjet.Eta()),lvjet.Pt());
      	if (shiftflag == 3 || MistagUncertUp ) _lightSf = readerSJ.eval_auto_bounds("up",BTagEntry::FLAV_UDSG,fabs(lvjet.Eta()),lvjet.Pt());
      	else if (shiftflag == 4 ||  MistagUncertDown ) _lightSf = readerSJ.eval_auto_bounds("down",BTagEntry::FLAV_UDSG,fabs(lvjet.Eta()),lvjet.Pt());
      	_lightEff = mBtagCond.GetMistagRate(lvjet.Et(), fabs(lvjet.Eta()), "SJDeepCSV"+btagOP, year);
      }

      SetSeed(abs(static_cast<int>(sin(jet.phi())*1e5)));

      //modifyBTagsWithSF modifies _isTagged ! need to Check ! -- Mar 19, 2019
      modifyBTagsWithSF(_isTagged, _jetFlavor, _heavySf, _heavyEff, _lightSf, _lightEff);
      
    } // end of btag scale factor corrections

    return _isTagged;
}
