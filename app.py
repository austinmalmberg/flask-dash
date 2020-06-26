import os

from flask import Flask

import database
from helpers import user_manager, brand


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ['SECRET_KEY'],
        SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    database.init_app(app)

    user_manager.init_app(app)

    @app.context_processor
    def inject_brand():
        return dict(brand=brand)

    import routes
    routes.register_blueprints(app)

    return app


