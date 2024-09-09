from flask import request, jsonify
from database import db
from models.schemas.profileSchema import profile_schema, profiles_schema
from models.profile import Profile
from models.schemas.dogOwnerSchema import dog_owner_schema
from models.schemas import profileSchema 
from services import profileService
from services.profileService import save, find_profile_by_id, find_all_profiles, update_profile, delete_profile
from services import dogOwnerService
from services.profileService import save
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from utils.util import token_required, handle_options




@handle_options
@token_required
def save_profile(current_owner_id):
    try:
        profile_data = profile_schema.load(request.json)
        profile_data['owner_id'] = current_owner_id
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    try:
        profile_saved = save(profile_data, current_owner_id)
        return profile_schema.jsonify(profile_saved), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@handle_options
@token_required
def find_by_id(current_owner_id, profile_id):
    try:
        profile = find_profile_by_id(profile_id)
        if profile.owner_id != current_owner_id:
            return jsonify({"message": "Unauthorized"}), 403
        
        profile_data = {
            'id': profile.id,
            'name': profile.name,
            'date_of_birth': profile.date_of_birth.isoformat() if profile.date_of_birth else None,
            'sex': profile.sex,
            'fixed': profile.fixed,
            'breed': profile.breed,
            'weight': profile.weight,
            'chip_number': profile.chip_number,
            'image_path': profile.image_path,
            'vet_clinic_name': profile.vet_clinic_name,
            'vet_clinic_phone': profile.vet_clinic_phone,
            'vet_clinic_email': profile.vet_clinic_email,
            'vet_doctor_name': profile.vet_doctor_name,
            'owner_id': profile.owner_id
        }
        return jsonify({"profile": profile_data}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 404
    
    
@handle_options
@token_required
def find_all(current_owner_id):
    try:
        profiles = db.session.query(Profile).filter(Profile.owner_id == current_owner_id).all()
        if not profiles:
            return jsonify({"message": "No profiles found for the given owner."}), 404
        result = profiles_schema.dump(profiles)
        return jsonify(result), 200
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        return jsonify({'error': f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@handle_options
@token_required
def update_profile_info(current_owner_id, profile_id):
    profile_data = request.json
    
    try:
        profile = find_profile_by_id(profile_id)
        if profile.owner_id != current_owner_id:
            return jsonify({"message": "Unauthorized"}), 403
        
        updated_profile = update_profile(profile_id, profile_data)
        return profile_schema.jsonify(updated_profile), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400



@handle_options
@token_required
def delete_profile_info(current_owner_id, profile_id):
    try:
        profile = find_profile_by_id(profile_id)
        if profile.owner_id != current_owner_id:
            return jsonify({"message": "Unauthorized"}), 403
        
        delete_profile(profile_id)
        return jsonify({"message": "Profile deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


