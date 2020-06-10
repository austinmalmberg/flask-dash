import requests
from flask_login import current_user

from routes.google import GoogleApis


def get_userinfo(token=None, credentials=None):
    if token is None:

        if credentials:
            token = credentials.token
        elif current_user and current_user.token:
            token = current_user.token
        else:
            return {
                'error': 'No token provided'
            }

    # make a request for userinfo with the newly received token
    response = requests.get(
        url=GoogleApis.user_info,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    )

    return response.json()
