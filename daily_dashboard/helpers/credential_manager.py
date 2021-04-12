import functools

from flask import session, g, Request, flash, redirect
from flask_login import logout_user
from google.auth.exceptions import RefreshError

from daily_dashboard.providers.google import build_credentials


def use_credentials(view):
    """
    Decorator.

    Sets the following variables within the request context variable known as g:

    - g.credentials - Google OAuth credentials, most notably containing access and refresh tokens for API calls.

    :param view: A route view
    """

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        credentials = None
        error = None

        if 'refresh_token' not in session:
            error = 'Refresh token not set.'
            set_tokens(token=None)
        else:

            token = session.get('token', None)

            credentials = build_credentials(token, session['refresh_token'], g.device.is_lid)

            # attempt to refresh invalid credentials
            if not credentials.valid:
                try:
                    credentials.refresh(Request())

                    # update session token
                    set_tokens(token=credentials.token)

                    # set request variable
                    g.credentials = credentials

                except RefreshError:
                    error = 'Token refresh error'
                    set_tokens(token=None, refresh_token=None)

        if error:
            logout_user()
            flash(error, 'error')
            return redirect('main.login', code=307)

        g.credentials = credentials

        return view(*args, **kwargs)

    return wrapped_view


def set_access_token(token):
    if token is None:
        session.pop('token', None)
    else:
        session['token'] = token


def set_refresh_token(refresh_token):
    if refresh_token is None:
        session.pop('refresh_token', None)
    else:
        session['refresh_token'] = refresh_token


def set_tokens(**kwargs):
    if 'token' in kwargs:
        token = kwargs['token']
        set_access_token(token)

    if 'refresh_token' in kwargs:
        refresh_token = kwargs['refresh_token']
        set_access_token(refresh_token)
