from flask import request, jsonify
from models.schemas.dogOwnerSchema import dog_owner_schema
from services import dogOwnerService
from services.dogOwnerService import update_owner, delete_owner
from marshmallow import ValidationError


def login():
    try:
        credentials = request.json
        username = credentials['username']
        password = credentials['password']
        
        token = dogOwnerService.login(username, password)
    except KeyError:
        return jsonify({'messages': 'Invalid payload, expecting username and password'}), 401
    
    if token:
        return jsonify(token), 200
    else:
        return jsonify({'messages': "Invalid username or password"}), 401
    
    
def save(): 
    try:
        owner_data = dog_owner_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    owner_saved = dogOwnerService.save(owner_data)
    return dog_owner_schema.jsonify(owner_saved), 201

def update_owner(id):
    try:
        owner_data = request.json
        updated_owner = dogOwnerService.update_owner(id, owner_data)
        if updated_owner:
            return dog_owner_schema.jsonify(updated_owner), 200
        else:
            return jsonify({"message": "Dog owner not found"}), 404
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    
def delete_owner(id):
    try:
        success = dogOwnerService.delete_owner(id)
        if success:
            return jsonify({"message": "Dog owner removed successfully"}), 200
        else:
            return jsonify({"message": "Dog owner not found"}), 404
    except ValidationError as e:
        return jsonify(e.messages), 400

