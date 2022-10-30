# Single Lep Analyzer -- Three Top to Single Lepton Final State

## Environment Setup

Before running this repository, run the following setup instructions once (prepared for BRUX):

    # retrieve CMSSW environment
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    setenv SCRAM_ARCH slc7_amd64_gcc700
    cmsrel CMSSW_10_6_29
    cd CMSSW_10_6_29/src/
    cmsenv
    # retrieve Higgs Combine and Combine Harvester
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    cd HiggsAnalysis/CombinedLimit
    git fetch origin
    git checkout v8.2.0
    git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
    scramv1 b clean; scramv1 b
    # retrieve singleLepAnalyzer
    git clone -b UL https://github.com/daniel-sunyou-li/TTT-singleLep.git

## Quick Start Instructions

To run `singleLepAnalyzer`, 

    cd CMSSW_10_6_29/src/TTT-singleLep/singleLepAnalyzer/
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    cmsenv 
    python automate.py -y <era1> <era2> -v <var1> <var2> -t <tag> -r <region> -s <step1-4>
    python automate.py -v <var1> <var2> -t <tag> -r <region> -s 5
    python automate.py -y <era1> <era2> -v <var1> <var2> -t <tag> -r <region> -s 6
    python automate.py -v <var1> <var2> -t <tag> -r <region> -s 7

Where the following arguments are supported:
* `-y` (`--year`): `16APV`, `16`, `17`, `18`
* `-r` (`--region`): see [config.py](https://github.com/daniel-sunyou-li/TTT-singleLep/blob/UL/singleLepAnalyzer/config.py#L268-L275)
* `-v` (`--variables`): see [config.py](https://github.com/daniel-sunyou-li/TTT-singleLep/blob/UL/singleLepAnalyzer/config.py#L334-L422)
* `-t` (`--tag`): unique postfix for templates generated for a given config setting
* `-s` (`--step`): `1` through `7`, for an explanation, see below

## Detailed Step Explanations

All scripts run automatically by `automate.py` can be run interactively via the terminal. All example interactive submissions are for the 2017 era running a fit on the DNN discriminator binned for the signal region.

### Step 0 Edit `config.py`

All settings and parameters are defined in `config.py` and any edits should only be made to `config.py`. Check (and edit) the following settings/parameters before running `singleLepAnalyzer`:
* `inputDir` -- path to ROOT files containing events
* `options` -- boolean analysis options
* `params` -- non-boolean analysis parameters 
* `systematics` -- indicate systematics to include in analysis as well as uncertainty values
* `hist_bins` -- define template binning regions
* `event_cuts` -- event selection cut values
* `base_cut` -- cuts applied to branches in ROOT files
* `mc_weight` -- scale factor weights applied per event, also modified in `hists.py`
* `plot_params` -- new analysis variables need to be added along with desired binning and plotting name

### Step 1 -- Draw Histograms

To populate histograms interactively,

        cd makeTemplates/
        python hists.py -v DNN -y 17 -nh 1p -nb 3p -nj 7p -sd templates_UL17_DNN_SR
        
Running `hists.py` once creates the template for a single combination of the template binning regions. Running step 1 for `automate.py` calls on `condor_templates.py` to submit all combinations of the signal region template binning as condor jobs and saves each template to the same subdirectory


### Step 2 -- Format and Clean `Higgs Combine` Templates

### (Optional) Step 3 -- Plot Histograms

### Steo 4 -- Create Datacards and Run `Higgs Combine` by Era

### Step 5 -- Combine Eras and Final States Datacards 

### Step 6 -- Study Systematic Uncertainties with Impact Plots by Era

### Step 7 -- Study Systematic Uncertainties for Combined Eras

