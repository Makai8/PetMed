"""PetMed API server (Sprint IV).

Run from the repository root:   python src/app.py
The API listens on http://localhost:4000. The website (frontend/, at
http://localhost:5173) calls it for sign-in and for every role's data.
"""
import datetime
import decimal
import importlib
import pkgutil

from flask import Flask, jsonify, request
from flask.json.provider import DefaultJSONProvider

import auth
import routes
from db import close_db, query_one

# The website's address while developing (npm run dev). Only it may call the API.
WEBSITE_ORIGINS = {"http://localhost:5173", "http://127.0.0.1:5173"}


class PetMedJSON(DefaultJSONProvider):
    """Send dates as '2026-10-28 10:00:00' and decimals (pet weight) as numbers."""

    @staticmethod
    def default(o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            return o.isoformat()
        if isinstance(o, decimal.Decimal):
            return float(o)
        return DefaultJSONProvider.default(o)


def create_app():
    app = Flask(__name__)
    app.json = PetMedJSON(app)
    app.teardown_appcontext(close_db)

    app.register_blueprint(auth.bp)
    # Every file in src/routes/ that defines `bp` is added automatically,
    # so each role's feature can be added without editing this file.
    for found in sorted(pkgutil.iter_modules(routes.__path__), key=lambda m: m.name):
        module = importlib.import_module(f"routes.{found.name}")
        if hasattr(module, "bp"):
            app.register_blueprint(module.bp)

    @app.get("/api/health")
    def health():
        """Quick check that the API can reach the database."""
        row = query_one("SELECT COUNT(*) AS users FROM User")
        return jsonify(status="ok", users_in_database=row["users"])

    @app.after_request
    def allow_website(response):
        """Let the React site on port 5173 call this API on port 4000 (CORS)."""
        origin = request.headers.get("Origin")
        if origin in WEBSITE_ORIGINS:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            response.headers["Vary"] = "Origin"
        return response

    @app.errorhandler(404)
    def not_found(_e):
        return jsonify(message="Not found."), 404

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=4000, debug=True)
