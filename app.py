import os
from dotenv import load_dotenv
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS 
from flask_mail import Mail
from config import DevelopmentConfig, db, migrate
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
from routes.testBP import test_blueprint
from reminders.reminderScheduler import start_reminder_scheduler


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

cache = Cache()
mail = Mail()

def create_app(config_name='DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    

    CORS(app)

    app.register_blueprint(dog_owner_blueprint, url_prefix='/owner')
    app.register_blueprint(profile_blueprint, url_prefix='/profile')
    app.register_blueprint(medical_record_blueprint, url_prefix='/medical_record')
    app.register_blueprint(event_blueprint, url_prefix='/event')
    app.register_blueprint(test_blueprint, url_prefix='/test')


    with app.app_context():
        
        # conn = DevelopmentConfig.create_db_connection()
        # cursor = conn.cursor()
        # cursor.close()
        # conn.close()
        # # db.drop_all()
        # db.create_all()
        
        migrate.init_app(app, db)
        
    start_reminder_scheduler(app)

    return app

       
if __name__ == '__main__':
    app = create_app()
    app.run()
