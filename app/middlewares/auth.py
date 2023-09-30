from flask import request, jsonify
from app import app
from functools import wraps
import jwt

def jwt_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # Decode the token and get the user ID
            payload = jwt.decode(token, app.config['SECRET_KEY'])
            user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        # Add the user_id to the kwargs so it's available in the route
        kwargs['user_id'] = user_id
        return func(*args, **kwargs)

    return decorated