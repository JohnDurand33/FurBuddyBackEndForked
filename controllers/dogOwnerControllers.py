from flask import request, jsonify
from models.schemas.dogOwnerSchema import dog_owner_schema
from models.dogOwner import DogOwner
from services import dogOwnerService
from services.dogOwnerService import update_owner_info, delete_owner_from_db, show_info
from marshmallow import ValidationError
from utils.util import token_required, handle_options


@handle_options
def login():
    try:
        credentials = request.json
        owner_email = credentials['owner_email']
        password = credentials['password']
        
        token = dogOwnerService.login(owner_email, password)
    except KeyError:
        return jsonify({'messages': 'Invalid payload, expecting user email and password'}), 401
    
    if token:
        return jsonify(token), 200
    else:
        return jsonify({'messages': "Invalid user email or password"}), 401
    

@handle_options
def save(): 
    try:
        owner_data = dog_owner_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    try:
        owner_saved = dogOwnerService.save(owner_data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    response = {
        "message": "Account was successfully created",
        "owner": dog_owner_schema.dump(owner_saved)
    }
    return jsonify(response), 201


@handle_options
@token_required
def show_owner_info(current_owner_id):
    try:
        result, status_code = dogOwnerService.show_info(current_owner_id)  
        if result is None:
            return jsonify({"message": "Owner not found"}), 404
        
        owner_data = result.get('owner') 
        if not owner_data:
            return jsonify({"message": "Owner data not found"}), 404

        response = {
            "owner_email": owner_data['owner_email'],
            "owner_name": owner_data['owner_name'],
            "owner_phone": owner_data['owner_phone']
        }
        return jsonify(response), status_code
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@handle_options
@token_required
def update_owner(current_owner_id, id):
    if current_owner_id != id:
        return jsonify({"message": "Unauthorized access"}), 403
    try:
        owner_data = request.json
        response, status_code = update_owner_info(id, owner_data)
        return jsonify(response), status_code
    except ValidationError as e:
        return jsonify(e.messages), 400

    
    
@handle_options
@token_required
def delete_owner(current_owner_id, id):
    if current_owner_id != id:
        return jsonify({"message": "Unauthorized access"}), 403

    response, status_code = delete_owner_from_db(id)
    if status_code == 404:
        return jsonify(response), 404
    return jsonify(response), status_code



