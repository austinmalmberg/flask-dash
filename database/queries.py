from database import db
from database.models import Calendar


def add_calendar(user_id, calendar, watching=False, check_if_exists=False):
    new_calendar = None

    if check_if_exists:
        new_calendar = Calendar.query.filter_by(user_id=user_id, calendar_id=calendar['id']).first()

    if new_calendar is None:
        new_calendar = Calendar(
            user_id=user_id,
            calendar_id=calendar['id'],
            summary=calendar.get('summary'),
            watching=watching
        )

        db.session.add(new_calendar)
        db.session.commit()

    return new_calendar


def remove_calendar(id):
    calendar_to_remove = Calendar.query.get(id)
    db.session.delete(calendar_to_remove)
    db.commit()
