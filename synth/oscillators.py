import math
import numpy
import itertools
import wave_functions as wave

# oscillators for different waveforms
def get_triangular_oscillator(frequency, amplitude, sample_rate = 44100):
    '''
    Returns an iterator for a triangular wave.
    '''
    increment = frequency / sample_rate
    return (wave.triangular(v) * amplitude for v in itertools.count(start = 0, step = increment))

def get_saw_oscillator(frequency, amplitude, sample_rate = 44100):
    '''
    Returns an iterator for a sawtooth wave.
    '''
    increment = frequency / sample_rate
    return (wave.saw(v) * amplitude for v in itertools.count(start = 0, step = increment))

def get_square_oscillator(frequency, amplitude, sample_rate = 44100):
    '''
    Returns an iterator for a square wave.
    '''
    increment = frequency / sample_rate
    return (wave.square(v) * amplitude for v in itertools.count(start = 0, step = increment))

def get_sin_oscillator(frequency, amplitude, sample_rate = 44100):
    '''
    Returns an iterator for a sine wave.
    '''
    increment = (2 * math.pi * frequency) / sample_rate
    return (wave.math.sin(v) * amplitude for v in itertools.count(start = 0, step = increment))

def osc_to_array(osc, sec, sample_rate = 44100):
    '''
    Turns an iterator to a numpy array with its length depending on the given length in seconds and the sample rate.
    '''
    samples = [next(osc) for i in range(round(44100 * sec))]
    wav_array = numpy.array(samples)
    return wav_array

def array_to_wav(wav_array, amp):
    '''
    Turns a numpy array into a numpy array with the fitting format to create a wav file.
    '''
    wav = numpy.int16(wav_array * amp * (2**15 - 1))
    return wav

def osc_to_wav(osc, sec, amp = 0.1, sample_rate = 44100):
    '''
    Turns an iterator into a numpy array with the fitting format to create a wav file.
    '''
    wav_array = osc_to_array(osc, sec, sample_rate)
    wav = array_to_wav(wav_array, amp)
    return wav

def apply_envelope(osc, sec, attack, decay, release, sample_rate = 44100):
    '''
    Applies an envelope to an oscillator and returns a numpy array.

    attack, delay, and release represent durations (in seconds).
    '''
    sustain = sec - attack - decay - release
    if sustain < 0:
        raise ValueError("attack + decay + release must not exceed the entire duration")

    # points for interpolation
    p1 = (0, 0)
    p2 = (attack, 2)
    p3 = (attack + decay, 1)
    p4 = (attack + decay + sustain, 1)
    p5 = (sec, 0)

    attack_fun = wave.get_linear_interpolation_function(p1, p2)
    decay_fun = wave.get_linear_interpolation_function(p2, p3)
    sustain_fun = wave.get_linear_interpolation_function(p3, p4)
    release_fun = wave.get_linear_interpolation_function(p4, p5)

    def envelope_function(x):
        x = x / sample_rate
        if x <= attack:
            return attack_fun(x)
        elif x <= attack + decay:
            return decay_fun(x)
        elif x <= attack + decay + sustain:
            return sustain_fun(x)
        else:
            return release_fun(x)

    samples = [next(osc) * envelope_function(i) for i in range(round(sample_rate * sec))]
    wav_array = numpy.array(samples)
    return wav_array