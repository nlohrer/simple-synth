import synth
import numpy
from scipy.io import wavfile

# 12-TET examples for sin waves
#synth.sin_to_file(440, sec = 10, fname = "./synth/wavs/concert_a4.wav")
#synth.sin_to_file(440 * 2**(2 / 12), sec = 10, fname = "./synth/wavs/concert_b4.wav")
#synth.sin_to_file(440 * 2**(7 / 12), sec = 10, fname = "./synth/wavs/concert_e5.wav")
#synth.sin_to_file(440 * 2**(1 / 24), sec = 10, fname = "./synth/wavs/half_sharp_a4.wav")
#synth.sin_to_file(440 / 2**(9 / 12), sec = 10, fname = "./synth/wavs/concert_c4.wav")

# triangular waves
'''
wav_tri = synth.tri_to_wav(440, 5)
wavfile.write('./synth/wavs/concert_a4_tri.wav', 44100, wav_tri)
'''

# saw waves
'''
wav_saw = synth.saw_to_wav(440, 5)
wavfile.write('./synth/wavs/concert_a4_saw.wav', 44100, wav_saw)
'''

#  square waves
'''
wav_square = synth.square_to_wav(440, 5)
wavfile.write('./synth/wavs/concert_a4_square.wav', 44100, wav_square)
'''

# Twinkle Twinkle Little Star - rhythm is not not perfect
'''
notes = {'A4': 440, 'B4': round(440 * (9 / 8)), 'Cs5': round(440 * (5 / 4)), 'Ds5': round(440 * (4 / 3)), 'E5': round(440 * 1.5), 'Fs5': round(440 * (5 / 3))}
notes_synth = {note: synth.sin_to_wav(freq, 0.7) for note, freq in notes.items()}
notes_synth['rest'] = synth.sin_to_wav(0, 0.1)

melody = ['A4', 'rest', 'A4', 'rest', 'E5', 'rest', 'E5', 'rest', 'Fs5', 'rest', 'Fs5', 'rest', 'E5', 'E5', 'rest', 'Ds5', 'rest', 'Ds5', 'rest', 'Cs5', 'rest', 'Cs5', 'rest', 'B4', 'rest', 'B4', 'rest', 'A4', 'A4']

melody_wav = notes_synth[melody[0]]
for note in melody[1:]:
    melody_wav = numpy.append(melody_wav, notes_synth[note])
wavfile.write('./synth/wavs/twinkle_twinkle.wav', 44100, melody_wav)
'''

# An example for additive synthesis
'''
def calc_harmonic_series(freq, n):
    return [freq * i for i in range(1, n + 1)]

n = 10
freqs = calc_harmonic_series(220, n)
synth.sin_to_file_additive(freqs, [0.2 * (1 / 2) ** i for i in range(1, n + 1)], 5, fname = './synth/wavs/additive.wav')
'''
