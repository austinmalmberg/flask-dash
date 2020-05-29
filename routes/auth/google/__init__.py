import os
from google_auth_oauthlib.flow import Flow

api_endpoints = {
    # USER INFO -- GET
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
    'userinfo': 'https://www.googleapis.com/userinfo/v2/me',

    # Documentation -- https://developers.google.com/calendar/v3/reference/calendarList/list
    'calendar_list': 'https://www.googleapis.com/calendar/v3/users/me/calendarList',

    # Documentation -- https://developers.google.com/calendar/v3/reference/events/list
    'calendar_events': lambda calendar_id: f'https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events',

    # Documentation -- https://developers.google.com/calendar/v3/reference/colors/get
    'calendar_colors': 'https://www.googleapis.com/calendar/v3/colors',

    # Documentation -- https://developers.google.com/calendar/v3/reference/events/watch
    'calendar_watch': lambda calendar_id: f'https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events/watch',

    # Documentation -- https://developers.google.com/calendar/v3/reference/settings/list
    'calendar_settings': 'https://www.googleapis.com/calendar/v3/users/me/settings',

    # for requesting/refreshing tokens
    'oauth_token': 'https://oauth2.googleapis.com/token',

    # for revoking tokens
    'oauth_token_revoke': 'https://oauth2.googleapis.com/revoke',

    # for authorizing an application from a different device
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