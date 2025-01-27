# Infor
"""
     this function generates maps link for the located route
"""


def generate_map_link(route_coordinates):
    coords = '/'.join([f'{point[1]},{point[0]}' for point in route_coordinates])
    return f'https://www.google.com/maps/dir/{coords}/'
