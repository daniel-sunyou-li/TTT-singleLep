#!/bin/sh

eos_username=${1}
year=${2}
seed_vars=${3}
NJETS=${4}
NBJETS=${5}
AK4HT=${6}
MET=${7}
LEPPT=${8}
MT=${9}
MINDR=${10}

echo ">> Setting Up TTT Job"

# Enter environment
source /cvmfs/cms.cern.ch/cmsset_default.sh
scramv1 project CMSSW CMSSW_13_3_0
cd CMSSW_13_3_0/src/
eval `scramv1 runtime -sh`
cd -

#source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.16.00/x86_64-centos7-gcc48-opt/bin/thisroot.sh

python3 remote.py -y $year -s $seed_vars -nj $NJETS -nb $NBJETS -ht $AK4HT -met $MET -lpt $LEPPT -mt $MT -dr $MINDR 
