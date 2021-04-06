from datetime import datetime, timedelta

from daily_dashboard.database import db
from daily_dashboard.database.models import User


def find_user(google_id):
    if google_id is None:
        raise ValueError('google_id cannot be None')

    return User.query.filter_by(google_id=google_id).first()


def create_new_user(userinfo, settings):
    """
    Creates a new user in the database.

    :param userinfo: userinfo from Google
    :param settings: list of Google calendar settings for the user
    :param refresh_token: OAuth refresh token
    :param is_limited_input_device: determines which database field to add the refresh token to
    :return: The newly created user, or None if a user already exists
    """

    # add user to the database
    user = User(
        google_id=userinfo['id'],
        email=userinfo['email'],
        name=userinfo['name']
    )

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


def update_existing_user(user, userinfo):
    """
    Updates an existing user's user info and tokens, if provided.  Tokens will not be overridden if they are not
    provided.

    Calendars are not modified in this method.

    :param user: The user
    :param userinfo: The userinfo from Google
    :param refresh_token: OAuth refresh token
    :param refresh_token_lid: OAuth refresh token granted for limited input devices
    :return: The user that was updated, or None if the user was not found
    """

    was_modified = False

    user.last_updated = datetime.utcnow()

    if userinfo:
        user.google_id = userinfo.get('id', user.google_id)
        user.name = userinfo.get('name', user.name)
        user.email = userinfo.get('email', user.email)
        was_modified = True

    if was_modified:
        db.session.commit()

    return user


def remove_devices(user):
    was_modified = False

    for device in user.devices:
        db.session.delete(device)
        was_modified = True

    if was_modified:
        db.session.commit()


def remove_stale_devices(user):
    DAY_THRESHOLD_UNTIL_STALE = 30

    device_removed = False

    for device in user.devices:
        if datetime.utcnow() >= device.last_used + timedelta(days=DAY_THRESHOLD_UNTIL_STALE):
            db.session.delete(device)
            device_removed = True

    if device_removed:
        db.session.commit()


