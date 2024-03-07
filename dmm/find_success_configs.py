import numpy as np
import csv

output_arr = []

with open('../dmm_unroll_repeat1.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0
  ind = 0
  temp_arr = []
  for row in csv_reader:
    temp_arr.append(row[2])
    if (line_count % 3 == 2):
      if (temp_arr[0] == temp_arr[1] and temp_arr[1] == temp_arr[2]):
        output_arr.append(row[2])
      else:
        print("this configs has some contentions -- ", ind)
        output_arr.append("True")
      temp_arr = []
      ind += 1

    line_count += 1

ind = 0
v = 0
num_v = int((96 - 60)//2)
highest_freqs = [0 for i in range(num_v)]
for i in np.arange(0.60, 0.96, 0.02):
  for j in range(20, 150, 10):
    if (output_arr[ind] == "False"):
      print("({},{:.2f})".format(j, i))
    else:
      highest_freqs[v] = j
    ind += 1
  v += 1

print("highest_freq - ", highest_freqs)
