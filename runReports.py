
from reportFunctions import runReports,isRacketFile
from sys import argv,exit
import os

try:
	directory = argv[1] 
except IndexError:
	print 'usage: ' + argv[0] + ' <input file>'
	exit(0)

for root, dirnames, filenames in os.walk(directory):
	for filename in filenames:
		if isRacketFile(filename):
			fh = open(os.path.join(root,filename))
			runReports(directory+filename,filename)


