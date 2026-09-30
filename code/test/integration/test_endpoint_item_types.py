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
def test_get_item_types_200(_data: dict[str, str]):
    url = _data["url"] + "item_types"

    # Send a GET request to the API
    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200


def test_get_item_types_wrong_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_types"

    response = requests.get(url, headers={"API_KEY": "verkeerde-api-key"})

    assert response.status_code == 401


def test_get_item_types_no_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_types"

    response = requests.get(url)

    assert response.status_code == 401


# item/{id}
def test_get_item_type_by_id_200(_data: dict[str, str]):
    url = _data["url"] + "item_types/1"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200


# non exsistent id
def test_get_item_type_not_found_404(_data: dict[str, str]):
    url = _data["url"] + "item_types/9999999999"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 404


# geen int gebruikt maar letters.
def test_get_item_type_invalid_id_400(_data: dict[str, str]):
    url = _data["url"] + "item_types/abc"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


# api key mag niet deleten
def test_delete_item_types_collection_not_allowed_405(_data: dict[str, str]):
    url = _data["url"] + "item_types"

    response = requests.delete(url, headers={"API_KEY": "r2e4c6e8i0v3i5n7g9s"})

    assert response.status_code == 405


# POST


def test_post_item_type_201(_data: dict[str, str]):
    url = _data["url"] + "item_types"

    item: dict[str, str | int | float] = {
        "id": 20,
        "name": "Double",
        "description": "In pairs",
    }

    response = requests.post(url, json=item, headers={
                             "API_KEY": _data["api_key"]})

    assert response.status_code == 201


def test_post_item_type_incomplete_400(_data: dict[str, str]):
    url = _data["url"] + "item_types"

    item = {
        "name": "TEST-INCOMPLETE-ITEMTYPE",
        "description": "Integration Test Item",
    }

    response = requests.post(url, json=item, headers={
                             "API_KEY": _data["api_key"]})

    assert response.status_code == 400


# Verkeerde types, strings waar int's en int's waar strings
def test_post_item_type_incorrect_types_400(_data: dict[str, str]):
    url = _data["url"] + "item_types"

    item: dict[str, str | int | float] = {
        "id": "20",
        "name": "Double",
        "description": "In pairs",
    }

    response = requests.post(url, json=item, headers={
                             "API_KEY": _data["api_key"]})

    assert response.status_code == 400


# PUT


def test_put_item_type_200(_data: dict[str, str]):
    url = _data["url"] + "item_types/1"

    item: dict[str, str | int | float] = {
        "id": 20,
        "name": "Double Up",
        "description": "In pairs of two",
    }

    response = requests.put(url, json=item, headers={
                            "API_KEY": _data["api_key"]})

    assert response.status_code == 200


def test_put_item_type_not_found_404(_data: dict[str, str]):
    url = _data["url"] + "item_types/999999"

    item = {"code": "ITM-TEST-004", "description": "Non Existing Item"}

    response = requests.put(url, json=item, headers={
                            "API_KEY": _data["api_key"]})

    assert response.status_code == 404


def test_put_item_type_wrong_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_types/1"

    item = {"description": "Unauthorized update"}

    response = requests.put(url, json=item, headers={
                            "API_KEY": "wrong-api-key"})

    assert response.status_code == 401
