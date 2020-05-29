from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(100), unique=True)
    token = db.Column(db.String())
    refresh_token = db.Column(db.String())


# class Devices(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     uid = db.Column()
#
#     user_id = db.relationship('User')
#
#
# class Calendar(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     calendar_id = db.Column()
#
#     user_id = db.relationship('User')


# configuration
#     time_format = db.Column()
#     show_tod = db.Column()  # time of day
#     show_seconds = db.Column()