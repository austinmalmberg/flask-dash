
def test_login_redirect(client):

    def assert_login_redirect(endpoint):
        response = client.get(f'https://localhost{endpoint}')
        assert response.status_code == 302
        assert response.headers['Location'] == 'https://localhost/login'

    assert_login_redirect('/')
    assert_login_redirect('/settings')
    assert_login_redirect('/oauth/revoke')

    assert_login_redirect('/userinfo')

    assert_login_redirect('/calendars/')
    assert_login_redirect('/calendars/events')
    assert_login_redirect('/calendars/settings')
