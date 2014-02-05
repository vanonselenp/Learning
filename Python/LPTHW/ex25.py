def breakWords(text):
	words = text.split(' ')
	return words

def sortWords(words):
	return sorted(words)

def printFirstWord(words):
	word = words.peek()
	print word

def printLastWord(words):
	word = words.pop(-1)
	print word

def sortSentence(sentence):
	return sortWords(breakWords(sentence))

def printFirstAndLastWord(sentence):
	words = breakWords(sentence)
	printFirstWord(words)
	printLastWord(words)

def printSortedFirstAndLast(sentence):
	words = sortWords(breakWords(sentence))
	printFirstWord(words)
	printLastWord(words)