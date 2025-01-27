import numpy as np
from scipy.spatial import cKDTree

from core.api.utils.station_filter import filter_stations


def find_optimal_stations_ml(route_coordinates, model):
    optimal_stations = []
    total_cost = 0
    max_range = 500
    miles_per_gallon = 10

    try:
        # filter stations near the truck route
        nearby_stations = filter_stations(route_coordinates)
        # add state_avg_price and distance_to_next_stop for nearby stations
        nearby_stations['state_avg_price'] = nearby_stations.groupby('State')['Retail Price'].transform('mean')
        nearby_stations['distance_to_next_stop'] = nearby_stations['Retail Price'].diff().fillna(
            nearby_stations['Retail Price'].median()
        ).abs()

        # Prepare route and station coordinates
        route_coords = np.array(route_coordinates)[:, ::-1]  # Convert (lng, lat) -> (lat, lng)
        station_coords = np.array(list(zip(nearby_stations['Latitude'], nearby_stations['Longitude'])))

        # build a KDTree for stations for performance
        station_tree = cKDTree(station_coords)

        # find closest stations for all route points
        distances, indices = station_tree.query(route_coords)

        # get closest stations
        closest_stations = nearby_stations.iloc[indices]

        # features for ML model
        features = np.column_stack([
            closest_stations['Retail Price'], closest_stations['state_avg_price'],
            closest_stations['distance_to_next_stop']
        ])

        # prredict the optimal stations
        predictions = model.predict(features)

        # get valid stations based on predictions
        valid_indices = np.where(predictions == 1)[0]
        valid_stations = closest_stations.iloc[valid_indices]
        valid_route_points = np.array(route_coordinates)[valid_indices]

        # get the fisrt optimal station, total total cost and optimal stations
        for station in valid_stations.itertuples():
            station_dict = station._asdict()
            optimal_stations.append(station_dict)
            total_cost += (max_range / miles_per_gallon) * station_dict['_7']

        return optimal_stations, total_cost, valid_route_points.tolist()

    except Exception as e:
        print(f'Error: {e}')
