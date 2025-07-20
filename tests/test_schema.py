
import pytest
from app.schema import UserRegistration
from app.model import User
from marshmallow.exceptions import ValidationError


def test_valid_data(session):
    schema = UserRegistration(only=("username", "email", "password"))
    input_data = {
        "username": "mugah",
        "email": "mugah@example.com",
        "password": "securepass"
    }
    result = schema.load(input_data)
    assert result["email"] == input_data["email"]



# def test_invalid_email_format():
#     schema = UserRegistration()
#     input_data = {
#         "username": "test",
#         "email": "invalid-email",
#         "password": "123456"
#     }

#     with pytest.raises(ValidationError) as e:
#         schema.load(input_data)
#     assert "email" in e.value.messages


# def test_short_password():
#     schema = UserRegistration()
#     input_data = {
#         "username": "test",
#         "email": "shortpass@example.com",
#         "password": "123"
#     }

#     with pytest.raises(ValidationError) as e:
#         schema.load(input_data)
#     assert "password" in e.value.messages


# def test_duplicate_email(session):
#     # Add a user first
#     user = User(username="existing", email="existing@example.com")
#     user.set_password("password123")
#     session.add(user)
#     session.commit()

#     schema = UserRegistration()
#     input_data = {
#         "username": "newuser",
#         "email": "existing@example.com",
#         "password": "newpassword"
#     }

#     with pytest.raises(ValidationError) as e:
#         schema.load(input_data)
#     assert "Email already exists" in str(e.value)
