from database import db
from sqlalchemy import Index
from enum import Enum
from sqlalchemy import Enum as SqlEnum
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, DateTime


class Color(Enum):
    RED = '#FF5733'
    GREEN = '#28A745'
    BLUE = '#007BFF'
    YELLOW = '#FFC107'
    ORANGE = '#FF6F20'

class Event(db.Model):
    __tablename__ = 'Event'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    street = db.Column(db.String(255), nullable=True)
    zip_code = db.Column(db.String(20), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    color_id = db.Column(SqlEnum(Color), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('Owner.id'), nullable=False)  

    owner = db.relationship('DogOwner', backref=db.backref('events', lazy=True))
    

    __table_args__ = (
        Index('ix_event_owner_id', 'owner_id'), 
        Index('ix_event_start_time', 'start_time'), 
        Index('ix_event_end_time', 'end_time'),
    )    
    