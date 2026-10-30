from app.services.booking_service import booking_service


def test_bus_search(client):
    """Tests bus search route and service."""
    response = client.get("/booking/search?type=bus&origin=New+York&destination=Boston")
    assert response.status_code == 200
    assert b"BlueArrow Express" in response.data
    assert b"Select Seats" in response.data


def test_train_search(client):
    """Tests train search route and service."""
    response = client.get("/booking/search?type=train&origin=New+York&destination=Washington+DC")
    assert response.status_code == 200
    assert b"Acela High-Speed Express" in response.data
    assert b"Reserve Now" in response.data


def test_flight_search(client):
    """Tests flight search route and service."""
    response = client.get("/booking/search?type=flight&origin=JFK&destination=LAX")
    assert response.status_code == 200
    assert b"SkyWing Airways" in response.data
    assert b"SW-402" in response.data


def test_hotel_search_budget_filter(client):
    """Tests that budget hotel filter returns properties under $100."""
    response = client.get("/booking/search?type=hotel&category=budget")
    assert response.status_code == 200
    assert b"MetroPod Smart Budget Stay" in response.data
    assert b"Budget Saver" in response.data
    # Should not include ultra luxury $380 hotel
    assert b"The Grand Azure Palace &amp; Spa" not in response.data


def test_hotel_search_luxury_filter(client):
    """Tests that luxury hotel filter returns 5-star properties."""
    response = client.get("/booking/search?type=hotel&category=luxury")
    assert response.status_code == 200
    assert b"The Grand Azure Palace &amp; Spa" in response.data
    assert b"Pacific Bayfront Luxury Resort" in response.data
    # Should not include budget pod
    assert b"MetroPod Smart Budget Stay" not in response.data


def test_search_api_json(client):
    """Tests REST API search for client-side JavaScript."""
    response = client.get("/api/search?type=bus&origin=New+York")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["count"] > 0
    assert len(data["results"]) > 0
