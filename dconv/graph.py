import numpy as np
import csv
import matplotlib.pyplot as plt

def overall_stats():
  times = []
  highest_freq = [] # vdd_core, vdd_mem, freq
  freqs = []
  sorted_times = []

  # find the times
  with open('dconv_unroll.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
      if (line_count % 2 == 1): 
        highest_freq.append((row[4], row[5], row[6]))
        execution_time = (float(row[3].split(":")[2])/5000)
        if (row[2] == "True"):
          times.append(execution_time)
          sorted_times.append(execution_time)
          freqs.append(int(row[6]))
        else:
          times.append(-1) # invalidate this data point
          print("re-measure this - ", row)
      line_count += 1

  # find the core power consumption:
  vdd_core = []
  i_core = []
  power_core = []
  with open('dconv_unroll_core.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    '''
    example:
    voltage (v),current (a),0.6,0.6,20000000
    0.5973872570000001,0.00319522102
    '''
    temp_vdd = 0
    temp_i = 0
    for row in csv_reader:
      line_count += 1
      if ("voltage (v)" not in row):
        temp_vdd += float(row[0])
        temp_i += float(row[1])
      if (line_count % 6 == 0 and times[line_count // 6 - 1] != -1):
        # print(temp_vdd, temp_i)
        vdd_core.append(temp_vdd / 3) # V
        i_core.append((temp_i / 3)) # A
        power_core.append((temp_vdd / 3)*(temp_i / 3)) # W
        temp_vdd = 0
        temp_i = 0
      elif (line_count % 6 == 0):
        temp_vdd = 0
        temp_i = 0

  # find the mem power consumption:
  vdd_mem = []
  i_mem = []
  power_mem = []
  with open('dconv_unroll_mem.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    '''
    example:
    voltage (v),current (a),0.6,0.6,20000000
    0.5973872570000001,0.00319522102
    '''
    temp_vdd = 0
    temp_i = 0
    for row in csv_reader:
      line_count += 1
      if ("voltage (v)" not in row):
        temp_vdd += float(row[0])
        temp_i += float(row[1])
      if (line_count % 6 == 0 and times[line_count // 6 - 1] != -1):
        # print(temp_vdd, temp_i)
        vdd_mem.append(temp_vdd / 3) # V
        i_mem.append((temp_i / 3)) # A
        power_mem.append((temp_vdd / 3)*(temp_i / 3)) #W
        temp_vdd = 0
        temp_i = 0
      elif (line_count % 6 == 0):
        temp_vdd = 0
        temp_i = 0

  total_power_lst = []
  total_energy_lst = []
  for i in range(len(power_core)):
    total_power_lst.append(power_core[i] + power_mem[i])
    print("total_power = {} and power_core = {} and power_mem = {}".format(power_core[i] + power_mem[i], power_core[i], power_mem[i]))
    total_energy_lst.append(total_power_lst[i]*sorted_times[i])
    print("energy - ", total_energy_lst[i])

  if (len(power_core) == len(total_power_lst) == len(freqs)):
    print("they are of the same length...")
  
  # calculate MOPS:
  arith_ops = 180000
  mops_lst = []
  for time in sorted_times:
    mops = (arith_ops / time)
    mops_lst.append(mops)
        
  # print("times - ", times)

  # calculate GOPS/W
  gops_w_lst = []
  for i in range(len(mops_lst)):
    mops = mops_lst[i]
    gops_w = (mops / total_power_lst[i])/10**9
    gops_w_lst.append(round(gops_w, 3))

  # print("gops - ", gops_w_lst)

  min_mops = np.argmin(mops_lst)
  max_mops = np.argmax(mops_lst)

  min_gops = np.argmin(gops_w_lst)
  max_gops = np.argmax(gops_w_lst)

  print("min MOPS = {} with config = {} and execution_time = {} ms"
        .format(round(mops_lst[min_mops]/10**6, 2), highest_freq[min_mops], round(times[min_mops]*10**3, 3)))
  print("max MOPS = {} with config = {} and execution_time = {} ms"
        .format(round(mops_lst[max_mops]/10**6, 2), highest_freq[max_mops], round(times[max_mops]*10**3, 3)))
  print("min GOPS/W = {} with config = {} and execution_time = {} ms"
        .format(gops_w_lst[min_gops], highest_freq[min_gops], round(times[min_gops]*10**3, 3)))
  print("max GOPS/W = {} with config = {} and execution_time = {} ms"
        .format(gops_w_lst[max_gops], highest_freq[max_gops], round(times[max_gops]*10**3, 3)))

  # plot #1: total energy and voltage against frequency:
  # Create a dictionary to store the lowest energy point per frequency
  min_energy_per_freq = {}

  # Iterate through the data
  for i in range(len(freqs)):
      current_freq = freqs[i]

      # If the frequency is not in the dictionary or the energy is lower, update the values
      if current_freq not in min_energy_per_freq or total_energy_lst[i] < min_energy_per_freq[current_freq]['energy']:
          min_energy_per_freq[current_freq] = {
              'voltage': vdd_core[i],
              'power': total_power_lst[i],
              'energy': total_energy_lst[i],
              'time' : sorted_times[i]
          }

  # Print the results
  print("Lowest energy consumption per frequency:")
  freqs_axis = []
  min_energy_lst = []
  min_volt_lst = []
  min_energy_times = []
  for freq, values in min_energy_per_freq.items():
      print(f"Frequency: {freq}, Voltage: {values['voltage']}, Power: {values['power']}, Energy: {values['energy']}")
      freqs_axis.append(freq/10**6)
      min_energy_lst.append(round(values['energy']*10**6, 2)) # uW
      min_volt_lst.append(values['voltage' ])
      min_energy_times.append(values['time'])
      
  # scatter plot:
  fig, ax = plt.subplots()
  fig.subplots_adjust(right=0.75)

  twin1 = ax.twinx() # voltage on the right and energy on the left

  # "#7B2D43", "#59B217"
  p1 = ax.scatter(freqs_axis, min_energy_lst, label="Energy (in uJ)", color = "#7B2D43")
  p2 = twin1.scatter(freqs_axis, min_volt_lst, label="Voltage (in V)", color = "#59B217")

  ax.set(xlim=(0, 100), ylim=(0, 30), xlabel="Frequency (in MHz)", ylabel="Energy (in uJ)")
  twin1.set(ylim=(0, 1.25), ylabel="Voltage (in V)")
  
  ax.legend(handles=[p1, p2])

  plt.show()
  
  # Plot #2: Energy against MOPS
  min_energy_mops_lst = []
  for i in range(len(freqs_axis)):
    time = min_energy_times[i]
    min_energy_mops_lst.append(round((arith_ops / time)/10**6, 3)) # MOPS
  
  print(min_energy_mops_lst) 
  print(min_energy_lst) 

  # Adding labels and title
  plt.scatter(min_energy_mops_lst, min_energy_lst, label='Energy Consumption v MOPS')
  # plt.scatter(mops_lst, energy_lst, label='Energy Consumption v MOPS')

  plt.xlabel('MOPS')
  plt.xlim((0, 300))
  plt.ylabel('Energy (in uJ)')
  plt.ylim((0, 40))

  # plt.title('Min. Energy vs MOPS for Dense Matrix Multiply (arith_ops = 524288)')

  # Adding a legend
  plt.legend()

  # Display the plot
  plt.show()

  # Plot #3: Max GOPS/W
  max_gops_per_freq = {}

  print("gops/w ")
  for i in range(len(freqs)):
    print(freqs[i])
    print(mops_lst[i])
    print(total_power_lst[i])
    print(gops_w_lst[i])

  # Iterate through the data
  for i in range(len(freqs)):
      current_freq = freqs[i]

      # If the frequency is not in the dictionary or the energy is lower, update the values
      if current_freq not in max_gops_per_freq or gops_w_lst[i] > max_gops_per_freq[current_freq]['gops']:
          max_gops_per_freq[current_freq] = {
              'voltage': vdd_core[i],
              'power': total_power_lst[i],
              'energy': total_energy_lst[i],
              'time' : sorted_times[i],
              'gops' : gops_w_lst[i]
          }
  
  max_gops_lst = []
  for freq, values in max_gops_per_freq.items():
      print(f"Frequency: {freq}, GOPS/W : {values['gops']} Voltage: {values['voltage']}, Power: {values['power']}, Energy: {values['energy']}")
      max_gops_lst.append(values['gops'])

  print("plotting graph 3 - ")
  print(freqs_axis)
  print(max_gops_lst)

  plt.scatter(freqs_axis, max_gops_lst, label="Max GOPS/W per MHz Freq")
  plt.xlim(0, 140) # freqs
  plt.ylim(0, 40)

  # Adding labels and title
  plt.xlabel('Frequnecy (in MHz)')
  plt.ylabel('GOPS/W')

  # plt.title('Max GOPS/W per Freq -- Arith_Ops = 524288 for dconv')

  # Adding a legend
  plt.legend()

  # Display the plot
  plt.show()

  # Plot #4: static vs dynamic power for dconv
  power_fab_core = []
  power_fab_mem = []
  with open('../fab_core.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
      if ("voltage (v)" not in row): 
        power_fab_core.append(float(row[0]) * float(row[1]))

  with open('../fab_mem.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
      if ("voltage (v)" not in row): 
        power_fab_mem.append(float(row[0]) * float(row[1]))   

  print("power_fab_core - ", power_fab_core)
  print("power_fab_mem - ", power_fab_mem)

  total_fab_power = []
  print(len(power_core), len(power_fab_core))
  for i in range(len(power_fab_core)):
    total_fab_power.append(round((power_fab_core[i] + power_fab_mem[i]) * 10**3, 2))

  for j in range(len(total_power_lst)):
    total_power_lst[j] = total_power_lst[j]*10**3 # mW

  print("total_fab_power - ", total_fab_power)
  print("total_power_lst - ", total_power_lst)

  # print(total_fab_power, len(total_fab_power))
  # print(total_power, len(total_power))

  volt_axis = []
  for i in np.arange(0.56, 0.96, 0.02):
    volt = round(i, 2)
    volt_axis.append(volt)

  plt.scatter(vdd_core, total_power_lst, label='dynamic power consumption', color='#a05195')
  plt.scatter(volt_axis, total_fab_power, label='static power consumption', color='#f95d6a')
  plt.xlim(0, 1.0)
  plt.ylim(0, 20)

  # Adding labels and title
  plt.xlabel('Voltage (in V)')
  plt.ylabel('Power (in mW)')
  plt.title('Static Power vs Dynamic Power (at its highest functional frequency) for dconv')


  # plt.title('Max GOPS/W per Freq -- Arith_Ops = 524288 for dconv')

  # Adding a legend
  plt.legend()

  # Display the plot
  plt.show()

  

overall_stats()