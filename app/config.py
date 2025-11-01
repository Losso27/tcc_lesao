import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_port = os.environ.get('DB_PORT')
    db_url = os.environ.get('DB_URL')
    db_database = os.environ.get('DB_DATABASE')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_url}:{db_port}/{db_database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET')