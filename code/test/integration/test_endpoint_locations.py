import pytest
import requests


@pytest.fixture
def _data() -> dict[str, str]:
    return {
        'host': 'localhost:3000',
        'api_path': '/api/v1/',
        'api_key': 'f4a5c6i7l8i9t0y1m2a3n4a5g6',  # facility_management key
    }


# 1. GET /locations (List locations)
def test_get_locations_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations"

    response: requests.Response = requests.get(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 2. GET /locations/{id} (Bestaande locatie ophalen)
def test_get_location_by_id_200(_data: dict[str, str]) -> None:
    # Haal eerst de lijst op om een gegarandeerd geldig ID te pakken
    list_url: str = f"http://{_data['host']}{_data['api_path']}locations"
    res_list = requests.get(list_url, headers={'API_KEY': _data['api_key']})
    locations = res_list.json()

    assert len(locations) > 0
    target_id = locations[0]["id"]

    url: str = f"http://{_data['host']}{_data['api_path']}locations/{target_id}"
    response: requests.Response = requests.get(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    assert response.status_code == 200
    assert response.json()["id"] == target_id


# 3. POST /locations (Nieuwe locatie toevoegen)
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

    response: requests.Response = requests.post(
        url,
        headers={
            'API_KEY': _data['api_key'],
            'Content-Type': 'application/json'
        },
        json=payload
    )

    assert response.status_code == 201


# 4. PUT /locations/{id} (Bestaande locatie wijzigen)
def test_put_location_200(_data: dict[str, str]) -> None:
    list_url: str = f"http://{_data['host']}{_data['api_path']}locations"
    res_list = requests.get(list_url, headers={'API_KEY': _data['api_key']})
    locations = res_list.json()
    target_loc = locations[0]
    target_id = target_loc["id"]

    url: str = f"http://{_data['host']}{_data['api_path']}locations/{target_id}"
    target_loc["name"] = "Updated Location Name Pytest"

    response: requests.Response = requests.put(
        url,
        headers={
            'API_KEY': _data['api_key'],
            'Content-Type': 'application/json'
        },
        json=target_loc
    )

    assert response.status_code == 200


# 5. DELETE /locations/{id}
def test_delete_location_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations/8881"

    response: requests.Response = requests.delete(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    # BUG IN BACKEND:
    # Verwachting: 200 OK.
    # Resultaat kan 500 zijn als remove_location faalt op de pool.
    assert response.status_code == 200


# 6. GET /locations (401 Unauthorized)
def test_get_locations_401(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations"

    response: requests.Response = requests.get(
        url,
        headers={'API_KEY': 'verkeerde_sleutel_123'}
    )

    assert response.status_code == 401


# 7. GET /locations/{id} (404 Not Found)
def test_get_location_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations/999999"

    response: requests.Response = requests.get(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    # BUG IN BACKEND:
    # Verwachting: 404 Not Found.
    # Resultaat: 500 of 200 null.
    assert response.status_code == 404


# 8. DELETE /locations (405 Method Not Allowed op collectie)
def test_delete_locations_collection_405(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}locations"

    response: requests.Response = requests.delete(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    # BUG IN BACKEND:
    # Verwachting: 405 Method Not Allowed.
    # Resultaat: 500 Internal Server Error wegens IndexError op paths[1].
    assert response.status_code == 405