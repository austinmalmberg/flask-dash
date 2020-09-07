
def register_blueprints(app):
    """
    The method that registers all route blueprints

    :param app: The app.py application
    :return: None
    """

    # Endpoints for index and dashboard
    from daily_dashboard.routes import dashboard
    app.register_blueprint(dashboard.bp)

    # Endpoints for managing weather cookies
    from daily_dashboard.routes import weather
    app.register_blueprint(weather.bp)

    # Endpoints for authentication and retrieving calendar data
    from daily_dashboard.routes import google
    google.register_blueprints(app)
