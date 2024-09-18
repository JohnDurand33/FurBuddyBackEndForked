from flask import request, jsonify
import os
from flask import current_app
from database import db
from datetime import date
from services.medicalRecordService import create_medical_record, get_medical_record_by_id, update_medical_record, delete_medical_record_by_id, get_paginated_records, filtered_records
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
def get_categories():
    try:
        categories = db.session.query(Category).all()
        result = [{'id': cat.id, 'category_name': cat.category_name} for cat in categories]
        return jsonify(result)
    except SQLAlchemyError as e:
        return jsonify({'message': str(e)}), 500
    

@handle_options
def get_service_types():
    try:
        service_types = db.session.query(ServiceType).all()
        result = [
            {
                'id': st.id,
                'name': st.service_type_name,
                'category_id': st.category_id
            } 
            for st in service_types
        ]
        return jsonify(result)
    except SQLAlchemyError as e:
        return jsonify({'message': str(e)}), 500
    

@handle_options
def get_service_types_by_category(category_id):
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
def add_medical_record(current_owner_id, profile_id):
    json_data = request.get_json()
    try:
        data = medical_record_schema.load(json_data)
        if profile_id != data['profile_id']:
            return jsonify({'message': 'Profile ID mismatch'}), 400

        new_record = create_medical_record(current_owner_id, data)
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
def get_medical_record(current_owner_id, profile_id, record_id):
    try:
        record = get_medical_record_by_id(record_id, profile_id)

        if record.profile.owner_id != current_owner_id:
            return jsonify({'message': 'Unauthorized access to this record'}), 403

        response_data = {
            'record_id': record.id,
            'service_date': record.service_date,
            'category_name': record.category.category_name if record.category else None,
            'service_type_name': record.service_type.service_type_name if record.service_type else None,
            'follow_up_date': record.follow_up_date,
            'fee': str(record.fee) if record.fee else None,
            'image_path': record.image_path,
            'profile_id': record.profile_id,
            'profile_name': record.profile.name if record.profile else None  ,
            'service_type_id': record.service_type_id,
            'category_id': record.category_id
        }

        return jsonify(response_data)
    except ValueError as e:
        return jsonify({'message': str(e)}), 404
    except SQLAlchemyError as e:
        return jsonify({'message': str(e)}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
 

@handle_options
@token_required
def edit_medical_record(current_owner_id, profile_id, record_id):
    json_data = request.get_json()
    try:
        data = medical_record_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        updated_record = update_medical_record(current_owner_id, profile_id, record_id, data)
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
def delete_medical_record(current_owner_id, profile_id, record_id):
    try:
        delete_medical_record_by_id(current_owner_id, profile_id, record_id)
        return jsonify({'message': 'Record deleted successfully'})

    except ValueError as ve:
        return jsonify({'message': str(ve)}), 404
    except SQLAlchemyError as e:
        return jsonify({'message': str(e)}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
    

# @handle_options
# @token_required
# def get_medical_records(current_owner_id, profile_id):
#     try:
#         records = db.session.query(MedicalRecord).join(Category).join(ServiceType).filter(MedicalRecord.profile_id == profile_id).all()
#         profile = db.session.query(Profile).filter(Profile.id == profile_id).first()
#         if not profile or profile.owner_id != current_owner_id:
#             return jsonify({'message': 'Unauthorized access to this profile'}), 403
        
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
#         return jsonify(result)

#     except SQLAlchemyError as e:
#         return jsonify({'message': str(e)}), 500
#     except Exception as e:
#         return jsonify({'message': str(e)}), 500

    
@handle_options
@token_required
def get_medical_records(current_owner_id, profile_id):
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', default=0, type=int)

    try:
        records = get_paginated_records(page, limit, offset, profile_id)
        return jsonify(records)
    except RuntimeError as re:
        return jsonify({'message': str(re)}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    


@handle_options
@token_required
def get_filtered_records(current_owner_id, profile_id):
    category_id = request.args.get('category_id', type=int)
    service_type_id = request.args.get('service_type_id', type=int)

    if category_id is None and service_type_id is None:
        return jsonify({"error": "At least one filter parameter (category_id or service_type_id) is required."}), 400

    try:
        records = filtered_records(profile_id, category_id, service_type_id)
        return jsonify(records), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500  

