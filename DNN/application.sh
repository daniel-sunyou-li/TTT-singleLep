#!/bin/sh

condorDir=${1}
fileName=${2}
outputDir=${3}
eosUserName=${4}
tag=${5}

xrdcp -s root://cmseos.fnal.gov//store/user/$eosUserName/CMSSW106_ttt.tgz .
tar -xf CMSSW106_ttt.tgz
rm CMSSW106_ttt.tgz

mv *.tf CMSSW_10_6_19/src/TTT-singleLep/DNN/
mv *.json CMSSW_10_6_19/src/TTT-singleLep/DNN/

cd CMSSW_10_6_19/src/TTT-singleLep/DNN/

source /cvmfs/cms.cern.ch/cmsset_default.sh
source /cvmfs/sft.cern.ch/lcg/views/LCG_97/x86_64-centos7-gcc8-opt/setup.sh

python step3.py -i $condorDir -f $fileName -o $outputDir -t $tag

xrdcp -f $fileName\.root root://cmseos.fnal.gov//store/user/$eosUserName/$outputDir
