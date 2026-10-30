import os
import secrets
from flask import Flask, render_template, session, request, abort, jsonify
from config import config_by_name


def create_app(config_name=None):
    """Application Factory for TravelGo."""
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["default"]))

    # Security: Simple Session-based CSRF Protection
    @app.before_request
    def ensure_csrf_token():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_hex(32)

    @app.before_request
    def validate_csrf():
        # Validate CSRF on mutating POST, PUT, DELETE requests (excluding purely public mock APIs if exempted)
        if request.method in ("POST", "PUT", "DELETE", "PATCH"):
            # Check header 'X-CSRFToken' or form field 'csrf_token'
            token = request.headers.get("X-CSRFToken") or request.form.get("csrf_token")
            # If Content-Type is json, check json body
            if not token and request.is_json:
                data = request.get_json(silent=True) or {}
                token = data.get("csrf_token")

            # During tests or if token matches session, allow; otherwise verify
            if not app.config.get("TESTING") and not app.config.get("CSRF_DISABLED"):
                if not token or token != session.get("csrf_token"):
                    # Check if endpoint is exempt or return 400
                    if not request.path.startswith("/static/"):
                        if request.is_json or request.path.startswith("/api/"):
                            return jsonify({"success": False, "error": "Invalid or missing CSRF token"}), 400
                        # For regular forms, abort with 400
                        abort(400, description="CSRF verification failed. Please refresh and try again.")

    # Context processor to inject common variables into all templates
    @app.context_processor
    def inject_global_template_vars():
        return {
            "csrf_token": session.get("csrf_token", ""),
            "current_user": session.get("user", None),
            "is_authenticated": "user" in session,
            "app_name": "TravelGo"
        }

    # Register blueprints
    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.booking_routes import booking_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.api_routes import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(booking_bp, url_prefix="/booking")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(api_bp, url_prefix="/api")

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        if request.is_json or request.path.startswith("/api/"):
            return jsonify({"success": False, "error": "Resource not found"}), 404
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        if request.is_json or request.path.startswith("/api/"):
            return jsonify({"success": False, "error": "Internal server error"}), 500
        return render_template("errors/500.html"), 500

    return app
