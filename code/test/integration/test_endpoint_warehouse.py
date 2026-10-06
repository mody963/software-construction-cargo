import pytest
import requests
from typing import Any

# Zorg dat je zelf de juiste api key invult voor de werkende tests
@pytest.fixture
def _data() -> dict[str, str]:
    return {
        'host': 'localhost:3000',
        'api_path': '/api/v1/',
        'api_key': 'f4a5c6i7l8i9t0y1m2a3n4a5g6',  # facility_management key (volledige CRUD op warehouses)
    }

# facility_management heeft alle rechten op warehouses, receiving_station heeft geen POST/PUT/DELETE.
NO_ACCESS_API_KEY = 'r2e4c6e8i0v3i5n7g9s'

# GET

def test_get_warehouses_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses"
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_warehouses_wrong_api_key_401(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses"
    response = requests.get(url, headers={'API_KEY': 'ongeldige_key_123'})
    assert response.status_code == 401


def test_get_warehouse_invalid_id_integer_not_found_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/999999" # Warehouse die niet bestaat.
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    
    # Deze geeft momenteel geen 404 mee maar alsnog een 200 met null of een 500.
    # Het zoekt nog steeds naar het warehouse maar geeft gewoon geen juiste waardes terug mee.
    assert response.status_code == 404


def test_get_warehouse_invalid_id_string_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/abcdef"
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    
    # Momenteel geeft dit een 500 omdat de backend crasht op int(paths[1]) met een ValueError.
    assert response.status_code == 404


def test_get_warehouse_invalid_id_string_integer_non_alphanumeric_not_found_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/ABC6d1Xyz$"
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    
    # Zelfde bug als bij test_get_warehouse_invalid_id_string_404 (crasht op ValueError).
    assert response.status_code == 404


def test_get_warehouse_by_id_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/1" # Warehouse met id 1 zit in seed data
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_warehouse_locations_200(_data: dict[str, str]) -> None:
    # sub-resource: /warehouses/<id>/locations (Warehouse 2 of 3 heeft locaties)
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/3/locations"
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# POST

def test_post_warehouse_201(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses"
    json_body: dict[str, Any] = {
        "id": 999001,
        "code": "WH-TEST-001",
        "name": "Test Magazijn BV",
        "address": "Teststraat 1",
        "zip_code": "3011AB",
        "city": "Rotterdam",
        "province": "Zuid-Holland",
        "country": "Netherlands",
        "contact_name": "Test Persoon",
        "contact_phone": "010-1234567",
        "contact_email": "test.wh@example.com",
        "created_at": "2026-09-25T12:00:00Z",
        "updated_at": "2026-09-25T12:00:00Z"
    }
    response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert response.status_code == 201


def test_post_and_get_warehouse_201(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses"
    json_body: dict[str, Any] = {
        "id": 999002,
        "code": "WH-TEST-002",
        "name": "Test Magazijn Post-Get",
        "address": "Teststraat 2",
        "zip_code": "3011AC",
        "city": "Rotterdam",
        "province": "Zuid-Holland",
        "country": "Netherlands",
        "contact_name": "Test Persoon 2",
        "contact_phone": "010-7654321",
        "contact_email": "test.wh2@example.com",
    }
    post_response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert post_response.status_code == 201

    get_response = requests.get(f"{url}/999002", headers={'API_KEY': _data['api_key']})
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test Magazijn Post-Get"
    assert get_response.json()["city"] == "Rotterdam"


def test_post_warehouse_wrong_key_403(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses"
    json_body: dict[str, Any] = {
        "id": 999099,
        "name": "Mag Niet Aangemaakt Worden",
    }
    response = requests.post(url, headers={'API_KEY': NO_ACCESS_API_KEY}, json=json_body)
    
    # Deze key heeft geen POST rechten op warehouses
    assert response.status_code == 403


# PUT

def test_put_warehouse_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/1"
    json_body: dict[str, Any] = {
        "id": 1, # ID moet expliciet mee, anders is hij het kwijt in de json pool
        "code": "VGH-AMB",
        "name": "Jumbo DC Veghel Ambient",
        "address": "De Amert 409",
        "city": "Veghel",
        "zip_code": "5462 GH",
        "province": "Noord-Brabant",
        "country": "Netherlands",
        "contact_name": "Test Put",
        "contact_phone": "020-1112223",
        "contact_email": "put.test@example.com"
    }
    response = requests.put(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert response.status_code == 200


def test_put_and_get_warehouse_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/1"
    json_body: dict[str, Any] = {
        "id": 1,
        "code": "VGH-AMB",
        "name": "Jumbo DC Veghel Ambient",
        "address": "Aangepaste Straat 123",
        "city": "Veghel",
        "zip_code": "5462 GH",
        "province": "Noord-Brabant",
        "country": "Netherlands"
    }
    put_response = requests.put(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert put_response.status_code == 200

    get_response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert get_response.status_code == 200
    assert get_response.json()["address"] == "Aangepaste Straat 123"


def test_put_warehouse_wrong_key_403(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/1"
    json_body: dict[str, Any] = {
        "id": 1,
        "name": "Mag niet aangepast worden",
    }
    response = requests.put(url, headers={'API_KEY': NO_ACCESS_API_KEY}, json=json_body)
    assert response.status_code == 403


# DELETE

def test_delete_warehouses_collection_not_allowed_405(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses"
    response = requests.delete(url, headers={'API_KEY': _data['api_key']})
    
    # DELETE is niet toegestaan op de hele collectie. Huidige backend crasht op IndexError.
    assert response.status_code == 405


def test_delete_warehouse_200(_data: dict[str, str]) -> None:
    create_url: str = f"http://{_data['host']}{_data['api_path']}warehouses"
    json_body: dict[str, Any] = {
        "id": 999003,
        "code": "WH-DEL-01",
        "name": "Te Verwijderen WH"
    }
    post_response = requests.post(create_url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert post_response.status_code == 201

    delete_url: str = f"{create_url}/999003"
    delete_response = requests.delete(delete_url, headers={'API_KEY': _data['api_key']})
    assert delete_response.status_code == 200


def test_delete_and_get_warehouse_404(_data: dict[str, str]) -> None:
    create_url: str = f"http://{_data['host']}{_data['api_path']}warehouses"
    json_body: dict[str, Any] = {
        "id": 999004,
        "code": "WH-DEL-02",
        "name": "Te Verwijderen en Opvragen WH"
    }
    post_response = requests.post(create_url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert post_response.status_code == 201

    delete_url: str = f"{create_url}/999004"
    delete_response = requests.delete(delete_url, headers={'API_KEY': _data['api_key']})
    assert delete_response.status_code == 200

    get_response = requests.get(delete_url, headers={'API_KEY': _data['api_key']})
    
    # Zelfde bug als standaard 404: backend retourneert momenteel 200 met null of 500 na verwijdering.
    assert get_response.status_code == 404


def test_delete_warehouse_wrong_key_403(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/1"
    response = requests.delete(url, headers={'API_KEY': NO_ACCESS_API_KEY})
    assert response.status_code == 403