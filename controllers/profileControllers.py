from flask import request, jsonify
from models.schemas.profileSchema import profile_schema, profiles_schema
from models.schemas.dogOwnerSchema import dog_owner_schema
from services import profileService
from services import dogOwnerService
from services.profileService import get_profile_with_owner
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

def save(owner_id):
    try: 
        profile_data = profile_schema.load(request.json)
        profile_data['owner_id'] = owner_id 
    except ValidationError as e:
        return jsonify(e.messages), 400
    try:
        profile_saved = profileService.save(profile_data, owner_id)
        return profile_schema.jsonify(profile_saved), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    


def get_profile_with_owner(owner_id, profile_id):
    try:
        data = profileService.get_profile_with_owner(profile_id, owner_id)
        response = {
            'profile': profile_schema.dump(data['profile']),
            'owner': dog_owner_schema.dump(data['owner'])
        }
        return jsonify(response)
    except NoResultFound as e:
        return jsonify({'error': str(e)}), 404


def find_all(owner_id):
    try:
        all_profiles = profileService.find_all(owner_id)
        return profiles_schema.jsonify(all_profiles), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


def find_by_id(profile_id, owner_id):
    try:
        profile = profileService.find_by_id(profile_id, owner_id)
        return profile_schema.jsonify(profile), 200
    except profileService.NoResultFound as e:
        return jsonify({'error': str(e)}), 404


def update_profile(owner_id, profile_id):
    profile_data = request.json
    try:
        updated_profile = profileService.update_profile(profile_id, profile_data, owner_id)
        return jsonify(profile_schema.dump(updated_profile))
    except NoResultFound as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 500


def delete_profile(owner_id, profile_id):
    try:
        result = profileService.delete_profile(profile_id, owner_id)
        return jsonify(result), 200
    except NoResultFound as e:
        return jsonify({'error': str(e)}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 500

