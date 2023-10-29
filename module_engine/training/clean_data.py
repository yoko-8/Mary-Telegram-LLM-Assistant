import csv

# Define the input and output file names
input_file = 'training_data.csv'
output_file = 'training_data2.csv'

# Open the input and output CSV files
with open(input_file, 'r', newline='') as input_csv, open(output_file, 'w', newline='') as output_csv:
    # Create CSV reader and writer objects
    reader = csv.DictReader(input_csv)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(output_csv, fieldnames=fieldnames)

    # Write the header to the output file
    writer.writeheader()

    # Iterate through the rows in the input CSV
    for row in reader:
        label = row['label']
        # Check if the label is not "Home Assistant" or "DeepL"
        if label != "News":
            # If the label is not one of the specified values, write the row to the output file
            writer.writerow(row)

print("Rows with 'Home Assistant' and 'DeepL' labels removed. Output saved to", output_file)
