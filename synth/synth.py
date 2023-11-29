from scipy.io import wavfile
import oscillators

WAVE_TYPE_MAP = {'sine': oscillators.get_sin_oscillator,
                 'triangular': oscillators.get_triangular_oscillator,
                  'square': oscillators.get_square_oscillator,
                  'sawtooth': oscillators.get_saw_oscillator}

def get_wav(freq, sec, waveform, amp = 0.1, sample_rate = 44100, envelope = None):
    '''
    Creates an array with the fitting format to create a wav file.

    Parameters
    ---
    freq: The frequency of the wav file.
    sec: The duration of the wav file in seconds.
    waveform: The waveform for the wav file.
    amp: The amplitude of the wav file, which corresponds to its volume.
    sample_rate: The sample rate used to create the wav file.
    envelope: The envelope, which is a dictionary specifying values for attack, release and decay (in seconds). Sustain is implicitly calculated as sustain = duration - attack - release - decay.

    Return value
    ---
    A numpy array with the fitting format to create a wav file.
    '''
    osc_generator = WAVE_TYPE_MAP[waveform]
    osc = osc_generator(frequency = freq, amplitude = 1)
    if envelope is None:
        return oscillators.osc_to_wav(osc, sec, amp, sample_rate)
    else:
        attack, decay, release = envelope['attack'], envelope['decay'], envelope['release']
        wav_array = oscillators.apply_envelope(osc, sec, attack, decay, release, sample_rate)
        return oscillators.array_to_wav(wav_array, amp)

def sin_to_wav(freq, sec, amp = 0.1, sample_rate = 44100, envelope = None):
    '''
    Creates an array with the fitting format to create a wav file, based on a sine waveform.

    Parameters
    ---
    freq: The frequency of the wav file.
    sec: The duration of the wav file in seconds.
    amp: The amplitude of the wav file, which corresponds to its volume.
    sample_rate: The sample rate used to create the wav file.
    envelope: The envelope, which is a dictionary specifying values for attack, release and decay (in seconds). Sustain is implicitly calculated as sustain = duration - attack - release - decay.

    Return value
    ---
    A numpy array with the fitting format to create a wav file.
    '''
    return get_wav(freq, sec, 'sine', amp, sample_rate, envelope)

def tri_to_wav(freq, sec, amp = 0.1, sample_rate = 44100, envelope = None):
    '''
    Creates an array with the fitting format to create a wav file, based on a triangular waveform.

    Parameters
    ---
    freq: The frequency of the wav file.
    sec: The duration of the wav file in seconds.
    amp: The amplitude of the wav file, which corresponds to its volume.
    sample_rate: The sample rate used to create the wav file.
    envelope: The envelope, which is a dictionary specifying values for attack, release and decay (in seconds). Sustain is implicitly calculated as sustain = duration - attack - release - decay.

    Return value
    ---
    A numpy array with the fitting format to create a wav file.
    '''
    return get_wav(freq, sec, 'triangular', amp, sample_rate, envelope)

def saw_to_wav(freq, sec, amp = 0.1, sample_rate = 44100, envelope = None):
    '''
    Creates an array with the fitting format to create a wav file, based on a sawtooth waveform.

    Parameters
    ---
    freq: The frequency of the wav file.
    sec: The duration of the wav file in seconds.
    amp: The amplitude of the wav file, which corresponds to its volume.
    sample_rate: The sample rate used to create the wav file.
    envelope: The envelope, which is a dictionary specifying values for attack, release and decay (in seconds). Sustain is implicitly calculated as sustain = duration - attack - release - decay.

    Return value
    ---
    A numpy array with the fitting format to create a wav file.
    '''
    return get_wav(freq, sec, 'sawtooth', amp, sample_rate, envelope)

def square_to_wav(freq, sec, amp = 0.1, sample_rate = 44100, envelope = None):
    '''
    Creates an array with the fitting format to create a wav file, based on a square waveform.

    Parameters
    ---
    freq: The frequency of the wav file.
    sec: The duration of the wav file in seconds.
    amp: The amplitude of the wav file, which corresponds to its volume.
    sample_rate: The sample rate used to create the wav file.
    envelope: The envelope, which is a dictionary specifying values for attack, release and decay (in seconds). Sustain is implicitly calculated as sustain = duration - attack - release - decay.

    Return value
    ---
    A numpy array with the fitting format to create a wav file.
    '''
    return get_wav(freq, sec, 'square', amp, sample_rate, envelope)

# example usage: sin_to_file_additive([220, 380, 440], [0.6, 0.01, 0.02], 5, fname = 'test.wav')
def sin_to_file_additive(freqs, amps, sec, fname = 'temp.wav', sample_rate = 44100):
    wavs = [sin_to_wav(freq, sec, amp, sample_rate) for freq, amp in zip(freqs, amps)]
    combined_wav = sum(wavs)
    wavfile.write(fname, sample_rate, combined_wav)

def tri_to_file_additive(freqs, amps, sec, fname = 'temp.wav', sample_rate = 44100):
    wavs = [tri_to_wav(freq, sec, amp, sample_rate) for freq, amp in zip(freqs, amps)]
    combined_wav = sum(wavs)
    wavfile.write(fname, sample_rate, combined_wav)

def waveform_to_file(freq, sec, waveform, fname = "temp.wav", amp = 0.1, sample_rate = 44100, envelope = None):
    '''
    Creates a wav file based on the given waveform.

    Parameters
    ---
    freq: The frequency of the wav file.
    sec: The duration of the wav file in seconds.
    waveform: The waveform for the wav file.
    fname: The filename (which may include the path) for the wave file.
    amp: The amplitude of the wav file, which corresponds to its volume.
    sample_rate: The sample rate used to create the wav file.
    envelope: The envelope, which is a dictionary specifying values for attack, release and decay (in seconds). Sustain is implicitly calculated as sustain = duration - attack - release - decay.
    '''
    wav = get_wav(freq, sec, waveform, amp, sample_rate, envelope)
    wavfile.write(fname, sample_rate, wav)

def sin_to_file(freq, sec, fname = "temp.wav", amp = 0.1, sample_rate = 44100, envelope = None):
    '''
    Creates a wav file based on a sine waveform.

    Parameters
    ---
    freq: The frequency of the wav file.
    sec: The duration of the wav file in seconds.
    waveform: The waveform for the wav file.
    fname: The filename (which may include the path) for the wave file.
    amp: The amplitude of the wav file, which corresponds to its volume.
    sample_rate: The sample rate used to create the wav file.
    envelope: The envelope, which is a dictionary specifying values for attack, release and decay (in seconds). Sustain is implicitly calculated as sustain = duration - attack - release - decay.
    '''
    waveform_to_file(freq, sec, 'sine', fname, amp, sample_rate, envelope)

def tri_to_file(freq, sec, fname = "temp.wav", amp = 0.1, sample_rate = 44100, envelope = None):
    '''
    Creates a wav file based on a triangular waveform.

    Parameters
    ---
    freq: The frequency of the wav file.
    sec: The duration of the wav file in seconds.
    waveform: The waveform for the wav file.
    fname: The filename (which may include the path) for the wave file.
    amp: The amplitude of the wav file, which corresponds to its volume.
    sample_rate: The sample rate used to create the wav file.
    envelope: The envelope, which is a dictionary specifying values for attack, release and decay (in seconds). Sustain is implicitly calculated as sustain = duration - attack - release - decay.
    '''
    waveform_to_file(freq, sec, 'triangular', fname, amp, sample_rate, envelope)

def saw_to_file(freq, sec, fname = "temp.wav", amp = 0.1, sample_rate = 44100, envelope = None):
    '''
    Creates a wav file based on a sawtooth waveform.

    Parameters
    ---
    freq: The frequency of the wav file.
    sec: The duration of the wav file in seconds.
    waveform: The waveform for the wav file.
    fname: The filename (which may include the path) for the wave file.
    amp: The amplitude of the wav file, which corresponds to its volume.
    sample_rate: The sample rate used to create the wav file.
    envelope: The envelope, which is a dictionary specifying values for attack, release and decay (in seconds). Sustain is implicitly calculated as sustain = duration - attack - release - decay.
    '''
    waveform_to_file(freq, sec, 'sawtooth', fname, amp, sample_rate, envelope)

def square_to_file(freq, sec, fname = "temp.wav", amp = 0.1, sample_rate = 44100, envelope = None):
    '''
    Creates a wav file based on a square waveform.

    Parameters
    ---
    freq: The frequency of the wav file.
    sec: The duration of the wav file in seconds.
    waveform: The waveform for the wav file.
    fname: The filename (which may include the path) for the wave file.
    amp: The amplitude of the wav file, which corresponds to its volume.
    sample_rate: The sample rate used to create the wav file.
    envelope: The envelope, which is a dictionary specifying values for attack, release and decay (in seconds). Sustain is implicitly calculated as sustain = duration - attack - release - decay.
    '''
    waveform_to_file(freq, sec, 'square', fname, amp, sample_rate, envelope)