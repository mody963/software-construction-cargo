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


def test_get_item_lines_returns_list(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert isinstance(response.json(), list)


def test_get_item_lines_items_have_required_fields(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    item_lines = response.json()

    assert len(item_lines) > 0

    required_fields = {"id", "name", "description", "created_at", "updated_at"}

    assert required_fields.issubset(item_lines[0].keys())


def test_get_item_lines_content_type_json(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert "application/json" in response.headers["Content-Type"]


def test_get_item_lines_wrong_http_method_405(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    response = requests.patch(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 405


# item_line/id


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


def test_get_item_line_by_id_returns_correct_id(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    data = response.json()

    assert data["id"] == 1


def test_get_item_line_by_id_returns_all_fields(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    data = response.json()

    required_fields = {"id", "name", "description", "created_at", "updated_at"}

    assert required_fields.issubset(data.keys())


def test_get_item_line_not_found_404(_data: dict[str, str]):
    url = _data["url"] + "item_lines/999999"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 404


def test_get_item_line_id_text_400(_data: dict[str, str]):
    url = _data["url"] + "item_lines/abc"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


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


def test_post_item_line_invalid_json_400(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    response = requests.post(
        url,
        data="{naam:",
        headers={"API_KEY": _data["api_key"], "Content-Type": "application/json"},
    )

    assert response.status_code == 400


def test_post_item_line_null_values_400(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    item = {
        "id": None,
        "name": None,
        "description": None,
        "created_at": None,
        "updated_at": None,
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_post_item_line_name_empty_400(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    item: dict[str, str | int | float] = {
        "id": 2003,
        "name": "",
        "description": "Test description",
        "created_at": "2025-08-01T15:30:26Z",
        "updated_at": "2025-08-23T22:38:58Z",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_post_item_line_name_only_spaces_400(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    item: dict[str, str | int | float] = {
        "id": 2004,
        "name": "   ",
        "description": "Test description",
        "created_at": "2025-08-01T15:30:26Z",
        "updated_at": "2025-08-23T22:38:58Z",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_post_item_line_wrong_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    item: dict[str, str | int | float] = {
        "id": 2005,
        "name": "Test item line",
        "description": "Test description",
        "created_at": "2025-08-01T15:30:26Z",
        "updated_at": "2025-08-23T22:38:58Z",
    }

    response = requests.post(url, json=item, headers={"API_KEY": "verkeerde-api-key"})

    assert response.status_code == 401


def test_post_item_line_no_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    item: dict[str, str | int | float] = {
        "id": 2006,
        "name": "Test item line",
        "description": "Test description",
        "created_at": "2025-08-01T15:30:26Z",
        "updated_at": "2025-08-23T22:38:58Z",
    }

    response = requests.post(url, json=item)

    assert response.status_code == 401


def test_post_item_line_duplicate_id_400(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    item: dict[str, str | int | float] = {
        "id": 2007,
        "name": "Test duplicate item line",
        "description": "Test description",
        "created_at": "2025-08-01T15:30:26Z",
        "updated_at": "2025-08-23T22:38:58Z",
    }

    # Eerste POST maakt het item aan
    first_response = requests.post(
        url, json=item, headers={"API_KEY": _data["api_key"]}
    )

    assert first_response.status_code == 201

    # Tweede POST gebruikt hetzelfde ID
    second_response = requests.post(
        url, json=item, headers={"API_KEY": _data["api_key"]}
    )

    assert second_response.status_code == 400


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


def test_put_item_line_missing_required_fields_400(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    item: dict[str, str | int | float] = {"name": "Only name"}

    response = requests.put(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_put_item_line_empty_body_400(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    response = requests.put(url, json={}, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_put_item_line_incorrect_types_400(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    item: dict[str, str | int | float] = {
        "name": 123,
        "description": True,
        "created_at": "2025-08-01T15:30:26Z",
        "updated_at": "2025-08-23T22:38:58Z",
    }

    response = requests.put(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_put_item_line_invalid_json_400(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    response = requests.put(
        url,
        data="{naam:",
        headers={"API_KEY": _data["api_key"], "Content-Type": "application/json"},
    )

    assert response.status_code == 400


def test_put_item_line_no_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    item = {"name": "Unauthorized update", "description": "Test"}

    response = requests.put(url, json=item)

    assert response.status_code == 401


def test_put_item_line_name_empty_400(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    item: dict[str, str | int | float] = {
        "name": "",
        "description": "Test description",
        "created_at": "2025-08-01T15:30:26Z",
        "updated_at": "2025-08-23T22:38:58Z",
    }

    response = requests.put(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_put_item_line_change_is_persisted_200(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    item: dict[str, str | int | float] = {
        "name": "Updated Test Item Line",
        "description": "Updated description",
        "created_at": "2025-08-01T15:30:26Z",
        "updated_at": "2025-08-23T22:38:58Z",
    }

    put_response = requests.put(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert put_response.status_code == 200

    get_response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Updated Test Item Line"


# DELETE
def test_delete_item_line_403(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    response = requests.delete(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 403


def test_delete_item_line_wrong_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    response = requests.delete(url, headers={"API_KEY": "wrong_api_key"})

    assert response.status_code == 401


def test_delete_item_line_record_still_exists_after_403(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    delete_response = requests.delete(url, headers={"API_KEY": _data["api_key"]})

    assert delete_response.status_code == 403

    get_response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert get_response.status_code == 200


def test_delete_item_line_nonexistent_id_403(_data: dict[str, str]):
    url = _data["url"] + "item_lines/999999"

    response = requests.delete(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 403


def test_delete_item_line_twice_403(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    first_response = requests.delete(url, headers={"API_KEY": _data["api_key"]})

    second_response = requests.delete(url, headers={"API_KEY": _data["api_key"]})

    assert first_response.status_code == 403
    assert second_response.status_code == 403


def test_delete_item_line_no_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "item_lines/1"

    response = requests.delete(url)

    assert response.status_code == 401


def test_delete_item_lines_collection_not_allowed_405(_data: dict[str, str]):
    url = _data["url"] + "item_lines"

    response = requests.delete(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 405
