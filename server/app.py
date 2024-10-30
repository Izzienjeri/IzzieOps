from flask import Flask
from config import Config
from flask_migrate import Migrate
from extensions import db 
from serializer import serializer_bp

# Initialize migration tools
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(serializer_bp)

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
