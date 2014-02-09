import sys
import random

class Scene(object):
	def enter(self):
		print "Scene not yet implemented"
		exit(1)

class Engine(object):
	def __init__(self, scene_map):
		self.scene_map = scene_map

	def play(self):
		current_scene = self.scene_map.opening_scene()
		print self.scene_map.opening_scene()
		while True:
			print "\n--------------"
			next_scene_name = current_scene.enter()
			current_scene = self.scene_map.next_scene(next_scene_name)

class Death(Scene):
	quips = ['evil quip number 1','great skill one doe snot have','evil quip number are we still counting?','you are dead, so sad']

	def enter(self):
		print Death.quips[random.randint(0, len(self.quips) - 1)]
		exit(1)

class CentralCorridor(Scene):
	def enter(self):
		print 'central corridor'
		action = raw_input('> ')
		if action == 'shoot':
			print 'you shoot, you die'
			return 'death'
		elif action == 'dodge':
			print 'you dodge, you die'
			return 'death'
		elif action == 'tell a joke':
			print 'you are amusing, continue'
			return 'laser_weapon_armory'
		else:
			print 'DOES NOT COMPUTE'
			return 'central_corridor'

class LaserWeaponArmory(Scene):
	def enter(self):
		print 'guess the code to continue, you have 10 tries'
		code = '%d%d%d' % (random.randint(0,10), random.randint(0,10), random.randint(0,10))
		guess = raw_input('> ')
		guesses = 1

		print code

		while guess != code and guesses < 10:
			print 'wrong'
			guesses += 1
			guess = raw_input('>')

		if guess == code:
			print 'continue.'
			return 'the_bridge'
		else:
			print 'you die'
			return 'death'

class TheBridge(Scene):
	def enter(self):
		print 'the bridge of doom'
		action = raw_input('>')
		if action == 'throw the bomb':
			print 'you throw the bomb and it explodes, killing you.'
			return 'death'
		elif action == 'slowly place the bomb':
			print 'you place the bomb slowly and successfully arm it. you leave to the escape pod'
			return 'escape_pod'
		else:
			print 'does not compute'
			return 'the_bridge'

class EscapePod(Scene):
	def enter(self):
		print 'you enter the escape pod room, there are 5 here, only one is working, which do you choose? (1-5)'
		good_pod = random.randint(1,5)
		print good_pod
		guess = raw_input('>')

		if int(guess) != good_pod:
			print 'you enter pod %s, however it explodes the moment you start it. you die' % (guess)
			return 'death'
		else:
			print 'you chose the working pod and make it out alive'
			return 'finished'


class Map(object):
	scenes = {
		'central_corridor': CentralCorridor(),
		'laser_weapon_armory': LaserWeaponArmory(),
		'the_bridge': TheBridge(),
		'escape_pod': EscapePod(),
		'death': Death()
	}

	def __init__(self, start_scene):
		self.start_scene = start_scene

	def next_scene(self, scene_name):
		return Map.scenes.get(scene_name)

	def opening_scene(self):
		return self.next_scene(self.start_scene)

a_map = Map("central_corridor")
a_game = Engine(a_map)
a_game.play()