# conftest.py
import pytest
from app import create_app, db
from app.model import User

@pytest.fixture(scope="module")
def test_app():
    app = create_app("testing")  # your config key
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def session(test_app):
    return db.session
