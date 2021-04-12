
def register_blueprints(app):
    from . import v0_calendars
    app.register_blueprint(v0_calendars.bp)

    from . import v0_weather
    app.register_blueprint(v0_weather.bp)
