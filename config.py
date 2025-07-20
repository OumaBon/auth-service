import os 
from datetime import timedelta
from dotenv import load_dotenv 

load_dotenv()

Base_Dir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY', "something very tough to gauuze")
    JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', "ihateusingthisthing")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 15)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 30)))
    JWT_TOKEN_LOCATION = ["headers","cookies"]
    JWT_COOKIE_CSRF_PROTECT =True
    JWT_COOKIE_SECURE = False
    JWT_BLACKLIST_ENABLED = True
    
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'oumamugah@gmail.com')

    
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
