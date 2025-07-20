from flask import current_app
from itsdangerous import URLSafeTimedSerializer 


def generate_token(email, salt='email-confirm'):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=salt)


def confirm_token(token, salt='email-confirm', expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        return serializer.loads(token, salt=salt, max_age=expiration)
    except Exception:
        return None