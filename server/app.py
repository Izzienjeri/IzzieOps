from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from serializer import serializer_bp

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database and migration tools
db = SQLAlchemy(app)  # Initialize SQLAlchemy with the Flask app
migrate = Migrate(app, db)  # Initialize Flask-Migrate with the app and db

# Register the serializer blueprint
app.register_blueprint(serializer_bp)

# Import your models here to ensure they're registered with SQLAlchemy
from models import Employee, OnboardingDocument, WelcomeEmail, Policy 

# Optional: Create a route to test the application
@app.route('/')
def index():
    return "Welcome to the Employee Management System!"

# Run the application
if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for development
