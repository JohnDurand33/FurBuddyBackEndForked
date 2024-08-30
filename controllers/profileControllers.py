from flask import request, jsonify
from database import db
from models.schemas.profileSchema import profile_schema, profiles_schema
from models.profile import Profile
from models.schemas.dogOwnerSchema import dog_owner_schema
from models.schemas import profileSchema 
from services import profileService
from services.profileService import save, find_profile_by_id, update_profile, delete_profile
from services import dogOwnerService
from services.profileService import save
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound
from utils.util import token_required, handle_options


def save_profile(owner_id):
    try: 
        profile_data = profile_schema.load(request.json)
        profile_data['owner_id'] = owner_id 
    except ValidationError as e:
        return jsonify(e.messages), 400
    try:
        profile_saved = save(profile_data, owner_id)
        return profile_schema.jsonify(profile_saved), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    

    
@token_required
def find_by_id(current_owner_id, owner_id, profile_id):
    if current_owner_id != owner_id:
        return jsonify({"message": "Unauthorized"}), 403
    
    try:
        profile = find_profile_by_id(profile_id)
        if profile.owner_id != owner_id:
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
    

@token_required
def update_profile_info(current_owner_id, owner_id, profile_id):
    if current_owner_id != owner_id:
        return jsonify({"message": "Unauthorized"}), 403

    profile_data = request.json
    
    profile = db.session.get(Profile, profile_id)
    if not profile or profile.owner_id != owner_id:
        return jsonify({"message": "Profile not found or unauthorized"}), 404
    
    try:
        updated_profile = update_profile(profile_id, profile_data)
        return profile_schema.jsonify(updated_profile), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    
    
@token_required
def delete_profile_info(current_owner_id, owner_id, profile_id):
    profile = db.session.get(Profile, profile_id)
    if not profile:
        return jsonify({"message": "Profile not found"}), 404

    if profile.owner_id != owner_id:
        return jsonify({"message": "Unauthorized"}), 403

    try:
        delete_profile(profile_id)
        return jsonify({"message": "Profile deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    
    

# @token_required
# def get_profile_with_owner(current_owner_id, profile_id):
#     try:
#         data = profileService.get_profile_with_owner(profile_id, current_owner_id)
#         response = {
#             'profile': profile_schema.dump(data['profile']),
#             'owner': dog_owner_schema.dump(data['owner'])
#         }
#         return jsonify(response), 200
#     except NoResultFound as e:
#         return jsonify({'error': str(e)}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    
# @token_required
# def get_all_profiles(current_owner_id):
#     try:
#         profiles = find_all_profiles(current_owner_id)
#         return profiles_schema.jsonify(profiles), 200
#     except ValueError as e:
#         return jsonify({'error': str(e)}), 400
    

# @token_required
# def find_all(owner_id):
#     try:
#         all_profiles = find_all_profiles(owner_id, db)
#         profiles_schema = profileSchema(many=True)
#         result = profiles_schema.dump(all_profiles)
#         return jsonify(result), 200
#     except ValueError as e:
#         return jsonify({'error': str(e)}), 400
    

