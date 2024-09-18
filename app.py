import os
from dotenv import load_dotenv
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS 
from flask_mail import Mail
from config import DevelopmentConfig
from database import db
from models.schemas import ma

from models.dogOwner import DogOwner
from models.profile import Profile
from models.medicalRecord import MedicalRecord
from models.event import Event
from routes.dogOwnerBP import dog_owner_blueprint
from routes.profileBP import profile_blueprint
from routes.medicalRecordBP import medical_record_blueprint
from routes.eventBP import event_blueprint



load_dotenv()

cache = Cache()
mail = Mail()

def create_app(config_name='DevelopmentConfig'):
    
    app = Flask(__name__)

    app.config.from_object(f'config.{config_name}')
    
    db.init_app(app)
    ma.init_app(app)
    # mail.init_app(app)
    cache.init_app(app)
    
# def blueprint_config(app):

    CORS(app)

    app.register_blueprint(dog_owner_blueprint, url_prefix='/owner')
    app.register_blueprint(profile_blueprint, url_prefix='/profile')
    app.register_blueprint(medical_record_blueprint, url_prefix='/medical_record')
    app.register_blueprint(event_blueprint, url_prefix='/event')
    
    # blueprint_config(app)

    with app.app_context():
        # db.drop_all()
        db.create_all()
        
        
    return app
    
    
if __name__ == '__main__':
    app = create_app()
    
app.run()
