from geopy.distance import geodesic
from geopy.geocoders import Nominatim

from app.models.coordinates import Coordinates

geolocator = Nominatim(user_agent="myapplication")


def get_coordinates(city_name: str) -> Coordinates:
    location = geolocator.geocode(city_name)
    return Coordinates(location.latitude, location.longitude)


def count_distance(point1: Coordinates, point2: Coordinates):
    return geodesic((point1.longitude, point1.latitude), (point2.longitude, point2.latitude)).km
