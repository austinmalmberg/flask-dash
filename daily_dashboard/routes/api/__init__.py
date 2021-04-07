
def register_blueprints(app):
    from . import calendars
    app.register_blueprint(calendars.bp)

    from . import weather
    app.register_blueprint(weather.bp)
