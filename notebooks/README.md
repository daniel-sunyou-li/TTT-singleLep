# `python` Notebook Explanations
All notebooks are intended to be run on [SWAN](swan.cern.ch) and require having a valid grid certificate uploaded. Samples are sourced primarily from BRUX (@brux30.hep.brown), but also from the LPC (@cmslpc.fnal.gov). A supporting script `xsec.py` is included that will skim the `step1hadds` files to extract the event weights used for calculating the cross-section normalization. It is necessary to update the era in `xsec.py` when updating the era in a notebook. Also, note that there are naming differences in the electron data and four top sample between 2018 and the remaining eras which needs to be adjusted when running on 2018.

### `check_2018_HEM.ipnyb`
This notebook visualizes the region in $(\phi,\eta)$ during the 2018 when an ECAL was out resulting in many jets being misreconstructed as fake electrons. A veto is applied in `singleLepAnalyzer` to veto events where the electron falls into this region.

### `compare_DNN_shape.ipynb`
This notebook is intended to compare DNN discriminator branches added from the `DNN` repository and calculate ROC AUC scores between the three top signal and various backgrounds. The results can be used to determine which discriminators have the best shape separation.

### `compare_ttbar_MC.ipynb`
This notebook compares a ``nominal'' top-pair MC sample to one that is enriched with events having, at generator-level, at least nine jets with $H_T>500~GeV$. Importantly, the high $H_T$ tail should be better-modeled statistically, which is also where there is likely to be more signal. This feature is not as important in the context of the data-driven background estimation methods since top-pair events are not modeled with MC any longer.

### `data_MC_agreement.ipynb`
This notebook plots variable distributions and can be used for data versus MC agreement comparisons. This effectively performs the task of ``step 2'' in `singleLepAnalyzer` for plotting, but is faster due to excluding the systematic uncertainties. 

### `deepJet_renorm_comparison.ipynb`
This notebook plots evaluates the impact of including DeepJet renormalization weights, which are calculated in `step2`. The DeepJet iterative fit weights correct the DeepJet score MC shape, but also affects the overall yield, which should not happen. Thus, the renormalization weight should recover the yield prior to when the DeepJet shape weights are applied.

### `plot_DNN_loss.ipynb`
This notebook plots the training and validation loss produced from the k-fold cross validation training in the `DNN` repository. It also plots the ROC curves.

### `plot_variable_correlation.ipynb`
This notebook computes and visualizes the correlation between variables used during the `DNN` training. Importantly, the correlations should be compared between data and MC to ensure that MC is modeling data accurately. Variables that aren't correlated in a similar manner may indicate poor modeling and should be excluded from training.

### `plot_variables.ipynb` 
Plots MC variable inputs and visualizes correlation between two inputs using scatter and 2D histogram plots. Can be used for determining triangle cuts.

### `trigger_efficiency.ipynb` 
Plot the crossing trigger data and MC efficiency as well as scale factors.

### `xsec.py`
Called by various notebooks and is used for retrieving event weights used in calculating the cross section normalization weight.
