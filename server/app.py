# app.py

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)  # Initialize db after the app is created
migrate = Migrate(app, db)

from models import Employee, OnboardingDocument, WelcomeEmail, Policy  # Import models after db is initialized

if __name__ == '__main__':
    app.run(debug=True)
