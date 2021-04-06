from flask import redirect, url_for, session, g
from flask_login import LoginManager

from daily_dashboard.database.models import User, Device
from daily_dashboard.data_access.devices import device_check_in

login = LoginManager()


def init_app(app):
    # Implement flask_login
    login.init_app(app)


@login.user_loader
def load_authenticated_user(user_id):
    user = User.query.get(user_id)

    if user:
        device_id = session.get('device_id', None)
        if device_id:
            device = Device.query.get(device_id)
            device_check_in(device)

            g.device = device

    return user


@login.unauthorized_handler
def handle_unauthorized_device():
    return redirect(url_for('main.login'))
