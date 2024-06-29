#!/bin/sh

fileName=${1}
inputDir=${2}
outputDir=${3}

# Enter environment

source /cvmfs/cms.cern.ch/cmsset_default.sh
scramv1 project CMSSW CMSSW_13_3_0
cd CMSSW_13_3_0/src/
eval `scramv1 runtime -sh`
cd -

python3 step3.py -f $inputDir 

xrdcp -vpf $fileName $outputDir 
rm $fileName
