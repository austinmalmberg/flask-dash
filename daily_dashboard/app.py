import os
from datetime import date, datetime
from dateutil import parser

from flask import Flask, request, redirect

from daily_dashboard import database
from daily_dashboard.helpers import user_manager, brand
from daily_dashboard.util.converters import DatetimeConverter


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

    @app.before_request
    def redirect_to_https():
        if not request.is_secure:
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)

    @app.context_processor
    def datetime_formatters():
        def _convert_to_dt(non_dt_variable):
            try:
                if not isinstance(non_dt_variable, (date, datetime)):
                    return parser.isoparse(non_dt_variable)
            except ValueError:
                raise ValueError
            return non_dt_variable

        def _format_time(dt, platform='windows'):
            return _convert_to_dt(dt).strftime('%#I:%M %p' if platform == 'windows' else '%-I:%M %p')

        def _format_date(dt, platform='windows'):
            return _convert_to_dt(dt).strftime('%B %#d' if platform == 'windows' else '%B %-d')

        def _format_iso_date(dt):
            return _convert_to_dt(dt).strftime('%Y-%m-%d')

        def _date_comparator(d1, d2):
            """
            Compares two dates and returns the number of days between them.

            :param d1: A date, datetime, or iso formatted string.
            :param d2: A date, datetime, or iso formatted string.
            :return: the number of days between d1 and d2
                If d2 is greater than d1, the result will be positive.
                If d1 is greater than d2, the result will be negative.

            """
            diff = datetime.combine(_convert_to_dt(d2), datetime.min.time()) - \
                datetime.combine(_convert_to_dt(d1), datetime.min.time())

            return diff.days

        return dict(format_time=_format_time, format_date=_format_date, format_iso_date=_format_iso_date,
                    date_comparator=_date_comparator)

    @app.context_processor
    def inject_brand():
        return dict(brand=brand)

    database.init_app(app)

    user_manager.init_app(app)

    from daily_dashboard import routes
    routes.register_blueprints(app)

    return app
