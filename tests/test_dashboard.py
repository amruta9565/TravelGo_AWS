from app.services.booking_service import booking_service
from datetime import date, timedelta


def test_dashboard_unauthenticated_redirect(client):
    """Tests that unauthenticated users are redirected to login."""
    response = client.get("/dashboard/")
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_dashboard_authenticated_view(auth_client):
    """Tests that logged in user sees dashboard with stats and upcoming trips."""
    client, user = auth_client

    # Seed an upcoming booking and a past booking
    upcoming_date = str(date.today() + timedelta(days=10))
    past_date = str(date.today() - timedelta(days=10))

    booking_service.create_booking(
        user_id=user["user_id"],
        user_email=user["email"],
        service_type="flight",
        item_id="flt_301",
        item_title="SkyWing Flight SW-402",
        travel_date=upcoming_date,
        passenger_name=user["full_name"],
        passenger_phone=user.get("phone", ""),
        total_amount=245.00
    )

    booking_service.create_booking(
        user_id=user["user_id"],
        user_email=user["email"],
        service_type="bus",
        item_id="bus_101",
        item_title="BlueArrow Bus Express",
        travel_date=past_date,
        passenger_name=user["full_name"],
        passenger_phone=user.get("phone", ""),
        total_amount=45.00
    )

    response = client.get("/dashboard/")
    assert response.status_code == 200
    assert user["full_name"].encode() in response.data
    assert b"SkyWing Flight SW-402" in response.data
    assert b"BlueArrow Bus Express" in response.data
    assert b"Total Reservations" in response.data
    assert b"290.00" in response.data  # 245 + 45
