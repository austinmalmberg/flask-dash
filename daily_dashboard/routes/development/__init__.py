from daily_dashboard.routes.development import themes


def register_blueprints(app):
    app.register_blueprint(themes.bp)
