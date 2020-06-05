import os
from datetime import datetime, timedelta

from flask import Blueprint, session, Response, redirect, url_for, flash
from flask_login import login_user

import requests

from routes.google import scopes, GoogleApis
from database import User, db

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
    Used by frontend (index.js) to check when the user authenticates with Google.

    :return:
    """

    # redirect to '/' if no credentials, or credentials expired
    if 'device_credentials' not in session or datetime.utcnow() > session['device_credentials']['valid_until']:
        return redirect(
            location=url_for('index'),
            code=303
        )

    token_response = requests.post(
        GoogleApis.auth['oauth_token'],
        params={
            'client_id': os.environ['GOOGLE_OAUTH2_CLIENT_ID_LIMITED'],
            'client_secret': os.environ['GOOGLE_OAUTH2_CLIENT_SECRET_LIMITED'],
            'code': session['device_credentials']['device_code'],
            'grant_type': 'http://oauth.net/grant_type/device/1.0'
        },
        headers={'content-type': 'application/x-www-form-urlencoded'}
    )

    token_data = token_response.json()

    # user denied access
    if token_response.status_code == 403:
        flash('Code timeout.', 'info')
        session.pop('device_credentials')
        return redirect(
            location=url_for('index'),
            code=303
        )

    # device has not been authenticated through Google yet
    if token_response.status_code == 428:
        return Response(status=202)

    # on other 400+ status code
    if token_response.status_code >= 400:
        flash('There was a problem retrieving your credentials. Please try again.', 'error')
        flash(token_data, 'info')
        return redirect(
            location=url_for('index'),
            code=303
        )

    token = token_data['access_token']
    refresh_token = token_data['refresh_token']

    # make a request for userinfo
    user_response = requests.get(
        url=GoogleApis.user_info,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    )

    user_data = user_response.json()

    if user_response.status_code == 200:

        email = user_data['email']
        name = user_data['name']

        user = User.query.filter_by(email=email).first()

        if user:
            user.name = name
            user.token = token
            user.refresh_token = refresh_token
        else:
            user = User(
                name=name,
                email=email,
                token=token,
                refresh_token=refresh_token
            )

            db.session.add(user)

        db.session.commit()

        login_user(user)

        # redirect to dashboard on creation
        return redirect(
            location=url_for('main.dashboard'),
            code=303
        )

    else:
        flash('There was a problem retreiving your user information. Please try again later.', 'error')
        flash(user_data, 'info')
        return redirect(
            location=url_for('index'),
            code=303
        )
