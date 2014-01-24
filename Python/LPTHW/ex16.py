import sys

script, filename = sys.argv

print "clearing file, continue?"
raw_input("?")

target = open(filename, "w")

line = raw_input("Enter text")

target.write(line + "\n")
target.close()

target = open(filename)
print target.read()