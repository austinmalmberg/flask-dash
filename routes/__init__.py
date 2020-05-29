
def register_blueprints(app):
    """
    The method that registers all route blueprints

    :param app: The app.py application
    :return: None
    """

    # endpoints for index and dashboard
    from . import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')

    # general methods to load user and logout
    from . import auth
    app.register_blueprint(auth.bp)

    # oauth: Endpoints to authenticate the user from the same device
    # oauth_limited_input_device: Endpoints to authenticate the user from devices without peripherals
    #       Asks user to visit Google from another device while displaying a code for the user to enter.
    #       Application front-end queries '/poll' endpoint at a specified duration, checking whether the device has
    #           been authenticated
    from .auth.google import oauth, oauth_limited_input_device
    app.register_blueprint(oauth.bp)
    app.register_blueprint(oauth_limited_input_device.bp)

    # tests
    # only registered in FLASK_ENV=development
    if app.env == 'development':
        from routes import tests
        tests.register_blueprints(app)
