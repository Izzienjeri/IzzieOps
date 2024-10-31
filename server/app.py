# app.py
from flask import Flask
from config import Config
from flask_migrate import Migrate
from extensions import db 
from routes.employee import employee_bp  # Import the Employee Blueprint
from routes.onboarding_document import onboarding_document_bp  # Import Onboarding Document Blueprint
from routes.welcome_email import welcome_email_bp  # Import Welcome Email Blueprint
from routes.policy import policy_bp  # Import Policy Blueprint

# Initialize migration tools
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register Blueprints
    app.register_blueprint(employee_bp, url_prefix='/api')
    app.register_blueprint(onboarding_document_bp, url_prefix='/api')
    app.register_blueprint(welcome_email_bp, url_prefix='/api')
    app.register_blueprint(policy_bp, url_prefix='/api')

    with app.app_context():
        from models import Employee, OnboardingDocument, WelcomeEmail, Policy
        db.create_all()

    @app.route('/')
    def index():
        return "Welcome to the Employee Management System!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
