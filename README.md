# 🔐 Authentication Service Specification Document

**Service Name**: `auth-service`
**Owner**: Boniface Ouma
**Version**: 1.0
**Date**: July 2025
**Target Stack**: Flask, SQLAlchemy, PostgreSQL
**Audience**: Backend Developers, Frontend Developers, QA, DevOps

---

## 1. 📘 Purpose

The `auth-service` is a secure and modular microservice responsible for handling user authentication and authorization across our platform. It offers user registration, login, token issuance and refresh, logout, and access protection for downstream services.

---

## 2. ⚙️ System Requirements

### ✅ Software Dependencies

| Component          | Version / Tool               |
| ------------------ | ---------------------------- |
| Python             | 3.10+                        |
| Flask              | 2.x                          |
| Flask-JWT-Extended | 4.x                          |
| Flask-Bcrypt       | 1.x                          |
| SQLAlchemy         | 2.x                          |
| Marshmallow        | 3.x                          |
| PostgreSQL         | 13+ (prod), SQLite (dev)     |
| Flask-CORS         | latest                       |
| Flask-Limiter      | Optional (for rate limiting) |

> All dependencies are listed in `requirements.txt`

---

## 3. 📁 Folder Structure

```
auth-service/
├── app/
│   ├── auth_v1/          # Route Blueprints
│   ├── model.py/          # SQLAlchemy Models
│   ├── services/        # Token generation, hashing logic
│   ├── schema.py/         # Marshmallow Validation
│   └── utils/           # Helpers
│
├── config.py            # Environment-based configuration
├── run.py              # App entry point
├── .env                 # Local env variables
├── requirements.txt
└── tests/
```

---

## 4. 📦 Features

| Feature            | Description                                     |
| ------------------ | ----------------------------------------------- |
| Register           | Email/password sign-up with validation          |
| Login              | Email/password sign-in with JWT generation      |
| Token Refresh      | Issue new access token with valid refresh token |
| Logout             | Revoke refresh token                            |
| Me                 | Return current user using JWT                   |
| Role Support (opt) | Basic role-based access support                 |

---

## 5. 📜 API Endpoints

### POST `/register`

* **Request**:

```json
{
  "username": "boniface",
  "email": "boniface@example.com",
  "password": "StrongPass123"
}
```

* **Response**: 201 Created

---

### POST `/login`

* **Request**:

```json
{
  "email": "boniface@example.com",
  "password": "StrongPass123"
}
```

* **Response**:

```json
{
  "access_token": "<JWT>",
  "refresh_token": "<JWT>",
  "user": {
    "id": "<uuid>",
    "username": "boniface",
    "email": "boniface@example.com"
  }
}
```

---

### POST `/refresh`

* **Header**: `Authorization: Bearer <refresh_token>`
* **Response**: New access token

---

### POST `/logout`

* Invalidates the current refresh token (DB/Redis)

---

### GET `/me`

* **Header**: `Authorization: Bearer <access_token>`
* **Response**:

```json
{
  "id": "<uuid>",
  "email": "boniface@example.com"
}
```

---

## 6. 🔒 Security Policies

### 🔐 Passwords

* Use `bcrypt` with 12+ salt rounds.
* Never log or store raw passwords.

### 🔐 JWT

* **Access Token**: 15 minutes expiry
* **Refresh Token**: 7 days expiry
* Stored in **HttpOnly cookie** or **secure storage**
* Tokens are signed with `JWT_SECRET_KEY` from environment

### 🛡️ Token Blacklisting

* Implemented using Redis or database to track used/expired refresh tokens.

### 🔐 CORS & HTTPS

* `flask-cors` configured per environment
* HTTPS enforced in production

### ⛔ Brute Force Protection

* Use `Flask-Limiter` or Redis-based counters
* Optional: CAPTCHA on frontend after failed attempts

### 📥 Input Validation

* Handled using `Marshmallow`
* Validates:

  * Email format
  * Password strength (8+ characters, alphanumeric)
  * Unique constraints (email, username)

### 🛡️ CSRF & XSS

* All token exchanges via `Authorization` header
* Cookie-based tokens are marked: `HttpOnly`, `Secure`, `SameSite=Lax`

---

## 7. 🧪 Testing

Use `pytest` to cover:

| Test Type         | Examples                         |
| ----------------- | -------------------------------- |
| Unit Tests        | Token creation, password hashing |
| Integration Tests | Register/Login/Refresh flows     |
| Security Tests    | Token tampering, expiry, reuse   |
| Rate-Limit Tests  | Optional, if implemented         |

---

## 8. 🔗 Frontend Integration Guide

### Expected Frontend Behavior

| Action            | Description                                                       |
| ----------------- | ----------------------------------------------------------------- |
| Login             | Call `/login` → store `access_token` and `refresh_token` securely |
| Authenticated API | Attach `Authorization: Bearer <access_token>`                     |
| Token Expiry      | On 401, call `/refresh`, retry the request                        |
| Logout            | Call `/logout`, clear stored tokens                               |

### Token Storage Recommendation

* Access Token: In memory or secure storage (short-lived)
* Refresh Token: HttpOnly cookie or encrypted local storage

---

## 9. 🧑‍💻 Developer Onboarding

To run locally:

```bash
# 1. Create .env
cp .env.example .env

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations (if using Flask-Migrate)
flask db upgrade

# 4. Start dev server
flask run
```

---

## 10. 🧰 Configuration (config.py / .env)

```env
FLASK_ENV=development
JWT_SECRET_KEY=super_secret_key
JWT_ACCESS_TOKEN_EXPIRES=900
JWT_REFRESH_TOKEN_EXPIRES=604800
SQLALCHEMY_DATABASE_URI=postgresql://user:pass@localhost/auth_db
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

---

## 11. ✅ Sign-Off Checklist

| Requirement                           | Status |
| ------------------------------------- | ------ |
| Secure password hashing               | ✅      |
| JWT-based access/refresh token system | ✅      |
| Refresh token rotation and revocation | ✅      |
| Full schema validation                | ✅      |
| CORS configuration                    | ✅      |
| Token expiry and security hardening   | ✅      |
| Automated tests                       | ✅      |
| Frontend integration guide            | ✅      |

---

## 12. 📌 Appendix

### Dependencies (from `requirements.txt`):

```
Flask==2.3.x
Flask-JWT-Extended==4.x
Flask-Bcrypt==1.x
Flask-CORS==3.x
Flask-SQLAlchemy==3.x
Flask-Migrate==4.x
python-dotenv
marshmallow==3.x
```
