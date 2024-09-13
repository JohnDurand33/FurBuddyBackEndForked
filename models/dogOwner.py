from sqlalchemy import Column, Integer, String
from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class DogOwner(db.Model):
    __tablename__ = 'Owner'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    owner_name: Mapped[str] = mapped_column(db.String(100), nullable=True)
    owner_email: Mapped[str] = mapped_column(db.String(100), nullable=False)
    owner_phone: Mapped[str] = mapped_column(db.String(25), nullable=True)
    
    profiles = relationship("Profile", back_populates="owner")

 