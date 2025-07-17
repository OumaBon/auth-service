import pytest 
from app import create_app
from app import db as _db 


@pytest.fixture
def app():
    app=create_app(config_name='testing')
    with app.app_context():
        _db.create_all()
        yield app 
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()