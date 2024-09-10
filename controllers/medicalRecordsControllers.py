from flask import request, jsonify
import os
from flask import current_app
from database import db
from werkzeug.utils import secure_filename
from services.medicalRecordService import create_medical_record, get_medical_record, get_medical_records, update_medical_record, delete_medical_record
from models.schemas.medicalRecordSchema import CategorySchema, medical_record_schema
from models.medicalRecord import MedicalRecord
from models.medicalRecord import ServiceType
from models.medicalRecord import Category
from models.profile import Profile
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from utils.util import token_required, handle_options


@handle_options
@token_required
def get_categories(current_owner_id):
    try:
        categories = Category.query.all()
        result = [{'id': cat.id, 'category_name': cat.category_name} for cat in categories]
        return jsonify(result)
    except SQLAlchemyError as e:
        return jsonify({'message': str(e)}), 500
    

@handle_options
@token_required
def get_service_types(current_owner_id):
    try:
        service_types = ServiceType.query.all()
        result = [{'id': st.id, 'name': st.service_type_name} for st in service_types]
        return jsonify(result)
    except SQLAlchemyError as e:
        return jsonify({'message': str(e)}), 500


@handle_options
@token_required
def add_medical_record(current_owner_id):
    json_data = request.get_json()

    try:
        data = medical_record_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        profile = db.session.query(Profile).get(data['profile_id'])
        if not profile or profile.owner_id != current_owner_id:
            return jsonify({'message': 'Unauthorized access to this profile'}), 403

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

        result = medical_record_schema.dump(new_record)

        return jsonify({'message': 'Record added successfully', 'record': result}), 201

    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400
    except SQLAlchemyError as e:
        return jsonify({'message': str(e)}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@handle_options
@token_required
def get_medical_record(current_owner_id, record_id):
    try:
        record = db.session.query(MedicalRecord).filter_by(id=record_id).first()
        
        if not record:
            return jsonify({'message': 'Record not found'}), 404

        if record.profile.owner_id != current_owner_id:
            return jsonify({'message': 'Unauthorized access to this record'}), 403

        response_data = {
            'service_date': record.service_date,
            'category_name': record.category.category_name if record.category else None,
            'service_type_name': record.service_type.service_type_name if record.service_type else None,
            'follow_up_date': record.follow_up_date,
            'fee': str(record.fee) if record.fee else None,
            'image_path': record.image_path,
            'profile_id': record.profile_id
        }

        return jsonify(response_data)

    except SQLAlchemyError as e:
        return jsonify({'message': str(e)}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
    

@handle_options
@token_required
def edit_medical_record(current_owner_id, record_id):
    json_data = request.get_json()

    try:
        data = medical_record_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        record = db.session.query(MedicalRecord).get(record_id)
        if not record:
            return jsonify({'message': 'Record not found'}), 404
        
        if record.profile.owner_id != current_owner_id:
            return jsonify({'message': 'Unauthorized access to this record'}), 403
        
        record.service_date = data.get('service_date', record.service_date)
        record.category_id = data.get('category_id', record.category_id)
        record.service_type_id = data.get('service_type_id', record.service_type_id)
        record.follow_up_date = data.get('follow_up_date', record.follow_up_date)
        record.fee = data.get('fee', record.fee)
        record.image_path = data.get('image_path', record.image_path)
        record.profile_id = data.get('profile_id', record.profile_id)

        db.session.commit()

        result = medical_record_schema.dump(record)
        return jsonify({'message': 'Record updated successfully', 'record': result})

    except SQLAlchemyError as e:
        return jsonify({'message': str(e)}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@handle_options
@token_required
def delete_medical_record(current_owner_id, record_id):
    try:
        record = db.session.query(MedicalRecord).get(record_id)
        if not record:
            return jsonify({'message': 'Record not found'}), 404

        if record.profile.owner_id != current_owner_id:
            return jsonify({'message': 'Unauthorized access to this record'}), 403

        db.session.delete(record)
        db.session.commit()

        return jsonify({'message': 'Record deleted successfully'})

    except SQLAlchemyError as e:
        return jsonify({'message': str(e)}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
    

@handle_options
@token_required
def get_paginated_medical_records(current_owner_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    try:
        result = get_medical_records(current_owner_id, page, per_page)
        
        if isinstance(result, dict) and 'message' in result:
            return jsonify(result), 500
        
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
    
    
@handle_options
@token_required
def filter_records_by_category(current_owner_id, category_id):
    print(f"Current Owner ID: {current_owner_id}, Category ID: {category_id}")
    try:
        records = db.session.query(MedicalRecord).filter_by(category_id=category_id, profile_id=current_owner_id).all()
        
        if not records:
            print("No records found.")
            return jsonify({'message': 'No records found'}), 404

        result = [{
            'id': record.id,
            'service_date': record.service_date,
            'service_type': record.service_type.service_type_name if record.service_type else None,
            'follow_up_date': record.follow_up_date,
            'fee': str(record.fee),
            'image_path': record.image_path,
            'profile_id': record.profile_id
        } for record in records]

        return jsonify(result)
        
    except SQLAlchemyError as e:
        return jsonify({'message': str(e)}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@handle_options
@token_required
def filter_records_by_service_type(service_type_id, current_owner_id):
    try:
        records = db.session.query(MedicalRecord).filter_by(service_type_id=service_type_id, profile_id=current_owner_id).all()
        if not records:
            print("No records found.")
            return jsonify({'message': 'No records found'}), 404
    
        result = [{
            'id': record.id,
            'service_date': record.service_date,
            'category': record.category.category_name,
            'follow_up_date': record.follow_up_date,
            'fee': str(record.fee),
            'image_path': record.image_path,
            'profile_id': record.profile_id
        } for record in records]
        return jsonify(result)
    
    except SQLAlchemyError as e:
        return jsonify({'message': str(e)}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@handle_options
def get_service_types_by_category(category_id):
    try:
        service_types = db.session.query(ServiceType).filter_by(category_id=category_id).all()
        if not service_types:
            return jsonify({'message': 'No service types found for this category'}), 404

        result = [{
            'id': service_type.id,
            'service_type_name': service_type.service_type_name
        } for service_type in service_types]

        return jsonify(result)

    except Exception as e:
        return jsonify({'message': str(e)}), 500

