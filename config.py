import os
from dotenv import load_dotenv

load_dotenv()

class DevelopmentConfig:
<<<<<<< HEAD
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    CACHE_TYPE = os.getenv("CACHE_TYPE")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    DEBUG = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
=======
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/dogs_db'
    CACHE_TYPE = "SimpleCache"
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
>>>>>>> upstream/main
