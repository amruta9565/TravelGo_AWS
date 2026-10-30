from flask import Blueprint, render_template
from app.services.booking_service import booking_service

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Homepage with hero search, destination cards, and service highlights."""
    destinations = booking_service.get_destinations()
    return render_template("index.html", destinations=destinations)


@main_bp.route("/about")
def about():
    """About TravelGo & AWS Architecture overview."""
    return render_template("about.html")
