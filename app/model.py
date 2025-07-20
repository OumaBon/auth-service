from datetime import datetime
import uuid

from . import db,bcrypt, jwt


class User(db.Model):
    __tablename__="users"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String, unique=True, nullable=False,index=True)
    email = db.Column(db.String, unique=True, nullable=False,index=True)
    password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)
    
    
    def set_password(self,password):
        self.password_hash=bcrypt.generate_password_hash(password).decode('utf-8')
    
    
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()