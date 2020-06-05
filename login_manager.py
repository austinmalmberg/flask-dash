from flask import redirect, url_for
from flask_login import LoginManager

from database import User

login = LoginManager()


def init_app(app):
    # implement flask_login
    login.init_app(app)


@login.user_loader
def load_user(user_id):
    if user_id is None:
        return None

    return User.query.filter_by(id=user_id).first()


@login.unauthorized_handler
def handle_unauthorized_user():
    return redirect(url_for('main.login'))
