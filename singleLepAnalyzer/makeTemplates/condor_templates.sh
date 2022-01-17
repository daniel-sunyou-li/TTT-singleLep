#!/bin/bash

outputDir=${1}
variable=${2}
region=${3}
categorize=${4}
year=${5}
lepton=${6}
nhot=${7}
nT=${8}
nW=${9}
nB=${10}
nJ=${11}
exeDir=${12}
condorDir=$PWD

echo $PWD

source /cvmfs/cms.cern.ch/cmsset_default.sh

cd $exeDir
eval `scramv1 runtime -sh`

cd $runDir

pwd
python -u hists.py \
  -v $variable \
  -c $categorize \
  -y $year \
  -l $lepton \
  -nh $nhot \
  -nt $nT \
  -nw $nW \
  -nb $nB \
  -nj $nJ \
  -d $condorDir \
  -w $cmsswDir
