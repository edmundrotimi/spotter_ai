# flake8: noqa
import requests

from core.project.settings import OPENROUTESERVICE_API_KEY  # type: ignore

# Infor
"""
    this function fetch the route using openrouteservice map API
"""


def get_route(start, finish):
    url = 'https://api.openrouteservice.org/v2/directions/driving-car'
    payload = {
        "api_key": OPENROUTESERVICE_API_KEY,
        "start": f"{start[1]},{start[0]}",
        "end": f"{finish[1]},{finish[0]}"
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.get(url, params=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Failed to fetch route')
