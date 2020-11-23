from datetime import datetime

from daily_dashboard.database import db
from daily_dashboard.database.models import User


def find_user(google_id):
    if google_id is None:
        raise ValueError('google_id cannot be None')

    return User.query.filter_by(google_id=google_id).first()


def init_new_user(userinfo, settings, refresh_token=None):
    """
    Creates a new user in the database.

    :param userinfo: userinfo from Google
    :param settings: list of Google calendar settings for the user
    :param refresh_token: OAuth refresh token
    :param credentials: google.oauth2.credentials.Credentials
    :return: The newly created user, or None if a user already exists
    """

    # add user to the database
    user = User(
        google_id=userinfo['id'],
        email=userinfo['email'],
        name=userinfo['name'],
        refresh_token=refresh_token
    )

    user.locale = settings['locale']
    user.timezone = settings['timezone']
    user.date_field_order = settings['dateFieldOrder']
    user.time_24hour = (settings['format24HourTime'] == 'true')
    user.hide_weekends = (settings['hideWeekends'] == 'true')

    db.session.add(user)
    db.session.commit()

    return user


def update_existing_user(user, userinfo=None, refresh_token=None):
    """
    Updates an existing user's user info and tokens, if provided.  Tokens will not be overridden if they are not
    provided.

    Calendars are not modified in this method.

    :param user: The user
    :param userinfo: The userinfo from Google
    :param refresh_token: OAuth refresh token
    :return: The user that was updated, or None if the user was not found
    """

    user.last_updated = datetime.utcnow()

    if userinfo:
        user.google_id=userinfo.get('id', user.google_id)
        user.name = userinfo.get('name', user.name)
        user.email = userinfo.get('email', user.email)

    if refresh_token:
        user.refresh_token = refresh_token

    db.session.commit()

    return user
