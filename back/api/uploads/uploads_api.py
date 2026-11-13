import os
from flask import Blueprint, request, send_from_directory, abort, current_app

uploads_api = Blueprint('uploads', __name__)
ALLOWED_EXT = {'.jpg', '.jpeg', '.png', '.webp'}

@uploads_api.route('/')
def get_upload():
    name = request.args.get('name')
    if not name:
        abort(400)

    safe_name = os.path.basename(name)
    if os.path.splitext(safe_name)[1].lower() not in ALLOWED_EXT:
        abort(403)

    upload_dir = os.path.join(current_app.root_path, 'uploads')
    return send_from_directory(upload_dir, safe_name)