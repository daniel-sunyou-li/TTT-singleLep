# `FWLJMET` -- Full Framework `LJMet`
`LJMet` is an `EDAnalyzer` that performs various selections and calculations on CMS datasets in the `MiniAOD` data format. `LJMet` refers to 'leptons', 'jets' and 'missing transverse energy'--the primary physics objects being analyzed. The `EDAnalyzer` is run using a configuration file and the CMS alias `cmsRun`. The general flow of an `EDAnalyzer` is sequential where your various "selector" and "calculator" modules are chained together in a `Path()`. These various modules are defined in their respective `c++` code with the header files in `/FWLJMET/LJMet/interface/` and the source files in `/FWLJMET/LJMet/plugins/`. 

Some of these modules have file and library dependencies which require use of the `CMSSW` environment, as well as having files locally stored in `FWLJMET/LJMet/data/`. Furthermore, due to the large list of samples we run `LJMet` on, as well as the size of those files, we use a distributed computing grid known as `CRAB3` to manage and run our many computing jobs. The scripts necessary for running the "CRAB3" jobs are in `FWLJMET/LJMet/CRAB3/` and can be stored either on the LPC EOS group storage or Brown's BRUX storage. 

There are four different data taking periods that will be processed separately: 2016APV, 2016, 2017 and 2018. A different `CRAB` configuration file will be run for each of the years and the samples from each of the years will be stored in a directory with a naming convention like `FWLJMET106XUL_*Lep20*UL_RunIISummer20`.

## Setting-up `LJMet`  
It is recommended to run `LJMet` on the LPC, which requires having completed [the instructions here](https://uscms.org/uscms_at_work/computing/getstarted/uaf.shtml). For the following instructions, replace [###] with the appropriate user-specific variables.

__Signing in to FNAL LPC:__	

	kinit -f [username]@FNAL.GOV
	ssh [username]@cmslpc-sl7.fnal.gov

__Retrieving the `CMSSW` environment:__  
Note that if you are running a `bash` environment, the postfix should be `.sh` rather than `.csh` for `tcsh`. Also, `setenv [alias] [name]` in `tcsh` should be `export [alias]=[name]` in `bash`.

For `tcsh`:
	
	cd ~/nobackup
	source /cvmfs/cms.cern.ch/cmsset_default.csh
	setenv SCRAM_ARCH slc7_amd64_gcc700
	cmsrel CMSSW_10_6_29
	cd CMSSW_10_6_29/src/
	cmsenv

For `bash`:
	
	cd ~/nobackup
	source /cvmfs/cms.cern.ch/cmsset_default.sh
	export SCRAM_ARCH=slc7_amd64_gcc700
	cmsrel CMSSW_10_6_29
	cd CMSSW_10_6_29/src/
	cmsenv
	
The following instructions are all assumed to be referencing the `src` directory in `CMSSW_10_6_29` which can be reached using the command `cd ${CMSSW_BASE}/src/` after running the `cmsenv` environment once.
	
__Redo the [MET filters](https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2):__
	
	git cms-addpkg RecoMET/METFilters

__[HOT (Resolved top) Tagger](https://github.com/susy2015/TopTagger/tree/master/TopTagger#instructions-for-saving-tagger-results-to-nanoaod-with-cmssw_9_4_11) Part One:__

	git clone https://github.com/susy2015/TopTagger.git
	
To make `TopTagger` compatible with `CMSSW_10_6_29`, you must manually edit (i.e. using 'vim') the following file: `/TopTagger/DataFormats/BuildFile.xml` with the following:
* Add `<use name="clhep"/>`
* Add `<use name="root"/>`
	
__Adding `Axis1` information for `RecoJets`:__

	git cms-addpkg RecoJets/JetProducers

The old instruction for adding Axis1 information "git cms-merge-topic -u pastika:AddAxis1_1026" doesn't work for `CMSSW_10_6_29`, please do the following steps by hand:
* Replace `RecoJets/JetProducers/plugins/QGTagger.cc` with [this version](https://github.com/jingyuluo/QG_SA/blob/master/QGTagger.cc)
	* Instructions using 'vim':
		1. Open `QGTagger.cc` with 'vim': `vim RecoJets/JetProducers/plugins/QGTagger.cc`
		2. Delete all contents: `dG`
		3. Set 'paste' mode: `:set paste`
		4. Set 'insert' mode: `i`
		5. Copy new `QGTagger.cc` contents into empty file using 'copy+paste'
		6. Exit 'insert' mode: `esc` key
		7. Save and exit: `:wq`
* Update `RecoJets/JetProducers/interface/QGTagger.h` by replacing L24: `std::tuple<int, float, float> calcVariables` with `std::tuple<int, float, float, float> calcVariables`

__Adding `EGammaPostRecoTools` and `ElectronTools` for [Electron MVA ID](https://twiki.cern.ch/twiki/bin/view/CMS/EgammaMiniAODV2):__

	git cms-addpkg RecoEgamma/EgammaTools
	git clone https://github.com/cms-egamma/EgammaPostRecoTools.git
	mv EgammaPostRecoTools/python/EgammaPostRecoTools.py RecoEgamma/EgammaTools/python/.
	git clone -b ULSSfiles_correctScaleSysMC https://github.com/jainshilpi/EgammaAnalysis-ElectronTools.git EgammaAnalysis/ElectronTools/data/
	git cms-addpkg EgammaAnalysis/ElectronTools

__Adding `BestCalc`:__  
Copy `lwtnn` for `BestCalc.cc` to compile:

	cp -r ~jmanagan/nobackup/CMSSW_9_4_12/src/lwtnn .
	
If not running on the LPC, use `scp` instead. 

For more information about `BestCalc`, or BoostedEventShapeTagger (BEST):
* https://bregnery.github.io/docs/BESTstandaloneTutorial/
* https://github.com/justinrpilot/BESTAnalysis/tree/master
* https://github.com/demarley/lwtnn/tree/CMSSW_8_0_X-compatible#cmssw-compatibility

__Checking out FWLJMET from Github:__  
Finally, we can download the `FWLJMET` code base after setting up all the necessary dependencies:

	git clone -b 10_6_29_UL https://github.com/cms-ljmet/FWLJMET.git
	cd FWLJMET

__Add `PUPPI` Mass Corrections to `FWLJMET/LJMet/data/` for `JetSubCalc`:__  

	cd ${CMSSW_BASE}/src/FWLJMET/LJMet/data/
	git clone https://github.com/thaarres/PuppiSoftdropMassCorr
	cd ${CMSSW_BASE}/src/

__Compile all the code:__  
This is necessary anytime you make changes to the `c++` code, so either `.h` or `.cc` files:

	scram b

__HOT Tagger Part Two:__  

	cmsenv
	mkdir -p ${CMSSW_BASE}/src/TopTagger/TopTagger/data
	cd ${CMSSW_BASE}/src/TopTagger/TopTagger/scripts/
	./getTaggerCfg.sh -o -n -t DeepResolved_DeepCSV_GR_noDisc_Release_v1.0.0 -d $CMSSW_BASE/src/TopTagger/TopTagger/data


## (OPTIONAL) Running a test `LJMet` EDAnalyzer
There are four test configuration scripts (`2016APV`,`2016`,`2017`,`2018`) available that allow you to run the EDAnalyzer locally for purposes such as quick debugging or viewing. Run parameters can be changed inside the script, such as the input sample and number of events. 

    cd ${CMSSW_BASE}/src/FWLJMET/LJMet/
    voms-proxy-init --voms cms
    cmsRun tester2017UL.py 

At the end of running, you should have a `.root` file with a name similar to `test_2017UL.root`.
