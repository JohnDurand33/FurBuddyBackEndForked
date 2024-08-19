from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, Integer, String

class Profile(Base):
    __tablename__ = 'Profile'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    age: Mapped[int] = mapped_column(db.Integer, nullable=False)
    sex: Mapped[str] = mapped_column(db.String(20), nullable=False)
    fixed: Mapped[bool] = mapped_column(db.Boolean, nullable=False)
    breed: Mapped[str] = mapped_column(db.String(100), nullable=False)
    weight: Mapped[str] = mapped_column(db.String(100), nullable=False)
    chip_number: Mapped[str] = mapped_column(db.String(25), nullable=False)
    image_path: Mapped[str] = mapped_column(db.String(255), nullable=True)
   
        
 
    