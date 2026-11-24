"""Any signed-in user: report a post or a piece of health advice.

This is the prerequisite for the Community Moderator use case: the reports
filed here are what the moderator reviews on Reported Posts and Advice.

POST /api/reports   {"post_id": 123, "reason": "..."}  or  {"response_id": 45, "reason": "..."}
"""
from flask import Blueprint, g, jsonify, request

from auth import (ADMINISTRATOR, COMMUNITY_MODERATOR, PET_HEALTH_EXPERT, PET_OWNER, VETERINARIAN,
                  require_roles)
from db import execute, query_one
from helpers import clean, log_event, missing, now

bp = Blueprint("reports", __name__, url_prefix="/api/reports")


@bp.post("")
@require_roles(PET_OWNER, VETERINARIAN, PET_HEALTH_EXPERT, COMMUNITY_MODERATOR, ADMINISTRATOR)
def file_report():
    data = request.get_json(silent=True) or {}
    post_id, response_id = clean(data, "post_id"), clean(data, "response_id")

    # 1. Exactly one thing to report, and a reason
    if bool(post_id) == bool(response_id):
        return jsonify(message="Report one post or one answer."), 400
    problem = missing(data, "reason")
    if problem:
        return jsonify(message="Please say what is wrong with it."), 400

    # 2. It must exist (a removed post can't be reported again)
    if post_id:
        target = query_one("SELECT post_id AS id, author_user_id AS author FROM Post "
                           "WHERE post_id = %s AND status = 'published'", (post_id,))
        column = "post_id"
    else:
        target = query_one("SELECT response_id AS id, author_user_id AS author FROM Advice_Response "
                           "WHERE response_id = %s", (response_id,))
        column = "response_id"
    if target is None:
        return jsonify(message="That post or answer was not found."), 404

    # 3. Not your own content, and not twice while your first report is open
    if target["author"] == g.user["user_id"]:
        return jsonify(message="You can't report your own content."), 400
    if query_one(f"SELECT report_id FROM Report WHERE {column} = %s AND reporter_user_id = %s "
                 "AND status = 'open'", (target["id"], g.user["user_id"])):
        return jsonify(message="You already reported this. A moderator will review it."), 409

    report_id = execute(f"INSERT INTO Report (reporter_user_id, {column}, reason, status, created_at) "
                        "VALUES (%s, %s, %s, 'open', %s)",
                        (g.user["user_id"], target["id"], clean(data, "reason", 1000), now()))
    log_event(g.user["user_id"], "file_report", "Report", report_id)
    return jsonify(message="Thanks. A moderator will review your report.", report_id=report_id), 201
