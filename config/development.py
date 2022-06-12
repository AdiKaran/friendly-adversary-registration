import os

FLASK_ENV = "development"
DEBUG=True

BASE_DIR = os.path.abspath(os.path.dirname(__file__) + "/../")

SQLALCHEMY_DATABASE_URI = "postgresql://adityakamireddy@localhost:5432/adversary"