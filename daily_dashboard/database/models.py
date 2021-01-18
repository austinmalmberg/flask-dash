from datetime import datetime

from flask_login import UserMixin

from daily_dashboard.database import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    last_updated = db.Column(db.DateTime, default=datetime.utcnow())

    # Google OAuth 2.0 token
    refresh_token = db.Column(db.String())

    # Google userinfo
    google_id = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String())

    # calendar settings
    locale = db.Column(db.String(10), default='en')
    timezone = db.Column(db.String(), default='Etc/GMT')
    date_field_order = db.Column(db.String(3), default='MDY')
    time_24hour = db.Column(db.Boolean, default=False)
    hide_weekends = db.Column(db.Boolean, default=False)

    def __init__(self, google_id=None, email=None, name=None, refresh_token=None, credentials=None):
        self.google_id = google_id
        self.email = email
        self.name = name

        self.refresh_token = credentials.refresh_token if credentials else refresh_token
