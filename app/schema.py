from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields,validate, ValidationError, validates, post_load
from .model import User 



class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance =True
        include_relationship = False
        include_fk = True
        
    username = fields.Str(required=True)
    email = fields.Email(required=True, validate=validate.Length(min=10, max=65))
    password = fields.Str(required=True, validate=validate.Length(min=6), load_only=True)
    
    
    

class UserRegistration(UserSchema):
    class Meta(UserSchema.Meta):
        fields = ("username","email", "password")
   
    @validates('email')
    def validate_email_address(self, value, **kwargs):
        if User.query.filter_by(email=value).first():
            raise ValidationError("Email Already Exists")
        
        

class UserLogin(UserSchema):
    class Meta(UserSchema.Meta):
        load_instance = False
        fields = ("email", "password")
    
    @post_load
    def get_user(self, data, **kwargs):
        user = User.query.filter_by(email=data["email"]).first()
        if not user:
            raise ValidationError("Invalid Email or Password")
        return user
    
        
