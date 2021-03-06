import os,sys

signaldict =       { "2016": {}, "2017": {}, "2018": {} }
bkgdict =          { "2016": {}, "2017": {}, "2018": {} }
bkghtdict =        { "2016": {}, "2017": {}, "2018": {} }
ttbarbkgdict =     { "2016": {}, "2017": {}, "2018": {} }
datadict =         { "2016": {}, "2017": {}, "2018":{} }
#trigdict =         { "2016": {}, "2017": {}, "2018": {} }
trigdictmc =       { "2016": {}, "2017": {}, "2018": {} }
threetopsttdict =  { "2016": {}, "2017": {}, "2018": {} }
threetopsbkgdict = { "2016": {}, "2017": {}, "2018": {} }

# signal samples
signaldict["2016"]['TTTW'] = '/TTTW_TuneCUETP8M2T4_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM'
signaldict["2016"]['TTTJ'] = '/TTTJ_TuneCUETP8M2T4_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM'

signaldict["2017"]['TTTW'] = '/TTTW_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
signaldict["2017"]['TTTJ'] = '/TTTJ_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM'

signaldict["2018"]['TTTW'] = '/TTTW_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM'
signaldict["2018"]['TTTJ'] = '/TTTJ_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM'

#DYJetsToLL M-50
bkghtdict["2016"]['DYM50HT200to400'] = '/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
bkghtdict["2016"]['DYM50HT200to400ext1'] = '/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'
bkghtdict["2016"]['DYM50HT400to600'] = '/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
bkghtdict["2016"]['DYM50HT400to600ext1'] = '/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'
bkghtdict["2016"]['DYM50HT600to800'] = '/DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
bkghtdict["2016"]['DYM50HT800to1200'] = '/DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
bkghtdict["2016"]['DYM50HT1200to2500'] = '/DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
bkghtdict["2016"]['DYM50HT2500toInf'] = '/DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'

bkghtdict["2017"]['DYM50HT200to400'] = '/DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM'
bkghtdict["2017"]['DYM50HT400to600'] = '/DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM'
bkghtdict["2017"]['DYM50HT600to800'] = '/DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM'
bkghtdict["2017"]['DYM50HT800to1200'] = '/DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM'
bkghtdict["2017"]['DYM50HT1200to2500'] = '/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
bkghtdict["2017"]['DYM50HT2500toInf'] = '/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM'

bkghtdict["2018"]['DYM50HT200to400'] = '/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM'
bkghtdict["2018"]['DYM50HT400to600'] = '/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext2-v3/MINIAODSIM'
bkghtdict["2018"]['DYM50HT600to800'] = '/DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM'
bkghtdict["2018"]['DYM50HT800to1200'] = '/DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM'
bkghtdict["2018"]['DYM50HT1200to2500'] = '/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM'
bkghtdict["2018"]['DYM50HT2500toInf'] = '/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM'

# <<< QCD >>>
bkghtdict["2016"]['QCD700'] = '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM' 
bkghtdict["2016"]['QCD700ext1'] = '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'
bkghtdict["2016"]['QCD500'] = '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM' 
bkghtdict["2016"]['QCD500ext1'] = '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'
bkghtdict["2016"]['QCD300'] = '/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
bkghtdict["2016"]['QCD300ext1'] = '/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'
bkghtdict["2016"]['QCD200'] = '/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
bkghtdict["2016"]['QCD200ext1'] = '/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'
bkghtdict["2016"]['QCD2000'] = '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM' 
bkghtdict["2016"]['QCD2000ext1'] = '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'
bkghtdict["2016"]['QCD1500'] = '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
bkghtdict["2016"]['QCD1500ext1'] = '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'
bkghtdict["2016"]['QCD1000'] = '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
bkghtdict["2016"]['QCD1000ext1'] = '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'

bkghtdict["2017"]['QCD700'] = '/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM'
bkghtdict["2017"]['QCD500'] = '/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM'
bkghtdict["2017"]['QCD300'] = '/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM'
bkghtdict["2017"]['QCD200'] = '/QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM'
bkghtdict["2017"]['QCD2000'] = '/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM'
bkghtdict["2017"]['QCD1500'] = '/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM'
bkghtdict["2017"]['QCD1000'] = '/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM'

bkghtdict["2018"]['QCD700'] = '/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
bkghtdict["2018"]['QCD500'] = '/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
bkghtdict["2018"]['QCD300'] = '/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
bkghtdict["2018"]['QCD200'] = '/QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
bkghtdict["2018"]['QCD2000'] = '/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
bkghtdict["2018"]['QCD1500'] = '/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
bkghtdict["2018"]['QCD1000'] = '/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'

# <<< SM single top bck >>>
bkgdict["2016"]['ST_tW_antitop'] = '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM' 
bkgdict["2016"]['ST_tW_top'] = '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM' 
bkgdict["2016"]['ST_t_antitop'] = '/ST_t-channel_antitop_4f_inclusiveDecays_13TeV_PSweights-powhegV2-madspin/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
bkgdict["2016"]['ST_t_top'] = '/ST_t-channel_top_4f_inclusiveDecays_13TeV_PSweights-powhegV2-madspin/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v3/MINIAODSIM'
bkgdict["2016"]['ST_s'] = '/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'

bkgdict["2017"]['ST_tW_antitop'] = '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM'
bkgdict["2017"]['ST_tW_top'] = '/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM'
bkgdict["2017"]['ST_t_antitop'] = '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
bkgdict["2017"]['ST_t_top'] = '/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
bkgdict["2017"]['ST_s_top'] = '/ST_s-channel_top_leptonDecays_13TeV-PSweights_powheg-pythia/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
bkgdict["2017"]['ST_s_antitop'] = '/ST_s-channel_antitop_leptonDecays_13TeV-PSweights_powheg-pythia/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'

bkgdict["2018"]['ST_tW_antitop'] = '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v1/MINIAODSIM'
bkgdict["2018"]['ST_tW_top'] = '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v1/MINIAODSIM'
bkgdict["2018"]['ST_t_antitop'] = '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
bkgdict["2018"]['ST_t_top'] = '/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
bkgdict["2018"]['ST_s'] = '/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v3/MINIAODSIM'

# TTbar to 2L2Nu

threetopsttdict["2016"]['TTTo2L2Nu'] = '/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
#threetopsttdict['TTToSemiLepton_HT500Njet9'] ='/TTToSemiLepton_HT500Njet9_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
threetopsttdict["2016"]['TTToSemiLepton_HT500Njet9'] = '/TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
threetopsttdict["2016"]['TTTo2L2Nu_TuneCP5down'] = '/TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
threetopsttdict["2016"]['TTTo2L2Nu_TuneCP5down_ext1'] = '/TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM'
threetopsttdict["2016"]['TTTo2L2Nu_TuneCP5down_ext2'] = '/TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM'
threetopsttdict["2016"]['TTTo2L2Nu_TuneCP5up'] = '/TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
threetopsttdict["2016"]['TTTo2L2Nu_TuneCP5up_ext1'] = '/TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM'
threetopsttdict["2016"]['TTTo2L2Nu_TuneCP5up_ext2'] = '/TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM'
threetopsttdict["2016"]['TTTo2L2Nu_hdampDOWN'] = '/TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
threetopsttdict["2016"]['TTTo2L2Nu_hdampDOWN_ext1'] = '/TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM'
threetopsttdict["2016"]['TTTo2L2Nu_hdampDOWN_ext2'] = '/TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM'
threetopsttdict["2016"]['TTTo2L2Nu_hdampUP'] = '/TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
threetopsttdict["2016"]['TTTo2L2Nu_hdampUP_ext1'] = '/TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM'
threetopsttdict["2016"]['TTTo2L2Nu_hdampUP_ext2'] = '/TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM'

ttbarbkgdict["2017"]['TTTo2L2Nu'] = '/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM'
threetopsttdict["2017"]['TTTo2L2Nu_TuneCP5down'] ='/TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
threetopsttdict["2017"]['TTTo2L2Nu_TuneCP5up'] ='/TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
threetopsttdict["2017"]['TTTo2L2Nu_hdampUP'] ='/TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
threetopsttdict["2017"]['TTTo2L2Nu_hdampDOWN'] ='/TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
threetopsttdict["2017"]['TTTo2L2Nu_erdON'] ='/TTTo2L2Nu_TuneCP5_erdON_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'

ttbarbkgdict["2018"]['TTTo2L2Nu'] = '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
threetopsttdict["2018"]['TTTo2L2Nu_TuneCP5down'] = '/TTTo2L2Nu_TuneCP5down_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
threetopsttdict["2018"]['TTTo2L2Nu_TuneCP5up'] = '/TTTo2L2Nu_TuneCP5up_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
threetopsttdict["2018"]['TTTo2L2Nu_hdampUP'] ='/TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
threetopsttdict["2018"]['TTTo2L2Nu_hdampDOWN'] ='/TTTo2L2Nu_hdampDOWN_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
threetopsttdict["2018"]['TTTo2L2Nu_erdON'] ='/TTTo2L2Nu_TuneCP5_erdON_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'

# TT to hadronic
threetopsttdict["2016"]['TTToHadronic'] = '/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
threetopsttdict["2016"]['TTToHadronic_TuneCP5down'] = '/TTToHadronic_TuneCP5down_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
threetopsttdict["2016"]['TTToHadronic_TuneCP5up'] = '/TTToHadronic_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
threetopsttdict["2016"]['TTToHadronic_hdampDOWN'] = '/TTToHadronic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
threetopsttdict["2016"]['TTToHadronic_hdampUP'] = '/TTToHadronic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'

ttbarbkgdict["2017"]['TTToHadronic'] = '/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM'
threetopsttdict["2017"]['TTToHadronic_TuneCP5down'] = '/TTToHadronic_TuneCP5down_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
threetopsttdict["2017"]['TTToHadronic_TuneCP5up'] = '/TTToHadronic_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
threetopsttdict["2017"]['TTToHadronic_hdampUP'] ='/TTToHadronic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
threetopsttdict["2017"]['TTToHadronic_hdampDOWN'] ='/TTToHadronic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
threetopsttdict["2017"]['TTToHadronic_erdON'] ='/TTToHadronic_TuneCP5_erdON_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3/MINIAODSIM'

ttbarbkgdict["2018"]['TTToHadronic'] = '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
threetopsttdict["2018"]['TTToHadronic_TuneCP5down'] = '/TTToHadronic_TuneCP5down_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
threetopsttdict["2018"]['TTToHadronic_TuneCP5up'] = '/TTToHadronic_TuneCP5up_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
threetopsttdict["2018"]['TTToHadronic_hdampUP'] ='/TTToHadronic_hdampUP_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
threetopsttdict["2018"]['TTToHadronic_hdampDOWN'] ='/TTToHadronic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
threetopsttdict["2018"]['TTToHadronic_erdON'] ='/TTToHadronic_TuneCP5_erdON_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'

# TT to semi lepton
threetopsttdict["2016"]['TTToSemiLepton_HT500Njet9_TuneCP5down'] = '/TTToSemiLepton_HT500Njet9_TuneCP5down_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
threetopsttdict["2016"]['TTToSemiLepton_HT500Njet9_TuneCP5up'] = '/TTToSemiLepton_HT500Njet9_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
threetopsttdict["2016"]['TTToSemiLepton_HT500Njet9_hdampDOWN'] = '/TTToSemiLepton_HT500Njet9_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
threetopsttdict["2016"]['TTToSemiLepton_HT500Njet9_hdampUP'] = '/TTToSemiLepton_HT500Njet9_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'

threetopsttdict["2017"]['TTToSemiLepton_HT500Njet9'] = '/TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'

threetopsttdict["2018"]['TTToSemiLepton_HT500Njet9'] = '/TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'

# TT to semi leptonic
threetopsttdict["2016"]['TTToSemiLeptonic'] = '/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
threetopsttdict["2016"]['TTToSemiLeptonic_TuneCP5down'] = '/TTToSemiLeptonic_TuneCP5down_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
threetopsttdict["2016"]['TTToSemiLeptonic_TuneCP5up'] = '/TTToSemiLeptonic_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
threetopsttdict["2016"]['TTToSemiLeptonic_hdampDOWN'] = '/TTToSemiLeptonic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
threetopsttdict["2016"]['TTToSemiLeptonic_hdampUP'] = '/TTToSemiLeptonic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'

ttbarbkgdict["2017"]['TTToSemiLeptonic'] = '/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM'
threetopsttdict["2017"]['TTToSemiLeptonic_TuneCP5down'] = '/TTToSemiLeptonic_TuneCP5down_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
threetopsttdict["2017"]['TTToSemiLeptonic_TuneCP5up'] = '/TTToSemiLeptonic_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
threetopsttdict["2017"]['TTToSemiLeptonic_hdampUP'] ='/TTToSemiLeptonic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
threetopsttdict["2017"]['TTToSemiLeptonic_hdampDOWN'] ='/TTToSemiLeptonic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM'
threetopsttdict["2017"]['TTToSemiLeptonic_erdON'] ='/TTToSemiLeptonic_TuneCP5_erdON_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'

ttbarbkgdict["2018"]['TTToSemiLeptonic'] = '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
threetopsttdict["2018"]['TTToSemiLeptonic_TuneCP5down'] = '/TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
threetopsttdict["2018"]['TTToSemiLeptonic_TuneCP5up'] = '/TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
threetopsttdict["2018"]['TTToSemiLeptonic_hdampUP'] ='/TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
threetopsttdict["2018"]['TTToSemiLeptonic_hdampDOWN'] ='/TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
threetopsttdict["2018"]['TTToSemiLeptonic_erdON'] ='/TTToSemiLeptonic_TuneCP5_erdON_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'

#WJetsToLNu
bkghtdict["2016"]['WJetsHT200to400'] = '/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
bkghtdict["2016"]['WJetsHT200to400ext1'] = '/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'
bkghtdict["2016"]['WJetsHT200to400ext2'] = '/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2/MINIAODSIM'
bkghtdict["2016"]['WJetsHT400to600'] = '/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM' 
bkghtdict["2016"]['WJetsHT400to600ext1'] = '/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'
bkghtdict["2016"]['WJetsHT600to800'] = '/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
bkghtdict["2016"]['WJetsHT600to800ext1'] = '/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'
bkghtdict["2016"]['WJetsHT800to1200'] = '/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
bkghtdict["2016"]['WJetsHT800to1200ext1'] = '/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'
bkghtdict["2016"]['WJetsHT1200to2500'] = '/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM' 
bkghtdict["2016"]['WJetsHT1200to2500ext1'] = '/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'
bkghtdict["2016"]['WJetsHT2500toInf'] = '/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM' 
bkghtdict["2016"]['WJetsHT2500toInfext1'] = '/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'

bkghtdict["2017"]['WJetsHT200to400'] = '/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
bkghtdict["2017"]['WJetsHT400to600'] = '/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
bkghtdict["2017"]['WJetsHT600to800'] = '/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
bkghtdict["2017"]['WJetsHT800to1200'] = '/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
bkghtdict["2017"]['WJetsHT1200to2500'] = '/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
bkghtdict["2017"]['WJetsHT2500toInf'] = '/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3/MINIAODSIM'

bkghtdict["2018"]['WJetsHT200to400'] = '/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
bkghtdict["2018"]['WJetsHT400to600'] = '/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
bkghtdict["2018"]['WJetsHT600to800'] = '/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
bkghtdict["2018"]['WJetsHT800to1200'] = '/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
bkghtdict["2018"]['WJetsHT1200to2500'] = '/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
bkghtdict["2018"]['WJetsHT2500toInf'] = '/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'

#TTWJets
bkgdict["2016"]['TTW'] = '/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'
bkgdict["2016"]['TTWext1'] = '/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM'

bkgdict["2017"]['TTW'] = '/TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM'

bkgdict["2018"]['TTW'] = '/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM'

#TTZ
bkgdict["2016"]['TTZM10'] = '/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'
bkgdict["2016"]['TTZM10ext2'] = '/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM'
bkgdict["2016"]['TTZM10ext1'] = '/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext3-v1/MINIAODSIM'
bkgdict["2016"]['TTZM1to10'] = '/TTZToLL_M-1to10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'

bkgdict["2017"]['TTZM10'] = '/TTZToLLNuNu_M-10_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
bkgdict["2017"]['TTZM1to10'] = '/TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM'

bkgdict["2018"]['TTZM10'] = '/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM'
bkgdict["2018"]['TTZM1to10'] = '/TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'

#TTH
bkgdict["2016"]['TTHbb'] = '/ttHTobb_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
bkgdict["2016"]['TTHnonbb'] = '/ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'

bkgdict["2017"]['TTHbb'] = '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM'
bkgdict["2017"]['TTHnonbb'] = '/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM'

bkgdict["2018"]['TTHbb'] = '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v3/MINIAODSIM'
bkgdict["2018"]['TTHnonbb'] = '/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM'

# <<< diboson >>>
bkgdict["2016"]['WW'] = '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
bkgdict["2016"]['WWext'] = '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'
bkgdict["2016"]['WZ'] = '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
bkgdict["2016"]['WZext1'] = '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'
bkgdict["2016"]['ZZ'] = '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
bkgdict["2016"]['ZZext1'] = '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'

bkgdict["2017"]['WW'] = '/WW_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM'
bkgdict["2017"]['WZ'] = '/WZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
bkgdict["2017"]['ZZ'] = '/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM'

bkgdict["2018"]['WW'] = '/WW_TuneCP5_PSweights_13TeV-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
bkgdict["2018"]['WZ'] = '/WZ_TuneCP5_PSweights_13TeV-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
bkgdict["2018"]['ZZ'] = '/ZZ_TuneCP5_13TeV-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM'

# <<< data >>> 
datadict["2016"]['SingleElectronRun2016B']  = '/SingleElectron/Run2016B-17Jul2018_ver2-v1/MINIAOD'
datadict["2016"]['SingleElectronRun2016C']  = '/SingleElectron/Run2016C-17Jul2018-v1/MINIAOD'
datadict["2016"]['SingleElectronRun2016D']  = '/SingleElectron/Run2016D-17Jul2018-v1/MINIAOD'
datadict["2016"]['SingleElectronRun2016E']  = '/SingleElectron/Run2016E-17Jul2018-v1/MINIAOD'
datadict["2016"]['SingleElectronRun2016F']  = '/SingleElectron/Run2016F-17Jul2018-v1/MINIAOD'
datadict["2016"]['SingleElectronRun2016G']  = '/SingleElectron/Run2016G-17Jul2018-v1/MINIAOD'
datadict["2016"]['SingleElectronRun2016H']  = '/SingleElectron/Run2016H-17Jul2018-v1/MINIAOD'

datadict["2017"]['SingleElectronRun2017B']  = '/SingleElectron/Run2017B-31Mar2018-v1/MINIAOD'
datadict["2017"]['SingleElectronRun2017C']  = '/SingleElectron/Run2017C-31Mar2018-v1/MINIAOD'
datadict["2017"]['SingleElectronRun2017D']  = '/SingleElectron/Run2017D-31Mar2018-v1/MINIAOD'
datadict["2017"]['SingleElectronRun2017E']  = '/SingleElectron/Run2017E-31Mar2018-v1/MINIAOD'
datadict["2017"]['SingleElectronRun2017F']  = '/SingleElectron/Run2017F-31Mar2018-v1/MINIAOD'

datadict["2018"]['SingleElectronRun2018A']  = '/EGamma/Run2018A-17Sep2018-v2/MINIAOD'
datadict["2018"]['SingleElectronRun2018B']  = '/EGamma/Run2018B-17Sep2018-v1/MINIAOD'
datadict["2018"]['SingleElectronRun2018C']  = '/EGamma/Run2018C-17Sep2018-v1/MINIAOD'
datadict["2018"]['SingleElectronRun2018D']  = '/EGamma/Run2018D-PromptReco-v2/MINIAOD'

datadict["2016"]['SingleMuonRun2016B']  = '/SingleMuon/Run2016B-17Jul2018_ver2-v1/MINIAOD'
datadict["2016"]['SingleMuonRun2016C']  = '/SingleMuon/Run2016C-17Jul2018-v1/MINIAOD'
datadict["2016"]['SingleMuonRun2016D']  = '/SingleMuon/Run2016D-17Jul2018-v1/MINIAOD'
datadict["2016"]['SingleMuonRun2016E']  = '/SingleMuon/Run2016E-17Jul2018-v1/MINIAOD'
datadict["2016"]['SingleMuonRun2016F']  = '/SingleMuon/Run2016F-17Jul2018-v1/MINIAOD'
datadict["2016"]['SingleMuonRun2016G']  = '/SingleMuon/Run2016G-17Jul2018-v1/MINIAOD'
datadict["2016"]['SingleMuonRun2016H']  = '/SingleMuon/Run2016H-17Jul2018-v1/MINIAOD'

datadict["2017"]['SingleMuonRun2017B']  = '/SingleMuon/Run2017B-31Mar2018-v1/MINIAOD'
datadict["2017"]['SingleMuonRun2017C']  = '/SingleMuon/Run2017C-31Mar2018-v1/MINIAOD'
datadict["2017"]['SingleMuonRun2017D']  = '/SingleMuon/Run2017D-31Mar2018-v1/MINIAOD'
datadict["2017"]['SingleMuonRun2017E']  = '/SingleMuon/Run2017E-31Mar2018-v1/MINIAOD'
datadict["2017"]['SingleMuonRun2017F']  = '/SingleMuon/Run2017F-31Mar2018-v1/MINIAOD'

datadict["2018"]['SingleMuonRun2018A']  = '/SingleMuon/Run2018A-17Sep2018-v2/MINIAOD'
datadict["2018"]['SingleMuonRun2018B']  = '/SingleMuon/Run2018B-17Sep2018-v1/MINIAOD'
datadict["2018"]['SingleMuonRun2018C']  = '/SingleMuon/Run2018C-17Sep2018-v1/MINIAOD'
datadict["2018"]['SingleMuonRun2018D']  = '/SingleMuon/Run2018D-PromptReco-v2/MINIAOD'

datadict["2016"]['JetHTRun2016B']  = '/JetHT/Run2016B-17Jul2018_ver2-v2/MINIAOD'
datadict["2016"]['JetHTRun2016C']  = '/JetHT/Run2016C-17Jul2018-v1/MINIAOD'
datadict["2016"]['JetHTRun2016D']  = '/JetHT/Run2016D-17Jul2018-v1/MINIAOD'
datadict["2016"]['JetHTRun2016E']  = '/JetHT/Run2016E-17Jul2018-v1/MINIAOD'
datadict["2016"]['JetHTRun2016F']  = '/JetHT/Run2016F-17Jul2018-v1/MINIAOD'
datadict["2016"]['JetHTRun2016G']  = '/JetHT/Run2016G-17Jul2018-v1/MINIAOD'
datadict["2016"]['JetHTRun2016H']  = '/JetHT/Run2016H-17Jul2018-v1/MINIAOD'

datadict["2017"]['JetHTRun2017B']  = '/JetHT/Run2017B-31Mar2018-v1/MINIAOD'
datadict["2017"]['JetHTRun2017C']  = '/JetHT/Run2017C-31Mar2018-v1/MINIAOD'
datadict["2017"]['JetHTRun2017D']  = '/JetHT/Run2017D-31Mar2018-v1/MINIAOD'
datadict["2017"]['JetHTRun2017E']  = '/JetHT/Run2017E-31Mar2018-v1/MINIAOD'
datadict["2017"]['JetHTRun2017F']  = '/JetHT/Run2017F-31Mar2018-v1/MINIAOD'

datadict["2018"]['JetHTRun2018A'] = '/JetHT/Run2018A-17Sep2018-v1/MINIAOD'
datadict["2018"]['JetHTRun2018B'] = '/JetHT/Run2018B-17Sep2018-v1/MINIAOD'
datadict["2018"]['JetHTRun2018C'] = '/JetHT/Run2018C-17Sep2018-v1/MINIAOD'
datadict["2018"]['JetHTRun2018D'] = '/JetHT/Run2018D-PromptReco-v2/MINIAOD'

trigdictmc["2017"]['TTTo2L2Nu'] = '/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM'

# <<< 3 tops ttbar background >>>
threetopsttdict["2016"]['TTWH'] = '/TTWH_TuneCUETP8M2T4_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM'
threetopsttdict["2016"]['TTWW'] = '/TTWW_TuneCUETP8M2T4_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM'
threetopsttdict["2016"]['TTWZ'] = '/TTWZ_TuneCUETP8M2T4_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM'
threetopsttdict["2016"]['TTZZ'] = '/TTZZ_TuneCUETP8M2T4_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM'
threetopsttdict["2016"]['TTZH'] = '/TTZH_TuneCUETP8M2T4_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM'
threetopsttdict["2016"]['TTHH'] = '/TTHH_TuneCUETP8M2T4_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM'
threetopsttdict["2016"]['TTTT'] = '/TTTT_TuneCUETP8M2T4_PSweights_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
threetopsttdict["2016"]['TTTT_TuneCP5'] = '/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_correctnPartonsInBorn/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'

threetopsttdict["2017"]['TTWH'] = '/TTWH_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
threetopsttdict["2017"]['TTWW'] = '/TTWW_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM'
threetopsttdict["2017"]['TTWZ'] = '/TTWZ_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
threetopsttdict["2017"]['TTZZ'] = '/TTZZ_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
threetopsttdict["2017"]['TTZH'] = '/TTZH_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
threetopsttdict["2017"]['TTHH'] = '/TTHH_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
threetopsttdict["2017"]['TTTTnoPS'] = '/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM'
threetopsttdict["2017"]['TTTT'] =     '/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'

threetopsttdict["2018"]['TTWH'] = '/TTWH_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM'
threetopsttdict["2018"]['TTWWext1'] = '/TTWW_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM'
threetopsttdict["2018"]['TTWWext2'] = '/TTWW_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext2-v1/MINIAODSIM'
threetopsttdict["2018"]['TTWZ'] = '/TTWZ_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM'
threetopsttdict["2018"]['TTZZ'] = '/TTZZ_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM'
threetopsttdict["2018"]['TTZH'] = '/TTZH_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM'
threetopsttdict["2018"]['TTHH'] = '/TTHH_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM'
threetopsttdict["2018"]['TTTT'] = '/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM'
