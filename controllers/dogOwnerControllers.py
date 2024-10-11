from flask import request, jsonify
from models.schemas.dogOwnerSchema import dog_owner_schema
from models.dogOwner import DogOwner
from services import dogOwnerService
from services.dogOwnerService import update_owner_info, delete_owner_from_db, show_info
from marshmallow import ValidationError
from utils.util import token_required, handle_options




def login():
    try:
        credentials = request.json
        owner_email = credentials['owner_email']
        password = credentials['password']
        
        token = dogOwnerService.login(owner_email, password)
    except KeyError:
        print(KeyError)
        return jsonify({'messages': 'Invalid payload, expecting user email and password'}), 401
    
    if token:
        return jsonify(token), 200
    else:
        return jsonify({'messages': "Invalid user email or password"}), 401
    

def save(): 
    print('In controller') 
    print('Request JSON:', request.json)
    try:
        owner_data = dog_owner_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    print('schema pulled')
    try:
        owner_saved = dogOwnerService.save(owner_data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    print('owner saved')
    response = {
        "message": "Account was successfully created",
        "owner": dog_owner_schema.dump(owner_saved)
    }
    print('response completed')
    return jsonify(response), 201



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
            "id": owner_data['id'],
            "owner_email": owner_data['owner_email'],
            "owner_name": owner_data['owner_name'],
            "owner_phone": owner_data['owner_phone']
        }
        return jsonify(response), status_code
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



@token_required
def update_owner(current_owner_id):
    try:
        owner_data = request.json
        updated_owner, status_code = dogOwnerService.update_owner_info(current_owner_id, owner_data)
        return jsonify(updated_owner), status_code
    except ValidationError as e:
        return jsonify(e.messages), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@token_required
def delete_owner(current_owner_id):
    print(f"Attempting to delete owner with ID: {current_owner_id}") 
    try:
        response, status_code = dogOwnerService.delete_owner_from_db(current_owner_id)
        return jsonify(response), status_code
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
