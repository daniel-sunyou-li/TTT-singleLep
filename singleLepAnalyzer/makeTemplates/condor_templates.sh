#!/bin/bash

variable=${1}
year=${2}
category=${3}
exeDir=${4}
subDir=${5}
condorDir=$PWD

source /cvmfs/cms.cern.ch/cmsset_default.sh

cd $exeDir
eval `scramv1 runtime -sh`

python -u hists.py \
  -v $variable \
  -y $year \
  -c $category \
  -sd $subDir
