# Demo users database
from app.core.security import get_password_hash

# For demonstration, passwords are 'password123'
DEMO_USERS = {
    "student@example.com": {
        "id": "1",
        "email": "student@example.com",
        "password_hash": get_password_hash("password123"),
        "role": "student"
    },
    "teacher@example.com": {
        "id": "2",
        "email": "teacher@example.com",
        "password_hash": get_password_hash("password123"),
        "role": "teacher"
    }
}

def get_user(email: str):
    return DEMO_USERS.get(email)
