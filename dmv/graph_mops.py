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
(70,0.84),
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
(80,0.90),
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
(90,0.94),
(100,0.94),
(110,0.94),
(120,0.94),
(130,0.94),
(140,0.94)]

currents_mem = []
voltages_mem = []
currents_core = []
voltages_core = []

totalV = 0
totalA = 0

with open('../dmv_unroll_repeat_core.csv') as csv_file:
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

with open('../dmv_unroll_repeat_mem.csv') as csv_file:
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
with open('../dmv_unroll_100.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line = 0
  temp_time = 0
  successful = 0
  for row in csv_reader:
    if (row[2] == "True"): 
      successful += 1
      temp_time += float(row[3].split(":")[2])/100
    if (line % 3 == 2):
      if (successful > 0):
        execution_time = temp_time / successful # given that the repeats are 100 times???
      else:
        execution_time = float(row[3].split(":")[2])
      times.append(execution_time)
      successful = 0
      temp_time = 0
    line += 1
    
# only plot the min energy per MOPS / frequnecy!
mops_lst = [] # x-axis
energy_lst = []
for f in range(20, 150, 10):
  ind  = 0
  temp_mops_lst = []
  temp_energy_lst = []
  for i in np.arange(0.60, 0.96, 0.02):
    for j in range(20, 150, 10):
      if (j == f):
        config = (j, round(i, 2))
        if config not in failed_configs:
          # calculate the energy + MOPS
          mops = 8192 / times[ind]
          energy = (currents_core[ind]*voltages_core[ind] + currents_mem[ind]*voltages_mem[ind])*times[ind]
          temp_mops_lst.append(round(mops/(10**6), 3)) # MOPS
          temp_energy_lst.append(round(energy*10**6, 3)) #uJ
      ind += 1
  mops_lst.append(temp_mops_lst)
  energy_lst.append(temp_energy_lst)

# plot:
print(mops_lst)
print(energy_lst)

final_mops_lst = []
final_energy_lst = []

for i in range(len(mops_lst)):
  if mops_lst[i] != []:
    min_energy_ind = np.argmin(energy_lst[i])
    # print(mops_lst[min_energy_ind], energy_lst[min_energy_ind])
    final_mops_lst.append(mops_lst[i][min_energy_ind])
    final_energy_lst.append(energy_lst[i][min_energy_ind])

plt.scatter(final_mops_lst, final_energy_lst, label='Energy Consumption v MOPS')

print(final_mops_lst)
print(final_energy_lst)


# Adding labels and title
plt.xlabel('MOPS')
plt.xlim((0, 300))
plt.ylabel('Energy (in uJ)')
plt.ylim((0, 1))

# plt.title('Min. Energy vs MOPS for Dense Matrix Multiply (arith_ops = 524288)')

# Adding a legend
plt.legend()

# Display the plot
plt.show()