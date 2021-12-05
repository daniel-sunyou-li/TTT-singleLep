#!/bin/bash

infilename=${1}
outfilename=${2}
inputDir=${3}
outputDir=${4}

macroDir=${PWD}

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700

scramv1 project CMSSW CMSSW_10_6_19
cd CMSSW_10_6_19
eval `scramv1 runtime -sh`
cd -

export PATH=$PATH:$macroDir

root -l -b -q make_step2.C\(\"$macroDir\",\"$inputDir/$infilename\",\"$outfilename\"\)

xrdcp -f $outfilename $outputDir/
rm $outfilename
