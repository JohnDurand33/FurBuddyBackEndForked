from database import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Date
from sqlalchemy import Integer, ForeignKey

class Profile(db.Model):
    __tablename__ = 'Profile'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    sex = db.Column(db.String(20), nullable=True)
    fixed = db.Column(db.Boolean, nullable=True)
    breed = db.Column(db.String(100), nullable=True)
    weight = db.Column(db.String(100), nullable=True)
    chip_number = db.Column(db.String(25), nullable=True)
    image_path = db.Column(db.String(500), nullable=True)
    
    vet_clinic_name = db.Column(db.String(250), nullable=True)
    vet_clinic_phone = db.Column(db.String(25), nullable=True)
    vet_clinic_email = db.Column(db.String(100), nullable=True)
    vet_doctor_name = db.Column(db.String(100), nullable=True)
    
    owner_id = db.Column(db.Integer, db.ForeignKey('Owner.id'), nullable=True)
    owner = db.relationship("DogOwner", back_populates="profiles")
    medical_records = db.relationship("MedicalRecord", back_populates="profile", cascade="all, delete-orphan")
    
  