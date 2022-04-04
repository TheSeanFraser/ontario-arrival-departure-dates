import pandas as pd

# M = 0.2 X (P - W) + W
#
# Where:
# M = mass arrival date
# P = peak arrival date
# W = winter frequency

M_factor = 0.2

data = pd.read_csv("Toronto Charts\\ALL_YEARS_barswa.txt", delimiter="\t", header=None)
print(data.to_string())

print(data[2][12])

def calculate_peak_spring_arrival():


def calculate_winter_frequency():


def calculate_spring_mass_arrival():