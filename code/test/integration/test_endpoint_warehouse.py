import pytest
import requests


@pytest.fixture
def _data() -> dict[str, str]:
    return {
        'host': 'localhost:3000',
        'api_path': '/api/v1/',
        'api_key': 'f4a5c6i7l8i9t0y1m2a3n4a5g6',  # facility_management key (volledige CRUD op warehouses)
    }

# GET

def test_get_warehouses_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses"

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_warehouse_by_id_200(_data: dict[str, str]) -> None:
    # We halen eerst de lijst op om een gegarandeerd geldig ID te pakken
    list_url: str = f"http://{_data['host']}{_data['api_path']}warehouses"
    warehouses = requests.get(list_url, headers={'API_KEY': _data['api_key']}).json()
    target_id = warehouses[0]["id"]

    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/{target_id}"
    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    assert response.status_code == 200
    assert response.json()["id"] == target_id


def test_get_warehouse_locations_200(_data: dict[str, str]) -> None:
    # Warehouse 2 of 3 heeft normaal gesproken locaties gekoppeld
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/3/locations"

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_warehouses_wrong_api_key_401(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses"

    response = requests.get(url, headers={'API_KEY': 'ongeldige_key_123'})

    assert response.status_code == 401


def test_get_warehouse_not_found_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/999999"

    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # BUG IN BACKEND: Verwachting is 404 Not Found, maar backend crasht (500) of geeft 200 met null.
    assert response.status_code == 404


# POST

def test_post_warehouse_201(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses"

    payload = {
        "id": 9995,
        "code": "WH-TEST-DYNAMIC",
        "name": "Dynamic Test Warehouse",
        "address": "Testbaan 5",
        "zip_code": "1234AB",
        "city": "Utrecht",
        "province": "Utrecht",
        "country": "Netherlands",
        "contact_name": "Jan Jansen",
        "contact_phone": "0612345678",
        "contact_email": "jan@cargohub.local",
        "created_at": "2026-09-25T12:00:00Z",
        "updated_at": "2026-09-25T12:00:00Z"
    }

    response = requests.post(url, headers={'API_KEY': _data['api_key'], 'Content-Type': 'application/json'}, json=payload)

    assert response.status_code == 201


def test_post_warehouse_incomplete_400(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses"

    # Ontbrekende verplichte velden
    payload = {"name": "Incomplete Warehouse"}

    response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=payload)
    
    # BUG IN BACKEND: Verwachting 400 Bad Request. Huidige backend geeft waarschijnlijk 500.
    assert response.status_code == 400


def test_post_warehouse_incorrect_types_400(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses"

    # Verkeerde datatypes
    payload = {
        "id": "geen-int",
        "code": 12345,
        "name": "Type Test",
    }

    response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=payload)
    
    # BUG IN BACKEND: Verwachting 400 Bad Request. Huidige backend crasht op types.
    assert response.status_code == 400


def test_post_warehouse_empty_400(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses"

    response = requests.post(url, headers={'API_KEY': _data['api_key']}, json={})
    
    # BUG IN BACKEND: Verwachting 400 Bad Request.
    assert response.status_code == 400

# PUT

def test_put_warehouse_200(_data: dict[str, str]) -> None:
    list_url: str = f"http://{_data['host']}{_data['api_path']}warehouses"
    warehouses = requests.get(list_url, headers={'API_KEY': _data['api_key']}).json()
    target_wh = warehouses[0]
    target_id = target_wh["id"]

    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/{target_id}"

    target_wh["name"] = "Updated Name Through Pytest"

    response = requests.put(url, headers={'API_KEY': _data['api_key'], 'Content-Type': 'application/json'}, json=target_wh)

    assert response.status_code == 200


def test_put_warehouse_not_found_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/999999"

    update_payload = {"name": "Does Not Exist"}
    response = requests.put(url, headers={'API_KEY': _data['api_key']}, json=update_payload)
    
    # BUG IN BACKEND: Verwachting 404 Not Found. Backend crasht of geeft 200 OK.
    assert response.status_code == 404


def test_put_warehouse_wrong_key_401(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/1"
    
    update_payload = {"name": "Unauthorized Update"}
    response = requests.put(url, headers={'API_KEY': 'verkeerde-api-key'}, json=update_payload)
    
    assert response.status_code == 401

# DELETE
def test_delete_warehouse_200(_data: dict[str, str]) -> None:
    # We verwijderen het zojuist aangemaakte test-warehouse (ID 9995)
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/9995"

    response = requests.delete(url, headers={'API_KEY': _data['api_key']})

    # BUG IN BACKEND: Geeft 500 als object al mist of corrupt is in data pool.
    assert response.status_code == 200


def test_delete_warehouses_collection_not_allowed_405(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses"

    response = requests.delete(url, headers={'API_KEY': _data['api_key']})

    # BUG IN BACKEND: Verwachting 405 Method Not Allowed. Backend geeft 500 wegens IndexError.
    assert response.status_code == 405