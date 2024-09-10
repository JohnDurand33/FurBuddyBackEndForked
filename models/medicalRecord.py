from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from sqlalchemy import Date


class Category(Base):
    __tablename__ = 'Category'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(255), nullable=False)

    medical_records = relationship("MedicalRecord", back_populates="category")
    service_types = relationship("ServiceType", back_populates="category")
    
    
class ServiceType(Base):
    __tablename__ = 'ServiceType'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    service_type_name: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('Category.id'), nullable=False)

    category = relationship("Category", back_populates="service_types")
    medical_records = relationship("MedicalRecord", back_populates="service_type")


class MedicalRecord(Base):
    __tablename__ = 'MedicalRecord'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    service_date: Mapped[date] = mapped_column(Date, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('Category.id'), nullable=False)
    service_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('ServiceType.id'), nullable=False)
    follow_up_date: Mapped[date] = mapped_column(Date, nullable=True)
    fee: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=True)
    image_path: Mapped[str] = mapped_column(String(500), nullable=True)  
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey('Profile.id'), nullable=False)  
    
    category = relationship("Category")
    service_type = relationship("ServiceType")
    profile = relationship("Profile", back_populates="medical_records")