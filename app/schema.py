from . import ma 
from model import User 
from marshmallow import validates, ValidationError,fields,validate





class UserSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = User
        load_instance = True
        exclude = ('password_hash',)
    username = fields.Email(required=True)
    email = fields.Str(required=True, validate=validate.Length(min=8, max=50))
    password = fields.Str(required=True, load_only=True,validate=validate.Length(min=6))
    
    
    @validates('email')
    def validate_email(self, value):
        if User.query.filter_by(email=value).first():
            raise ValidationError("Email is already registered.")
    
    
        