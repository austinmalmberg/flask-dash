import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow


class GoogleApiEndpoints:
    # GET returns the JSON object as follows:
    # {
    #   "id": <number string>,
    #   "email": <string>,
    #   "verified_email": <boolean>,
    #   "name": <string>,
    #   "given_name": <string>,
    #   "family_name": <string>,
    #   "picture": <url>
    #   "locale": "en"
    # }
    USER_INFO = 'https://www.googleapis.com/oauth2/v2/userinfo'

    AUTH = {
        # used in client secrets
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://oauth2.googleapis.com/token',

        # for requesting/refreshing tokens
        'oauth_token': 'https://oauth2.googleapis.com/token',

        # for revoking tokens
        'oauth_token_revoke': 'https://oauth2.googleapis.com/revoke',

        # for authorizing an application from a different device
        'limited_input_device_code': 'https://oauth2.googleapis.com/device/code',
    }


CLIENT_SECRETS = {
    'client_id': os.environ['GOOGLE_OAUTH2_CLIENT_ID'],
    'client_secret': os.environ['GOOGLE_OAUTH2_CLIENT_SECRET'],
    'auth_uri': GoogleApiEndpoints.AUTH['auth_uri'],
    'token_uri': GoogleApiEndpoints.AUTH['token_uri']
}

SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/calendar.readonly'
]

# used to control the flow of the OAuth2.0 authentication process
FLOW = Flow.from_client_config({
    'web': CLIENT_SECRETS
}, SCOPES)


def build_credentials(token=None, refresh_token=None):
    return Credentials(
        token=token,
        refresh_token=refresh_token,
        token_uri=GoogleApiEndpoints.AUTH['token_uri'],
        client_id=CLIENT_SECRETS['client_id'],
        client_secret=CLIENT_SECRETS['client_secret'],
        scopes=SCOPES
    )
