import sys

script, input_file = sys.argv

def print_all(f):
	print f.read()

def rewind (f):
	f.seek(0)

def printline (lineCount, f):
	print lineCount, f.readline()

currentFile = open(input_file)

print_all(currentFile)
rewind(currentFile)
printline(1, currentFile)