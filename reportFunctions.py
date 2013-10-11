import re,datetime,os
from CONFIG import *

def runReports(fullFileName, fileName, directory):
	FULLOUTPUTFILENAME = 'ReportsOn-'+directory[:-1]
	EQUALSSTRING = '='*NUMEQUALS+'\n'
	outFile = fileName[:-3] + 'Report'
	inFh = open(fullFileName,'r')
	if not os.path.isdir(FULLOUTPUTFILENAME):
		os.mkdir(FULLOUTPUTFILENAME)
	outFh = open(FULLOUTPUTFILENAME+'/'+outFile,'w+')
	content = []
	with inFh as f:
			content = f.readlines()
	lineReport = runLineReport(content)
	commentReport = commentCodeRatio(content)

	theTime = datetime.datetime.now().strftime("%H:%M %B %d, %Y")
	outFh.write('Report on ' + fileName + '\n')
	outFh.write('Run on ' + theTime + '\n\n')
	outFh.write('LINE REPORT ' + '\n' + EQUALSSTRING)
	outFh.write(lineReport)
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
	for x in content:
		if len(x) > 81 and lineNum > 3:
			returnString +=  str(lineNum-3) + ' is over 80 characters. got ' + x 
		lineNum = lineNum + 1
	return returnString + '\n'

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



