from flask import request, jsonify
from models.schemas.dogOwnerSchema import dog_owner_schema
from services import dogOwnerService 
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
