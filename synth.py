import numpy
from scipy.io import wavfile
import math
import itertools


def get_sin_oscillator(frequency, sample_rate, amplitude):
  increment = (2 * math.pi * frequency) / sample_rate
  return (math.sin(v) * amplitude for v in itertools.count(start = 0, step = increment))

osc = get_sin_oscillator(frequency = 1, sample_rate = 44100, amplitude = 1)
samples = [next(osc) for i in range(512)]

def wave_to_file(wav, wav2 = None, fname = "temp.wav", amp = 0.1, sample_rate = 44100):
  wav = numpy.array(wav)
  wav = nympy.int16(wav * amp * (2**15 - 1))

  if wav2 is not None:
    wav2 = nympy.array(wav2)
    wav2 = np.int16(wav2 * amp * (2 ** 15 - 1))
    wav = np.stack([wav, wav2]).T

  wavfile.write(fname, sample_rate, wav)

print(samples)
