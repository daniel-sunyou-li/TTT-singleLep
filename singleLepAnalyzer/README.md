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

All scripts run automatically by `automate.py` can be run interactively via the terminal. All example interactive submissions are for the 2017 era running a fit on the DNN discriminator binned for the signal region. If you create a new production of step1, step2 or step3 files, you may need to update `samplesUL##.py` with the correct file names, as well as indiate number of hadded files. You may also redefine the background groupings used for formatting the backgrounds. You may also update the process cross-sections used in normalizing the MC yields in `xsec.py`. 

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
        python hists.py -v DNN -y 17 -nh 1p -nb 3p -nj 7p -sd templates_UL17_DNN_SR_postfix
        
Possible arguments include:
* `-v` (`--variable`) -- see `config.plot_params["VARIABLES"]`
* `-y` (`--year`) -- `16APV`, `16`, `17`, `18`
* `-l` (`--lepton`) -- `E` (electron) or `M` (muon)
* `-nh` (`--nhot`) -- HOT-tagged jet multiplicity requirement (use `#p` to indicate inclusive bin)
* `-nt` (`--nt`) -- top-tagged jet multiplicity requirement
* `-nw` (`--nw`) -- W-tagged jet multiplicity requirement
* `-nb` (`--nb`) -- b-tagged jet multiplicity requirement
* `-nj` (`--nj`) -- jet multiplicity requirement
* `-sd` (`-subDir`) -- name of subdirectory to store the histogrms and templates

Running `hists.py` once creates the template for a single combination of the template binning regions. Each template constitutes a pickled file of histograms for the background, signal and data files. The event selection and MC scaling is applied during this step, as well as defining some of the systematic histograms. Running step 1 for `automate.py` calls on `condor_templates.py` to submit all combinations of the signal region template binning as condor jobs and saves each template to the same subdirectory.

### Step 2 -- Format and Clean `Higgs Combine` Templates

To combine the histograms into a single template and perform some histogram corrections,

        cd makeTemplates/
        python templates.py -v DNN -y 17 -t postfix -r SR 
        python modify_binning.py -v DNN -y 17 -t postfix -r SR 
        
Possible arguments for `templates.py` and `modify_binning.py` include:
* `-v` (`--variable`)
* `-y` (`--year`)
* `-t` (`--tag`) -- unique postfix to distinguish templates
* `-r` (`--region`) -- template binning region
* `--abcdnn` (`modify_binning.py` only) -- perform binning according to ABCDnn MC background

In `templates.py`, the histograms are formatted according to the category-by-category statistics, producing a single ROOT template file along with a table with category yields in the subdirectory. Statistical significance thresholds are applied to determine whether or not to include the defined background groups. Other general bin corrections are applied including overflow and underflow, negative bins. 

In `modify_binning.py`, the histograms are further formatted to improve the `Higgs Combine` likelihood analysis, producing a single ROOT template file with modified binning to be run on. Several of these corrections include rebinning the histograms to achieve a required bin-by-bin statistical significance, symmetrizing and smoothing the up/down systematic shifts, and defining some of the theoretical systematic uncertainties. 

### (Optional) Step 3 -- Plot Histograms

To plot the histograms for each category, 

        cd makeTemplates/
        python plot_templates.py -v DNN -y 17 -t postfix -r SR --templates
        
Possible arguments for `plot_templates.py` include:
* `-v` (`--variable`)
* `-y` (`--year`)
* `-t` (`--tag`)
* `-r` (`--region`)
* `--templates` -- produce the histogram plots by template bin category
* `--ratios` -- produce bar graphs showing the relative background composition by template bins

There are additional arguments that can be used to format the plots as well as control which uncertainties are displayed in `config_plot.py`. Some of the important options to check include whether the rebinned templates are being plotted and whether the data is shown or not (i.e. blinded vs unblinded). The different plots can be found in the subdirectory. 

### Steo 4 -- Create Datacards and Run `Higgs Combine` by Era

Datacards to be used in `Higgs Combine` are produced using,

        cd combine/
        python create_datacard.py -v DNN -y 17 -t postfix -r SR --shapeSyst --normSyst
        cd limits_UL17_DNN_SR_postfix_LOWESS/
        combineTool.py -M T2W -i cmb/ -o workspace.root --parallel 4
        combine -M Significance cmb/workspace.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 > significance.txt
        combine -M AsymptoticLimits cmb/workspace.root --run=blind --cminDefaultMinimizerStrategy 0 > limits.txt
        
Possible arguments for `create_datacard.py` include:
* `-v` (`--variable`)
* `-y` (`--year`)
* `-t` (`--tag`)
* `-r` (`--region`)
* `-m` (`--mode`) -- Options include `0` through `3` (default = `0`) which determine whether to treat the template categories as a control or signal region
* `--shapeSyst` -- Flag to include the shape systematic uncertainties in the datacard
* `--normSyst` -- Flag to include the normalization systematic uncertainties in the datacard

Additional options and parameters can be configured in `config.py`, including whether to run with ABCDnn MC background or not and to use the smoothed templates or not. `create_datacard.py` produces a subdirectory (indicating if the smoothing is used, ABCDnn is used, shape uncertainties are included and normalization uncertainties are included) that will contain the `Combine` datacards in `cmb/`. `Higgs Combine` takes the datacard as an input to interpret the histogram groups and systematics to include during the simultaneous binned likelihood fit. There are datacards produced for the individual template bins beginning with `TTTX_*.txt` and they are consolidated into a single datacard for the given era in `combined.txt.cmb`.

More information regarding the `Higgs Combine` commands can be found on the [webpage](http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/commonstatsmethods/). The default running settings in `singleLepAnalyzer` are blinded and generate Asimov toy datasets to simulate the data for computing an expected significance and signal strength limits. The results are stored in significance.txt and limits.txt, respectively. 

### Step 5 -- Combine Eras and Final States Datacards 

After producing datacards for the individual eras (or final states), they can be combined into a single datacard (for a Run2 analysis, as an example) with,

        cd combine/
        combineCards.py UL16APV=limits_UL16APV_DNN_SR_postfix_LOWESS/cmb/combined.txt.cmb UL16=limits_UL16_DNN_SR_postfix_LOWESS/cmb/combined.txt.cmb UL17=limits_UL17_DNN_SR_postfix_LOWESS/cmb/combined.txt.cmb UL18=limits_UL18_DNN_SR_postfix_LOWESS/cmb/combined.txt.cmb
        text2workspace.py Results/DNN_SR_postfix_LOWESS/workspace.txt -o Results/DNN_SR_postfix_LOWESS/workspace.root 
        combine -M Significance Results/DNN_SR_postfix_LOWESS/workspace.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 > Results/DNN_SR_postfix_LOWESS/significance.txt
        combine -M AsymptoticLimits Results/DNN_SR_postfix_LOWESS/workspace.root --run=blind --cminDefaultMinimizerStrategy 0 > Results/DNN_SR_postfix_LOWESS/limits.txt

### Step 6 -- Study Systematic Uncertainties with Impact Plots by Era

The systematic uncertainties can be studied using tools available in `Higgs Combine`.  In particular, the systematic uncertainty impacts on the signal strength (`r`) likelihood fit can be evaluated by freezing all-but-one nuisance parameters and seeing how much the post-fit vs pre-fit pull shifts affect the signal strength. The command for retrieving the impacts are,

        cd combine/
        cd limits_UL17_DNN_SR_postfix_LOWESS/cmb/
        combineTool.py -M Impacts -d workspace.root -m 125 --doInitialFit --robustFit 1 -t -1 --expectSignal 1 --rMin -100 --rMax 100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerType Minuit
        combineTool.py -M Impacts -d workspace.root -m 125 --doFits --robustFit 1 -t -1 --expectSignal 1 --rMin -100 --rMax 100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --exclude rgx"\prop_bin.*\}" --cminDefaultMinimizerType Minuit
        combineTool.py -M Impacts -d workspace.root -m 125 -o impacts_UL17_DNN_SR_postfix_LOWESS --exclude rgx"\prop_bin.*\}"
        plotImpacts.py -i impacts_UL17_DNN_SR_postfix_LOWESS -o impacts_UL17_DNN_SR_postfix_LOWESS
        
Some of the options for producing the impact plots include:
* `-t -1` -- this is for blinding the data and using a toy Asimov dataset
* `--rMin` and `--rMax` -- allows the fit to test `r` at defined bounds, default set to `--rMin` at `0` and `--rMax` at `20`
* `--exclude rgx"\prop_bin.*\}"` -- this excludes the statistical uncertainties by bin (which add a significant amount of computing time)
        
### Step 7 -- Study Systematic Uncertainties for Combined Eras

The systematic uncertainties for the combined datacards can be evaluated in a similar method using the combined datacard (and workspace) instead of the ones for the individual eras.
