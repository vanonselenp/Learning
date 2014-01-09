import sys

script, user_name = sys.argv
prompt = '>'

print 'Hi %s, I am %s \nSome quick Q\'s' % (user_name, script)

likes = raw_input("what are your likes" + prompt)
lives = raw_input("where do you live" + prompt)
compu = raw_input("what computer do you have" + prompt)

print 'typed the following %s, %s, %s' % (likes, lives, compu)
