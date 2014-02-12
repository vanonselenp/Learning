from nose.tools import *
from ex47.game import Room

def setup():
	print 'setup'

def teardown():
	print 'teardown'

def test_room():
	gold = Room("GoldRoom", """This room has gold in it""")
	assert_equal(gold.name, "GoldRoom")
	assert_equal(gold.paths, {})

def test_room_paths():
	center = Room("center", "test center room")
	north = Room("north", "test north room")
	south = Room("south", "test south room")

	center.add_paths({'north': north, 'south': south})
	assert_equal(center.go('north'), north)
	assert_equal(center.go('south'), south)

def test_map():
	start = Room('start','you can go west and down')
	west = Room('west', 'there are trees, you can go east')
	down = Room('dungeon', 'it is dark, you can go up')

	start.add_paths({'west': west, 'down': down})
	west.add_paths({'east': start})
	down.add_paths({'up': start})

	assert_equal(start.go('west'), west)
	assert_equal(start.go('west').go('east'), start)
	assert_equal(start.go('down').go('up'), start)