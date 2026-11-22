import pytest
import requests
from typing import Any
from concurrent.futures import ThreadPoolExecutor # dit is om te zorgen dat je de 2 orders tegelijkertijd kunt proberen te doen want anders gaat het gewoon na mekaar zijnb
from uuid import uuid4 # is voor unieke id creeatie

# zorg dat je zelf de juiste api key invult voor de werkende tests 
# en mocht je een foute key willen hebben qua test let er dan op. 
@pytest.fixture
def _data():
    return {
        'host': 'localhost:3000',
        'api_path': '/api/v1/',
        'api_key': 'r2e4c6e8i0v3i5n7g9s',
    }



NO_ACCESS_API_KEY = 'f4a5c6i7l8i9t0y1m2a3n4a5g6'

# Get------------------------------------------------------------------------------------------------

def test_get_orders_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}orders"

    response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})

    assert response.status_code == 200


def test_get_orders_wrong_api_key_401(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}orders"

    response: requests.Response = requests.get(url, headers={'API_KEY': 'a1b2c3d4e5'})

    assert response.status_code == 401


def test_get_orderinvalid_id_int_not_found_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}orders/9999999" # order die niet bestaat

    response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})
    print(response.status_code)
    print(response.text)

    assert response.status_code == 404

    # zelfde soort bug als bij clients: dit endpoint geeft momenteel 200 + null terug
    # in plaats van 404, ook al bestaat de ord niet.

def test_get_order_invalid_id_string_not_found_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}orders/AAAAAAA" # order die niet bestaat

    response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})
    print(response.status_code)
    print(response.text)

    assert response.status_code == 404

    # zelfde soort bug als bij clients: dit endpoint geeft momenteel 200 + null terug
    # in plaats van 404, ook al bestaat de ord niet.

def test_get_order_invalid_id_string_integer_non_alphanumeric_not_found_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}orders/ABC6d1Xyz$" # order die niet bestaat

    response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})
    print(response.status_code)
    print(response.text)

    assert response.status_code == 404

    # zelfde soort bug als bij clients: dit endpoint geeft momenteel 200 + null terug
    # in plaats van 404, ook al bestaat de ord niet.


def test_get_order_by_id_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}orders/1" # order met id 1 bestaat altijd in de seed data

    response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_order_items_200(_data: dict[str, str]) -> None:
    # sub-resource: /orders/<id>/items
    url: str = f"http://{_data['host']}{_data['api_path']}orders/1/items"

    response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})

    assert response.status_code == 200
    assert isinstance(response.json(), list)


#--------------------------------------POST------------------------------------

def _new_test_order(items=None):
    order_id = 900000000 + (uuid4().int % 100000000)
    return {
        "id": order_id,
        "client_id": 1,
        "order_date": "2026-11-11T10:00:00Z",
        "request_date": "2026-11-12T10:00:00Z",
        "reference": f"ORD-EDGE-{order_id}",
        "customer_po_number": f"PO-EDGE-{order_id}",
        "order_status": "Pending",
        "shipping_notes": None,
        "warehouse_id": 1,
        "ship_to_client_id": 1,
        "bill_to_client_id": 1,
        "items": items if items is not None else [{"item_id": 1, "amount": 1}],
    }


def _orders_url(_data):
    return f"http://{_data['host']}{_data['api_path']}orders"


def _order_headers(_data):
    return {"API_KEY": _data["api_key"]}


def test_post_order_201(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}orders"
    json_body: dict[str, Any] = {
        "id": 999001,
        "client_id": 1,
        "order_date": "2026-09-29T10:00:00Z",
        "request_date": "2026-10-01T10:00:00Z",
        "reference": "ORD-TEST-001",
        "customer_po_number": "PO-TEST-001",
        "order_status": "Pending",
        "shipping_notes": None,
        "warehouse_id": 1,
        "ship_to_client_id": 1,
        "bill_to_client_id": 1,
        "items": [
            {"item_id": 1, "amount": 3}
        ],
    }

    response: requests.Response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=json_body)

    assert response.status_code == 201


def test_post_and_get_order_201(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}orders"
    json_body: dict[str, Any] = {
        "id": 999002,
        "client_id": 1,
        "order_date": "2026-09-29T10:00:00Z",
        "request_date": "2026-10-01T10:00:00Z",
        "reference": "ORD-TEST-002",
        "customer_po_number": "PO-TEST-002",
        "order_status": "Pending",
        "shipping_notes": None,
        "warehouse_id": 1,
        "ship_to_client_id": 1,
        "bill_to_client_id": 1,
        "items": [
            {"item_id": 1, "amount": 2}
        ],
    }

    post_response: requests.Response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert post_response.status_code == 201

    get_response: requests.Response = requests.get(f"{url}/999002", headers={'API_KEY': _data['api_key']})
    assert get_response.status_code == 200
    assert get_response.json()["reference"] == "ORD-TEST-002"
    assert get_response.json()["order_status"] == "Pending"


def test_post_order_wrong_key_403(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}orders"
    json_body: dict[str, Any] = {
        "id": 999099,
        "client_id": 1,
        "reference": "ORD-MAG-NIET",
    }

    response: requests.Response = requests.post(url, headers={'API_KEY': NO_ACCESS_API_KEY}, json=json_body)

    # deze key heeft alleen GET rechten op orders, dus POST hoort geweigerd te worden
    assert response.status_code == 403


# ------------ extra post tests erbij maken mbv feedback jurn---------------------- --------------------------
def test_post_order_same_id_twice_simultaneously_409(_data: dict[str, str]) -> None:
    # Twee gelijktijdige POSTs met hetzelfde ID: exact een mag slagen
    url = _orders_url(_data)
    body = _new_test_order()
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(requests.post, url, headers=_order_headers(_data), json=body, timeout=15) for _ in range(2)]
        responses = [future.result() for future in futures]
    assert sorted(response.status_code for response in responses) == [201, 409]
    response = requests.get(f"{url}/{body['id']}", headers=_order_headers(_data), timeout=15)
    assert response.status_code == 200
    assert sum(order["id"] == body["id"] for order in requests.get(url, headers=_order_headers(_data), timeout=15).json()) == 1


def test_post_orders_different_ids_simultaneously_201(_data: dict[str, str]) -> None:
    # Beide gelijktijdige aanvragen met verschillende IDs moeten worden blijben bewaard blijven 
    url = _orders_url(_data)
    first, second = _new_test_order(), _new_test_order()

    
    while second["id"] == first["id"]:     
        second = _new_test_order()
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(requests.post, url, headers=_order_headers(_data), json=body, timeout=15) for body in (first, second)]
        responses = [future.result() for future in futures]   
    assert all(response.status_code == 201 for response in responses)
    for body in (first, second):
        response = requests.get(f"{url}/{body['id']}", headers=_order_headers(_data), timeout=15)
        assert response.status_code == 200 
        assert response.json()["reference"] == body["reference"]    


def test_post_order_amount_more_than_stock_400(_data: dict[str, str]) -> None:
    # eenextreem grote hoeveelheid mag niet worden geaccept
    body = _new_test_order([{"item_id": 1, "amount": 1000000000}])    

    response = requests.post(_orders_url(_data), headers=_order_headers(_data), json=body, timeout=15)


    assert response.status_code == 400
    assert requests.get(f"{_orders_url(_data)}/{body['id']}", headers=_order_headers(_data), timeout=15).status_code == 404



#------------------------------------------------------------------PUT-------------------------------------------------------------

def test_put_order_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}orders/1"
    json_body: dict[str, Any] = {
        "id": 1, # let op: id moet expliciet mee anders raakt de bestaandeecord z'n id kwijt
        "client_id": 123,
        "order_date": "2025-03-05T04:42:29Z",
        "request_date": "2025-03-09T00:27:04Z",
        "reference": "ORD-000001",
        "customer_po_number": "PO-662159",
        "order_status": "Delivered",
        "shipping_notes": None,
        "warehouse_id": 2,
        "ship_to_client_id": 31,
        "bill_to_client_id": 87,
    }

    response: requests.Response = requests.put(url, headers={'API_KEY': _data['api_key']}, json=json_body)

    assert response.status_code == 200


def test_put_and_get_order_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}orders/1"
    json_body: dict[str, Any] = {
        "id": 1,
        "client_id": 123,
        "order_date": "2025-03-05T04:42:29Z",
        "request_date": "2025-03-09T00:27:04Z",
        "reference": "ORD-000001",
        "customer_po_number": "PO-662159",
        "order_status": "Cancelled",
        "shipping_notes": "Klant heeft geannuleerd via test",
        "warehouse_id": 2,
        "ship_to_client_id": 31,
        "bill_to_client_id": 87,
    }

    put_response: requests.Response = requests.put(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert put_response.status_code == 200

    get_response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert get_response.status_code == 200
    assert get_response.json()["order_status"] == "Cancelled"


def test_put_order_wrong_key_403(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}orders/1"
    json_body: dict[str, Any] = {
        "id": 1,
        "order_status": "Mag niet",
    }

    response: requests.Response = requests.put(url, headers={'API_KEY': NO_ACCESS_API_KEY}, json=json_body)

    assert response.status_code == 403


# ---------------------- EXTRA PUT EDGE CASE TESTS ---------------------------

def test_put_order_not_found_404(_data: dict[str, str]) -> None:
    # PUT op een onbekend order-ID mag geen succesvolle wijziging melden.
    body = _new_test_order()
    response = requests.put(f"{_orders_url(_data)}/{body['id']}", headers=_order_headers(_data), json=body, timeout=15)
    assert response.status_code == 404
    assert requests.get(f"{_orders_url(_data)}/{body['id']}", headers=_order_headers(_data), timeout=15).status_code == 404


def test_put_order_simultaneously_no_lost_data_200(_data: dict[str, str]) -> None:
    # Twee gelijktijdige wijzigingen aan verschillende velden mogen elkaar niet wissen.
    url = _orders_url(_data)
    body = _new_test_order()
    created = requests.post(url, headers=_order_headers(_data), json=body, timeout=15)
    assert created.status_code == 201
    first = body.copy()
    first["order_status"] = "Processing"
    second = body.copy()
    second["shipping_notes"] = "Gelijktijdige testnotitie"
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(requests.put, f"{url}/{body['id']}", headers=_order_headers(_data), json=update, timeout=15) for update in (first, second)]
        responses = [future.result() for future in futures]
    assert all(response.status_code == 200 for response in responses)
    result = requests.get(f"{url}/{body['id']}", headers=_order_headers(_data), timeout=15)
    assert result.status_code == 200
    assert result.json()["order_status"] == "Processing"
    assert result.json()["shipping_notes"] == "Gelijktijdige testnotitie"


#---DELETE-------------------------------------------------------------------------------------------------

def test_delete_order_wrong_key_403(_data: dict[str, str]) -> None:
    # geen enkele api key in user.json heeft delete=True voor orders, dus dit hoort
    # met elke geldige key altijd een 403 te geven, ook met de "hoofd" key van dit bestand.
    url: str = f"http://{_data['host']}{_data['api_path']}orders/1"

    response: requests.Response = requests.delete(url, headers={'API_KEY': _data['api_key']})

    assert response.status_code == 403