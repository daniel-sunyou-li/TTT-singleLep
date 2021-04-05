import os,sys,shutil,datetime,time
import getpass
from ROOT import *

start_time = time.time()
shift = sys.argv[1]

#IO directories must be full paths
foldnum = '-1'
relbase   = '/home/wzhang/work/fwljmet_201905/CMSSW_10_2_16_UL/'
inputDir  = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_02162021_step1hadds/'+shift+'/'
#inputDir  = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2016_Feb2020_4t_080420_step1hadds/'+shift+'/'
# outputDir = '/mnt/hadoop/users/jlee/TTTT/LJMet94X_1lepTT_022219_step2/'+shift+'/'
outputDir = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_03062021_step2/'+shift+'/'
runDir=os.getcwd()
gROOT.ProcessLine('.x compileStep2.C')

cTime=datetime.datetime.now()
date='%i_%i_%i_%i_%i_%i'%(cTime.year,cTime.month,cTime.day,cTime.hour,cTime.minute,cTime.second)

condorDir=runDir+'/'+outputDir.split('/')[-3]+'_condorLogs/'+shift+'/'
print 'Starting submission'
count=0

rootfiles = os.popen('ls '+inputDir)
os.system('mkdir -p '+outputDir)
os.system('mkdir -p '+condorDir)

for file in rootfiles:
    if 'root' not in file: continue
#    if 'TTTT' in file: continue
#    if 'TTTo' in file: continue
    rawname = file[:-6]
    count+=1
    dict={'RUNDIR':runDir, 'CONDORDIR':condorDir, 'INPUTDIR':inputDir, 'FILENAME':rawname, 'CMSSWBASE':relbase, 'OUTPUTDIR':outputDir}
    jdfName=condorDir+'/%(FILENAME)s.job'%dict
    print jdfName
    jdf=open(jdfName,'w')
    jdf.write(
"""universe = vanilla
Executable = %(RUNDIR)s/makeStep2.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
request_memory = 3072
Transfer_Input_Files = %(RUNDIR)s/HT_njets_SF_4tops_dcsv_djet.root, %(RUNDIR)s/S2HardcodedConditions.cc, %(RUNDIR)s/S2HardcodedConditions.h, %(RUNDIR)s/makeStep2.C, %(RUNDIR)s/step2.cc, %(RUNDIR)s/step2.h, %(RUNDIR)s/step2_cc.d, %(RUNDIR)s/step2_cc.so, %(RUNDIR)s/Davismt2.cc, %(RUNDIR)s/Davismt2.h, %(RUNDIR)s/Davismt2_cc.d, %(RUNDIR)s/Davismt2_cc.so
Output = %(FILENAME)s.out
Error = %(FILENAME)s.err
Log = %(FILENAME)s.log
JobBatchName = step2_wzhang
Notification = Never
Arguments = %(FILENAME)s.root %(FILENAME)s.root %(INPUTDIR)s %(OUTPUTDIR)s
Queue 1"""%dict)
    jdf.close()
    os.chdir('%s/'%(condorDir))
    os.system('condor_submit %(FILENAME)s.job'%dict)
    os.system('sleep 0.5')                                
    os.chdir('%s'%(runDir))
    print count, "jobs submitted!!!"
    break 

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))
