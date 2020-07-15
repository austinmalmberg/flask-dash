
def register_blueprints(app):
    # Endpoints to authenticate the user from the same device
    from daily_dashboard.routes.google import oauth
    app.register_blueprint(oauth.bp)

    # Endpoints to authenticate the user from devices without peripherals
    from daily_dashboard.routes.google import oauth_limited_input_device
    app.register_blueprint(oauth_limited_input_device.bp)

    from daily_dashboard.routes.google import userinfo
    app.register_blueprint(userinfo.bp)

    # Endpoints for getting calendar JSON data
    from daily_dashboard.routes.google import calendars
    app.register_blueprint(calendars.bp)

