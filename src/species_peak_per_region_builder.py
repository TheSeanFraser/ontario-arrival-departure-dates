import json
import os
import pathlib
import re
from _csv import reader
import pandas as pd
import config


def build_species_names_list_from_6_letter_codes():
    species_to_code_dict = {}
    code_to_species_dict = {}
    directory = config.regions_data_dir + "\\CA-ON-BN\\20_YEARS\\"

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        file_list = []
        with open(f) as file:
            for line in file:
                if line != "\n":
                    line = line.split("\t")
                    file_list.append(line)

        full_species_name = file_list[2][1]
        species_code = filename[9:-4]
        species_to_code_dict[full_species_name] = species_code
        code_to_species_dict[species_code] = full_species_name

    with open(config.res_dir + "species_to_code.json", 'w') as fp:
        json.dump(species_to_code_dict, fp)

    with open(config.res_dir + "code_to_species.json", 'w') as fp:
        json.dump(code_to_species_dict, fp)


def build_species_peaks():
    # Load the list of species we are working with
    with open(config.res_dir +"species_to_code.json") as json_file:
        species_to_code_dict = json.load(json_file)
    with open(config.res_dir + "code_to_species.json") as json_file:
        code_to_species_dict = json.load(json_file)

    # Load the list of eBird regions in Ontario
    with open(config.res_dir + "regions_complete.json") as json_file:
        regions_dict = json.load(json_file)

    # Create list of regions to be used as DataFrame columns
    region_list = []
    for region in regions_dict:
        region_list.append(region)
    region_list_dict = {"Region": region_list}

    species_list = []
    for species in species_to_code_dict:
        species_list.append(species)
    species_list_dict = {"Species": species_list}

    # Create a DataFrame to store all of the information
    df = pd.DataFrame(columns=region_list_dict, index=species_list_dict)
    df2 = pd.DataFrame(columns=species_list_dict, index=region_list_dict)

    # How to set a single value
    # df.loc["Acadian Flycatcher", "Algoma" ] = "AAAA"

    directory = config.regions_data_dir + "\\region_spring_peaks\\20_YEARS\\"
    for subdir, dirs, files in os.walk(directory):
        path = pathlib.PurePath(subdir)
        year = path.name
        if year == "20_YEARS":
            for file in files:
                cur_region_code = file[0:8]
                cur_region = list(regions_dict.keys())[list(regions_dict.values()).index(cur_region_code)]
                f = os.path.join(subdir, file)

                # Read each file line by line and store the species and date to the DF
                with open(f, 'r') as read_obj:
                    csv_reader = reader(read_obj)
                    header = next(csv_reader)
                    for row in csv_reader:
                        species, date = row[0], row[1]
                        if date == "2022-01-01":
                            date = None
                        # Add to the DataFrames
                        df.loc[species, cur_region] = date
                        df2.loc[cur_region, species] = date
    print(df)
    df.to_csv(
        config.species_data_dir + "20_YEARS_peak_dates_Region_index.csv")
    df2.to_csv(
        config.species_data_dir + "20_YEARS_peak_dates_Species_index.csv")


def make_all_species_peaks_per_region():
    data = pd.read_csv(config.species_data_dir + "20_YEARS_peak_dates_Region_index.csv")

    # Save species data separately
    for i in range(303):
        df = data.loc[i]
        print(data.loc[i][0])
        species_name = data.loc[i][0]
        if species_name != "Species":
            df.to_csv(config.species_data_dir +"20_YEARS_SPRING_PEAKS\\" + species_name + ".csv")


def make_html_table_for_each_region():
    directory = config.regions_data_dir + "region_spring_peaks\\20_YEARS\\"
    list_dir = config.regions_data_dir + "media\\lists\\20_YEARS\\"

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        print(filename)
        region = re.search("(CA-ON-..)",filename).group(1)
        data = pd.read_csv(f)

        # Sort by date
        data.sort_values("20_YEARS", inplace=True)
        # Modify date string to be in the proper format for the map
        data["20_YEARS"] = pd.to_datetime(data["20_YEARS"],
                                              format="%Y-%m-%d")
        data["20_YEARS"] = pd.to_datetime(data["20_YEARS"]).dt.strftime(
            '%b %d')

        # Remove species without data
        data = data[~data["20_YEARS"].isin(['Jan 01'])]

        # Adjust column names
        data.columns = ["Species", "Date"]
        data = data[["Date", "Species"]]
        # Save to html
        data.to_html(list_dir + region + ".html",index=False)

# build_species_names_list_from_6_letter_codes()
# build_species_peaks()
# make_all_species_peaks_per_region()
make_html_table_for_each_region()
