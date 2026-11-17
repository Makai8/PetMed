"""Sign up: anyone can create an account. Every new account is a Pet Owner.

The form can also ask for another role ("user type"): Veterinarian, Pet Health
Expert, Community Moderator or Administrator. That becomes a pending role
request, and the user stays a Pet Owner until an administrator approves it.
"""
import re

from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash

from auth import PET_OWNER, make_token, public_user
from db import execute, query_one
from routes.role_requests import check_request, save_request

bp = Blueprint("signup", __name__, url_prefix="/api")

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def password_problem(password):
    """Return what's wrong with the password, or None if it's strong enough."""
    if len(password) < 8:
        return "Password must be at least 8 characters."
    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        return "Password must include at least one letter and one number."
    return None


@bp.post("/signup")
def signup():
    data = request.get_json(silent=True) or {}
    full_name = " ".join(str(data.get("full_name", "")).split())
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not full_name or not email or not password:
        return jsonify(message="Enter your name, email and password."), 400
    if len(full_name) > 255 or len(email) > 255:
        return jsonify(message="Name and email must be under 255 characters."), 400
    if not EMAIL_PATTERN.match(email):
        return jsonify(message="Enter a valid email address."), 400
    problem = password_problem(password)
    if problem:
        return jsonify(message=problem), 400
    if query_one("SELECT user_id FROM User WHERE LOWER(email) = %s", (email,)):
        return jsonify(message="An account with this email already exists. Try signing in."), 409

    # Optional user type: anything but Pet Owner becomes a pending request
    wanted = str(data.get("requested_role") or PET_OWNER)
    role_request = None
    if wanted != PET_OWNER:
        role_request = {k: data.get(k, "") for k in ("reason", "credentials", "specialty", "organization", "experience")}
        role_request["role"] = wanted
        problem, code = check_request(role_request, [PET_OWNER])
        if problem:
            return jsonify(message=problem), code

    role = query_one("SELECT role_id FROM Role WHERE role_name = %s", (PET_OWNER,))
    user_id = execute(
        "INSERT INTO User (email, password_hash, full_name, account_status) VALUES (%s, %s, %s, 'active')",
        (email, generate_password_hash(password, method="pbkdf2:sha256:600000"), full_name),
    )
    execute("INSERT INTO User_Role (user_id, role_id) VALUES (%s, %s)", (user_id, role["role_id"]))

    requested = None
    if role_request:
        request_id, _error = save_request(user_id, role_request)
        requested = {"request_id": request_id, "role": wanted, "status": "pending"}

    user = {"user_id": user_id, "full_name": full_name, "email": email}
    return jsonify(token=make_token(user_id), requested_role=requested, **public_user(user, [PET_OWNER])), 201
