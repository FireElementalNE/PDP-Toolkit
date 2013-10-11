import re

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



