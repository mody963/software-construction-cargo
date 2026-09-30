import pytest
import requests


@pytest.fixture
def _data() -> dict[str, str]:
    return {
        'host': 'localhost:3000',
        'api_path': '/api/v1/',
        'api_key': 'f4a5c6i7l8i9t0y1m2a3n4a5g6',  # facility_management key
    }

# GET

def test_get_locations_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations"

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_location_by_id_200(_data: dict[str, str]) -> None:
    list_url: str = f"http://{_data['host']}{_data['api_path']}locations"
    locations = requests.get(list_url, headers={'API_KEY': _data['api_key']}).json()
    target_id = locations[0]["id"]

    url: str = f"http://{_data['host']}{_data['api_path']}locations/{target_id}"
    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    assert response.status_code == 200
    assert response.json()["id"] == target_id


def test_get_locations_wrong_api_key_401(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations"

    response = requests.get(url, headers={'API_KEY': 'verkeerde_sleutel_123'})

    assert response.status_code == 401


def test_get_location_not_found_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations/999999"

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # BUG IN BACKEND: Verwachting is 404 Not Found. Backend crasht of geeft 200 met null.
    assert response.status_code == 404

# POST

def test_post_location_201(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations"

    payload = {
        "id": 8881,
        "warehouse_id": 2,
        "code": "LOC-TEST-AUTO",
        "name": "Automated Location Test",
        "created_at": "2026-09-25T12:00:00Z",
        "updated_at": "2026-09-25T12:00:00Z"
    }

    response = requests.post(url, headers={'API_KEY': _data['api_key'], 'Content-Type': 'application/json'}, json=payload)

    assert response.status_code == 201


def test_post_location_incomplete_400(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations"

    payload = {"name": "Missing ID and Code"}

    response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=payload)
    
    # BUG IN BACKEND: Verwachting 400 Bad Request.
    assert response.status_code == 400


def test_post_location_incorrect_types_400(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations"

    payload = {
        "id": "geen-int",
        "warehouse_id": "ook-geen-int",
        "code": 100,
        "name": "Invalid Location Types"
    }

    response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=payload)
    
    # BUG IN BACKEND: Verwachting 400 Bad Request.
    assert response.status_code == 400


def test_post_location_empty_400(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations"

    response = requests.post(url, headers={'API_KEY': _data['api_key']}, json={})
    
    # BUG IN BACKEND: Verwachting 400 Bad Request.
    assert response.status_code == 400

# PUT

def test_put_location_200(_data: dict[str, str]) -> None:
    list_url: str = f"http://{_data['host']}{_data['api_path']}locations"
    locations = requests.get(list_url, headers={'API_KEY': _data['api_key']}).json()
    target_loc = locations[0]
    target_id = target_loc["id"]

    url: str = f"http://{_data['host']}{_data['api_path']}locations/{target_id}"
    target_loc["name"] = "Updated Location Name Pytest"

    response = requests.put(url, headers={'API_KEY': _data['api_key'], 'Content-Type': 'application/json'}, json=target_loc)

    assert response.status_code == 200


def test_put_location_not_found_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations/999999"

    update_payload = {"name": "Ghost Location"}
    response = requests.put(url, headers={'API_KEY': _data['api_key']}, json=update_payload)
    
    # BUG IN BACKEND: Verwachting 404 Not Found.
    assert response.status_code == 404


def test_put_location_wrong_key_401(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations/1"
    
    update_payload = {"name": "Hacked Location"}
    response = requests.put(url, headers={'API_KEY': 'foute-key-123'}, json=update_payload)
    
    assert response.status_code == 401


# DELETE

def test_delete_location_200(_data: dict[str, str]) -> None:
    # Verwijder testlocatie
    url: str = f"http://{_data['host']}{_data['api_path']}locations/8881"

    response = requests.delete(url, headers={'API_KEY': _data['api_key']})

    # BUG IN BACKEND: Kan crashen met 500 als het record al weg is of de pool stuk is.
    assert response.status_code == 200


def test_delete_locations_collection_not_allowed_405(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations"

    response = requests.delete(url, headers={'API_KEY': _data['api_key']})

    # BUG IN BACKEND: Verwachting 405 Method Not Allowed. Backend geeft 500 wegens IndexError op paths[1].
    assert response.status_code == 405