# import API classes into the current namespace
# from pulsestreamer import PulseStreamer, findPulseStreamers

# import API classes into the current namespace
from pulsestreamer import PulseStreamer, Sequence

import numpy as np
import matplotlib.pyplot as plt

T_s = 2e-5  # switching period
N = int((1 / 50) / (T_s))  # number of switching periods in one period of fundamental at 50 Hz
K = 100  # number of samples in one switching period,
# picked 100 as easy to calculate duty ratio as percentage
delta = T_s / K  # time duration of one interval in switching period


def v_m(t):
    # Define reference signal sinusoidal waveform
    result = 0.85 * np.sin(2 * np.pi * 50 * t)  # modulation depth 85% is peak-to-peak of duty ratio waveform
    return result


def v_cr(t):
    # Define carrier signal triangular waveform
    t = t % T_s
    if 0 <= t < T_s / 4:
        result = 4 / T_s * t

    elif T_s / 4 <= t < 3 * T_s / 4:
        result = -4 / T_s * t + 2

    else:
        result = 4 / T_s * t - 4

    return result

duty = []  # For storing the duty ratio of each switching period of the carrier signal
gate = []  # For storing Boolean values of bipolar sinusoidal PWM gate control voltage
reference = []
carrier = []
time = []
time_1 = []
for i in range(N):
    # iterate over all switching periods in one fundamental period
    ones = 0
    for k in range(K):
        # iterate within each switching period
        t = i * T_s + k * delta
        time.append(t)
        reference.append(v_m(t))
        carrier.append(v_cr(t))
        if v_m(t) > v_cr(t):
            ones += 1
            gate.append(1)
        else:
            gate.append(0)
    time_1.append(i * T_s)
    duty.append(ones)  # store duty ratio as percentage

plt.plot(time_1, duty)
# plt.plot(time, reference) to verify waveforms  of carrier and reference signals
# plt.plot(time, carrier)
plt.xlabel("Time / seconds")
plt.ylabel("Duty Ratio per switching period as a percentage")
plt.show()

# A pulse with 10µs HIGH and 30µs LOW levels
pattern = [(40000, 1), (25000, 0)]

# Connect to Pulse Streamer
ip = '169.254.8.2' # Do not change it!!
ps = PulseStreamer(ip)

# Create a sequence object
sequence = ps.createSequence()

# Create sequence and assign pattern to digital channel 0
sequence.setDigital(0, pattern)

# Stream the sequence and repeat it indefinitely
n_runs = PulseStreamer.REPEAT_INFINITELY
ps.stream(sequence, n_runs)