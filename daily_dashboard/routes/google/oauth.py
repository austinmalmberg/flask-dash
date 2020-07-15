import functools
import os
import hashlib

from flask import Blueprint, session, url_for, redirect, request, flash
from flask_login import logout_user, current_user, login_required, login_user

import requests
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request

from daily_dashboard.database import db
from daily_dashboard.database.queries import find_user, init_new_user, update_existing_user
from daily_dashboard.helpers.google import FLOW, GoogleApiEndpoints, build_credentials
from daily_dashboard.helpers.google.calendars import get_calendar_list, get_calendar_settings
from daily_dashboard.helpers.google.userinfo import get_userinfo

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
        credentials = build_credentials(token=session.get('token', None), refresh_token=current_user.refresh_token)

        if not credentials.valid:

            err = refresh_credentials(credentials)

            if err:
                flash(f'{err}. Please login again.', 'error')
                return redirect(url_for('main.login'), code=303)

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

        db.session.commit()

    except RefreshError:
        session.pop('token', None)
        current_user.refresh_token = None
        db.session.commit()

        return 'Token refresh error'


# ROUTES

@bp.route('/authorize')
def authorize():
    # create a random state variable
    session['state'] = hashlib.sha256(os.urandom(1024)).hexdigest()

    # set the redirect url for the oauth
    FLOW.redirect_uri = url_for('oauth.callback', _external=True)

    # get the authorization url
    authorization_url, _ = FLOW.authorization_url(
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
        FLOW.fetch_token(authorization_response=request.url)

        credentials = FLOW.credentials

        userinfo = get_userinfo(credentials=credentials)

        error = userinfo.get('error')

        if not error:
            user = find_user(userinfo['id'])

            if user is None:
                calendar_list = get_calendar_list(credentials)
                settings = get_calendar_settings(credentials)

                user = init_new_user(userinfo, calendar_list, settings, refresh_token=credentials.refresh_token)
            else:
                user = update_existing_user(user, userinfo=userinfo, refresh_token=credentials.refresh_token)

            login_user(user)

            return redirect(url_for('main.dashboard'))

    flash(error, 'error')
    return redirect(url_for('index'))


@bp.route('/revoke')
@login_required
@validate_oauth_token
def revoke():
    if session.get('token', None):
        response = requests.post(
            GoogleApiEndpoints.AUTH['oauth_token_revoke'],
            headers={'content-type': 'application/x-www-form-urlencoded'},
            params={'token': session.get('token', None)}
        )

        session.pop('token', None)
        current_user.refresh_token = None
        db.session.commit()

        logout_user()

        flash('Credentials revoked', 'info')

        if response.status_code != 200:
            print('An unhandled error occurred on revoke attempt', response.json())

    return redirect(url_for('index'))
