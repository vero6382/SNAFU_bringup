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
  total_powers =  [2.076, 2.098, 1.156, 2.021, 1.172, 2.092, 2.45, 2.86, 3.541, 2.024, 2.08, 2.436, 2.859, 3.458, 3.905, 4.439, 4.593, 5.344, 5.433, 5.819, 6.282, 6.284, 6.264, 2.174, 3.17, 3.509, 3.563, 4.268, 4.775, 5.256, 5.79, 6.007, 6.271, 6.661, 6.709, 6.721, 2.457, 2.976, 3.267, 3.943, 4.58, 5.074, 5.513, 6.168, 6.474, 6.653, 6.919, 6.956, 6.968, 2.511, 3.057, 3.553, 4.263, 4.603, 5.411, 6.046, 6.51, 6.843, 6.665, 6.188, 6.279, 6.243, 2.858, 3.454, 4.037, 4.584, 4.862, 5.399, 6.35, 6.785, 7.105, 6.76, 6.249, 6.416, 6.306, 3.044, 3.513, 4.342, 4.872, 5.462, 5.879, 6.806, 7.303, 7.238, 6.705, 6.37, 6.447, 6.332, 3.342, 3.766, 4.568, 5.376, 5.89, 6.244, 6.802, 7.455, 7.331, 6.779, 6.403, 6.34, 6.472, 3.53, 4.004, 4.666, 5.551, 6.288, 6.605, 7.283, 7.892, 7.361, 7.616, 6.737, 6.55, 6.468, 3.619, 4.583, 5.332, 6.164, 6.661, 7.02, 7.708, 8.385, 8.136, 7.025, 6.535, 6.568, 6.502, 3.893, 4.835, 5.59, 6.301, 7.536, 7.49, 8.219, 8.772, 8.187, 7.711, 6.574, 7.262, 6.548, 4.165, 5.236, 5.695, 7.22, 8.194, 7.986, 8.816, 8.793, 8.275, 7.738, 6.721, 6.663, 6.732, 4.479, 5.313, 6.105, 7.189, 8.763, 8.66, 9.338, 8.806, 8.289, 7.798, 7.362, 7.364, 7.427, 4.777, 5.972, 6.938, 7.651, 9.348, 9.637, 8.716, 8.923, 8.371, 7.9, 7.48, 7.48, 7.521, 5.685, 6.463, 7.682, 8.1, 9.763, 9.39, 8.766, 9.007, 8.475, 8.028, 7.575, 7.596, 7.6, 5.567, 7.161, 7.42, 9.616, 10.277, 9.437, 9.643, 9.102, 8.592, 8.149, 7.69, 7.713, 7.716, 6.555, 7.797, 7.883, 10.279, 10.621, 9.997, 8.921, 8.482, 8.709, 8.306, 7.861, 7.825, 7.91, 7.167, 8.073, 9.481, 10.691, 10.996, 9.719, 9.165, 8.597, 8.847, 8.459, 8.093, 7.962, 8.019, 7.792, 8.953, 9.164]
  
  highest_freqs = [20, 20, 20, 30, 30, 40, 40, 40, 50, 50, 60, 60, 60, 70, 70, 70, 80, 80]

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
  plt.bar(x_values, y_values1, width = 0.01, label='dynamic power consumption', color='#a05195')
  plt.bar(x_values, y_values0, width = 0.01, label='static power consumption', color='#f95d6a')

  # Adding labels and title
  plt.xlabel('Voltage (in V)')
  plt.ylabel('Power (in mW)')
  plt.title('Static Power vs Dynamic Power (at its highest functional frequency) for DMV')

  # Adding a legend
  plt.legend()

  # Display the plot
  plt.show()

find_fab()