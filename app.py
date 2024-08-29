import os
from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail
from config import DevelopmentConfig
from database import db
from models.schemas import ma

from models.dogOwner import DogOwner
from models.profile import Profile
# from models.task import Task
from routes.dogOwnerBP import dog_owner_blueprint
from routes.profileBP import profile_blueprint
# from routes.taskBP import task_blueprint


load_dotenv()

mail = Mail()

def create_app(config_name='DevelopmentConfig'):
    
    app = Flask(__name__)

    app.config.from_object(f'config.{config_name}')
    
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    
# blueprint_config(app)
# def blueprint_config(app):

    app.register_blueprint(dog_owner_blueprint, url_prefix='/owner')
    app.register_blueprint(profile_blueprint, url_prefix='/profile')
    # app.register_blueprint(task_blueprint, url_prefix='/task')
    
    # blueprint_config(app)

    with app.app_context():
        #db.drop_all()
        db.create_all()
        
    return app
    
    
if __name__ == '__main__':
    app = create_app()
    
app.run()
