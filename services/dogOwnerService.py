import bcrypt
from flask import request, jsonify
from models.dogOwner import DogOwner
from models.schemas.dogOwnerSchema import dog_owner_schema 
from database import db
from sqlalchemy import select, delete
from utils.util import encode_token
from utils.util import handle_options
from sqlalchemy.exc import SQLAlchemyError


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
    print('Inservice')
    hashed_password = hash_password(owner_data['password'])
    new_owner = DogOwner(
        password=hashed_password,
        owner_email=owner_data['owner_email'],
        owner_name=owner_data.get('owner_name'),
        owner_phone=owner_data.get('owner_phone')
    )
    db.session.add(new_owner)
    db.session.commit()
    db.session.refresh(new_owner)
    print('Usercreated')
    return new_owner



def show_info(id):
    try:
        owner = db.session.query(DogOwner).filter(DogOwner.id == id).first()
        if not owner:
            raise ValueError("Owner not found")
        return {
            "owner": dog_owner_schema.dump(owner)  
        }, 200
    except SQLAlchemyError as e:
        raise ValueError(f"Database error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error retrieving owner: {str(e)}")



def update_owner_info(id, owner_data):
    try:
        owner = db.session.query(DogOwner).filter(DogOwner.id == id).first()
        if owner:
            for key, value in owner_data.items():
                setattr(owner, key, value)
            db.session.commit()
            db.session.refresh(owner)
            return {
                "message": "Account information was successfully updated",
                "owner": dog_owner_schema.dump(owner)  
            }, 200
        else:
            return {"message": "Owner not found"}, 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"message": str(e)}, 500


def delete_owner_from_db(id):
    try:
        print(f"Attempting to delete owner with ID: {id}")
        query = delete(DogOwner).filter(DogOwner.id == id)
        result = db.session.execute(query)
        db.session.commit()
        print(f"Rows affected: {result.rowcount}")
        if result.rowcount == 0:
            return {"message": "Owner not found"}, 404
        return {'message': 'Owner deleted successfully'}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"message": str(e)}, 500