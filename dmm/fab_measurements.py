import csv
import numpy as np
import matplotlib.pyplot as plt

def find_fab ():
  voltages = []
  fab_meas = [] # fab measurements = voltages * current (W)
  power_meas = []

  totalV = 0
  totalA = 0

  with open('../fabric_mem.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
      if 'voltage (v)' not in row:
        tempV = float(row[0])
        tempA = float(row[1])
        totalV += tempV
        totalA += tempA
      else:
        avg_volts = totalV / 3
        avg_amps = totalA / 3
        fab_meas.append(round(avg_volts * avg_amps * 1000, 3))
        totalV = 0
        totalA = 0

  with open('../fabric_core.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
      if 'voltage (v)' not in row:
        tempV = float(row[0])
        tempA = float(row[1])
        totalV += tempV
        totalA += tempA
      else:
        avg_volts = totalV / 3
        avg_amps = totalA / 3
        fab_meas[line_count] += round(avg_volts * avg_amps * 1000, 3)
        totalV = 0
        totalA = 0
        line_count += 1

  for i in range(len(fab_meas)):
    fab_meas[i] = round(fab_meas[i], 3)

  # let's look at the actual power measurements -- from min_energy.py
  total_powers = [1.91, 2.551, 3.039, 3.307, 3.63, 4.055, 5.076, 4.952, 5.391, 5.656, 6.037, 6.077, 
   6.155, 2.111, 2.741, 3.027, 3.507, 4.093, 4.413, 5.071, 5.216, 5.664, 6.425, 6.547, 
   6.585, 6.57, 2.34, 2.752, 3.448, 3.713, 4.217, 4.706, 5.264, 5.829, 6.328, 6.527, 
   6.246, 6.214, 6.3, 2.49, 2.958, 3.748, 4.006, 4.831, 5.231, 5.662, 6.297, 6.592, 
   6.669, 6.988, 7.005, 7.0, 2.935, 3.39, 3.901, 4.979, 4.796, 5.364, 5.948, 6.442, 
   6.581, 6.865, 6.364, 6.551, 6.311, 3.013, 3.807, 4.592, 4.568, 5.983, 5.727, 6.566, 
   7.202, 7.108, 6.699, 6.462, 6.567, 6.406, 3.496, 3.763, 4.741, 4.913, 6.309, 6.078, 
   6.702, 7.086, 7.359, 6.883, 6.644, 6.535, 6.635, 3.735, 4.239, 5.114, 5.562, 5.854, 
   6.49, 7.104, 7.773, 7.437, 6.834, 6.693, 6.62, 6.357, 4.036, 4.621, 5.213, 5.876, 6.635, 
   6.908, 7.608, 8.271, 8.018, 7.136, 6.533, 6.459, 6.489, 3.911, 4.718, 5.874, 6.66, 6.969, 
   7.257, 8.095, 7.912, 8.073, 7.641, 6.415, 6.445, 6.465, 4.156, 5.694, 5.89, 7.185, 7.634, 
   8.244, 8.449, 8.655, 8.084, 7.675, 6.462, 6.833, 6.387, 4.952, 5.99, 6.772, 7.623, 7.927, 
   8.338, 9.123, 8.475, 8.138, 7.698, 7.216, 7.071, 7.211, 5.2, 6.301, 7.286, 7.869, 8.351, 
   9.035, 8.611, 7.95, 8.099, 7.645, 7.113, 7.333, 7.238, 5.608, 6.792, 7.915, 8.631, 8.317, 
   9.177, 8.413, 8.722, 8.29, 7.63, 7.182, 7.445, 7.386, 5.424, 6.465, 8.378, 9.187, 9.618,
   9.232, 8.682, 8.786, 8.304, 7.722, 7.423, 7.27, 7.398, 6.368, 7.7, 9.057, 9.716, 9.435, 
   9.638, 8.65, 8.902, 8.329, 7.919, 7.441, 7.299, 7.479, 6.757, 8.189, 9.591, 10.897, 
   10.544, 9.327, 9.111, 9.021, 8.517, 7.9, 7.511, 7.569, 7.544, 6.573, 8.761, 10.195, 11.092, 
   10.74, 9.493, 8.888, 8.251, 7.652, 7.896, 7.581, 7.59, 7.539]
  
  highest_freqs = [20, 20, 20, 30, 30, 40, 40, 40, 50, 50, 60, 60, 70, 70, 70, 80, 80, 90]

  volt_ind = 0
  total_ind = 0
  for j in np.arange(0.60, 0.96, 0.02):
    volt_ind = int((j*100 - 60)//2)
    for i in range(20, 150, 10):
      if highest_freqs[volt_ind] == i:
        power_meas.append(total_powers[total_ind])
      total_ind += 1

  for i in np.arange(0.60, 0.96, 0.02):
    voltages.append(round(i, 2))

  # Sample dataset
  x_values = voltages
  y_values0 = fab_meas
  y_values1 = power_meas

  # Plotting the graph
  # plt.plot(x_values, y_values0, label='Static Power')
  # plt.plot(x_values, y_values1, label='Highest Power Consumption with Correct Output')

  # Adding labels and title
  # plt.xlabel('Voltage (in V)')
  # plt.ylabel('Fabric Power Consumption (in mW)')
  # plt.title('Static Power for different V')

  # Adding a legend
  # plt.legend()

  # Display the plot
  # plt.show()

  # stacked bar graph:
  plt.scatter(x_values, y_values1, label='dynamic power consumption', color='#a05195')
  plt.scatter(x_values, y_values0, label='static power consumption', color='#f95d6a')
  plt.xlim(0, 1.4)
  plt.ylim(0, 10)

  # Adding labels and title
  plt.xlabel('Voltage (in V)')
  plt.ylabel('Power (in mW)')
  plt.title('Static Power vs Dynamic Power (at its highest functional frequency) for DMM')

  # Adding a legend
  plt.legend()

  # Display the plot
  plt.show()

find_fab()