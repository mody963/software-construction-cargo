import pytest
import requests
from typing import Any
# gwn voornamelijk clients dingen maar dan omgezet naar shipment behalve b9ijde psot ofc
# zorg dat je zelf de juiste api key invult voor de werkende tests 
# en mocht je een foute key willen hebben qua test let er dan op. 
@pytest.fixture
def _data():
    return {
        'host': 'localhost:3000',
        'api_path': '/api/v1/',
        'api_key': 'r2e4c6e8i0v3i5n7g9s', 
    }


# dzelfde als bij clients om de no permesion ding te testen. 
NO_ACCESS_API_KEY = 'f4a5c6i7l8i9t0y1m2a3n4a5g6'


#------------------------------------------------------GET------
# status_code = response.status_code
def test_get_shipment_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}shipments"

    response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})

    assert response.status_code == 200


def test_get_shipment_401(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}shipments"

    response: requests.Response = requests.get(url, headers={'API_KEY': 'a1b2c3d4e5'})

    assert response.status_code == 401


def test_get_shipment_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}shipments/9999999" # shipment die niet bestaat

    response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})
    print(response.status_code)
    print(response.text)

    assert response.status_code == 404

    # zelfde soort bug als bij clients: dit endpoint geeft momenteel 200 + null terug
    # in plaats van 404, ook al bestaat de shipment niet.


def test_get_shipment_by_id_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}shipments/1" # shipment met id 1 bestaat altijd in de seed data

    response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_shipment_items_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}shipments/1/items"

    response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_shipment_orders_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}shipments/1/orders"

    response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})

    assert response.status_code == 200
    assert isinstance(response.json(), list)


#-----------------------------------------------------POST--------------------------------------------

def test_post_shipment_201(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}shipments"
    json_body: dict[str, Any] = {
        "id": 999001,
        "reference": "SHP-TEST-001",
        "order_id": 1,
        "shipment_date": "2026-09-29T10:00:00Z",
        "shipment_type": "Outgoing",
        "shipment_status": "Pending",
        "carrier_name": "PostNL",
        "shipping_method": "Standard",
        "payment_type": "Automated",
        "items": [
            {"item_id": 1, "amount": 3}
        ],
    }

    response: requests.Response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=json_body)

    assert response.status_code == 201


def test_post_and_get_shipment_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}shipments"
    json_body: dict[str, Any] = {
        "id": 999002,
        "reference": "SHP-TEST-002",
        "order_id": 1,
        "shipment_date": "2026-09-29T10:00:00Z",
        "shipment_type": "Outgoing",
        "shipment_status": "Pending",
        "carrier_name": "PostNL",
        "shipping_method": "Standard",
        "payment_type": "Automated",
        "items": [
            {"item_id": 1, "amount": 2}
        ],
    }

    post_response: requests.Response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert post_response.status_code == 201

    # POST geeft zelf geen body terug, dus moet via de  GET kijken op of dat de shipement wel goed gegaan is verdeerrs
    get_response: requests.Response = requests.get(f"{url}/999002", headers={'API_KEY': _data['api_key']})
    assert get_response.status_code == 200
    assert get_response.json()["reference"] == "SHP-TEST-002"
    assert get_response.json()["shipment_status"] == "Pending"


def test_post_shipment_403(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}shipments"
    json_body: dict[str, Any] = {
        "id": 999099,
        "reference": "SHP-MAG-NIET",
        "order_id": 1,
    }

    response: requests.Response = requests.post(url, headers={'API_KEY': NO_ACCESS_API_KEY}, json=json_body)

    # deze key heeft alleen GET rechten op shipments, dus POST moe geweigerd te worden
    assert response.status_code == 403


#-------------------------------PUT------------------------------------------------------

def test_put_shipment_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}shipments/1"
    json_body: dict[str, Any] = {
        "id": 1, # let op: id moet expliciet mee anders raakt de bestaande record z'n id kwijt
        "reference": "SHP-000001",
        "order_id": 1,
        "shipment_date": "2025-03-05T18:51:53Z",
        "shipment_type": "Outgoing",
        "shipment_status": "Delivered",
        "carrier_name": "GLS",
        "shipping_method": "Standard",
        "payment_type": "Automated",
    }

    response: requests.Response = requests.put(url, headers={'API_KEY': _data['api_key']}, json=json_body)

    assert response.status_code == 200


def test_put_and_get_shipment_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}shipments/1"
    json_body: dict[str, Any] = {
        "id": 1,
        "reference": "SHP-000001",
        "order_id": 1,
        "shipment_date": "2025-03-05T18:51:53Z",
        "shipment_type": "Outgoing",
        "shipment_status": "Cancelled",
        "carrier_name": "DHL",
        "shipping_method": "Express",
        "payment_type": "Automated",
    }

    put_response: requests.Response = requests.put(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert put_response.status_code == 200

    get_response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert get_response.status_code == 200
    assert get_response.json()["shipment_status"] == "Cancelled"
    assert get_response.json()["carrier_name"] == "DHL"


def test_put_shipment_403(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}shipments/1"
    json_body: dict[str, Any] = {
        "id": 1,
        "shipment_status": "Mag niet",
    }

    response: requests.Response = requests.put(url, headers={'API_KEY': NO_ACCESS_API_KEY}, json=json_body)

    assert response.status_code == 403


#-----------------------------------------------------------------------------DELETE---------------------

def test_delete_shipment_403(_data: dict[str, str]) -> None:
    # geen enkele api key in user.json heeft delete=True voor shipments, dus dit hoort
    # met elke geldige key altijd een 403 te geven, ook met de "hoofd" key van dit bestand.
    url: str = f"http://{_data['host']}{_data['api_path']}shipments/1"

    response: requests.Response = requests.delete(url, headers={'API_KEY': _data['api_key']})

    assert response.status_code == 403