import requests

from daily_dashboard.helpers.google import GoogleApiEndpoints


def get_userinfo(token=None, credentials=None):
    if credentials:
        token = credentials.token

    # make a request for userinfo with the newly received token
    response = requests.get(
        url=GoogleApiEndpoints.USER_INFO,
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    return response.json()
