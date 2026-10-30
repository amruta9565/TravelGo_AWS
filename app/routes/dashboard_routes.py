from flask import Blueprint, render_template, session, redirect, url_for, flash
from datetime import date
from app.services.db_service import db

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard_view():
    """User dashboard displaying profile, upcoming bookings, and past history."""
    user = session.get("user")
    if not user:
        flash("Please log in to view your TravelGo dashboard.", "info")
        return redirect(url_for("auth.login", next=url_for("dashboard.dashboard_view")))

    all_bookings = db.get_user_bookings(user["user_id"])
    today_str = str(date.today())

    upcoming_bookings = []
    past_bookings = []
    cancelled_bookings = []

    total_spent = 0.0

    for b in all_bookings:
        status = b.get("status", "CONFIRMED")
        t_date = b.get("travel_date", "")

        if status == "CANCELLED":
            cancelled_bookings.append(b)
        elif t_date >= today_str:
            upcoming_bookings.append(b)
            total_spent += float(b.get("total_amount", 0.0))
        else:
            past_bookings.append(b)
            total_spent += float(b.get("total_amount", 0.0))

    stats = {
        "total_bookings": len(all_bookings),
        "upcoming_count": len(upcoming_bookings),
        "past_count": len(past_bookings),
        "cancelled_count": len(cancelled_bookings),
        "total_spent": total_spent
    }

    return render_template(
        "dashboard.html",
        user=user,
        stats=stats,
        upcoming_bookings=upcoming_bookings,
        past_bookings=past_bookings,
        cancelled_bookings=cancelled_bookings
    )
