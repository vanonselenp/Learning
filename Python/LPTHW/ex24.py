text = """ 
words, more words \ttabs\n\tand stuff
"""

print text

def function(number):
	beans = number * 500
	jars = beans / 1000
	crates = jars / 100
	return beans, jars, crates

start = 10000

beans, jars, crates = function(start)

print "%s %s %s" % (beans, jars, crates)