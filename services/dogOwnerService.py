import bcrypt
from models.dogOwner import DogOwner
from database import db
from sqlalchemy import select
from utils.util import encode_token

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def login(username, password):
    query = select(DogOwner).where(DogOwner.username == username)
    owner = db.session.execute(query).scalar_one_or_none()

    if owner and check_password(owner.password, password):
        auth_token = encode_token(owner.id)

        response = {
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token
        }
        return response

def save(owner_data):
    hashed_password = hash_password(owner_data['password'])
    new_owner = DogOwner(
        username=owner_data['username'],
        password=hashed_password,
        owner_name=owner_data['owner_name'],
        owner_email=owner_data['owner_email'],
        owner_phone=owner_data['owner_phone']
    )
    db.session.add(new_owner)
    db.session.commit()

    db.session.refresh(new_owner)
    return new_owner
