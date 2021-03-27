import os

from flask import Flask, request, redirect, session

from daily_dashboard import brand, database
from daily_dashboard.helpers import device_manager
from daily_dashboard.util.converters import DatetimeConverter, CustomFloatConverter


def create_app(config_str=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ['SECRET_KEY'],
    )

    if config_str:
        app.config.from_object(config_str)
    elif app.env == 'development':
        app.config.from_object('daily_dashboard.config.DevelopmentConfig')
    else:
        app.config.from_object('daily_dashboard.config.ProductionConfig')

    # Add a datetime converter
    # this is used in route validation
    app.url_map.converters['datetime'] = DatetimeConverter
    app.url_map.converters['float_neg'] = CustomFloatConverter

    @app.before_request
    def set_permanent_session():
        session.permanent = True

    @app.before_request
    def redirect_to_https():
        if not request.is_secure:
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)

    @app.context_processor
    def inject_brand():
        return dict(brand=brand)

    database.init_app(app)

    device_manager.init_app(app)

    from daily_dashboard import routes
    routes.register_blueprints(app)

    return app
