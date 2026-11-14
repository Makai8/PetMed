"""Administrator use case: search, browse and list users."""
from flask import Blueprint, jsonify, request

from auth import ADMINISTRATOR, require_roles
from db import query

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
