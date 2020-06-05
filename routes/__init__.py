
def register_blueprints(app):
    """
    The method that registers all route blueprints

    :param app: The app.py application
    :return: None
    """

    # Endpoints for index and dashboard
    from routes import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')

    # Endpoints for authentication and retreiveing calendar data
    from routes import google
    google.register_blueprints(app)
