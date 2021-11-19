# this script runs the condor job for applying ABCDnn to step3
#!/bin/sh

condorDir=${1}
sampleName=${2}
sampleDir=${3}
eosUserName=${4}
tag=${5}

xrdcp -s root://cmseos.fnal.gov//store/user/$eosUserName/ABCDnn.tgz .
tar -xf ABCDnn.tgz
rm ABCDnn.tgz

cd CMSSW_9_4_6_patch1/src/TTT-singleLep/ABCDnn/

source /cvmfs/cms.cern.ch/cmsset_default.csh
cmsenv
source /cvmfs/sft.cern.ch/lcg/views/LCG_98/x86_64-centos7-gcc8-opt/setup.csh

python remote_abcdnn.py 
