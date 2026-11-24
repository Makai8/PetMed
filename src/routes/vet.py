"""Veterinarian use cases.

Sprint IV: view pet-health questions submitted by pet owners.
Sprint V:  answer a question with general veterinary guidance
           (POST /api/vet/questions/<question_id>/answer  {"response_text": "..."}).
"""
from flask import Blueprint, g, jsonify, request

from auth import VETERINARIAN, require_roles
from db import execute, query, query_one
from helpers import clean, log_event, now

bp = Blueprint("vet", __name__, url_prefix="/api/vet")

FILTERS = ("all", "mine", "open", "unanswered")


@bp.get("/questions")
@require_roles(VETERINARIAN)
def health_questions():
    show = request.args.get("show", "all")
    if show not in FILTERS:
        show = "all"
    q = request.args.get("q", "").strip()

    sql = ("SELECT hq.question_id, hq.question_text, hq.created_at, hq.directed_to_user_id, "
           "asker.full_name AS asked_by, pet.name AS pet_name, pet.species AS pet_species, "
           "pet.breed AS pet_breed, sent_to.full_name AS sent_to, "
           "(SELECT COUNT(*) FROM Advice_Response ar WHERE ar.question_id = hq.question_id) AS answers "
           "FROM Health_Question hq "
           "JOIN User asker ON asker.user_id = hq.asker_user_id "
           "LEFT JOIN Pet pet ON pet.pet_id = hq.pet_id "
           "LEFT JOIN User sent_to ON sent_to.user_id = hq.directed_to_user_id "
           "WHERE 1 = 1")
    params = []
    if show == "mine":
        sql += " AND hq.directed_to_user_id = %s"
        params.append(g.user["user_id"])
    elif show == "open":
        sql += " AND hq.directed_to_user_id IS NULL"
    elif show == "unanswered":
        sql += " AND NOT EXISTS (SELECT 1 FROM Advice_Response ar WHERE ar.question_id = hq.question_id)"
    if q:
        sql += " AND (hq.question_text LIKE %s OR pet.name LIKE %s OR asker.full_name LIKE %s)"
        params += [f"%{q}%"] * 3
    sql += " ORDER BY hq.created_at DESC, hq.question_id DESC"
    questions = query(sql, params)

    answers = {}
    for r in query("SELECT ar.question_id, ar.source_type, ar.response_text, ar.created_at, "
                   "u.full_name AS author FROM Advice_Response ar "
                   "JOIN User u ON u.user_id = ar.author_user_id ORDER BY ar.created_at"):
        answers.setdefault(r["question_id"], []).append(
            {k: r[k] for k in ("author", "source_type", "response_text", "created_at")})
    for item in questions:
        item["sent_to_me"] = item.pop("directed_to_user_id") == g.user["user_id"]
        item["answer_list"] = answers.get(item["question_id"], [])

    return jsonify(questions=questions, count=len(questions), show=show)


# ------------------------------------------------------------- Sprint V

MIN_ANSWER = 20  # characters; a one-word answer isn't guidance


@bp.post("/questions/<int:question_id>/answer")
@require_roles(VETERINARIAN)

def answer_question(question_id):
    data = request.get_json(silent=True) or {}
    text = clean(data, "response_text")

    if len(text) < MIN_ANSWER:
        return jsonify(
            message=f"Write at least {MIN_ANSWER} characters of guidance."
        ), 400

    user_id = g.user["user_id"]

    profile = query_one(
        "SELECT verification_status FROM Professional_Profile "
        "WHERE user_id = %s AND professional_type = %s",
        (user_id, VETERINARIAN)
    )

    if profile is None or profile["verification_status"] != "approved":
        return jsonify(
            message="Your veterinarian profile is not verified, so you can't answer questions yet."
        ), 403

    question = query_one(
        "SELECT question_id, directed_to_user_id "
        "FROM Health_Question WHERE question_id = %s",
        (question_id,)
    )

    if question is None:
        return jsonify(message="Question not found."), 404

    if question["directed_to_user_id"] not in (None, user_id):
        return jsonify(
            message="This question was sent to another professional."
        ), 403

    existing = query_one(
        "SELECT response_id FROM Advice_Response "
        "WHERE question_id = %s AND author_user_id = %s",
        (question_id, user_id)
    )

    if existing:
        return jsonify(
            message="You already answered this question."
        ), 409

    response_id = execute(
        "INSERT INTO Advice_Response "
        "(question_id, author_user_id, source_type, response_text, created_at) "
        "VALUES (%s, %s, %s, %s, %s)",
        (question_id, user_id, VETERINARIAN, text, now())
    )

    log_event(
        user_id, "answer_question",
        "Advice_Response", response_id
    )

    return jsonify(
        message="Your guidance was posted.",
        response_id=response_id,
        author=g.user["full_name"],
        source_type=VETERINARIAN,
        response_text=text
    ), 201
