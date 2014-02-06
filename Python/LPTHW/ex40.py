class Song(object):
	def __init__(self, lyrics):
		self.lyrics = lyrics

	def sing_me_a_song(self):
		for line in self.lyrics:
			print line

happy_bday = Song(['this is only a test','of the emergency broadcast system','it is a product of hysterical mass consumption'])

happy_bday.sing_me_a_song()