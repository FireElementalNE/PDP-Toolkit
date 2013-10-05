from sys import argv
import datetime

try:
	inFile = argv[1] 
	outFile = argv[2]
except IndexError:
	print 'usage: ' + argv[0] + ' <input file> <output file>'

outFh = open(outFile,'w+')
theTime = datetime.datetime.now().strftime("%H:%M %B %d, %Y")
outFh.write('Line Number Report on ' + argv[1] + '\n')
outFh.write('Run on ' + theTime + '\n')

lineNum = 1
content = []
with open(inFile,'r') as f:
    content = f.readlines()

for x in content:
	if len(x) > 81 and lineNum > 3:
		outFh.write(str(lineNum) + ' is over 80 characters. got ' + x )
	lineNum = lineNum + 1

outFh.close()

