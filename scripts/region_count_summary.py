from collections import defaultdict
import csv
import os

IN_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/data"
OUT_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/output"

regions = ['a.10.5', 'b.5.0', 'c.0.-5', 'd.-5.-10', 'e.-10.-15', 'f.-15.-20', 'g.-20.-25']
region_output = defaultdict(lambda: 0)
region_elevation_output = defaultdict(lambda: 0)

os.chdir(IN_LOC)
for region in regions:
    filename = f'species_elevation_count/species_elevation_count.{region}.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
        headers = data.pop(0)

    # count region q1s and q2s
    species_occurrences_in_region = {}
    for row in data:
        species = row[0]
        occurrences_per_elevation = row[1:]
        species_occurrences_in_region[species] = sum(int(num_occurrences) > 0 for num_occurrences in occurrences_per_elevation)

    region_q1 = sum(count == 1 for count in species_occurrences_in_region.values())
    region_q2 = sum(count == 2 for count in species_occurrences_in_region.values())
    region_output[region] = [region_q1, region_q2]

    # count region+elevation q1s and q2s
    region_elevation_q1 = defaultdict(lambda: 0)
    region_elevation_q2 = defaultdict(lambda: 0)
    for row in data:
        for index, value in enumerate(row[1:]):
            if int(value) == 1:
                region_elevation_q1[headers[index + 1]] += 1
            if int(value) == 2:
                region_elevation_q2[headers[index + 1]] += 1

    for elevation in headers[1:]:
        region_elevation_output[(region, elevation)] = [region_elevation_q1[elevation], region_elevation_q2[elevation]]


os.chdir(OUT_LOC)
with open('region_count_summary.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['region', 'q1', 'q2'])
    for region, data in region_output.items():
        row = [region] + [data[0], data[1]]
        writer.writerow(row)

with open('region_elevation_count_summary.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['region', 'elevation', 'q1', 'q2'])
    for region_elevation, data in region_elevation_output.items():
        row = [region_elevation[0], region_elevation[1], data[0], data[1]]
        writer.writerow(row)
