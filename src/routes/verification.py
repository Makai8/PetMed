"""Administrator use case (Sprint V): review a Veterinarian or Pet Health Expert
account and update its professional verification status.

GET  /api/admin/professionals?status=pending|approved|rejected|suspended|all
POST /api/admin/professionals/<profile_id>/status   {"status": "...", "notes": "..."}

What a decision changes in the database:
- Professional_Profile.verification_status gets the new status.
- A Verification_Review row records who decided, when, and why.
- Approving also gives the user the matching role (User_Role) if they don't
  have it yet, and closes their pending Role_Request for that role.
- Rejected or suspended professionals keep their account, but the vet and
  expert features check verification_status and lock them out.
- An Audit_Event row is added for the history.
"""
from flask import Blueprint, g, jsonify, request

from auth import ADMINISTRATOR, require_roles
from db import execute, query, query_one
from helpers import clean, log_event, now, one_of

bp = Blueprint("verification", __name__, url_prefix="/api/admin/professionals")

STATUSES = ("pending", "approved", "rejected", "suspended")
DECISIONS = ("approved", "rejected", "suspended")


def profile_rows(where="", params=()):
    rows = query(
        "SELECT pp.profile_id, pp.user_id, pp.professional_type, pp.credentials, pp.specialty, "
        "pp.organization, pp.experience, pp.verification_status, "
        "u.full_name, u.email, u.account_status, u.created_at "
        "FROM Professional_Profile pp JOIN User u ON u.user_id = pp.user_id " + where +
        " ORDER BY CASE pp.verification_status WHEN 'pending' THEN 0 ELSE 1 END, u.full_name",
        params)
    history = {}
    for r in query("SELECT vr.profile_id, vr.decision, vr.reviewed_at, vr.notes, a.full_name AS reviewed_by "
                   "FROM Verification_Review vr JOIN User a ON a.user_id = vr.admin_user_id "
                   "ORDER BY vr.reviewed_at DESC, vr.review_id DESC"):
        history.setdefault(r["profile_id"], []).append(
            {k: r[k] for k in ("decision", "reviewed_at", "notes", "reviewed_by")})
    for r in rows:
        r["history"] = history.get(r["profile_id"], [])
    return rows


@bp.get("")
@require_roles(ADMINISTRATOR)
def list_professionals():
    status = request.args.get("status", "pending")
    if status in STATUSES:
        rows = profile_rows("WHERE pp.verification_status = %s", (status,))
    else:
        rows = profile_rows()
    counts = {s: 0 for s in STATUSES}
    for r in query("SELECT verification_status AS s, COUNT(*) AS n FROM Professional_Profile "
                   "GROUP BY verification_status"):
        counts[r["s"]] = r["n"]
    return jsonify(professionals=rows, count=len(rows), counts=counts)


@bp.post("/<int:profile_id>/status")
@require_roles(ADMINISTRATOR)
def update_status(profile_id):
    data = request.get_json(silent=True) or {}
    problem = one_of(data, "status", DECISIONS)
    if problem:
        return jsonify(message="Choose Approve, Reject or Suspend."), 400
    status = clean(data, "status")
    notes = clean(data, "notes")
    if status != "approved" and not notes:
        return jsonify(message="Add a note explaining why. The professional will see it."), 400

    profile = query_one("SELECT pp.profile_id, pp.user_id, pp.professional_type, pp.verification_status "
                        "FROM Professional_Profile pp WHERE pp.profile_id = %s", (profile_id,))
    if profile is None:
        return jsonify(message="Professional profile not found."), 404
    if profile["verification_status"] == status:
        return jsonify(message=f"This profile is already {status}."), 409

    when = now()
    execute("UPDATE Professional_Profile SET verification_status = %s WHERE profile_id = %s",
            (status, profile_id))
    execute("INSERT INTO Verification_Review (profile_id, admin_user_id, decision, reviewed_at, notes) "
            "VALUES (%s, %s, %s, %s, %s)",
            (profile_id, g.user["user_id"], status, when, notes or "Credentials verified."))

    if status == "approved":
        role = query_one("SELECT role_id FROM Role WHERE role_name = %s", (profile["professional_type"],))
        if not query_one("SELECT 1 AS found FROM User_Role WHERE user_id = %s AND role_id = %s",
                         (profile["user_id"], role["role_id"])):
            execute("INSERT INTO User_Role (user_id, role_id) VALUES (%s, %s)",
                    (profile["user_id"], role["role_id"]))
        execute("UPDATE Role_Request SET status = 'approved', reviewed_by_user_id = %s, reviewed_at = %s, "
                "review_notes = %s WHERE user_id = %s AND role_id = %s AND status = 'pending'",
                (g.user["user_id"], when, notes, profile["user_id"], role["role_id"]))

    log_event(g.user["user_id"], f"verification_{status}", "Professional_Profile", profile_id)

    return jsonify(message=f"Verification status changed from {profile['verification_status']} to {status}.",
                   before=profile["verification_status"],
                   professional=profile_rows("WHERE pp.profile_id = %s", (profile_id,))[0])
