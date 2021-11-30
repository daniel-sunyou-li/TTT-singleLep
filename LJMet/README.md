# FWLJMET: Full Framework LJMET (wrapper)

To install FWLJMET on the LPC:
    
    setenv SCRAM_ARCH slc7_amd64_gcc700
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    cmsrel CMSSW_10_6_19
    cd CMSSW_10_6_19/src
    cmsenv
    
Redo the MET filter
    
    git cms-addpkg RecoMET/METFilters
    
HOT Tagger (need to update)

    git clone https://github.com/susy2015/TopTagger.git
    
The current top tagger version on Github is not compatible with CMSSW_10_6_19 and requires modifications in `TopTagger/DataFormats/BuildFile.xml`, add:

    <use name="clhep"/>
    <use name="root"/>
    
Add the Axis1 information manually using:

    git cms-addpkg RecoJets/JetProducers
    
Replace `RecoJets/JetProducers/plugins/QCTagger.cc` with [this file](https://github.com/jingyuluo/QG_SA/blob/master/QGTagger.cc).  And in `RecoJets/JetProducers/interface/QCTagger.h` replace the line:

    std::tuple<int, float, float> calcVariables
    
with:

    std::tuple<int, float, float, float> calcVariables
    
For the EGamma post-reco MVA values use:

    git cms-merge-topic cms-egamma:EgammaPostRecoTools
    
Finally, check-out `LJMET`:

    git clone -b UL https://github.com/daniel-sunyou-li/TTT-singleLep.git
    
Update the pre-firing map for UL17 (from the [L1ECALPrefiring Twiki](https://twiki.cern.ch/twiki/bin/viewauth/CMS/L1ECALPrefiringWeightRecipe)):

    git-cms-addpkg PhysicsTools/PatUtils
    cd PhysicsTools/PatUtils/data/
    wget --no-check-certificate https://github.com/cms-data/PhysicsTools-PatUtils/raw/master/L1PrefiringMaps.root
    
`JetSubCalc` uses `PUPPI` mass corrections:

    cd ../../../TTT-singleLep/LJMet/data/ 
    git clone https://github.com/thaarres/PuppiSoftdropMassCorr
    
Compile everything:

    cd ../../..
    scram b
    
Continue setting up HOT tagger (part 2):

    cmsenv
    mkdir -p TopTagger/TopTagger/data
    cd TopTagger/TopTagger/scripts/
    ./getTaggerCfg.sh -o -n -t DeepResolved_DeepCSV_GR_noDisc_Release_v1.0.0 -d ../data
    cd ../../../TTT-singleLep/
    
To run LJMET interactively:

    cmsRun LJMet/runFWLJMet_singleLep.py era=2017
    
To run LJMET through CRAB3:

    source /cvmfs/cms.cern.ch/crab3/crab.sh
    crab submit --dryrun crab_FWLJMET_cfg.py
    python create_crab_config_template.py --finalState singleLep --year 2017 
    python submit_crab.py --finalState singleLep --year 2017
    
Optionally, can include the argument `--nominal` to only run the nominal tree.