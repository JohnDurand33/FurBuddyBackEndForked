from flask import request, jsonify
import os
from flask import current_app
from database import db
from services.medicalRecordService import create_medical_record, get_medical_record, update_medical_record, delete_medical_record, get_paginated_records, records_by_service_type, records_by_category
from models.schemas.medicalRecordSchema import CategorySchema, medical_record_schema, medical_records_schema
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
        categories = db.session.query(Category).all()
        result = [{'id': cat.id, 'category_name': cat.category_name} for cat in categories]
        return jsonify(result)
    except SQLAlchemyError as e:
        return jsonify({'message': str(e)}), 500
    

@handle_options
@token_required
def get_service_types(current_owner_id):
    try:
        service_types = db.session.query(ServiceType).all()
        result = [{'id': st.id, 'name': st.service_type_name} for st in service_types]
        return jsonify(result)
    except SQLAlchemyError as e:
        return jsonify({'message': str(e)}), 500
    

@handle_options
@token_required
def get_service_types_by_category(current_owner_id, category_id):
    try:
        category = db.session.query(Category).filter_by(id=category_id).first()
        if not category:
            return jsonify({'message': 'Invalid category ID'}), 400

        service_types = db.session.query(ServiceType).filter_by(category_id=category_id).all()
        result = [{'id': st.id, 'name': st.service_type_name} for st in service_types]

        return jsonify(result)

    except SQLAlchemyError as e:
        return jsonify({'message': str(e)}), 500
    except Exception as e:
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

        category = db.session.query(Category).filter_by(id=data['category_id']).first()
        if not category:
            return jsonify({'message': 'Invalid category ID'}), 400

        service_type = db.session.query(ServiceType).filter_by(id=data['service_type_id']).first()
        if not service_type:
            return jsonify({'message': 'Invalid service type ID'}), 400

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
        record = db.session.query(MedicalRecord).join(Category).join(ServiceType).filter(MedicalRecord.id == record_id).first()
        
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
        updated_record = update_medical_record(current_owner_id, record_id, data)
        result = {
            'service_date': updated_record.service_date,
            'category_name': updated_record.category.category_name if updated_record.category else None,
            'service_type_name': updated_record.service_type.service_type_name if updated_record.service_type else None,
            'follow_up_date': updated_record.follow_up_date,
            'fee': str(updated_record.fee) if updated_record.fee else None,
            'image_path': updated_record.image_path,
            'profile_id': updated_record.profile_id
        }
        return jsonify({'message': 'Record updated successfully', 'record': result})

    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400
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
def get_medical_records(current_owner_id):
    try:
        records = db.session.query(MedicalRecord).join(Category).join(ServiceType).all()
        result = []
        for record in records:
            result.append({
                'id': record.id,
                'service_date': record.service_date,
                'category_name': record.category.category_name,
                'service_type_name': record.service_type.service_type_name,
                'follow_up_date': record.follow_up_date,
                'fee': record.fee,
                'image_path': record.image_path,
                'profile_id': record.profile_id
            })
        return jsonify(result)
    except SQLAlchemyError as e:
        return jsonify({'message': str(e)}), 500
    
    
@handle_options
@token_required
def get_paginated_medical_records(current_owner_id):
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    try:
        records = get_paginated_records(page, per_page)
        return jsonify(records)
    except RuntimeError as re:
        return jsonify({'message': str(re)}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
    

@handle_options
@token_required
def get_records_by_category(current_owner_id, category_id):
    try:
        records = records_by_category(category_id)
        return jsonify(records)
    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400
    except RuntimeError as re:
        return jsonify({'message': str(re)}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
    
    
@handle_options
@token_required
def get_records_by_service_type(current_owner_id, service_type_id):
    try:
        records = records_by_service_type(service_type_id)
        return jsonify(records)
    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400
    except RuntimeError as re:
        return jsonify({'message': str(re)}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
    

    

