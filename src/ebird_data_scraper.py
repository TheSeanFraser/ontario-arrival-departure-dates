import datetime
from pathlib import Path

import requests as req
import config

ont_all_years_url = "https://ebird.org/linegraph?bmo=1&emo=12&byr=1900&eyr=2022&r=CA-ON&spp="
ont_20_years_url = "https://ebird.org/linegraph?bmo=1&emo=12&byr=2002&eyr=2022&r=CA-ON&spp="
tor_all_years_url = "https://ebird.org/linegraph?bmo=1&emo=12&byr=1900&eyr=2022&r=CA-ON-TO&spp="
tor_20_years_url = "https://ebird.org/linegraph?bmo=1&emo=12&byr=2002&eyr=2022&r=CA-ON-TO&spp="

url1 = "https://ebird.org/linegraph?bmo=1&emo=12&byr="
url2_start_year = "2002"
url3_end_year_tag = "&eyr="
url4_end_year = "2002"
url5_region_tag = "&r="
url6_region = "CA-ON"
url7_species_tag = "&spp="
url8_species = "barswa"
url9_post = "&fmt=tsv"


# Removes quotes from species codes
def fix_species_quotes(species):
    if "\"" in species:
        species = species[:-1]
    if "\"" in species:
        species = species[:-1]

    return species


# Downloads eBird frequency data
def get_charts():
    species_list = open("../res/ont_species_6letter_likely.txt",
                        'r').read().splitlines()

    # For each year of available data, get everything
    for year in range(1952, 2022):

        Path(config.data_dir + "\ontario\\" + str(year)).mkdir(parents=True, exist_ok=True)
        for species in species_list:
            species_fixed = fix_species_quotes(species)
            url2_start_year = str(year)
            url4_end_year = str(year)
            year_url = url1 + url2_start_year + url3_end_year_tag \
                       + url4_end_year + url5_region_tag + url6_region \
                       + url7_species_tag + url8_species + url9_post

            # Get data from web
            session = req.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'})

            r = session.get(year_url)

            # Write to file
            f = open(config.data_dir + "ontario\\" + str(year) + "\\" + str(year) + species_fixed + ".txt",
                     "w", encoding="utf-8")
            f.write(r.text)
            f.close()

        print(str(year) + " complete" + str(datetime.datetime.now()))


get_charts()
