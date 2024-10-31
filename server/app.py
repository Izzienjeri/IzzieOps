from flask import Flask
from config import Config
from flask_migrate import Migrate
from extensions import db, mail  # Import mail
from serializer import serializer_bp
from routes.onboarding import onboarding_bp

# Initialize migration tools
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)  # Initialize mail

    # Register blueprints
    app.register_blueprint(serializer_bp)
    app.register_blueprint(onboarding_bp, url_prefix='/api/onboarding')

    # Create tables if not exist
    with app.app_context():
        from models import Employee, OnboardingDocument, WelcomeEmail, Policy
        db.create_all()

    @app.route('/')
    def index():
        return "Welcome to IzzieOps!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
