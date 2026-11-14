"""Sign-in, sessions and role-based authorization.

How it works:
1. POST /api/login checks the email and password against the User table.
2. If they match, the server looks up the user's roles (User_Role -> Role)
   and returns a signed token.
3. Every protected route uses @require_roles(...). It reads the token, loads the
   user and their roles from the database again, and refuses the request
   (403) if none of the user's roles is allowed. Hiding a menu item is not
   enough: the server itself says no.
"""
from functools import wraps

from flask import Blueprint, g, jsonify, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import check_password_hash

import config
from db import query, query_one

bp = Blueprint("auth", __name__, url_prefix="/api")

# Role names exactly as stored in the Role table
ADMINISTRATOR = "administrator"
PET_OWNER = "pet_owner"
VETERINARIAN = "veterinarian"
PET_HEALTH_EXPERT = "pet_health_expert"
COMMUNITY_MODERATOR = "community_moderator"

INVALID_LOGIN = "Invalid email or password."


def _serializer():
    return URLSafeTimedSerializer(config.SECRET_KEY, salt="petmed-session")


def make_token(user_id):
    return _serializer().dumps({"uid": user_id})


def roles_for(user_id):
    rows = query(
        "SELECT r.role_name FROM User_Role ur JOIN Role r ON r.role_id = ur.role_id "
        "WHERE ur.user_id = %s ORDER BY r.role_id",
        (user_id,),
    )
    return [r["role_name"] for r in rows]


def password_matches(stored_hash, password):
    """True only for a real hash that matches. Placeholder hashes never match."""
    try:
        return check_password_hash(stored_hash, password)
    except (ValueError, TypeError):
        return False


def public_user(user, roles):
    """The shape the website expects (frontend/src/auth/authApi.js)."""
    return {
        "userId": user["user_id"],
        "name": user["full_name"],
        "email": user["email"],
        "role": roles[0] if roles else None,  # main role: picks the landing page
        "roles": roles,
    }


@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    if not email or not password:
        return jsonify(message="Enter your email and password."), 400

    user = query_one(
        "SELECT user_id, email, password_hash, full_name, account_status "
        "FROM User WHERE LOWER(email) = %s",
        (email,),
    )
    # Same message whether the email or the password is wrong,
    # so nobody can use the form to find out which emails exist.
    if user is None or not password_matches(user["password_hash"], password):
        return jsonify(message=INVALID_LOGIN), 401

    if user["account_status"] != "active":
        return jsonify(message=f"This account is {user['account_status']}. Contact PetMed support."), 403

    roles = roles_for(user["user_id"])
    if not roles:
        return jsonify(message="This account has no role assigned yet."), 403

    return jsonify(token=make_token(user["user_id"]), **public_user(user, roles))


def current_user_from_token():
    """Return (user, roles), or (None, error_message)."""
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None, "Please sign in."
    try:
        data = _serializer().loads(header[7:], max_age=config.TOKEN_MAX_AGE_SECONDS)
    except SignatureExpired:
        return None, "Your session expired. Please sign in again."
    except BadSignature:
        return None, "Please sign in."

    user = query_one(
        "SELECT user_id, email, full_name, account_status FROM User WHERE user_id = %s",
        (data.get("uid"),),
    )
    if user is None or user["account_status"] != "active":
        return None, "Please sign in."
    return (user, roles_for(user["user_id"])), None


def require_roles(*allowed):
    """Protect a route. Only signed-in users holding one of `allowed` roles get in."""

    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            found, error = current_user_from_token()
            if found is None:
                return jsonify(message=error), 401
            user, roles = found
            if allowed and not set(roles) & set(allowed):
                return jsonify(message="Your role is not allowed to use this feature.",
                               your_roles=roles, allowed_roles=list(allowed)), 403
            g.user, g.roles = user, roles
            return view(*args, **kwargs)

        return wrapper

    return decorator


@bp.get("/me")
@require_roles()  # any signed-in user
def me():
    return jsonify(public_user(g.user, g.roles))
