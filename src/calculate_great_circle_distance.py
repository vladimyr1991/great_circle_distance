from math import radians, sin, cos, acos
from itertools import combinations_with_replacement
import os
import random
import pandas as pd
import numpy as np
import argparse




parser = argparse.ArgumentParser(description='Program to calculate average circle distances between location set by latitude and longitude')
parser.add_argument('-n',
                    '--generate_n_locations',
                    help='Input integer value (n) to generate n random locations',
                    default=0,
                    required=False)

args = parser.parse_args()
n = int(args.generate_n_locations)

# it will help to execute script from different working directories
abs_path_to_script = os.path.dirname(os.path.abspath(__file__))


def calc_great_circle_distance(lat_1: float, lon_1: float, lat_2: float, lon_2: float):
    """
    formula for circle distance calculation ref: https://en.wikipedia.org/wiki/Great-circle_distance

    :param lat_1:
    :param lon_1:
    :param lat_2:
    :param lon_2:
    :return: circle_distance
    """

    # converting degree to radians
    lon_1, lat_1, lon_2, lat_2 = map(radians, [lon_1, lat_1, lon_2, lat_2])

    # earth radius in kilometers
    earth_radius = float(6371)

    # applying formula
    circle_distance = earth_radius * (acos(sin(lat_1) * sin(lat_2) + cos(lat_1) * cos(lat_2) * cos(abs(lon_1-lon_2))))

    return circle_distance


def extract_location_lat_lon(df, loc_name):
    """

    :param df:
    :param loc_name:
    :return: lat, lon
    """
    data_row = df.loc[df['Name'] == loc_name]

    lat = data_row["Latitude"].tolist()[0]
    lon = data_row["Longitude"].tolist()[0]

    return float(lat), float(lon)


def calc_closest_pair_to_avg(sorted_df, average_distance_value):
    lowest_distance = 999999999
    best_index = None
    for idx in range(len(sorted_df)):
        circle_distance = sorted_df.loc[idx, 'circle_distance']
        abs_delta = abs(average_distance_value - circle_distance)
        if abs_delta < lowest_distance:
            best_index = idx
            lowest_distance = abs_delta

    # extracting values from the closest pair
    loc_1 = sorted_df.loc[best_index, ['loc_1']].item()
    loc_2 = sorted_df.loc[best_index, ['loc_2']].item()
    closest_circle_distance = sorted_df.loc[best_index, ['circle_distance']].item()

    return loc_1, loc_2, closest_circle_distance


def generate_n_default_location(n_items=0):
    new_random_data = {
        "Name": [],
        "Latitude": [],
        "Longitude": []
        }

    for item_num in range(n_items):
        new_random_data["Name"].append(f"Location {item_num}")
        new_random_data["Latitude"].append(random.choice(np.arange(-90.0, 91.0, 0.01)))
        new_random_data["Longitude"].append(random.choice(np.arange(-180.0, 181.0, 0.01)))

    new_random_data_df = pd.DataFrame(new_random_data)
    # print(new_random_data_df)
    return new_random_data_df


def start_calculations():

    # checking of we need to generate data
    if n == 0:
        file_path = 'data/places.csv'
        data = pd.read_csv(os.path.join(abs_path_to_script, file_path))
    else:
        data = generate_n_default_location(n_items=n)

    # creating combinations of locations without repetitions
    # eliminating pairs of places having same pair
    names = data['Name'].tolist()
    locs_combs = [x for x in combinations_with_replacement(names, 2) if x[0] != x[1]]

    # we will use this dummy dict to create dataframe for calculations
    loc_pairs_dist = {
        "loc_1": [],
        "loc_2": [],
        "circle_distance": [],
        "unit": []
        }

    for i, loc_pair in enumerate(locs_combs):
        loc_1 = loc_pair[0]
        loc_2 = loc_pair[1]

        lat_1, lon_1 = extract_location_lat_lon(df=data, loc_name=loc_1)
        lat_2, lon_2 = extract_location_lat_lon(df=data, loc_name=loc_2)

        circle_distance = calc_great_circle_distance(lat_1=lat_1, lon_1=lon_1, lat_2=lat_2, lon_2=lon_2)
        circle_distance = round(circle_distance, 1)

        loc_pairs_dist["loc_1"].append(loc_1)
        loc_pairs_dist["loc_2"].append(loc_2)
        loc_pairs_dist["circle_distance"].append(circle_distance)
        loc_pairs_dist["unit"].append("km")

    # creating dataframe from dict and making necessary calculations
    loc_pairs_dist_df = pd.DataFrame(loc_pairs_dist).sort_values(by=['circle_distance'], ascending=True)
    avr_dist = round(loc_pairs_dist_df["circle_distance"].mean(), 1)
    loc_1, loc_2, closest_pair_to_average = calc_closest_pair_to_avg(sorted_df=loc_pairs_dist_df, average_distance_value=avr_dist)

    return loc_pairs_dist_df, avr_dist, loc_1, loc_2, closest_pair_to_average


if __name__ == '__main__':

    loc_pairs_dist_df, avr_dist, loc_1, loc_2, closest_pair_to_average = start_calculations()

    print(loc_pairs_dist_df.to_string(index=False, header=False))
    print(f"\nAverage distance: {avr_dist} km. Closest pair: {loc_1} - {loc_2} {closest_pair_to_average} km.")