import synth

synth.sin_to_file(220, sec = 10, fname = "concert_a3.wav")
synth.sin_to_file(440, sec = 10, fname = "concert_a4.wav")
synth.sin_to_file(440 * 2**(1 / 12), sec = 10, fname = "concert_bb4.wav")
synth.sin_to_file(440 * 2**(2 / 12), sec = 10, fname = "concert_b4.wav")
synth.sin_to_file(440 * 2**(7 / 12), sec = 10, fname = "concert_e5.wav")
synth.sin_to_file(440 * 2**(1 / 24), sec = 10, fname = "half_sharp_a4.wav")
