import os
from app import create_app

env = os.getenv("FLASK_ENV", "development")
app = create_app(env)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "1") in ("1", "true", "True")
    print(f"🚀 Starting TravelGo platform on http://127.0.0.1:{port} (Environment: {env})")
    app.run(host="0.0.0.0", port=port, debug=debug)
