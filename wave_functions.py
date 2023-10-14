import math

# function for triangular waves
def triangular(x):
    if x < 0 or x > 1:
        return triangular(x - math.floor(x))
    elif x < 0.5:
        return -1 + 4*x
    else:
        return 3 - 4*x

# function for sawtooth waves
def saw(x):
    if x < 0 or x > 1:
        return saw(x - math.floor(x))
    else:
        return -1 + 2*x

# function for square waves
def square(x):
    if x < 0 or x > 1:
        return square(x - math.floor(x))
    elif x < 0.5:
        return 1
    else:
        return -1