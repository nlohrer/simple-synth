import math

def triangular(x):
    '''
    Triangular wave function.
    '''
    if x < 0 or x > 1:
        return triangular(x - math.floor(x))
    elif x < 0.5:
        return -1 + 4*x
    else:
        return 3 - 4*x

def saw(x):
    '''
    Sawtooth wave function.
    '''
    if x < 0 or x > 1:
        return saw(x - math.floor(x))
    else:
        return -1 + 2*x

def square(x):
    '''
    Square wave function.
    '''
    if x < 0 or x > 1:
        return square(x - math.floor(x))
    elif x < 0.5:
        return 1
    else:
        return -1

def get_linear_interpolation_function(p1, p2):
    '''
    Returns a linear function that interpolates the two given points.

    p1 and p2 are given as pairs of integers.
    '''
    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2:
        def linear(x):
            return y2
        return linear

    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    def linear(x):
        return slope * x + intercept
    return linear