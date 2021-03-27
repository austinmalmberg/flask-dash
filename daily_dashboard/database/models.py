from datetime import datetime, timedelta
import uuid

from flask_login import UserMixin

from daily_dashboard.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    last_updated = db.Column(db.DateTime, default=datetime.utcnow())

    # Google OAuth 2.0 tokens
    refresh_token = db.Column(db.String())
    refresh_token_lid = db.Column(db.String())

    # Google userinfo
    google_id = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String())

    # calendar settings pulled from Google
    # these will be the initial values for new devices
    locale = db.Column(db.String(10), default='en')
    timezone = db.Column(db.String(), default='Etc/GMT')
    date_field_order = db.Column(db.String(3), default='MDY')
    time_24hour = db.Column(db.Boolean, default=False)
    hide_weekends = db.Column(db.Boolean, default=False)

    devices = db.relationship('Device', back_populates='user')

    def __init__(self, google_id=None, email=None, name=None):
        self.google_id = google_id
        self.email = email
        self.name = name


class Device(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    last_updated = db.Column(db.DateTime, default=datetime.utcnow())
    last_check_in = db.Column(db.DateTime, default=datetime.utcnow())

    uuid = db.Column(db.String(), nullable=False)
    uuid_expiration = db.Column(db.DateTime, default=datetime.utcnow())

    common_name = db.Column(db.String())

    # set depending on the authentication method
    is_limited_input_device = db.Column(db.Boolean, default=False)

    # foreign user keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='devices')

    # Device Preferences
    # these variables are stored in the database as opposed to a cookie so they can be changed from another device,
    # specifically for devices that do not have input devices (i.e. TVs and kiosks)
    locale = db.Column(db.String(10), default='en')
    timezone = db.Column(db.String(), default='Etc/GMT')
    date_field_order = db.Column(db.String(3), default='MDY')
    time_24hour = db.Column(db.Boolean, default=False)

    # a semicolon delimited string of watched calendars
    _watched_calendars = db.Column(db.String(), default='')

    @property
    def watched_calendars(self):
        return self._watched_calendars.split(';')

    def __init__(self, user, is_limited_input_device=False):
        self.update_uuid()

        self.is_limited_input_device = is_limited_input_device

        self.common_name = f'Device {self.uuid}'

        self.user_id = user.id

        self.locale = user.locale
        self.timezone = user.timezone
        self.date_field_order = user.date_field_order
        self.time_24hour = user.time_24hour

        self.add_calendar(user.email)

    def update_device(self, common_name=None, locale=None, timezone=None, date_field_order=None, time_24hour=None):
        was_modified = False

        if common_name:
            self.common_name = common_name
            was_modified = True

        if locale:
            self.locale = locale
            was_modified = True

        if timezone:
            self.timezone = timezone
            was_modified = True

        if date_field_order:
            self.date_field_order = date_field_order
            was_modified = True

        if time_24hour:
            self.time_24hour = time_24hour
            was_modified = True

        if was_modified:
            self.last_updated = datetime.utcnow()

        return self

    def set_calendars(self, calendar_ids):
        self._watched_calendars = ';'.join(calendar_ids)

        self.last_updated = datetime.utcnow()

    def add_calendar(self, calendar_id):
        self._watched_calendars = calendar_id if len(self._watched_calendars) == 0 \
            else f'{self._watched_calendars};{calendar_id}'

        self.last_updated = datetime.utcnow()

        return self.watched_calendars

    def remove_calendar(self, calendar_id):
        calendars = self.watched_calendars
        if calendar_id not in calendars:
            return calendars

        cal_index = calendars.index(calendar_id)
        new_calendar_list = calendars[:cal_index] + calendars[cal_index + 1:]

        self._watched_calendars = ';'.join(new_calendar_list)
        self.last_updated = datetime.utcnow()

        return new_calendar_list

    def update_uuid(self):
        # TODO: check for uuid conflicts
        self.uuid = uuid.uuid4()
        self.uuid_expiration = datetime.utcnow() + timedelta(minutes=20)

        self.last_updated = datetime.utcnow()
