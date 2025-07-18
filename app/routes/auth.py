from flask import jsonify, request,redirect, url_for
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token

from ..model import User 
from ..schema import UserSchema, UserLogin
from . import api 
from ..import db



@api.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    user_schema = UserSchema()
    
    try:
        validated_data = user_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    
    if User.query.filter_by(email=validated_data.get('email')).first():
        return jsonify({"error": "Email already exist"}),409
    else:
        user = User(**validated_data)
        user.set_password(data.get("password"))
        
        db.session.add(user)
        db.session.commit()
    return jsonify(user_schema.dump(user)), 201
    



@api.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    login_schema = UserLogin()
    
    try:
        validated_data = login_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    
    email = validated_data.get('email')
    password = validated_data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return jsonify({"error": "Invalid Email or Password"}),401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token, "user_id": user.id, "message": "Login Successful"})
  
    
   
   
      