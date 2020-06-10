import os

from google_auth_oauthlib.flow import Flow


class GoogleApis:
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
    user_info = 'https://www.googleapis.com/userinfo/v2/me'

    auth = {
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


client_secrets = {
    'client_id': os.environ['GOOGLE_OAUTH2_CLIENT_ID'],
    'client_secret': os.environ['GOOGLE_OAUTH2_CLIENT_SECRET'],
    'auth_uri': GoogleApis.auth['auth_uri'],
    'token_uri': GoogleApis.auth['token_uri']
}

scopes = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/calendar.readonly'
]

# used to control the flow of the OAuth2.0 authentication process
flow = Flow.from_client_config({
    'web': client_secrets
}, scopes)


def register_blueprints(app):
    # Endpoints to authenticate the user from the same device
    from routes.google import oauth
    app.register_blueprint(oauth.bp)

    # Endpoints to authenticate the user from devices without peripherals
    from routes.google import oauth_limited_input_device
    app.register_blueprint(oauth_limited_input_device.bp)

    # Endpoints for getting calendar JSON data
    from routes.google import calendars
    app.register_blueprint(calendars.bp)

