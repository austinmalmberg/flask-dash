from datetime import datetime, timedelta
import uuid

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

    name = db.Column(db.String(), default='')
    uuid = db.Column(db.String(), nullable=False)

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

    # for weather
    _position = db.Column(db.String(20))

    def __init__(self, user, is_lid=False):
        self.uuid = str(uuid.uuid4())
        self.is_lid = is_lid

        self.user_id = user.id

        self.locale = user.locale
        self.timezone = user.timezone
        self.date_order = user.date_order
        self.time_24hour = user.time_24hour

        self._watched_calendars = user.email

    @property
    def is_stale(self):
        return datetime.utcnow() >= self.last_updated + timedelta(days=6*30)

    @property
    def watched_calendars(self):
        return self._watched_calendars.split(';')

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

    @property
    def position(self):
        """
        A tuple representing the lat and lon coordinates to pull weather for

        :return: (lat, lon) as float values or None, None if not set
        """
        if self._position is None:
            return None

        lat, lon = self._position.split(',')
        return float(lat), float(lon)

    def set_position(self, lat, lon):
        if lat is None and lon is None:
            self._position = None
        else:
            lat = round(lat, 2)
            lon = round(lon, 2)

            self._position = f"{lat},{lon}"

        self.last_updated = datetime.utcnow()
