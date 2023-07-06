import csv
import os


LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis"
datasets = ['a.10.5', 'b.5.0', 'c.0.-5', 'd.-5.-10', 'e.-10.-15', 'f.-15.-20', 'g.-20.-25']
allowed_countries = {'Colombia', 'Peru', 'Bolivia (Plurinational State of)', 'Ecuador', 'Argentina', 'Venezuela (Bolivarian Republic of)'}
allowed_bor = {'PRESERVED_SPECIMEN'}


os.chdir(LOC)
for dataset in datasets:
    input_filename = f'data/deduped_occurrences/occurrences_deduped.{dataset}.csv'
    output_filename = f'output/filtered_occurrences.{dataset}.csv'
    with open(input_filename, 'r') as f_in, open(output_filename, 'w', newline='') as f_out:
        reader = csv.reader(f_in)
        writer = csv.writer(f_out)
        headers = next(reader)
        writer.writerow(headers)

        for row in reader:
            species, lat, long, elevation, country, bor = row
            if country in allowed_countries and bor in allowed_bor:
                writer.writerow(row)
