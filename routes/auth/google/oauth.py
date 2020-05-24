import functools
import os
import hashlib

from flask import Blueprint, session, url_for, redirect, request, flash, g
import requests

from routes.auth.google import flow, api_endpoints
from database import User, db, clear_user_tokens

bp = Blueprint('oauth', __name__)


@bp.route('/authorize')
def authorize():
    """
    The endpoint use authorize the application using OAuth2.0.

    :return:
    """

    session['state'] = hashlib.sha256(os.urandom(1024)).hexdigest()

    flow.redirect_uri = url_for('oauth.oauth2callback', _external=True)

    authorization_url, _state = flow.authorization_url(
        state=session['state'],
        access_type='offline',
        prompt='consent'
    )

    return redirect(authorization_url)


@bp.route('/oauth2callback')
def oauth2callback():
    error = None

    # ensure authorization was provided
    if request.args.get('error'):
        error = 'Authorization denied'

    # ensure states match (to prevent forgery)
    elif request.args.get('state', '') != session['state']:
        error = 'Invalid state'

    if error:
        flash(error, 'error')
    else:
        # use the request url (or more specifically, the params passed in the url)
        # to exchange the authentication code for an access_token
        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials

        # make a request for userinfo
        response = requests.get(
            url=api_endpoints['userinfo'],
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

            session['user_id'] = user.id

            return redirect(url_for('main.dashboard'))

        else:
            error = 'Unable to retrieve user information'
            flash(error, 'error')
            flash(data, 'info')

    return redirect(url_for('index'))


@bp.route('/revoke')
def revoke():
    if g.user and g.user.token:
        response = requests.post(
            api_endpoints['oauth_token_revoke'],
            headers={'content-type': 'application/x-www-form-urlencoded'},
            params={'token': g.user.token}
        )

        token_cleared = clear_user_tokens(g.user.id)
        if token_cleared:
            session.clear()
            flash('Credentials revoked', 'success')

        data = response.json()
        if response.status_code != 200 or data.get('error') != 'invalid_token':
            print(f"An unhandled error ocurred at { url_for('oauth.revoke') }", data)

    return redirect(url_for('index'))


def refresh_token_if_needed(func):
    """
    A decorator for methods that use OAuth tokens.

    Takes a function that returns a response from a 'requests' call. If the response status code is
    401 Unauthorized, this method tries to refresh the token and run the given function again. If
    the token was not refreshed, redirects to '/' to login again.

    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper_func(*args, **kwargs):
        result = func(*args, **kwargs)
        if result.status_code == 401:
            token_refreshed = refresh_token()

            if not token_refreshed:
                flash('Could not refresh your authentication token.  Please login again.')
                return redirect(url_for('index'))

            result = func(*args, **kwargs)

        return result
    return wrapper_func


def refresh_token():
    """
    Attempts to refresh oauth authentication token.  Returns True if the token was refreshed and False otherwise.

    :return: True if the token was refreshed and False otherwise
    """
    response = requests.post(
        api_endpoints['oauth_token'],
        headers={'content-type': 'application/x-www-form-urlencoded'},
        params={
            'client_id': os.environ['GOOGLE_OAUTH2_CLIENT_ID_LIMITED'],
            'client_secret': os.environ['GOOGLE_OAUTH2_CLIENT_SECRET_LIMITED'],
            'grant_type': 'refresh_token',
            'refresh_token': g.user.refresh_token
        }
    )

    data = response.json()

    if response.status_code == 200:
        user = User.query.filter_by(id=g.user.id).first()

        user.token = data['access_token']

        db.session.commit()

        return True

    return False
