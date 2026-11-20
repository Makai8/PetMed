"""Community Moderator use cases.

Sprint IV: view reported posts and reported health advice.
Sprint V:  review a report and update its moderation case with the action taken
           (POST /api/moderation/reports/<report_id>/decision
            {"action": "dismiss|remove_content|warn_user|escalate", "reason": "..."}).
"""
from flask import Blueprint, g, jsonify, request

from auth import COMMUNITY_MODERATOR, require_roles
from db import execute, query, query_one
from helpers import clean, log_event, missing, now, one_of

bp = Blueprint("moderator", __name__, url_prefix="/api/moderation")


@bp.get("/reports")
@require_roles(COMMUNITY_MODERATOR)
def reported_content():
    kind = request.args.get("type", "all")      # all | post | advice
    status = request.args.get("status", "open")  # open | resolved | all

    sql = ("SELECT r.report_id, r.reason, r.status, r.created_at, "
           "reporter.full_name AS reported_by, "
           "r.post_id, p.body AS post_body, post_author.full_name AS post_author, "
           "r.response_id, ar.response_text, ar.source_type, advice_author.full_name AS advice_author, "
           "hq.question_text AS advice_question, "
           "mc.case_id, mc.case_status, moderator.full_name AS assigned_to, "
           "(SELECT ma.action_type FROM Moderation_Action ma WHERE ma.case_id = mc.case_id "
           " ORDER BY ma.created_at DESC, ma.action_id DESC LIMIT 1) AS last_action "
           "FROM Report r "
           "JOIN User reporter ON reporter.user_id = r.reporter_user_id "
           "LEFT JOIN Post p ON p.post_id = r.post_id "
           "LEFT JOIN User post_author ON post_author.user_id = p.author_user_id "
           "LEFT JOIN Advice_Response ar ON ar.response_id = r.response_id "
           "LEFT JOIN User advice_author ON advice_author.user_id = ar.author_user_id "
           "LEFT JOIN Health_Question hq ON hq.question_id = ar.question_id "
           "LEFT JOIN Moderation_Case mc ON mc.report_id = r.report_id "
           "LEFT JOIN User moderator ON moderator.user_id = mc.assigned_moderator_id ")
    if kind == "post":
        sql += "WHERE r.post_id IS NOT NULL"
    elif kind == "advice":
        sql += "WHERE r.response_id IS NOT NULL"
    else:
        sql += "WHERE (r.post_id IS NOT NULL OR r.response_id IS NOT NULL)"
    params = []
    if status in ("open", "resolved"):
        sql += " AND r.status = %s"
        params.append(status)
    sql += " ORDER BY r.created_at DESC"
    reports = query(sql, params)

    for r in reports:
        r["content_type"] = "post" if r["post_id"] is not None else "advice"
    return jsonify(reports=reports, count=len(reports))


# ------------------------------------------------------------- Sprint V

ACTIONS = ("dismiss", "remove_content", "warn_user", "escalate")
REMOVED_TEXT = "[Removed by a PetMed moderator]"


@bp.post("/reports/<int:report_id>/decision")
@require_roles(COMMUNITY_MODERATOR)
def decide_report(report_id):
    # ===================== MAKEL: build this (Sprint V) =====================
    # The moderator reviews a report and records the action on its moderation case.
    # Worked example to copy from: update_status() in routes/verification.py
    # Done when: python -m pytest tests -k Moderator   passes (no skips).
    #
    # 1. data = request.get_json(silent=True) or {}
    #    problem = one_of(data, "action", ACTIONS) or missing(data, "reason") -> 400
    # 2. report = query_one("SELECT r.report_id, r.status, r.post_id, r.response_id, "
    #                       "p.author_user_id AS post_author, ar.author_user_id AS advice_author "
    #                       "FROM Report r LEFT JOIN Post p ON p.post_id = r.post_id "
    #                       "LEFT JOIN Advice_Response ar ON ar.response_id = r.response_id "
    #                       "WHERE r.report_id = %s", (report_id,))
    #    Not found -> 404.  report["status"] != 'open' -> 409 "This report was already resolved."
    #    author = report["post_author"] or report["advice_author"]
    # 3. Find the report's Moderation_Case. If there isn't one, INSERT one
    #    (report_id, assigned_moderator_id = g.user["user_id"], case_status 'open', opened_at now()).
    # 4. If action is "remove_content":
    #      a post   -> UPDATE Post SET status = 'removed' WHERE post_id = ...
    #      advice   -> UPDATE Advice_Response SET response_text = REMOVED_TEXT WHERE response_id = ...
    # 5. INSERT INTO Moderation_Action (case_id, actor_user_id, target_user_id, action_type, reason, created_at)
    #    with target_user_id = author.
    # 6. "escalate": UPDATE Moderation_Case SET case_status = 'escalated', assigned_moderator_id = you
    #               (the report stays open).
    #    anything else: case_status 'closed', closed_at now(), assigned_moderator_id = you,
    #               and UPDATE Report SET status = 'resolved'.
    # 7. log_event(g.user["user_id"], f"moderation_{action}", "Moderation_Case", case_id)
    # 8. Read the case and report back and
    #    return jsonify(message="Case updated.", action_id=action_id, case=case, report=report)
    # Then delete the line below.
    return jsonify(message="Not built yet: Makel is building Review a Report (Sprint V)."), 501
