import os
from dotenv import load_dotenv

load_dotenv()

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/dogs_db'
    CACHE_TYPE = "Simple_Cache"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
   
    # CELERY_BROKER_URL = 'redis://localhost:6379/0'
    # CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 587
    # MAIL_USERNAME = 'your-email@gmail.com'
    # MAIL_PASSWORD = 'your-email-password'
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False