import numpy as np
import csv
import matplotlib.pyplot as plt

def overall_stats():
  times = []
  highest_freq = [] # vdd_core, vdd_mem, freq
  freqs = []

  # find the times
  with open('./old/dmv_time.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader: 
      highest_freq.append((row[4], row[5], row[6]))
      freqs.append(int(row[6]))
      print(int(row[6]))
      execution_time = (float(row[3].split(":")[2])/30000)
      times.append(execution_time)
      line_count += 1

  print("t_freqs = ", freqs)

  # find the core power consumption:
  vdd_core = []
  i_core = []
  power_core = []
  with open('dmv_unroll_core.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    '''
    example:
    voltage (v),current (a),0.6,0.6,20000000
    0.5973872570000001,0.00319522102
    '''
    for row in csv_reader:
      if ("voltage (v)" not in row):
        vdd_core.append(float(row[0]))
        i_core.append(float(row[1]))
        power_core.append(float(row[0])*float(row[1]))

  # find the mem power consumption:
  vdd_mem = []
  i_mem = []
  power_mem = []
  with open('dmv_unroll_mem.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    '''
    example:
    voltage (v),current (a),0.6,0.6,20000000
    0.5973872570000001,0.00319522102
    '''
    for row in csv_reader:
      if ("voltage (v)" not in row):
        vdd_mem.append(float(row[0]))
        i_mem.append(float(row[1]))
        power_mem.append(float(row[0])*float(row[1]))

  # DMV arith_ops = 8192
  
  # calculate MOPS:
  arith_ops = 8192
  mops_lst = []
  for time in times:
    mops = (arith_ops / time)/10**6
    mops_lst.append(round(mops, 3))

  # calculate GOPS/W
  gops_w_lst = []
  for i in range(len(times)):
    mops = arith_ops / times[i]
    gops_w = (mops / (power_mem[i] + power_core[i]))/10**9
    gops_w_lst.append(round(gops_w, 3))

  min_mops = np.argmin(mops_lst)
  max_mops = np.argmax(mops_lst)

  min_gops = np.argmin(gops_w_lst)
  max_gops = np.argmax(gops_w_lst)

  print("min MOPS = {} with config = {} and execution_time = {} ms"
        .format(mops_lst[min_mops], highest_freq[min_mops], round(times[min_mops]*10**3, 3)))
  print("max MOPS = {} with config = {} and execution_time = {} ms"
        .format(mops_lst[max_mops], highest_freq[max_mops], round(times[max_mops]*10**3, 3)))
  print("min GOPS/W = {} with config = {} and execution_time = {} ms"
        .format(gops_w_lst[min_gops], highest_freq[min_gops], round(times[min_gops]*10**3, 3)))
  print("max GOPS/W = {} with config = {} and execution_time = {} ms"
        .format(gops_w_lst[max_gops], highest_freq[max_gops], round(times[max_gops]*10**3, 3)))

  # plot #1: total energy and voltage against frequency:
  curr_freq = 10000000
  sub_energy_lst = []
  sub_volt_lst = []
  sub_mops_lst = []
  min_energy_lst = [] # y-axis
  min_volt_lst = [] # y-axis
  min_energy_mops_lst = []
  freqs_set = set()

  for i in range(len(freqs)):
    freq = freqs[i]
    freqs_set.add(freq//10**6)

    if (freq != curr_freq): # start of the subset
      min_energy_ind = np.argmin(sub_energy_lst)
      min_volt = sub_volt_lst[min_energy_ind]
      min_energy = sub_energy_lst[min_energy_ind]
      min_energy_lst.append(min_energy)
      min_volt_lst.append(min_volt)
      min_energy_mops_lst.append(sub_mops_lst[min_energy_ind])
      sub_energy_lst = []
      sub_volt_lst = []
      sub_mops_lst = []
      curr_freq = freq
    
    energy = (power_core[i]*times[i] + power_mem[i]*times[i])*10**6
    sub_energy_lst.append(round(energy, 3)) 
    sub_volt_lst.append(vdd_core[i])
    sub_mops_lst.append(round((arith_ops/times[i])/10**6, 3))
    
    if (i == len(freqs) - 1):
      min_energy_ind = np.argmin(sub_energy_lst)
      min_volt = sub_volt_lst[min_energy_ind]
      min_energy = sub_energy_lst[min_energy_ind]
      min_energy_lst.append(min_energy)
      min_volt_lst.append(min_volt)
      min_energy_mops_lst.append(sub_mops_lst[min_energy_ind])
      

  # conver the Hz to MHz:
  freqs_axis = sorted(list(freqs_set))

  # scatter plot:
  fig, ax = plt.subplots()
  fig.subplots_adjust(right=0.75)

  twin1 = ax.twinx() # voltage on the right and energy on the left

  # "#7B2D43", "#59B217"
  p1 = ax.scatter(freqs_axis, min_energy_lst, label="Energy (in uJ)", color = "#7B2D43")
  p2 = twin1.scatter(freqs_axis, min_volt_lst, label="Voltage (in V)", color = "#59B217")

  ax.set(xlim=(0, 140), ylim=(0, 0.5), xlabel="Frequency (in MHz)", ylabel="Energy (in uJ)")
  twin1.set(ylim=(0, 1), ylabel="Voltage (in V)")
  
  ax.legend(handles=[p1, p2])

  plt.show()
  
  # Plot #2: Energy against MOPS
  energy_lst = []
  for i in range(len(mops_lst)):
    energy = (power_core[i]*times[i] + power_mem[i]*times[i])*10**6
    energy_lst.append(round(energy, 3))

  print(min_energy_mops_lst)
  print(min_energy_lst)

  # Adding labels and title
  plt.scatter(min_energy_mops_lst, min_energy_lst, label='Energy Consumption v MOPS')
  # plt.scatter(mops_lst, energy_lst, label='Energy Consumption v MOPS')

  plt.xlabel('MOPS')
  plt.xlim((0, 330))
  plt.ylabel('Energy (in uJ)')
  plt.ylim((0, 1))

  # plt.title('Min. Energy vs MOPS for Dense Matrix Multiply (arith_ops = 524288)')

  # Adding a legend
  plt.legend()

  # Display the plot
  plt.show()

  # Plot #3: Max GOPS/W

  print(freqs)
  print(gops_w_lst)

  curr_freq = 10000000
  max_gops_lst = []
  sub_gops_lst = []

  for i in range(len(freqs)):
    freq = freqs[i]
    print(freq, sub_gops_lst)

    if (freq != curr_freq): # start of the subset
      max_gops_lst.append(max(sub_gops_lst))
      sub_gops_lst = []
      curr_freq = freq
    
    mops = arith_ops/times[i]
    gops_w = mops / (power_core[i] + power_mem[i])

    sub_gops_lst.append(round(gops_w/10**9, 3))
    
    if (i == len(freqs) - 1):
      max_gops_lst.append(max(sub_gops_lst))

  print("plotting graph 3 - ")
  print(freqs_axis)
  print(max_gops_lst)

  plt.scatter(freqs_axis, max_gops_lst, label="Max GOPS/W per MHz Freq")
  plt.xlim(0, 140) # freqs
  plt.ylim(0, 65)

  # Adding labels and title
  plt.xlabel('Frequnecy (in MHz)')
  plt.ylabel('GOPS/W')

  # plt.title('Max GOPS/W per Freq -- Arith_Ops = 524288 for dmv')

  # Adding a legend
  plt.legend()

  # Display the plot
  plt.show()

  # Plot #4: static vs dynamic power for DMM

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

  total_fab_power = []
  total_power = []
  fab_ratio = []
  for i in range(len(power_core)):
    total_fab_power.append(round(power_fab_core[i] * power_fab_mem[i] * 10**6, 2))
    total_power.append(round(power_core[i] * power_mem[i] * 10**6, 2))
    fab_ratio.append(total_fab_power[i] / total_power[i])

  # print(total_fab_power, len(total_fab_power))
  # print(total_power, len(total_power))
  print(fab_ratio)


  volt_axis = []
  for i in np.arange(0.60, 0.96, 0.02):
    volt = round(i, 2)
    volt_axis.append(volt)

  plt.scatter(volt_axis, total_power, label='dynamic power consumption', color='#a05195')
  plt.scatter(volt_axis, total_fab_power, label='static power consumption', color='#f95d6a')
  plt.xlim(0, 1.0)
  plt.ylim(0, 10)

  # Adding labels and title
  plt.xlabel('Voltage (in V)')
  plt.ylabel('Power (in uW)')
  plt.title('Static Power vs Dynamic Power (at its highest functional frequency) for DMV')


  # plt.title('Max GOPS/W per Freq -- Arith_Ops = 524288 for dmv')

  # Adding a legend
  plt.legend()

  # Display the plot
  plt.show()

  

overall_stats()