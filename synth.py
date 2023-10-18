from scipy.io import wavfile
import oscillators

def sin_to_wav(freq, sec, amp = 0.1, sample_rate = 44100):
    osc = oscillators.get_sin_oscillator(frequency = freq, amplitude = 1)
    return oscillators.osc_to_wav(osc, sec, amp, sample_rate)

def tri_to_wav(freq, sec, amp = 0.1, sample_rate = 44100):
    osc = oscillators.get_triangular_oscillator(frequency = freq, amplitude = 1)
    return oscillators.osc_to_wav(osc, sec, amp, sample_rate)

def saw_to_wav(freq, sec, amp = 0.1, sample_rate = 44100):
    osc = oscillators.get_saw_oscillator(frequency = freq, amplitude = 1)
    return oscillators.osc_to_wav(osc, sec, amp, sample_rate)

def square_to_wav(freq, sec, amp = 0.1, sample_rate = 44100):
    osc = oscillators.get_square_oscillator(frequency = freq, amplitude = 1)
    return oscillators.osc_to_wav(osc, sec, amp, sample_rate)

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

def tri_to_file(freq, sec, fname = "temp.wav", amp = 0.1, sample_rate = 44100):
    wav = tri_to_wav(freq, sec, amp, sample_rate)
    wavfile.write(fname, sample_rate, wav)

def saw_to_file(freq, sec, fname = "temp.wav", amp = 0.1, sample_rate = 44100):
    wav = saw_to_wav(freq, sec, amp, sample_rate)
    wavfile.write(fname, sample_rate, wav)

def square_to_file(freq, sec, fname = "temp.wav", amp = 0.1, sample_rate = 44100):
    wav = square_to_wav(freq, sec, amp, sample_rate)
    wavfile.write(fname, sample_rate, wav)