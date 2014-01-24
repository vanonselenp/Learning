import sys

script, filename = sys.argv

txt = open(filename, "a")

#print txt.read()

txt.write("this is a test of the emergency broadcast system\n");

print txt.mode

txt.close()