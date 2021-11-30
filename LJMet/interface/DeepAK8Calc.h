#ifndef LJMet_interface_DeepAK8Calc_h
#define LJMet_interface_DeepAK8Calc_h


#include <iostream>
#include <vector>

#include "TTT-singleLep/LJMet/interface/BaseCalc.h"
#include "TTT-singleLep/LJMet/interface/LjmetEventContent.h"
#include "TTT-singleLep/LJMet/interface/LjmetFactory.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "FWCore/PythonParameterSet/interface/PyBind11ProcessDesc.h"
//#include "TTT-singleLep/LJMET/interface/VVString.h"

// CMS
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "PhysicsTools/CandUtils/interface/EventShapeVariables.h"
#include "PhysicsTools/CandUtils/interface/Thrust.h"

#include "TLorentzVector.h" 



class DeepAK8Calc : public BaseCalc {
    //
    // DeepAK8 class for all calculators
    //
    //

    
 public:
    DeepAK8Calc(){};
    virtual ~DeepAK8Calc() { }
    DeepAK8Calc(const DeepAK8Calc &); // stop default
    std::string GetName() { return mName; }
    virtual int BeginJob(edm::ConsumesCollector && iC);
    virtual int ProduceEvent(edm::EventBase const & event, BaseEventSelector * selector) { return 0; }
    virtual int AnalyzeEvent(edm::Event const & event, BaseEventSelector * selector);
    virtual int EndJob();

 private:

};

#endif
