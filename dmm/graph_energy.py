import matplotlib.pyplot as plt
import numpy as np
import csv

# x-axis = time (frequency)
# y-axis = energy (min)

failed_configs = [
  (30,0.60),
  (40,0.60),
  (50,0.60),
  (60,0.60),
  (70,0.60),
  (80,0.60),
  (90,0.60),
  (100,0.60),
  (110,0.60),
  (120,0.60),
  (130,0.60),
  (140,0.60),
  (30,0.62),
  (40,0.62),
  (50,0.62),
  (60,0.62),
  (70,0.62),
  (80,0.62),
  (90,0.62),
  (100,0.62),
  (110,0.62),
  (120,0.62),
  (130,0.62),
  (140,0.62),
  (30,0.64),
  (40,0.64),
  (50,0.64),
  (60,0.64),
  (70,0.64),
  (80,0.64),
  (90,0.64),
  (100,0.64),
  (110,0.64),
  (120,0.64),
  (130,0.64),
  (140,0.64),
  (40,0.66),
  (50,0.66),
  (60,0.66),
  (70,0.66),
  (80,0.66),
  (90,0.66),
  (100,0.66),
  (110,0.66),
  (120,0.66),
  (130,0.66),
  (140,0.66),
  (40,0.68),
  (50,0.68),
  (60,0.68),
  (70,0.68),
  (80,0.68),
  (90,0.68),
  (100,0.68),
  (110,0.68),
  (120,0.68),
  (130,0.68),
  (140,0.68),
  (50,0.70),
  (60,0.70),
  (70,0.70),
  (80,0.70),
  (90,0.70),
  (100,0.70),
  (110,0.70),
  (120,0.70),
  (130,0.70),
  (140,0.70),
  (50,0.72),
  (60,0.72),
  (70,0.72),
  (80,0.72),
  (90,0.72),
  (100,0.72),
  (110,0.72),
  (120,0.72),
  (130,0.72),
  (140,0.72),
  (50,0.74),
  (60,0.74),
  (70,0.74),
  (80,0.74),
  (90,0.74),
  (100,0.74),
  (110,0.74),
  (120,0.74),
  (130,0.74),
  (140,0.74),
  (60,0.76),
  (70,0.76),
  (80,0.76),
  (90,0.76),
  (100,0.76),
  (110,0.76),
  (120,0.76),
  (130,0.76),
  (140,0.76),
  (60,0.78),
  (70,0.78),
  (80,0.78),
  (90,0.78),
  (100,0.78),
  (110,0.78),
  (120,0.78),
  (130,0.78),
  (140,0.78),
  (70,0.80),
  (80,0.80),
  (90,0.80),
  (100,0.80),
  (110,0.80),
  (120,0.80),
  (130,0.80),
  (140,0.80),
  (70,0.82),
  (80,0.82),
  (90,0.82),
  (100,0.82),
  (110,0.82),
  (120,0.82),
  (130,0.82),
  (140,0.82),
  (80,0.84),
  (90,0.84),
  (100,0.84),
  (110,0.84),
  (120,0.84),
  (130,0.84),
  (140,0.84),
  (80,0.86),
  (90,0.86),
  (100,0.86),
  (110,0.86),
  (120,0.86),
  (130,0.86),
  (140,0.86),
  (80,0.88),
  (90,0.88),
  (100,0.88),
  (110,0.88),
  (120,0.88),
  (130,0.88),
  (140,0.88),
  (90,0.90),
  (100,0.90),
  (110,0.90),
  (120,0.90),
  (130,0.90),
  (140,0.90),
  (90,0.92),
  (100,0.92),
  (110,0.92),
  (120,0.92),
  (130,0.92),
  (140,0.92),
  (100, 0.94),
  (110,0.94),
  (120,0.94),
  (130,0.94),
  (140,0.94)
]

currents_mem = []
voltages_mem = []
currents_core = []
voltages_core = []

totalV = 0
totalA = 0

with open('../dmm_unroll_repeat_core.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line = 0
  for row in csv_reader:
    if 'voltage (v)' not in row:
      tempV = float(row[0])
      tempA = float(row[1])
      totalV += tempV
      totalA += tempA
    if line % 4 == 3:
      avg_volts = totalV / 3
      avg_amps = totalA / 3
      totalV = 0
      totalA = 0
      voltages_core.append(avg_volts)
      currents_core.append(avg_amps)
    line += 1

totalV = 0  
totalA = 0

with open('../dmm_unroll_repeat_mem.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line = 0
  for row in csv_reader:
    if 'voltage (v)' not in row:
      tempV = float(row[0])
      tempA = float(row[1])
      totalV += tempV
      totalA += tempA
    if line % 4 == 3:
      avg_volts = totalV / 3
      avg_amps = totalA / 3
      totalV = 0
      totalA = 0
      voltages_mem.append(avg_volts)
      currents_mem.append(avg_amps)
    line += 1


# now select the lowest energy per frequency (functional energy):
times = []
with open('../dmm_unroll_repeat1.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line = 0
  temp_time = 0
  for row in csv_reader:
    temp_time += float(row[3].split(":")[2])
    if (line % 3 == 2):
      execution_time = temp_time / 6 # given that the repeats are 2 times
      times.append(execution_time)
      temp_time = 0
    line += 1

energy_freqs = [] # each []] will represent the functional energy measurements per freq
voltage_freqs = []
for f in range(20, 150, 10):
  energy_freq = []
  voltage_freq = []
  ind = 0
  for j in np.arange(0.60, 0.96, 0.02):
      for i in range(20, 150, 10):
        if f == i and (i, round(j, 2)) not in failed_configs:
          energy_freq.append(round(10**6*times[ind] * (voltages_mem[ind]*currents_mem[ind] + voltages_core[ind]*currents_core[ind]), 3))
          voltage_freq.append(round(j, 2))
        ind += 1
  energy_freqs.append(energy_freq)
  voltage_freqs.append(voltage_freq)

if (len(energy_freqs) != (150-20)//10):
  print("smth went wrong man -- ", len(energy_freqs), (150-20)//10)

min_energy_meas = [] # y-axis
min_energy_v_meas = []
for f in range(len(energy_freqs)):
  if (energy_freqs[f] == []):
    min_energy = -10
    min_energy_v = -10
  else: 
    min_ind = np.argmin(energy_freqs[f])
    min_energy = energy_freqs[f][min_ind]
    min_energy_v = voltage_freqs[f][min_ind]
  print("min energy - {} at {} V".format(min_energy, min_energy_v))
  min_energy_meas.append(min_energy)
  min_energy_v_meas.append(min_energy_v)

freqs = [] # x-axis
for x in range(20, 150, 10):
  freqs.append(x)

# Plotting the graph
print(freqs)
print(min_energy_meas)

# plot:
# plt.plot(freqs, min_energy_meas, label='Min Functional Energy per Freq')

# bar graph:
# plt.bar(freqs, min_energy_meas, label='Min Functional Energy', color='#a05195')
# colors = ["#7B2D43", "#59B217", "#3886C8", "#FF5C2F", "#AA44CC", "#0CBD8E", "#FFC857", "#22384E"]
# for i in range(len(colors)):
#   plt.bar(freqs[i], min_energy_meas[i], label="{} V".format(min_energy_v_meas[i]), color=colors[i])
# plt.bar(freqs, 0, color="white")

# scatter plot:
fig, ax = plt.subplots()
fig.subplots_adjust(right=0.75)

if (len(freqs) != len(min_energy_meas) or len(freqs) != len(min_energy_v_meas)):
  print("something is wrong!!!")

twin1 = ax.twinx() # voltage on the right and energy on the left

# "#7B2D43", "#59B217"
p1 = ax.scatter(freqs, min_energy_meas, label="Energy (in uJ)", color = "#7B2D43")
p2 = twin1.scatter(freqs, min_energy_v_meas, label="Voltage (in V)", color = "#59B217")

ax.set(xlim=(0, 140), ylim=(0, 80), xlabel="Frequency (in MHz)", ylabel="Energy (in uJ)")
twin1.set(ylim=(0, 1.4), ylabel="Voltage (in V)")

#ax.yaxis.label.set_color(p1.get_color())
#twin1.yaxis.label.set_color(p2.get_color())

#ax.tick_params(axis='y', colors=p1.get_color())
#twin1.tick_params(axis='y', colors=p2.get_color())

ax.legend(handles=[p1, p2])

plt.show()