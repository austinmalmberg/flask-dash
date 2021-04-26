import functools

from flask import session, g, abort
from flask_login import current_user

from daily_dashboard.data_access.devices import get_device, device_check_in, get_device_by_uuid


def use_device(view):
    """
    A decorator that assigns the current device to the request variable, g
    """

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        device_id = session.get('device_id', None)
        device = get_device(device_id)

        if device is None:
            return abort(404)

        # make sure the device id belongs to the authenticated user.
        # I don't think this can happen since the device_id is set within
        # the session during OAuth2 authentication, but just to be safe
        elif device.user_id != current_user.id:
            return abort(401)

        device_check_in(device)

        g.device = device

        return view(*args, **kwargs)

    return wrapped_view


