from flask import redirect, url_for
from flask_login import LoginManager

from database import db
from database.models import User, Calendar
from database.queries import add_calendar, remove_calendar
from helpers.google.calendars import get_calendar_list, get_calendar_settings

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


def find_user(google_id):
    if google_id is None:
        return None

    return User.query.filter_by(google_id=google_id).first()


def init_new_user(userinfo, token=None, refresh_token=None, credentials=None):
    """
    Creates a new user in the database.

    :param userinfo: userinfo from Google
    :param token: OAuth token
    :param refresh_token: OAuth refresh token
    :param credentials: google.oauth.credentials.Credentials
    :return: The newly created user, or None if a user already exists
    """

    # fail if this is null since we use the google_id to check if the user exists within the database
    google_id = userinfo['id']

    # ensure the user doesn't already exist
    user = find_user(google_id)

    if user:
        return None

    # add user to the database
    user = User(
        google_id=google_id,
        email=userinfo.get('email'),
        name=userinfo.get('name'),
        credentials=credentials,
        token=token,
        refresh_token=refresh_token
    )

    db.session.add(user)
    db.session.flush()

    if not credentials:
        credentials = user.build_credentials()

    # add calendars to the database
    calendar_list = get_calendar_list(credentials)

    for cal in calendar_list:
        calendar = Calendar(
            user_id=user.id,
            calendar_id=cal.get('id'),
            watching=cal.get('primary', False)
        )
        db.session.add(calendar)

    # populate calendar settings
    settings = get_calendar_settings(credentials)

    user.locale = settings.get('locale', user.locale)
    user.timezone = settings.get('timezone', user.timezone)
    user.date_field_order = settings.get('dateFieldOrder', user.date_field_order)
    user.time_24hour = settings.get('format24HourTime', user.time_24hour) == 'true'
    user.hide_weekends = settings.get('hideWeekends', user.hide_weekends) == 'true'

    db.session.commit()

    return user


def update_existing_user(user_id, userinfo, token=None, refresh_token=None, credentials=None):
    """
    Updates an existing user's user info and tokens, if provided.  Tokens will not be overridden if they are not
    provided.

    Calendars are not modified in this method.

    :param user_id: The user id
    :param userinfo: The userinfo from Google
    :param token: OAuth token
    :param refresh_token: OAuth refresh token
    :param credentials: google.oauth.credentials.Credentials
    :return: The user that was updated, or None if the user was not found
    """

    # ensure the user doesn't already exist
    user = User.query.get(user_id)

    if user:
        if credentials:
            token = credentials.token
            refresh_token = credentials.refresh_token

        user.google_id=userinfo.get('id', user.google_id)
        user.name = userinfo.get('name', user.name)
        user.email = userinfo.get('email', user.email)

        if token:
            user.token = token

        if refresh_token:
            user.refresh_token = refresh_token

        db.session.commit()

        return user

    return None


def sync_calendar(user_id, google_calendar, user_calendar):
    if user_calendar.user_id == user_id:
        user_calendar.calendar_id = google_calendar['id']
        user_calendar.summary = google_calendar.get('summary', user_calendar.summary)

        db.session.commit()

        return user_calendar

    return None


def sync_calendars(user_id, google_calendars, user_calendars):
    existing_calendar_ids = [cal.calendar_id for cal in user_calendars]

    for calendar in google_calendars:
        if calendar['id'] in existing_calendar_ids:
            sync_calendar(user_id, calendar, Calendar.query.filter_by(calendar_id=calendar['id']).first())

            # remove the calendar id from the list. Any existing calendars on this list
            # have been deleted and will be removed
            existing_calendar_ids.remove(calendar['id'])
        else:
            add_calendar(user_id, calendar)

    for calendar_id in existing_calendar_ids:
        Calendar.query.filter_by(calendar_id=calendar_id).delete()
        db.session.commit()
