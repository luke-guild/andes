from functools import reduce
from math import ceil, floor
from dedupe import read_gbif_data_to_occ_array
from collections import defaultdict
import os, csv, sys


IN_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/data"
OUT_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/output"
ERRORS_LOC = OUT_LOC


"""
"""
def get_elevation_range_from_occurrences(occurrences = []):
    ele_list = [float(occ.get('elevation')) for occ in occurrences]
    min_ele = reduce(lambda o1, o2: min(o1, o2), ele_list)
    max_ele = reduce(lambda o1, o2: max(o1, o2), ele_list)

    return min_ele, max_ele


"""
"""
def build_species_matrix(occurrences = [], max_elevation = 1):
    species_matrix = defaultdict(lambda: {})
    for occ in occurrences:
        species_matrix[occ.get('species')] = {
            'occurrences': defaultdict(lambda: []),
            'count': defaultdict(lambda: {}),
            'frequency': defaultdict(lambda: {}),
        }

    for _, item in species_matrix.items():
        high_bound = ceil(max_elevation / 100) * 100
        for bottom_bound in range(0, high_bound + 100, 100):
            item['occurrences'][bottom_bound] = []
            item['count'][bottom_bound] = None
            item['frequency'][bottom_bound] = None

    return species_matrix


"""
"""
def hydrate_species_counts(occurrences = [], species_matrix = {}):
    for occ in occurrences:
        species_name = occ.get('species')
        bottom_bound = floor(float(occ.get('elevation')) / 100) * 100
        species_matrix[species_name]['occurrences'][bottom_bound].append(occ)

    for _, item in species_matrix.items():
        for index, occurrences_for_elevation in item['occurrences'].items():
            item['count'][index] = len(occurrences_for_elevation)

    return species_matrix


"""
"""
def calculate_frequency_denominators(species_matrix = {}):
    evelation_frequency_map = defaultdict(lambda: 0)
    for _, item in species_matrix.items():
        for index, count in item['count'].items():
            evelation_frequency_map[index] += count

    return evelation_frequency_map


"""
"""
def hydrate_species_frequencies(species_matrix = {}, frequency_denominators= {}):
    for _, item in species_matrix.items():
        for index, count in item['count'].items():
            if frequency_denominators[index] == 0:
                item['frequency'][index] = 0
            else:
                item['frequency'][index] = count / frequency_denominators[index]

    return species_matrix


"""
write a species matrix to csv
"""
def write_matrix_to_file(species_matrix = {}, matrix_key='count', filname = 'output.csv',):
    os.chdir(OUT_LOC)

    sys.stdout.write("\nWriting to %s..." % filname)
    with open(filname, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        row1 = ['species']
        for index in species_matrix[next(iter(species_matrix))][matrix_key].keys():
            row1.append(f'{index}-{int(index) + 99}')
        writer.writerow(row1)

        for species, item in species_matrix.items():
            inner_row = [species]
            for index, value in item[matrix_key].items():
                inner_row.append(value)
            writer.writerow(inner_row)

    return


"""
"""
if __name__ == "__main__":
    datasets = ['a.10.5', 'b.5.0', 'c.0.-5', 'd.-5.-10', 'e.-10.-15', 'f.-15.-20', 'g.-20.-25']

    for dataset in datasets:
        occurrences = read_gbif_data_to_occ_array(f'filtered_occurrences/filtered_occurrences.{dataset}.csv')
        min_elevation, max_elevation = get_elevation_range_from_occurrences(occurrences)
        species_matrix = build_species_matrix(occurrences, max_elevation)
        species_matrix = hydrate_species_counts(occurrences, species_matrix)
        frequency_denominators = calculate_frequency_denominators(species_matrix)
        species_matrix = hydrate_species_frequencies(species_matrix, frequency_denominators)
        write_matrix_to_file(species_matrix, 'count', f'species_elevation_count.{dataset}.csv')
        write_matrix_to_file(species_matrix, 'frequency', f'species_elevation_freq.{dataset}.csv')
