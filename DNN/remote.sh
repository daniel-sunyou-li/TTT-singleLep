#!/bin/sh

eos_username=${1}
year=${2}
seed_vars=${3}
njets=${4}
nbjets=${5}
ak4ht=${6}

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

python remote.py -y $year -s $seed_vars -nj $njets -nb $nbjets -ht $ak4ht
