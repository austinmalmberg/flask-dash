from datetime import datetime, timedelta

from daily_dashboard.database import db
from daily_dashboard.database.models import Device

DAY_THRESHOLD_UNTIL_STALE = 30


def authenticate_device(user, is_limited_input_device):
    device = Device(user, is_limited_input_device)
    db.session.add(device)
    db.session.flush()
    db.session.commit()

    return device


def device_check_in(device):
    device.last_check_in = datetime.utcnow()
    db.session.commit()


def remove_stale_devices(devices):
    device_removed = False

    for device in devices:
        if device.last_check_in + timedelta(days=DAY_THRESHOLD_UNTIL_STALE) < datetime.utcnow():
            db.session.delete(device)
            device_removed = True

    if device_removed:
        db.session.commit()


def update_device_uuids(devices):
    for device in devices:
        device.update_uuid()

    db.session.commit()


def set_device_calendars(device, calendar_ids):
    device.set_calendars(calendar_ids)

    db.session.commit()


def remove_device(device):
    db.session.delete(device)
    db.session.commit()


def remove_multiple_devices(devices):
    for device in devices:
        db.session.delete(device)

    db.session.commit()


def update_device_settings(device, **kwargs):
    device.update_device(**kwargs)

    db.session.commit()
