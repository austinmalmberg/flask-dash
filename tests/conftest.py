import pytest

from daily_dashboard.app import create_app
from daily_dashboard.database.models import User


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


@pytest.fixture
def session(client):
    with client.session_transaction() as session:
        yield session


@pytest.fixture
def logged_in_user(client):
    response = client.get('/oauth/authorize', follow_redirects=True)

    # TODO: login user

    return None


def seed_db(db):
    test_user = User(
        google_id='Google id',
        email='austin.malmberg@gmail.com',
        name='Austin Malmberg',
        refresh_token='Refresh token'
    )

    db.session.add(test_user)
    db.session.flush()
