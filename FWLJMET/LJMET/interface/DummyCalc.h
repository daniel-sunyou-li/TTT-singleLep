#ifndef FWLJMET_LJMet_interface_DummyCalc_h
#define FWLJMET_LJMet_interface_DummyCalc_h

#include "FWLJMET/LJMET/interface/BaseCalc.h"
#include "FWLJMET/LJMET/interface/LjmetFactory.h"
#include "FWLJMET/LJMET/interface/LjmetEventContent.h"

class LjmetFactory;

class DummyCalc : public BaseCalc {
public:
    DummyCalc();
    virtual ~DummyCalc();
    virtual int BeginJob(edm::ConsumesCollector && iC);
    virtual int AnalyzeEvent(edm::Event const & event, BaseEventSelector * selector);
    virtual int EndJob(){return 0;};
    
private:
	bool debug;

};



#endif
