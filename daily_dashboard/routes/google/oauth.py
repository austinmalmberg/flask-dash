import functools
import os
import hashlib

from flask import Blueprint, session, url_for, redirect, request, flash
from flask_login import login_required, current_user as current_device, login_user as login_device,\
    logout_user as logout_device

import requests
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request

from daily_dashboard.database.data_access.user import find_user, init_new_user, update_existing_user, remove_tokens
from daily_dashboard.helpers.device_manager import authenticate_device_session, deauthenticate_device,\
    deauthenticate_all_devices, remove_stale_device_sessions
from daily_dashboard.providers.google import GoogleApiEndpoints, build_credentials, get_flow
from daily_dashboard.providers.google.calendars import get_calendar_settings
from daily_dashboard.providers.google.userinfo import request_userinfo

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
            session.pop('token', None)
            remove_tokens(
                current_device.guser,
                refresh_token=not current_device.is_limited_input_device,
                refresh_token_lid=current_device.is_limited_input_device,
            )
            logout_device()
            flash('Invalid token. Please login again')
            return redirect(url_for('main.login'), code=307)

    return wrapped_view


def validate_oauth_token(view):
    """
    Decorator function for maintaining the user's OAuth tokens. Should be present on all methods that use OAuth.

    NOTE: This method assumes current_device is present and not anonymous

    :param view: A view that requires a valid token
    :return: The view if the token is successfully refreshed. Otherwise, an error object
    """

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        refresh_token = current_device.guser.refresh_token_lid if current_device.is_limited_input_device else \
            current_device.guser.refresh_token
        credentials = build_credentials(session.get('token', None), refresh_token)

        if not credentials.valid:
            err = refresh_credentials(credentials, current_device.is_limited_input_device)

            if err:
                # remove tokens and logout device if the credentials could not be refreshed using the refresh token
                session.pop('token', None)
                remove_tokens(
                    current_device.guser,
                    refresh_token=not current_device.is_limited_input_device,
                    refresh_token_lid=current_device.is_limited_input_device,
                )
                logout_device()

                flash(f'{err}. Please login again.', 'error')
                return redirect('main.login', code=307)

        return view(*args, **kwargs)

    return wrapped_view


def refresh_credentials(credentials, is_lid):
    if credentials.refresh_token is None:
        return 'No refresh token'

    try:
        # attempt to refresh token
        credentials.refresh(Request())

        # update session token
        session['token'] = credentials.token

        # update refresh token in database
        kwargs = dict()
        if is_lid:
            kwargs['refresh_token_lid'] = credentials.refresh_token
        else:
            kwargs['refresh_token'] = credentials.refresh_token
        update_existing_user(current_device.guser, **kwargs)

    except RefreshError:
        return 'Token refresh error'

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
        # prompt='consent'
    )

    # redirect request to the authorization url received from the flow
    return redirect(authorization_url)


def create_or_update_authenticated_user(credentials, userinfo):
    # save token only when we have verified there are not errors
    session['token'] = credentials.token

    user = find_user(userinfo['id'])

    if user:
        user = update_existing_user(user, userinfo=userinfo, refresh_token=credentials.refresh_token)
    else:
        settings = get_calendar_settings(credentials)
        user = init_new_user(userinfo, settings, refresh_token=credentials.refresh_token)

    return user


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

        userinfo = request_userinfo(credentials.token)

        error = userinfo.get('error')

        if not error:
            user = create_or_update_authenticated_user(credentials, userinfo)
            remove_stale_device_sessions(user.devices)
            device = authenticate_device_session(user, is_limited_input_device=False)
            login_device(device, remember=True)

    if error:
        flash(error, 'error')

    return redirect(url_for('index'))


def revoke_token(token):
    if token:
        response = requests.post(
            GoogleApiEndpoints.AUTH['oauth_token_revoke'],
            headers={'content-type': 'application/x-www-form-urlencoded'},
            params={'token': token}
        )

        if response.status_code != 200:
            from datetime import datetime
            print(
                datetime.utcnow(),
                'An unhandled Google status code was received on token revoke attempt.',
                response.json()
            )

        return response.status_code == 200

    return False


@bp.route('/logout')
@login_required
def logout():
    # TODO: Deauthorize device

    session.pop('token', None)

    logout_device()

    flash('Logout successful', 'info')

    return redirect(url_for('main.login'))


@bp.route('/revoke')
@login_required
def revoke():
    # TODO: Deauthorize all devices

    revoke_token(session.get('token'))

    session.pop('token', None)
    remove_tokens(current_device.guser, refresh_token=True, refresh_token_lid=True)

    deauthenticate_all_devices(current_device.guser.devices)

    flash('Credentials revoked', 'info')

    return redirect(url_for('main.login'))
