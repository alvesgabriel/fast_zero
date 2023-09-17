from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_return_200_and_hello_world():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Hello World!'}
