"""Role home screens: the "at a glance" numbers and lists at the top of each
role's dashboard. GET /api/home?role=<role> returns what matters to that role,
read live from the database. The role must be one the signed-in user holds.
"""
from flask import Blueprint, g, jsonify, request

from auth import (ADMINISTRATOR, COMMUNITY_MODERATOR, PET_HEALTH_EXPERT, PET_OWNER,
                  VETERINARIAN, require_roles)
from db import query, query_one

bp = Blueprint("home", __name__, url_prefix="/api")


def count(sql, params=()):
    return query_one(sql, params)["n"]


def pet_owner_home(uid):
    pets = query("SELECT pet_id, name, species, breed, weight FROM Pet WHERE owner_user_id = %s ORDER BY name", (uid,))
    reminders = query(
        "SELECT r.due_at, p.name AS pet_name, pm.name AS medication FROM Reminder r "
        "JOIN Pet p ON p.pet_id = r.pet_id LEFT JOIN Pet_Medication pm ON pm.pet_medication_id = r.pet_medication_id "
        "WHERE r.user_id = %s AND r.status = 'scheduled' ORDER BY r.due_at LIMIT 3", (uid,))
    questions = query(
        "SELECT hq.question_id, hq.question_text, hq.created_at, "
        "(SELECT COUNT(*) FROM Advice_Response ar WHERE ar.question_id = hq.question_id) AS answers "
        "FROM Health_Question hq WHERE hq.asker_user_id = %s ORDER BY hq.created_at DESC LIMIT 3", (uid,))
    return {
        "stats": [
            {"label": "My pets", "value": len(pets)},
            {"label": "Questions asked", "value": count("SELECT COUNT(*) AS n FROM Health_Question WHERE asker_user_id = %s", (uid,))},
            {"label": "My posts", "value": count("SELECT COUNT(*) AS n FROM Post WHERE author_user_id = %s", (uid,))},
            {"label": "Scheduled reminders", "value": count("SELECT COUNT(*) AS n FROM Reminder WHERE user_id = %s AND status = 'scheduled'", (uid,))},
        ],
        "pets": pets,
        "reminders": reminders,
        "questions": questions,
    }


def veterinarian_home(uid):
    unanswered = "NOT EXISTS (SELECT 1 FROM Advice_Response ar WHERE ar.question_id = hq.question_id)"
    latest = query(
        "SELECT hq.question_id, hq.question_text, hq.created_at, asker.full_name AS asked_by, pet.name AS pet_name, "
        "hq.directed_to_user_id FROM Health_Question hq JOIN User asker ON asker.user_id = hq.asker_user_id "
        "LEFT JOIN Pet pet ON pet.pet_id = hq.pet_id "
        f"WHERE (hq.directed_to_user_id = %s OR hq.directed_to_user_id IS NULL) AND {unanswered} "
        "ORDER BY hq.created_at DESC LIMIT 3", (uid,))
    for item in latest:
        item["sent_to_me"] = item.pop("directed_to_user_id") == uid
    return {
        "stats": [
            {"label": "Sent to me", "value": count("SELECT COUNT(*) AS n FROM Health_Question hq WHERE hq.directed_to_user_id = %s", (uid,))},
            {"label": "Open to any vet", "value": count("SELECT COUNT(*) AS n FROM Health_Question hq WHERE hq.directed_to_user_id IS NULL")},
            {"label": "Unanswered", "value": count(f"SELECT COUNT(*) AS n FROM Health_Question hq WHERE {unanswered}")},
            {"label": "Records shared with me", "value": count(
                "SELECT COUNT(*) AS n FROM Data_Share_Authorization WHERE professional_user_id = %s AND revoked_at IS NULL", (uid,))},
        ],
        "questions": latest,
    }


def expert_home(uid):
    profile = query_one("SELECT specialty, organization, verification_status FROM Professional_Profile WHERE user_id = %s", (uid,))
    if profile is None:
        return {"profile": None, "stats": [], "posts": []}
    tag = profile["specialty"].strip().lower().replace(" ", "-")
    tagged = ("FROM Post p JOIN Post_Tag pt ON pt.post_id = p.post_id JOIN Tag t ON t.tag_id = pt.tag_id "
              "WHERE p.status = 'published' AND t.tag_name = %s")
    return {
        "profile": profile,
        "tag": tag,
        "stats": [
            {"label": "Questions sent to me", "value": count("SELECT COUNT(*) AS n FROM Health_Question WHERE directed_to_user_id = %s", (uid,))},
            {"label": "Waiting for an answer", "value": count(
                "SELECT COUNT(*) AS n FROM Health_Question hq WHERE hq.directed_to_user_id = %s AND NOT EXISTS "
                "(SELECT 1 FROM Advice_Response ar WHERE ar.question_id = hq.question_id)", (uid,))},
            {"label": f"Posts tagged #{tag}", "value": count(f"SELECT COUNT(*) AS n {tagged}", (tag,))},
            {"label": "My answers", "value": count("SELECT COUNT(*) AS n FROM Advice_Response WHERE author_user_id = %s", (uid,))},
        ],
        "posts": query(f"SELECT p.post_id, p.body, p.created_at, u.full_name AS author {tagged.replace('FROM Post p', 'FROM Post p JOIN User u ON u.user_id = p.author_user_id')} "
                       "ORDER BY p.created_at DESC LIMIT 3", (tag,)),
    }


def moderator_home(uid):
    return {
        "stats": [
            {"label": "Open reports", "value": count("SELECT COUNT(*) AS n FROM Report WHERE status = 'open'")},
            {"label": "My open cases", "value": count(
                "SELECT COUNT(*) AS n FROM Moderation_Case WHERE assigned_moderator_id = %s AND case_status = 'open'", (uid,))},
            {"label": "Unassigned cases", "value": count(
                "SELECT COUNT(*) AS n FROM Moderation_Case WHERE assigned_moderator_id IS NULL AND case_status = 'open'")},
            {"label": "Suspended users", "value": count("SELECT COUNT(*) AS n FROM User WHERE account_status = 'suspended'")},
        ],
        "reports": query(
            "SELECT r.report_id, r.reason, r.created_at, reporter.full_name AS reported_by, "
            "CASE WHEN r.post_id IS NOT NULL THEN 'post' WHEN r.response_id IS NOT NULL THEN 'advice' "
            "WHEN r.reported_user_id IS NOT NULL THEN 'user' WHEN r.product_id IS NOT NULL THEN 'product' ELSE 'comment' END AS kind "
            "FROM Report r JOIN User reporter ON reporter.user_id = r.reporter_user_id "
            "WHERE r.status = 'open' ORDER BY r.created_at DESC LIMIT 3"),
    }


def administrator_home(uid):
    stats = [
        {"label": "Total users", "value": count("SELECT COUNT(*) AS n FROM User")},
        {"label": "Active", "value": count("SELECT COUNT(*) AS n FROM User WHERE account_status = 'active'")},
        {"label": "Suspended", "value": count("SELECT COUNT(*) AS n FROM User WHERE account_status = 'suspended'")},
    ]
    try:
        stats.append({"label": "Pending role requests",
                      "value": count("SELECT COUNT(*) AS n FROM Role_Request WHERE status = 'pending'")})
    except Exception:  # Role_Request table not created yet (sprint5_role_requests.sql)
        stats.append({"label": "Open reports", "value": count("SELECT COUNT(*) AS n FROM Report WHERE status = 'open'")})
    newest = query("SELECT user_id, full_name, email, account_status, created_at FROM User "
                   "ORDER BY created_at DESC, user_id DESC LIMIT 4")
    return {"stats": stats, "newest_users": newest}


BUILDERS = {
    PET_OWNER: pet_owner_home,
    VETERINARIAN: veterinarian_home,
    PET_HEALTH_EXPERT: expert_home,
    COMMUNITY_MODERATOR: moderator_home,
    ADMINISTRATOR: administrator_home,
}


@bp.get("/home")
@require_roles()  # any signed-in user, for a role they actually hold
def role_home():
    role = request.args.get("role", "")
    if role not in g.roles:
        return jsonify(message="Your role is not allowed to use this feature."), 403
    return jsonify(role=role, **BUILDERS[role](g.user["user_id"]))
