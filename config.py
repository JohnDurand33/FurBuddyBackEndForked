import os
from dotenv import load_dotenv

load_dotenv()

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    CACHE_TYPE = os.getenv("CACHE_TYPE")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    DEBUG = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
