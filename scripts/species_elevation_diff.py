import csv
import os

IN_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/data"
OUT_LOC = "C:/Users/Luke/Documents/genomics/andes/gbif_analysis/output"


"""
"""
def midpoint(elevation_bracket=""):
    if elevation_bracket == 'N/A':
        return None
    low, _ = map(int, elevation_bracket.split('-'))
    return low + 50  # get midpoint


"""
"""
def read_in_min_max_data(threshold="", regions=[]):
    os.chdir(IN_LOC)

    species_data = {}
    region_presence = {}
    
    for region in regions:
        filename = f'species_min_max_elevation/{threshold}/species_min_max_elevation.{threshold}.{region}.csv'
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
                    if region not in region_presence:
                        region_presence[region] = 1
                    else:
                        region_presence[region] += 1

                    # species details
                    if species not in species_data:
                        species_data[species] = {
                            "ele_range": {},
                            "min_midpoint": {},
                            "max_midpoint": {},
                        }
                    
                    # add min and max elevations
                    species_data[species]["min_midpoint"][region] = min_bracket
                    species_data[species]["max_midpoint"][region] = max_bracket
                    
                    # then calculate range/diff
                    value = max_bracket - min_bracket
                    species_data[species]["ele_range"][region] = value

    return species_data, region_presence


"""
"""
def write_diff_file(threshold="", regions=[], species_data={}):
    os.chdir(OUT_LOC)

    output_csv = f'species_elevation_diff.{threshold}.csv'
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['species'] + regions + ['num_of_regions'])
        for species, data in species_data.items():
            row = [species] + [data["ele_range"].get(region, 'N/A') for region in regions] + [len(data["ele_range"].keys())]
            writer.writerow(row)


"""
"""
def write_pivotted_diff_unified_files(threshold="", regions=[], species_data={}):
    os.chdir(OUT_LOC)

    output_csv = f'species_elevation_diff_unified.{threshold}.csv'
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['species', 'min_elevation', 'max_elevation', 'range'])
        for species, data in species_data.items():
            elevations = [data["ele_range"].get(r) for r in regions if data["ele_range"].get(r) != None]
            min_elevation = min(elevations)
            max_elevation = max(elevations)
            elevation_range = max_elevation - min_elevation
            row = [species] + [min_elevation, max_elevation, elevation_range]
            writer.writerow(row)


"""
species_elevation_diff but pivotted to output 1 row per species,region pair
(TEMP REMOVED) always removes data from g.-20.-25
outputs multiple data sets filtered for "width", 
    i.e. only include data from species that occur in at least n regions
"""
def write_filtered_pivotted_diff_files(threshold="", regions=[], species_data={}):
    os.chdir(OUT_LOC)

    # for width in range(len([r for r in regions if r != 'g.-20.-25'])):
    for width in range(len(regions)):
        output_csv = f'species_elevation_diff_filtered.{width + 1}.{threshold}.csv'
        with open(output_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['species', 'genus', 'region', 'range', 'genus_in_region'])
            region_genus_count = {}

            # loop once for genus tallies
            for species, data in species_data.items():
                # valid_regions = [region for region in data["ele_range"].keys() if region != 'g.-20.-25']
                valid_regions = data["ele_range"].keys()
                if (len(data["ele_range"].values()) < width + 1):
                    continue
                genus = species.split(' ')[0]
                for region in regions:
                    # if region != 'g.-20.-25' and data["ele_range"].get(region):
                    if data["ele_range"].get(region):
                        if (genus, region) in region_genus_count:
                            region_genus_count[(genus, region)] += 1
                        else:
                            region_genus_count[(genus, region)] = 1

            # loop again to write rows
            for species, data in species_data.items():
                # valid_regions = [region for region in data.keys() if region != 'g.-20.-25']
                valid_regions = data["ele_range"].keys()
                if (len(valid_regions) < width + 1):
                    continue
                genus = species.split(' ')[0]
                for region in regions:
                    # if region != 'g.-20.-25' and data["ele_range"].get(region):
                    if data["ele_range"].get(region):
                        row = [species, genus, region, data["ele_range"].get(region), region_genus_count[(genus, region)]]
                        writer.writerow(row)


"""
"""
def write_region_unique_species_count_file(threshold="", region_presence={}):
    os.chdir(OUT_LOC)

    output_csv = f'region_unique_species_count.{threshold}.csv'
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['region', 'count'])
        for region, count in region_presence.items():
            writer.writerow([region, count])


"""
"""
if __name__ == "__main__":
    norm_thresholds = ['0.01', '0.05']
    regions = ['a.10.5', 'b.5.0', 'c.0.-5', 'd.-5.-10', 'e.-10.-15', 'f.-15.-20', 'g.-20.-25']
    
    for threshold in norm_thresholds:
        species_data, region_presence = read_in_min_max_data(threshold, regions)
        write_diff_file(threshold, regions, species_data)
        write_filtered_pivotted_diff_files(threshold, regions, species_data)
        write_pivotted_diff_unified_files(threshold, regions, species_data)
        write_region_unique_species_count_file(threshold, region_presence)
