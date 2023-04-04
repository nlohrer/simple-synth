import numpy
from scipy.io import wavfile
import math
import itertools

def get_sin_oscillator(frequency, amplitude, sample_rate = 44100):
    increment = (2 * math.pi * frequency) / sample_rate
    return (math.sin(v) * amplitude for v in itertools.count(start = 0, step = increment))

def sin_to_wav(freq, sec, amp = 0.1, sample_rate = 44100):
    osc = get_sin_oscillator(frequency = freq, amplitude = 1)
    samples = [next(osc) for i in range(44100 * sec)]
    wav = numpy.array(samples)
    wav = numpy.int16(wav * amp * (2**15 - 1))
    return wav
    
def sin_to_file_additive(freqs, amps, sec, fname = 'temp.wav', sample_rate = 44100):
    wavs = []
    for freq, amplitude in zip(freqs, amps):
        wav = sin_to_wav(freq, sec, amplitude, sample_rate)
        wavs.append(wav)
        wavfile.write(str(freq) + '.wav', sample_rate, wav)
    combined_wav = wavs[0]
    for wav in wavs[1:]:
        combined_wav += wav
    wavfile.write(fname, sample_rate, combined_wav)

def sin_to_file(freq, sec, fname = "temp.wav", amp = 0.1, sample_rate = 44100):
    wav = sin_to_wav(freq, sec, amp, sample_rate)
    wavfile.write(fname, sample_rate, wav)
