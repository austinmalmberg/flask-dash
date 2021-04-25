import os
import hashlib

from flask import Blueprint, session, url_for, redirect, request, flash, g
from flask_login import login_required, current_user, login_user, logout_user

import requests
from google_auth_oauthlib.flow import Flow

from daily_dashboard.data_access.devices import create_or_update_device
from daily_dashboard.data_access.user import find_user_by_google_id, create_new_user, update_existing_user, \
    remove_stale_devices, remove_devices
from daily_dashboard.helpers.credential_manager import set_tokens, use_credentials, AuthenticationMethod, \
    remove_credentials
from daily_dashboard.providers.google import GoogleApiEndpoints, CLIENT_SECRETS, SCOPES
from daily_dashboard.providers.google.calendars import get_calendar_settings
from daily_dashboard.providers.google.userinfo import request_userinfo

bp = Blueprint('oauth', __name__, url_prefix='/oauth')


@bp.route('/authorize')
def authorize():
    # create a random state variable
    session['oauth_state'] = hashlib.sha256(os.urandom(1024)).hexdigest()

    flow = Flow.from_client_config(
        {'web': CLIENT_SECRETS},
        SCOPES,
        redirect_uri=url_for('oauth.callback', _external=True)
    )

    # get the authorization url
    authorization_url, _ = flow.authorization_url(
        state=session['oauth_state'],
        access_type='offline'
    )

    # redirect request to the authorization url received from the flow
    return redirect(authorization_url)


@bp.route('/callback')
def callback():
    userinfo = None

    # ensure authorization was provided
    if request.args.get('error'):
        error = 'Authorization denied'

    # ensure the state received matches the state set in the initial `/authorize` request (to prevent forgery)
    elif request.args.get('state', '') != session['oauth_state']:
        error = 'Invalid state'

    else:
        # remove no longer required session variables
        session.pop('oauth_state', None)
        session.pop('device_credentials', None)

        flow = Flow.from_client_config(
            {'web': CLIENT_SECRETS},
            SCOPES,
            redirect_uri=url_for('oauth.callback', _external=True)
        )

        # use the request url (or more specifically, the params passed in the url)
        # to exchange the authentication code for an access token
        flow.fetch_token(authorization_response=request.url)

        g.credentials = flow.credentials

        set_tokens(
            auth_method=AuthenticationMethod.DIRECT,
            token=g.credentials.token,
            refresh_token=g.credentials.refresh_token
        )

        userinfo = request_userinfo(g.credentials.token)

        error = userinfo.get('error', None)

    if error:
        flash(error, 'error')
        return redirect(url_for('main.login'))

    user = find_user_by_google_id(userinfo['id'])

    # create or update existing user
    if user:
        user = update_existing_user(user, userinfo)
        remove_stale_devices(user)
    else:
        settings = get_calendar_settings(g.credentials)
        user = create_new_user(userinfo, settings)

    device = create_or_update_device(user, is_lid=False, device_id=session.get('device_id', None))
    session['device_id'] = device.id

    login_user(user, remember=True)

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
    set_tokens(token=None)

    logout_user()

    flash('Logout successful', 'info')

    return redirect(url_for('main.login'))


@bp.route('/revoke')
@login_required
@use_credentials
def revoke():
    revoke_token(g.credentials.token)

    # clear tokens
    remove_credentials()

    remove_devices(current_user)

    logout_user()

    flash('Credentials revoked', 'info')

    return redirect(url_for('main.login'))
