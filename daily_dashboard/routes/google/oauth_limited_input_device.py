import os
from datetime import datetime, timedelta

from flask import Blueprint, session, Response, redirect, url_for, flash
from flask_login import login_user as login_device

import requests

from daily_dashboard.database.data_access.user import find_user, init_new_user, update_existing_user
from daily_dashboard.helpers.device_manager import authenticate_device_session, remove_stale_device_sessions
from daily_dashboard.providers.google import SCOPES, GoogleApiEndpoints, build_credentials
from daily_dashboard.providers.google.calendars import get_calendar_settings
from daily_dashboard.providers.google.userinfo import request_userinfo

bp = Blueprint('oauth_lid', __name__)


def create_device_credentials():
    response = requests.post(
        GoogleApiEndpoints.AUTH['limited_input_device_code'],
        params={
            'client_id': os.environ['GOOGLE_OAUTH2_CLIENT_ID_LIMITED'],
            'scope': ' '.join(SCOPES)
        },
        headers={'content-type': 'application/x-www-form-urlencoded'}
    )

    if response.status_code == 200:
        device_credentials = response.json()
        device_credentials['valid_until'] = datetime.utcnow() + timedelta(seconds=device_credentials['expires_in'])

        return device_credentials


def create_or_update_authenticated_user(token, refresh_token, userinfo):
    # store tokens only when we have verified it works (by testing getting the userinfo)
    session['token'] = token
    user = find_user(userinfo.get('id'))

    if user:
        user = update_existing_user(user, userinfo, refresh_token=refresh_token, is_limited_input_device=True)
    else:
        credentials = build_credentials(token=session['token'], refresh_token=refresh_token)
        settings = get_calendar_settings(credentials)
        user = init_new_user(userinfo, settings, refresh_token=refresh_token, is_limited_input_device=True)

    return user


@bp.route('/poll', methods=('GET',))
def poll():
    """
    Used by frontend script to check when the user authenticates with Google.

    :return:
    """

    error = None

    if 'device_credentials' in session and datetime.utcnow() < session['device_credentials']['valid_until']:
        # make a request to google for tokens
        response = requests.post(
            GoogleApiEndpoints.AUTH['oauth_token'],
            params={
                'client_id': os.environ['GOOGLE_OAUTH2_CLIENT_ID_LIMITED'],
                'client_secret': os.environ['GOOGLE_OAUTH2_CLIENT_SECRET_LIMITED'],
                'code': session['device_credentials']['device_code'],
                'grant_type': 'http://oauth.net/grant_type/device/1.0'
            },
            headers={'content-type': 'application/x-www-form-urlencoded'}
        )

        data = response.json()

        error = data.get('error', None)

        if response.status_code == 428:
            # error == 'authorization_pending'
            # user has not completed the authorization flow
            return Response(status=202)
        if response.status_code == 403:
            # error == 'slow_down'
            # polling too quickly
            return Response(status=202)

        # remove device_credentials from session when the code is consumed
        session.pop('device_credentials')

        if response.status_code >= 400 or error == 'access_denied':
            # Occurs on notable status codes, such as:
            # 400, invalid code or grant_type parameters
            # 401, invalid client_id
            # 403, user denied access
            flash('There was a problem authenticating. Please try again', 'error')
            return redirect(url_for('main.login'))

        userinfo = request_userinfo(token=data.get('access_token'))

        error = userinfo.get('error')

        if not error:
            user = create_or_update_authenticated_user(data.get('access_token'), data.get('refresh_token'), userinfo)
            remove_stale_device_sessions(user)
            device = authenticate_device_session(user, is_limited_input_device=True)
            login_device(device, remember=True)

            # redirect to dashboard on creation
            return redirect(
                location=url_for('index'),
                code=303
            )

    else:
        error = 'Credentials expired'

    flash(error, 'error')
    return redirect(url_for('main.login'))
