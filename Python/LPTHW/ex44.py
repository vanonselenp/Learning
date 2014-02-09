#also known as the why you don't do inheritance cos it is evil like a bad fantasy villian from princess bride.

class Parent(object):
	def implict(self):
		print 'parent implict()'

	def override(self):
		print 'parent crash override'

	def altered(self):
		print 'parent altered'

class Child(Parent):
	def __init__(self, stuff):
		self.stuff = stuff
		super(Child, self).__init__()

	def override(self):
		print 'child crash override'

	def altered(self):
		print 'child altered start'
		super(Child, self).altered()
		print 'child altered end'

class Other(object):
	def override(self):
		print 'other crash override'

	def implict(self):
		print 'other implict'

	def altered(self):
		print 'other altered'

class NovaChild(object):
	def __init__(self):
		self.other = Other()

	def implict(self):
		self.other.implict()

	def override(self):
		print 'novachild crash override'

	def altered(self):
		print 'novachild start'
		self.other.altered()
		print 'novachild end'


parent = Parent()
child = Child("stuff")

parent.implict()
child.implict()

parent.override()
child.override()

parent.altered()
child.altered()

novachild = NovaChild()
novachild.implict()
novachild.override()
novachild.altered()