import pytest
import requests

@pytest.fixture
def _data() -> dict[str, str]:
    return {
        'host': 'localhost:3000',
        'api_path': '/api/v1/',
        'api_key': 'r2e4c6e8i0v3i5n7g9s',        # receiving_station key (voor POST/PUT op transfers)
        'facility_key': 'f4a5c6i7l8i9t0y1m2a3n4a5g6', # facility key (geen mutatierechten op transfers)
    }

# GET

def test_get_transfers_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers"
    response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 200

def test_get_transfers_wrong_api_key_401(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers"
    response = requests.get(url, headers={'API_KEY': 'verkeerde-api-key'})
    assert response.status_code == 401

def test_get_transfer_by_id_200(_data: dict[str, str]) -> None:
    # Haal een bestaande ID op om succesvol te testen
    list_url: str = f"http://{_data['host']}{_data['api_path']}transfers"
    transfers = requests.get(list_url, headers={'API_KEY': _data['api_key']}).json()
    assert len(transfers) > 0
    target_id = transfers[0]["id"]

    url: str = f"http://{_data['host']}{_data['api_path']}transfers/{target_id}"
    response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 200

def test_get_transfer_not_found_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers/999999"
    response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 404

def test_get_transfer_items_200(_data: dict[str, str]) -> None:
    list_url: str = f"http://{_data['host']}{_data['api_path']}transfers"
    transfers = requests.get(list_url, headers={'API_KEY': _data['api_key']}).json()
    target_id = transfers[0]["id"]

    url: str = f"http://{_data['host']}{_data['api_path']}transfers/{target_id}/items"
    response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 200

# POST

def test_create_transfer_201(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers"
    payload = {
        "id": 7771,
        "reference": "TR-TEST-AUTO-01",
        "transfer_from": 1,
        "transfer_to": 2,
        "transfer_status": "Scheduled",
        "items": [{"item_id": 82, "amount": 5}]
    }
    response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=payload)
    assert response.status_code == 201

def test_create_transfer_incomplete_400(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers"
    payload = {"transfer_from": 1}
    response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=payload)
    assert response.status_code == 400

def test_create_transfer_incorrect_types_400(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers"
    payload = {
        "id": "zeven",
        "reference": 1000,
        "transfer_from": "een",
        "transfer_to": "twee"
    }
    response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=payload)
    assert response.status_code == 400

def test_create_transfer_empty_400(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers"
    response = requests.post(url, headers={'API_KEY': _data['api_key']}, json={})
    assert response.status_code == 400

def test_post_transfer_forbidden_403(_data: dict[str, str]) -> None:
    # facility key mag geen transfers aanmaken
    url: str = f"http://{_data['host']}{_data['api_path']}transfers"
    payload = {"id": 7772, "reference": "TR-FORBIDDEN-TEST"}
    response = requests.post(url, headers={'API_KEY': _data['facility_key']}, json=payload)
    assert response.status_code == 403

# PUT

def test_update_transfer_200(_data: dict[str, str]) -> None:
    list_url: str = f"http://{_data['host']}{_data['api_path']}transfers"
    transfers = requests.get(list_url, headers={'API_KEY': _data['api_key']}).json()
    target_tr = transfers[0]
    
    url: str = f"http://{_data['host']}{_data['api_path']}transfers/{target_tr['id']}"
    target_tr["reference"] = "TR-REF-UPDATED"
    
    response = requests.put(url, headers={'API_KEY': _data['api_key']}, json=target_tr)
    assert response.status_code == 200

def test_update_transfer_not_found_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers/999999"
    payload = {"reference": "Ghost Transfer"}
    response = requests.put(url, headers={'API_KEY': _data['api_key']}, json=payload)
    assert response.status_code == 404

def test_update_transfer_wrong_api_key_401(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers/1"
    response = requests.put(url, headers={'API_KEY': 'wrong-api-key'}, json={"reference": "Hacked"})
    assert response.status_code == 401

# DELETE

def test_delete_transfers_collection_not_allowed_405(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}transfers"
    response = requests.delete(url, headers={'API_KEY': _data['api_key']})
    assert response.status_code == 405