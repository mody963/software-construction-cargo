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

# item_types
def test_get_inventories(_data: dict[str, str]):
    url = _data["url"] + "inventories"

    # Send a GET request to the API
    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200


def test_get_inventories_wrong_api_key(_data: dict[str, str]):
    url = _data["url"] + "inventories"

    response = requests.get(url, headers={"API_KEY": "verkeerde-api-key"})

    assert response.status_code == 401


def test_get_inventories_no_api_key(_data: dict[str, str]):
    url = _data["url"] + "inventories"

    response = requests.get(url)

    assert response.status_code == 401

# POST


def test_create_inventories(_data: dict[str, str]):
    url = _data["url"] + "inventories"

    item: dict[str, str | int | float] = {
        "item_id": 0,
        "location_id": 0,
        "quantity_on_hand": 0,
        "quantity_expected": 0,
        "quantity_ordered": 0,
        "quantity_allocated": 0,
    }

    response = requests.post(url, json=item, headers={
                             "API_KEY": _data["api_key"]})

    assert response.status_code == 201


def test_create_incomplete_inventories(_data: dict[str, str]):
    url = _data["url"] + "inventories"

    item = {
        "item_id": 0,
        "location_id": 0,
        "quantity_on_hand": 0,
        "quantity_expected": 0,
        "quantity_ordered": 0,
    }

    response = requests.post(url, json=item, headers={
                             "API_KEY": _data["api_key"]})

    assert response.status_code == 400


# Verkeerde types, strings waar int's en int's waar strings
def test_create_incorrecte_inventories(_data: dict[str, str]):
    url = _data["url"] + "inventories"

    item: dict[str, str | int | float] = {
        "item_id": "0",
        "location_id": "0",
        "quantity_on_hand": 0,
        "quantity_expected": 0,
        "quantity_ordered": 0,
        "quantity_allocated": 0,
    }

    response = requests.post(url, json=item, headers={
                             "API_KEY": _data["api_key"]})

    assert response.status_code == 400
