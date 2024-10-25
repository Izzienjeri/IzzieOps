# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import your models
from models import User, Document  # Adjust as necessary

with app.app_context():
    db.create_all()  # This creates tables in the database based on your models

if __name__ == '__main__':
    app.run(debug=True)
