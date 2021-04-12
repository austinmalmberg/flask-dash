from datetime import datetime

from flask_login import UserMixin

from daily_dashboard.database import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    last_updated = db.Column(db.DateTime, default=datetime.utcnow())

    # Google userinfo
    google_id = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String())

    # calendar settings pulled from Google
    # these will be the initial values for new devices
    locale = db.Column(db.String(10), default='en')
    timezone = db.Column(db.String(), default='Etc/GMT')
    date_order = db.Column(db.String(3), default='MDY')
    time_24hour = db.Column(db.Boolean, default=False)
    hide_weekends = db.Column(db.Boolean, default=False)

    devices = db.relationship('Device', back_populates='user')

    def __init__(self, google_id=None, email=None, name=None):
        self.google_id = google_id
        self.email = email
        self.name = name


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    last_used = db.Column(db.DateTime, default=datetime.utcnow())
    last_updated = db.Column(db.DateTime, default=datetime.utcnow())

    name = db.Column(db.String())

    # set depending on the authentication method
    is_lid = db.Column(db.Boolean, default=False)

    # foreign user keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='devices')

    # Device Preferences
    # these variables are stored in the database as opposed to a cookie so they can be changed from another device,
    # specifically for devices that do not have input devices (i.e. TVs and kiosks)
    locale = db.Column(db.String(10), default='en')
    timezone = db.Column(db.String(), default='Etc/GMT')
    date_order = db.Column(db.String(3), default='MDY')
    time_24hour = db.Column(db.Boolean, default=False)

    # a semicolon delimited string of watched calendars
    _watched_calendars = db.Column(db.String(), default='')

    @property
    def watched_calendars(self):
        return self._watched_calendars.split(';')

    def __init__(self, user, is_lid=False):
        self.is_lid = is_lid

        self.user_id = user.id

        self.locale = user.locale
        self.timezone = user.timezone
        self.date_order = user.date_order
        self.time_24hour = user.time_24hour

        self._watched_calendars = user.email

    def update_device(self, is_lid=None, name=None, locale=None, timezone=None, date_order=None, time_24hour=None,
                      calendars=None):
        was_modified = False

        if is_lid is not None:
            self.is_lid = is_lid
            was_modified = True

        if name:
            self.name = name
            was_modified = True

        if locale:
            self.locale = locale
            was_modified = True

        if timezone:
            self.timezone = timezone
            was_modified = True

        if date_order:
            self.date_order = date_order
            was_modified = True

        if time_24hour is not None:
            self.time_24hour = time_24hour
            was_modified = True

        if calendars:
            self.set_calendars(calendars)
            was_modified = True

        if was_modified:
            self.last_updated = datetime.utcnow()

        return self

    def set_calendars(self, calendar_ids):
        self._watched_calendars = ';'.join(calendar_ids)

        self.last_updated = datetime.utcnow()

    def add_calendar(self, calendar_id):
        if self._watched_calendars == '':
            self._watched_calendars = calendar_id
        else:
            self._watched_calendars = f'{self._watched_calendars};{calendar_id}'

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
