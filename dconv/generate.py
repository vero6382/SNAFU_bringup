import matplotlib.pyplot as plt
import numpy as np
import csv

# Generate some sample data (replace this with your actual data)
freq = np.linspace(20, 140, 10) # 20 - 140 MHz by 10 MHz
voltage = np.arange(0.6, 0.94, 0.2) # 0.6 - 0.94 V by 0.2 V

# Create a meshgrid for x and y values
X, Y = np.meshgrid(freq, voltage)

output_dict = dict() # keys = (freq, voltage)

output_arr = []
with open('dmm_unroll_repeat1.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0
  for row in csv_reader:
    output_arr.append(row[2])

print(output_arr)

# Define a function that represents the performance of your device
# This is just a placeholder; replace it with your actual performance data
def isSuccessful(freq, voltage):
  int_v = voltage*100
  ind = ((int_v-60)//2) *((150 - 20)//10) + (freq-20)//10
  print(freq, voltage, ind)
  output = output_arr[ind]
  if (output == "False"): return False
  return True

# Calculate the Z values (performance) using the function
Z = isSuccessful(X, Y)

# Create the Shmoo plot
fig, ax = plt.subplots()
shmoo_plot = ax.contourf(X, Y, Z, cmap='viridis')
plt.colorbar(shmoo_plot, label='Performance')

# Set axis labels and title
ax.set_xlabel('Frequency (in MHz)')
ax.set_ylabel('Voltage (in V)')
plt.title('Shmoo Plot')

# Show the plot
plt.show()
