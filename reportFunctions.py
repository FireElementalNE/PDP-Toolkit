import re,datetime,os,platform
from CONFIG import *

myOS = platform.system()
slashDirection = '\\'
if myOS != 'Windows':
	slashDirection = '/'

def runReports(fullFileName, fileName, directory):
	FULLOUTPUTDIRNAME = directory+'ReportsOn'
	EQUALSSTRING = '='*NUMEQUALS+'\n'
	outFile = fileName[:-3] + 'Report'
	inFh = open(fullFileName,'r')
	if not os.path.isdir(FULLOUTPUTDIRNAME):
		os.mkdir(FULLOUTPUTDIRNAME)
	outFh = open(FULLOUTPUTDIRNAME+slashDirection+outFile,'w+')
	content = []
	with inFh as f:
			content = f.readlines()
	lineReport = runLineReport(content)
	commentReport = commentCodeRatio(content)
	theTime = datetime.datetime.now().strftime("%H:%M %B %d, %Y")
	outFh.write('Report on ' + fileName + '\n')
	outFh.write('Run on ' + theTime + '\n\n')
	outFh.write('LINE REPORT ' + '\n' + EQUALSSTRING)
	if lineReport[1] == 0:
		outFh.write(CONGRATSLINEMESSEGE + '\n' + '\n')
	else:
		outFh.write(lineReport[0])
	outFh.write('COMMENT/CODE REPORT ' + '\n' + EQUALSSTRING)
	outFh.write(commentReport)

def isRacketFile(fileName):
	racketRe = '^.*\.rkt$'
	if re.match(racketRe,fileName):
		return True
	return False

def runLineReport(content):
	lineNum = 1
	returnString = ''
	count = 0
	for x in content:
		if len(x) > 81 and lineNum > 3:
			returnString +=  str(lineNum-3) + ' is over 80 characters. got ' + x 
			count = count + 1
		lineNum = lineNum + 1
	return [returnString + '\n',count]

def commentCodeRatio(content):
	myRegex = '^;.*$'
	comments = 0.0
	code = 0.0
	empty = 0.0
	for x in content:
		if not re.match(myRegex,x) and len(x) > 1:
			code = code + 1.0
	codeToWaste = code/len(content)
	return 'Number of Lines with Code: ' + str(code) + '\n' + 'Total Lines: ' + str(len(content)) + '\n' + 'Code to total Ratio: ' + str(codeToWaste) + '\n'



