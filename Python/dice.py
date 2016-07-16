import random

# simple functions to roll random dice, because reasons

def dice(amount, times):
    results = []
    for num in range(times):
        results.append(random.randint(1, amount))
    return results

def success_dice(amount, times, success_value):
    values = dice(amount, times)
    count = 0
    reroll = 0
    for x in values:
        if x > success_value:
            count = count + 1
        if x == 10:
            reroll = reroll + 1
    print values
    print "Successes - %s" % count
    print "Reroll %s dice" % reroll

def d10(times):
    success_dice(10, times, 7)

def d6(times):
    success_dice(6, times, 4)

def d20(times):
    success_dice(20, times, 15)

