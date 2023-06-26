import csv, os

IN_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/data"
OUT_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/output"
ERRORS_LOC = OUT_LOC

# Load the normalized frequency CSV
input_csv = 'species_elevation_freq_normalized/species_elevation_freq_normalized.a.10.5.csv'
output_csv = 'species_min_max_elevation.0.05.a.10.5.csv'

os.chdir(IN_LOC)
with open(input_csv, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    data = list(reader)

species_elevation_ranges = []
for row in data:
    species = row[0]
    frequencies = [float(value) for value in row[1:]]

    # Find the indices of frequencies > 0.05
    indices = [i for i, freq in enumerate(frequencies) if freq > 0.05]

    if indices:
        # Find the corresponding elevation brackets
        min_elevation_bracket = header[indices[0] + 1]
        max_elevation_bracket = header[indices[-1] + 1]
    else:
        min_elevation_bracket = 'N/A'
        max_elevation_bracket = 'N/A'

    species_elevation_ranges.append([species, min_elevation_bracket, max_elevation_bracket])

# Write the output to a new CSV file
os.chdir(OUT_LOC)
with open(output_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Species', 'Min Elevation Bracket', 'Max Elevation Bracket'])
    writer.writerows(species_elevation_ranges)

print(f"Species minimum and maximum elevation brackets with a normalized frequency greater than 0.01 have been written to '{output_csv}'")
