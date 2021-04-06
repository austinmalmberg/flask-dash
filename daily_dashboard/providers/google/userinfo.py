import requests

from daily_dashboard.providers.google import GoogleApiEndpoints


def request_userinfo(token):
    """
    Makes a call to the Google endpoint for user info

    :param token: A Google token
    :return: a JSON reponse containing the user's info
    """

    # TODO: Implement logic to addreess invalid tokens.  This really isn't crucially important at the moment since
    # TODO: this info is requested immediately after getting fresh credentials, but it should still be address for
    # TODO: the sake of completeness

    # make a request for userinfo with the newly received token
    response = requests.get(
        url=GoogleApiEndpoints.USER_INFO,
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    return response.json()
