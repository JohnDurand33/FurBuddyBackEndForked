from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey

class Profile(Base):
    __tablename__ = 'Profile'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    age: Mapped[int] = mapped_column(db.Integer, nullable=True)
    sex: Mapped[str] = mapped_column(db.String(20), nullable=True)
    fixed: Mapped[bool] = mapped_column(db.Boolean, nullable=True)
    breed: Mapped[str] = mapped_column(db.String(100), nullable=True)
    weight: Mapped[str] = mapped_column(db.String(100), nullable=True)
    chip_number: Mapped[str] = mapped_column(db.String(25), nullable=True)
    image_path: Mapped[str] = mapped_column(db.String(500), nullable=True)
    
    vet_clinic_name: Mapped[str] = mapped_column(db.String(250), nullable=True)
    vet_clinic_phone: Mapped[str] = mapped_column(db.String(25), nullable=True)
    vet_clinic_email: Mapped[str] = mapped_column(db.String(100), nullable=True)
    vet_doctor_name: Mapped[str] = mapped_column(db.String(100), nullable=True)
    
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('Owner.id'), nullable=True)
    owner = relationship("DogOwner", back_populates="profiles")
   
        
 
    