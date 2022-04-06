import math
import itertools


def get_sin_oscillator(frequency, sample_rate, amplitude):
  increment = (2 * math.pi * frequency) / sample_rate
  return (math.sin(v) * amplitude for v in itertools.count(start = 0, step = increment))

osc = get_sin_oscillator(frequency = 1, sample_rate = 44100, amplitude = 1)
samples = [next(osc) for i in range(512)]

print(samples)
