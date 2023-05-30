from flask import Flask
from .db import mongo
from .auth import auth as auth_bp
from .kyc import kyc as kyc_bp
from .staff import staff as staff_bp
from .services import services as services_bp
from .bookings import bookings as bookings_bp
from .stores import stores as stores_bp

def create_app(config_object='core.settings'):
    app = Flask(__name__)

    app.config.from_object(config_object)
    mongo.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(kyc_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(stores_bp)

    return app