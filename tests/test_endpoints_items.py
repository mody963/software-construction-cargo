import pytest
import requests

# zorg dat je zelf de juiste api key invult voor de werkende tests 
# en mocht je een foute key willen hebben qua test let er dan op. 
@pytest.fixture
def _data():
    return {
        'url': 'http://localhost:3000/api/v1/',
        'api_key': 'a1b2c3d4e5',
    }



def test_get_item(_data):
    url = _data['url'] + 'items'

    # Send a GET request to the API
    response = requests.get(url, headers={'API_KEY': _data['api_key']})

    # Get the status code and response data
    status_code = response.status_code

    # Verify that the status code is 200 (OK)
    assert status_code == 200
