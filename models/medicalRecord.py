from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from database import db
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from sqlalchemy import Date

class Category(db.Model):
    __tablename__ = 'Category'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(255), nullable=False)

    medical_records = db.relationship("MedicalRecord", back_populates="category")
    service_types = db.relationship("ServiceType", back_populates="category")

class ServiceType(db.Model):
    __tablename__ = 'ServiceType'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_type_name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.id'), nullable=False)

    category = db.relationship("Category", back_populates="service_types")
    medical_records = db.relationship("MedicalRecord", back_populates="service_type")


class MedicalRecord(db.Model):
    __tablename__ = 'MedicalRecord'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_date = db.Column(db.Date, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.id'), nullable=False)
    service_type_id = db.Column(db.Integer, db.ForeignKey('ServiceType.id'), nullable=False)
    follow_up_date = db.Column(db.Date, nullable=True)
    fee = db.Column(db.Numeric(10, 2), nullable=True)
    image_path = db.Column(db.String(500), nullable=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('Profile.id'), nullable=False)
    
    category = db.relationship("Category")
    service_type = db.relationship("ServiceType")
    profile = db.relationship("Profile", back_populates="medical_records")