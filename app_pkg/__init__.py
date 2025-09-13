from flask import Flask
from .extensions import db, cors


def create_app() -> Flask:
    """Application factory that initializes extensions and registers blueprints."""
    app = Flask(
        __name__,
        static_folder='../static',
        template_folder='../templates',
    )

    # Base config
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patientsss.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    cors.init_app(app)
    db.init_app(app)

    # No-cache headers for dev
    @app.after_request
    def add_no_cache_headers(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    # Register blueprints
    from .blueprints.pages import pages_bp
    from .blueprints.camera import camera_bp
    from .blueprints.voice import voice_bp
    from .blueprints.sensors import sensors_bp
    from .blueprints.patients import patients_bp
    from .blueprints.serial import serial_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(camera_bp)
    app.register_blueprint(voice_bp)
    app.register_blueprint(sensors_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(serial_bp)

    # Ensure database tables exist
    with app.app_context():
        db.create_all()

    # Register teardown hooks for services
    from .services.camera import cleanup
    app.teardown_appcontext(cleanup)

    return app


