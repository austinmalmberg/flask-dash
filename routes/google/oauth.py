import functools
import os
import hashlib

from flask import Blueprint, session, url_for, redirect, request, flash
from flask_login import login_user, logout_user, current_user, login_required

import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from routes.google import flow, client_secrets, scopes, GoogleApis
from database import User, db

bp = Blueprint('oauth', __name__, url_prefix='/oauth')


@bp.route('/authorize')
def authorize():
    # create a random state variable
    session['state'] = hashlib.sha256(os.urandom(1024)).hexdigest()

    # set the redirect url for the oauth
    flow.redirect_uri = url_for('oauth.callback', _external=True)

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

    if error:
        flash(error, 'error')
    else:
        # use the request url (or more specifically, the params passed in the url)
        # to exchange the authentication code for an access token
        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials

        # make a request for userinfo with the newly received token
        response = requests.get(
            url=GoogleApis.user_info,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {credentials.token}'
            }
        )

        data = response.json()

        # store userinfo on successful response
        if response.status_code == 200:
            name = data['name']
            email = data['email']

            user = User.query.filter_by(email=email).first()

            if user:
                user.name = name
                user.token = credentials.token
                user.refresh_token = credentials.refresh_token
            else:
                user = User(
                    name=name,
                    email=email,
                    token=credentials.token,
                    refresh_token=credentials.refresh_token
                )

                db.session.add(user)

            db.session.commit()

            login_user(user)

            return redirect(url_for('main.dashboard'))

        else:
            error = 'Unable to retrieve user information'
            flash(error, 'error')
            flash(data, 'info')

    return redirect(url_for('index'))


@bp.route('/revoke')
@login_required
def revoke():
    if current_user.token is not None:
        response = requests.post(
            GoogleApis.auth['oauth_token_revoke'],
            headers={'content-type': 'application/x-www-form-urlencoded'},
            params={'token': current_user.token}
        )

        data = response.json()

        current_user.token = None
        current_user.refresh_token = None

        db.session.commit()

        logout_user()

        flash('Credentials revoked', 'success')

        if response.status_code != 200:
            print('An unhandled error occurred on revoke attempt', data)

    return redirect(url_for('index'))


def validate_oauth_token(func):
    """
    Decorator function for maintaining the user's oauth tokens. Should be present on all methods that use oauth.

    :param func:
    :return:
    """

    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):

        # manually build credentials
        credentials = Credentials(
            token=current_user.token,
            refresh_token=current_user.refresh_token,
            token_uri=GoogleApis.auth['token_uri'],
            client_id=client_secrets['web']['client_id'],
            client_secret=client_secrets['web']['client_secret'],
            scopes=scopes
        )

        # on invalid credentials:
        if not credentials.valid:
            # attempt to refresh expired credentials
            if credentials.expired and credentials.refresh_token:
                try:
                    credentials.refresh(Request())

                    current_user.token = credentials.token
                    current_user.refresh_token = credentials.refresh_token

                    db.session.commit()
                except Exception as e:
                    return {
                        'message': 'Unable to refresh your token. Please login again.',
                        'error': e
                    }

            return {
                'message': 'Your credentials are no longer valid. Please login again.',
                'error': 'Invalid credentials'
            }

        return func(*args, **kwargs)

    return wrapped_func
