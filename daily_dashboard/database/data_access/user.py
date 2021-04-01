from datetime import datetime

from daily_dashboard.database import db
from daily_dashboard.database.models import GoogleUser


def find_user(google_id):
    if google_id is None:
        raise ValueError('google_id cannot be None')

    return GoogleUser.query.filter_by(google_id=google_id).first()


def init_new_user(userinfo, settings, refresh_token=None, is_limited_input_device=False):
    """
    Creates a new user in the database.

    :param userinfo: userinfo from Google
    :param settings: list of Google calendar settings for the user
    :param refresh_token: OAuth refresh token
    :param is_limited_input_device: determines which database field to add the refresh token to
    :return: The newly created user, or None if a user already exists
    """

    # add user to the database
    user = GoogleUser(
        google_id=userinfo['id'],
        email=userinfo['email'],
        name=userinfo['name']
    )

    if refresh_token:
        if is_limited_input_device:
            user.refresh_token_lid = refresh_token
        else:
            user.refresh_token = refresh_token

    user.locale = settings['locale']
    user.timezone = settings['timezone']
    user.date_field_order = settings['dateFieldOrder']
    user.time_24hour = (settings['format24HourTime'] == 'true')
    user.hide_weekends = (settings['hideWeekends'] == 'true')

    db.session.add(user)
    db.session.flush()
    db.session.commit()

    print('New user added.', user)

    return user


def update_existing_user(user, userinfo=None, refresh_token=None, is_limited_input_device=False):
    """
    Updates an existing user's user info and tokens, if provided.  Tokens will not be overridden if they are not
    provided.

    Calendars are not modified in this method.

    :param user: The user
    :param userinfo: The userinfo from Google
    :param refresh_token: OAuth refresh token
    :param is_limited_input_device: determines which database field to update with the refresh token
    :return: The user that was updated, or None if the user was not found
    """

    user.last_updated = datetime.utcnow()

    if userinfo:
        user.google_id = userinfo.get('id', user.google_id)
        user.name = userinfo.get('name', user.name)
        user.email = userinfo.get('email', user.email)

    if refresh_token:
        if is_limited_input_device:
            user.refresh_token_lid = refresh_token
        else:
            user.refresh_token = refresh_token

    db.session.commit()

    return user
