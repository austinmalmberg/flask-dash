def register_blueprints(app):
    """
    The method that registers all route blueprints

    :param app: The app.py application
    :return: None
    """

    # Main Dashboard
    from daily_dashboard.routes import dashboard
    app.register_blueprint(dashboard.bp)

    # Authorization #
    from daily_dashboard.routes.google import oauth, oauth_limited_input_device
    app.register_blueprint(oauth.bp)
    app.register_blueprint(oauth_limited_input_device.bp)
