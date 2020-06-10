import requests

from routes.google import GoogleApis


def get_userinfo(token=None, credentials=None):
    if token is None and credentials:
        token = credentials.token

    # make a request for userinfo with the newly received token
    response = requests.get(
        url=GoogleApis.user_info,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    )

    return response.json()
