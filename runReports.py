from reportFunctions import runReports,isRacketFile,shouldSkip
from sys import argv,exit
from CONFIG import PROBLEMSET
import os,re,urllib



try:
	directory = argv[1] 
except IndexError:
	print 'usage: ' + argv[0] + ' <input directory>'
	exit(0)

for root, dirnames, filenames in os.walk(directory):
	for filename in filenames:
		if isRacketFile(filename) and not shouldSkip(filename):
			fh = open(os.path.join(root,filename))
			runReports(directory+filename,filename,directory)

myPS = None
if PROBLEMSET > 9:
	myPS = 'ps'	+ str(PROBLEMSET)
else:
 myPS = 'ps0' + str(PROBLEMSET)

fh = open(directory+myPS+'-provides','w+')
content = urllib.urlopen('http://www.ccs.neu.edu/course/cs5010f13/problem-sets/' + myPS + '.html').read()
providesRegex = '\<pre\>([\w\d\-]*)\s\:\s'
allprivides = re.findall(providesRegex,contetn)
print allprivides




