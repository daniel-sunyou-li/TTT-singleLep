# Run II Ultra Legacy Jet Energy Corrections and Resolution Scale Factors
Scale factor `.csv` files are available for the Ultra Legacy (UL) production of 2016, 2016APV, 2017 and 2018 MC samples. The preferred production to use as of _December 2, 2021_ is Summer20 and in the MiniAODv2 ntuple format. The `.csv` files can be found in the respective [JECDatabase](https://github.com/cms-jet/JECDatabase) and [JRDatabase](https://github.com/cms-jet/JRDatabase) Github repositories, along with the [Jet Energy Resolution Twiki](https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution) which can be referenced for usage of the scale factors.

### _b_-tagging Ultra Legacy Scale Factors
Both `deepCSV` and `DeepJet` are _b_-tagging methods that have associated scale factors. Implementation of the _b_-taggers, as well as calibrating the taggers, can be found on the [BTagCalibration Twiki](https://twiki.cern.ch/twiki/bin/view/CMS/BTagCalibration) and the recommended scale factor campaigns can be found in the respective Twiki pages for the years:
* [2016preVFP](https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16preVFP)
* [2016postVFP](https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP)
* [2017](https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17)
* [2018](https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL18)  

As of November 2021, the scale factor file format has changed to include also a human-readable `.json` version, which can be found at the [jsonPOG GitLab page](https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/tree/master/), as well as still in the `.csv` format. However, the entries for the working point (`operatingPoint`) and jet flavor (`jetFlavor`) have changed:
* `operatingPoint` = 0, 1, 2, 3 (loose/medium/tight/reshape) to L, M, T and a separate reshaping file
* `jetFlavor` = 0, 1, 2 (_b_/_c_/light) to 6, 5, and 0 (to match the pdgID convention)

The newer version for 2016 is `v2`, for 2017 is `v3` and for 2018 is `v2`.
