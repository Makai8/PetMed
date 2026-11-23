"""Pet Health Expert use case: browse questions and posts in the expert's approved specialty.

The specialty comes from Professional_Profile. Posts match when they carry the
tag with the same name (specialty "Nutrition" -> tag "nutrition").
An expert whose profile is not approved yet cannot use this feature.

Sprint V: answer a question inside the expert's approved area
(POST /api/expert/questions/<question_id>/answer  {"response_text": "..."}).
A question is inside the expert's area when it was sent to this expert.
"""
from flask import Blueprint, g, jsonify, request

from auth import PET_HEALTH_EXPERT, require_roles
from db import execute, query, query_one
from helpers import clean, log_event, now

bp = Blueprint("expert", __name__, url_prefix="/api/expert")


@bp.get("/topics")
@require_roles(PET_HEALTH_EXPERT)
def expertise_topics():
    profile = query_one(
        "SELECT specialty, verification_status, organization FROM Professional_Profile "
        "WHERE user_id = %s", (g.user["user_id"],))
    if profile is None or profile["verification_status"] != "approved":
        return jsonify(message="Your expert profile has not been approved yet, "
                             "so expertise features are locked."), 403

    specialty = profile["specialty"]
    tag = specialty.strip().lower().replace(" ", "-")
    q = request.args.get("q", "").strip()
    like = f"%{q}%"

    q_sql = ("SELECT hq.question_id, hq.question_text, hq.created_at, "
             "asker.full_name AS asked_by, pet.name AS pet_name, pet.species AS pet_species, "
             "(SELECT COUNT(*) FROM Advice_Response ar WHERE ar.question_id = hq.question_id) AS answers "
             "FROM Health_Question hq "
             "JOIN User asker ON asker.user_id = hq.asker_user_id "
             "LEFT JOIN Pet pet ON pet.pet_id = hq.pet_id "
             "WHERE hq.directed_to_user_id = %s")
    q_params = [g.user["user_id"]]
    if q:
        q_sql += " AND hq.question_text LIKE %s"
        q_params.append(like)
    q_sql += " ORDER BY hq.created_at DESC"

    p_sql = ("SELECT p.post_id, p.body, p.post_type, p.created_at, u.full_name AS author, "
             "pet.name AS pet_name "
             "FROM Post p JOIN User u ON u.user_id = p.author_user_id "
             "LEFT JOIN Pet pet ON pet.pet_id = p.pet_id "
             "JOIN Post_Tag pt ON pt.post_id = p.post_id "
             "JOIN Tag t ON t.tag_id = pt.tag_id "
             "WHERE p.status = 'published' AND t.tag_name = %s")
    p_params = [tag]
    if q:
        p_sql += " AND p.body LIKE %s"
        p_params.append(like)
    p_sql += " ORDER BY p.created_at DESC"

    return jsonify(
        specialty=specialty,
        organization=profile["organization"],
        tag=tag,
        questions=query(q_sql, q_params),
        posts=query(p_sql, p_params),
    )


# ------------------------------------------------------------- Sprint V

MIN_ANSWER = 20


@bp.post("/questions/<int:question_id>/answer")
@require_roles(PET_HEALTH_EXPERT)
def answer_question(question_id):
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return jsonify(message="Send your answer as a JSON object."), 400
    text = clean(data, "response_text")
    if len(text) < MIN_ANSWER:
        return jsonify(message=f"Write at least {MIN_ANSWER} characters."), 400

    user_id = g.user["user_id"]
    profile = query_one(
        "SELECT specialty, verification_status FROM Professional_Profile "
        "WHERE user_id = %s AND professional_type = %s", (user_id, PET_HEALTH_EXPERT))
    if profile is None or profile["verification_status"] != "approved":
        return jsonify(message="Your expert profile has not been approved yet, "
                             "so you can't answer questions."), 403

    question = query_one(
        "SELECT question_id, directed_to_user_id FROM Health_Question WHERE question_id = %s",
        (question_id,))
    if question is None:
        return jsonify(message="Question not found."), 404
    if question["directed_to_user_id"] != user_id:
        return jsonify(message=f"This question is outside your approved area ({profile['specialty']})."), 403

    existing = query_one(
        "SELECT response_id FROM Advice_Response WHERE question_id = %s AND author_user_id = %s",
        (question_id, user_id))
    if existing is not None:
        return jsonify(message="You already answered this question."), 409

    response_id = execute(
        "INSERT INTO Advice_Response (question_id, author_user_id, response_text, source_type, created_at) "
        "VALUES (%s, %s, %s, %s, %s)", (question_id, user_id, text, PET_HEALTH_EXPERT, now()))
    log_event(user_id, "answer_question", "Advice_Response", response_id)
    return jsonify(message="Your answer was posted.", response_id=response_id,
                   author=g.user["full_name"], source_type=PET_HEALTH_EXPERT, response_text=text), 201
