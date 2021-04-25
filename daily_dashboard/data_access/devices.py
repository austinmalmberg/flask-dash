from datetime import datetime

from daily_dashboard.database import db
from daily_dashboard.database.models import Device


def get_device(device_id):
    return Device.query.get(device_id)


def create_device(user, is_lid):
    device = Device(user, is_lid)
    db.session.add(device)
    db.session.flush()
    db.session.commit()

    return device


def remove_device(device):
    db.session.delete(device)
    db.session.commit()


def device_check_in(device):
    device.last_used = datetime.utcnow()

    db.session.commit()


def create_or_update_device(user, is_lid, device_id=None):
    if device_id is None:
        return create_device(user, is_lid)

    device = get_device(device_id)

    if device and device.user_id == user.id:
        return update_device_settings(device, is_lid=is_lid)

    return create_device(user, is_lid)


def set_device_calendars(device, calendar_ids):
    device.set_calendars(calendar_ids)

    db.session.commit()


def set_device_position(device, lat, lon):
    device.set_position(lat, lon)

    db.session.commit()


def update_device_settings(device, is_lid=None, name=None, locale=None, timezone=None, date_order=None,
                           time_24hour=None, calendars=None, position=None):
    was_modified = False

    if is_lid is not None:
        device.is_lid = is_lid
        was_modified = True

    if name is not None:
        device.name = name
        was_modified = True

    if locale:
        device.locale = locale
        was_modified = True

    if timezone:
        device.timezone = timezone
        was_modified = True

    if date_order:
        device.date_order = date_order
        was_modified = True

    if time_24hour is not None:
        device.time_24hour = time_24hour
        was_modified = True

    if calendars:
        device.set_calendars(calendars)
        was_modified = True

    if position is not None:
        device.set_position(**position)
        was_modified = True

    if was_modified:
        device.last_updated = datetime.utcnow()
        db.session.commit()

    return device
