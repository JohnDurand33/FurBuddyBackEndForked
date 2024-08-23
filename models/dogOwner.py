from sqlalchemy import Column, Integer, String
from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class DogOwner(Base):
    __tablename__ = 'Owner'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(db.String(100), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    owner_name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    owner_email: Mapped[str] = mapped_column(db.String(100), nullable=False)
    owner_phone: Mapped[str] = mapped_column(db.String(25), nullable=False)
    
    profiles = relationship("Profile", back_populates="owner")

 