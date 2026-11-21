from functools import wraps
from flask import g, request, jsonify
import jwt
from config import JWT_SECRET, JWT_ALGORITHM

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token")
        if not token:
            return jsonify({"error": "non authentifié"}), 401
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM],
                              options={"require": ["exp", "sub"]})
        except jwt.InvalidTokenError:
            return jsonify({"error": "non authentifié"}), 401
        g.user_id = int(data["sub"])
        return f(*args, **kwargs)
    return wrapper


