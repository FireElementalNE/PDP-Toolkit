from reportFunctions import runReports,runQualifications
from sys import argv,exit
from CONFIG import PROBLEMSET
import os,re,urllib

def isRacketFile(fileName):
	racketRe = '^.*\.rkt$'
	return re.match(racketRe,fileName)

def shouldSkipExtra(fileName):
	skipRegex = '^extras\.rkt$'
	return re.match(skipRegex,fileName)

def shouldSkipQual(fileName):
	skipRegex = '^ps\d{2}\-[\w\-\d]*qualification\.rkt$'
	return re.match(skipRegex,fileName)

try:
	directory = argv[1] 
except IndexError:
	print 'usage: ' + argv[0] + ' <input directory>'
	exit(0)

for root, dirnames, filenames in os.walk(directory):
	for filename in filenames:
		if isRacketFile(filename) and not shouldSkipExtra(filename) and not shouldSkipQual(filename):
			fh = open(os.path.join(root,filename))
			runReports(directory+filename,filename,directory)
		if shouldSkipQual(filename):
			runQualifications(directory,filename)

myPS = None
if PROBLEMSET > 9:
	myPS = 'ps'	+ str(PROBLEMSET)
else:
 myPS = 'ps0' + str(PROBLEMSET)

fh = open(directory+myPS+'-provides','w+')
content = urllib.urlopen('http://www.ccs.neu.edu/course/cs5010f13/problem-sets/' + myPS + '.html').read()
providesRegex = '([\w\d\-\?]*)\s\:\s'
allprivides = re.findall(providesRegex,content)


for x in allprivides:
	fh.write('(provide ' + x + ')\n')

fh.close()	



