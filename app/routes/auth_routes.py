from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.auth_service import auth_service
from app.services.db_service import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("dashboard.dashboard_view"))

    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        success, res = auth_service.authenticate_user(email, password)
        if success:
            session["user"] = res
            flash(f"Welcome back, {res.get('full_name')}!", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("dashboard.dashboard_view"))
        else:
            error = res

    return render_template("login.html", error=error)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user" in session:
        return redirect(url_for("dashboard.dashboard_view"))

    error = None
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        phone = request.form.get("phone", "").strip()

        is_valid, validation_err = auth_service.validate_registration_input(
            full_name, email, password, confirm_password
        )
        if not is_valid:
            error = validation_err
        else:
            success, res = auth_service.register_user(full_name, email, password, phone)
            if success:
                session["user"] = res
                flash("Your TravelGo account was created successfully! Welcome aboard.", "success")
                return redirect(url_for("dashboard.dashboard_view"))
            else:
                error = res

    return render_template("register.html", error=error)


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been signed out safely.", "info")
    return redirect(url_for("main.index"))


@auth_bp.route("/demo-login")
def demo_login():
    """Provides instant 1-click test login for easy evaluation."""
    demo_email = "alex.traveler@example.com"
    user = db.get_user_by_email(demo_email)

    if not user:
        # Seed demo user
        auth_service.register_user(
            full_name="Alex Traveler",
            email=demo_email,
            password="Password123!",
            phone="+1 (555) 019-2834"
        )
        user = db.get_user_by_email(demo_email)

    safe_user = {k: v for k, v in user.items() if k != "password_hash"}
    session["user"] = safe_user
    flash("Logged in as Demo User (Alex Traveler).", "success")
    return redirect(url_for("dashboard.dashboard_view"))
