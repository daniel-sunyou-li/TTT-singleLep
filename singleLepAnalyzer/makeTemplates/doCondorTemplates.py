#!/usr/bin/python

import os,sys,datetime,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from utils import *

thisDir = os.getcwd()
outputDir = thisDir+'/'

year=sys.argv[1]
region='SR' #PS,SR,TTCR,WJCR
categorize=1 #1==categorize into t/W/b/j, 0==only split into flavor

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
if region=='TTCR': pfix='ttbar'
elif region=='WJCR': pfix='wjets'
else: pfix='templates'
if not categorize: pfix='kinematics_'+region
pfix+='_'+year+'_'+sys.argv[3]#+date#+'_'+time

iPlotList = [#distribution name as defined in "doHists.py"
sys.argv[2],
]

isEMlist  = ['E','M']
nhottlist = ['0','1','2p']
nttaglist = ['0p']
nWtaglist = ['0','1p']
nbtaglist = ['2','3p']
njetslist = ['5','6','7','8p']

# baseline categories
#isEMlist  = ['E','M']
#nhottlist = ['0p']
#nttaglist = ['0p']
#nWtaglist = ['0p']
#nbtaglist = ['2p']
#njetslist = ['4p']

if not categorize: 	
	nhottlist = ['0p']
	nttaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['2p']
	njetslist = ['4p']
catList = list(itertools.product(isEMlist,nhottlist,nttaglist,nWtaglist,nbtaglist,njetslist))
	
outDir = outputDir+pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
if year=='R16': 
	os.system('cp ../weights16.py ../weights.py')
	os.system('cp ../samples16.py ../samples.py')
if year=='R17': 
	os.system('cp ../weights17.py ../weights.py')
	os.system('cp ../samples17.py ../samples.py')
elif year=='R18': 
	os.system('cp ../weights18.py ../weights.py')
	os.system('cp ../samples18.py ../samples.py')
os.system('cp ../analyze.py ../weights.py ../samples.py ../utils.py doHists.py doCondorTemplates.py doCondorTemplates.sh '+outDir+'/')
os.chdir(outDir)

count=0
for iplot in iPlotList:
	for cat in catList:
		if skip(cat): continue #check the "skip" function in utils module to see if you want to remove specific categories there!!!
		catDir = cat[0]+'_nHOT'+cat[1]+'_nT'+cat[2]+'_nW'+cat[3]+'_nB'+cat[4]+'_nJ'+cat[5]
		print "iPlot: "+iplot+", cat: "+catDir
		if (int(cat[1][0])+int(cat[2][0])+int(cat[3][0])+int(cat[4][0])) > int(cat[5][0]):
			print( "{} is not topologically possible, skipping...".format( catDir ) )
			continue
		if (int(cat[5][0])==5) and ( ( int(cat[1][0])+int(cat[2][0])+int(cat[3][0])+int(cat[4][0]) ) > 3 ): 
			print( "{} has too few signal yield, skipping...".format( catDir ) )
			continue
		if not os.path.exists(outDir+'/'+catDir): os.system('mkdir '+catDir)
		os.chdir(catDir)
	
		dict={'dir':outDir,'iPlot':iplot,'region':region,'isCategorized':categorize,'year':year,
			  'isEM':cat[0],'nhott':cat[1],'nttag':cat[2],'nWtag':cat[3],'nbtag':cat[4],'njets':cat[5],'step1dir':sys.argv[4],
			  'exeDir':thisDir}
	
		jdf=open('condor_'+iplot+'.job','w')
		jdf.write(
"""universe = vanilla
Executable = %(dir)s/doCondorTemplates.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
request_memory = 5000
Output = condor_%(iPlot)s.out
Error = condor_%(iPlot)s.err
Log = condor_%(iPlot)s.log
JobBatchName = SLA_step1_DNN250
Notification = Error
Arguments = %(dir)s %(iPlot)s %(region)s %(isCategorized)s %(year)s %(isEM)s %(nhott)s %(nttag)s %(nWtag)s %(nbtag)s %(njets)s %(step1dir)s
Queue 1"""%dict)
		jdf.close()
		os.system('condor_submit condor_'+iplot+'.job')
		os.chdir('..')
		count+=1

print "Total jobs submitted:", count
