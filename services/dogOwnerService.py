import bcrypt
from flask import request, jsonify
from models.dogOwner import DogOwner
from database import db
from sqlalchemy import select, delete
from utils.util import encode_token, token_required


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, password):
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def login(owner_email, password):
    query = select(DogOwner).where(DogOwner.owner_email == owner_email)
    owner = db.session.execute(query).scalar_one_or_none()

    if owner and check_password(owner.password, password):
        auth_token = encode_token(owner.id)
        return {
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token
        }
    return None


def save(owner_data):
    hashed_password = hash_password(owner_data['password'])
    new_owner = DogOwner(
        password=hashed_password,
        owner_name=owner_data['owner_name'],
        owner_email=owner_data['owner_email'],
        owner_phone=owner_data['owner_phone']
    )
    db.session.add(new_owner)
    db.session.commit()

    db.session.refresh(new_owner)
    return new_owner


@token_required
def update_owner(current_owner_id, owner_data):
    owner = db.session.query(DogOwner).filter(DogOwner.id == current_owner_id).first()
    if owner:
        for key, value in owner_data.items():
            setattr(owner, key, value)
        db.session.commit()
        db.session.refresh(owner)
        return owner
    else:
        return None

   
@token_required
def delete_owner(current_owner_id):
    query = delete(DogOwner).filter(DogOwner.id == current_owner_id)
    db.session.execute(query)
    db.session.commit()
    return {'message': 'Dog owner deleted successfully'}, 200
   