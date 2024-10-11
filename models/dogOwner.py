from sqlalchemy import Column, Integer, String
from database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence

class DogOwner(db.Model):
    __tablename__ = 'Owner'
    
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    owner_name = db.Column(db.String(100), nullable=True)
    owner_email = db.Column(db.String(100), nullable=False)
    owner_phone = db.Column(db.String(25), nullable=True)
    
    profiles = db.relationship("Profile", back_populates="owner")

 