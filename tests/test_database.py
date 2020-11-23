from daily_dashboard.database.models import User


def test_db_seeding(app):
    with app.app_context():
        user = User.query.get(1)
        assert user.email == 'austin.malmberg@gmail.com'
