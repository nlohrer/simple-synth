import numpy
from scipy.io import wavfile
import math
import itertools

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
        
# oscillators for different waveforms
def get_triangular_oscillator(frequency, amplitude, sample_rate = 44100):
    increment = frequency / sample_rate
    return (triangular(v) * amplitude for v in itertools.count(start = 0, step = increment))

def get_saw_oscillator(frequency, amplitude, sample_rate = 44100):
    increment = frequency / sample_rate
    return (saw(v) * amplitude for v in itertools.count(start = 0, step = increment))

def get_square_oscillator(frequency, amplitude, sample_rate = 44100):
    increment = frequency / sample_rate
    return (square(v) * amplitude for v in itertools.count(start = 0, step = increment))

def get_sin_oscillator(frequency, amplitude, sample_rate = 44100):
    increment = (2 * math.pi * frequency) / sample_rate
    return (math.sin(v) * amplitude for v in itertools.count(start = 0, step = increment))

def osc_to_wav(osc, sec, amp = 0.1, sample_rate = 44100):
    samples = [next(osc) for i in range(round(44100 * sec))]
    wav = numpy.array(samples)
    wav = numpy.int16(wav * amp * (2**15 - 1))
    return wav

# helper functions for different waveforms - will clean up later
def sin_to_wav(freq, sec, amp = 0.1, sample_rate = 44100):
    osc = get_sin_oscillator(frequency = freq, amplitude = 1)
    return osc_to_wav(osc, sec, amp, sample_rate)

def tri_to_wav(freq, sec, amp = 0.1, sample_rate = 44100):
    osc = get_triangular_oscillator(frequency = freq, amplitude = 1)
    return osc_to_wav(osc, sec, amp, sample_rate)

def saw_to_wav(freq, sec, amp = 0.1, sample_rate = 44100):
    osc = get_saw_oscillator(frequency = freq, amplitude = 1)
    return osc_to_wav(osc, sec, amp, sample_rate)

def square_to_wav(freq, sec, amp = 0.1, sample_rate = 44100):
    osc = get_square_oscillator(frequency = freq, amplitude = 1)
    return osc_to_wav(osc, sec, amp, sample_rate)

# example usage: sin_to_file_additive([220, 380, 440], [0.6, 0.01, 0.02], 5, fname = 'test.wav')
def sin_to_file_additive(freqs, amps, sec, fname = 'temp.wav', sample_rate = 44100):
    wavs = [sin_to_wav(freq, sec, amp, sample_rate) for freq, amp in zip(freqs, amps)]
    combined_wav = sum(wavs)
    wavfile.write(fname, sample_rate, combined_wav)

def tri_to_file_additive(freqs, amps, sec, fname = 'temp.wav', sample_rate = 44100):
    wavs = [tri_to_wav(freq, sec, amp, sample_rate) for freq, amp in zip(freqs, amps)]
    combined_wav = sum(wavs)
    wavfile.write(fname, sample_rate, combined_wav)

def sin_to_file(freq, sec, fname = "temp.wav", amp = 0.1, sample_rate = 44100):
    wav = sin_to_wav(freq, sec, amp, sample_rate)
    wavfile.write(fname, sample_rate, wav)
