import sys
import synth

freq = sys.argv[1]
sec = sys.argv[2]
fname = sys.argv[3]

print( freq + " " + sec + " " + fname)
synth.sin_to_file(float(freq), sec = int(sec), fname = fname)
