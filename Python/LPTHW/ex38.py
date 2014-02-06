stuff = "this is just a test of the emergency broadcast system".split(' ')
second = ['game', 'files', 'world']

while len(second) > 0:
	next = second.pop()
	stuff.append(next)

print stuff
print stuff[-1]
print stuff[1]
print ' '.join(stuff)
print '_'.join(stuff[3:5])