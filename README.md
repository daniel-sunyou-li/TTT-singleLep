# Search for three top quarks decaying to the single-lepton plus jets final state
Full framework of running the three top quark to single-lepton final state search analysis.  Begins with running the `FWLJMET` EDAnalyzer to produce the `LJMet` ntuples and ends with evaluating the expected/observed significance and cross section limits for three top quark production. The subdirectories listed here are derived from other repositories that are used by other analyses. The steps specific to the search for three top quarks begin with "Variable Importance" where the first three steps are applicable to any analysis ending in the single-lepton final state. A description of each of the steps is provided below.

The overall steps throughout the analysis framework are as follows:
> 1. __`FWLJMET`__ - an EDProducer instance producing the AOD file with relevant collections
> 2. __`LJMET-Slimmer-4tops/step1`__ - slims the ntuple to only include necessary variables  
> 3. __`LJMET-Slimmer-4tops/step2`__ - adds multivariate jet-tagging discriminators to the 'Step 1' ntuple  
> 4. __`Variable Importance`__ - train and optimize a dense neural network to produce a single discriminator for the analysis
> 5. __`Step 3`__ - adds the DNN discriminator(s) to the 'Step 2' ntuple
> 6. __`ABCDnn`__
> 6. __`singleLepAnalyzer`__ - computes the significance and limits for the signal strength 

This repository contains code for running the full analysis on either the HT (sum of jet transverse momentum) or the DNN discriminator. For the HT option, only steps 1, 2, 3 and 6 are necessary. In addition to the HT and DNN discriminator, the TTT single lepton final state analysis is also carried out with a BDT discriminator, not included in this repository.

## Quick-Start Instructions
1. __Set-up the analysis environment on the LPC__  

    kinit -f [username]@FNAL.GOV
    ssh [username]@cmslpc-sl7.fnal.gov
    cd 
  
2. 
3. 
4. __
