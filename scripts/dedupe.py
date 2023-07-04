import os, csv, sys


IN_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/data"
OUT_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/output"
ERRORS_LOC = OUT_LOC


"""
Converts

```csv
species,lat,long,elevation,country,bor
Abatia parviflora,5.055659,-75.495525,2167.0,Colombia,LIVING_SPECIMEN
...
```

to [occurrence]
"""
def read_gbif_data_to_occ_array(filename):
    sys.stdout.write("\nReading GBIF Occurrence Data...")
    os.chdir(IN_LOC)

    occurrences = []
    with open(filename, newline='', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for index, row in enumerate(reader):
            if index == 0:
                continue

            occurrence = {
                'species': row[0],
                'lat': row[1],
                'long': row[2],
                'elevation': row[3],
                'country': row[4],
                'bor': row[5],
            }

            occurrences.append(occurrence)

    return occurrences


"""
write a list of occurrences to csv
"""
def write_occ_to_file(occurrences = [], filname = 'output.csv',):
    os.chdir(OUT_LOC)

    sys.stdout.write("\nWriting to %s..." % filname)
    with open(filname, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([
            'species',
            'lat',
            'long',
            'elevation',
            'country',
            'bor',
        ])
    
        for occ in occurrences:
            writer.writerow([
                occ['species'],
                occ['lat'],
                occ['long'],
                occ['elevation'],
                occ['country'],
                occ['bor'],
            ])

    return


"""
deduplicate occ on lat, long, and elevation (all 3 have to match to be considered a duplicate record)
"""
def deduplicate_occurrences(occurrences = []):
    sys.stdout.write("\nDeduping occurrences...")

    unique_occurrences = []
    unique_id_set = {'foo', 'bar'}
    # for every species, build a set of unique values
    for occ in occurrences:
        id = f'{occ.get("species")}%{occ.get("lat")}%{occ.get("long")}%{occ.get("elevation")}'
        if id in unique_id_set:
            continue
        
        unique_id_set.add(id)
        unique_occurrences.append(occ)

    return unique_occurrences


"""
This file imports and parses the csv data from a huge list of gbif occurence records and produces a new 
csv that's deduplicated on lat, long, and elevation (all 3 have to match to be considered a duplicate record)
"""
if __name__ == "__main__":
    all_occurrences = read_gbif_data_to_occ_array('occurrences.-25.-20.csv')
    unique_occurrences = deduplicate_occurrences(all_occurrences)
    write_occ_to_file(unique_occurrences, 'occurrences_deduped.-25.-20.csv')
