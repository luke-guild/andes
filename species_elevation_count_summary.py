from collections import defaultdict
import csv
import os

IN_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/data"
OUT_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/output"

datasets = ['a.10.5', 'b.5.0', 'c.0.-5', 'd.-5.-10', 'e.-10.-15', 'f.-15.-20', 'g.-20.-25']
output = defaultdict(lambda: 0)

os.chdir(IN_LOC)
for dataset in datasets:
    filename = f'species_elevation_count/species_elevation_count.{dataset}.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        data = list(reader)

    # Count occurrences in buckets for each species
    species_bucket_counts = {row[0]: sum(int(val) > 0 for val in row[1:]) for row in data}

    # Find number of species that occur in only 1 or 2 buckets
    one_bucket_count = sum(count == 1 for count in species_bucket_counts.values())
    two_bucket_count = sum(count == 2 for count in species_bucket_counts.values())

    output[dataset] = [one_bucket_count, two_bucket_count]

os.chdir(OUT_LOC)
with open('species_elevation_count_summary.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['species', 'one_bucket', 'two_buckets'])
    for dataset, data in output.items():
        row = [dataset] + [data[0], data[1]]
        writer.writerow(row)