import os
import pytest
from app import create_app
from app.services.db_service import db
from app.services.notification_service import notification_service


@pytest.fixture
def app():
    """Creates test application instance."""
    app = create_app("testing")
    app.config["CSRF_DISABLED"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    
    # Reset in-memory database store for test isolation
    db.use_mock = True
    store = db._load_local_store()
    store["users"] = {}
    store["bookings"] = {}
    db._save_local_store(store)

    # Clear notification list
    notification_service.sent_notifications.clear()

    yield app


@pytest.fixture
def client(app):
    """Provides test client."""
    return app.test_client()


@pytest.fixture
def auth_client(client, app):
    """Provides an authenticated test client with a logged-in user."""
    from app.services.auth_service import auth_service
    success, user = auth_service.register_user(
        full_name="Tester Smith",
        email="tester@travelgo.com",
        password="TestPassword123!",
        phone="+1 555-1234"
    )
    with client.session_transaction() as sess:
        sess["user"] = user
        sess["csrf_token"] = "test-token"
    return client, user
