import os
from database import db
from werkzeug.utils import secure_filename
from flask import current_app
from models.medicalRecord import Category, ServiceType, MedicalRecord
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError



def create_medical_record(data):
    new_record = MedicalRecord(
        service_date=data['service_date'],
        category_id=data['category_id'],
        service_type_id=data['service_type_id'],
        follow_up_date=data.get('follow_up_date'),
        fee=data.get('fee'),
        image_path=data.get('image_path'),  
        profile_id=data['profile_id']
    )
    
    db.session.add(new_record)
    db.session.commit()
    

def get_medical_record(record_id):
    return MedicalRecord.query.get(record_id)


def update_medical_record(record, data):
    record.service_date = data.get('service_date', record.service_date)
    record.category_id = data.get('category_id', record.category_id)
    record.service_type_id = data.get('service_type_id', record.service_type_id)
    record.follow_up_date = data.get('follow_up_date', record.follow_up_date)
    record.fee = data.get('fee', record.fee)
    record.image_path = data.get('image_path', record.image_path)
    record.profile_id = data.get('profile_id', record.profile_id)
    
    db.session.commit()


def delete_medical_record(record):
    db.session.delete(record)
    db.session.commit()
    
    
def get_medical_records(current_owner_id, page=1, per_page=10):
    try:
        page = int(page)
        per_page = int(per_page)
        
        records_query = db.session.query(MedicalRecord).filter_by(profile_id=current_owner_id)
        
        paginated_records = records_query.paginate(page, per_page, False)
        
        records = [{
            'service_date': record.service_date,
            'category_name': record.category.category_name if record.category else None,
            'service_type_name': record.service_type.service_type_name if record.service_type else None,
            'follow_up_date': record.follow_up_date,
            'fee': str(record.fee) if record.fee else None,
            'image_path': record.image_path,
            'profile_id': record.profile_id
        } for record in paginated_records.items]
        
        response = {
            'total': paginated_records.total,
            'pages': paginated_records.pages,
            'current_page': paginated_records.page,
            'records': records
        }
        
        return response

    except SQLAlchemyError as e:
        return {'message': str(e)}, 500
    except Exception as e:
        return {'message': str(e)}, 500

    
def get_records_by_category(category_id, profile_id):
    try:
        records = MedicalRecord.query.filter_by(category_id=category_id, profile_id=profile_id).all()
        return records
    except SQLAlchemyError as e:
        raise Exception(f"Database query failed: {str(e)}")
    
    
def get_records_by_service_type(service_type_id, profile_id):
    try:
        records = MedicalRecord.query.filter_by(service_type_id=service_type_id, profile_id=profile_id).all()
        return records
    except SQLAlchemyError as e:
        raise Exception(f"Database query failed: {str(e)}")
