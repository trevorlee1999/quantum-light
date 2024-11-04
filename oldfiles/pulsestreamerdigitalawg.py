import numpy as np
import matplotlib.pyplot as plt

# Parameters for the sine wave and triangular wave
modulation_depth = 0.85      # Amplitude of the sinusoidal wave (0.85)
fundamental_freq = 50        # Frequency of the sinusoidal wave (50 Hz)
carrier_freq = 1000        # Frequency of the triangular wave (50 kHz)
# TODO: Change back to 50k! 1000 is for visualisation!
sampling_rate = 10 ** 6     # TODO: Nyquist sampling theorem not applicable here? - check!

# Time array for one full cycle of the sine wave
T_s = 1 / fundamental_freq  # Period of the sine wave
t = np.linspace(0, T_s, int(sampling_rate * T_s), endpoint=False)

print(len(t))
# # Now there are 20000 data points in t to consider
# # So in each of these 20000 data points we need to consider when v_m > v_cr and otherwise
# # If the first condition is met then we treat that as being 1
# # Else we must consider that under the 0

# Generate the sine wave (one cycle)
# v_m = modulation_depth * -1 * np.cos(2 * np.pi * fundamental_freq * t)
v_m = []
for timestamp in t:
    v_m.append(modulation_depth * -1 * np.cos(2 * np.pi * fundamental_freq * timestamp))
v_m = np.array(v_m)

# Generate the triangular wave (1000 cycles within one sine cycle, for 50Hz and 50kHz)
# v_cr = 4 * np.abs(t * carrier_freq - np.floor(t * carrier_freq + 0.5)) - 1
v_cr = []
for timestamp in t:
    v_cr.append(4 * np.abs(timestamp * carrier_freq - np.floor(timestamp * carrier_freq + 0.5)) - 1)
v_cr = np.array(v_cr)

digital_awg_vector = []

# TODO: This is the actual code for the Pulse Streamer!
# for i in range(len(t)):
#     if v_m[i] > v_cr[i]:
#         digital_awg_vector.append((int(1/sampling_rate * 10 ** 11), 1))
#     elif v_m[i] <= v_cr[i]:
#         digital_awg_vector.append((int(1/sampling_rate * 10 ** 11), 0))

# # The following code is purely for visualisation
for i in range(len(t)):
    if v_m[i] > v_cr[i]:
        digital_awg_vector.append(1)
    elif v_m[i] <= v_cr[i]:
        digital_awg_vector.append(0)
# print(digital_awg_vector)

# # Figure plotting
# plt.figure(figsize=(10, 6))
# plt.plot(t, v_m, label='Slow sinusoidal fundamental', color='blue')
# plt.plot(t, v_cr, label='Fast sawtooth carrier', color='red', alpha=0.7)

# # Plot settings
# plt.title('Single Cycle of sinusoidal wave')
# plt.xlabel('Time [s]')
# plt.ylabel('Amplitude')
# plt.legend()
# plt.grid(True)

# # Plot to visualise what should be seen on the oscilloscope
plt.plot(t, digital_awg_vector, label='digital AWG')

# # Show the plot
plt.show()
