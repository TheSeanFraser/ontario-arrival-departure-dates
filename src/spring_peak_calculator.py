import os
from datetime import datetime
import pandas as pd
import numpy as np

# M = 0.2 X (P - W) + W
#
# Where:
# M = mass arrival frequency
# P = peak arrival frequency
# W = winter frequency
# Date is extrapolated by M

M_factor = 0.2


def calculate_peak_spring_arrival(data):
    # "Spring" starts March 1 and ends week of June 1
    spring_list = list(map(float, ([data[10][2], data[11][2], data[12][2],
                                    data[13][2], data[14][2], data[15][2],
                                    data[16][2], data[17][2], data[18][2],
                                    data[19][2], data[20][2], data[21][2],
                                    data[22][2]])))
    spring_frequency = max(spring_list)
    # +8 to make up for the rest of the year not in this list
    spring_date_index = spring_list.index(spring_frequency) + 8

    return spring_frequency, spring_date_index


def calculate_winter_frequency(data):
    winter_list = list(map(float, ([data[2][2], data[3][2], data[4][2],
                                    data[5][2], data[6][2], data[7][2],
                                    data[8][2], data[9][2]])))

    # Average the frequencies recorded through winter
    winter_avg = sum(winter_list) / len(winter_list)
    # Max value of winter frequency needed
    winter_max = max(winter_list)
    winter_frequency = (winter_max + winter_avg) / 2

    return winter_frequency


def calculate_spring_mass_arrival():

    directory = "ontario\\20_YEARS\\"
    for file in os.listdir(directory):
        f = os.path.join(directory, file)
        data = pd.read_csv(f, delimiter="\t", header=None)
        # Dates start at column 2, frequency is row 2
        # Full species name at [1][2]

        spring_peak, spring_peak_index = calculate_peak_spring_arrival(data)
        winter_frequency = calculate_winter_frequency(data)
        mass_frequency = (0.2 * (spring_peak - winter_frequency)) + winter_frequency

        # Create a list to store all frequency numbers in each day of year
        calendar_list = pd.Series([np.nan] * 365)
        # Store a list of weeks presented as day number of year
        week_day_of_year_list = [0, 7, 14, 21, 31, 38, 45, 52, 59, 66, 73, 80, 90,
                                 97, 104, 111, 120, 127, 134, 141, 151, 158, 165,
                                 172, 181, 188, 195, 202, 213, 219, 226, 233, 243,
                                 250, 257, 264, 273, 280, 287, 294, 304, 311, 318,
                                 325, 334, 341, 348, 356]

        print(spring_peak_index)
        peak_day = int(week_day_of_year_list[int(spring_peak_index)])

        # Enter the frequency data into the calendar list
        for x in range(len(week_day_of_year_list)):
            calendar_list[week_day_of_year_list[x]] = float(data[x + 2][2])

        # Interpolate the frequency data for each day of year,
        # not just week start
        calendar_list = calendar_list.interpolate()

        # Find the mass arrival day based on peak day
        mass_arrival_day = 1
        for i in range(peak_day, 0, -1):
            print(peak_day, i, calendar_list[i], mass_frequency)
            if calendar_list[i] - mass_frequency < 0:
                print(calendar_list.to_string())
                mass_arrival_day = i
                break




        # Find the closest match of mass arrival frequency in calendar day list
        # mass_arrival_day = (np.abs(calendar_list - mass_frequency)).argmin()

        mass_arrival_date = str(mass_arrival_day)
        mass_arrival_date.rjust(3 + len(mass_arrival_date), '0')
        year = "2022"
        date = datetime.strptime(year + "-" + mass_arrival_date, "%Y-%j").strftime("%m-%d")

        date_string = str(date)
        # print(date_string)
        print(data[1][2], winter_frequency, spring_peak, mass_arrival_day)
        output_file = open("../data/ontario/20_YEARS/species_arrivals.txt", "a")
        output_file.write(data[1][2] + ", " + date_string + "\n")
        # output_file.write(data[1][2] + ", " + mass_arrival_date + "\n")
        output_file.close()



calculate_spring_mass_arrival()
