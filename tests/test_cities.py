import pytest
import requests

from app.models.city import CityIn


@pytest.fixture()
def city_data() -> CityIn:
    city = CityIn(id='11111111-1111-1111-1111-111111111111', name='Moscow')
    city.init_coordinates()
    return city


pytestmark = pytest.mark.asyncio
base_url = 'http://0.0.0.0:8001/api/v1/cities'


async def test_create_without_id(city_data: CityIn):
    city = {
        'name': city_data.name
    }
    response = requests.post(base_url + '/', json=city)
    assert response.status_code == 200
    json = response.json()
    assert json['name'] == city_data.name and json['latitude'] == city_data.latitude and json[
        'longitude'] == city_data.longitude


async def test_create_with_id(city_data: CityIn):
    city = {
        'id': str(city_data.id),
        'name': city_data.name
    }
    response = requests.post(base_url + '/', json=city)
    assert response.status_code == 200
    json = response.json()
    assert json['name'] == city_data.name and json['latitude'] == city_data.latitude and json[
        'longitude'] == city_data.longitude


async def test_read(city_data: CityIn):
    response = requests.get(base_url + '/%7Bid%7D?', params={'city_id': str(city_data.id)}, )
    assert response.status_code == 200
    assert response.json() == {
        'id': str(city_data.id),
        'name': city_data.name,
        'latitude': city_data.latitude,
        'longitude': city_data.longitude
    }


async def test_read_wrong_id():
    response = requests.get(base_url + '/%7Bid%7D?', params={'city_id': '21111111-1111-1111-1111-111111111111'}, )
    assert response.status_code == 404


async def test_update(city_data: CityIn):
    city = {
        'id': str(city_data.id),
        'name': city_data.name,
        'longitude': '123123123.2121',
        'latitude': city_data.latitude
    }
    response = requests.put(base_url + '/', json=city)
    json = response.json()
    assert response.status_code == 200
    assert json['id'] == city['id'], json['name'] == city['name'] and json['latitude'] == city['latitude'] and json[
        'longitude'] == city['longitude']


async def test_update_wrong_id(city_data: CityIn):
    city = {
        'id': '21111111-1111-1111-1111-111111111111',
        'name': city_data.name,
        'longitude': '123123123.2121',
        'latitude': city_data.latitude
    }
    response = requests.put(base_url + '/', json=city)
    assert response.status_code == 404


async def test_delete(city_data: CityIn):
    get_response = requests.get(base_url + '/%7Bid%7D?', params={'city_id': str(city_data.id)})
    response = requests.delete(base_url + '/%7Bid%7D?', params={'city_id': str(city_data.id)})
    assert response.status_code == 200
    assert response.json() == get_response.json()
    get_response = requests.get(base_url + '/%7Bid%7D?', params={'city_id': str(city_data.id)})
    assert get_response.status_code == 404


async def test_delete_wrong_id(city_data: CityIn):
    response = requests.delete(base_url + '/%7Bid%7D?', params={'city_id': str(city_data.id)})
    assert response.status_code == 404
