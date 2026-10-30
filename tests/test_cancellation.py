from app.services.booking_service import booking_service
from app.services.notification_service import notification_service
from app.services.db_service import db


def test_booking_cancellation_flow(auth_client):
    """Tests booking cancellation, status update and SNS cancellation dispatch."""
    client, user = auth_client

    # Create a booking for this user
    booking = booking_service.create_booking(
        user_id=user["user_id"],
        user_email=user["email"],
        service_type="bus",
        item_id="bus_101",
        item_title="BlueArrow Express",
        travel_date="2026-12-15",
        passenger_name=user["full_name"],
        passenger_phone=user.get("phone", ""),
        seats=["1A"],
        total_amount=45.00
    )
    booking_id = booking["booking_id"]

    # Clear notification list before cancellation
    notification_service.sent_notifications.clear()

    # Cancel the booking
    response = client.post("/booking/cancel", data={
        "booking_id": booking_id
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"cancelled successfully" in response.data

    # Check updated database record
    updated = db.get_booking_by_id(booking_id)
    assert updated["status"] == "CANCELLED"
    assert "cancelled_at" in updated

    # Check SNS cancellation alert dispatch
    assert len(notification_service.sent_notifications) > 0
    notif = notification_service.sent_notifications[-1]
    assert notif["alert_type"] == "CANCELLATION"
    assert "Cancelled" in notif["subject"]


def test_booking_cancellation_unauthorized(client):
    """Tests that unauthenticated requests to cancel a booking are rejected."""
    response = client.post("/booking/cancel", data={"booking_id": "BK-BUS-FAKE"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in" in response.data


def test_double_cancellation_prevention(auth_client):
    """Tests that cancelling an already cancelled booking returns an error."""
    client, user = auth_client
    booking = booking_service.create_booking(
        user_id=user["user_id"],
        user_email=user["email"],
        service_type="train",
        item_id="trn_201",
        item_title="Acela Express",
        travel_date="2026-12-20",
        passenger_name=user["full_name"],
        total_amount=85.00
    )
    b_id = booking["booking_id"]

    # First cancel
    client.post("/booking/cancel", data={"booking_id": b_id}, follow_redirects=True)

    # Second cancel attempt
    res = client.post("/booking/cancel", data={"booking_id": b_id}, follow_redirects=True)
    assert res.status_code == 200
    assert b"already been cancelled" in res.data
