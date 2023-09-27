from fast_zero.schemas import UserPublic


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


def test_create_user_already_exist(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == 400


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_read_user_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        f'/users/{user.id}',
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


def test_delete_user(client, user):
    user_id = user.id
    response = client.delete(f'/users/{user_id}')

    assert response.status_code == 200
    assert response.json() == {'detail': f'User id({user_id}) deleted'}


def test_delete_invalid_user(client):
    response = client.delete('/users/0')

    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}
