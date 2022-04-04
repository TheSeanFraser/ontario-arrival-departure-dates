import pandas as pd

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
    spring_list = list(map(float, ([data[10][2], data[11][2], data[12][2], data[13][2],
                   data[14][2], data[15][2], data[16][2], data[17][2],
                   data[18][2], data[19][2], data[20][2], data[21][2],
                   data[22][2]])))
    spring_frequency = max(spring_list)
    spring_date_index = data[spring_list.index(spring_frequency) + 10][0]

    print(spring_frequency, spring_date_index)

    return spring_frequency


def calculate_winter_frequency(data):
    winter_list = list(map(float, ([data[2][2], data[3][2], data[4][2],
                                    data[5][2], data[6][2],data[7][2],
                                    data[8][2], data[9][2], data[46][2],
                                    data[47][2], data[48][2], data[49][2]])))
    print(winter_list)

    winter_frequency = sum(winter_list) / len(winter_list)
    print(winter_frequency)

    return winter_frequency


def calculate_spring_mass_arrival():
    data = pd.read_csv("Toronto Charts\\ALL_YEARS\\ALL_YEARS_barswa.txt", delimiter="\t",
                       header=None)
    # Dates start at column 2, frequency is row 2
    # Full species name at [1][2]
    print(data.to_string())
    print(data[1][2])

    spring_peak = calculate_peak_spring_arrival(data)
    winter_frequency = calculate_winter_frequency(data)
    mass_frequency = (0.2 * (spring_peak - winter_frequency)) - winter_frequency
    print("Mass arrival freq: " + str(mass_frequency))



calculate_spring_mass_arrival()
