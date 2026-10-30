from app.services.booking_service import booking_service
from app.services.notification_service import notification_service
from app.services.db_service import db


def test_bus_seats_view(client):
    """Tests loading the dynamic bus seat selection page."""
    response = client.get("/booking/bus/bus_101/seats")
    assert response.status_code == 200
    assert b"BlueArrow Express" in response.data
    assert b"Interactive Coach Floor Plan" in response.data
    assert b"data-seat=\"1A\"" in response.data


def test_bus_booking_flow(client):
    """Tests booking a bus trip with dynamic seat selection and SNS alert."""
    response = client.post("/booking/checkout", data={
        "service_type": "bus",
        "item_id": "bus_101",
        "item_title": "BlueArrow Express (New York to Boston)",
        "travel_date": "2026-11-20",
        "total_amount": "90.00",
        "seats": "2A,2B",
        "passenger_name": "Sarah Connor",
        "passenger_email": "sarah@travelgo.com",
        "passenger_phone": "+1 555-8888"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Booking successful" in response.data
    assert b"TravelGo E-Ticket Voucher" in response.data
    assert b"Sarah Connor" in response.data
    assert b"2A, 2B" in response.data

    # Check notification dispatch
    assert len(notification_service.sent_notifications) > 0
    last_notif = notification_service.sent_notifications[-1]
    assert last_notif["recipient"] == "sarah@travelgo.com"
    assert "Confirmed" in last_notif["subject"]
    assert last_notif["alert_type"] == "CONFIRMATION"


def test_hotel_booking_flow(client):
    """Tests hotel reservation with nights calculation and database record."""
    response = client.post("/booking/checkout", data={
        "service_type": "hotel",
        "item_id": "htl_401",
        "item_title": "The Grand Azure Palace & Spa",
        "travel_date": "2026-11-25",
        "nights": "3",
        "total_amount": "1140.00",
        "passenger_name": "Bruce Wayne",
        "passenger_email": "bruce@travelgo.com",
        "passenger_phone": "+1 555-7777"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"The Grand Azure Palace &amp; Spa" in response.data
    assert b"1140.00" in response.data

    # Verify database record
    user_bookings = [b for b in db._load_local_store()["bookings"].values() if b.get("passenger_name") == "Bruce Wayne"]
    assert len(user_bookings) == 1
    assert user_bookings[0]["status"] == "CONFIRMED"
    assert user_bookings[0]["nights"] == 3


def test_flight_booking_flow(client):
    """Tests booking a flight ticket."""
    response = client.post("/booking/checkout", data={
        "service_type": "flight",
        "item_id": "flt_301",
        "item_title": "SkyWing Airways SW-402 (JFK -> LAX)",
        "travel_date": "2026-12-01",
        "total_amount": "245.00",
        "passenger_name": "Tony Stark",
        "passenger_email": "tony@travelgo.com",
        "passenger_phone": "+1 555-3000"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"SkyWing Airways" in response.data
    assert b"245.00" in response.data
