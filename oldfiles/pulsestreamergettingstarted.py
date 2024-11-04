# import API classes into the current namespace
from pulsestreamer import PulseStreamer, Sequence

# A pulse with 10µs (10000) HIGH (or 1) and 30µs (30000) LOW (or 0) levels
# Each time unit is 10**(-11) seconds
pattern = [(10000, 1), (30000, 0)]

# Connect to Pulse Streamer
ip = '169.254.8.2'  # Do not change it!!
ps = PulseStreamer(ip)

# Create a sequence object
sequence = ps.createSequence()

# Create sequence and assign pattern to digital channel 0
sequence.setDigital(0, pattern)

# Stream the sequence and repeat it indefinitely
n_runs = PulseStreamer.REPEAT_INFINITELY
ps.stream(sequence, n_runs)
