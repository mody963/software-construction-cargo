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
def test_get_item_lines_200(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    # Send a GET request to the API
    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200


def test_get_item_lines_wrong_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    response = requests.get(url, headers={"API_KEY": "verkeerde-api-key"})

    assert response.status_code == 401


def test_get_item_lines_no_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    response = requests.get(url)

    assert response.status_code == 401


# POST
def test_post_item_line_201(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    item: dict[str, str | int | float] = {
        "id": 2001,
        "name": "TestItem Aardappelen, groente en fruit",
        "description": "Jumbo assortment line: Aardappelen, groente en fruit",
        "created_at": "2025-08-01T15:30:26Z",
        "updated_at": "2025-08-23T22:38:58Z",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 201


def test_post_item_line_incomplete_400(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    item = {
        "name": "TestItem Aardappelen, groente en fruit",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_post_item_line_incorrect_types_400(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    item: dict[str, str | int | float] = {
        "id": 2002,
        "name": 2,
        "description": 1,
        "created_at": "2025-08-01T15:30:26Z",
        "updated_at": "2025-08-23T22:38:58Z",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_post_item_line_empty_400(_data: dict[str, str]):
    url = _data["url"] + "item_lines"
    item: dict[str, str | int | float] = {}

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


# Item_lines/id


# GET
def test_get_item_line_by_id_200(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    # Send a GET request to the API
    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200


def test_get_item_line_by_id_wrong_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    response = requests.get(url, headers={"API_KEY": "verkeerde-api-key"})

    assert response.status_code == 401


def test_get_item_line_by_id_no_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    response = requests.get(url)

    assert response.status_code == 401


# GET itemlines/id/items
def test_get_item_line_items_200(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1/items"

    # Send a GET request to the API
    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200


def test_get_item_line_items_wrong_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1/items"

    response = requests.get(url, headers={"API_KEY": "verkeerde-api-key"})

    assert response.status_code == 401


def test_get_item_line_items_no_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1/items"

    response = requests.get(url)

    assert response.status_code == 401


# PUT


def test_put_item_line_200(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    item: dict[str, str | int | float] = {
        "name": "Updated Aardappelen, groente en fruit",
        "description": "Jumbo assortment line: Aardappelen, groente en fruit",
        "created_at": "2025-08-01T15:30:26Z",
        "updated_at": "2025-08-23T22:38:58Z",
    }

    response = requests.put(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200


def test_put_item_line_not_found_404(_data: dict[str, str]):
    url = _data["url"] + "item_lines/999999"

    item = {"code": "ITM-TEST-004", "description": "Non Existing Item"}

    response = requests.put(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 404


def test_put_item_line_wrong_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    item = {"description": "Unauthorized update"}

    response = requests.put(url, json=item, headers={"API_KEY": "wrong-api-key"})

    assert response.status_code == 401


# DELETE
def test_delete_item_line_403(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    response = requests.delete(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 403


def test_delete_item_line_wrong_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    response = requests.delete(url, headers={"API_KEY": "wrong_api_key"})

    assert response.status_code == 401
