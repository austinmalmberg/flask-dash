import functools

from flask import session, g, flash, redirect, url_for
from flask_login import current_user

from daily_dashboard.data_access.devices import get_device, device_check_in, create_or_update_device


def use_device(view):
    """
    A decorator that assigns the current device to the request variable, g
    """

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        device_id = session.get('device_id', None)
        if device_id is None:
            flash('Device authentication error. Please login again.')
            return redirect(url_for('main.login'))

        device = get_device(device_id)
        device_check_in(device)

        g.device = device

        return view(*args, **kwargs)

    return wrapped_view


