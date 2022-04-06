import numpy
from scipy.io import wavfile
import math
import itertools


def get_sin_oscillator(frequency, amplitude, sample_rate = 44100):
  increment = (2 * math.pi * frequency) / sample_rate
  return (math.sin(v) * amplitude for v in itertools.count(start = 0, step = increment))

def wave_to_file(wav, fname = "temp.wav", amp = 0.1, sample_rate = 44100):
  wav = numpy.array(wav)
  wav = numpy.int16(wav * amp * (2**15 - 1))
  wavfile.write(fname, sample_rate, wav)

def sin_to_file(freq, sec, fname = "temp.wav", amp = 0.1, sample_rate = 44100):
  osc = get_sin_oscillator(frequency = freq, amplitude = 1)
  samples = [next(osc) for i in range(44100 * sec)]
  wave_to_file(samples, fname = fname, amp = amp, sample_rate = sample_rate)
