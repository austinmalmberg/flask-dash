import functools
import os
import hashlib

from flask import Blueprint, session, url_for, redirect, request, flash
from flask_login import current_user, login_required, login_user, logout_user

import requests
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request

from daily_dashboard.database import db
from daily_dashboard.database.queries import find_user, init_new_user, update_existing_user
from daily_dashboard.helpers.google import GoogleApiEndpoints, build_credentials, get_flow
from daily_dashboard.helpers.google.calendars import get_calendar_settings
from daily_dashboard.helpers.google.userinfo import get_userinfo

bp = Blueprint('oauth', __name__, url_prefix='/oauth')


def handle_refresh_error(view):
    """
    Redirects the user to the login page if the function returns a RefreshError while attempting to refresh an OAuth
    token.

    :param view: A view that uses Google OAuth
    :return: The the function or a redirect to the login page if a RefreshError is thrown
    """
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        try:
            return view(*args, **kwargs)
        except RefreshError:
            return redirect(url_for('main.login'), code=307)

    return wrapped_view


def validate_oauth_token(view):
    """
    Decorator function for maintaining the user's OAuth tokens. Should be present on all methods that use OAuth.

    NOTE: This method assumes current_user is present and not anonymous

    :param view: A view that requires a valid token
    :return: The view if the token is successfully refreshed. Otherwise, an error object
    """

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        credentials = build_credentials(session.get('token', None), current_user.refresh_token)

        if not credentials.valid:
            err = refresh_credentials(credentials)

            if err:
                session.pop('token', None)
                logout_user()

                current_user.refresh_token = None
                db.session.commit()

                flash(f'{err}. Please login again.', 'error')
                redirect('main.login', code=307)

        return view(*args, **kwargs)

    return wrapped_view


def refresh_credentials(credentials):
    if credentials.refresh_token is None:
        return 'No refresh token'

    try:
        # attempt to refresh token
        credentials.refresh(Request())

        # update the credentials in the database
        session['token'] = credentials.token
        current_user.refresh_token = credentials.refresh_token

    except RefreshError:
        session.pop('token', None)
        current_user.refresh_token = None

        return 'Token refresh error'

    finally:
        db.session.commit()

    return None


# ROUTES

@bp.route('/authorize')
def authorize():
    # create a random state variable
    session['state'] = hashlib.sha256(os.urandom(1024)).hexdigest()

    flow = get_flow(url_for('oauth.callback', _external=True))

    # get the authorization url
    authorization_url, _ = flow.authorization_url(
        state=session['state'],
        access_type='offline',
        prompt='consent'
    )

    # redirect request to the authorization url received from the flow
    return redirect(authorization_url)


@bp.route('/callback')
def callback():
    error = None

    # ensure authorization was provided
    if request.args.get('error'):
        error = 'Authorization denied'

    # ensure the state received matches the state set in the initial `/authorize` request (to prevent forgery)
    elif request.args.get('state', '') != session['state']:
        error = 'Invalid state'

    else:
        flow = get_flow(url_for('oauth.callback', _external=True))

        # use the request url (or more specifically, the params passed in the url)
        # to exchange the authentication code for an access token
        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials

        session['token'] = credentials.token

        userinfo = get_userinfo(session['token'])

        error = userinfo.get('error')

        if not error:
            user = find_user(userinfo['id'])

            if user is None:
                settings = get_calendar_settings(credentials)

                user = init_new_user(userinfo, settings, refresh_token=credentials.refresh_token)

            else:
                user = update_existing_user(user, userinfo=userinfo, refresh_token=credentials.refresh_token)

            login_user(user, remember=True)

            return redirect(url_for('main.dashboard'))

    flash(error, 'error')
    return redirect(url_for('index'))


def revoke_token(token):
    print('token:', token)

    if token:
        response = requests.post(
            GoogleApiEndpoints.AUTH['oauth_token_revoke'],
            headers={'content-type': 'application/x-www-form-urlencoded'},
            params={'token': token}
        )

        print('response:', response.status_code)

        if response.status_code != 200:
            print('An unhandled error occurred on revoke attempt', response.json())

        return response.status_code == 200

    return False


@bp.route('/logout')
@login_required
def logout():
    # TODO: Deauthorize device

    revoke_token(session.get('token'))

    print('token after logout:', session.get('token'))

    session.pop('token', None)
    logout_user()

    flash('Logout successful', 'info')

    return redirect(url_for('main.login'))


@bp.route('/revoke')
@login_required
def revoke():
    # TODO: Deauthorize all devices

    revoke_token(session.get('token'))

    print('token after revoking:', session.get('token'))

    session.pop('token', None)
    logout_user()

    current_user.refresh_token = None
    db.session.commit()

    flash('Credentials revoked', 'info')

    return redirect(url_for('main.login'))
