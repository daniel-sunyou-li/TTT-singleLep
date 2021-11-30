#include "FWLJMET/LJMET/interface/DummyCalc.h"


DummyCalc::DummyCalc()
{
}

DummyCalc::~DummyCalc()
{
}

int DummyCalc::BeginJob(edm::ConsumesCollector && iC)
{
	debug = mPset.getParameter<bool>("debug");

    return 0;
}

int DummyCalc::AnalyzeEvent(edm::Event const & event, BaseEventSelector * selector)
{     
	if(debug)std::cout << "Processing Event in DummyCalc::AnalyzeEvent" << std::endl;

	// ----- Get objects from the selector -----
    //std::vector<edm::Ptr<pat::Electron> >       const & vSelectedElectrons = selector->GetSelectedElectrons();

    // ----- Event kinematics -----
    //int _nSelElectrons   = (int)vSelElectrons.size();

    // Electron
    //std::vector <double> elPt;

    //
    //_____Electrons______
    //
    //for (std::vector<edm::Ptr<pat::Electron> >::const_iterator iel = vSelElectrons.begin(); iel != vSelElectrons.end(); iel++){
    //    elPt     . push_back((*iel)->pt()); //Must check: why ecalDrivenMomentum?
    //}

    //SetValue("elPt"     , elPt);
    
    return 0;
}
