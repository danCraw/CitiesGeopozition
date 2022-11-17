from typing import List

from app.core.utils.geoposition import count_distance
from app.models.city import CityBase, CityOut
from app.models.coordinates import Coordinates


def get_more_close_cities(central_city: CityBase, cities: List[CityBase], amount_close_cities) -> List[CityOut | None]:
    close_cities = []
    min_distance = float('inf')
    more_close_city = None
    for count in range(amount_close_cities):
        for city in cities:
            if city.id != central_city.id:
                if city not in close_cities:
                    distance = count_distance(Coordinates(city.latitude, city.longitude),
                                              Coordinates(central_city.latitude, central_city.longitude))
                    if distance < min_distance:
                        min_distance = distance
                        more_close_city = city
        close_cities.append(more_close_city)
        min_distance = float('inf')
    return close_cities
