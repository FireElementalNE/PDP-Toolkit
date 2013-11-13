import re,datetime,os,platform
import collections
import subprocess
from CONFIG import *

myOS = platform.system()
slashDirection = '\\'
if myOS != 'Windows':
	slashDirection = '/'

def runReports(fullFileName, fileName, directory):
	FULLOUTPUTDIRNAME = directory+'Reports'
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
	lambdaReport = lambdaAnalysis(content)
	theTime = datetime.datetime.now().strftime("%H:%M %B %d, %Y")
	outFh.write('Report on ' + fileName + '\n')
	outFh.write('Run on ' + theTime + '\n\n')
	outFh.write('LINE REPORT ' + '\n' + EQUALSSTRING)
	if lineReport[1] == 0:
		outFh.write(CONGRATSLINEMESSEGE + '\n' + '\n')
	else:
		outFh.write(lineReport[0])
	outFh.write('LAMBDA REPORT ' + '\n' + EQUALSSTRING)
	outFh.write(lambdaReport)
	outFh.write('COMMENT/CODE REPORT ' + '\n' + EQUALSSTRING)
	outFh.write(commentReport)

def runLineReport(content):
	lineNum = STARTAT
	returnString = ''
	count = 0
	for x in content:
		if len(x) > 81 and lineNum > 0:
			returnString +=  str(lineNum) + ' is over 80 characters. got ' + x 
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
		elif re.match(myRegex,x) and len(x) > 1:
			comments = comments + 1.0
		else:
			empty = empty + 1.0
	codeToWaste = code/len(content)
	codeLines = 'Number of Lines with Code:     ' + str(int(code))
	commentLines = 'Number of Lines with Comments: ' + str(int(comments))
	emptyLines = 'Number of Empty Lines:         ' + str(int(empty))
	return codeLines + '\n' + commentLines + '\n' + emptyLines + '\n' + 'Total Lines: ' + str(len(content)) + '\n' + 'Code to total Ratio: ' + str(codeToWaste) + '\n'

def lambdaAnalysis(content):
	badDict = {}
	lambdaRegex = '.*\(lambda.*'
	commentRegex = '.*\;'
	lineFixer = '^[\t\s]*(.*)\n$'
	lambdaCount = 0
	lambdaGood = 0
	lambdaBad = 0
	lineNum = STARTAT
	prevLine = None

	for x in content:
		if re.match(lambdaRegex,x):
			lambdaCount = lambdaCount + 1
			m = re.match(commentRegex,prevLine)
			if m:
				lambdaGood = lambdaGood + 1
			else:
				m = re.match(lineFixer,x)
				badDict[lineNum-1] = m.group(1)
				lambdaBad = lambdaBad + 1
			myFlag = True
		prevLine = x
		lineNum = lineNum + 1
	total = 'Found ' + str(lambdaCount) + ' lambda Functions' + '\n'
	good = None
	bad = None
	if lambdaGood == 1:
		good = str(lambdaGood) + ' is apparently all set' + '\n'
	else:
		good = str(lambdaGood) + ' are apparently all set' + '\n'
	if lambdaBad == 0:
		bad = CONGRATSLAMBDAMESSEGE + '\n'
	else:
		bad = str(lambdaBad) + ' of these have no contract and are as follows: ' + '\n'
	badString = ''
	badDict = collections.OrderedDict(sorted(badDict.items()))
	for key,value in badDict.iteritems():
		badString = badString + '\t' + 'line ' + str(key) + ' had this: ' + value + '\n'
	return total + good + bad + badString + '\n'

def runQualifications(directory,fileName):
	print 'RUNNING: ' + fileName
	proc = subprocess.Popen(['racket',directory+fileName],stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	print out





