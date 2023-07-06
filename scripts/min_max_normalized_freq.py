import csv, os

IN_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/data"
OUT_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/output"
datasets = ['a.10.5', 'b.5.0', 'c.0.-5', 'd.-5.-10', 'e.-10.-15', 'f.-15.-20', 'g.-20.-25']

for dataset in datasets:
    os.chdir(IN_LOC)
    input_csv = f'species_elevation_freq_normalized/species_elevation_freq_normalized.{dataset}.csv'
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
    output_csv = f'species_min_max_elevation.0.05.{dataset}.csv'
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Species', 'Min Elevation Bracket', 'Max Elevation Bracket'])
        writer.writerows(species_elevation_ranges)
