import datetime
import json
from pathlib import Path
import concurrent.futures
import re
import requests as req
import config

# Split the complete URL into discrete parts for easy alterations
url1 = "https://ebird.org/linegraph?bmo=1&emo=12&byr="
url2_start_year = "2002"
url3_end_year_tag = "&eyr="
url4_end_year = "2002"
url5_region_tag = "&r="
url6_region = "CA-ON-TO"
url7_species_tag = "&spp="
url8_species = "barswa"
url9_post = "&fmt=tsv"

# Flag for downloading every year or past 20 years
every_year = False


# Downloads eBird frequency data
def get_charts(region="Ontario"):
    global every_year

    # Load the list of species we are working with
    species_list = open("../res/ont_species_all_2025.txt",
                        'r').read().splitlines()

    # Load the list of eBird regions in Ontario
    with open(config.res_dir + "regions_completeYO.json") as json_file:
        regions_dict = json.load(json_file)

    print("Starting...")

    # Iterate through every region to get all data
    for region in regions_dict:
        print("Now working on: ", region, regions_dict[region])
        url6_region = regions_dict[region]

        # Build the URL list to download
        url_list = []
        year = "20_YEARS"

        for species in species_list:
            url2_start_year = "2004"
            url4_end_year = "2024"
            url8_species = species
            year_url = url1 + url2_start_year + url3_end_year_tag \
                       + url4_end_year + url5_region_tag + url6_region \
                       + url7_species_tag + url8_species + url9_post
            url_list.append(year_url)

        # Download multiple urls with threads
        # with concurrent.futures.ThreadPoolExecutor(
        #         max_workers=2) as executor:
        #     executor.map(download_url_multi, url_list)

        for url in url_list:
            download_url_multi(url)


        print(str(year) + " complete: " + str(datetime.datetime.now()))


# Downloads URL from eBird
def download_url_multi(url):
    global every_year
    # Get data from web
    session = req.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'})

    r = session.get(url)

    file_path = ""

    # Use RegEx to extract the year, region, and species for the filepath
    year = "20_YEARS"
    region = re.search("r=(\D*)&s", url).group(1)
    species = re.search("spp=(.*)&fmt", url).group(1)
    file_path = config.regions_data_dir + region + "\\" + year + "\\" \
                + year + "_" + species + ".txt"

    # Make sure file path exists first
    Path(config.regions_data_dir + "\\" + region + "\\" + str(year)).mkdir(parents=True,
                                                                           exist_ok=True)
    # Write to file
    f = open(file_path, "w", encoding="utf-8")
    f.write(r.text)
    f.close()


get_charts()


