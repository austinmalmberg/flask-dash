import pytest


@pytest.mark.parametrize('endpoint',
    ['/', '/settings', '/oauth/revoke', '/calendars/', '/calendars/events', '/calendars/settings'])
def test_redirect_to_login(client, endpoint):
    response = client.get(f'https://localhost{endpoint}')
    assert response.status_code == 307
    assert response.headers['Location'] == 'https://localhost/login'


def test_login_revoke(client):
    # TODO: login user

    # TODO: revoke token and logout

    # TODO: login with limited input device
    login_response = client.get('/login')
    print(login_response.headers)

    assert 0


def test_login(client):
    response = client.get('/oauth/authorize')


def login_limited_input_device(client):
    response = client.get('/login')


def revoke(client):
    return client.get('/oauth/revoke')
