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


def test_get_items_200(_data: dict[str, str]):
    url = _data["url"] + "items"

    # Send a GET request to the API
    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200


def test_get_items_wrong_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "items"

    response = requests.get(url, headers={"API_KEY": "verkeerde-api-key"})

    assert response.status_code == 401


def test_get_items_no_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "items"

    response = requests.get(url)

    assert response.status_code == 401


def test_get_items_empty_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "items"

    response = requests.get(url, headers={"API_KEY": ""})

    assert response.status_code == 401


def test_get_items_api_key_extra_chars_401(_data: dict[str, str]):
    url = _data["url"] + "items"

    response = requests.get(url, headers={"API_KEY": _data["api_key"] + "xyz"})

    assert response.status_code == 401


def test_get_items_wrong_http_method_405(_data: dict[str, str]):
    url = _data["url"] + "items"

    response = requests.patch(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 405


def test_get_items_returns_list(_data: dict[str, str]):
    url = _data["url"] + "items"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_items_content_type_json(_data: dict[str, str]):
    url = _data["url"] + "items"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]


# item/{id}
def test_get_item_by_id_200(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200


# non exsistent id
def test_get_item_not_found_404(_data: dict[str, str]):
    url = _data["url"] + "items/9999999999"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 404


# geen int gebruikt maar letters.
def test_get_item_invalid_id_400(_data: dict[str, str]):
    url = _data["url"] + "items/abc"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_get_item_by_id_returns_all_fields_200(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200

    item = response.json()

    required_fields = [
        "id",
        "code",
        "description",
        "barcode",
        "model_number",
        "commodity_code",
        "unit_weight",
        "item_line_id",
        "item_group_id",
        "item_type_id",
        "min_purchase_qty",
        "case_size",
        "packaging_type",
        "order_multiple",
        "supplier_id",
        "supplier_sku",
        "created_at",
        "updated_at",
    ]

    for field in required_fields:
        assert field in item


def test_get_item_id_zero_404(_data: dict[str, str]):
    url = _data["url"] + "items/0"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 404


def test_get_item_negative_id_400(_data: dict[str, str]):
    url = _data["url"] + "items/-1"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_get_item_extremely_large_id_404(_data: dict[str, str]):
    url = _data["url"] + "items/99999999999999999999"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 404


# server mag niet crashen vandaar de != 500  andere passende foutcode is prma
def test_get_item_empty_id_not500(_data: dict[str, str]):
    url = _data["url"] + "items/"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code != 500


def test_get_item_by_id_wrong_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    response = requests.get(url, headers={"API_KEY": "verkeerde-api-key"})

    assert response.status_code == 401


def test_get_item_by_id_no_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    response = requests.get(url)

    assert response.status_code == 401


def test_get_item_by_id_empty_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    response = requests.get(url, headers={"API_KEY": ""})

    assert response.status_code == 401


# /items/id/inventory
def test_get_item_inventory_200(_data: dict[str, str]):
    url = _data["url"] + "items/1/inventory"

    # Send a GET request to the API
    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200


def test_get_item_inventory_wrong_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "items/1/inventory"

    response = requests.get(url, headers={"API_KEY": "verkeerde-api-key"})

    assert response.status_code == 401


def test_get_item_inventory_no_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "items/1/inventory"

    response = requests.get(url)

    assert response.status_code == 401


def test_get_item_inventory_returns_list_200(_data: dict[str, str]):
    url = _data["url"] + "items/1/inventory"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_item_inventory_wrong_item_id_404(_data: dict[str, str]):
    url = _data["url"] + "items/999999/inventory"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 404


def test_get_item_inventory_invalid_id_400(_data: dict[str, str]):
    url = _data["url"] + "items/abc/inventory"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_get_item_inventory_empty_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "items/1/inventory"

    response = requests.get(url, headers={"API_KEY": ""})

    assert response.status_code == 401


def test_get_item_inventory_api_key_extra_chars_401(_data: dict[str, str]):
    url = _data["url"] + "items/1/inventory"

    response = requests.get(url, headers={"API_KEY": _data["api_key"] + "xyz"})

    assert response.status_code == 401


# items/id/inventory/totals


def test_get_item_inventory_totals_200(_data: dict[str, str]):
    url = _data["url"] + "items/1/inventory/totals"

    # Send a GET request to the API
    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200


def test_get_item_inventory_totals_wrong_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "items/1/inventory/totals"

    response = requests.get(url, headers={"API_KEY": "verkeerde-api-key"})

    assert response.status_code == 401


def test_get_item_inventory_totals_returns_object_200(_data: dict[str, str]):
    url = _data["url"] + "items/1/inventory/totals"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_item_inventory_totals_has_required_fields_200(_data: dict[str, str]):
    url = _data["url"] + "items/1/inventory/totals"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 200

    totals = response.json()

    required_fields = [
        "expected",
        "ordered",
        "allocated",
        "available",
    ]

    for field in required_fields:
        assert field in totals


def test_get_item_inventory_totals_wrong_item_id_404(_data: dict[str, str]):
    url = _data["url"] + "items/999999/inventory/totals"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 404


def test_get_item_inventory_totals_invalid_id_400(_data: dict[str, str]):
    url = _data["url"] + "items/abc/inventory/totals"

    response = requests.get(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_get_item_inventory_totals_no_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "items/1/inventory/totals"

    response = requests.get(url)

    assert response.status_code == 401


def test_get_item_inventory_totals_empty_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "items/1/inventory/totals"

    response = requests.get(url, headers={"API_KEY": ""})

    assert response.status_code == 401


def test_get_item_inventory_totals_api_key_extra_chars_401(_data: dict[str, str]):
    url = _data["url"] + "items/1/inventory/totals"

    response = requests.get(url, headers={"API_KEY": _data["api_key"] + "xyz"})

    assert response.status_code == 401


# POST


def test_post_item_201(_data: dict[str, str]):
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


def test_post_item_incomplete_400(_data: dict[str, str]):
    url = _data["url"] + "items"

    item = {
        "code": "ITM-TEST-001",
        "description": "Integration Test Item",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


# Verkeerde types, strings waar int's en int's waar strings
def test_post_item_incorrect_types_400(_data: dict[str, str]):
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


def test_post_item_empty_body_400(_data: dict[str, str]):
    url = _data["url"] + "items"

    item: dict[str, str | int | float] = {}

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_post_item_invalid_json_400(_data: dict[str, str]):
    url = _data["url"] + "items"

    invalid_json = '{"code":'

    response = requests.post(
        url,
        data=invalid_json,
        headers={
            "API_KEY": _data["api_key"],
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 400


def test_post_item_null_values_400(_data: dict[str, str]):
    url = _data["url"] + "items"

    item = {
        "code": None,
        "description": None,
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_post_item_string_too_long_400(_data: dict[str, str]):
    url = _data["url"] + "items"

    item: dict[str, str | int | float] = {
        "code": "A" * 10000,
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

    assert response.status_code == 400


def test_post_item_duplicate_id_400(_data: dict[str, str]):
    url = _data["url"] + "items"

    item: dict[str, str | int | float] = {
        "id": 1,
        "code": "ITM-TEST-001",
        "description": "Duplicate ID Test",
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

    assert response.status_code == 400


def test_post_item_unknown_extra_fields_201(_data: dict[str, str]):
    url = _data["url"] + "items"

    item: dict[str, str | int | float] = {
        "code": "ITM-TEST-001",
        "description": "Extra Field Test",
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
        "foo": "bar",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 201


def test_post_item_wrong_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "items"

    item = {
        "code": "ITM-TEST-001",
        "description": "Wrong API Key Test",
    }

    response = requests.post(
        url,
        json=item,
        headers={"API_KEY": "verkeerde-api-key"},
    )

    assert response.status_code == 401


def test_post_item_no_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "items"

    item = {
        "code": "ITM-TEST-001",
        "description": "No API Key Test",
    }

    response = requests.post(url, json=item)

    assert response.status_code == 401


def test_post_item_duplicate_code_400(_data: dict[str, str]):
    url = _data["url"] + "items"

    item: dict[str, str | int | float] = {
        "code": "ITM-TEST-001",
        "description": "Duplicate Code Test",
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

    assert response.status_code in [400, 409]


def test_post_item_nonexistent_item_line_id_400(_data: dict[str, str]):
    url = _data["url"] + "items"

    item: dict[str, str | int | float] = {
        "code": "ITM-TEST-001",
        "description": "Invalid Item Line Test",
        "barcode": "1234567890123",
        "model_number": "TEST-001",
        "commodity_code": 1234567,
        "unit_weight": 0.500,
        "item_line_id": 999999,
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

    assert response.status_code == 400


def test_post_item_nonexistent_item_group_id_400(_data: dict[str, str]):
    url = _data["url"] + "items"

    item: dict[str, str | int | float] = {
        "code": "ITM-TEST-001",
        "description": "Invalid Item Group Test",
        "barcode": "1234567890123",
        "model_number": "TEST-001",
        "commodity_code": 1234567,
        "unit_weight": 0.500,
        "item_line_id": 5,
        "item_group_id": 999999,
        "item_type_id": 2,
        "min_purchase_qty": 10,
        "case_size": 5,
        "packaging_type": "Case",
        "order_multiple": 1,
        "supplier_id": 17,
        "supplier_sku": "TEST-SKU-001P",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_post_item_nonexistent_item_type_id_400(_data: dict[str, str]):
    url = _data["url"] + "items"

    item: dict[str, str | int | float] = {
        "code": "ITM-TEST-001",
        "description": "Invalid Item Type Test",
        "barcode": "1234567890123",
        "model_number": "TEST-001",
        "commodity_code": 1234567,
        "unit_weight": 0.500,
        "item_line_id": 5,
        "item_group_id": 3,
        "item_type_id": 999999,
        "min_purchase_qty": 10,
        "case_size": 5,
        "packaging_type": "Case",
        "order_multiple": 1,
        "supplier_id": 17,
        "supplier_sku": "TEST-SKU-001",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_post_item_nonexistent_supplier_id_400(_data: dict[str, str]):
    url = _data["url"] + "items"

    item: dict[str, str | int | float] = {
        "code": "ITM-TEST-001",
        "description": "Invalid Supplier Test",
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
        "supplier_id": 999999,
        "supplier_sku": "TEST-SKU-001",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_post_item_negative_unit_weight_400(_data: dict[str, str]):
    url = _data["url"] + "items"

    item: dict[str, str | int | float] = {
        "code": "ITM-TEST-001",
        "description": "Negative Weight Test",
        "barcode": "1234567890123",
        "model_number": "TEST-001",
        "commodity_code": 1234567,
        "unit_weight": -1.5,
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

    assert response.status_code == 400


def test_post_item_zero_case_size_400(_data: dict[str, str]):
    url = _data["url"] + "items"

    item: dict[str, str | int | float] = {
        "code": "ITM-TEST-001",
        "description": "Zero Case Size Test",
        "barcode": "1234567890123",
        "model_number": "TEST-001",
        "commodity_code": 1234567,
        "unit_weight": 0.500,
        "item_line_id": 5,
        "item_group_id": 3,
        "item_type_id": 2,
        "min_purchase_qty": 10,
        "case_size": 0,
        "packaging_type": "Case",
        "order_multiple": 1,
        "supplier_id": 17,
        "supplier_sku": "TEST-SKU-001",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_post_item_negative_min_purchase_qty_400(_data: dict[str, str]):
    url = _data["url"] + "items"

    item: dict[str, str | int | float] = {
        "code": "ITM-TEST-001",
        "description": "Negative Quantity Test",
        "barcode": "1234567890123",
        "model_number": "TEST-001",
        "commodity_code": 1234567,
        "unit_weight": 0.500,
        "item_line_id": 5,
        "item_group_id": 3,
        "item_type_id": 2,
        "min_purchase_qty": -10,
        "case_size": 5,
        "packaging_type": "Case",
        "order_multiple": 1,
        "supplier_id": 17,
        "supplier_sku": "TEST-SKU-001",
    }

    response = requests.post(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 400


def test_post_item_empty_code_400(_data: dict[str, str]):
    url = _data["url"] + "items"

    item: dict[str, str | int | float] = {
        "code": "",
        "description": "Empty Code Test",
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

    assert response.status_code == 400


# PUT


def test_put_item_200(_data: dict[str, str]):
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


def test_put_item_not_found_404(_data: dict[str, str]):
    url = _data["url"] + "items/999999"

    item = {"code": "ITM-TEST-004", "description": "Non Existing Item"}

    response = requests.put(url, json=item, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 404


def test_put_item_wrong_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    item = {"description": "Unauthorized update"}

    response = requests.put(url, json=item, headers={"API_KEY": "wrong-api-key"})

    assert response.status_code == 401


def test_put_item_missing_required_fields_400(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    item = {
        "code": "ITM-TEST-004",
    }

    response = requests.put(
        url,
        json=item,
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 400


def test_put_item_empty_body_400(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    item: dict[str, str | int | float] = {}

    response = requests.put(
        url,
        json=item,
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 400


def test_put_item_incorrect_types_400(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    item: dict[str, str | int | float] = {
        "code": "ITM-000001",
        "description": "Incorrect Types Test",
        "barcode": "Test in plaats van nummer",
        "model_number": "VS-10414",
        "commodity_code": "Dit moet een nummer zijn",
        "unit_weight": "Dit moet een nummer zijn",
        "item_line_id": "vijf",
        "item_group_id": 3,
        "item_type_id": 2,
        "min_purchase_qty": "vierentwintig",
        "case_size": 6,
        "packaging_type": "Case",
        "order_multiple": 1,
        "supplier_id": 17,
        "supplier_sku": "SKU-9642297",
    }

    response = requests.put(
        url,
        json=item,
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 400


def test_put_item_invalid_json_400(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    invalid_json = '{"code":'

    response = requests.put(
        url,
        data=invalid_json,
        headers={
            "API_KEY": _data["api_key"],
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 400


def test_put_item_no_api_key_401(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    item = {
        "description": "No API Key Test",
    }

    response = requests.put(url, json=item)

    assert response.status_code == 401


def test_put_item_change_is_persisted_200(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    item: dict[str, str | int | float] = {
        "code": "ITM-000001",
        "description": "Updated Description",
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

    put_response = requests.put(
        url,
        json=item,
        headers={"API_KEY": _data["api_key"]},
    )

    assert put_response.status_code == 200

    get_response = requests.get(
        url,
        headers={"API_KEY": _data["api_key"]},
    )

    assert get_response.status_code == 200
    assert get_response.json()["description"] == "Updated Description"


def test_put_item_nonexistent_item_line_id_400(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    item: dict[str, str | int | float] = {
        "code": "ITM-000001",
        "description": "Invalid Item Line Test",
        "barcode": "4313291212776",
        "model_number": "VS-10414",
        "commodity_code": 6268604,
        "unit_weight": 0.336,
        "item_line_id": 999999,
        "item_group_id": 3,
        "item_type_id": 2,
        "min_purchase_qty": 24,
        "case_size": 6,
        "packaging_type": "Case",
        "order_multiple": 1,
        "supplier_id": 17,
        "supplier_sku": "SKU-9642297",
    }

    response = requests.put(
        url,
        json=item,
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 400


def test_put_item_nonexistent_item_group_id_400(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    item: dict[str, str | int | float] = {
        "code": "ITM-000001",
        "description": "Invalid Item Group Test",
        "barcode": "4313291212776",
        "model_number": "VS-10414",
        "commodity_code": 6268604,
        "unit_weight": 0.336,
        "item_line_id": 5,
        "item_group_id": 999999,
        "item_type_id": 2,
        "min_purchase_qty": 24,
        "case_size": 6,
        "packaging_type": "Case",
        "order_multiple": 1,
        "supplier_id": 17,
        "supplier_sku": "SKU-9642297",
    }

    response = requests.put(
        url,
        json=item,
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 400


def test_put_item_nonexistent_item_type_id_400(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    item: dict[str, str | int | float] = {
        "code": "ITM-000001",
        "description": "Invalid Item Type Test",
        "barcode": "4313291212776",
        "model_number": "VS-10414",
        "commodity_code": 6268604,
        "unit_weight": 0.336,
        "item_line_id": 5,
        "item_group_id": 3,
        "item_type_id": 999999,
        "min_purchase_qty": 24,
        "case_size": 6,
        "packaging_type": "Case",
        "order_multiple": 1,
        "supplier_id": 17,
        "supplier_sku": "SKU-9642297",
    }

    response = requests.put(
        url,
        json=item,
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 400


def test_put_item_nonexistent_supplier_id_400(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    item: dict[str, str | int | float] = {
        "code": "ITM-000001",
        "description": "Invalid Supplier Test",
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
        "supplier_id": 999999,
        "supplier_sku": "SKU-9642297",
    }

    response = requests.put(
        url,
        json=item,
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 400


# DELETE


def test_delete_items_not_allowed_405(_data: dict[str, str]):
    url = _data["url"] + "items"

    response = requests.delete(url, headers={"API_KEY": _data["api_key"]})

    assert response.status_code == 405


def test_delete_item_403(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    response = requests.delete(
        url,
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 403


def test_delete_item_twice_403(_data: dict[str, str]):
    url = _data["url"] + "items/1"

    first_response = requests.delete(
        url,
        headers={"API_KEY": _data["api_key"]},
    )

    second_response = requests.delete(
        url,
        headers={"API_KEY": _data["api_key"]},
    )

    assert first_response.status_code == 403
    assert second_response.status_code == 403


def test_delete_item_nonexistent_id_403(_data: dict[str, str]):
    url = _data["url"] + "items/999999"

    response = requests.delete(
        url,
        headers={"API_KEY": _data["api_key"]},
    )

    assert response.status_code == 403
