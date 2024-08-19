from flask import request, jsonify
from models.schemas.profileSchema import profile_schema, profiles_schema
from services import profileService
from marshmallow import ValidationError

def save():
    try: 
        profile_data = profile_schema.load(request.form)
        image_file = request.files.get('image')
    except ValidationError as e:
        return jsonify(e.messages), 400
    profile_saved = profileService.save(profile_data, image_file)
    return profile_schema.jsonify(profile_data), 201


def find_all():
    all_profiles = profileService.find_all()
    return profiles_schema.jsonify(all_profiles), 200


def find_by_id(profile_id):
    try:
        profile = profileService.find_by_id(profile_id)
    except profileService.NoResultFound as e:
        return jsonify({'error': str(e)}), 404

    return profile_schema.jsonify(profile), 200

def update(profile_id):
    try:
        profile_data = profile_schema.load(request.form, partial=True)
        image_file = request.files.get('image')
    except ValidationError as e:
        return jsonify(e.messages), 400

    try:
        updated_profile = profileService.update(profile_id, profile_data, image_file)
    except profileService.NoResultFound as e:
        return jsonify({'error': str(e)}), 404

    return profile_schema.jsonify(updated_profile), 200

def delete(profile_id):
    try:
        profileService.delete(profile_id)
        return jsonify({'message': 'Profile was successfully deleted'}), 200
    except profileService.NoResultFound as e:
        return jsonify({'error': str(e)}), 404
