from collections import defaultdict
import csv
import os


IN_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/data"
OUT_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/output"

datasets = ['a.10.5', 'b.5.0', 'c.0.-5', 'd.-5.-10', 'e.-10.-15', 'f.-15.-20', 'g.-20.-25']
elevation_sets = {}
total_elevation_set = defaultdict(lambda: {})
unique_species_set = {}
elevation_counts = {}
sum_count = {}
max_headers = []

os.chdir(IN_LOC)
for dataset in datasets:
    filename = f'species_elevation_count/species_elevation_count.{dataset}.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        data = list(reader)

    if len(headers[1:]) > len(max_headers):
        max_headers = headers[1:]

    elevation_counts[dataset] = {header: 0 for header in max_headers}
    elevation_sets[dataset] = defaultdict(lambda: {})

    for row in data:
        for header, val in zip(max_headers, row[1:]):
            if int(val) > 0:
                elevation_counts[dataset][header] += 1
                elevation_sets[dataset][row[0]] = 1
                total_elevation_set[header][row[0]] = 1
                unique_species_set[row[0]] = 1

os.chdir(OUT_LOC)
with open('species_richness.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Region'] + max_headers + ['Total Unique Species'])

    for dataset in datasets:
        sum_count[dataset] = sum(elevation_counts[dataset].values())
        writer.writerow([dataset] + list(elevation_counts[dataset].values()) + [len(elevation_sets[dataset].keys())])

    total_elevation_set_out = []
    for header in max_headers:
        total_elevation_set_out += [len(total_elevation_set[header].keys())]

    writer.writerow(['All Regions'] + total_elevation_set_out + [len(unique_species_set.keys())])
