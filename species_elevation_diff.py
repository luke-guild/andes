import csv
import os

IN_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/data"
OUT_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/output"

def midpoint(elevation_bracket):
    if elevation_bracket == 'N/A':
        return None
    low, _ = map(int, elevation_bracket.split('-'))
    return low + 50  # Get midpoint

norm_thresholds = ['0.01', '0.05']
datasets = ['a.10.5', 'b.5.0', 'c.0.-5', 'd.-5.-10', 'e.-10.-15', 'f.-15.-20', 'g.-20.-25']

species_data = {}
for threshold in norm_thresholds:
    os.chdir(IN_LOC)
    for dataset in datasets:
        filename = f'species_min_max_elevation/{threshold}/species_min_max_elevation.{threshold}.{dataset}.csv'
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                species = row[0]
                min_bracket = midpoint(row[1])
                max_bracket = midpoint(row[2])
                if min_bracket is not None and max_bracket is not None:
                    value = max_bracket - min_bracket
                    if species not in species_data:
                        species_data[species] = {}
                    species_data[species][dataset] = value

    os.chdir(OUT_LOC)
    output_csv = f'species_elevation_diff.{threshold}.csv'
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['species'] + datasets)
        for species, data in species_data.items():
            row = [species] + [data.get(dataset, 'N/A') for dataset in datasets]
            writer.writerow(row)
