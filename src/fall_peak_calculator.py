import json
import os
import pathlib
from datetime import datetime
import pandas as pd
import numpy as np
import config

M_factor = 0.2

# Store a list of weeks presented as day number of year
week_day_of_year_list = [0, 7, 14, 21, 31, 38, 45, 52, 59, 66, 73, 80, 90,
                         97, 104, 111, 120, 127, 134, 141, 151, 158, 165,
                         172, 181, 188, 195, 202, 213, 219, 226, 233, 243,
                         250, 257, 264, 273, 280, 287, 294, 304, 311, 318,
                         325, 334, 341, 348, 356]


# Find the maximum frequency during fall
def calculate_peak_fall_arrival(data):
    # "Fall" starts August 15 and ends November 15
    # Create a list of the frequency values during the fall weeks
    fall_list = list(map(float, ([data[32][2], data[33][2], data[34][2],
                                    data[35][2], data[36][2], data[37][2],
                                    data[38][2], data[39][2], data[40][2],
                                    data[41][2], data[42][2], data[43][2],
                                    data[44][2]])))
    peak_fall_frequency = max(fall_list)

    # + 30 to make up for the rest of the year not in this list
    # First two columns are useless, column index should start at 2
    # Then add 30 to include the previous weeks of the year in the overall index
    peak_fall_date_index = fall_list.index(peak_fall_frequency) + 30

    return peak_fall_frequency, peak_fall_date_index


# Calculate the summer frequency of the species
def calculate_summer_frequency(data):
    # Create a list of the frequency values during the summer weeks
    summer_list = list(map(float, ([data[23][2], data[24][2], data[25][2],
                                    data[26][2], data[27][2], data[28][2],
                                    data[29][2], data[30][2], data[31][2]])))

    # Average the frequencies recorded through winter
    summer_avg = sum(summer_list) / len(summer_list)
    # Max value of winter frequency needed
    summer_max = max(summer_list)
    summer_freq = (summer_max + summer_avg) / 2

    return summer_freq


# Calculate the date of the mass fall arrivals
def calculate_fall_mass_arrival():
    directory = config.proj_path + "data\ontario\\20_YEARS"
    for file in os.listdir(directory):
        f = os.path.join(directory, file)
        data = pd.read_csv(f, delimiter="\t", header=None)
        # Dates start at column 2, frequency is row 2
        # Full species name at [1][2]

        fall_peak_freq, peak_fall_date_index = calculate_peak_fall_arrival(data)
        summer_freq = calculate_summer_frequency(data)
        mass_freq = (M_factor * (fall_peak_freq - summer_freq)) + summer_freq

        # Create a list to store all frequency numbers in each day of year
        calendar_list = pd.Series([np.nan] * 365)

        # Find the day of the year with the peak fall frequency week
        peak_day = int(week_day_of_year_list[int(peak_fall_date_index)])

        # Enter the frequency data into the calendar list
        for x in range(len(week_day_of_year_list)):
            calendar_list[week_day_of_year_list[x]] = float(data[x + 2][2])

        # Interpolate the frequency data for each day of year, not just week
        # start day. This calculates all the "in-between" frequencies needed
        # to find the exact day with the matching frequency
        calendar_list = calendar_list.interpolate()

        # Find the mass arrival day based on peak day. Starts at the peak and
        # goes backwards until it finds a matching frequency
        mass_arrival_day = 1
        for i in range(peak_day, 0, -1):
            # If the mass frequency is greater than the frequency on the
            # selected day, that means we have the right day because all others
            # have been higher than the mass frequency.
            if calendar_list[i] - mass_freq < 0:
                mass_arrival_day = i
                break

        # Convert the day to a string, then create a datetime object for the
        # date for easier conversion.
        mass_arrival_date = str(mass_arrival_day)
        mass_arrival_date.rjust(3 + len(mass_arrival_date), '0')
        year = "2022"
        date = datetime.strptime(year + "-" + mass_arrival_date,
                                 "%Y-%j").strftime("%m-%d")
        date_string = str(date)

        output_file = open(config.proj_path +
                           "data\ontario\\20_YEARS\species_departures.txt", "a")
        output_file.write(data[1][2] + ", " + date_string + "\n")
        output_file.close()


# Calculate the date of the mass fall arrivals
def bulk_20_years_calculate_fall_mass_arrival():
    # Load the list of eBird regions in Ontario
    with open(config.res_dir + "regions_complete.json") as json_file:
        regions_dict = json.load(json_file)

    for region in regions_dict:
        all_data = {
            "Year": []
        }
        print("Starting " + region)
        directory = config.regions_data_dir + regions_dict[region] \
                    + "\\20_YEARS\\"

        year = "TWENTY"
        for subdir, dirs, files in os.walk(directory):
            path = pathlib.PurePath(subdir)
            year = path.name
            if year == "20_YEARS":
                print(year)
                all_data["Year"] = all_data["Year"] + [year]
                for file in files:
                    f = os.path.join(subdir, file)
                    data = pd.read_csv(f, delimiter="\t", header=None)
                    # Dates start at column 2, frequency is row 2
                    # Full species name at [1][2]

                    fall_peak_freq, peak_fall_date_index = calculate_peak_fall_arrival(data)
                    summer_freq = calculate_summer_frequency(data)
                    mass_freq = (M_factor * (
                                fall_peak_freq - summer_freq)) + summer_freq

                    # Create a list to store all frequency numbers in each day of year
                    calendar_list = pd.Series([np.nan] * 365)

                    # Find the day of the year with the peak fall frequency week
                    peak_day = int(
                        week_day_of_year_list[int(peak_fall_date_index)])

                    # Enter the frequency data into the calendar list
                    for x in range(len(week_day_of_year_list)):
                        calendar_list[week_day_of_year_list[x]] = float(
                            data[x + 2][2])

                    # Interpolate the frequency data for each day of year, not just week
                    # start day. This calculates all the "in-between" frequencies needed
                    # to find the exact day with the matching frequency
                    calendar_list = calendar_list.interpolate()

                    # Find the mass arrival day based on peak day. Starts at the peak and
                    # goes backwards until it finds a matching frequency
                    mass_arrival_day = 1
                    for i in range(peak_day, 0, -1):
                        # If the mass frequency is greater than the frequency on the
                        # selected day, that means we have the right day because all others
                        # have been higher than the mass frequency.
                        if calendar_list[i] - mass_freq < 0:
                            mass_arrival_day = i
                            break

                    # Convert the day to a string, then create a datetime object for the
                    # date for easier conversion.
                    mass_arrival_date = str(mass_arrival_day)
                    mass_arrival_date.rjust(3 + len(mass_arrival_date), '0')
                    year = "2022"
                    date = datetime.strptime(year + "-" + mass_arrival_date,
                                             "%Y-%j").strftime("%Y-%m-%d")
                    date_string = str(date)

                    if str(data[1][2]) in all_data.keys():
                        all_data[str(data[1][2])] = all_data[str(data[1][2])] + [date_string]
                    else:
                        all_data[str(data[1][2])] = [date_string]

        fall_peaks_path = config.regions_data_dir + "\\region_fall_peaks\\20_YEARS\\" + regions_dict[region] + "_fall_peaks.csv"
        pd.DataFrame.from_dict(data=all_data, orient='index').to_csv(fall_peaks_path, header=False)
        print(region + " complete")


# calculate_fall_mass_arrival()
bulk_20_years_calculate_fall_mass_arrival()
