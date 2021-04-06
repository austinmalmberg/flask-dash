import os
from datetime import datetime, timedelta

from flask import Blueprint, session, Response, redirect, url_for, flash
from flask_login import login_user

import requests

from daily_dashboard.data_access.devices import create_device
from daily_dashboard.data_access.user import find_user, create_new_user, update_existing_user, remove_stale_devices
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

        # clean up device_credentials from session when the code is consumed
        session.pop('device_credentials', None)

        if response.status_code >= 400 or error == 'access_denied':
            # Occurs on notable status codes, such as:
            # 400, invalid code or grant_type parameters
            # 401, invalid client_id
            # 403, user denied access
            flash('There was a problem authenticating. Please try again', 'error')
            return redirect(url_for('main.login'))

        token = data.get('access_token')
        userinfo = request_userinfo(token)

        error = userinfo.get('error', None)

        if not error:
            session['token'] = token
            session['refresh_token'] = data['refresh_token']

            user = find_user(userinfo['id'])

            if user:
                user = update_existing_user(user, userinfo)
                remove_stale_devices(user)
            else:
                credentials = build_credentials(token, refresh_token=session['refresh_token'])
                settings = get_calendar_settings(credentials)
                user = create_new_user(userinfo, settings)

            # create a new device if the device has not been signed into before
            if 'device_id' not in session:
                device = create_device(user, is_limited_input_device=True)
                session['device_id'] = device.id

            login_user(user, remember=True)

            # redirect to dashboard on creation
            return redirect(
                location=url_for('index'),
                code=303
            )

    else:
        error = 'Access code expired'

    flash(error, 'error')
    return redirect(url_for('main.login'))
