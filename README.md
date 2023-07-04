# Collecting and analyzing gbif occurrence data

## Step 1: Querying the data from GBIF
Using the forest plot data, we generated a list of unique species and filtered out all morphos and indets. 

We then queried GBIF for the species' [usage/taxon key](https://discourse.gbif.org/t/understanding-gbif-taxonomic-keys-usagekey-taxonkey-specieskey/3045) with the GBIF [Species API]() using the `species/match` endpoint with the following parameters:
```
'status': 'ACCEPTED', 
'rank': 'SPECIES', 
'name': species_name,
```
Where `species_name` is the name of the particular species we're querying for to form a list of keys we could use to query GBIF for occurrences.

We then queried the [GBIF Occurence API](https://www.gbif.org/developer/occurrence) using the `/occurrence/search` endpoint with the following parameters:

```
'usage_key': usage_key
'hasCoordinate': True,
'elevation' = '150,4000'
'geometry' = 'POLYGON((-80 11,-63 11,-63 -26,-80 -26, -80 11))'
'decimalLatitude': lat_filer
```
Where `usage_key` is the usage key for a particular species fetched from the above `species/match` api endpoint, and `lat_filer` is a pair of latitudes that form the boundaries for this particular search. The search is done for all species against a particular `lat_filter` and then replicated entirely for each `lat_filter`.

In total, there were 2574 unique accepted species and 7 different latitudinal ranges. In addition, each occurrence query was limited to 300 occurrences for performance reasons. If a species had more than 300 occurrence records in a latitudinal range we used an `offset` parameter to query the remaining occurrences until all records were fetched, meaning some species took many queries to fetch all of their occurrences. In all this amounted to an estimated 20000+ API requests to the GBIF occurrence API, resulting in an unfiltered collection of 775,088 occurrences.

## Step 2: Data cleaning

In order to sanitize the data we had to ensure there were no duplicate records both within a latitudinal range and between latitudinal ranges. For the former, we ran through all occurrences in each file (the files are distinct latitudinal ranges) and eliminated any records that were duplicated on species, latitude, longitude, and elevation. This not only eliminated any possible erroneous duplication of the same records but also removed multiple observations recorded from the same site, resulting in a 1-record-per-site occurrence list. Code for performing this deduplication can be found in `dedupe.py`. We also needed to account for the fact that there was some overlap in the occurrences pulled for different latitudinal ranges when considering the minimum lat value for one range vs the maximum lat value for the next range. For example, a range query of `10,5` and a range query of `5,0` have overlap at the `5.0` latitudinal value. We elected to eliminate occurrences at the minimum lat value for each range, meaning that all occurrences at exactly latitude `5.0` in the `10,5` range set were deleted, all of the `0.0` occurrences in the `5,0` set, etc.. This process was performed by hand. It's important to note that this process did not eliminate any unique data from the overall occurrence data collection, occurrence removed from one file were all present in the subsequent file. This left us with a total collection of 386,962 occurrences.

## Step 3: Analysis

We generated artifacts for each latitudal range independently. From each range's occurrence set we calculated:
- Counts for how many times a species occurred in a 100m elevation range (keep in mind this is only tracking 1 occurrence per site)
```csv
species,0-99,100-199,200-299,300-399,...
Abatia parviflora,0,0,0,0,...
Acalypha cuneata,0,2,1,8,...
...
```

- The relative frequency at which each species occurred in each elevation bucket compared to the rest of the species in the set
```csv
species,0-99,100-199,200-299,300-399,...
Abatia parviflora,0.0,0.0,0.0,0.0,...
Acalypha cuneata,0.0,0.0003471017007983339,0.00015928639694170118,0.0012511729746637473,...
...
```

- The above frequencies normalized by the elevational range they're present in
```csv
species,0-99,100-199,200-299,300-399,...
Abatia parviflora,0.0,0.0,0.0,0.0,...
Acalypha cuneata,0.0,0.0036101083032490976,0.005555555555555556,0.020512820512820513,...
...
```

- Each species' minimum and maximum elevation buckets where they occur with a normalized frequency greater than or equal to a given threshhold (0.01 and 0.05)
```csv
Species,Min Elevation Bracket,Max Elevation Bracket
Abatia parviflora,1900-1999,3300-3399
Acalypha cuneata,300-399,300-399
...
```

Code for performing this analysis can be found in `counts_and_freq.py`, `normalize.py`, and `min_max_normalized_freq.py`.

___

We generated a combined data set that compared the elevation ranges of each species within each latitudinal band, and created versions for each threshhold (0.01 and 0.05) used in generating the normalized frequencies. The `range/diff` is calculated from the midpoint of each elevation bucket (ie 1450 for 1400-1499):
```csv
species,a.10.5,b.5.0,c.0.-5,d.-5.-10,e.-10.-15,f.-15.-20,g.-20.-25
Abatia parviflora,300,1600,2600,800,0,N/A,N/A
Acalypha cuneata,0,800,2000,1700,1100,400,N/A
...
```

Code for performing this analysis can be found in `species_elevation_diff.py`

___

We generated a combined data set that counted how many times, in each latitudinal band, a species occurred in only one or two buckets:
```csv
species,q1,q2
a.10.5,149,120
b.5.0,199,131
...
```

Code for performing this analysis can be found in `species_elevation_count_summary.py`

___

We created a matrix of the amount of unique species located in each elevation bucket across each latitudinal band, and among the entire sampling region:
```csv
Region,0-99,100-199,200-299,...,Total Unique Species
a.10.5,0,771,893,...,1811
b.5.0,0,710,1025,...,1901
...
All Regions,0,1327,1546,...,2446
```

Code for performing this analysis can be found in `species_richness.py`
