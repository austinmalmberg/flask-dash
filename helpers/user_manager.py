from flask import redirect, url_for
from flask_login import LoginManager, current_user

from database import db
from database.models import User, Calendar
from helpers.google.calendars import get_calendar
from helpers.google.userinfo import get_userinfo

login = LoginManager()


def init_app(app):
    # implement flask_login
    login.init_app(app)


@login.user_loader
def load_user(user_id):
    if user_id is None:
        return None

    return User.query.get(user_id)


@login.unauthorized_handler
def handle_unauthorized_user():
    return redirect(url_for('main.login'))


def add_or_update_user(token=None, refresh_token=None, credentials=None):
    """
    Creates a new user by making a request to Google for user info. If the Google id matches any stored in the database,
    updates the existing user.  Otherwise, creates a new user.

    :param token: The OAuth 2.0 token
    :param refresh_token: The refresh token
    :param credentials: google.oauth2.credentials.Credentials. If provided, takes precedence over token and
    refresh_token
    :return: The created/modified User or None if there was a problem retrieving userinfo
    """
    if credentials:
        token = credentials.token
        refresh_token = credentials.refresh_token

    userinfo = get_userinfo(token=token)

    if userinfo.get('error'):
        return None

    google_id = userinfo.get('id')
    email = userinfo.get('email')
    name = userinfo.get('name')

    user = User.query.filter_by(google_id=google_id).first()

    # create or update user
    if user:
        user.google_id=google_id
        user.name = name
        user.email = email
        user.token = token
        user.refresh_token = refresh_token
    else:
        user = User(
            google_id=google_id,
            name=name,
            email=email,
            token=token,
            refresh_token=refresh_token
        )

        db.session.add(user)

    db.session.commit()

    return user


def add_calendar(id):
    """

    :param id: The calendar id
    :return:
    """
    calendar = get_calendar(id)

    if calendar.get('error'):
        return None

    calendar_entry = Calendar(
        user_id=current_user.id,
        calendar_id=calendar.get('id')
    )

    db.session.add(calendar_entry)
    db.session.commit()

    return calendar_entry
