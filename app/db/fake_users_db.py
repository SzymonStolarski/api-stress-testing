from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": password_context.hash("admin")  # Only for testing:)
    }
}
