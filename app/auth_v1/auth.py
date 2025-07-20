from flask import jsonify, request, url_for
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity

from ..model import User 
from ..schema import UserLogin, UserRegistration
from ..utils.token import generate_token, confirm_token
from ..utils.email import send_email
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



@api.route('/verify_email/confirm/<token>',  methods=["GET"])
def confirm_email(token):
    email = confirm_token(token, salt='email-confirm')
    if not email:
        return jsonify({"message": "Invalid or Expired Token"}), 400
    
    user= User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"messege": "User not Found."}), 404
    
    if user.is_verified:
        return jsonify({"message": "Account already verified"}), 200
    user.is_verified = True
    db.session.commit()
    return jsonify({"message": "Email verified successfully"}), 200



@api.route('/verify_email/rquest', methods=["POST"])
def send_verification_email():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        token = generate_token(user.email, salt='email-confirm')
        confirm_url = url_for('api.confirm_email', token=token, _external=True)
        html = f"Click to confirm your email: <a href='{confirm_url}'>{confirm_url}</a>"
        send_email(user.email, "Confirm your Email", html)
    return jsonify({"message": "Check your inbox to verify your email."}), 200


@api.route('/reset_password/<token>', methods=["POST"])
def reset_password(token):
    email = confirm_token(token, salt='password-reset')
    if not email:
        return jsonify({"message": "Invalid or expired token."}),400
    data = request.get_json()
    new_password = data.get("password")
    
    if not new_password:
        return jsonify({"message": "Invalid or expired token."}), 400
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({"message": "User not Found"}), 404
    
    user.set_password(new_password)
    db.session.commit()
    return jsonify({"message": "Password has been reset successfully"}), 200
    
    
@api.route('/reset_password/request', methods=["POST"])
def send_reset_password_email():
    data = request.get_json()
    user = User.query.filter_by(email=data).first()
    
    if user:
        token = generate_token(user.email, salt="password-reset")
        reset_url = url_for('api.reset_password', token=token, _external=True)
        html = f"Click to reset your password: <a href='{reset_url}'>{reset_url}</a>"
        send_email(user.email, "Reset Your Password", html)
    return jsonify({"message": "Check your inbox for password reset instructions."}), 200