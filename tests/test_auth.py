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
