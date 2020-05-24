import os
from google_auth_oauthlib.flow import Flow

api_endpoints = {
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
    'userinfo': 'https://www.googleapis.com/oauth2/v2/userinfo',

    'oauth_token': 'https://oauth2.googleapis.com/token',
    'oauth_token_revoke': 'https://oauth2.googleapis.com/revoke',
    'limited_input_device_code': 'https://oauth2.googleapis.com/device/code'
}

client_secrets = {
    'web': {
        'client_id': os.environ['GOOGLE_OAUTH2_CLIENT_ID'],
        'client_secret': os.environ['GOOGLE_OAUTH2_CLIENT_SECRET'],
        'auth_uri': os.environ['GOOGLE_AUTH_URI'],
        'token_uri': os.environ['GOOGLE_TOKEN_URI']
    }
}

scopes = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/calendar.readonly'
]

# used to control the flow of the OAuth2.0 authentication process
flow = Flow.from_client_config(client_secrets, scopes)