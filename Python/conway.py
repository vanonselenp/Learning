import unittest
import itertools

class CellState(object):
	Dead = 0
	Alive = 1

class World(object):
	#this needs to be refactored
	def __init__(self, liveCells):
		self.world = liveCells

	def getNeighbors(self, cell):
		return map(lambda c: [c[0] + cell[0], c[1] + cell[1]], filter(lambda x: x != (0, 0), itertools.product(range(-1, 2), range(-1, 2))))

	def liveCells(self):
		return len(self.world)

	def getCellState(self, cell):
		exists = self.world.__contains__(cell)
		if exists:
			return CellState.Alive
		return CellState.Dead

	def run(self):
		worldNeighbors = list(itertools.chain(*map(lambda cell: self.getNeighbors(cell), self.world)))
		worldNeighbors.sort(key = lambda k: (k[0], k[1]))
		grouped = map(lambda x: [x[0], len(list(x[1]))], itertools.groupby(worldNeighbors))
		data = filter(lambda freq: freq[1] == 3 or (freq[1] == 2 and self.world.__contains__(freq[0])), grouped)
		return World(map(lambda x: x[0], data))

class Conway_Tests(unittest.TestCase):
	def test_given_aWorldWithNoCells_When_Run_Then_NoCellsAreAlive(self):
		world = World([])

		new_world = world.run()

		assert 0 == new_world.liveCells()

	def test_given_aWorldWithOneCell_when_run_then_noCellsAreAlive(self):
		test_cell = [1, 1]
		world = World([test_cell])

		new_world = world.run()

		assert 0 == new_world.liveCells()
		assert CellState.Dead == new_world.getCellState(test_cell)

	def test_given_aWorldWithAnAliveCellWithTwoNeighbors_when_run_then_oneCellIsLeft(self):
		world = World([[0, 0], [1, 1], [2, 2]])

		new_world = world.run()

		assert 1 == new_world.liveCells()
		assert CellState.Alive == new_world.getCellState([1, 1])

	def test_given_aWorldWithAPositionWithThreeNeighbors_when_run_then_cellIsAlive(self):
		world = World([[0, 0], [1, 1], [0, 1]])

		new_world = world.run()

		assert CellState.Alive == new_world.getCellState([1, 0])

	def test_given_aWorldWithCellWithMoreThanThreeNeighbors_when_run_then_cellIsDead(self):
		world = World([[0, 0], [0, 1], [0, 2], [1, 0],[1, 2], [1, 1]])

		new_world = world.run()

		assert CellState.Dead == new_world.getCellState([1, 1])
