import pytest
import requests

# zorg dat je zelf de juiste api key invult voor de werkende tests 
# en mocht je een foute key willen hebben qua test let er dan op. 
@pytest.fixture
def _data():
    return {
        'host': 'localhost:3000', # hierdoor kan je als er een andere host is er makkelijker een verandering in maken
        'api_path': '/api/v1/',
        'api_key': 'f4a5c6i7l8i9t0y1m2a3n4a5g6',
    }



def test_get_client_200(_data: dict[str,str]):
    url: str = f"http://{_data['host']}{_data['api_path']}clients"

    # Send a GET request to the API
    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200


def test_get_client_401(_data: dict[str, str]) -> None:
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


def test_get_client_404(_data: dict[str, str]) -> None:
    url: str = f"{_data['base_url']}clients/999999" # hierbij heb je dus een compleet verkeerd pad

    response: requests.Response = requests.get(
        url,
        headers={'API_KEY': _data['api_key']}
    )

    assert response.status_code == 404


def test_get_client_405(_data: dict[str, str]) -> None:
    url: str = f"{_data['base_url']}clients"

    response: requests.Response = requests.delete(
        url,
        headers={'API_KEY': _data['api_key']}
    ) # je kan geen delete gebruiken op deze edpoint

    assert response.status_code == 405