print "you enter a dark room with 2 doors, the 1st door is dark and scary, and the 2nd door there is a light in the room beyond."

door = raw_input('>')

if door == '1':
	print 'there is a scary bear eating a cake with some tea and a hatter'
	print 'do you: \n\t1.Take the cake\n\t2.scream at the bear'
	bear = raw_input('>')
	if bear == '1':
		print 'you take the cake and lose your face.'
	elif bear == '2':
		print 'you lose your legs and die screaming'
	else:
		print 'you run away. good job'
else:
	print 'you didn\'t go into the dark scary door of doom, you live'