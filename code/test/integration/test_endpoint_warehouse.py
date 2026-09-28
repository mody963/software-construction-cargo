import pytest
import requests


@pytest.fixture
def _data() -> dict[str, str]:
    return {
        'host': 'localhost:3000',
        'api_path': '/api/v1/',
        'api_key': 'f4a5c6i7l8i9t0y1m2a3n4a5g6',  # facility_management key
    }


# 1. GET /warehouses (List warehouses)
def test_get_warehouses_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses"

    response: requests.Response = requests.get(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 2. GET /warehouses/{id} (Bestaand warehouse opvragen)
def test_get_warehouse_by_id_200(_data: dict[str, str]) -> None:
    # We halen eerst de lijst op en pakken het ID van het eerste beschikbare warehouse
    list_url: str = f"http://{_data['host']}{_data['api_path']}warehouses"
    res_list = requests.get(list_url, headers={'API_KEY': _data['api_key']})
    warehouses = res_list.json()

    assert len(warehouses) > 0
    target_id = warehouses[0]["id"]

    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/{target_id}"
    response: requests.Response = requests.get(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    assert response.status_code == 200
    assert response.json()["id"] == target_id


# 3. POST /warehouses (Aanmaken van nieuw warehouse)
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

    response: requests.Response = requests.post(
        url,
        headers={
            'API_KEY': _data['api_key'],
            'Content-Type': 'application/json'
        },
        json=payload
    )

    assert response.status_code == 201


# 4. PUT /warehouses/{id} (Updaten van bestaand warehouse)
def test_put_warehouse_200(_data: dict[str, str]) -> None:
    # Pak een bestaand warehouse uit de lijst
    list_url: str = f"http://{_data['host']}{_data['api_path']}warehouses"
    res_list = requests.get(list_url, headers={'API_KEY': _data['api_key']})
    warehouses = res_list.json()
    target_wh = warehouses[0]
    target_id = target_wh["id"]

    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/{target_id}"

    # Stuur bestaande payload mee met gewijzigde naam
    target_wh["name"] = "Updated Name Through Pytest"

    response: requests.Response = requests.put(
        url,
        headers={
            'API_KEY': _data['api_key'],
            'Content-Type': 'application/json'
        },
        json=target_wh
    )

    assert response.status_code == 200


# 5. GET /warehouses/{id}/locations
def test_get_warehouse_locations_200(_data: dict[str, str]) -> None:
    # We bevragen warehouse 3 of een ander bestaand ID
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/3/locations"

    response: requests.Response = requests.get(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 6. DELETE /warehouses/{id} (Verwijderen van test-warehouse)
def test_delete_warehouse_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/9995"

    response: requests.Response = requests.delete(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    # BUG IN BACKEND:
    # Geeft 500 als het ID niet in de data pool gevonden wordt door remove_warehouse()
    assert response.status_code == 200


# 7. GET /warehouses (401 Unauthorized check)
def test_get_warehouse_401(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses"

    response: requests.Response = requests.get(
        url,
        headers={'API_KEY': 'ongeldige_key_123'}
    )

    assert response.status_code == 401


# 8. GET /warehouses/{id} (404 check)
def test_get_warehouse_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses/999999"

    response: requests.Response = requests.get(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    # BUG IN BACKEND:
    # Verwachting: 404 Not Found.
    # Resultaat: 500 Server Error of 200 OK met null.
    assert response.status_code == 404


# 9. DELETE /warehouses (405 Method Not Allowed check)
def test_delete_warehouses_collection_405(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}warehouses"

    response: requests.Response = requests.delete(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    # BUG IN BACKEND:
    # Verwachting: 405 Method Not Allowed.
    # Resultaat: 500 Internal Server Error wegens IndexError op paths[1].
    assert response.status_code == 405