#!/bin/sh

fileName=${1}
inputDir=${2}
outputDir=${3}

# Enter environment

source /cvmfs/cms.cern.ch/cmsset_default.sh
source /cvmfs/sft.cern.ch/lcg/views/LCG_97/x86_64-centos7-gcc8-opt/setup.sh
export SCRAM_ARCH=slc7_amd64_gcc700
scramv1 project CMSSW CMSSW_10_6_29
cd CMSSW_10_6_29
cd -

python step3.py -f $inputDir 

xrdcp -vpf $fileName $outputDir 
rm $fileName
