from datetime import datetime

from daily_dashboard.database import db
from daily_dashboard.database.models import Device


def create_device(user, is_limited_input_device):
    device = Device(user, is_limited_input_device)
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


def set_device_calendars(device, calendar_ids):
    device.set_calendars(calendar_ids)

    db.session.commit()


def update_device_settings(device, **kwargs):
    device.update_device(**kwargs)

    db.session.commit()
