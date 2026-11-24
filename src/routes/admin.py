"""Administrator: manage user accounts.

Sprint IV: search, browse and list users.
    GET  /api/admin/users?q=&role=&status=
Account management:
    POST /api/admin/users/<user_id>/status   {"status": "suspended", "reason": "..."} or {"status": "active"}
    POST /api/admin/users                    {"full_name", "email", "password", "role"}

A suspended user can't sign in, and any session they already have stops
working on their next click (auth.py checks account_status on every request).
"""
from flask import Blueprint, g, jsonify, request
from werkzeug.security import generate_password_hash

from auth import ADMINISTRATOR, COMMUNITY_MODERATOR, PET_HEALTH_EXPERT, PET_OWNER, VETERINARIAN, require_roles
from db import execute, query, query_one
from helpers import clean, log_event, missing, now
from routes.signup import EMAIL_PATTERN, password_problem

bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@bp.get("/users")
@require_roles(ADMINISTRATOR)
def list_users():
    q = request.args.get("q", "").strip()
    role = request.args.get("role", "").strip()
    status = request.args.get("status", "").strip()

    sql = ("SELECT u.user_id, u.full_name, u.email, u.account_status, u.created_at "
           "FROM User u WHERE 1 = 1")
    params = []
    if q:
        sql += " AND (u.full_name LIKE %s OR u.email LIKE %s)"
        params += [f"%{q}%", f"%{q}%"]
    if status:
        sql += " AND u.account_status = %s"
        params.append(status)
    if role:
        sql += (" AND EXISTS (SELECT 1 FROM User_Role ur JOIN Role r ON r.role_id = ur.role_id "
                "WHERE ur.user_id = u.user_id AND r.role_name = %s)")
        params.append(role)
    sql += " ORDER BY u.full_name"
    users = query(sql, params)

    # Attach each user's roles (a user can hold more than one)
    role_rows = query("SELECT ur.user_id, r.role_name FROM User_Role ur "
                      "JOIN Role r ON r.role_id = ur.role_id ORDER BY r.role_id")
    roles_by_user = {}
    for r in role_rows:
        roles_by_user.setdefault(r["user_id"], []).append(r["role_name"])
    for u in users:
        u["roles"] = roles_by_user.get(u["user_id"], [])

    all_roles = [r["role_name"] for r in query("SELECT role_name FROM Role ORDER BY role_id")]
    return jsonify(users=users, count=len(users), roles=all_roles)


# ------------------------------------------------------------- Account management

STATUSES = ("active", "suspended")
# Vets and experts can't be created directly: they apply with credentials
# and an administrator verifies them (Professional Verification).
CREATABLE_ROLES = (PET_OWNER, COMMUNITY_MODERATOR, ADMINISTRATOR)


def user_row(user_id):
    user = query_one("SELECT user_id, full_name, email, account_status, created_at FROM User WHERE user_id = %s",
                     (user_id,))
    if user:
        user["roles"] = [r["role_name"] for r in query(
            "SELECT r.role_name FROM User_Role ur JOIN Role r ON r.role_id = ur.role_id "
            "WHERE ur.user_id = %s ORDER BY r.role_id", (user_id,))]
    return user


@bp.post("/users/<int:user_id>/status")
@require_roles(ADMINISTRATOR)
def change_status(user_id):
    data = request.get_json(silent=True) or {}
    status, reason = clean(data, "status"), clean(data, "reason", 500)
    if status not in STATUSES:
        return jsonify(message="Choose Suspend or Reactivate."), 400
    if status == "suspended" and not reason:
        return jsonify(message="Give a reason for the suspension. The user is told why."), 400
    if user_id == g.user["user_id"]:
        return jsonify(message="You can't change your own account status."), 400

    user = user_row(user_id)
    if user is None:
        return jsonify(message="User not found."), 404
    if user["account_status"] == status:
        return jsonify(message=f"{user['full_name']} is already {status}."), 409

    execute("UPDATE User SET account_status = %s WHERE user_id = %s", (status, user_id))
    note = (f"Your PetMed account was suspended by an administrator. Reason: {reason}" if status == "suspended"
            else "Your PetMed account was reactivated. You can sign in again.")
    execute("INSERT INTO Notification (user_id, type, message, is_read, created_at) VALUES (%s, 'account', %s, FALSE, %s)",
            (user_id, note, now()))
    log_event(g.user["user_id"], "user_suspended" if status == "suspended" else "user_reactivated", "User", user_id)

    verb = "suspended" if status == "suspended" else "reactivated"
    return jsonify(message=f"{user['full_name']} was {verb}.", before=user["account_status"], user=user_row(user_id))


@bp.post("/users")
@require_roles(ADMINISTRATOR)
def add_user():
    data = request.get_json(silent=True) or {}
    problem = missing(data, "full_name", "email", "password", "role")
    if problem:
        return jsonify(message=problem), 400
    full_name = clean(data, "full_name", 255)
    email = clean(data, "email", 255).lower()
    password = str(data.get("password", ""))
    role = clean(data, "role")

    if role in (VETERINARIAN, PET_HEALTH_EXPERT):
        return jsonify(message="Vets and experts must apply with their credentials and be verified. "
                               "Create them as a Pet Owner, then have them use Request a Professional Role."), 400
    if role not in CREATABLE_ROLES:
        return jsonify(message="Choose Pet Owner, Community Moderator or Administrator."), 400
    if not EMAIL_PATTERN.match(email):
        return jsonify(message="Enter a valid email address."), 400
    problem = password_problem(password)
    if problem:
        return jsonify(message=problem), 400
    if query_one("SELECT user_id FROM User WHERE LOWER(email) = %s", (email,)):
        return jsonify(message="An account with this email already exists."), 409

    new_id = execute("INSERT INTO User (email, password_hash, full_name, account_status, created_at) "
                     "VALUES (%s, %s, %s, 'active', %s)",
                     (email, generate_password_hash(password, method="pbkdf2:sha256:600000"), full_name, now()))
    role_id = query_one("SELECT role_id FROM Role WHERE role_name = %s", (role,))["role_id"]
    execute("INSERT INTO User_Role (user_id, role_id) VALUES (%s, %s)", (new_id, role_id))
    log_event(g.user["user_id"], "user_created", "User", new_id)
    return jsonify(message=f"{full_name} was added. Give them the temporary password so they can sign in.",
                   user=user_row(new_id)), 201
