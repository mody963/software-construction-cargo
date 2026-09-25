import pytest
import requests


# zorg dat je zelf de juiste api key invult voor de werkende tests
# en mocht je een foute key willen hebben qua test let er dan op.
@pytest.fixture
def _data():
    return {
        "url": "http://localhost:3000/api/v1/",
        "api_key": "r2e4c6e8i0v3i5n7g9s",
    }


# GET


def test_get_item(_data: dict[str, str]):
    url = _data["url"] + "items"

    # Send a GET request to the API
    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200


def test_get_items_wrong_api_key(_data: dict[str, str]):
    url = _data["url"] + "items"

    response = requests.get(url, headers={"API_KEY": "verkeerde-api-key"})

    assert response.status_code == 401


def test_get_items_no_api_key(_data: dict[str, str]):
    url = _data["url"] + "items"

    response = requests.get(url)

    assert response.status_code == 401


# item/{id}


def test_get_item_by_id(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200


# non exsistent id
def test_get_item_not_found(_data: dict[str, str]):
    url = _data["url"] + "items/9999999999"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 404


# geen int gebruikt maar letters.
def test_get_item_invalid_id(_data: dict[str, str]):
    url = _data["url"] + "items/abc"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


# api key mag niet deleten
def test_delete_items_not_allowed(_data: dict[str, str]):
    url = _data["url"] + "items"

    response = requests.delete(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 405


# POST


def test_create_item(_data: dict[str, str]):
    url = _data["url"] + "items"

    item: dict[str, str | int | float] = {
        "code": "ITM-TEST-001",
        "description": "Integration Test Item",
        "barcode": "1234567890123",
        "model_number": "TEST-001",
        "commodity_code": 1234567,
        "unit_weight": 0.500,
        "item_line_id": 5,
        "item_group_id": 3,
        "item_type_id": 2,
        "min_purchase_qty": 10,
        "case_size": 5,
        "packaging_type": "Case",
        "order_multiple": 1,
        "supplier_id": 17,
        "supplier_sku": "TEST-SKU-001",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 201


def test_create_incomplete_item(_data: dict[str, str]):
    url = _data["url"] + "items"

    item = {
        "code": "ITM-TEST-001",
        "description": "Integration Test Item",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


# Verkeerde types, strings waar int's en int's waar strings
def test_create_incorrecte_item_types(_data: dict[str, str]):
    url = _data["url"] + "items"

    item: dict[str, str | int | float] = {
        "code": "ITM-TEST-001",
        "description": "Integration Test Item",
        "barcode": "Tesks inplaats van numbers",
        "model_number": "TEST-001",
        "commodity_code": 1234567,
        "unit_weight": "Tekst inplaatsvan nummers",
        "item_line_id": 5,
        "item_group_id": 3,
        "item_type_id": 2,
        "min_purchase_qty": "Tien (moet een nummer zijn)",
        "case_size": "Vijf",
        "packaging_type": "Case",
        "order_multiple": 1,
        "supplier_id": "Zeventien",
        "supplier_sku": "TEST-SKU-001",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


# PUT


def test_update_item(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    item: dict[str, str | int | float] = {
        "code": "ITM-000001",
        "description": "Updated Test Item",
        "barcode": "4313291212776",
        "model_number": "VS-10414",
        "commodity_code": 6268604,
        "unit_weight": 0.336,
        "item_line_id": 5,
        "item_group_id": 3,
        "item_type_id": 2,
        "min_purchase_qty": 24,
        "case_size": 6,
        "packaging_type": "Case",
        "order_multiple": 1,
        "supplier_id": 17,
        "supplier_sku": "SKU-9642297",
    }

    response = requests.put(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200


def test_update_item_not_found(_data: dict[str, str]):
    url = _data["url"] + "items/999999"

    item = {"code": "ITM-TEST-004", "description": "Non Existing Item"}

    response = requests.put(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 404


def test_update_item_wrong_api_key(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    item = {"description": "Unauthorized update"}

    response = requests.put(url, json=item, headers={"API_KEY": "wrong-api-key"})

    assert response.status_code == 401
