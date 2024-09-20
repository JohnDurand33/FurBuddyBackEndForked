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
    
    
    MAIL_DEBUG = os.getenv("MAIL_DEBUG") == 'True' 
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))  
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"  
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

