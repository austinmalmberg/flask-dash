import functools
import os
import hashlib

from flask import Blueprint, session, url_for, redirect, request, flash
from flask_login import logout_user, current_user, login_required, login_user

import requests
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request

from helpers.user_manager import init_user, init_calendar
from routes.google import flow, GoogleApis
from database import db

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
        return redirect(url_for('index'))

    # use the request url (or more specifically, the params passed in the url)
    # to exchange the authentication code for an access token
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials

    user = init_user(credentials=credentials)
    if user:
        login_user(user)

    init_calendar('primary')


    return redirect(url_for('main.dashboard'))


@bp.route('/revoke')
@login_required
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

        flash('Credentials revoked', 'success')

        if response.status_code != 200:
            print('An unhandled error occurred on revoke attempt', response.json())

    return redirect(url_for('index'))


def validate_oauth_token(view):
    """
    Decorator function for maintaining the user's oauth tokens. Should be present on all methods that use oauth.

    :param view: A view that requires a valid token
    :return: The view if the token is successfully refreshed. Otherwise, an error object
    """

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):

        refresh_attempt = refresh_credentials()

        if refresh_attempt.get('error'):
            return refresh_attempt

        return view(*args, **kwargs)

    return wrapped_view


def refresh_credentials():
    token_refreshed = False
    error = None

    if not current_user or current_user.refresh_token is None:
        error = 'No stored credentials'

    else:
        credentials = current_user.build_credentials()

        if credentials.valid:
            return {
                'message': 'Valid token',
                'token_refreshed': token_refreshed
            }

        if credentials.expired:
            try:
                # attempt to refresh token
                credentials.refresh(Request())

                # update the credentials in the database
                current_user.token = credentials.token
                current_user.refresh_token = credentials.refresh_token
                db.session.commit()

                token_refreshed = True

            except RefreshError:
                current_user.token = None
                current_user.refresh_token = None
                db.session.commit()

        if not token_refreshed:
            error = 'Token refresh error'

    return {
        'token_refreshed': token_refreshed,
        'error': error
    }
