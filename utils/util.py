from datetime import datetime, timedelta, timezone
from secrets import token_bytes
import jwt
from flask import jsonify, request, make_response
from functools import wraps 

SECRET_KEY = "super_secret_secrets"

def encode_token(owner_id): 
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0,hours=1), 
        'iat': datetime.now(timezone.utc), 
        'sub': owner_id,
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(func): 
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]  
        else:
            return jsonify({"message": "Token is missing"}), 401

        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                current_owner_id = payload['sub']
                return func(current_owner_id, *args, **kwargs)  
            except jwt.ExpiredSignatureError:
                return jsonify({'message': "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid token"}), 401
        return jsonify({"message": "Token is missing"}), 401
    
    return wrapper


def handle_options(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'OPTIONS':
            return jsonify({'message': 'CORS preflight request'}), 200
        return f(*args, **kwargs)
    return decorated_function


