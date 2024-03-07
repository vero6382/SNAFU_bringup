import numpy as np
import csv

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

def find_min_energy():
  times = []

  with open('../dmv_unroll_100.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line = 0
    temp_time = 0
    successful = 0
    for row in csv_reader:
      if (row[2] == "True"): 
        successful += 1
        temp_time += float(row[3].split(":")[2])/101
      if (line % 3 == 2):
        if (successful > 0):
          execution_time = temp_time / successful # given that the repeats are 100 times???
        else:
          execution_time = float(row[3].split(":")[2])
        times.append(execution_time)
        successful = 0
        temp_time = 0
      line += 1

  currents_mem = []
  voltages_mem = []
  currents_core = []
  voltages_core = []

  configs = [] # tuples of (volts, amps)
  ind = 0
  for j in np.arange(0.60, 0.96, 0.02):
    for i in range(20, 150, 10):
      volt = float("{:.2f}".format(j))
      configs.append((i, volt))
      if ((i, volt) not in failed_configs):
        print("configs = {} and execution_time = {} us".format((i, volt), times[ind]*10**6))
      ind += 1
    

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

  energy_lst = []
  power_lst = []
  final_configs = []
  final_times = []
  mops_lst = []
  gops_w_lst = []

  if (len(voltages_mem) != len(times)): 
    print("something is wrong!")
    print(len(voltages_mem),len(times))

  total_powers = []

  for i in range(len(times)):
    power = currents_mem[i] * voltages_mem[i] + currents_core[i] * voltages_core[i]
    total_powers.append(round(power*1000, 3))
    energy = times[i] * power # time * power
    curr_config = configs[i]
    mops = 8192 / times[i]
    gops_w = mops / power
    if (curr_config not in failed_configs):
      energy_lst.append(energy)
      power_lst.append(power)
      final_configs.append(configs[i])
      final_times.append(times[i])
      mops_lst.append(mops)
      gops_w_lst.append(gops_w)
    
  min_energy = np.argmin(energy_lst)
  min_power = np.argmin(power_lst)
  max_energy = np.argmax(energy_lst)
  max_power = np.argmax(power_lst)

  min_mops = np.argmin(mops_lst)
  min_gops_w = np.argmin(gops_w_lst)
  max_mops = np.argmax(mops_lst)
  max_gops_w = np.argmax(gops_w_lst)

  print("total_powers = ", total_powers)

  print("min energy = {:.3f} uJ with configs = {} and execution time = {:.3f} ms".format(energy_lst[min_energy]*10**6, final_configs[min_energy], final_times[min_energy]*10**3))
  print("min power = {:.3f} mW with configs = {}".format(power_lst[min_power]*10**3, final_configs[min_power]))
  print("max energy = {:.3f} uJ with configs = {} and execution time = {:.3f} ms".format(energy_lst[max_energy]*10**6, final_configs[max_energy], final_times[max_energy]*10**3))
  print("max power = {:.3f} mW with configs = {}".format(power_lst[max_power]*10**3, final_configs[max_power]))
  print("min mops = {:.3f} with configs = {}".format(mops_lst[min_mops]/10**6, final_configs[min_mops]))
  print("min gops/w = {:.3f} with configs = {}".format(gops_w_lst[min_gops_w]/10**9, final_configs[min_gops_w]))
  print("max mops = {:.3f} with configs = {}".format(mops_lst[max_mops]/10**6, final_configs[max_mops]))
  print("max gops/w = {:.3f} with configs = {}".format(gops_w_lst[max_gops_w]/10**9, final_configs[max_gops_w]))

find_min_energy()


  