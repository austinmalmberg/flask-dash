import os

from daily_dashboard.app import create_app


def test_config():
    prod_app = create_app()
    assert not prod_app.testing
    assert not prod_app.debug
    assert prod_app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL')

    test_app = create_app('daily_dashboard.config.TestingConfig')
    assert test_app.testing
    assert not test_app.debug
    assert test_app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_TEST_URL')

    dev_app = create_app('daily_dashboard.config.DevelopmentConfig')
    assert not dev_app.testing
    assert dev_app.debug
    assert dev_app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL')

