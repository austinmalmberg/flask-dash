from flask import redirect, url_for
from flask_login import LoginManager

from daily_dashboard.database.models import Device
from daily_dashboard.database.data_access.devices import authenticate_device, device_check_in, remove_device,\
    remove_multiple_devices

login = LoginManager()


def init_app(app):
    # Implement flask_login
    login.init_app(app)


@login.user_loader
def load_authenticated_device(device_id):
    device = Device.query.get(device_id)
    device_check_in(device)
    return device


@login.unauthorized_handler
def handle_unauthorized_device():
    return redirect(url_for('main.login'))


def authenticate_device_session(user, is_limited_input_device=False):
    authenticate_device(user, is_limited_input_device)


def deauthenticate_device(device):
    remove_device(device)


def deauthenticate_all_devices(devices):
    remove_multiple_devices(devices)
