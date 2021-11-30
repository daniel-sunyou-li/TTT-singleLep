#ifndef FWLJMET_LJMet_interface_TestCalc_h
#define FWLJMET_LJMet_interface_TestCalc_h

#include "FWLJMET/LJMET/interface/BaseCalc.h"
#include "FWLJMET/LJMET/interface/LjmetFactory.h"
#include "FWLJMET/LJMET/interface/LjmetEventContent.h"

class LjmetFactory;

class TestCalc : public BaseCalc {
public:
    TestCalc();
    virtual ~TestCalc();
    virtual int BeginJob(edm::ConsumesCollector && iC);
    virtual int AnalyzeEvent(edm::Event const & event, BaseEventSelector * selector);
    virtual int EndJob(){return 0;};
    
private:
	bool debug;

    //edm::EDGetTokenT<pat::ElectronCollection>   electronsToken;

};



#endif
