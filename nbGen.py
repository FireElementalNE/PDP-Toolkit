#!/usr/bin/env python
import os, datetime, platform
from CONFIG import WHOSTRING,NBGEN_FILENAME,NBGEN_DIR,LONG_NB

filename = NBGEN_FILENAME
date = datetime.datetime.now().strftime('%m/%d')
start = datetime.datetime.now().strftime('%H:%M')
stop = datetime.datetime.now().strftime('%H:%M')
who = WHOSTRING
interruptions = "0"
question = "1"
comments = " "
justChanged = False

def getInterruptions():
	if interruptions[0] == " ":
		return 0
	else:
		return eval(interruptions)

def getTimeOnTask():
	return (int(stop.split(":")[0]) - int(start.split(":")[0]))*60 + (int(stop.split(":")[1]) - int(start.split(":")[1])) - getInterruptions()

def printEntry():
	print "Date\tWho\tStart\tStop\tInterruptions\tQuestion\tTimeOnTask\tComments"
	print "%(date)s\t%(who)s\t%(start)s\t%(stop)s\t%(interruptions)s\t\t%(question)s\t\t%(timeOnTask)d\t\t%(comments)s" % \
		{"timeOnTask" : getTimeOnTask(), "date" : date, "who" : who, "start" : start, "stop" : stop, 
		 "interruptions": interruptions, 
		 "question" : question, 
		 "comments" : comments}

def printFile():
	print "="*30
	print "Contents of " + filename + " - "
	print open(NBGEN_DIR+filename,'r').read()
	print "="*30

def putFirstLine():	
	f = open(NBGEN_DIR+filename, 'w')
	f.write("Date\tWho\tStart\tStop\tInterruptions\tQuestion\tTimeOnTask\tComments\n")
	f.close()

def putEntry():
	f = open(NBGEN_DIR+filename, 'a')
	if LONG_NB:
		f.write("%(date)s\t%(who)s\t\t%(start)s\t%(stop)s\t%(interruptions)s\t\t\t\t%(question)s\t\t\t%(timeOnTask)d\t\t\t%(comments)s\n" % \
			{"timeOnTask" : getTimeOnTask(), "date" : date, "who" : who, "start" : start, "stop" : stop, 
		 	"interruptions": interruptions, 
		 	"question" : question, 
		 	"comments" : comments})
	else:
		f.write("%(date)s\t%(who)s\t%(start)s\t%(stop)s\t%(interruptions)s\t\t%(question)s\t\t%(timeOnTask)d\t\t%(comments)s\n" % \
			{"timeOnTask" : getTimeOnTask(), "date" : date, "who" : who, "start" : start, "stop" : stop, 
		 	"interruptions": interruptions, 
		 	"question" : question, 
		 	"comments" : comments})

	f.close()

	global start, stop
	start = datetime.datetime.now().strftime('%H:%M')
	stop = datetime.datetime.now().strftime('%H:%M')
	

def putGitEntry():
	f = open(NBGEN_DIR+filename,'a')
	f.write("============committing to git: %(date)s %(time)s ===================\n" % {"date" : date, "time" : datetime.datetime.now().strftime('%H:%M')})
	f.close()

def getTotals():
	contents = open(NBGEN_DIR+filename,'r').readlines()[1:] #Skip first line
	totals = {}
	for i in contents:
		if i[0:3] == "===" or len(i) < 5: #arbitrary 5 means not just a \n
			continue # skip git statements and empty lines
		theSplit = i.split()
		if theSplit[5] in totals:
			totals[theSplit[5]] = totals[theSplit[5]] + int(theSplit[6])
		else: 
			totals[theSplit[5]] = int(theSplit[6])
	return totals

def putTotals():
	totals = getTotals()
	f = open(NBGEN_DIR+filename, 'a')
	f.write("\n")
	for i in sorted(totals.iterkeys()):
		m = "%d" % totals[i]
		label = "Total Time On Task Q" + str(i) + " (minutes)"
		f.write(label + " "*(52-len(m)-len(label)) + m +"\n")
	for i in sorted(totals.iterkeys()):
		hAndT = "%.1f" % (float(totals[i])/60)
		label = "TOTQ" + str(i) + " (hours and tenths)"
		f.write(label + " "*(52-len(hAndT)-len(label)) + hAndT + "\n")
	f.close()

def clearScreen():
	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")

def vim():
	os.system("vim " + filename)

if __name__ == "__main__":
	clearScreen()
	while(True):
		if not(justChanged):
			stop = datetime.datetime.now().strftime('%H:%M')
		justChanged = False
		print "The current entry is:"
		printEntry()
		command = raw_input("Please enter a command:")
		theSplit = command.split()

		comm = ""
		arg = ""

		if len(theSplit) > 1:
			comm = theSplit[0]
			arg = command[(len(comm)+1):]
		else:
			comm = theSplit[0]

		try:

			if comm == "h" or comm == "help":
				print "Commands are:"
				print "\t(h)elp"
				print "\t(d)ate [date] - defaults to today"
				print "\t(w)ho [initials] - defaults to 'who' global"
				print "\tstart [time] - defaults to current time"
				print "\tstop [time] - defaults to current time"
				print "\t(i)nterruptions [num] - appends to current list with a '+', no args will clear"
				print "\t(q)uestion <question>"
				print "\t(c)omment <comment>"
				print "\t(pfl) - put first line (Date, Who, etc)"
				print "\t(p)ut - puts the entry in the file"
				print "\t(g)it - puts a git push entry in the file"
				print "\t(t)otal - adds totals to the end of the file"
				print "\t(f)ile <filename> - change the filename (and path)"
				print "\t(cls) - clear screen"
				print "\t(vim) - open the notebook in vim"
				print "\t(pf) - print the full file"
				print "\tquit/(e)xit"
				continue
			elif comm == "d" or comm == "date":
				date = arg
			elif comm == "w" or comm == "who":
				who = arg
			elif comm == "start":
				if len(arg) == 0:
					start = datetime.datetime.now().strftime('%H:%M')
				else:
					start = arg
			elif comm == "stop":
				if len(arg) == 0:
					stop = datetime.datetime.now().strftime('%H:%M')
				else:
					stop = arg
					justChanged = True
			elif comm == "i" or comm == "interruptions":
				if len(arg) == 0:
					interruptions = "0"
				elif interruptions[0] == "0":
					interruptions = arg
				else:
					interruptions = interruptions + "+" + arg
			elif comm == "q" or comm == "question":
				question = arg
			elif comm == "c" or comm == "comment":
				comments = arg
			elif comm == "pfl":
				putFirstLine()
			elif comm == "p" or comm == "put":
				putEntry()
			elif comm == "g" or comm == "git":
				putGitEntry()
			elif comm == "t" or comm == "total":
				putTotals()
			elif comm == "f" or comm == "file":
				filename = arg
			elif comm == "cls":
				clearScreen()
			elif comm == "vim":
				vim()
			elif comm == "pf":
				try:
					printFile()
				except IOError:
					print "File doesn't exist - use pfl to make it"
				continue
			elif comm == "quit" or comm == "e" or comm == "exit":
				break
			else:
				print "Invalid command"
				continue
			clearScreen()
		except:
			print "Invalid command\n"
