from flask import jsonify, request,redirect, url_for
from marshmallow import ValidationError


from ..model import User 
from ..schema import UserSchema 
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
    
    
    if User.query.filter_by(email=validated_data.get('email')).first:
        redirect(url_for('login')), 302
    else:
        user = User(**validated_data)
        user.set_password(data.get("password"))
        
        db.session.add(user)
        db.session.commit()
    return jsonify(user_schema.dump(user)), 201
    



@api.route('/login', method=["POST"])
def login():
    pass
    
    
    
   
   
      