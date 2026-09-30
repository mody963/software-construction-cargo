import pytest
import requests
from typing import Any  # omdat ik nog een oude versie heb werkt de any niet maar dat is nodig voor de typehinting
# zorg dat je zelf de juiste api key invult voor de werkende tests 
# en mocht je een foute key willen hebben qua test let er dan op. 
@pytest.fixture
def _data():
    return {
        'host': 'localhost:3000', # hierdoor kan je als er een andere host is er makkelijker een verandering in maken
        'api_path': '/api/v1/',
        'api_key': 'f4a5c6i7l8i9t0y1m2a3n4a5g6',
    }

# facility_management heeft alle rechten op clients, receiving_station alleen GET.
# Die tweede key om de 403 (geen rechten) tests mee te doen.
NO_ACCESS_API_KEY = 'r2e4c6e8i0v3i5n7g9s'

# -------------------------------------------------------GET--------------------------------------------------------------------------------------------------

def test_get_clients_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}clients"

    # Send a GET request to the API
    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200


def test_get_clients_wrong_api_key_401(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}clients"

    # Send a GET request to the API with an incorrect API key
    response: requests.Response = requests.get(
        url,
        headers={'API_KEY': 'a1b2c3d4e5'}
    )
    # Get the status code
    status_code: int = response.status_code

    # Verify that the status code is 401
    assert status_code == 401


def test_get_client_invalid_id_integer_not_found_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}clients/999999" # Ik vraag een client op die niet bestaat.

    response: requests.Response = requests.get(
        url,
        headers={'API_KEY': _data['api_key']}
    )
    print(response.status_code)
    print(response.text)

    assert response.status_code == 404

    # deze geeft momenteel geen 404 mee maar alsnog een 200 maar dan samen met null zelfs al werkt de endpoint zelf niet omdat het niet bestaand is.
    # het zoekt dus nogsteeds naar de client maar geeft gewoon geen juiste waardes terug mee. 

def test_get_client_invalid_id_string_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}clients/abcdef" # Ik vraag een client op die niet bestaat.

    response: requests.Response = requests.get(
        url,
        headers={'API_KEY': _data['api_key']}
    )
    print(response.status_code)
    print(response.text)

    assert response.status_code == 404

    # deze geeft momenteel geen 404 maar een 500 dit is omdat het namelijkbij de do get niet door de try heen komt 
    # omdat het daarna bij client get met id de melding heeft dat het geen id op int kan vinden en dus meteen een 500 returned uit het exept blok

def test_get_client_invalid_id_string_integer_non_alphanumeric_not_found_404(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}clients/ABC6d1Xyz$" # Ik vraag een client op die niet bestaat.

    response: requests.Response = requests.get(
        url,
        headers={'API_KEY': _data['api_key']}
    )
    print(response.status_code)
    print(response.text)

    assert response.status_code == 404

    # zelfde als bij test_get_client_invalid_id_string_404


def test_delete_clients_collection_not_allowed_405(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}clients"

    response: requests.Response = requests.delete(
        url,
        headers={'API_KEY': _data['api_key']}
    ) # DELETE is niet toegestaan op dit endpoint

    assert response.status_code == 405

def test_get_client_by_id_200(_data: dict[str, str]) -> None:
    # client met id 1 bestaat altijd in de seed data (sinds er nog niks verwijderd kan worden ofc)
    url: str = f"http://{_data['host']}{_data['api_path']}clients/1" 

    response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_client_orders_200(_data: dict[str, str]) -> None:
    # sub-resource: /clients/<id>/orders
    url: str = f"http://{_data['host']}{_data['api_path']}clients/1/orders"

    response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})

    assert response.status_code == 200
    assert isinstance(response.json(), list)


#-----------------------------------------------------------POST-------------------------------------------------------------------------

def test_post_client_201(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}clients"
    json_body: dict[str, Any] = {
        "id": 999001,
        "name": "Test Klant BV",
        "address": "Teststraat 1",
        "city": "Rotterdam",
        "zip_code": "3011AB",
        "province": "Zuid-Holland",
        "country": "Netherlands",
        "contact_name": "Test Persoon",
        "contact_phone": "010-1234567",
        "contact_email": "test.klant@example.com",
    }

    response: requests.Response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=json_body)

    assert response.status_code == 201


def test_post_and_get_client_201(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}clients"
    json_body: dict[str, Any] = {
        "id": 999002,
        "name": "Test Klant Post-Get BV",
        "address": "Teststraat 2",
        "city": "Rotterdam",
        "zip_code": "3011AC",
        "province": "Zuid-Holland",
        "country": "Netherlands",
        "contact_name": "Test Persoon 2",
        "contact_phone": "010-7654321",
        "contact_email": "test.klant2@example.com",
    }

    post_response: requests.Response = requests.post(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert post_response.status_code == 201

    # de POST endpoint geeft zelf geen body terug dus check via een losse GET of de client goed is aangemaakt
    get_response: requests.Response = requests.get(f"{url}/999002", headers={'API_KEY': _data['api_key']})
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test Klant Post-Get BV"
    assert get_response.json()["city"] == "Rotterdam"


def test_post_client_wrong_key_403(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}clients"
    json_body: dict[str, Any] = {
        "id": 999099,
        "name": "Mag Niet Aangemaakt Worden BV",
        "address": "Teststraat 99",
        "city": "Rotterdam",
        "zip_code": "3011ZZ",
        "province": "Zuid-Holland",
        "country": "Netherlands",
        "contact_name": "Niemand",
        "contact_phone": "010-0000000",
        "contact_email": "niemand@example.com",
    }

    response: requests.Response = requests.post(url, headers={'API_KEY': NO_ACCESS_API_KEY}, json=json_body)

    # deze key heeft alleen GET rechten op clients de post moet eig geweiged worden en dus de 403
    assert response.status_code == 403


#------------------------------------------------------------PUT-------------------------------

def test_put_client_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}clients/1"
    json_body: dict[str, Any] = {
        "id": 1, # let op: het id moet expliciet mee anders raakt de bestaande record z'n id kwijt
        "name": "Jumbo Amersfoort Leusderweg",
        "address": "Leusderweg 152",
        "city": "Amersfoort",
        "zip_code": "9704WL",
        "province": "Drenthe",
        "country": "Netherlands",
        "contact_name": "Test Persoon Put",
        "contact_phone": "020-1112223",
        "contact_email": "put.test@example.com",
    }

    response: requests.Response = requests.put(url, headers={'API_KEY': _data['api_key']}, json=json_body)

    assert response.status_code == 200


def test_put_and_get_client_200(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}clients/1"
    json_body: dict[str, Any] = {
        "id": 1,
        "name": "Jumbo Amersfoort Leusderweg",
        "address": "Aangepaste Straat 123",
        "city": "Amersfoort",
        "zip_code": "9704WL",
        "province": "Drenthe",
        "country": "Netherlands",
        "contact_name": "Test Persoon Put",
        "contact_phone": "020-1112223",
        "contact_email": "put.test@example.com",
    }

    put_response: requests.Response = requests.put(url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert put_response.status_code == 200

    get_response: requests.Response = requests.get(url, headers={'API_KEY': _data['api_key']})
    assert get_response.status_code == 200
    assert get_response.json()["address"] == "Aangepaste Straat 123"


def test_put_client_wrong_key_403(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}clients/1"
    json_body: dict[str, Any] = {
        "id": 1,
        "name": "Mag niet aangepast worden",
    }

    response: requests.Response = requests.put(url, headers={'API_KEY': NO_ACCESS_API_KEY}, json=json_body)

    assert response.status_code == 403


#----------------------------------------DELETE-----------------------------------------------------------------------------------------------------

def test_delete_client_200(_data: dict[str, str]) -> None:
    create_url: str = f"http://{_data['host']}{_data['api_path']}clients"
    json_body: dict[str, Any] = {
        "id": 999003,
        "name": "Te Verwijderen Klant BV",
        "address": "Teststraat 3",
        "city": "Rotterdam",
        "zip_code": "3011AD",
        "province": "Zuid-Holland",
        "country": "Netherlands",
        "contact_name": "Weg Ermee",
        "contact_phone": "010-1111111",
        "contact_email": "delete.test@example.com",
    }
    post_response: requests.Response = requests.post(create_url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert post_response.status_code == 201

    delete_url: str = f"{create_url}/999003"
    delete_response: requests.Response = requests.delete(delete_url, headers={'API_KEY': _data['api_key']})

    assert delete_response.status_code == 200


def test_delete_and_get_client_404(_data: dict[str, str]) -> None:
    create_url: str = f"http://{_data['host']}{_data['api_path']}clients"
    json_body: dict[str, Any] = {
        "id": 999004,
        "name": "Te Verwijderen En Op Te Vragen Klant BV",
        "address": "Teststraat 4",
        "city": "Rotterdam",
        "zip_code": "3011AE",
        "province": "Zuid-Holland",
        "country": "Netherlands",
        "contact_name": "Ook Weg Ermee",
        "contact_phone": "010-2222222",
        "contact_email": "delete.get.test@example.com",
    }
    post_response: requests.Response = requests.post(create_url, headers={'API_KEY': _data['api_key']}, json=json_body)
    assert post_response.status_code == 201

    delete_url: str = f"{create_url}/999004"
    delete_response: requests.Response = requests.delete(delete_url, headers={'API_KEY': _data['api_key']})
    assert delete_response.status_code == 200

    get_response: requests.Response = requests.get(delete_url, headers={'API_KEY': _data['api_key']})
    assert get_response.status_code == 404

    # zelfde soort bug als test_get_client_404: momenteel komt hier nog een 200 + null terug
    # in plaats van een 404, omdat er geen None-check zit na het weghalen van de client.


def test_delete_client_wrong_key_403(_data: dict[str, str]) -> None:
    url: str = f"http://{_data['host']}{_data['api_path']}clients/1"

    response: requests.Response = requests.delete(url, headers={'API_KEY': NO_ACCESS_API_KEY})

    assert response.status_code == 403

