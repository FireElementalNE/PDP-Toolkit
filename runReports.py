from reportFunctions import runReports,isRacketFile,shouldSkip
from sys import argv,exit
import os,re



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


