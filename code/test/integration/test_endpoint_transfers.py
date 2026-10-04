import pytest
import requests
from typing import Any

@pytest.fixture
def _data() -> dict[str, str]:
    return {
        'host': 'localhost:3000',
        'api_path': '/api/v1/',
        'api_key': 'r2e4c6e8i0v3i5n7g9s',        # receiving_station key (voor POST/PUT op transfers)
    }

# facility_management key mist schrijfrechten op transfers
NO_ACCESS_API_KEY = 'f4a5c6i7l8i9t0y1m2a3n4a5g6' 

# GET

def test_get_transfers_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers"
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 200


def test_get_transfers_wrong_api_key_401(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers"
    response = requests.get(url, headers={'API_KEY': 'verkeerde-api-key'})
    assert response.status_code == 401


def test_get_transfer_invalid_id_integer_not_found_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers/9999999" 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    
    # Zelfde soort bug als bij clients: geeft 200 + null terug
    assert response.status_code == 404


def test_get_transfer_invalid_id_string_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers/AAAAAAAAAAA" 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 404


def test_get_transfer_invalid_id_string_integer_non_alphanumeric_not_found_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers/ABC6d1Xyz$" 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 404


def test_get_transfer_by_id_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers/1" 
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_transfer_items_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers/1/items"
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# POST

def test_post_transfer_201(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers"
    json_body: dict[str, Any] = {
        "id": 777001,
        "reference": "TR-TEST-001",
        "transfer_from": 1,
        "transfer_to": 2,
        "transfer_status": "Scheduled",
        "items": [{"item_id": 82, "amount": 5}]
    }
    response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert response.status_code == 201


def test_post_and_get_transfer_201(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers"
    json_body: dict[str, Any] = {
        "id": 777002,
        "reference": "TR-TEST-002",
        "transfer_from": 1,
        "transfer_to": 2,
        "transfer_status": "Pending",
        "items": [{"item_id": 82, "amount": 2}]
    }
    post_response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert post_response.status_code == 201

    get_response = requests.get(f"{url}/777002", headers={'API_KEY': _data['api_key']})
    assert get_response.status_code == 200
    assert get_response.json()["reference"] == "TR-TEST-002"
    assert get_response.json()["transfer_status"] == "Pending"


def test_post_transfer_wrong_key_403(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers"
    json_body: dict[str, Any] = {
        "id": 777099,
        "reference": "TR-FORBIDDEN-TEST",
    }
    response = requests.post(url, headers={'API_KEY': NO_ACCESS_API_KEY}, json=json_body)
    
    # Facility key mag geen transfers posten
    assert response.status_code == 403


# PUT

def test_put_transfer_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers/1"
    json_body: dict[str, Any] = {
        "id": 1, 
        "reference": "TR00001",
        "transfer_from": 10,
        "transfer_to": 15,
        "transfer_status": "Scheduled"
    }
    response = requests.put(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert response.status_code == 200


def test_put_and_get_transfer_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers/1"
    json_body: dict[str, Any] = {
        "id": 1,
        "reference": "TR00001",
        "transfer_from": 10,
        "transfer_to": 15,
        "transfer_status": "Completed"
    }
    put_response = requests.put(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert put_response.status_code == 200

    get_response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert get_response.status_code == 200
    assert get_response.json()["transfer_status"] == "Completed"


def test_put_transfer_wrong_key_403(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers/1"
    json_body: dict[str, Any] = {
        "id": 1,
        "transfer_status": "Mag niet",
    }
    response = requests.put(url, headers={'API_KEY': NO_ACCESS_API_KEY}, json=json_body)
    assert response.status_code == 403


# DELETE

def test_delete_transfers_collection_not_allowed_405(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers"
    response = requests.delete(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 405


def test_delete_transfer_wrong_key_403(_data: dict[str, str]) -> None:
    # Zelfs r2e4c6e8i0v3i5n7g9s heeft geen delete=True permissie op transfers
    url: str = f"http://{_data['host']}{_data['api_path']}transfers/1"
    response = requests.delete(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 403