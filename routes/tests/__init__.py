
def register_blueprints(app):
    from . import oauth
    app.register_blueprint(oauth.bp)

    from . import general
    app.register_blueprint(general.bp)