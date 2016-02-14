import random

# simple functions to roll random dice, because reasons

def dice(amount, times):
    for num in range(times):
        print random.randint(1, amount)

def d10(times):
    dice(10, times)

def d6(times):
    dice(6, times)

def d20(times):
    dice(20, times)

