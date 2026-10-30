from flask import Blueprint, jsonify, request, session
from app.services.booking_service import booking_service
from app.services.auth_service import auth_service
from app.services.db_service import db

api_bp = Blueprint("api", __name__)


@api_bp.route("/search")
def search_api():
    """Returns JSON search results for dynamic frontend filtering."""
    service_type = request.args.get("type", "bus").lower()
    origin = request.args.get("origin", "")
    destination = request.args.get("destination", "")
    travel_date = request.args.get("date", "")
    category = request.args.get("category", "all")

    if service_type == "bus":
        results = booking_service.search_buses(origin, destination, travel_date)
    elif service_type == "train":
        results = booking_service.search_trains(origin, destination, travel_date)
    elif service_type == "flight":
        results = booking_service.search_flights(origin, destination, travel_date)
    elif service_type == "hotel":
        results = booking_service.search_hotels(destination or origin, category=category)
    else:
        results = []

    return jsonify({"success": True, "type": service_type, "count": len(results), "results": results})


@api_bp.route("/bus/<bus_id>/seats")
def bus_seats_api(bus_id):
    """Returns bus seat map, booked seats, and pricing."""
    bus = booking_service.get_bus_by_id(bus_id)
    if not bus:
        return jsonify({"success": False, "error": "Bus not found"}), 404

    return jsonify({
        "success": True,
        "bus": bus,
        "booked_seats": bus.get("booked_seats", []),
        "price_per_seat": bus.get("price_per_seat", 0.0),
        "total_seats": bus.get("total_seats", 40)
    })


@api_bp.route("/book", methods=["POST"])
def book_api():
    """Creates a booking via JSON API."""
    data = request.get_json() or {}
    user = session.get("user")
    user_id = user.get("user_id") if user else data.get("user_id", "guest_user")
    user_email = user.get("email") if user else data.get("passenger_email", "guest@travelgo.com")

    try:
        booking = booking_service.create_booking(
            user_id=user_id,
            user_email=user_email,
            service_type=data.get("service_type", "bus"),
            item_id=data.get("item_id"),
            item_title=data.get("item_title", "Travel Reservation"),
            travel_date=data.get("travel_date"),
            passenger_name=data.get("passenger_name", "Traveler"),
            passenger_phone=data.get("passenger_phone", ""),
            seats=data.get("seats", []),
            nights=int(data.get("nights", 1)),
            total_amount=float(data.get("total_amount", 0.0)),
            special_requests=data.get("special_requests", "")
        )
        return jsonify({"success": True, "booking": booking}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@api_bp.route("/cancel", methods=["POST"])
def cancel_api():
    """Cancels a booking via JSON API."""
    user = session.get("user")
    if not user:
        return jsonify({"success": False, "error": "Authentication required"}), 401

    data = request.get_json() or {}
    booking_id = data.get("booking_id")
    if not booking_id:
        return jsonify({"success": False, "error": "booking_id is required"}), 400

    success, res = booking_service.cancel_booking(booking_id, user["user_id"], user["email"])
    if success:
        return jsonify({"success": True, "booking": res})
    return jsonify({"success": False, "error": str(res)}), 400


@api_bp.route("/user")
def user_api():
    """Returns the current authenticated user session."""
    user = session.get("user")
    if user:
        return jsonify({"authenticated": True, "user": user})
    return jsonify({"authenticated": False, "user": None})
