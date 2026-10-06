import pytest
import requests
from typing import Any

@pytest.fixture
def _data() -> dict[str, str]:
    return {
        'host': 'localhost:3000',
        'api_path': '/api/v1/',
        'api_key': 'f4a5c6i7l8i9t0y1m2a3n4a5g6',  # facility_management key
    }

NO_ACCESS_API_KEY = 'r2e4c6e8i0v3i5n7g9s'

# GET

def test_get_locations_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations"
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_locations_wrong_api_key_401(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations"
    response = requests.get(url, headers={'API_KEY': 'ongeldige_key_123'})
    assert response.status_code == 401


def test_get_location_invalid_id_integer_not_found_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations/999999"
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 404


def test_get_location_invalid_id_string_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations/abcdef"
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    # Crasht op ValueError in int() momenteel
    assert response.status_code == 404


def test_get_location_invalid_id_string_integer_non_alphanumeric_not_found_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations/ABC6d1Xyz$"
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 404


def test_get_location_by_id_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations/1"
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 200
    assert response.json()["id"] == 1


# POST

def test_post_location_201(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations"
    json_body: dict[str, Any] = {
        "id": 888001,
        "warehouse_id": 1,
        "code": "LOC-TEST-001",
        "name": "Automated Location Test",
        "created_at": "2026-09-25T12:00:00Z",
        "updated_at": "2026-09-25T12:00:00Z"
    }
    response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert response.status_code == 201


def test_post_and_get_location_201(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations"
    json_body: dict[str, Any] = {
        "id": 888002,
        "warehouse_id": 1,
        "code": "LOC-TEST-002",
        "name": "Automated Location Post-Get",
    }
    post_response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert post_response.status_code == 201

    get_response = requests.get(f"{url}/888002", headers={'API_KEY': _data['api_key']})
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Automated Location Post-Get"


def test_post_location_wrong_key_403(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations"
    json_body: dict[str, Any] = {
        "id": 888099,
        "name": "Mag Niet Aangemaakt Worden",
    }
    response = requests.post(url, headers={'API_KEY': NO_ACCESS_API_KEY}, json=json_body)
    assert response.status_code == 403


# PUT

def test_put_location_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations/1"
    json_body: dict[str, Any] = {
        "id": 1,
        "warehouse_id": 1,
        "code": "A.1.0",
        "name": "Updated Location Name Pytest"
    }
    response = requests.put(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert response.status_code == 200


def test_put_and_get_location_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations/1"
    json_body: dict[str, Any] = {
        "id": 1,
        "warehouse_id": 1,
        "code": "A.1.0",
        "name": "Updated Name For Get Validation"
    }
    put_response = requests.put(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert put_response.status_code == 200

    get_response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Updated Name For Get Validation"


def test_put_location_wrong_key_403(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations/1"
    json_body: dict[str, Any] = {
        "id": 1,
        "name": "Mag niet aangepast worden",
    }
    response = requests.put(url, headers={'API_KEY': NO_ACCESS_API_KEY}, json=json_body)
    assert response.status_code == 403


# DELETE

def test_delete_locations_collection_not_allowed_405(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations"
    response = requests.delete(url, headers={'API_KEY': _data['api_key']})
    
    # Huidige backend crasht op IndexError op paths[1]
    assert response.status_code == 405


def test_delete_location_200(_data: dict[str, str]) -> None:
    create_url: str = f"http://{_data['host']}{_data['api_path']}locations"
    json_body: dict[str, Any] = {
        "id": 888003,
        "name": "Te Verwijderen LOC"
    }
    post_response = requests.post(create_url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert post_response.status_code == 201

    delete_url: str = f"{create_url}/888003"
    delete_response = requests.delete(delete_url, headers={'API_KEY': _data['api_key']})
    assert delete_response.status_code == 200


def test_delete_location_wrong_key_403(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations/1"
    response = requests.delete(url, headers={'API_KEY': NO_ACCESS_API_KEY})
    assert response.status_code == 403