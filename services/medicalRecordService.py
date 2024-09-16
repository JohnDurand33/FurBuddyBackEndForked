import os
from database import db
from flask import jsonify, request
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
from sqlalchemy.dialects import mysql



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
    print('in the update service')
    record = db.session.query(MedicalRecord).join(Profile).filter(MedicalRecord.id == record_id, MedicalRecord.profile_id == profile_id).first()
    if not record:
        raise ValueError('Record not found or unauthorized access')
    
    if record.profile.owner_id != current_owner_id:
        raise ValueError('Unauthorized access to this record')
    
    if 'service_date' in data:
        print('service date in data')
        record.service_date = data['service_date']
    if 'category_id' in data:
        print('category id in data')
        category = db.session.query(Category).filter_by(id=data['category_id']).first()
        if not category:
            raise ValueError('Invalid category ID')
        record.category_id = data['category_id']
        print(f'category id: {category.id}')
    if 'service_type_id' in data:
        print('service type id in data')
        service_type = db.session.query(ServiceType).filter_by(id=data['service_type_id']).first()
        if not service_type:
            raise ValueError('Invalid service type ID')
        record.service_type_id = data['service_type_id']
        print(f'service type id: {service_type.id}')
    if 'follow_up_date' in data:
        record.follow_up_date = data['follow_up_date']
        print(f'follow up date: {record.follow_up_date}')
    if 'fee' in data:
        print('fee in data')
        record.fee = data['fee']
    if 'image_path' in data:
        print('image path in data')
        record.image_path = data['image_path']
        print(f'image path: {record.image_path}')
    print('about to commit')
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Database error: {str(e)}")
    print('committed')
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
    
    
# def get_paginated_records(page, limit, offset, profile_id=None):
#     try:
#         # Calculate offset based on page and limit
#         if page is not None and limit is not None:
#             offset = (page - 1) * limit
        
#         # Build the base query
#         query = db.session.query(MedicalRecord).join(Category).join(ServiceType).filter(MedicalRecord.profile_id == profile_id)

#         # Apply pagination
#         records = query.offset(offset).limit(limit).all()

#         # Format the result
#         result = []
#         for record in records:
#             result.append({
#                 'id': record.id,
#                 'service_date': record.service_date,
#                 'category_name': record.category.category_name if record.category else None,
#                 'service_type_name': record.service_type.service_type_name if record.service_type else None,
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

     

def get_paginated_records(page, limit, offset, profile_id=None):
    try:
        query = db.session.query(MedicalRecord).join(Category).join(ServiceType, MedicalRecord.service_type_id == ServiceType.id).filter(
            MedicalRecord.profile_id == profile_id).limit(limit).offset(offset)
        print(query)
        
        records = query.all()

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
    



def filtered_records(profile_id, category_id=None, service_type_id=None):
    query = db.session.query(MedicalRecord).filter_by(profile_id=profile_id)
    
    if category_id is not None:
        query = query.filter_by(category_id=category_id)
    
    if service_type_id is not None:
        query = query.filter_by(service_type_id=service_type_id)
    
    records = query.all()
    
    records = [{
            'id': record.id,
            'service_date': record.service_date,
            'category_name': record.category.category_name if record.category else None,
            'service_type_name': record.service_type.service_type_name if record.service_type else None,
            'follow_up_date': record.follow_up_date if record.follow_up_date else None,
            'fee': str(record.fee) if record.fee else None,
            'image_path': record.image_path,
            'profile_id': record.profile_id
    } for record in records]
    return records