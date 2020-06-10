import os
from datetime import datetime, timedelta

from flask import Blueprint, session, Response, redirect, url_for
from flask_login import login_user

import requests

from helpers.user_manager import add_or_update_user, add_calendar
from routes.google import scopes, GoogleApis

bp = Blueprint('oauth_lid', __name__)


def create_device_credentials():
    response = requests.post(
        GoogleApis.auth['limited_input_device_code'],
        params={
            'client_id': os.environ['GOOGLE_OAUTH2_CLIENT_ID_LIMITED'],
            'scope': ' '.join(scopes)
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

    # redirect to '/' if no credentials, or credentials expired
    if 'device_credentials' not in session or datetime.utcnow() > session['device_credentials']['valid_until']:
        return redirect(
            location=url_for('index'),
            code=303
        )

    response = requests.post(
        GoogleApis.auth['oauth_token'],
        params={
            'client_id': os.environ['GOOGLE_OAUTH2_CLIENT_ID_LIMITED'],
            'client_secret': os.environ['GOOGLE_OAUTH2_CLIENT_SECRET_LIMITED'],
            'code': session['device_credentials']['device_code'],
            'grant_type': 'http://oauth.net/grant_type/device/1.0'
        },
        headers={'content-type': 'application/x-www-form-urlencoded'}
    )

    data = response.json()

    error = data.get('error')

    if error == 'authorization_pending':
        # status 428, user has not completed the authorization flow
        return Response(status=202)
    if error == 'slow_down':
        # status 403, polling too quickly
        return Response(status=202)
    elif error == 'access_denied' or response.status_code > 400:
        # Occurs on notable status codes
        # 400, invalid code or grant_type parameters
        # 401, invalid client_id
        # 403, user denied access
        session.pop('device_credentials')
        return redirect(
            location=url_for('index'),
            code=303
        )

    token = data.get('access_token')
    refresh_token = data.get('refresh_token')

    user = add_or_update_user(token=token, refresh_token=refresh_token)
    if user:
        login_user(user)

        credentials = user.build_credentials()
        add_calendar(credentials, 'primary')

    # redirect to dashboard on creation
    return redirect(
        location=url_for('main.dashboard'),
        code=303
    )
