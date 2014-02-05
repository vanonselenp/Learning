import sys
import os.path

script, from_file, to_file = sys.argv

print "copying from file to file: %s %s" % (from_file, to_file)

indata = open(from_file).read()

out_file = open(to_file, 'w')

out_file.write(indata)

out_file.close()
