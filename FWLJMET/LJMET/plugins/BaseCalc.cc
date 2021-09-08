/*************************************************************
Updated: Daniel Li 09-08-2021
v 1.2
*************************************************************/

#include "FWLJMET/LJMet/interface/BaseCalc.h"
#include "FWLJMET/LJMet/interface/LjmetEventContent.h"

BaseCalc::BaseCalc():
mName(""),
mLegend("")
{
}

void BaseCalc::SetHistogram(std::string name, int nbins, double low, double high)
{
    mpEc->SetHistogram(mName, name, nbins, low, high);
}

void BaseCalc::SetHistValue(std::string name, double value)
{
    mpEc->SetHistValue(mName, name, value);
}

void BaseCalc::SetValue(std::string name, bool value)
{
    std::string _name = name + "_" + mName;
    mpEc->SetValue(_name, value);
}

void BaseCalc::SetValue(std::string name, int value)
{
    std::string _name = name + "_" + mName;
    mpEc->SetValue(_name, value);
}

void BaseCalc::SetValue(std::string name, long long value)
{
    std::string _name = name + "_" + mName;
    mpEc->SetValue(_name, value);
}

void BaseCalc::SetValue(std::string name, double value)
{
    std::string _name = name + "_" + mName;
    mpEc->SetValue(_name, value);
}

void BaseCalc::SetValue(std::string name, std::vector<bool> value)
{
    std::string _name = name + "_" + mName;
    mpEc->SetValue(_name, value);
}

void BaseCalc::SetValue(std::string name, std::vector<int> value)
{
    std::string _name = name + "_" + mName;
    mpEc->SetValue(_name, value);
}

void BaseCalc::SetValue(std::string name, std::vector<double> value)
{
    std::string _name = name + "_" + mName;
    mpEc->SetValue(_name, value);
}

void BaseCalc::SetValue(std::string name, std::vector<std::string> value)
{
  std::string _name = name + "_" + mName;
  mpEc->SetValue(_name, value);
}

void BaseCalc::init()
{
    mLegend = "[" + mName + "]: ";
    std::cout << mLegend << "registering " << mName << std::endl;
}
