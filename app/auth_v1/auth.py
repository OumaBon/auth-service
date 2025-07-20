from flask import jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity

from ..model import User 
from ..schema import UserLogin, UserRegistration
from . import api 
from ..import db


@api.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    schema = UserRegistration(session=db.session)
    try:
        user = schema.load(data)
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    
    if User.query.filter_by(email=user.email).first():
        return jsonify({"error": "User already exists. Please log in."}), 409

    user.set_password(data.get("password"))

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Registered successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 201


@api.route('/login', methods=["POST"])
def login():
    data=request.get_json()
    schema=UserLogin(session=db.session)
    
    try:
        user=schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 401
    
    
    if not user or not user.verify_password(data.get("password")):
        return jsonify({"error": "Invalid Login Credentials"}), 401
    
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify({"Message":"Login Successfull", "Access_Token": access_token, "Refresh_Token": refresh_token}), 200
    


@api.route('/refresh', methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token=create_access_token(identity=current_user)
    return jsonify({"New_Access_Token": new_access_token}), 200



@api.route('/protected', methods=["GET"])
@jwt_required()
def protected():
    return jsonify(Message="Access Granted"), 200



@api.route('/me', methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"Error":"User Not Found"}), 404
    return jsonify({"ID": user.id,
                    "Username": user.username,
                    "Email": user.email}), 200

