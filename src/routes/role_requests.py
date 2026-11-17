"""Role requests (Sprint V).

Any signed-in user can ask for an extra role: Veterinarian, Pet Health Expert,
Community Moderator or Administrator. Nobody gets a role by asking: an
administrator approves or rejects every request.

Veterinarians and Pet Health Experts also send their credentials. Those go in
Professional_Profile (status "pending"), and the administrator's decision is
recorded in Verification_Review, the tables the ERD already has for this.
"""
import datetime

from flask import Blueprint, g, jsonify, request

from auth import (ADMINISTRATOR, COMMUNITY_MODERATOR, PET_HEALTH_EXPERT,
                  VETERINARIAN, require_roles)
from db import execute, query, query_one

bp = Blueprint("role_requests", __name__, url_prefix="/api")

REQUESTABLE = (VETERINARIAN, PET_HEALTH_EXPERT, COMMUNITY_MODERATOR, ADMINISTRATOR)
PROFESSIONAL = (VETERINARIAN, PET_HEALTH_EXPERT)


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def text(data, key, limit=2000):
    return " ".join(str(data.get(key, "")).split())[:limit]


# ---------------------------------------------------------------- user side

def check_request(data, current_roles):
    """Check a role request before saving anything.
    Returns (problem, http_status), or (None, None) if it's fine."""
    role_name = str(data.get("role", ""))
    if role_name not in REQUESTABLE:
        return "Choose Veterinarian, Pet Health Expert, Community Moderator or Administrator.", 400
    if not text(data, "reason"):
        return "Tell the administrators why you're requesting this role.", 400
    if role_name in current_roles:
        return "You already have this role.", 409
    if role_name in PROFESSIONAL:
        if not text(data, "credentials") or not text(data, "organization"):
            return "Enter your license or credentials and where you work.", 400
        if role_name == PET_HEALTH_EXPERT and not text(data, "specialty"):
            return "Enter your area of expertise, for example Nutrition.", 400
    return None, None


def save_request(user_id, data):
    """Save a checked request (and a pending Professional_Profile for vets and
    experts). Returns (request_id, None), or (None, (problem, http_status))."""
    role_name = str(data.get("role", ""))
    reason = text(data, "reason")
    role = query_one("SELECT role_id FROM Role WHERE role_name = %s", (role_name,))
    if query_one("SELECT request_id FROM Role_Request WHERE user_id = %s AND role_id = %s AND status = 'pending'",
                 (user_id, role["role_id"])):
        return None, ("You already have a pending request for this role.", 409)

    if role_name in PROFESSIONAL:
        details = {k: text(data, k, 255 if k in ("specialty", "organization") else 2000)
                   for k in ("credentials", "specialty", "organization", "experience")}
        if role_name == VETERINARIAN and not details["specialty"]:
            details["specialty"] = "General Practice"
        profile = query_one("SELECT profile_id, professional_type, verification_status "
                            "FROM Professional_Profile WHERE user_id = %s", (user_id,))
        if profile and profile["professional_type"] != role_name and profile["verification_status"] != "rejected":
            return None, ("You already have a professional profile of another type.", 409)
        if profile:
            execute("UPDATE Professional_Profile SET professional_type = %s, credentials = %s, specialty = %s, "
                    "organization = %s, experience = %s, verification_status = 'pending' WHERE profile_id = %s",
                    (role_name, details["credentials"], details["specialty"], details["organization"],
                     details["experience"], profile["profile_id"]))
        else:
            execute("INSERT INTO Professional_Profile (user_id, professional_type, credentials, specialty, "
                    "organization, experience, verification_status) VALUES (%s, %s, %s, %s, %s, %s, 'pending')",
                    (user_id, role_name, details["credentials"], details["specialty"], details["organization"],
                     details["experience"]))

    request_id = execute("INSERT INTO Role_Request (user_id, role_id, reason, status, requested_at) "
                         "VALUES (%s, %s, %s, 'pending', %s)", (user_id, role["role_id"], reason, now()))
    return request_id, None


@bp.post("/role-requests")
@require_roles()  # any signed-in user
def create_request():
    data = request.get_json(silent=True) or {}
    problem, code = check_request(data, g.roles)
    if problem:
        return jsonify(message=problem), code
    request_id, error = save_request(g.user["user_id"], data)
    if error:
        return jsonify(message=error[0]), error[1]
    return jsonify(request_id=request_id, status="pending",
                   message="Request sent. An administrator will review it."), 201


@bp.get("/role-requests/mine")
@require_roles()
def my_requests():
    rows = query("SELECT rr.request_id, r.role_name AS role, rr.status, rr.reason, rr.requested_at, "
                 "rr.reviewed_at, rr.review_notes FROM Role_Request rr JOIN Role r ON r.role_id = rr.role_id "
                 "WHERE rr.user_id = %s ORDER BY rr.requested_at DESC, rr.request_id DESC",
                 (g.user["user_id"],))
    return jsonify(requests=rows, roles=g.roles)


# --------------------------------------------------------------- admin side

@bp.get("/admin/role-requests")
@require_roles(ADMINISTRATOR)
def list_requests():
    status = request.args.get("status", "pending")
    sql = ("SELECT rr.request_id, rr.status, rr.reason, rr.requested_at, rr.reviewed_at, rr.review_notes, "
           "r.role_name AS role, u.user_id, u.full_name, u.email, reviewer.full_name AS reviewed_by, "
           "pp.credentials, pp.specialty, pp.organization, pp.experience "
           "FROM Role_Request rr "
           "JOIN Role r ON r.role_id = rr.role_id "
           "JOIN User u ON u.user_id = rr.user_id "
           "LEFT JOIN User reviewer ON reviewer.user_id = rr.reviewed_by_user_id "
           "LEFT JOIN Professional_Profile pp ON pp.user_id = rr.user_id AND pp.professional_type = r.role_name ")
    params = []
    if status in ("pending", "approved", "rejected"):
        sql += "WHERE rr.status = %s "
        params.append(status)
    sql += "ORDER BY rr.requested_at DESC, rr.request_id DESC"
    rows = query(sql, params)
    return jsonify(requests=rows, count=len(rows))


def decide(request_id, decision):
    data = request.get_json(silent=True) or {}
    notes = text(data, "notes")
    req = query_one("SELECT rr.request_id, rr.user_id, rr.role_id, rr.status, r.role_name "
                    "FROM Role_Request rr JOIN Role r ON r.role_id = rr.role_id WHERE rr.request_id = %s",
                    (request_id,))
    if req is None:
        return jsonify(message="Request not found."), 404
    if req["status"] != "pending":
        return jsonify(message=f"This request was already {req['status']}."), 409

    when = now()
    execute("UPDATE Role_Request SET status = %s, reviewed_by_user_id = %s, reviewed_at = %s, review_notes = %s "
            "WHERE request_id = %s", (decision, g.user["user_id"], when, notes, request_id))

    if decision == "approved" and not query_one(
            "SELECT 1 AS found FROM User_Role WHERE user_id = %s AND role_id = %s", (req["user_id"], req["role_id"])):
        execute("INSERT INTO User_Role (user_id, role_id) VALUES (%s, %s)", (req["user_id"], req["role_id"]))

    if req["role_name"] in PROFESSIONAL:
        profile = query_one("SELECT profile_id FROM Professional_Profile WHERE user_id = %s", (req["user_id"],))
        if profile:
            execute("UPDATE Professional_Profile SET verification_status = %s WHERE profile_id = %s",
                    (decision, profile["profile_id"]))
            execute("INSERT INTO Verification_Review (profile_id, admin_user_id, decision, reviewed_at, notes) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (profile["profile_id"], g.user["user_id"], decision, when, notes))

    return jsonify(request_id=request_id, status=decision)


@bp.post("/admin/role-requests/<int:request_id>/approve")
@require_roles(ADMINISTRATOR)
def approve(request_id):
    return decide(request_id, "approved")


@bp.post("/admin/role-requests/<int:request_id>/reject")
@require_roles(ADMINISTRATOR)
def reject(request_id):
    return decide(request_id, "rejected")
