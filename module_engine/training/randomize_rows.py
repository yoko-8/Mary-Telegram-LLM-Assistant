import csv
import random

# Specify the input and output file names
input_file = 'training_data.csv'
output_file = 'training_data2.csv'

# Read the CSV file into a list of rows
with open(input_file, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)

# Shuffle the list of rows randomly
random.shuffle(rows)

# Write the shuffled list back to a new CSV file
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

print(f'{len(rows)} rows randomized and saved to {output_file}')
