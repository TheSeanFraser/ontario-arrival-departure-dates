import geopandas as gpd
import matplotlib
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable

import config
import matplotlib.pyplot as plt
import os
import re

print("Loading Ontario shape...")
ontario_shape = gpd.read_file(config.res_dir + "ontario_2011.json")
print("Ontario shape loaded!")


def make_maps():
    global ontario_shape
    directory = config.species_data_dir + "20_YEARS_SPRING_PEAKS\\"

    # Loop through all of the species to build a dataframe
    for filename in os.listdir(directory):
        single_data = pd.read_csv(directory + filename, header=1)
        species = re.search("(.*).csv", filename).group(1)
        print("Making map for: " + species)
        # Modify date string to be in the proper format for the map
        single_data[species] = pd.to_datetime(single_data[species], format="%Y-%m-%d")
        single_data[species] = pd.to_datetime(single_data[species]).dt.strftime('%b %d')

        # Merges the dataframes with the matching region names column
        merged = ontario_shape.set_index("CDNAME").join(
            single_data.set_index("Unnamed: 0"))

        # Define the map plot
        fig, ax = plt.subplots(1, figsize=(12, 8))
        ax.axis('off')
        ax.set_title(species + ' Spring Mass Arrival Dates in Ontario',
                     fontdict={'fontsize': '20', 'fontweight': '3'})

        # "Missing values" will not plot anything if there are no missing values
        # so there needs to be a check
        if merged[str(species)].isnull().values.any():
            merged.plot(column=str(species),
                        cmap=matplotlib.cm.get_cmap('viridis_r'),
                        linewidth=0.9,
                        ax=ax,
                        edgecolor='1',
                        legend=True, legend_kwds={'loc': 'center right',
                                                  'bbox_to_anchor': (1.5, 0.5),
                                                  'ncol': 2,
                                                  'fontsize': 'large'},
                        missing_kwds={
                    "color": "lightgrey",
                    "label": "No data", }, )
        else:
            merged.plot(column=str(species),
                        cmap=matplotlib.cm.get_cmap('viridis_r'),
                        linewidth=0.9,
                        ax=ax,
                        edgecolor='1',
                        legend=True, legend_kwds={'loc': 'center right',
                                                  'bbox_to_anchor': (1.5, 0.5),
                                                  'ncol': 2,
                                                  'fontsize': 'large'})

        plt.subplots_adjust(left=-0.1)
        # plt.tight_layout()
        fig.savefig(config.proj_path + "maps\\spring\\" + species + ".png", dpi=100)
        plt.close()


def load_ontario_shape():
    print("Loading Ontario shape")
    ontario_shape = gpd.read_file(config.res_dir + "ontario_2011.json")

    return ontario_shape


def make_map_multi(species_data_file):
    directory = config.species_data_dir + "20_YEARS_SPRING_PEAKS\\"
    single_data = pd.read_csv(directory + str(species_data_file), header=0)
    number = re.search("_(\d*)", species_data_file).group(1)
    species = re.search("(.*)_", species_data_file).group(1)

    # Merges the dataframes with the matching region names column
    merged = ontario_shape.set_index("CDNAME").join(
        single_data.set_index("Unnamed: 0"))

    # Define the map plot
    fig, ax = plt.subplots(1, figsize=(20, 20))
    ax.axis('off')
    ax.set_title(species + ' Spring Mass Arrival Dates Through Ontario',
                 fontdict={'fontsize': '25', 'fontweight': '3'})

    # "Missing values" will not plot anything if there are no missing values
    # so there needs to be a check
    if merged[str(number)].isnull().values.any():
        # merged[str(number)] = merged[str(number)].astype(str)
        merged.plot(column=str(number),
                    cmap='Greens',
                    linewidth=0.9,
                    ax=ax,
                    edgecolor='1',
                    legend=True, missing_kwds={
                "color": "lightgrey",
                "label": "Missing values", }, )
    else:
        merged.plot(column=str(number),
                    cmap='Greens',
                    linewidth=0.9,
                    ax=ax,
                    edgecolor='1',
                    legend=True, )
    fig.savefig(
        config.proj_path + "maps\\spring\\" + species + " spring map.png",
        dpi=100)
    plt.close()


make_maps()
