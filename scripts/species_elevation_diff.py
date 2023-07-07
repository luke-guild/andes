import csv
import os

IN_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/data"
OUT_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/output"

def midpoint(elevation_bracket):
    if elevation_bracket == 'N/A':
        return None
    low, _ = map(int, elevation_bracket.split('-'))
    return low + 50  # get midpoint

norm_thresholds = ['0.01', '0.05']
datasets = ['a.10.5', 'b.5.0', 'c.0.-5', 'd.-5.-10', 'e.-10.-15', 'f.-15.-20', 'g.-20.-25']

for threshold in norm_thresholds:
    os.chdir(IN_LOC)

    species_data = {}
    region_presence = {}
    
    for dataset in datasets:
        filename = f'species_min_max_elevation/{threshold}/species_min_max_elevation.{threshold}.{dataset}.csv'
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                species = row[0]
                min_bracket = midpoint(row[1])
                max_bracket = midpoint(row[2])
                # if present in at least 1 region
                if min_bracket is not None and max_bracket is not None:
                    # tally region presence for this species
                    if dataset not in region_presence:
                        region_presence[dataset] = 1
                    else:
                        region_presence[dataset] += 1
                    # then calculate range/diff
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

    # another output csv with only "wide" ranging species that occur in at least 3 lat bands
    output_csv = f'species_elevation_diff_wide.{threshold}.csv'
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['species'] + datasets)
        for species, data in species_data.items():
            if (len(data.values()) < 3):
                continue
            row = [species] + [data.get(dataset, 'N/A') for dataset in datasets]
            writer.writerow(row)

    # the above "wide" output but transposed to fit ggplot better
    output_csv = f'species_elevation_diff_wide_pivot.{threshold}.csv'
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['species', 'region', 'range'])
        for species, data in species_data.items():
            if (len(data.values()) < 3):
                continue
            for dataset in datasets:
                if data.get(dataset):
                    row = [species, dataset] + [data.get(dataset)]
                    writer.writerow(row)

    # species presence (after threshhold)
    output_csv = f'species_elevation_presence.{threshold}.csv'
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['region', 'count'])
        for region, count in region_presence.items():
            writer.writerow([region, count])
