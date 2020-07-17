import pytest

from daily_dashboard.app import create_app
from daily_dashboard.database.models import User, Calendar


@pytest.fixture
def app():
    app = create_app('daily_dashboard.config.TestingConfig')

    with app.app_context():
        from daily_dashboard.database import db

        seed_db(db)

        yield app

        db.session.remove()
        db.drop_all()
        db.get_engine(app).dispose()


@pytest.fixture
def client(app):
    return app.test_client()


def seed_db(db):
    test_user = User(
        google_id='Google id',
        email='austin.malmberg@gmail.com',
        name='Austin Malmberg',
        refresh_token='Refresh token'
    )

    db.session.add(test_user)
    db.session.flush()

    test_calendar = Calendar(
        user_id=test_user.id,
        calendar_id='austin.malmberg@gmail.com',
        summary='Test calendar',
        watching=True
    )

    db.session.add(test_calendar)

    db.session.commit()