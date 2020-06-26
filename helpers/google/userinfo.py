import requests

from helpers.google import GoogleApis


def get_userinfo(token=None, credentials=None):
    if credentials:
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
