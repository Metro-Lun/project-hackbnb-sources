from flask import jsonify, Blueprint, request
from database.init import db
from api.users.users_models import User

import jwt
from datetime import datetime, timedelta, timezone
from config import IS_PROD, JWT_SECRET, JWT_ALGORITHM, JWT_TTL

auth_api = Blueprint('auth', __name__)

@auth_api.route('/login', methods=['POST'])
def login():
    if "email" not in request.json:
        return {'error': 'Missing email'}, 400
    if "password" not in request.json:
        return {'error': 'Missing password'}, 400

    # Check if user exists
    user: User = User.query.where(User.email == request.json["email"]).first()
    if not user:
        return {'error': 'User not found'}, 404
    
     # Check if user exists
    if not user.is_valid_password(request.json["password"]):
        return {'error': 'Invalid password'}, 401

    res = jsonify({})

    now = datetime.now(timezone.utc)
    token = jwt.encode(
        {
            "sub": str(user.id),
            "iat": now,
            "exp": now + timedelta(seconds=JWT_TTL),
        },
        JWT_SECRET,
        JWT_ALGORITHM
    )

    res.set_cookie("token", token, httponly=True, secure=IS_PROD, samesite="Strict")

    return res

@auth_api.route('/register', methods=['POST'])
def create_account():
    if "name" not in request.json:
        return {'error': 'Missing name'}, 400
    if "email" not in request.json:
        return {'error': 'Missing email'}, 400
    if "password" not in request.json:
        return {'error': 'Missing password'}, 400

    # Error if user already exists
    existing_user: User = User.query.where(User.email == request.json["email"]).first()
    if existing_user:
        return {'error': 'User with same email already exists'}, 409

    user = User(
        name=request.json["name"],
        email=request.json["email"],
    )

    user.set_password(request.json["password"])
    
    # Create user in database
    db.session.add(user)
    db.session.commit()

    return jsonify({})

@auth_api.route("/logout", methods=["POST"])
def logout():
    res = jsonify({})
    res.delete_cookie("token")
    return res

