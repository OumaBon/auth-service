import os 
from datetime import timedelta
from dotenv import load_dotenv 

load_dotenv()

Base_Dir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY', "something very tough to gauuze")
    JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', "ihateusingthisthing")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_EXP_MINUTES", 15)))
    
    JWT_REFRESH_TOKEN_EXPIRES=os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 3600)
    JWT_TOKEN_LOCATION = ["headers","cookies"]
    JWT_COOKIE_CSRF_PROTECT =True
    JWT_COOKIE_SECURE = False

    
    @staticmethod
    def init_app(app):
        pass 


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI=os.environ.get("DEV_URI") or \
        "sqlite:///" + os.path.join(Base_Dir, "dev-data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False 


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_URI") or \
        "sqlite:///" + os.path.join(Base_Dir, "test-data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = True



config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
