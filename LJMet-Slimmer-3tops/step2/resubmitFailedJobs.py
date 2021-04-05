#!/usr/bin/python

import os, sys, fnmatch
import math

inDir = '/user_data/jlee/chargedHiggs/CMSSW_7_4_7/src/FOR_EPS2017/slimmers/step2_htb_Moriond17_newIDtrig/LJMet80X_1lep_100217_step2_xsecEffFixed_condorLogs/nominal'
shifts = ['nominal']#,'JERup','JERdown','JECup','JECdown']

currentDir = os.getcwd()

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)

grandTot = 0
for shift in shifts:
	inputDir = inDir.replace('nominal',shift)
	logfilelist = []
	for logfile in findfiles(inputDir, '*.log'):
		logfilelist.append(logfile)

	print shift, len(logfilelist)
	i=0
	for file in logfilelist:
		relPath = file.replace(inputDir,'')
		jFile = file.replace('.log','.job')
		lFile = file
		eFile = file.replace('.log','.err')
		oFile = file.replace('.log','.out')
		rFile = file.split('/')[-1].replace('.log','.root')
		#statement1 = os.path.exists(rFile)
		#statement2 = True
		#if statement1: statement2 = os.path.getsize(rFile)>1000
		if not os.path.exists(oFile): statement2 = False
		if os.path.exists(oFile): 
			outFdata = open(oFile).read()
			statement2 = 'DONE' in outFdata
		if not os.path.exists(eFile): statement3 = False
		if os.path.exists(eFile): 
			errFdata = open(eFile).read()
			statement3 = not ('error' in errFdata or 'Error' in errFdata) or len(errFdata.split())>25
		if not os.path.exists(lFile): statement4 = False
		if os.path.exists(lFile):
			logFdata = open(lFile).read()
			statement4 = ('Normal termination (return value 0)' in logFdata)
		statement = statement2 and statement3 and statement4
		if not statement:
			print "*" * 40
			print ">cd " + file.replace(file.split('/')[-1],'')
			os.chdir(file.replace(file.split('/')[-1],''))
			print ">condor_submit " + jFile
# 			os.system('rm ' + lFile)
# 			os.system('rm ' + eFile)
# 			os.system('rm ' + oFile)
# 			os.system('condor_submit ' + jFile)
			print "*" * 40
			i+=1
	print i, "jobs resubmitted from",shift
	grandTot+=i
print grandTot, "total jobs resubmitted!!!"
