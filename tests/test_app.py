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


def test_update_user(client, user, token):
    headers = {'Authorization': f'Bearer {token}'}

    response = client.put(
        f'/users/{user.id}',
        headers=headers,
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


def test_update_forbidden_user(client, user_alice, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = client.put(
        f'/users/{user_alice.id}',
        headers=headers,
        json={
            'username': 'alice.wonderland',
            'email': 'alice@wonderland.com',
            'password': 'rabbit',
        },
    )

    assert response.status_code == 403
    assert response.json() == {'detail': 'Not enough permission'}


def test_delete_user(client, user, token):
    user_id = user.id
    headers = {'Authorization': f'Bearer {token}'}
    response = client.delete(f'/users/{user_id}', headers=headers)

    assert response.status_code == 200
    assert response.json() == {'detail': f'User id({user_id}) deleted'}


def test_delete_forbidden_user(client, user_alice, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = client.delete(f'/users/{user_alice.id}', headers=headers)

    assert response.status_code == 403
    assert response.json() == {'detail': 'Not enough permission'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_email_invalid(client):
    response = client.post(
        '/token',
        data={'username': 'alice@wonderland.com', 'password': 'rabbit'},
    )
    body = response.json()

    assert response.status_code == 400
    assert body.get('detail') == 'Incorrect email or password'


def test_get_token_password_invalid(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': 'rabbit'},
    )
    body = response.json()

    assert response.status_code == 400
    assert body.get('detail') == 'Incorrect email or password'
