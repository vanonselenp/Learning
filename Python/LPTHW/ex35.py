import sys

def gold_room():
	print "room is full of gold, take?"

	next = raw_input('>')
	if '0' in next or '1' in next:
		how_much = int(next)
	else:
		dead("type a number")

	if how_much < 50:
		print "not greedy"
		sys.exit(0)
	else:
		dead("greedy")

def bear_room():
	print "bear, has honey, in front of door, move bear?"
	bear_moved = False

	while True:
		next = raw_input('>')
		if next == 'take honey':
			dead("bear don't like that")
		elif next == 'taunt bear':
			print "bear moved"
			bear_moved = True
		elif next == 'taunt bear' and bear_moved:
			dead("bear angry")
		elif next == 'open door' and bear_moved:
			gold_room()
		else:
			print 'unknown command'

def cthulu_room():
	print 'room of cthulu, flee or eat head?'
	next = raw_input('>')
	if 'flee' in next:
		start()
	elif 'head' in next:
		dead('tasty')
	else:
		cthulu_room()

def dead(why):
	print why, "Excellent!"
	sys.exit(0)

def start():
	print 'in a dark room, door on the left and right, move?'
	next = raw_input('>')
	if next == 'left':
		bear_room()
	elif next == 'right':
		cthulu_room()
	else:
		dead('lots of stumbling')

start()