#ifndef LJMet_interface_DummyCalc_h
#define LJMet_interface_DummyCalc_h

#include "TTT-singleLep/LJMet/interface/BaseCalc.h"
#include "TTT-singleLep/LJMet/interface/LjmetFactory.h"
#include "TTT-singleLep/LJMet/interface/LjmetEventContent.h"

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
