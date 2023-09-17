def test_root_return_200_and_hello_world(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Hello World!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {
        'users': [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'alice.wonderland',
            'email': 'alice@wonderland.com',
            'password': 'rabbit',
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'username': 'alice.wonderland',
        'email': 'alice@wonderland.com',
        'id': 1,
    }


def test_update_invalid_user(client):
    response = client.put(
        '/users/0',
        json={
            'username': 'alice.wonderland',
            'email': 'alice@wonderland.com',
            'password': 'rabbit',
        },
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    user_id = 1
    response = client.delete(f'/users/{user_id}')

    assert response.status_code == 200
    assert response.json() == {'detail': f'User id({user_id}) deleted'}


def test_delete_invalid_user(client):
    response = client.delete('/users/0')

    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}
