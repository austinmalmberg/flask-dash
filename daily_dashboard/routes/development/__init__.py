from daily_dashboard.routes.development import index


def register_blueprints(app):
    app.register_blueprint(index.bp)
