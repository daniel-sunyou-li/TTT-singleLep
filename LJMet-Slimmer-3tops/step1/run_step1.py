import os,shutil,datetime,time
import getpass
from ROOT import *
from XRootD import client
xrdClient = client.FileSystem("root://brux11.hep.brown.edu:1094/")
execfile("/uscms_data/d3/jmanagan/EOSSafeUtils.py")

start_time = time.time()

#IO directories must be full paths

Year = 2018
finalStateYear = 'singleLep'+str(Year)
#inputDir='/isilon/hadoop/store/group/bruxljm/FWLJMET102X_1lep'+str(Year)+'_Jan2021/' # 2016
#inputDir='/eos/uscms/store/user/lpcljm/FWLJMET_crab_output/' #Extended signal and filtered hDamp/UE sample location for 2017 and 2018
inputDir='/eos/uscms/store/user/lpcljm/FWLJMET102X_1lep'+str(Year)+'_Oct2019/' # 2017 and 2018 on lpc
#inputDir='/isilon/hadoop/store/group/bruxljm/FWLJMET102X_1lep'+str(Year)+'_Oct2019/' # 2018 on brux
outputDir='/eos/uscms/store/user/ssagir/FWLJMET102X_1lep'+str(Year)+'_Oct2019_4t_032721_step1/nominal/'
condorDir='/uscms_data/d3/ssagir/FWLJMET102X_1lep'+str(Year)+'_Oct2019_4t_032721_step1/'
shifts = [] #['JECup','JECdown','JERup','JERdown']
nFilesPerJob=30
inputLoc='lpc'
if inputDir.startswith('/isilon/hadoop/'): inputLoc='brux'

csvFilename='DeepCSV_94XSF_V5_B_F.csv'
deepJetFilename='DeepFlavour_94XSF_V4_B_F.csv'
if Year==2018: 
  csvFilename='DeepCSV_102XSF_V2.csv'
  deepJetFilename='DeepJet_102XSF_V2.csv'
if Year==2016: 
  csvFilename='DeepCSV_2016LegacySF_V1.csv'
  deepJetFilename='DeepJet_2016LegacySF_V1.csv'
runDir=os.getcwd()
inDir=inputDir[10:]
if inputLoc=='brux': inDir=inputDir
outDir=outputDir[10:]

gROOT.ProcessLine('.x compileStep1.C')

print 'Starting submission'
count=0

dirList16 = [
#Samples to run in /isilon/hadoop/store/group/bruxljm/FWLJMET102X_1lep2016_Jan2021/
'DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8',
'ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
'ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
'ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
'SingleElectron',
'SingleMuon',
'TTHH_TuneCUETP8M2T4_13TeV-madgraph-pythia8',
'TTTJ_TuneCUETP8M2T4_13TeV-madgraph-pythia8',
'TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_correctnPartonsInBorn',
'TTTW_TuneCUETP8M2T4_13TeV-madgraph-pythia8',
'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8',
'TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8',
'TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToHadronic_TuneCP5down_PSweights_13TeV-powheg-pythia8',
'TTToHadronic_TuneCP5up_PSweights_13TeV-powheg-pythia8',
'TTToHadronic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToHadronic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToSemiLepton_HT500Njet9_TuneCP5down_PSweights_13TeV-powheg-pythia8',
'TTToSemiLepton_HT500Njet9_TuneCP5up_PSweights_13TeV-powheg-pythia8',
'TTToSemiLepton_HT500Njet9_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToSemiLepton_HT500Njet9_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToSemiLeptonic_TuneCP5down_PSweights_13TeV-powheg-pythia8',
'TTToSemiLeptonic_TuneCP5up_PSweights_13TeV-powheg-pythia8',
'TTToSemiLeptonic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToSemiLeptonic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTWH_TuneCUETP8M2T4_13TeV-madgraph-pythia8',
'TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8',
'TTWW_TuneCUETP8M2T4_13TeV-madgraph-pythia8',
'TTWZ_TuneCUETP8M2T4_13TeV-madgraph-pythia8',
'TTZH_TuneCUETP8M2T4_13TeV-madgraph-pythia8',
'TTZToLLNuNu_M-10_TuneCP5_PSweights_13TeV-amcatnlo-pythia8',
'TTZToLL_M-1to10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'TTZZ_TuneCUETP8M2T4_13TeV-madgraph-pythia8',
'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'WW_TuneCUETP8M1_13TeV-pythia8',
'WZ_TuneCUETP8M1_13TeV-pythia8',
'ZZ_TuneCUETP8M1_13TeV-pythia8',
'ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8',
'ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8',
]

dirList17 = [
#Samples to run in /store/user/lpcljm/FWLJMET102X_1lep2017_Oct2019/
'DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8',
'QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8',
'QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8',
'QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8',
'QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8',
'QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8',
'QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8',
'QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8',
'ST_s-channel_antitop_leptonDecays_13TeV-PSweights_powheg-pythia',
'ST_s-channel_top_leptonDecays_13TeV-PSweights_powheg-pythia',
'ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
'ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
'ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
'SingleElectron',
'SingleMuon',
'TTHH_TuneCP5_13TeV-madgraph-pythia8',
'TTTJ_TuneCP5_13TeV-madgraph-pythia8',
'TTTW_TuneCP5_13TeV-madgraph-pythia8',
'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8',
'TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8',
'TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToHadronic_TuneCP5down_PSweights_13TeV-powheg-pythia8',
'TTToHadronic_TuneCP5up_PSweights_13TeV-powheg-pythia8',
'TTToHadronic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToHadronic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToSemiLeptonic_TuneCP5down_PSweights_13TeV-powheg-pythia8',
'TTToSemiLeptonic_TuneCP5up_PSweights_13TeV-powheg-pythia8',
'TTToSemiLeptonic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToSemiLeptonic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTWH_TuneCP5_13TeV-madgraph-pythia8',
'TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8',
'TTWW_TuneCP5_13TeV-madgraph-pythia8',
'TTWZ_TuneCP5_13TeV-madgraph-pythia8',
'TTZH_TuneCP5_13TeV-madgraph-pythia8',
'TTZToLLNuNu_M-10_TuneCP5_PSweights_13TeV-amcatnlo-pythia8',
'TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8',
'TTZZ_TuneCP5_13TeV-madgraph-pythia8',
'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8',
'WW_TuneCP5_13TeV-pythia8',
'WZ_TuneCP5_13TeV-pythia8',
'ZZ_TuneCP5_13TeV-pythia8',
'ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8',
'ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8',
]
if '/store/user/lpcljm/FWLJMET_crab_output/' in inputDir: dirList17 = [
#Samples to run in /store/user/lpcljm/FWLJMET_crab_output/
'TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_correctnPartonsInBorn',
'TTToSemiLepton_HT500Njet9_TuneCP5down_PSweights_13TeV-powheg-pythia8',
'TTToSemiLepton_HT500Njet9_TuneCP5up_PSweights_13TeV-powheg-pythia8',
'TTToSemiLepton_HT500Njet9_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToSemiLepton_HT500Njet9_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8',
]

dirList18lpc = [
#Samples to run in /store/user/lpcljm/FWLJMET102X_1lep2018_Oct2019/
'DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8',
'QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8',
'QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8',
'QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8',
'QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8',
'QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8',
'QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8',
'QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8',
'ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8',
'ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8',
'ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8',
'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',
'ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',
'EGamma',
'SingleMuon',
'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8',
'TTTo2L2Nu_TuneCP5down_13TeV-powheg-pythia8',
'TTTo2L2Nu_hdampDOWN_TuneCP5_13TeV-powheg-pythia8',
'TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8',
'TTToHadronic_TuneCP5_13TeV-powheg-pythia8',
'TTToHadronic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8',
'TTToHadronic_hdampUP_TuneCP5_13TeV-powheg-pythia8',
'TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8',
'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8',
'TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8',
'TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',
'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8',
'TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8',
'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8',
'WW_TuneCP5_PSweights_13TeV-pythia8',
'WZ_TuneCP5_PSweights_13TeV-pythia8',
'ZZ_TuneCP5_13TeV-pythia8',
'ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8',
'ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8',
]
if '/store/user/lpcljm/FWLJMET_crab_output/' in inputDir: dirList18lpc = [
#Samples to run in /store/user/lpcljm/FWLJMET_crab_output/
'TTTT_TuneCP5_13TeV-amcatnlo-pythia8',
'TTToSemiLepton_HT500Njet9_TuneCP5down_13TeV-powheg-pythia8',
'TTToSemiLepton_HT500Njet9_TuneCP5up_13TeV-powheg-pythia8',
'TTToSemiLepton_HT500Njet9_hdampDOWN_TuneCP5_13TeV-powheg-pythia8',
'TTToSemiLepton_HT500Njet9_hdampUP_TuneCP5_13TeV-powheg-pythia8',
]
dirList18brux = [
'TTHH_TuneCP5_13TeV-madgraph-pythia8',
'TTTJ_TuneCP5_13TeV-madgraph-pythia8',
'TTTo2L2Nu_TuneCP5up_13TeV-powheg-pythia8',
'TTToHadronic_TuneCP5down_13TeV-powheg-pythia8',
'TTToHadronic_TuneCP5up_13TeV-powheg-pythia8',
'TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8',
'TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8',
'TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8',
'TTTT_TuneCP5_13TeV-amcatnlo-pythia8',
'TTTW_TuneCP5_13TeV-madgraph-pythia8',
'TTWH_TuneCP5_13TeV-madgraph-pythia8',
'TTWW_TuneCP5_13TeV-madgraph-pythia8',
'TTWZ_TuneCP5_13TeV-madgraph-pythia8',
'TTZH_TuneCP5_13TeV-madgraph-pythia8',
'TTZZ_TuneCP5_13TeV-madgraph-pythia8',
]

dirList = dirList17[:]
if Year==2018: 
  dirList = dirList18lpc[:]
  if inputLoc=='brux': dirList = dirList18brux[:]
if Year==2016:
  dirList = dirList16[:]

for sample in dirList:
    print "------------ Sample:",sample,"---------------"
    outList = ['none']
    if 'TTTT' in sample and '/store/user/lpcljm/FWLJMET_crab_output/' in inputDir and Year==2018: outList = ['ext']
    if 'Tprime' in sample: outList = ['BWBW','TZBW','THBW','TZTH','TZTZ','THTH']
    elif 'Bprime' in sample: outList = ['TWTW','BZTW','BHTW','BZBH','BZBZ','BHBH']
    elif 'TTToSemiLeptonic' in sample: outList = ['HT0Njet0','HT500Njet9']  # comment out for simple run
    #elif 'TTTo' in sample: outList = ['Mtt0to700','Mtt700to1000','Mtt1000toInf']
    #if 'TuneCP5down' in sample or 'TuneCP5up' in sample or 'hdampDOWN' in sample or 'hdampUP' in sample: outList = ['none']
    if 'TTTo' in sample or 'TT_Mtt' in sample: 
    	if outList==['none']: outList = ['ttbb','tt2b','tt1b','ttcc','ttjj']
    	else:
    		outList_ = outList[:]
    		outList = []
    		for outlabel in outList_:
    			for flv in ['ttbb','tt2b','tt1b','ttcc','ttjj']: outList.append(outlabel+'_'+flv)

    isData = False
    if 'Single' in sample or 'EGamma' in sample or 'JetHT' in sample: isData = True

    for outlabel in outList:
        tmpcount = 0

        outsample = sample+'_'+outlabel
        if outlabel == 'none': outsample = sample

        os.system('eos root://cmseos.fnal.gov/ mkdir -p '+outDir+outsample)
        for shift in shifts: os.system('eos root://cmseos.fnal.gov/ mkdir -p '+outDir.replace('nominal',shift)+outsample)
        os.system('mkdir -p '+condorDir+outsample)

        if inputLoc=='lpc':
        	runlist = EOSlistdir(inputDir+'/'+sample+'/'+finalStateYear+'/')
        elif inputLoc=='brux':
        	status, dirList = xrdClient.dirlist(inDir+'/'+sample+'/'+finalStateYear+'/')
        	runlist = [item.name for item in dirList]
        print "Running",len(runlist),"crab directories"

        for run in runlist:
            if Year==2018 and sample=='EGamma' and run=='191031_131344': continue # Skip old SingleElectronRun2018D
            if Year==2018 and sample=='SingleMuon' and run=='191031_131820': continue # Skip old SingleMuonRun2018D
            if inputLoc=='lpc':
            	numlist = EOSlistdir(inputDir+'/'+sample+'/'+finalStateYear+'/'+run+'/')
            elif inputLoc=='brux':
            	status, dirList = xrdClient.dirlist(inDir+'/'+sample+'/'+finalStateYear+'/'+run+'/')
            	numlist = [item.name for item in dirList]
            
            for num in numlist:
                numpath = inputDir+'/'+sample+'/'+finalStateYear+'/'+run+'/'+num
                pathsuffix = numpath.split('/')[-3:]
                pathsuffix = '/'.join(pathsuffix)

                if inputLoc=='lpc':
                	rootfiles = EOSlist_root_files(numpath)
                elif inputLoc=='brux':
                	status, fileList = xrdClient.dirlist(inDir+'/'+sample+'/'+finalStateYear+'/'+run+'/'+num+'/')
                	rootfiles = [item.name for item in fileList if item.name.endswith('.root')]
                if not rootfiles: #Check if rootfiles is empty list (remove failed jobs)
                    continue
                basefilename = (rootfiles[0].split('.')[0]).split('_')[:-1]
                basefilename = '_'.join(basefilename)
                print "Running path:",pathsuffix,"\tBase filenames:",basefilename

                for i in range(0,len(rootfiles),nFilesPerJob):
                    count+=1
                    tmpcount += 1

                  #  if tmpcount > 1: continue

                    segment1 = (rootfiles[i].split('.')[0]).split('_')[-1] ## 1-1
                    segment2 = (rootfiles[i].split('.')[0]).split('_')[-2] ## SingleElectronRun2017C

                    #if isData:    # need unique IDs across eras
                    #    idlist = segment2[-1]+segment1+' '
                    #    for j in range(i+1,i+nFilesPerJob):
                    #        if j >= len(rootfiles): continue
                    #        idparts = (rootfiles[j].split('.')[0]).split('_')[-2:]
                    #        idlist += idparts[0][-1]+idparts[1]+' '
                    #elif 'ext' in segment2:     # WON'T WORK in FWLJMET 052219, but ok since no samples need it
                    #    idlist = segment2[-4:]+segment1+' '
                    #    for j in range(i+1,i+nFilesPerJob):
                    #        if j >= len(rootfiles): continue
                    #        idparts = (rootfiles[j].split('.')[0]).split('_')[-2:]
                    #        idlist += idparts[0][-4:]+idparts[1]+' '
                    #else:
                    idlist = segment1+' '
                    for j in range(i+1,i+nFilesPerJob):
                        if j >= len(rootfiles): continue
                        idlist += (rootfiles[j].split('.')[0]).split('_')[-1]+' '
                        
                    idlist = idlist.strip()
                    #remove the problematic 2018 fwljmet jobs
                    if Year==2018 and sample=='ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8':
                    	problematicIDs = ['1048','1177','1217','1412','1413','1414','1415','1416','1417','1418','1419','1429','1441','1664','1883']
                    	for id_ in problematicIDs:
                    		idlist = idlist.replace(id_,'').replace('  ',' ')
                    print "Running IDs",idlist
                
                    dict={'RUNDIR':runDir, 'SAMPLE':sample, 'INPATHSUFFIX':pathsuffix, 'INPUTDIR':inDir, 'FILENAME':basefilename, 'OUTFILENAME':outsample, 'OUTPUTDIR':outDir, 'LIST':idlist, 'ID':tmpcount, 'YEAR':Year, 'CSVFILE':csvFilename, 'DEEPJETFILE':deepJetFilename}
                    jdfName=condorDir+'/%(OUTFILENAME)s/%(OUTFILENAME)s_%(ID)s.job'%dict
                    print jdfName
                    jdf=open(jdfName,'w')
                    jdf.write(
                        """use_x509userproxy = true
universe = vanilla
Executable = %(RUNDIR)s/makeStep1.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = %(RUNDIR)s/compileStep1.C, %(RUNDIR)s/makeStep1.C, %(RUNDIR)s/step1.cc, %(RUNDIR)s/step1.h, %(RUNDIR)s/HardcodedConditions.cc, %(RUNDIR)s/HardcodedConditions.h, %(RUNDIR)s/BTagCalibForLJMet.cpp, %(RUNDIR)s/BTagCalibForLJMet.h, %(RUNDIR)s/%(CSVFILE)s, %(RUNDIR)s/%(DEEPJETFILE)s
Output = %(OUTFILENAME)s_%(ID)s.out
Error = %(OUTFILENAME)s_%(ID)s.err
Log = %(OUTFILENAME)s_%(ID)s.log
Notification = Never
Arguments = "%(FILENAME)s %(OUTFILENAME)s %(INPUTDIR)s/%(SAMPLE)s/%(INPATHSUFFIX)s %(OUTPUTDIR)s/%(OUTFILENAME)s '%(LIST)s' %(ID)s %(YEAR)s"
Queue 1"""%dict)
                    jdf.close()
                    os.chdir('%s/%s'%(condorDir,outsample))
                    os.system('condor_submit %(OUTFILENAME)s_%(ID)s.job'%dict)
                    os.system('sleep 0.5')                                
                    os.chdir('%s'%(runDir))
                    print count, "jobs submitted!!!"
        
print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))
