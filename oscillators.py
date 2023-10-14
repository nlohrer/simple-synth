import math
import numpy
import itertools
import wave_functions as wave

# oscillators for different waveforms
def get_triangular_oscillator(frequency, amplitude, sample_rate = 44100):
    increment = frequency / sample_rate
    return (wave.triangular(v) * amplitude for v in itertools.count(start = 0, step = increment))

def get_saw_oscillator(frequency, amplitude, sample_rate = 44100):
    increment = frequency / sample_rate
    return (wave.saw(v) * amplitude for v in itertools.count(start = 0, step = increment))

def get_square_oscillator(frequency, amplitude, sample_rate = 44100):
    increment = frequency / sample_rate
    return (wave.square(v) * amplitude for v in itertools.count(start = 0, step = increment))

def get_sin_oscillator(frequency, amplitude, sample_rate = 44100):
    increment = (2 * math.pi * frequency) / sample_rate
    return (wave.math.sin(v) * amplitude for v in itertools.count(start = 0, step = increment))

def osc_to_wav(osc, sec, amp = 0.1, sample_rate = 44100):
    samples = [next(osc) for i in range(round(44100 * sec))]
    wav = numpy.array(samples)
    wav = numpy.int16(wav * amp * (2**15 - 1))
    return wav