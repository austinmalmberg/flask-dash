import functools
import os
import hashlib
from datetime import timedelta, datetime

from flask import Blueprint, session, url_for, redirect, request, flash
from flask_login import logout_user, current_user, login_required, login_user

import requests
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request

from database.models import User
from helpers.google.userinfo import get_userinfo
from helpers.user_manager import find_user, init_new_user, update_existing_user
from helpers.google import flow, GoogleApis
from database import db

bp = Blueprint('oauth', __name__, url_prefix='/oauth')


def validate_oauth_token(view):
    """
    Decorator function for maintaining the user's OAuth tokens. Should be present on all methods that use OAuth.

    NOTE: This method assumes current_user is present and not anonymous

    :param view: A view that requires a valid token
    :return: The view if the token is successfully refreshed. Otherwise, an error object
    """

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        credentials = current_user.build_credentials()

        if not credentials.valid:
            err = refresh_credentials(credentials)

            if err:
                flash(f'{err}. Please login again.', 'error')
                return redirect(url_for('main.login'))

        return view(*args, **kwargs)

    return wrapped_view


def refresh_credentials(credentials):
    if credentials.refresh_token is None:
        return 'No refresh token'

    try:
        # attempt to refresh token
        credentials.refresh(Request())

        # update the credentials in the database
        current_user.token = credentials.token
        current_user.refresh_token = credentials.refresh_token

        db.session.commit()

        # test that this is updating the database since we're updating the current_user
        user = User.query.get(current_user.id)
        print(f'Token refreshed for {current_user}.')

    except RefreshError:
        current_user.token = None
        current_user.refresh_token = None
        db.session.commit()

        return 'Token refresh error'


# ROUTES

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

    else:
        # use the request url (or more specifically, the params passed in the url)
        # to exchange the authentication code for an access token
        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials

        userinfo = get_userinfo(credentials=credentials)

        error = userinfo.get('error')

        if not error:
            user = find_user(userinfo.get('id'))

            if user is None:
                user = init_new_user(userinfo, credentials=credentials)

            elif user and datetime.utcnow() > user.last_updated + timedelta(days=7):
                # update the existing user's info after 7 days since the last update
                user = update_existing_user(user, userinfo, credentials=credentials)

            login_user(user)

            return redirect(url_for('main.dashboard'))

    flash(error, 'error')
    return redirect(url_for('index'))


@bp.route('/revoke')
@login_required
@validate_oauth_token
def revoke():
    if current_user.token:
        response = requests.post(
            GoogleApis.auth['oauth_token_revoke'],
            headers={'content-type': 'application/x-www-form-urlencoded'},
            params={'token': current_user.token}
        )

        current_user.token = None
        current_user.refresh_token = None
        db.session.commit()

        logout_user()

        flash('Credentials revoked', 'info')

        if response.status_code != 200:
            print('An unhandled error occurred on revoke attempt', response.json())

    return redirect(url_for('index'))
