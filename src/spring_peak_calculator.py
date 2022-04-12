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

all_data = {
    "Year": []
}


# Find the maximum frequency during spring
def calculate_peak_spring_arrival(data):
    # "Spring" starts March 1 and ends week of June 1
    # Create a list of the frequency values during the spring weeks
    spring_list = list(map(float, ([data[10][2], data[11][2], data[12][2],
                                    data[13][2], data[14][2], data[15][2],
                                    data[16][2], data[17][2], data[18][2],
                                    data[19][2], data[20][2], data[21][2],
                                    data[22][2]])))
    peak_spring_frequency = max(spring_list)
    # +8 to make up for the rest of the year not in this list
    peak_spring_date_index = spring_list.index(peak_spring_frequency) + 8

    return peak_spring_frequency, peak_spring_date_index


# Calculate the winter frequency of the species
def calculate_winter_frequency(data):
    # Create a list of the frequency values during the winter weeks
    winter_list = list(map(float, ([data[2][2], data[3][2], data[4][2],
                                    data[5][2], data[6][2], data[7][2],
                                    data[8][2], data[9][2]])))

    # Average the frequencies recorded through winter
    winter_avg = sum(winter_list) / len(winter_list)
    # Max value of winter frequency needed
    winter_max = max(winter_list)
    winter_freq = (winter_max + winter_avg) / 2

    return winter_freq


# Calculate the date of the mass spring arrivals
def calculate_spring_mass_arrival():
    directory = config.proj_path + "data\\toronto\\"

    for subdir, dirs, files in os.walk(directory):
        path = pathlib.PurePath(subdir)
        year = path.name
        if len(year) == 4:
            print(year)
            all_data["Year"] = all_data["Year"] + [year]
            for file in files:
                f = os.path.join(subdir, file)
                data = pd.read_csv(f, delimiter="\t", header=None)
                # Dates start at column 2, frequency is row 2
                # Full species name at [1][2]

                spring_peak_freq, peak_spring_date_index = calculate_peak_spring_arrival(
                    data)
                winter_freq = calculate_winter_frequency(data)
                mass_freq = (M_factor * (
                            spring_peak_freq - winter_freq)) + winter_freq

                # Create a list to store all frequency numbers in each day of year
                calendar_list = pd.Series([np.nan] * 365)

                # Find the day of the year with the peak spring frequency week
                peak_day = int(
                    week_day_of_year_list[int(peak_spring_date_index)])

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


    # for file in os.listdir(directory):
    #     f = os.path.join(directory, file)
    #     data = pd.read_csv(f, delimiter="\t", header=None)
    #     # Dates start at column 2, frequency is row 2
    #     # Full species name at [1][2]
    #
    #     spring_peak_freq, peak_spring_date_index = calculate_peak_spring_arrival(
    #         data)
    #     winter_freq = calculate_winter_frequency(data)
    #     mass_freq = (M_factor * (spring_peak_freq - winter_freq)) + winter_freq
    #
    #     # Create a list to store all frequency numbers in each day of year
    #     calendar_list = pd.Series([np.nan] * 365)
    #
    #     # Find the day of the year with the peak spring frequency week
    #     peak_day = int(week_day_of_year_list[int(peak_spring_date_index)])
    #
    #     # Enter the frequency data into the calendar list
    #     for x in range(len(week_day_of_year_list)):
    #         calendar_list[week_day_of_year_list[x]] = float(data[x + 2][2])
    #
    #     # Interpolate the frequency data for each day of year, not just week
    #     # start day. This calculates all the "in-between" frequencies needed
    #     # to find the exact day with the matching frequency
    #     calendar_list = calendar_list.interpolate()
    #
    #     # Find the mass arrival day based on peak day. Starts at the peak and
    #     # goes backwards until it finds a matching frequency
    #     mass_arrival_day = 1
    #     for i in range(peak_day, 0, -1):
    #         # If the mass frequency is greater than the frequency on the
    #         # selected day, that means we have the right day because all others
    #         # have been higher than the mass frequency.
    #         if calendar_list[i] - mass_freq < 0:
    #             mass_arrival_day = i
    #             break
    #
    #     # Convert the day to a string, then create a datetime object for the
    #     # date for easier conversion.
    #     mass_arrival_date = str(mass_arrival_day)
    #     mass_arrival_date.rjust(3 + len(mass_arrival_date), '0')
    #     year = "2022"
    #     date = datetime.strptime(year + "-" + mass_arrival_date,
    #                              "%Y-%j").strftime("%m-%d")
    #     date_string = str(date)
    #
    #     output_file = open(config.proj_path +
    #                        "data\ontario\\20_YEARS\species_arrivals.txt", "a")
    #     output_file.write(data[1][2] + ", " + date_string + "\n")
    #     output_file.close()

    # print(all_data)
    pd.DataFrame.from_dict(data=all_data, orient='index').to_csv("toronto_all_data.csv", header=False)


calculate_spring_mass_arrival()
