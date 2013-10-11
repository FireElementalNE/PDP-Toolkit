import reportFunctions,datetime
from CONFIG import *
from sys import argv,exit

try:
	inFile = argv[1] 
except IndexError:
	print 'usage: ' + argv[0] + ' <input file>'
	exit(0)

EQUALSSTRING = '='*NUMEQUALS+'\n'

inFh = open(inFile,'r') 
outFh = open(outFile,'w+')
content = []
with inFh as f:
		content = f.readlines()

lineReport = reportFunctions.runLineReport(content)
commentReport = reportFunctions.commentCodeRatio(content)

theTime = datetime.datetime.now().strftime("%H:%M %B %d, %Y")
outFh.write('Report on ' + argv[1] + '\n')
outFh.write('Run on ' + theTime + '\n\n')
outFh.write('LINE REPORT ' + '\n' + EQUALSSTRING)
outFh.write(lineReport)
outFh.write('COMMENT/CODE REPORT ' + '\n' + EQUALSSTRING)
outFh.write(commentReport)