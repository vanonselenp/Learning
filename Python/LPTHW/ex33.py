def makeList(stop, increment):
	i = 0
	numbers = []

	while i < stop:
		numbers.append(i)
		i += increment
	return numbers

def alt(stop, increment):
	return range(0, stop, increment)

print makeList(9, 2)
print alt(9, 2)