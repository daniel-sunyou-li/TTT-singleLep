# TTT-singleLep
Full framework of running the three top quark to single lepton final state analysis.  Begins with running LJMET and ends with computing the significance and limits for the TTT signal strength.

The overall steps throughout the analysis framework are as follows:
> 1. LJMET - an EDProducer instance producing the AOD file with relevant collections
> 2. 'Step 1' - slims the ntuple to only include necessary variables  
> 3. 'Step 2' - adds multivariate jet-tagging discriminators to the 'Step 1' ntuple  
> 4. TTT DNN - train and optimize a dense neural network to produce a single discriminator for the analysis
> 5. 'Step 3' - adds the DNN discriminator(s) to the 'Step 2' ntuple
> 6. singleLepAnalyzer - computes the significance and limits for the signal strength 

This repository contains code for running the full analysis on either the HT (sum of jet transverse momentum) or the DNN discriminator. For the HT option, only steps 1, 2, 3 and 6 are necessary. In addition to the HT and DNN discriminator, the TTT single lepton final state analysis is also carried out with a BDT discriminator, not included in this repository.

## Quick-Start Instructions
