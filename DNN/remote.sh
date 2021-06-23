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

# Copy and Unpack Resources
xrdcp -s root://cmseos.fnal.gov//store/user/$eos_username/CMSSW946_ttt.tgz .
tar -xf CMSSW946_ttt.tgz
rm CMSSW946_ttt.tgz

cd ./CMSSW_9_4_6_patch1/src/TTT-singleLep/DNN/

export SCRAM_ARCH=slc7_amd64_gcc630
eval `scramv1 runtime -sh`
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.16.00/x86_64-centos7-gcc48-opt/bin/thisroot.sh

echo "[OK ] Setup finished."

python remote.py -y $year -s $seed_vars -nj $NJETS -nb $NBJETS -ht $AK4HT -met $MET -lpt $LEPPT -mt $MT -dr $MINDR 
