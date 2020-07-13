from datetime import datetime

from flask_login import UserMixin

from database import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    last_updated = db.Column(db.DateTime, default=datetime.utcnow())

    # Google OAuth
    refresh_token = db.Column(db.String())

    # Google userinfo
    google_id = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String())

    # calendar settings
    locale=db.Column(db.String(10), default='en')
    timezone=db.Column(db.String(), default='Etc/GMT')
    date_field_order = db.Column(db.String(3), default='MDY')
    time_24hour = db.Column(db.Boolean, default=False)
    hide_weekends = db.Column(db.Boolean, default=False)

    calendars = db.relationship('Calendar', backref='user', lazy=True)

    def __init__(self, google_id=None, email=None, name=None, token=None, refresh_token=None, credentials=None):
        self.google_id = google_id
        self.email = email
        self.name = name

        if credentials:
            self.token = credentials.token
            self.refresh_token = credentials.refresh_token
        else:
            self.token = token
            self.refresh_token = refresh_token


class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    calendar_id = db.Column(db.String(), nullable=False)
    summary = db.Column(db.String())
    watching = db.Column(db.Boolean, default=False)
