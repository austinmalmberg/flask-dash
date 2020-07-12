from datetime import datetime

from flask import redirect, url_for
from flask_login import LoginManager

from database import db
from database.models import User, Calendar
from database.queries import add_calendar
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
        raise ValueError('google_id cannot be None')

    return User.query.filter_by(google_id=google_id).first()


def init_new_user(userinfo, token=None, refresh_token=None, credentials=None):
    """
    Creates a new user in the database.

    :param userinfo: userinfo from Google
    :param token: OAuth token
    :param refresh_token: OAuth refresh token
    :param credentials: google.oauth2.credentials.Credentials
    :return: The newly created user, or None if a user already exists
    """

    # fails if userinfo is null since we use the google_id to check if the user exists within the database
    google_id = userinfo['id']

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


def update_existing_user(user, userinfo, token=None, refresh_token=None, credentials=None):
    """
    Updates an existing user's user info and tokens, if provided.  Tokens will not be overridden if they are not
    provided.

    Calendars are not modified in this method.

    :param user: The user
    :param userinfo: The userinfo from Google
    :param token: OAuth token
    :param refresh_token: OAuth refresh token
    :param credentials: google.oauth2.credentials.Credentials
    :return: The user that was updated, or None if the user was not found
    """
    if not user:
        return init_new_user(userinfo, token=token, refresh_token=refresh_token, credentials=credentials)

    user.last_updated = datetime.utcnow()

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


def sync_calendar(user, google_calendar):
    """
    Takes a google_calendar.  If a user_calendar is given, changes the user_calendar.summary to match.

    If user_calendar is None, queries the database for a calendar with a matching calendar_id.  If None exists, the
    method will add the calendar.

    :param user: A User from the database
    :param google_calendar: A Google Calendar resource as shown here:
        https://developers.google.com/calendar/v3/reference/calendarList#resource
    :return: The synced or newly created calendar
    """
    user_calendar = next((cal for cal in user.calendars if cal.calendar_id == google_calendar['id']), None)

    if not user_calendar:
        return add_calendar(user.id, google_calendar)

    user_calendar.summary = google_calendar.get('summary', user_calendar.summary)
    db.session.commit()

    return user_calendar


def sync_calendars(user, google_calendars):
    """
    Takes a User and a Google Calendar resource list. And sync the calendars by doing the following:

    - if the calendar exists in the database and in google_calendars, sync it
    - if the calendar does not exist in the database but does in google_calendars, add it
    - if the calendar exists in the database but not google calendars, delete it

    :param user: The User whose Calendars to sync
    :param google_calendars: A Google Calendar resource list as shown here:
        https://developers.google.com/calendar/v3/reference/calendarList#resource
    :return: None
    """
    calendars = {cal.calendar_id: cal for cal in user.calendars}

    for g_cal in google_calendars:
        # updates or adds the calendar
        sync_calendar(user, g_cal)

        # removes the calendar
        calendars.pop(g_cal['id'], None)

    # delete remaining calendars that weren't removed within the sync loop above
    for cal in calendars.values():
        db.session.delete(cal)

    db.session.commit()
