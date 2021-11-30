

#include "TTT-singleLep/LJMet/interface/JetMETCorrHelper.h"

using namespace std;

JetMETCorrHelper::JetMETCorrHelper()
{
}

JetMETCorrHelper::JetMETCorrHelper(const edm::ParameterSet& iConfig)
{
    Initialize(iConfig);
}


void JetMETCorrHelper::Initialize(const edm::ParameterSet& iConfig){

    //JET CORRECTION  initialization
    std::cout << mLegend << "Initializing JetMETCorrHelper object." << std::endl;

    debug              = iConfig.getParameter<bool>("debug");

    isMc               = iConfig.getParameter<bool>("isMc");

    std::string JEC_txtfile              = iConfig.getParameter<edm::FileInPath>("JEC_txtfile").fullPath();
    std::string JERSF_txtfile            = iConfig.getParameter<edm::FileInPath>("JERSF_txtfile").fullPath();
    std::string JER_txtfile              = iConfig.getParameter<edm::FileInPath>("JER_txtfile").fullPath();
    std::string JERAK8_txtfile           = iConfig.getParameter<edm::FileInPath>("JERAK8_txtfile").fullPath();
    int year = 2018;
    if(JEC_txtfile.find("UL17") != std::string::npos) year = 2017;
    else if(JEC_txtfile.find("UL16") != std::string::npos) year = 2016;

    if(debug) std::cout << mLegend << "Using JEC files JEC_txtfile    : " << JEC_txtfile << std::endl;
    if(debug) std::cout << mLegend << "Using JEC files JERSF_txtfile  : " << JERSF_txtfile << std::endl;
    if(debug) std::cout << mLegend << "Using JEC files JER_txtfile    : " << JER_txtfile << std::endl;
    if(debug) std::cout << mLegend << "Using JEC files JERAK8_txtfile : " << JERAK8_txtfile << std::endl;
    std::cout << mLegend << "Setting JEC year to " << year << std::endl;

    mJetParStr["MCL1JetPar"] = iConfig.getParameter<edm::FileInPath>("MCL1JetPar").fullPath();
    mJetParStr["MCL2JetPar"] = iConfig.getParameter<edm::FileInPath>("MCL2JetPar").fullPath();
    mJetParStr["MCL3JetPar"] = iConfig.getParameter<edm::FileInPath>("MCL3JetPar").fullPath();
    mJetParStr["MCL1JetParAK8"] = iConfig.getParameter<edm::FileInPath>("MCL1JetParAK8").fullPath();
    mJetParStr["MCL2JetParAK8"] = iConfig.getParameter<edm::FileInPath>("MCL2JetParAK8").fullPath();
    mJetParStr["MCL3JetParAK8"] = iConfig.getParameter<edm::FileInPath>("MCL3JetParAK8").fullPath();
    mJetParStr["DataL1JetPar"] = iConfig.getParameter<edm::FileInPath>("DataL1JetPar").fullPath();
    mJetParStr["DataL2JetPar"] = iConfig.getParameter<edm::FileInPath>("DataL2JetPar").fullPath();
    mJetParStr["DataL3JetPar"] = iConfig.getParameter<edm::FileInPath>("DataL3JetPar").fullPath();
    mJetParStr["DataResJetPar"] = iConfig.getParameter<edm::FileInPath>("DataResJetPar").fullPath();
    mJetParStr["DataL1JetParAK8"] = iConfig.getParameter<edm::FileInPath>("DataL1JetParAK8").fullPath();
    mJetParStr["DataL2JetParAK8"] = iConfig.getParameter<edm::FileInPath>("DataL2JetParAK8").fullPath();
    mJetParStr["DataL3JetParAK8"] = iConfig.getParameter<edm::FileInPath>("DataL3JetParAK8").fullPath();
    mJetParStr["DataResJetParAK8"] = iConfig.getParameter<edm::FileInPath>("DataResJetParAK8").fullPath();

    if ( isMc ) jecUnc = std::shared_ptr<JetCorrectionUncertainty>( new JetCorrectionUncertainty(JEC_txtfile) );

    resolution = JME::JetResolution(JER_txtfile);
    resolutionAK8 = JME::JetResolution(JERAK8_txtfile);
    resolution_SF = JME::JetResolutionScaleFactor(JERSF_txtfile);

    if ( isMc ) {

      // Create the JetCorrectorParameter objects, the order does not matter.
      mStrJetCorPar["L3JetPar"]  = std::shared_ptr<JetCorrectorParameters>(new JetCorrectorParameters(mJetParStr["MCL3JetPar"]) );
      mStrJetCorPar["L2JetPar"]  = std::shared_ptr<JetCorrectorParameters>(new JetCorrectorParameters(mJetParStr["MCL2JetPar"]) );
      mStrJetCorPar["L1JetPar"]  = std::shared_ptr<JetCorrectorParameters>(new JetCorrectorParameters(mJetParStr["MCL1JetPar"]) );
      mStrJetCorPar["L3JetParAK8"]  = std::shared_ptr<JetCorrectorParameters>(new JetCorrectorParameters(mJetParStr["MCL3JetParAK8"]) );
      mStrJetCorPar["L2JetParAK8"]  = std::shared_ptr<JetCorrectorParameters>(new JetCorrectorParameters(mJetParStr["MCL2JetParAK8"]) );
      mStrJetCorPar["L1JetParAK8"]  = std::shared_ptr<JetCorrectorParameters>(new JetCorrectorParameters(mJetParStr["MCL1JetParAK8"]) );

      // Load the JetCorrectorParameter objects into a std::vector,
      // IMPORTANT: THE ORDER MATTERS HERE !!!!
      vPar.push_back(*mStrJetCorPar["L1JetPar"]);
      vPar.push_back(*mStrJetCorPar["L2JetPar"]);
      vPar.push_back(*mStrJetCorPar["L3JetPar"]);

      vParAK8.push_back(*mStrJetCorPar["L1JetParAK8"]);
      vParAK8.push_back(*mStrJetCorPar["L2JetParAK8"]);
      vParAK8.push_back(*mStrJetCorPar["L3JetParAK8"]);

      JetCorrector = std::shared_ptr<FactorizedJetCorrector>(new FactorizedJetCorrector(vPar) );
      JetCorrectorAK8 = std::shared_ptr<FactorizedJetCorrector>(new FactorizedJetCorrector(vParAK8) );

    }
    else if ( !isMc ) {
      // Create the JetCorrectorParameter objects, the order does not matter.

      std::string searchStr = "A_V";
      if(year == 2018){
	mEraReplaceStr["A"] = "A_V";
	mEraReplaceStr["B"] = "B_V";
	mEraReplaceStr["C"] = "C_V";
	mEraReplaceStr["D"] = "D_V";
      }else if(year == 2017){
	searchStr = "B_V";
	mEraReplaceStr["B"] = "B_V";
	mEraReplaceStr["C"] = "C_V";
	mEraReplaceStr["D"] = "D_V";
	mEraReplaceStr["E"] = "E_V";
	mEraReplaceStr["F"] = "F_V";
      }else{ // 2016
	searchStr = "BCD_V";
	mEraReplaceStr["BCD"] = "BCD_V";
	mEraReplaceStr["EF"] = "EF_V";
	mEraReplaceStr["GH"] = "GH_V"; // I don't think this available yet
      }

      for (std::map<std::string,std::string>::iterator it=mEraReplaceStr.begin();it!=mEraReplaceStr.end();it++){

          std::string era = it->first;
          std::string replaceStr = it->second;

          //Fetch the text files
          mEraJetParStr[era]["DataL1JetParByIOV"]  = std::regex_replace(mJetParStr["DataL1JetPar"],std::regex(searchStr), replaceStr);
          mEraJetParStr[era]["DataL2JetParByIOV"]  = std::regex_replace(mJetParStr["DataL2JetPar"],std::regex(searchStr), replaceStr);
          mEraJetParStr[era]["DataL3JetParByIOV"]  = std::regex_replace(mJetParStr["DataL3JetPar"],std::regex(searchStr), replaceStr);
          mEraJetParStr[era]["DataResJetParByIOV"]  = std::regex_replace(mJetParStr["DataResJetPar"],std::regex(searchStr), replaceStr);

          mEraJetParStr[era]["DataL1JetParAK8ByIOV"]  = std::regex_replace(mJetParStr["DataL1JetParAK8"],std::regex(searchStr), replaceStr);
          mEraJetParStr[era]["DataL2JetParAK8ByIOV"]  = std::regex_replace(mJetParStr["DataL2JetParAK8"],std::regex(searchStr), replaceStr);
          mEraJetParStr[era]["DataL3JetParAK8ByIOV"]  = std::regex_replace(mJetParStr["DataL3JetParAK8"],std::regex(searchStr), replaceStr);
          mEraJetParStr[era]["DataResJetParAK8ByIOV"]  = std::regex_replace(mJetParStr["DataResJetParAK8"],std::regex(searchStr), replaceStr);

          if(debug) std::cout << mLegend << "Using JEC files DataL1JetParByIOV : era "+era+": " <<  mEraJetParStr[era]["DataL1JetParByIOV"] << std::endl;
          if(debug) std::cout << mLegend << "Using JEC files DataL2JetParByIOV : era "+era+": " <<  mEraJetParStr[era]["DataL2JetParByIOV"] << std::endl;
          if(debug) std::cout << mLegend << "Using JEC files DataL3JetParByIOV : era "+era+": " <<  mEraJetParStr[era]["DataL3JetParByIOV"] << std::endl;
          if(debug) std::cout << mLegend << "Using JEC files DataResJetParByIOV : era "+era+": " <<  mEraJetParStr[era]["DataResJetParByIOV"] << std::endl;

          if(debug) std::cout << mLegend << "Using JEC files DataL1JetParAK8ByIOV : era "+era+": " <<  mEraJetParStr[era]["DataL1JetParAK8ByIOV"] << std::endl;
          if(debug) std::cout << mLegend << "Using JEC files DataL2JetParAK8ByIOV : era "+era+": " <<  mEraJetParStr[era]["DataL2JetParAK8ByIOV"] << std::endl;
          if(debug) std::cout << mLegend << "Using JEC files DataL3JetParAK8ByIOV : era "+era+": " <<  mEraJetParStr[era]["DataL3JetParAK8ByIOV"] << std::endl;
          if(debug) std::cout << mLegend << "Using JEC files DataResJetParAK8ByIOV : era "+era+": " <<  mEraJetParStr[era]["DataResJetParAK8ByIOV"] << std::endl;


          mEra_mStrJetCorPar[era]["ResJetPar"] = std::shared_ptr<JetCorrectorParameters>( new JetCorrectorParameters(mEraJetParStr[era]["DataResJetParByIOV"]) );
          mEra_mStrJetCorPar[era]["L3JetPar"]  = std::shared_ptr<JetCorrectorParameters>( new JetCorrectorParameters(mEraJetParStr[era]["DataL3JetParByIOV"]) );
          mEra_mStrJetCorPar[era]["L2JetPar"]  = std::shared_ptr<JetCorrectorParameters>( new JetCorrectorParameters(mEraJetParStr[era]["DataL2JetParByIOV"]) );
          mEra_mStrJetCorPar[era]["L1JetPar"]  = std::shared_ptr<JetCorrectorParameters>( new JetCorrectorParameters(mEraJetParStr[era]["DataL1JetParByIOV"]) );
          mEra_mStrJetCorPar[era]["ResJetParAK8"] = std::shared_ptr<JetCorrectorParameters>( new JetCorrectorParameters(mEraJetParStr[era]["DataResJetParAK8ByIOV"]) );
          mEra_mStrJetCorPar[era]["L3JetParAK8"]  = std::shared_ptr<JetCorrectorParameters>( new JetCorrectorParameters(mEraJetParStr[era]["DataL3JetParAK8ByIOV"]) );
          mEra_mStrJetCorPar[era]["L2JetParAK8"]  = std::shared_ptr<JetCorrectorParameters>( new JetCorrectorParameters(mEraJetParStr[era]["DataL2JetParAK8ByIOV"]) );
          mEra_mStrJetCorPar[era]["L1JetParAK8"]  = std::shared_ptr<JetCorrectorParameters>( new JetCorrectorParameters(mEraJetParStr[era]["DataL1JetParAK8ByIOV"]) );

          // Load the JetCorrectorParameter objects into a std::vector,
          // IMPORTANT: THE ORDER MATTERS HERE !!!!
          mEraVPar[era].push_back(*mEra_mStrJetCorPar[era]["L1JetPar"]);
          mEraVPar[era].push_back(*mEra_mStrJetCorPar[era]["L2JetPar"]);
          mEraVPar[era].push_back(*mEra_mStrJetCorPar[era]["L3JetPar"]);
          mEraVPar[era].push_back(*mEra_mStrJetCorPar[era]["ResJetPar"]);
          mEraVParAK8[era].push_back(*mEra_mStrJetCorPar[era]["L1JetParAK8"]);
          mEraVParAK8[era].push_back(*mEra_mStrJetCorPar[era]["L2JetParAK8"]);
          mEraVParAK8[era].push_back(*mEra_mStrJetCorPar[era]["L3JetParAK8"]);
          mEraVParAK8[era].push_back(*mEra_mStrJetCorPar[era]["ResJetParAK8"]);

          mEraFacJetCorr[era] = std::shared_ptr<FactorizedJetCorrector>( new FactorizedJetCorrector(mEraVPar[era]) );
	  mEraFacJetCorrAK8[era] = std::shared_ptr<FactorizedJetCorrector> (new FactorizedJetCorrector(mEraVParAK8[era]) );

      }

    }


}


//JET CORRECTION HELPER METHODS
void JetMETCorrHelper::SetFacJetCorr(edm::EventBase const & event)
{
/*
 *This function takes an event, looks up the correct JEC file, and produces the correct JetCorrector for JEC corrections.
 *JEC is run number dependent.
 *This first gets the run number for the event
 *It then pulls in the corersponding spring16_V10* file
 *Then uses that.
 *
 * This is called in singleLepEventSelector
 * */


  int iRun   = event.id().run();
  // run # get in https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/Era/Prompt/

  if(iRun <= 276812){
  	if(debug) std::cout << "\t\t\t using 2016 JEC for era BCD "<< std::endl;
  	JetCorrector = mEraFacJetCorr["BCD"];
  	JetCorrectorAK8 = mEraFacJetCorrAK8["BCD"];
  }
  else if(iRun <= 278801){
  	if(debug) std::cout << "\t\t\t using 2016 JEC for era EF "<< std::endl;
  	JetCorrector = mEraFacJetCorr["EF"];
  	JetCorrectorAK8 = mEraFacJetCorrAK8["EF"];
  }
  else if(iRun <= 284045){
  	if(debug) std::cout << "\t\t\t using 2016 JEC for era GH "<< std::endl;
  	JetCorrector = mEraFacJetCorr["GH"];
  	JetCorrectorAK8 = mEraFacJetCorrAK8["GH"];
  }
  else if(iRun <= 299330){
  	if(debug) std::cout << "\t\t\t using 2017 JEC for era B "<< std::endl;
  	JetCorrector = mEraFacJetCorr["B"];
  	JetCorrectorAK8 = mEraFacJetCorrAK8["B"];
  }
  else if(iRun <= 302029){
  	if(debug) std::cout << "\t\t\t using 2017 JEC for era C "<< std::endl;
  	JetCorrector = mEraFacJetCorr["C"];
  	JetCorrectorAK8 = mEraFacJetCorrAK8["C"];
  }
  else if(iRun <=303434){
        if(debug) std::cout << "\t\t\t using 2017 JEC for era D "<< std::endl;
        JetCorrector = mEraFacJetCorr["D"];
        JetCorrectorAK8 = mEraFacJetCorrAK8["D"];
  }
  else if(iRun <= 304827){
  	if(debug) std::cout << "\t\t\t using 2017 JEC for era E "<< std::endl;
  	JetCorrector = mEraFacJetCorr["E"];
  	JetCorrectorAK8 = mEraFacJetCorrAK8["E"];
  	}
  else if(iRun <= 306463){
        if(debug) std::cout << "\t\t\t using 2017 JEC for era F "<< std::endl;
  	JetCorrector = mEraFacJetCorr["F"];
  	JetCorrectorAK8 = mEraFacJetCorrAK8["F"];
  }
  else if(iRun <= 316995){
  	if(debug) std::cout << "\t\t\t using 2018 JEC for era A "<< std::endl;
  	JetCorrector = mEraFacJetCorr["A"];
  	JetCorrectorAK8 = mEraFacJetCorrAK8["A"];
  }
  else if(iRun <= 319312){
  	if(debug) std::cout << "\t\t\t using 2018 JEC for era B "<< std::endl;
  	JetCorrector = mEraFacJetCorr["B"];
  	JetCorrectorAK8 = mEraFacJetCorrAK8["B"];
  }
  else if(iRun <= 320393){
  	if(debug) std::cout << "\t\t\t using 2018 JEC for era C "<< std::endl;
  	JetCorrector = mEraFacJetCorr["C"];
  	JetCorrectorAK8 = mEraFacJetCorrAK8["C"];
  }
  else if(iRun <= 325273){
  	if(debug) std::cout << "\t\t\t using 2018 JEC for era D "<< std::endl;
  	JetCorrector = mEraFacJetCorr["D"];
  	JetCorrectorAK8 = mEraFacJetCorrAK8["D"];
    }

}

TLorentzVector JetMETCorrHelper::correctJet(const pat::Jet & jet,
                                                 edm::Event const & event,
                                                 edm::EDGetTokenT<double> rhoJetsToken,
                                                 bool doAK8Corr,
                                                 bool reCorrectJet,
                                                 unsigned int syst)
{

  pat::Jet correctedJet = correctJetReturnPatJet(jet, event, rhoJetsToken, doAK8Corr, reCorrectJet, syst);

  TLorentzVector jetP4;
  jetP4.SetPtEtaPhiM(correctedJet.pt(), correctedJet.eta(),correctedJet.phi(), correctedJet.mass() ); // Should this use SetPtEtaPhiE ? -- Mar 19, 2019.


  return jetP4;
}

pat::Jet JetMETCorrHelper::correctJetReturnPatJet(const pat::Jet & jet,
                                                       edm::Event const & event,
                                                       edm::EDGetTokenT<double> rhoJetsToken,
                                                       bool doAK8Corr,
                                                       bool reCorrectJet,
                                                       unsigned int syst)
{

  // JES and JES systematics
  pat::Jet correctedJet;
  if (reCorrectJet) correctedJet = jet.correctedJet(0);                 //copy original jet
  else correctedJet = jet;                                 //copy default corrected jet

  double ptscale = 1.0;
  double unc = 1.0;
  double pt = correctedJet.pt();
  double correction = 1.0;

  edm::Handle<double> rhoHandle;
  event.getByToken(rhoJetsToken, rhoHandle);
  double rho = std::max(*(rhoHandle.product()), 0.0);

  if ( isMc ){

    if (reCorrectJet) {
      // We need to undo the default corrections and then apply the new ones

      double pt_raw = jet.correctedJet(0).pt();

      if (doAK8Corr){
		JetCorrectorAK8->setJetEta(jet.eta());
		JetCorrectorAK8->setJetPt(pt_raw);
		JetCorrectorAK8->setJetA(jet.jetArea());
		JetCorrectorAK8->setRho(rho);

		try{
		  correction = JetCorrectorAK8->getCorrection();
		}
		catch(...){
		  std::cout << mLegend << "WARNING! Exception thrown by JetCorrectionUncertainty!" << std::endl;
		  std::cout << mLegend << "WARNING! Possibly, trying to correct a jet/MET outside correction range." << std::endl;
		  std::cout << mLegend << "WARNING! Jet/MET will remain uncorrected." << std::endl;
		}
      }

      else{
		JetCorrector->setJetEta(jet.eta());
		JetCorrector->setJetPt(pt_raw);
		JetCorrector->setJetA(jet.jetArea());
		JetCorrector->setRho(rho);

		try{
		  correction = JetCorrector->getCorrection();
		}
		catch(...){
		  std::cout << mLegend << "WARNING! Exception thrown by JetCorrectionUncertainty!" << std::endl;
		  std::cout << mLegend << "WARNING! Possibly, trying to correct a jet/MET outside correction range." << std::endl;
		  std::cout << mLegend << "WARNING! Jet/MET will remain uncorrected." << std::endl;
		}
      }

      correctedJet.scaleEnergy(correction);
      pt = correctedJet.pt();

    }

    Variation JERsystematic = Variation::NOMINAL;
    if( syst==3) JERsystematic = Variation::UP;
    if( syst==4) JERsystematic = Variation::DOWN;

    JME::JetParameters parameters;
    parameters.setJetPt(pt);
    parameters.setJetEta(correctedJet.eta());
    parameters.setRho(rho);
    double res = 0.0;
    if(doAK8Corr) res = resolutionAK8.getResolution(parameters);
    else res = resolution.getResolution(parameters);
    double factor = resolution_SF.getScaleFactor(parameters,JERsystematic) - 1;

    const reco::GenJet * genJet = jet.genJet();
    bool smeared = false;
    if(genJet){
      double deltaPt = fabs(genJet->pt() - pt);
      double deltaR = reco::deltaR(genJet->p4(),correctedJet.p4());
      if (deltaR < ((doAK8Corr) ? 0.4 : 0.2) && deltaPt <= 3*pt*res){
		double gen_pt = genJet->pt();
		double reco_pt = pt;
		double deltapt = (reco_pt - gen_pt) * factor;
		ptscale = max(0.0, (reco_pt + deltapt) / reco_pt);
		smeared = true;
      }
    }
    if (!smeared && factor>0) {
      JERrand.SetSeed(abs(static_cast<int>(jet.phi()*1e4)));
      ptscale = max(0.0, JERrand.Gaus(pt,sqrt(factor*(factor+2))*res*pt)/pt);
    }

    if (  syst==1 || syst==2) {
      jecUnc->setJetEta(jet.eta());
      jecUnc->setJetPt(pt*ptscale);

      if ( syst==1) {
	try{
	  unc = jecUnc->getUncertainty(true);
	}
	catch(...){ // catch all exceptions. Jet Uncertainty tool throws when binning out of range
	  std::cout << mLegend << "WARNING! Exception thrown by JetCorrectionUncertainty!" << std::endl;
	  std::cout << mLegend << "WARNING! Possibly, trying to correct a jet/MET outside correction range." << std::endl;
	  std::cout << mLegend << "WARNING! Jet/MET will remain uncorrected." << std::endl;
	  unc = 0.0;
	}
	unc = 1 + unc;
      }
      else {
	try{
	  unc = jecUnc->getUncertainty(false);
	}
	catch(...){
	  std::cout << mLegend << "WARNING! Exception thrown by JetCorrectionUncertainty!" << std::endl;
	  std::cout << mLegend << "WARNING! Possibly, trying to correct a jet/MET outside correction range." << std::endl;
	  std::cout << mLegend << "WARNING! Jet/MET will remain uncorrected." << std::endl;
	  unc = 0.0;
	}
	unc = 1 - unc;
      }

      if (pt*ptscale < 10.0 && ( syst==1)) unc = 2.0;
      if (pt*ptscale < 10.0 && ( syst==2)) unc = 0.01;

    }

    correctedJet.scaleEnergy(unc*ptscale);

  }
  else if (!isMc) {

    if (reCorrectJet) {

      double pt_raw = jet.correctedJet(0).pt();
      // We need to undo the default corrections and then apply the new ones

      if (doAK8Corr){
		JetCorrectorAK8->setJetEta(jet.eta());
		JetCorrectorAK8->setJetPt(pt_raw);
		JetCorrectorAK8->setJetA(jet.jetArea());
		JetCorrectorAK8->setRho(rho);

		try{
		  correction = JetCorrectorAK8->getCorrection();
		}
		catch(...){
		  std::cout << mLegend << "WARNING! Exception thrown by JetCorrectionUncertainty!" << std::endl;
		  std::cout << mLegend << "WARNING! Possibly, trying to correct a jet/MET outside correction range." << std::endl;
		  std::cout << mLegend << "WARNING! Jet/MET will remain uncorrected." << std::endl;
		}
      }

      else{
		JetCorrector->setJetEta(jet.eta());
		JetCorrector->setJetPt(pt_raw);
		JetCorrector->setJetA(jet.jetArea());
		JetCorrector->setRho(rho);

		try{
		  correction = JetCorrector->getCorrection();
		}
		catch(...){
		  std::cout << mLegend << "WARNING! Exception thrown by JetCorrectionUncertainty!" << std::endl;
		  std::cout << mLegend << "WARNING! Possibly, trying to correct a jet/MET outside correction range." << std::endl;
		  std::cout << mLegend << "WARNING! Jet/MET will remain uncorrected." << std::endl;
		}
      }
      correctedJet.scaleEnergy(correction);
      pt = correctedJet.pt();

    }
  }

  return correctedJet;
}

TLorentzVector JetMETCorrHelper::correctMet(const pat::MET & met,
                                                 edm::Event const & event,
                                                 edm::EDGetTokenT<double> rhoJetsToken,
                                                 std::vector<edm::Ptr<pat::Jet>> vAllJets,
                                                 bool reCorrectjet,
                                                 unsigned int syst,
                                                 bool useHF)
{
    double correctedMET_px = met.uncorPx();
    double correctedMET_py = met.uncorPy();
    if ( reCorrectjet ) {
        for (std::vector<edm::Ptr<pat::Jet> >::const_iterator ijet = vAllJets.begin(); ijet != vAllJets.end(); ++ijet) {
            if (!useHF && fabs((**ijet).eta())>2.6) continue;
            TLorentzVector lv = correctJetForMet(**ijet, event, rhoJetsToken, syst);
            correctedMET_px += lv.Px();
            correctedMET_py += lv.Py();
        }
    }
    else {
        correctedMET_px = met.px();
        correctedMET_py = met.py();
    }

    TLorentzVector correctedMET_p4_temp;

    correctedMET_p4_temp.SetPxPyPzE(correctedMET_px, correctedMET_py, 0, sqrt(correctedMET_px*correctedMET_px+correctedMET_py*correctedMET_py));

    return correctedMET_p4_temp;
}

TLorentzVector JetMETCorrHelper::correctJetForMet(const pat::Jet & jet,
                                                       edm::Event const & event,
                                                       edm::EDGetTokenT<double> rhoJetsToken,
                                                       unsigned int syst)
{

    TLorentzVector jetP4, offJetP4;
    jetP4.SetPtEtaPhiM(0.000001,1.,1.,0.000001);

    if ( jet.chargedEmEnergyFraction() + jet.neutralEmEnergyFraction() > 0.90 ) {
        return jetP4-jetP4;
    }

    pat::Jet correctedJet = jet.correctedJet(0);                 //copy original jet

    jetP4.SetPtEtaPhiM(correctedJet.pt(),correctedJet.eta(),correctedJet.phi(),correctedJet.mass());

    const std::vector<reco::CandidatePtr> & cands = jet.daughterPtrVector();
    for ( std::vector<reco::CandidatePtr>::const_iterator cand = cands.begin(); cand != cands.end(); ++cand ) {
        const reco::PFCandidate *pfcand = dynamic_cast<const reco::PFCandidate *>(cand->get());
        const reco::Candidate *mu = (pfcand != 0 ? ( pfcand->muonRef().isNonnull() ? pfcand->muonRef().get() : 0) : cand->get());
        if ( mu != 0 && (mu->isGlobalMuon() || mu->isStandAloneMuon()) ) {
	        TLorentzVector muonP4;
            muonP4.SetPtEtaPhiM((*cand)->pt(),(*cand)->eta(),(*cand)->phi(),(*cand)->mass());
	        jetP4 -= muonP4;
        }
    }
    offJetP4 = jetP4;

    double ptscale = 1.0;
    double unc = 1.0;
    double pt = correctedJet.pt();
    std::vector<float> corrVec;

    edm::Handle<double> rhoHandle;
    event.getByToken(rhoJetsToken, rhoHandle);
    double rho = std::max(*(rhoHandle.product()), 0.0);

    if ( isMc ){

        JetCorrector->setJetEta(correctedJet.eta());
  		JetCorrector->setJetPt(pt);
        JetCorrector->setJetA(jet.jetArea());
  		JetCorrector->setRho(rho);

        try{
    	    corrVec = JetCorrector->getSubCorrections();
        }
  		catch(...){
    	    std::cout << mLegend << "WARNING! Exception thrown by JetCorrectionUncertainty!" << std::endl;
    	    std::cout << mLegend << "WARNING! Possibly, trying to correct a jet/MET outside correction range." << std::endl;
    	    std::cout << mLegend << "WARNING! Jet/MET will remain uncorrected." << std::endl;
        }

        jetP4 *= corrVec[corrVec.size()-1];
        offJetP4 *= corrVec[0];
        pt = jetP4.Pt();

        Variation JERsystematic = Variation::NOMINAL;
        if(syst==3) JERsystematic = Variation::UP;
        if(syst==4) JERsystematic = Variation::DOWN;

        JME::JetParameters parameters;
        parameters.setJetPt(pt);
        parameters.setJetEta(jetP4.Eta());
        parameters.setRho(rho);
        double res = 0.0;
        res = resolution.getResolution(parameters);
        double factor = resolution_SF.getScaleFactor(parameters,JERsystematic) - 1;

        const reco::GenJet * genJet = jet.genJet();
        bool smeared = false;
        if(genJet){
            TLorentzVector genP4;
            genP4.SetPtEtaPhiE(genJet->pt(),genJet->eta(),genJet->phi(),genJet->energy());
            double deltaPt = fabs(genJet->pt() - pt);
            double deltaR = jetP4.DeltaR(genP4);
            if (deltaR < 0.2 && deltaPt <= 3*pt*res){
               double gen_pt = genJet->pt();
               double reco_pt = pt;
               double deltapt = (reco_pt - gen_pt) * factor;
               ptscale = max(0.0, (reco_pt + deltapt) / reco_pt);
               smeared = true;
            }
        }
        if (!smeared && factor>0) {
          JERrand.SetSeed(abs(static_cast<int>(jet.phi()*1e4)));
          ptscale = max(0.0, JERrand.Gaus(pt,sqrt(factor*(factor+2))*res*pt)/pt);
        }

        if ( syst==1 || syst==2) {
            jecUnc->setJetEta(jetP4.Eta());
            jecUnc->setJetPt(jetP4.Pt()*ptscale);

            if (syst==1) {
                try{
                    unc = jecUnc->getUncertainty(true);
                }
                catch(...){ // catch all exceptions. Jet Uncertainty tool throws when binning out of range
                    std::cout << mLegend << "WARNING! Exception thrown by JetCorrectionUncertainty!" << std::endl;
                    std::cout << mLegend << "WARNING! Possibly, trying to correct a jet/MET outside correction range." << std::endl;
                    std::cout << mLegend << "WARNING! Jet/MET will remain uncorrected." << std::endl;
                    unc = 0.0;
                }
                unc = 1 + unc;
            }
            else {
                try{
                    unc = jecUnc->getUncertainty(false);
                }
                catch(...){
                    std::cout << mLegend << "WARNING! Exception thrown by JetCorrectionUncertainty!" << std::endl;
                    std::cout << mLegend << "WARNING! Possibly, trying to correct a jet/MET outside correction range." << std::endl;
                    std::cout << mLegend << "WARNING! Jet/MET will remain uncorrected." << std::endl;
                    unc = 0.0;
                }
                unc = 1 - unc;
            }
            if (jetP4.Pt()*ptscale < 10.0 && (syst==1)) unc = 2.0;
            if (jetP4.Pt()*ptscale < 10.0 && (syst==2)) unc = 0.01;

        }

    }
    else if (!isMc) {

        JetCorrector->setJetEta(correctedJet.eta());
        JetCorrector->setJetPt(pt);
        JetCorrector->setJetA(jet.jetArea());
        JetCorrector->setRho(rho);

        try{
    	    corrVec = JetCorrector->getSubCorrections();
        }
        catch(...){
           std::cout << mLegend << "WARNING! Exception thrown by JetCorrectionUncertainty!" << std::endl;
           std::cout << mLegend << "WARNING! Possibly, trying to correct a jet/MET outside correction range." << std::endl;
           std::cout << mLegend << "WARNING! Jet/MET will remain uncorrected." << std::endl;
        }


        jetP4 *= corrVec[corrVec.size()-1];
        offJetP4 *= corrVec[0];
        pt = jetP4.Pt();

    }

    jetP4 *= unc*ptscale;
    offJetP4 *= unc*ptscale;
    if (jetP4.Pt()<=15.) {
        offJetP4 = jetP4;
    }

    return offJetP4-jetP4;
}
