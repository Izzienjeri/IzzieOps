# config.py

import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:njeri1456@localhost/izzieops')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
