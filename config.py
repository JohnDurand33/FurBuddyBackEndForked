import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()

class DevelopmentConfig:
    # SQLALCHEMY_DATABASE_URI = URL.create(
    #     "mssql+pyodbc",
    #     username=os.getenv("USERNAME"),
    #     password=os.getenv("PASSWORD"),
    #     host=os.getenv("HOST"),
    #     port=os.getenv("PORT"),
    #     database=os.getenv("DATABASE"),
    #     query={
    #     "Driver": "ODBC Driver 18 for SQL Server",
    #     "TrustServerCertificate": "yes",
    #     "Encrypt": "yes",
    #     "Connection Timeout": "30"
    #     },
    # )
    FLASK_APP = os.getenv("FLASK_APP")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    CACHE_TYPE ="SimpleCache"
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    DEBUG = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

    # CELERY_BROKER_URL = 'redis://localhost:6379/0'
    # CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 587
    # MAIL_USERNAME = 'your-email@gmail.com'
    # MAIL_PASSWORD = 'your-email-password'
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False
