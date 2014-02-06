import random
import sys

# WORD_URL = 'http://learncodethehardway.org/words.txt'
WORDS = ['account', 'achiever', 'actor', 'addition', 'adjustment', 'advertisement', 'advice', 'aftermath', 'agreement', 'airplane', 'airport', 'alarm', 'amount', 'amusement', 'angle', 'animal', 'answer', 'ant', 'apparatus', 'apparel', 'apple', 'appliance', 'approval', 'arch', 'argument', 'arithmetic', 'arm', 'army', 'art', 'attack', 'attempt', 'attention', 'attraction', 'aunt', 'authority', 'baby', 'back', 'badge', 'bag', 'bait', 'balance', 'ball', 'balloon', 'banana', 'band', 'base', 'baseball', 'basket', 'basketball', 'bat', 'bath', 'battle', 'bead', 'beam', 'bean', 'bear', 'beast', 'bed', 'bedroom', 'bee', 'beef', 'beetle', 'beggar', 'beginner', 'behavior', 'belief', 'believe', 'bell', 'berry', 'bike', 'bird', 'birth', 'birthday', 'bit', 'bite', 'blade', 'blood', 'blow', 'board', 'boat', 'body', 'bomb', 'bone', 'book', 'boot', 'border', 'bottle', 'boundary', 'box', 'boy', 'brain', 'brake', 'branch', 'brass', 'bread', 'breakfast', 'breath', 'brick', 'bridge', 'brother', 'brush', 'bubble', 'bucket', 'building', 'bulb', 'bun', 'burn', 'burst', 'business', 'butto', 'cabbage', 'cable', 'cactus', 'cake', 'cakes', 'calculator', 'calendar', 'camera', 'camp', 'can', 'cannon', 'canvas', 'cap', 'caption', 'car', 'card', 'carpenter', 'carriage', 'cart', 'cast', 'cat', 'cattle', 'cause', 'cave', 'celery', 'cellar', 'cemetery', 'cent', 'chain', 'chair', 'chalk', 'chance', 'change', 'channel', 'cheese', 'cherry', 'chess', 'chicken', 'children', 'chin', 'church', 'circle', 'clam', 'clock', 'cloth', 'cloud', 'clover', 'club', 'coach', 'coal', 'coast', 'coat', 'cobweb', 'coil', 'collar', 'color', 'comb', 'comfort', 'committee', 'company', 'competition', 'condition', 'connection', 'control', 'cook', 'copper', 'copy', 'cord', 'cork', 'corn', 'cough', 'country', 'cover', 'cow', 'crack', 'cracker', 'crate', 'crayon', 'cream', 'creator', 'creature', 'credit', 'crib', 'crime', 'crook', 'crow', 'crowd', 'crown', 'crush', 'cry', 'cub', 'cup', 'current', 'curtain', 'curve', 'cushion', 'dad', 'daughter', 'day', 'death', 'debt', 'decision', 'deer', 'degree', 'design', 'desire', 'desk', 'destruction', 'detail', 'development', 'digestion', 'dime', 'dinner', 'dinosaurs', 'direction', 'dirt', 'discovery', 'discussion', 'disease', 'disgust', 'distance', 'distribution', 'division', 'dock', 'doctor', 'dog', 'dogs', 'doll', 'donkey', 'door', 'downtown', 'drain', 'drawer', 'dress', 'drink', 'driving', 'drop', 'drug', 'drum', 'duck', 'dust']

PHRASES = {
	'class %%%(%%%):': 'Make class named %%% that is-a %%%.',
	'class %%%(object):\n\tdef__init__(self, ***)': 'class %%% has-a __init__ that takes self and *** parameters.',
	'class %%%(object):\n\tdef***(self, @@@)': 'class has-a function named *** that takes self and @@@ parameters.',
	'*** = %%%()': 'Set *** to an instance of class %%%.',
	'***.***(@@@)': 'From *** get the *** function, and call it with parameters self, @@@', 
	'***.*** = "***"': 'From *** get the *** attribute and set it to "***"'
}

PHRASE_FIRST = False

if len(sys.argv) == 2 and sys.argv[1] == 'english':
	PHRASE_FIRST = True

# for word in urllib.urlopen(WORD_URL).readlines():
	# WORDS.append(word.strip())

def convert(snippet, phrase):
	print "snippet: %s, phrase: %s" % (snippet, phrase)
	class_names = [w.capitalize() for w in random.sample(WORDS, snippet.count("%%%"))]
	other_names = random.sample(WORDS, snippet.count("***"))
	results = []
	param_names = []

	snippetCount = snippet.count("@@@")
	if snippetCount < 1:
		snippetCount = 1

	for i in range(0, snippetCount):
		param_count = random.randint(1, 3)
		param_names.append(', '.join(random.sample(WORDS, param_count)))

		for sentence in snippet, phrase:
			result = sentence[:]
			for word in class_names:
				result = result.replace('%%%', word, 1)

			for word in other_names:
				result = result.replace('***', word, 1)

			for word in param_names:
				result = result.replace('@@@', word, 1)

			results.append(result)

	print results
	return results

try:
	while True:
		snippets = PHRASES.keys()
		random.shuffle(snippets)

		for snippet in snippets:
			phrase = PHRASES[snippet]
			question, answer = convert(snippet, phrase)
			if PHRASE_FIRST:
				question, answer = answer, question

			print question
			raw_input('> ')
			print 'ANSWER: %s \n\n------------------------------------------\n\n' % answer
except EOFError:
	print '\nBye'