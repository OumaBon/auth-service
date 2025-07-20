from flask import Flask 
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager 
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_migrate import Migrate

from config import config


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
ma = Marshmallow()
mail = Mail()
migrate = Migrate()



def create_app(config_name='default'):
    app = Flask(__name__)
    config_class = config[config_name]
    app.config.from_object(config_class)
    config_class.init_app(app)
    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    
    from app.auth_v1 import api 
    
    app.register_blueprint(api)
    
    return app 



