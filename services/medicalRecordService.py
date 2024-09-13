import os
from database import db
from flask import jsonify
from werkzeug.utils import secure_filename
from flask import current_app
from models.medicalRecord import Category, ServiceType, MedicalRecord
from models.profile import Profile
from models.schemas.medicalRecordSchema import CategorySchema, medical_records_schema
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload



def create_medical_record(current_owner_id, data):
    profile_id = data['profile_id']

    profile = db.session.query(Profile).options(joinedload(Profile.medical_records)).get(profile_id)
    if not profile:
        raise ValueError('Invalid profile ID')
    if profile.owner_id != current_owner_id:
        raise ValueError('Unauthorized access to this profile')

    category = db.session.query(Category).get(data['category_id'])
    if not category:
        raise ValueError('Invalid category ID')

    service_type = db.session.query(ServiceType).get(data['service_type_id'])
    if not service_type:
        raise ValueError('Invalid service type ID')

    new_record = MedicalRecord(
        service_date=data['service_date'],
        category_id=data['category_id'],
        service_type_id=data['service_type_id'],
        follow_up_date=data.get('follow_up_date'),
        fee=data.get('fee'),
        image_path=data.get('image_path'),
        profile_id=profile_id
    )
    try:
        db.session.add(new_record)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Database error: {str(e)}")

    return new_record


def get_medical_record_by_id(record_id, profile_id):
    try:
        record = db.session.query(MedicalRecord).join(Profile).join(Category).join(ServiceType).filter(
            MedicalRecord.id == record_id,
            MedicalRecord.profile_id == profile_id
        ).first()

        if not record:
            raise ValueError('Record not found')

        return record
    except SQLAlchemyError as e:
        raise ValueError(f"Database error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")


def update_medical_record(current_owner_id, profile_id, record_id, data):
    record = db.session.query(MedicalRecord).join(Profile).filter(MedicalRecord.id == record_id, MedicalRecord.profile_id == profile_id).first()
    if not record:
        raise ValueError('Record not found or unauthorized access')
    
    if record.profile.owner_id != current_owner_id:
        raise ValueError('Unauthorized access to this record')
    
    if 'service_date' in data:
        record.service_date = data['service_date']
    if 'category_id' in data:
        category = db.session.query(Category).filter_by(id=data['category_id']).first()
        if not category:
            raise ValueError('Invalid category ID')
        record.category_id = data['category_id']
    if 'service_type_id' in data:
        service_type = db.session.query(ServiceType).filter_by(id=data['service_type_id']).first()
        if not service_type:
            raise ValueError('Invalid service type ID')
        record.service_type_id = data['service_type_id']
    if 'follow_up_date' in data:
        record.follow_up_date = data['follow_up_date']
    if 'fee' in data:
        record.fee = data['fee']
    if 'image_path' in data:
        record.image_path = data['image_path']

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Database error: {str(e)}")

    return record


def delete_medical_record_by_id(current_owner_id, profile_id, record_id):
    try:
        record = db.session.query(MedicalRecord).join(Profile).filter(
            MedicalRecord.id == record_id,
            MedicalRecord.profile_id == profile_id
        ).first()

        if not record:
            raise ValueError('Record not found or unauthorized access')

        if record.profile.owner_id != current_owner_id:
            raise ValueError('Unauthorized access to this record')

        db.session.delete(record)
        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Database error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")
     

def get_paginated_records(page, per_page=10, profile_id=None):
    try:
        offset = (page - 1) * per_page
        limit = per_page

        records_query = db.session.query(MedicalRecord).join(Category).join(ServiceType).offset(offset).limit(limit)
        records = records_query.all()

        result = []
        for record in records:
            result.append({
                'id': record.id,
                'service_date': record.service_date,
                'category_name': record.category.category_name,
                'service_type_name': record.service_type.service_type_name,
                'follow_up_date': record.follow_up_date,
                'fee': str(record.fee) if record.fee else None,
                'image_path': record.image_path,
                'profile_id': record.profile_id
            })

        return result

    except SQLAlchemyError as e:
        raise RuntimeError(f"Database error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error: {str(e)}")
    
    
def records_by_category(profile_id, category_id):
    try:
        category = db.session.query(Category).filter_by(id=category_id).first()
        if not category:
            raise ValueError('Invalid category ID')

        records = db.session.query(MedicalRecord).join(Category).join(ServiceType).filter(
            MedicalRecord.category_id == category_id,
            MedicalRecord.profile_id == profile_id
        ).all()

        result = []
        for record in records:
            result.append({
                'id': record.id,
                'service_date': record.service_date,
                'category_name': record.category.category_name,
                'service_type_name': record.service_type.service_type_name,
                'follow_up_date': record.follow_up_date,
                'fee': str(record.fee) if record.fee else None,
                'image_path': record.image_path,
                'profile_id': record.profile_id
            })

        return result

    except SQLAlchemyError as e:
        raise RuntimeError(f"Database error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error: {str(e)}")


def records_by_service_type(profile_id, service_type_id):
    try:
        service_type = db.session.query(ServiceType).filter_by(id=service_type_id).first()
        if not service_type:
            raise ValueError('Invalid service type ID')

        records = db.session.query(MedicalRecord).join(Category).join(ServiceType).filter(
            MedicalRecord.service_type_id == service_type_id,
            MedicalRecord.profile_id == profile_id
        ).all()

        result = []
        for record in records:
            result.append({
                'id': record.id,
                'service_date': record.service_date,
                'category_name': record.category.category_name,
                'service_type_name': record.service_type.service_type_name,
                'follow_up_date': record.follow_up_date,
                'fee': str(record.fee) if record.fee else None,
                'image_path': record.image_path,
                'profile_id': record.profile_id
            })

        return result

    except SQLAlchemyError as e:
        raise RuntimeError(f"Database error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error: {str(e)}")



# def records_by_service_date_range(profile_id, start_date, end_date):
#     try:
#         if start_date > end_date:
#             raise ValueError('Start date cannot be after end date')
#         records = db.session.query(MedicalRecord).filter(
#             MedicalRecord.profile_id == profile_id,
#             MedicalRecord.service_date >= start_date,
#             MedicalRecord.service_date <= end_date
#         ).all()

#         result = []
#         for record in records:
#             result.append({
#                 'id': record.id,
#                 'service_date': record.service_date,
#                 'category_name': record.category.category_name,
#                 'service_type_name': record.service_type.service_type_name,
#                 'follow_up_date': record.follow_up_date,
#                 'fee': str(record.fee) if record.fee else None,
#                 'image_path': record.image_path,
#                 'profile_id': record.profile_id
#             })

#         return result

#     except SQLAlchemyError as e:
#         raise RuntimeError(f"Database error: {str(e)}")
#     except Exception as e:
#         raise RuntimeError(f"Error: {str(e)}")

