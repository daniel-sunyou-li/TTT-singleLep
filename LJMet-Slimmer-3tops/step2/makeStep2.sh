#!/bin/bash

infilename=${1}
outfilename=${2}
inputDir=${3}
outputDir=${4}

macroDir=${PWD}

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc700

scramv1 project CMSSW CMSSW_10_2_10
cd CMSSW_10_2_10
eval `scramv1 runtime -sh`
cd -

export PATH=$PATH:$macroDir

root -l -b -q makeStep2.C\(\"$macroDir\",\"$inputDir/$infilename\",\"$outfilename\"\)

cp $outfilename $outputDir/
rm $outfilename
