import pandas as pd
from scipy.spatial import cKDTree

from core.api.utils.load_csv import pandas_load_update_csv

# Infor
"""
    this function filter stations based on a distance proximity within a 1 mile radius
"""


def filter_stations(route_coordinates):
    # load and read csv file
    df = pandas_load_update_csv()

    # get the latitudes and longitudes
    station_coords = df[['Latitude', 'Longitude']].dropna().to_numpy()
    route_coords = pd.DataFrame(route_coordinates, columns=['Longitude', 'Latitude']).to_numpy()

    # use cKDTree for efficient stations location within a 1 mile radius
    tree = cKDTree(station_coords)
    # index within 1 mile radius
    filtered_indices = tree.query_ball_point(route_coords, r=1)
    unique_indices = set([idx for sublist in filtered_indices for idx in sublist])
    return df.iloc[list(unique_indices)].copy()
