from flask import Flask
from app.logging import configure_logging
from app.routes import blueprint
from app.db import Database

def create_app():
    app = Flask(__name__)
    configure_logging()
    
    # Register Blueprints
    app.register_blueprint(blueprint)

    # Close DB connection after each request
    @app.teardown_appcontext
    def teardown_db(exception):
        Database.close_connection()

    return app
