from flask import Flask
from .extensions import db
from .config import Config
from .routes import pacientes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(pacientes, url_prefix="/pacientes")

    with app.app_context():
        db.create_all()

    return app