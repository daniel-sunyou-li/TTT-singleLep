#!/bin/bash

hostname
date

infilename=${1}
outfilename=${2}
inputDir=${3}
outputDir=${4}
idlist=${5}
ID=${6}
Year=20${7}
systematics=${8}
scratch=${PWD}

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700
scramv1 project CMSSW CMSSW_10_6_19
cd CMSSW_10_6_19
eval `scramv1 runtime -sh`
cd -

echo ">> Setting macroDir to PWD"
macroDir=${PWD}
export PATH=$PATH:$macroDir
root -l -b -q compile_step1.C

XRDpath=root://cmseos.fnal.gov/$inputDir
if [[ $inputDir == /isilon/hadoop/* ]] ;
then
XRDpath=root://brux11.hep.brown.edu:1094/$inputDir
fi

echo ">> Running step1 over list: ${idlist}"
rm filelist
for iFile in $idlist; do
  inFile=${iFile}
  if [[ $iFile == ext* ]] ;
  then
    inFile=${iFile:4}
  elif [[ $iFile == [ABCDEFWXYZ]* ]] ;
  then
    inFile=${iFile:1}
  fi

  echo ">> Adding ${outfilename}_${iFile}.root to the list by reading ${infilename}_${inFile}"
  echo  $XRDpath/${infilename}_${inFile}.root,${outfilename}_${iFile}.root>> filelist
done

root -l -b -q -g make_step1.C\(\"$macroDir\",\"filelist\",\"$systematics\",${Year}\)

echo ">> ROOT Files:"
ls -l *.root

# copy output to eos

NOM="nominal"
echo ">> xrdcp output for condor"

shifts=(nominal)
if $systematics == true;
then shifts=(nominal JECup JECdown JERup JERdown)
fi

for shift in ${shifts[@]}; do
  haddFile=${outfilename}_${ID}${shift}_hadd.root
  hadd ${haddFile} *${shift}.root
  if [[ $outputDir == /pnfs/iihe/* ]] ;
  then # for qsub jobs
    echo ">> gfal-copy -f file://$TMPDIR/${haddFile} srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/${outputDir//$NOM/$shift}/${haddFile//${shift}_hadd/}"
    gfal-copy -f file://$TMPDIR/${haddFile} srm://maite.iihe.ac.be:8443/${outputDir//$NOM/$shift}/${haddFile//${shift}_hadd/} 2>&1
  else # for condor jobs on lpc
    echo ">> xrdcp -f ${haddFile} root://cmseos.fnal.gov/${outputDir//$NOM/$shift}/${haddFile//${shift}_hadd/}"
    xrdcp -f ${haddFile} root://cmseos.fnal.gov/${outputDir//$NOM/$shift}/${haddFile//${shift}_hadd/} 2>&1
  fi

  XRDEXIT=$?
  if [[ $XRDEXIT -ne 0 ]]; then
    rm *.root
    echo "[ERR] Exit code $XRDEXIT, failure in xrdcp (or gfal-copy)"
    exit $XRDEXIT
  fi
  rm *${shift}.root
  rm ${haddFile}
  if [[ $haddFile == Single* || $haddFile == EGamma* ]]; then break; fi;
done

echo "[DONE]"
