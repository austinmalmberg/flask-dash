import functools

from flask import session, g, flash, redirect
from flask_login import logout_user
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials

from daily_dashboard.providers.google import GoogleApiEndpoints, SCOPES, CLIENT_SECRETS, CLIENT_SECRETS_LIMITED


class AuthenticationMethod:
    DIRECT = 'direct'
    INDIRECT = 'indirect'


def use_credentials(view):
    """
    Decorator.

    Sets the following variables within the request context variable known as g:

    - g.credentials - Google OAuth credentials, most notably containing access and refresh tokens for API calls.

    :param view: A route view
    """

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        error = None

        if 'credentials' in session:
            # set the credentials to be accessed within the view
            g.credentials = build_credentials()

            # the Google OAuth2 library automatically refreshes stale credentials
            # but we still need to catch any RefreshError that might occur.
            # This can happen if the credentials were revoked by the user, or
            # invalidated by Google usage conditions
            try:
                # the RefreshError would be caused within the view, where they are being
                # used by the Google OAuth2 library, should one occur
                v = view(*args, **kwargs)

                # store credentials in the event that they were refreshed
                set_tokens(
                    token=g.credentials.token,
                    refresh_token=g.credentials.refresh_token,
                )

                return v

            except RefreshError:
                remove_credentials()
                error = 'Token refresh error'
        else:
            # credentials are not stored within the session
            logout_user()
            error = 'Credentials do not exist'

        flash(error, 'error')
        return redirect('main.login', code=307)

    return wrapped_view


def set_tokens(**kwargs):
    if 'auth_method' in kwargs:
        session['auth_method'] = kwargs['auth_method']

    # initialize credentials dict if not present
    if 'credentials' not in session:
        session['credentials'] = dict()

    if 'token' in kwargs:
        session['credentials']['token'] = kwargs['token']

    if 'refresh_token' in kwargs:
        session['credentials']['refresh_token'] = kwargs['refresh_token']


def build_credentials():
    if session['auth_method'] == AuthenticationMethod.INDIRECT:
        kwargs = dict(
            client_id=CLIENT_SECRETS_LIMITED['client_id'],
            client_secret=CLIENT_SECRETS_LIMITED['client_secret']
        )
    else:
        kwargs = dict(
            client_id=CLIENT_SECRETS['client_id'],
            client_secret=CLIENT_SECRETS['client_secret']
        )

    return Credentials(
        token_uri=GoogleApiEndpoints.AUTH['token_uri'],
        scopes=SCOPES,
        **session['credentials'],
        **kwargs
    )


def remove_credentials():
    session.pop('credentials', None)
