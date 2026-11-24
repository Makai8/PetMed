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
    data = request.get_json(silent=True) or {}
    problem = one_of(data, "action", ACTIONS) or missing(data, "reason")
    if problem:
        return jsonify(message=problem), 400
    action = clean(data, "action")
    reason = clean(data, "reason")

    report = query_one("SELECT r.report_id, r.status, r.post_id, r.response_id, "
                       "p.author_user_id AS post_author, ar.author_user_id AS advice_author "
                       "FROM Report r LEFT JOIN Post p ON p.post_id = r.post_id "
                       "LEFT JOIN Advice_Response ar ON ar.response_id = r.response_id "
                       "WHERE r.report_id = %s", (report_id,))
    if report is None:
        return jsonify(message="Report not found."), 404
    if report["status"] != "open":
        return jsonify(message="This report was already resolved."), 409
    author = report["post_author"] or report["advice_author"]
    me = g.user["user_id"]
    when = now()

    case = query_one("SELECT case_id FROM Moderation_Case WHERE report_id = %s "
                     "ORDER BY case_id DESC LIMIT 1", (report_id,))
    if case is None:
        case_id = execute("INSERT INTO Moderation_Case (report_id, assigned_moderator_id, case_status, opened_at) "
                          "VALUES (%s, %s, 'open', %s)", (report_id, me, when))
    else:
        case_id = case["case_id"]

    if action == "remove_content":
        if report["post_id"] is not None:
            execute("UPDATE Post SET status = 'removed' WHERE post_id = %s", (report["post_id"],))
        elif report["response_id"] is not None:
            execute("UPDATE Advice_Response SET response_text = %s WHERE response_id = %s",
                    (REMOVED_TEXT, report["response_id"]))

    action_id = execute("INSERT INTO Moderation_Action (case_id, actor_user_id, target_user_id, action_type, "
                        "reason, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
                        (case_id, me, author, action, reason, when))

    if action == "escalate":
        execute("UPDATE Moderation_Case SET case_status = 'escalated', assigned_moderator_id = %s "
                "WHERE case_id = %s", (me, case_id))
    else:
        execute("UPDATE Moderation_Case SET case_status = 'closed', closed_at = %s, assigned_moderator_id = %s "
                "WHERE case_id = %s", (when, me, case_id))
        execute("UPDATE Report SET status = 'resolved' WHERE report_id = %s", (report_id,))

    log_event(me, f"moderation_{action}", "Moderation_Case", case_id)

    case = query_one("SELECT case_id, report_id, assigned_moderator_id, case_status, opened_at, closed_at "
                     "FROM Moderation_Case WHERE case_id = %s", (case_id,))
    report = query_one("SELECT report_id, status, post_id, response_id, reason FROM Report WHERE report_id = %s",
                       (report_id,))
    return jsonify(message="Case updated.", action_id=action_id, case=case, report=report)
