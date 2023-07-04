import csv, os


IN_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/data"
OUT_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/output"
datasets = ['a.10.5', 'b.5.0', 'c.0.-5', 'd.-5.-10', 'e.-10.-15', 'f.-15.-20', 'g.-20.-25']


def normalize(value, min_freq, max_freq):
    if max_freq - min_freq == 0:
        return 0.0
    else:
        return (float(value) - min_freq) / (max_freq - min_freq)
    

for dataset in datasets:
    os.chdir(IN_LOC)
    input_csv = f'species_elevation_freq/species_elevation_freq.{dataset}.csv'
    with open(input_csv, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = [row for row in reader]

    min_freqs = [min(float(row[i]) for row in data) for i in range(1, len(header))]
    max_freqs = [max(float(row[i]) for row in data) for i in range(1, len(header))]

    normalized_frequencies = []
    for row in data:
        species = row[0]
        frequencies = [normalize(row[i], min_freqs[i-1], max_freqs[i-1]) for i in range(1, len(row))]
        normalized_frequencies.append([species] + frequencies)

    output_csv = f'species_elevation_freq_normalized.{dataset}.csv'
    os.chdir(OUT_LOC)
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(normalized_frequencies)
