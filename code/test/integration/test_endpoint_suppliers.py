import pytest
import requests


# zorg dat je zelf de juiste api key invult voor de werkende tests
# en mocht je een foute key willen hebben qua test let er dan op.
@pytest.fixture
def _data():
    return {
        "url": "http://localhost:3000/api/v1/",
        "api_key": "f4a5c6i7l8i9t0y1m2a3n4a5g6",
    }


# GET

# item_types
def test_get_suppliers(_data: dict[str, str]):
    url = _data["url"] + "suppliers"

    # Send a GET request to the API
    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200


def test_get_suppliers_wrong_api_key(_data: dict[str, str]):
    url = _data["url"] + "suppliers"

    response = requests.get(url, headers={"API_KEY": "verkeerde-api-key"})

    assert response.status_code == 401


def test_get_suppliers_no_api_key(_data: dict[str, str]):
    url = _data["url"] + "suppliers"

    response = requests.get(url)

    assert response.status_code == 401


# item/{id}
def test_get_suppliers_by_id(_data: dict[str, str]):
    url = _data["url"] + "suppliers/1"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200


# non exsistent id
def test_get_suppliers_not_found(_data: dict[str, str]):
    url = _data["url"] + "suppliers/9999999999"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 404


# geen int gebruikt maar letters.
def test_get_suppliers_invalid_id(_data: dict[str, str]):
    url = _data["url"] + "suppliers/abc"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


# api key mag niet deleten
def test_delete_suppliers_not_allowed(_data: dict[str, str]):
    url = _data["url"] + "suppliers"

    response = requests.delete(url, headers={"API_KEY": "r2e4c6e8i0v3i5n7g9s"})

    assert response.status_code == 405


# POST


def test_create_suppliers(_data: dict[str, str]):
    url = _data["url"] + "suppliers"

    item: dict[str, str | int | float] = {
        "id": 10,
        "code": "string",
        "name": "string",
        "address": "string",
        "city": "string",
        "zip_code": "string",
        "province": "string",
        "country": "string",
        "contact_name": "string",
        "phone_number": "string",
        "reference": "string"
    }

    response = requests.post(url, json=item, headers={
                             "API_KEY": _data["api_key"]})

    assert response.status_code == 201


def test_create_incomplete_suppliers(_data: dict[str, str]):
    url = _data["url"] + "suppliers"

    item = {
        "code": "string",
        "name": "string",
        "address": "string",
        "city": "string",
        "zip_code": "string",
        "province": "string",
        "country": "string",
        "contact_name": "string",
        "phone_number": "string",
        "reference": "string"
    }

    response = requests.post(url, json=item, headers={
                             "API_KEY": _data["api_key"]})

    assert response.status_code == 400


# Verkeerde types, strings waar int's en int's waar strings
def test_create_incorrecte_suppliers(_data: dict[str, str]):
    url = _data["url"] + "suppliers"

    item: dict[str, str | int | float] = {
        "id": "10",
        "code": "string",
        "name": "string",
        "address": "string",
        "city": "string",
        "zip_code": "string",
        "province": "string",
        "country": "string",
        "contact_name": "string",
        "phone_number": "string",
        "reference": "string"
    }

    response = requests.post(url, json=item, headers={
                             "API_KEY": _data["api_key"]})

    assert response.status_code == 400


# PUT


def test_update_suppliers(_data: dict[str, str]):
    url = _data["url"] + "suppliers/1"

    item: dict[str, str | int | float] = {
        "id": 10,
        "code": "test",
        "name": "test",
        "address": "test",
        "city": "test",
        "zip_code": "test",
        "province": "test",
        "country": "test",
        "contact_name": "test",
        "phone_number": "test",
        "reference": "test"
    }

    response = requests.put(url, json=item, headers={
                            "API_KEY": _data["api_key"]})

    assert response.status_code == 200


def test_update_suppliers_not_found(_data: dict[str, str]):
    url = _data["url"] + "suppliers/999999"

    item = {"code": "ITM-TEST-004", "description": "Non Existing Item"}

    response = requests.put(url, json=item, headers={
                            "API_KEY": _data["api_key"]})

    assert response.status_code == 404


def test_update_suppliers_wrong_api_key(_data: dict[str, str]):
    url = _data["url"] + "suppliers/1"

    item = {"description": "Unauthorized update"}

    response = requests.put(url, json=item, headers={
                            "API_KEY": "wrong-api-key"})

    assert response.status_code == 401
