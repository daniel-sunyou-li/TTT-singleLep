#!/bin/bash

condorDir=$PWD
runDir=${1}
inputDir=${2}
cmsswDir=${3}
year=${4}
variable=${5}
region=${6}
categorize=${7}
lepton=${8}
nhot=${9}
nT=${10}
nW=${11}
nB=${12}
nJ=${13}

source /cvmfs/cms.cern.ch/cmsset_default.sh

cd $cmsswDir
eval `scramv1 runtime -sh`

cd $runDir

pwd
python -u hists.py \
  -v $variable \
  -r $region \
  -c $categorize \
  -y $year \
  -l $lepton \
  -nh $nhot \
  -nt $nT \
  -nw $nW \
  -nb $nB \
  -nj $nJ \
  -i $inputDir \
  -d $condorDir \
  -w $cmsswDir
