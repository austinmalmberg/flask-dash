from flask import redirect, url_for, session, g
from flask_login import LoginManager

from daily_dashboard.data_access.devices import get_device, device_check_in, create_device
from daily_dashboard.database.models import User

login = LoginManager()


class AuthenticationMethod:
    COOKIE_NAME = 'auth_method'

    DIRECT = 'direct'
    INDIRECT = 'indirect'


def init_app(app):
    # Implement flask_login
    login.init_app(app)


@login.user_loader
def load_authenticated_user(user_id):
    user = User.query.get(user_id)

    device = None

    # check if device_id cookie exists
    if 'device_id' in session:
        device_id = session['device_id']
        device = get_device(device_id)

        # if the device_id variable has been set within the session and not found in the database,
        # this means the device was flagged as stale and removed so just create another database entry
        if device is None:
            session.pop('device_id', None)

    auth_method = session[AuthenticationMethod.COOKIE_NAME]
    is_lid = (auth_method == AuthenticationMethod.INDIRECT)

    if device:
        device_check_in(device, is_lid)
    else:
        device = create_device(user, is_lid)
        session['device_id'] = device.id

    # load device into the request-scoped variable, g
    g.device = device

    return user


@login.unauthorized_handler
def handle_unauthorized_device():
    return redirect(url_for('main.login'))
