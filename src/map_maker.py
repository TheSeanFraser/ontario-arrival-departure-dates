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


def make_spring_maps():
    global ontario_shape
    directory = config.species_data_dir + "20_YEARS_SPRING_PEAKS\\"

    # Loop through all of the species to build a dataframe
    for filename in os.listdir(directory):
        single_data = pd.read_csv(directory + filename, header=1)
        species = re.search("(.*).csv", filename).group(1)
        print("Making map for: " + species)

        # Merges the dataframes with the matching region names column
        merged = ontario_shape.set_index("CDNAME").join(
            single_data.set_index("Unnamed: 0"))

        # Sort the date and change to easy format
        merged.sort_values(species, inplace=True)
        merged[species] = pd.to_datetime(merged[species], format="%Y-%m-%d")
        merged[species] = pd.to_datetime(merged[species]).dt.strftime('%#m-%d')


        # Define the map plot
        fig, ax = plt.subplots(1, figsize=(12, 8))
        ax.axis('off')
        ax.set_title(species + ' Spring Mass Arrival Dates in Ontario',
                     fontdict={'fontsize': '20', 'fontweight': '3'})

        # Add a watermark
        ax.text(0, 0, "Sean Fraser - 2022", transform=ax.transAxes,
            fontsize=10, color='gray', alpha=0.5,
            ha='left', va='bottom')

        # "Missing values" will not plot anything if there are no missing values
        # so there needs to be a check
        if merged[str(species)].isnull().values.any():
            merged.plot(column=species,
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
        fig.savefig(config.proj_path + "media\\maps\\spring\\" + species + ".png", dpi=100)
        plt.close()


def make_fall_maps():
    global ontario_shape
    directory = config.species_data_dir + "20_YEARS_FALL_PEAKS\\"

    # Loop through all of the species to build a dataframe
    for filename in os.listdir(directory):
        single_data = pd.read_csv(directory + filename, header=1)
        species = re.search("(.*).csv", filename).group(1)
        print("Making map for: " + species)

        # Merges the dataframes with the matching region names column
        merged = ontario_shape.set_index("CDNAME").join(
            single_data.set_index("Unnamed: 0"))

        # Sort the date and change to easy format
        merged.sort_values(species, inplace=True)
        merged[species] = pd.to_datetime(merged[species], format="%Y-%m-%d")
        merged[species] = pd.to_datetime(merged[species]).dt.strftime('%m-%d')


        # Define the map plot
        fig, ax = plt.subplots(1, figsize=(12, 8))
        ax.axis('off')
        ax.set_title(species + ' Fall Mass Arrival Dates in Ontario',
                     fontdict={'fontsize': '20', 'fontweight': '3'})

        # Add a watermark
        ax.text(0, 0, "Sean Fraser - 2022", transform=ax.transAxes,
            fontsize=10, color='gray', alpha=0.5,
            ha='left', va='bottom')

        # "Missing values" will not plot anything if there are no missing values
        # so there needs to be a check
        if merged[str(species)].isnull().values.any():
            merged.plot(column=species,
                        cmap=matplotlib.cm.get_cmap('inferno_r'),
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
                        cmap=matplotlib.cm.get_cmap('inferno_r'),
                        linewidth=0.9,
                        ax=ax,
                        edgecolor='1',
                        legend=True, legend_kwds={'loc': 'center right',
                                                  'bbox_to_anchor': (1.5, 0.5),
                                                  'ncol': 2,
                                                  'fontsize': 'large'})

        plt.subplots_adjust(left=-0.1)
        # plt.tight_layout()
        fig.savefig(config.proj_path + "media\\maps\\fall\\" + species + ".png", dpi=100)
        plt.close()


def load_ontario_shape():
    print("Loading Ontario shape")
    ontario_shape = gpd.read_file(config.res_dir + "ontario_2011.json")

    return ontario_shape


# make_spring_maps()
make_fall_maps()
