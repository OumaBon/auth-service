# generate_token.py
from app import create_app
from itsdangerous import URLSafeTimedSerializer

app = create_app("development")
with app.app_context():
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    token = s.dumps("mugahboniface@gmail.com", salt="email-confirm")
    print(token)
