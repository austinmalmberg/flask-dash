from flask import redirect, url_for
from flask_login import LoginManager

from daily_dashboard.database.models import User

login = LoginManager()


def init_app(app):
    # Implement flask_login
    login.init_app(app)


@login.user_loader
def load_authenticated_user(user_id):
    return User.query.get(user_id)


@login.unauthorized_handler
def handle_unauthorized_device():
    return redirect(url_for('main.login'))
