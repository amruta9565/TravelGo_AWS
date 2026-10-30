from app.services.auth_service import auth_service
from app.services.db_service import db


def test_user_registration_success(client):
    """Tests that a new user can register successfully."""
    response = client.post("/auth/register", data={
        "full_name": "Jordan Cloud",
        "email": "jordan@example.com",
        "password": "SecurePassword123!",
        "confirm_password": "SecurePassword123!",
        "phone": "+1 555-9876"
    }, follow_redirects=True)

    assert response.status_code == 200
    user = db.get_user_by_email("jordan@example.com")
    assert user is not None
    assert user["full_name"] == "Jordan Cloud"
    assert "password_hash" in user
    assert user["password_hash"] != "SecurePassword123!"  # Must be hashed


def test_user_registration_validation_mismatched_password(client):
    """Tests password confirmation mismatch rejection."""
    response = client.post("/auth/register", data={
        "full_name": "Jordan Cloud",
        "email": "mismatch@example.com",
        "password": "SecurePassword123!",
        "confirm_password": "DifferentPassword123!"
    })
    assert response.status_code == 200
    assert b"Passwords do not match" in response.data


def test_user_registration_short_password(client):
    """Tests rejecting short passwords."""
    response = client.post("/auth/register", data={
        "full_name": "Jordan Cloud",
        "email": "short@example.com",
        "password": "123",
        "confirm_password": "123"
    })
    assert response.status_code == 200
    assert b"Password must be at least 8 characters long" in response.data


def test_user_login_success(client):
    """Tests authentication with valid credentials."""
    auth_service.register_user("Login User", "login@example.com", "Password1234!")

    response = client.post("/auth/login", data={
        "email": "login@example.com",
        "password": "Password1234!"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome back, Login User" in response.data


def test_user_login_invalid_password(client):
    """Tests login rejection on incorrect password."""
    auth_service.register_user("Login User 2", "login2@example.com", "Password1234!")

    response = client.post("/auth/login", data={
        "email": "login2@example.com",
        "password": "WrongPassword!"
    })
    assert response.status_code == 200
    assert b"Invalid email or password" in response.data


def test_demo_user_quick_login(client):
    """Tests the 1-click test demo user login."""
    response = client.get("/auth/demo-login", follow_redirects=True)
    assert response.status_code == 200
    assert b"Alex Traveler" in response.data


def test_logout(auth_client):
    """Tests user session termination upon logout."""
    client, _ = auth_client
    response = client.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"You have been signed out safely" in response.data
