from flask import jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token

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
    return jsonify({"message":"Login Successfull", "access_token": access_token}), 200
    
    