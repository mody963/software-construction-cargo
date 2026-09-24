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
