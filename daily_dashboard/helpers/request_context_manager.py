import functools

from flask import session, request, g, Request, flash, redirect
from flask_login import logout_user
from google.auth.exceptions import RefreshError

from daily_dashboard.helpers.location_manager import set_location_from_ip
from daily_dashboard.providers.google import build_credentials


def use_credentials(view):
    """
    Decorator that sets g.credentials variable within the request context.
    """

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        error = None

        if 'refresh_token' in session:
            credentials = build_credentials(session.get('token', None), session['refresh_token'], g.device.is_lid)

            if credentials.valid:
                g.credentials = credentials

            else:
                # attempt to refresh token
                try:
                    credentials.refresh(Request())

                    # update session token
                    session['token'] = credentials.token
                    g.credentials = credentials

                except RefreshError:
                    # pop tokens on error and start over
                    session.pop('token', None)
                    session.pop('refresh_token', None)

                    logout_user()

                    error = 'Token refresh error'

        else:
            error = 'Refresh token not set.'

            session.pop('token', None)

            logout_user()

        if error:
            flash(error, 'error')
            return redirect('main.login', code=307)

        return view(*args, **kwargs)

    return wrapped_view


def use_location(view):
    """
    Decorator that sets g.location variable within the request context.
    """

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        set_location_from_ip(request.remote_addr)

        if 'location_error' in session:
            g.location_error = session['location_error']
        else:
            g.location = dict(
                lat=session['location_lat'],
                lon=session['location_lon'],
                timezone=session['location_timezone']
            )

        return view(*args, **kwargs)

    return wrapped_view
