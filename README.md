# Search for three top quarks decaying to the single-lepton plus jets final state
Full framework of running the three top quark to single-lepton final state search analysis. Begins with running the `FWLJMET` EDAnalyzer to produce the `LJMet` ntuples and ends with evaluating the expected/observed significance and cross section limits for three top quark production. The subdirectories listed here are derived from other repositories that are used by other analyses. The steps specific to the search for three top quarks begin with "Variable Importance" where the first three steps are applicable to any analysis ending in the single-lepton final state. A description of each of the steps is provided below, and, where relevant, the associated template repositories are linked.

The overall steps throughout the analysis framework are as follows:
> 1. [__`FWLJMET`__](https://github.com/cms-ljmet/FWLJMET/tree/10_6_29_UL) - An `EDAnalyzer` with various selectors and calculators that produce `LJMet` ntuples containing the basic physics objects used throughout the single-lepton final state analyses
> 2. [__`step1`__](https://github.com/daniel-sunyou-li/LJMet-Slimmer-1lepUL/tree/main/step1) - Consolidates `LJMet` ntuples, calculates "analysis"-level variables and adds the scale factors to the ntuples
> 3. [__`step2`__](https://github.com/daniel-sunyou-li/LJMet-Slimmer-1lepUL/tree/main/step2) - Adds machine-learning based jet-tagging discriminators and scale factors to the 'step1' ntuple  
> 4. __`step3 (Variable Importance)`__ - train and optimize a dense neural network to produce a single signal-versus-background discriminator for Higgs Combine and create a new ntuple. This step is only necessary if using the DNN discriminator for `singleLepAnalyzer`, otherwise can be skipped.
> 5. [__`ABCDnn`__](https://github.com/daniel-sunyou-li/ABCDnn) - data-driven background shape estimation for ttbar samples using the Higgs Combine variable 
> 6. __`singleLepAnalyzer`__ - computes the significance and limits for three top production using the variable from `step3` and `ABCDnn` 

For instructions and details related to each step, refer to the sub-directories.  The whole analysis can be run in `CMSSW_10_6_29`.
