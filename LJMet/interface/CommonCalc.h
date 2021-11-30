#ifndef LJMet_interface_CommonCalc_h
#define LJMet_interface_CommonCalc_h

/*
  Calculator for the most common event variables
   Author: Gena Kukartsev, 2012
*/



#include <iostream>
#include "TTT-singleLep/LJMet/interface/BaseCalc.h"
#include "TTT-singleLep/LJMet/interface/LjmetFactory.h"
#include "TTT-singleLep/LJMet/interface/LjmetEventContent.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 

#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"


class LjmetFactory;


class CommonCalc : public BaseCalc{
  
public:
  
  CommonCalc(){};
  virtual ~CommonCalc(){}

  virtual int BeginJob(edm::ConsumesCollector && iC);
  virtual int AnalyzeEvent(edm::Event const & event, BaseEventSelector * selector);
  virtual int EndJob(){return 0;}

  
private:
    edm::EDGetTokenT<double>                           L1prefiringToken;
    edm::EDGetTokenT<double>                           L1prefiringToken_up;
    edm::EDGetTokenT<double>                           L1prefiringToken_down;

};





#endif