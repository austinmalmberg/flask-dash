
def register_blueprints(app):
    from . import users
    app.register_blueprint(users.bp)

    from . import devices
    app.register_blueprint(devices.bp)

    from .v0 import calendars as v0_calendars, weather as v0_weather
    app.register_blueprint(v0_calendars.bp)
    app.register_blueprint(v0_weather.bp)
