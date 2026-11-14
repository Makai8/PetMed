"""Community Moderator use case: view reported posts and reported health advice."""
from flask import Blueprint, jsonify, request

from auth import COMMUNITY_MODERATOR, require_roles
from db import query

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
           "mc.case_status, moderator.full_name AS assigned_to "
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
