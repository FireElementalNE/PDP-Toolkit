#!/usr/bin/env python
import sys, re
from CONFIG import COMMENTSTYLE
'''
How to use me:

Usage: ./thisfile Filename.rkt

Parses through all comments in racket code and looks for sections that begin with ";;Examples:" and end with ";;Design Strategy:"
It then takes those lines, looks for an equal sign, and throws both sides as new lines at the end of the file. 
It also takes any other comments in those sections and translates them down to the bottom as well.
There may be some extra new lines but at least you don't have to copy and paste by hand.

Here's an example case:

MyFile.rkt -

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;FUNCTIONS

;;double : Number -> Number
;;GIVEN: a number
;;RETURN: that same number, doubled
;;Examples:
;;My comment here-
;; (double 2) = 4
;;My next comment-
;; (double 8) = 16
;;My final comment-
;; (double 42) = 84
(define (double x)
    (* x 2))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;TESTS

[originally empty, but after running ./thisfile MyFile.rkt it adds the following]

;;My comment here-
(double 2)
4

;;My next comment-
(double 8)
16

;;My final comment-
(double 42)
84

You can then proceed to copy+paste your heart out with "(check-equals?" and "This failed because you suck")

I would have done more to automatically add those parts but the logic was getting unwieldly. 

Enjoy!
-d1r3w0lf

'''

#Opens the given filename and converts all examples (in comments) 
def main(filename):
	f = open(filename, "r")
	contents = f.read().split(";;Examples:")
	f.close()

	f = open(filename, "a")
	for i in xrange(len(contents)):
		if i == 0:
			continue
		group = contents[i].split(";;Design Strategy:")[0]
		lines = group.split("\n")
		# print group
		for x in lines:
			if x[0:3] != COMMENTSTYLE and len(x) > 1: # a comment - throw it at the end
				f.write(x + "\n")
				# print "comment is: " + "'" + x + "'"
			else:
				for part in x.split("="):
					f.write(part.replace(";;","") + "\n")


	f.close()


def usage(myName):
	print "Usage:\n\t%s Filename.rkt" % myName

if __name__ == '__main__':
	if len(sys.argv) != 2:
		usage(sys.argv[0])
	else:
		main(sys.argv[1])
