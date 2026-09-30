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


def test_get_item_groups_200(_data: dict[str, str]):
    url = _data["url"] + "item_groups"

    # Send a GET request to the API
    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200


def test_get_item_groups_wrong_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_groups"

    response = requests.get(url, headers={"API_KEY": "verkeerde-api-key"})

    assert response.status_code == 401


def test_get_item_groups_no_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_groups"

    response = requests.get(url)

    assert response.status_code == 401


# /item_groups/{id}
def test_get_item_group_by_id_200(_data: dict[str, str]):
    url = _data["url"] + "item_groups/2"

    # Send a GET request to the API
    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200


def test_get_item_group_by_id_wrong_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_groups/2"

    response = requests.get(url, headers={"API_KEY": "verkeerde-api-key"})

    assert response.status_code == 401


def test_get_item_group_by_id_no_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_groups/2"

    response = requests.get(url)

    assert response.status_code == 401


# POST


def test_post_item_group_201(_data: dict[str, str]):
    url = _data["url"] + "item_groups"

    item: dict[str, str | int | float] = {
        "id": 4,
        "name": "Bedorven",
        "description": "Kan niet meer verkocht worden.",
        "created_at": "2025-08-01T15:30:26Z",
        "updated_at": "2025-08-16T23:31:09Z",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 201


def test_post_item_group_incomplete_400(_data: dict[str, str]):
    url = _data["url"] + "item_groups"

    item = {
        "name": "Bedorven",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_post_item_group_incorrect_types_400(_data: dict[str, str]):
    url = _data["url"] + "item_groups"

    item: dict[str, str | int | float] = {
        "id": "vier",
        "name": 3,
        "description": 2,
        "created_at": "2025-08-01T15:30:26Z",
        "updated_at": "2025-08-16T23:31:09Z",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_post_item_group_empty_400(_data: dict[str, str]):
    url = _data["url"] + "item_groups"
    item: dict[str, str | int | float] = {}

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


# PUT


def test_put_item_group_200(_data: dict[str, str]):
    url = _data["url"] + "item_groups/2"

    item: dict[str, str | int | float] = {
        "name": "Langer Houdbaar",
        "description": "Temperature/handling regime: Houdbaar",
        "created_at": "2025-08-01T15:30:26Z",
        "updated_at": "2025-08-14T08:35:01Z",
    }

    response = requests.put(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200


def test_put_item_group_not_found_404(_data: dict[str, str]):
    url = _data["url"] + "item_groups/999999"

    item = {"code": "ITM-TEST-004", "description": "Non Existing Item"}

    response = requests.put(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 404


def test_put_item_group_wrong_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_groups/1"

    item = {"description": "Niet houdtbaar"}

    response = requests.put(url, json=item, headers={"API_KEY": "wrong-api-key"})

    assert response.status_code == 401


# DELETE
def test_delete_item_group_403(_data: dict[str, str]):
    url = _data["url"] + "item_groups/1"

    response = requests.delete(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 403


def test_delete_item_group_wrong_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_groups/1"

    response = requests.delete(url, headers={"API_KEY": "wrong_api_key"})

    assert response.status_code == 401


def test_delete_item_group_wrong_id_401(_data: dict[str, str]):
    url = _data["url"] + "item_groups/20000"

    response = requests.delete(url, headers={"API_KEY": "wrong_api_key"})

    assert response.status_code == 401
