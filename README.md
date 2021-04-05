# TTT-singleLep
Full framework of running the three top quark to single lepton final state analysis.  Begins with running LJMET and ends with computing the significance and limits for the TTT signal strength.

The overall steps throughout the analysis framework are as follows:
> 1. __`FWLJMET`__ - an EDProducer instance producing the AOD file with relevant collections
> 2. __`LJMET-Slimmer-4tops/step1`__ - slims the ntuple to only include necessary variables  
> 3. __`LJMET-Slimmer-4tops/step2`__ - adds multivariate jet-tagging discriminators to the 'Step 1' ntuple  
> 4. __`Variable Importance`__ - train and optimize a dense neural network to produce a single discriminator for the analysis
> 5. __`Step 3`__ - adds the DNN discriminator(s) to the 'Step 2' ntuple
> 6. __`singleLepAnalyzer`__ - computes the significance and limits for the signal strength 

This repository contains code for running the full analysis on either the HT (sum of jet transverse momentum) or the DNN discriminator. For the HT option, only steps 1, 2, 3 and 6 are necessary. In addition to the HT and DNN discriminator, the TTT single lepton final state analysis is also carried out with a BDT discriminator, not included in this repository.

## Quick-Start Instructions
