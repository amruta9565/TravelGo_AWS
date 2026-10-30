from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from datetime import date, timedelta
from app.services.booking_service import booking_service
from app.services.db_service import db

booking_bp = Blueprint("booking", __name__)


@booking_bp.route("/search")
def search():
    """Unified search results page for Bus, Train, Flight, and Hotel."""
    service_type = request.args.get("type", "bus").lower()
    origin = request.args.get("origin", "").strip()
    destination = request.args.get("destination", "").strip()
    travel_date = request.args.get("date", str(date.today() + timedelta(days=5)))
    category = request.args.get("category", "all").lower()

    results = []
    if service_type == "bus":
        results = booking_service.search_buses(origin, destination, travel_date)
    elif service_type == "train":
        results = booking_service.search_trains(origin, destination, travel_date)
    elif service_type == "flight":
        results = booking_service.search_flights(origin, destination, travel_date)
    elif service_type == "hotel":
        results = booking_service.search_hotels(destination or origin, category=category)
    else:
        service_type = "bus"
        results = booking_service.search_buses(origin, destination, travel_date)

    return render_template(
        "search_results.html",
        service_type=service_type,
        origin=origin,
        destination=destination,
        travel_date=travel_date,
        category=category,
        results=results
    )


@booking_bp.route("/bus/<bus_id>/seats")
def bus_seats(bus_id):
    """Dynamic bus seat selection view."""
    bus = booking_service.get_bus_by_id(bus_id)
    if not bus:
        flash("Bus trip not found.", "danger")
        return redirect(url_for("booking.search", type="bus"))

    travel_date = request.args.get("date", str(date.today() + timedelta(days=3)))
    return render_template("bus_seats.html", bus=bus, travel_date=travel_date)


@booking_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    """Booking checkout flow with passenger details and payment confirmation."""
    if request.method == "POST":
        service_type = request.form.get("service_type", "bus")
        item_id = request.form.get("item_id")
        item_title = request.form.get("item_title", "Travel Reservation")
        travel_date = request.form.get("travel_date", str(date.today() + timedelta(days=3)))
        total_amount = float(request.form.get("total_amount", 0.0))
        seats_raw = request.form.get("seats", "")
        seats = [s.strip() for s in seats_raw.split(",") if s.strip()] if seats_raw else []
        nights = int(request.form.get("nights", 1))

        # Check user authentication or use passenger details from form
        user = session.get("user")
        user_id = user.get("user_id") if user else "guest_user"
        passenger_name = request.form.get("passenger_name", user.get("full_name") if user else "Traveler")
        passenger_email = request.form.get("passenger_email", user.get("email") if user else "guest@travelgo.com")
        passenger_phone = request.form.get("passenger_phone", user.get("phone", "") if user else "")
        special_requests = request.form.get("special_requests", "")

        booking = booking_service.create_booking(
            user_id=user_id,
            user_email=passenger_email,
            service_type=service_type,
            item_id=item_id,
            item_title=item_title,
            travel_date=travel_date,
            passenger_name=passenger_name,
            passenger_phone=passenger_phone,
            seats=seats,
            nights=nights,
            total_amount=total_amount,
            special_requests=special_requests
        )

        flash("🎉 Booking successful! Confirmation details and email sent.", "success")
        return redirect(url_for("booking.confirmation", booking_id=booking["booking_id"]))

    # GET request with query params
    service_type = request.args.get("type", "bus")
    item_id = request.args.get("id")
    travel_date = request.args.get("date", str(date.today() + timedelta(days=3)))
    seats_raw = request.args.get("seats", "")
    seats = [s.strip() for s in seats_raw.split(",") if s.strip()] if seats_raw else []
    nights = int(request.args.get("nights", 1))

    item = None
    item_title = "Reservation"
    total_amount = 0.0

    if service_type == "bus":
        item = booking_service.get_bus_by_id(item_id)
        if item:
            item_title = f"{item['operator']} ({item['origin']} → {item['destination']})"
            seat_count = max(len(seats), 1)
            total_amount = item["price_per_seat"] * seat_count
    elif service_type == "train":
        item = booking_service.get_train_by_id(item_id)
        if item:
            item_title = f"{item['train_name']} ({item['origin']} → {item['destination']})"
            total_amount = item["base_price"]
    elif service_type == "flight":
        item = booking_service.get_flight_by_id(item_id)
        if item:
            item_title = f"{item['airline']} {item['flight_number']} ({item['origin_code']} → {item['destination_code']})"
            total_amount = item["price"]
    elif service_type == "hotel":
        item = booking_service.get_hotel_by_id(item_id)
        if item:
            item_title = f"{item['name']} ({item['city']})"
            total_amount = item["price_per_night"] * nights

    if not item:
        flash("Selected travel item was not found.", "warning")
        return redirect(url_for("booking.search", type=service_type))

    return render_template(
        "booking_confirm.html",
        mode="checkout",
        service_type=service_type,
        item=item,
        item_title=item_title,
        travel_date=travel_date,
        seats=seats,
        nights=nights,
        total_amount=total_amount
    )


@booking_bp.route("/confirmation/<booking_id>")
def confirmation(booking_id):
    """Booking confirmation and printable voucher receipt."""
    booking = db.get_booking_by_id(booking_id)
    if not booking:
        flash("Booking reference not found.", "danger")
        return redirect(url_for("main.index"))

    return render_template("booking_confirm.html", mode="confirmed", booking=booking)


@booking_bp.route("/cancel", methods=["POST"])
def cancel_booking():
    """Cancels a booking from dashboard or management interface."""
    user = session.get("user")
    if not user:
        flash("Please log in to manage your bookings.", "warning")
        return redirect(url_for("auth.login"))

    booking_id = request.form.get("booking_id")
    if not booking_id:
        flash("Invalid booking identifier.", "danger")
        return redirect(url_for("dashboard.dashboard_view"))

    success, res = booking_service.cancel_booking(booking_id, user["user_id"], user["email"])
    if success:
        flash(f"Booking {booking_id} has been cancelled successfully. Refund initiated.", "success")
    else:
        flash(f"Could not cancel booking: {res}", "danger")

    return redirect(url_for("dashboard.dashboard_view"))
