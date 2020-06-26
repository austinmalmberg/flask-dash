
def register_blueprints(app):
    # Endpoints to authenticate the user from the same device
    from routes.google import oauth
    app.register_blueprint(oauth.bp)

    # Endpoints to authenticate the user from devices without peripherals
    from routes.google import oauth_limited_input_device
    app.register_blueprint(oauth_limited_input_device.bp)

    from routes.google import userinfo
    app.register_blueprint(userinfo.bp)

    # Endpoints for getting calendar JSON data
    from routes.google import calendars
    app.register_blueprint(calendars.bp)

