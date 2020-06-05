from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # general info
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(100), unique=True)

    # authentication
    token = db.Column(db.String())
    refresh_token = db.Column(db.String())
    token_type = db.Column(db.String(), default='Bearer')

    # locale info
    locale=db.Column(db.String(10), default='en')
    timezone=db.Column(db.String(), default='Etc/GMT')
    date_field_order = db.Column(db.String(3), default='MDY')
    time_24hour = db.Column(db.Boolean, default=False)

    # calendar info
    hide_weekends = db.Column(db.Boolean, default=False)


# class Devices(Model):
#     id = db.Column(db.Integer, primary_key=True)
#     uid = db.Column()
#
#     user_id = relationship('User')
#
#
# class Calendar(Model):
#     id = db.Column(db.Integer, primary_key=True)
#     calendar_id = db.Column()
#
#     user_id = relationship('User')


# configuration
#     time_format = db.Column()
#     show_tod = db.Column()  # time of day
#     show_seconds = db.Column()
