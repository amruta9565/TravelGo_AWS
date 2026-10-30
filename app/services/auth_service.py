import re
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from app.services.db_service import db

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


class AuthService:
    """Authentication and User Management Service."""

    @staticmethod
    def validate_registration_input(full_name, email, password, confirm_password):
        """Validates all inputs for user registration."""
        if not full_name or len(full_name.strip()) < 2:
            return False, "Full name must be at least 2 characters long."

        if not email or not EMAIL_REGEX.match(email.strip()):
            return False, "Please enter a valid email address."

        if not password or len(password) < 8:
            return False, "Password must be at least 8 characters long."

        if password != confirm_password:
            return False, "Passwords do not match."

        return True, None

    @staticmethod
    def register_user(full_name, email, password, phone=""):
        """Registers a new user with hashed password."""
        clean_email = email.strip().lower()

        # Check if user already exists
        existing = db.get_user_by_email(clean_email)
        if existing:
            return False, "An account with this email already exists."

        # Generate secure hash (scrypt / pbkdf2 with salt)
        password_hash = generate_password_hash(password, method="scrypt")
        user_id = f"usr_{uuid.uuid4().hex[:12]}"

        user_data = {
            "user_id": user_id,
            "full_name": full_name.strip(),
            "email": clean_email,
            "password_hash": password_hash,
            "phone": phone.strip() if phone else ""
        }

        created = db.create_user(user_data)
        
        # Return sanitized user data (no hash)
        safe_user = {k: v for k, v in created.items() if k != "password_hash"}
        return True, safe_user

    @staticmethod
    def authenticate_user(email, password):
        """Validates user credentials."""
        if not email or not password:
            return False, "Email and password are required."

        clean_email = email.strip().lower()
        user = db.get_user_by_email(clean_email)

        if not user:
            return False, "Invalid email or password."

        stored_hash = user.get("password_hash", "")
        if not check_password_hash(stored_hash, password):
            return False, "Invalid email or password."

        safe_user = {k: v for k, v in user.items() if k != "password_hash"}
        return True, safe_user


auth_service = AuthService()
