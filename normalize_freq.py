import csv, os

IN_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/data"
OUT_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/output"
ERRORS_LOC = OUT_LOC

# Step 1: Import the CSV
input_csv = 'species_elevation_freq/species_elevation_freq.g.-20.-25.csv'
output_csv = 'species_elevation_freq_normalized.g.-20.-25.csv'

os.chdir(IN_LOC)
with open(input_csv, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    data = [row for row in reader]

# Step 2-3: Find the minimum and maximum frequency value for each column
min_freqs = [min(float(row[i]) for row in data) for i in range(1, len(header))]
max_freqs = [max(float(row[i]) for row in data) for i in range(1, len(header))]

# Step 4: Normalize the frequencies
def normalize(value, min_freq, max_freq):
    if max_freq - min_freq == 0:
        return 0.0
    else:
        return (float(value) - min_freq) / (max_freq - min_freq)

normalized_frequencies = []
for row in data:
    species = row[0]
    frequencies = [normalize(row[i], min_freqs[i-1], max_freqs[i-1]) for i in range(1, len(row))]
    normalized_frequencies.append([species] + frequencies)

# Step 5: Write the normalized data set to a CSV file
os.chdir(OUT_LOC)
with open(output_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(normalized_frequencies)

print(f"Normalized frequencies have been written to '{output_csv}'")
