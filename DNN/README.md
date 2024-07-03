# Triple-Top Search in the Single-Lepton Final State: Classification DNN  -- Quick Start Instructions #
This repository contains code for producing step3 `.root` files used in calculating the limits for the single-lepton final state in triple-top quark events. The step3 outputs can also be used for a data-driven background estimation method [ABCDnn]([url](https://github.com/daniel-sunyou-li/ABCDnn)). The code is partitioned into four steps:

1. [__Variable Importance Calculation__](#Submit-Variable-Importance-Condor-Jobs)
2. [__Hyper Parameter Optimization__](#Run-the-Hyper-Parameter-Optimization)
3. [__k-Fold Cross Validation Training__](#Run-the-k-fold-Cross-Validation)
4. [__step3 `.root` File Production__](#Submit-Step3-Condor-Jobs)

The step3 files are to be used by the [singleLepAnalyzer](https://github.com/daniel-sunyou-li/TTT-singleLep/tree/UL/singleLepAnalyzer) to produce the limits. The TTTT DNN code is intended to be run on the LPC while the singleLepAnalyzer is intended to be run on the Brown Linux server (BRUX).  To run all the code successfully, you will need to have accounts on BRUX, FNAL LPC and CERN LXPLUS.  You will also need storage requested on [CMSEOS](https://uscms.org/uscms_at_work/computing/LPC/usingEOSAtLPC.shtml#createEOSArea) and have a working [CERN grid certificate](https://uscms.org/uscms_at_work/computing/getstarted/get_grid_cert.shtml). The general-use instructions are as follows:

## Setup on LPC
Sign-in to the LPC using your FNAL [username]

    kinit -f [username]@FNAL.GOV
    ssh -xy [username]@cmslpc-el9.fnal.gov
    
Install `scikit-optimize` (`skopt`) for hyper parameter optimization:

    pip install --user scikit-optimize  

Setup the `CMSSW` environment (__Note__: `CMSSW_13_3_0` is used rather than `CMSSW_10_6_29` for compatability reasons with cmslpc-el9. There is no dependency on the CMSSW version, it is only run in CMSSW to use ROOT for I/O.)

    source /cvmfs/cms.cern.ch/cmsset_default.csh
    cmsrel CMSSW_13_3_0
    cd CMSSW_13_3_0/src/
    git clone https://github.com/daniel-sunyou-li/TTT-singleLep.git
    cd src/TTT-singleLep/DNN/
    
Depending on the step being run, set-up the `DNN` environment with the commands listed in `env/start.txt`.

Edit `config.py` to define user and variable parameters. Make sure that the following are in agreement with your `step2` samples:
* `postfix`
* `FWLJMet` paths for BRUX, LPC, EOS, etc.
    
## Submit Variable Importance Condor Jobs
Setup the environment for submitting the Condor jobs (can find again in `env/start.txt.`.)

    source /cvmfs/cms.cern.ch/cmsset_default.csh # or .sh for bash
    cmsenv
    
Note that after running these source commands, you will not be able to upload files to CMSEOS.  You will need to restart the console and follow the previous steps. Submit _n_ seed Condor jobs.  The `.job`, `.log`, `.out` and `.err` files are stored in the directory `condor_log_[day].[month].[year]`. The submission options include:
* `-y` (year) = 16, 16APV, 17, 18 or Run2
* `-c` (correlation threshold) = 0 to 100, 60 (recommended)
* `-n` (number of seeds) = 100 (recommended)
* `--test` (submit only one job, optional)
* `-nj` (jet multiplicity cut $\geq$) = 4 (default)
* `-nb` (b-jet multiplicity cut $\geq$) = 1 (default)
* `-ht` ($H_T$ >) = 390 (default)
* `-lpt` (lepton $p_T$ >) = 20 (default)
* `-met` (missing transverse momentum >) = 20 (default)
* `-mt` (transverse mass of lepton and missing transverse momentum >) = 0 (default)
* `-dr` (minimum $\Delta r$ between lepton and jet) = 0.2 (default)

Submit the jobs using (as an example):

    python3 submit_vi_condor.py -y Run2 -n 100 -c 60 -nj 4 -nb 1 

While the jobs run, check on the progress using:
 
    python3 process_condor_log.py <condor log directory>
    
if there are any failed jobs, resubmit with:

    python3 submit.py -y Run2 --resubmit <condor log directory>

## Run the Variable Importance Calculation
After all your jobs have finished, calculate the variable importance.  First, compact all of the Condor results to a `.jtd` file with:

    python3 process_condor_log.py <condor log directory> -c
    
At this point, it's recommended to move all the `.jtd` files for a set of seeds with a similar selection into one directory:

    mkdir seed_output
    mv *.jtd seed_output
    
Run the calculation script and save the results to a similarly named directory

    mkdir dataset
    python3 calculate_vi.py -f dataset seed_output
    
The results produced are used automatically in the following steps.
    
## Run the Hyper Parameter Optimization
Hyper parameter optimization is used to optimize the performance of a neural network by tuning the network architecture for a given number of input variables using the `scikit-optimize` library.  The input variables are grouped based on their ranking, determined in the previous step.  For this step, it is important _not_ to run the previous `source` command and `cmsenv`. The main option to set for this step is `-n` (number of variables) = `1` to `X`, the recommended number is to include all variables that have a non-zero, positive significance value. You can also customize the hyper parameter phase space surveyed in `config.py` including how many optimization steps are used. Other running options include:
* `dataset` (positional) = folder where the variable importance results are stored
* `-n` (number of variables) = `1` to `X` where `X` is the total number of variables in the variable importance ranking list
* `-r` (signal-to-background ratio) = `1` (recommended) or `-1` to use all samples available
* `-t` (tag) = postfix to add to the new DNN branch to be produced
* `--Run2` (optional) = run the training over samples from all eras
* `--override` (optional) = produce a new `.root` file with all the selected events    

        source /cvmfs/cms.cern.ch/cmsset_default.csh
        source /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc12-opt/setup.csh
        source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.32.02/x86_64-almalinux9.4-gcc114-opt/bin/thisroot.csh
        python nn_hyperopt.py -n 50 -r 1 -t 3t dataset_4j_2017/ --Run2 
 
## Run the k-fold Cross Validation
After determining an optimal set of hyper parameters, with the results stored in a directory of the form `dataset`, run the k-fold cross validation to obtain statistics on the model performance. The important running options include: 
* `-d` (dataset) = folder containing the hyper parameter optimization results
* `-f` (folder) = folder to store the output of the k-fold CV training
* `-k` (folds) = 10 (recommended) number of partitions for the training/validation events
* `-m` (metric) = AUC (recommended) which metric to use for determining best model


The command is:

        python3 nn_final.py -k 10 -f dataset/1to50/ -d dataset/1to50/ -m AUC
    
After this step finishes, the model with the best performance out of the `k` folds is saved in `/dataset_4j_2017/1to50/` and will be applied to the produce the step3 files on Condor. 

## Submit Step3 Condor Jobs
The step3 files will be stored on cmslpc EOS. The step3 script can take multiple models so the step3 file can hold multiple discriminators for different sets of jet cuts and number of input variables. Some options include:
* `y` (year) = 16APV, 16, 17 or 18
* `-l` (optional) = name of the condor log directory
* `-i` (location of input files) = LPC or BRUX
* `-o` (location of output files) = LPC or BRUX (cannot transfer from LPC to BRUX, but checks if files are stored on BRUX)
* `--resubmit` (optional) = resubmit failed jobs
* `--test` (optional) = only submit a single job
* `--shift` (optional) = process the JEC reduced systematic samples

  
The command is:

    python3 application.py -y <16APV/16/17/18> -i BRUX -o LPC 
    
The Condor jobs can be checked directly by checking the Condor job outputs:

    ls application_log_2017/*.out | wc # the number of finished jobs
    ls application_log_2017/*.log | wc # the total number of jobs
    
Once jobs are finished, you will find the step3 files stored on cmslpc EOS at:

    eosls /store/user/[EOS Username]/FWLJMET106X_singleLep<year>UL_RunIISummer20_<tag>_step3/<shift>/
    
where `shift` can be `nominal`, or one of many JEC reduced systematics. After finishing producing the step3 files, refer to the [`singleLepAnalyzer`](https://github.com/daniel-sunyou-li/TTT-singleLep/tree/UL/singleLepAnalyzer) subdirectory for instructions for running on BRUX.
    
