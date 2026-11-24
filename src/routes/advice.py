"""Pet Owner: ask for health advice.

This is the prerequisite for the Veterinarian and Pet Health Expert use cases:
they answer questions that pet owners ask here.

A question can go to any veterinarian (left open), or to one verified
veterinarian or approved expert. A question sent to an expert is inside that
expert's area, so it shows on their Questions in My Expertise page.

GET  /api/owner/professionals   verified vets and approved experts to send a question to
GET  /api/owner/questions       the owner's questions and the answers they received
POST /api/owner/questions       {"question_text": "...", "pet_id": 7380000 (optional),
                                 "directed_to_user_id": 87370005 (optional)}
"""
from flask import Blueprint, g, jsonify, request

from auth import PET_HEALTH_EXPERT, PET_OWNER, VETERINARIAN, require_roles
from db import execute, query, query_one
from helpers import clean, log_event, missing, now

bp = Blueprint("advice", __name__, url_prefix="/api/owner")

MIN_QUESTION = 15  # characters


def professionals(where="", params=()):
    return query(
        "SELECT u.user_id, u.full_name, pp.professional_type, pp.specialty "
        "FROM Professional_Profile pp JOIN User u ON u.user_id = pp.user_id "
        "WHERE pp.verification_status = 'approved' AND u.account_status = 'active' "
        "AND pp.professional_type IN (%s, %s) " + where +
        " ORDER BY pp.professional_type DESC, u.full_name", (VETERINARIAN, PET_HEALTH_EXPERT) + tuple(params))


@bp.get("/professionals")
@require_roles(PET_OWNER)
def list_professionals():
    return jsonify(professionals=professionals())


@bp.get("/questions")
@require_roles(PET_OWNER)
def my_questions():
    questions = query(
        "SELECT hq.question_id, hq.question_text, hq.created_at, pet.name AS pet_name, "
        "sent_to.full_name AS sent_to "
        "FROM Health_Question hq LEFT JOIN Pet pet ON pet.pet_id = hq.pet_id "
        "LEFT JOIN User sent_to ON sent_to.user_id = hq.directed_to_user_id "
        "WHERE hq.asker_user_id = %s ORDER BY hq.created_at DESC, hq.question_id DESC", (g.user["user_id"],))
    answers = {}
    for r in query("SELECT ar.response_id, ar.question_id, ar.source_type, ar.response_text, ar.created_at, "
                   "u.full_name AS author FROM Advice_Response ar JOIN User u ON u.user_id = ar.author_user_id "
                   "JOIN Health_Question hq ON hq.question_id = ar.question_id WHERE hq.asker_user_id = %s "
                   "ORDER BY ar.created_at, ar.response_id", (g.user["user_id"],)):
        answers.setdefault(r.pop("question_id"), []).append(r)
    for q in questions:
        q["answer_list"] = answers.get(q["question_id"], [])
    return jsonify(questions=questions, count=len(questions))


@bp.post("/questions")
@require_roles(PET_OWNER)
def ask_question():
    data = request.get_json(silent=True) or {}

    # 1. The question itself
    problem = missing(data, "question_text")
    if problem:
        return jsonify(message="Please type your question."), 400
    text = clean(data, "question_text")
    if len(text) < MIN_QUESTION:
        return jsonify(message=f"Describe the problem in at least {MIN_QUESTION} characters."), 400

    # 2. The pet is optional, but must be the owner's own
    pet_id = None
    if clean(data, "pet_id"):
        pet = query_one("SELECT pet_id FROM Pet WHERE pet_id = %s AND owner_user_id = %s",
                        (clean(data, "pet_id"), g.user["user_id"]))
        if pet is None:
            return jsonify(message="Choose one of your own pets."), 400
        pet_id = pet["pet_id"]

    # 3. Sent to one professional (who must be verified) or left open for any vet
    directed_to = None
    if clean(data, "directed_to_user_id"):
        match = professionals("AND u.user_id = %s", (clean(data, "directed_to_user_id"),))
        if not match:
            return jsonify(message="Choose a verified veterinarian or approved expert."), 400
        directed_to = match[0]["user_id"]

    question_id = execute("INSERT INTO Health_Question (asker_user_id, pet_id, directed_to_user_id, question_text, "
                          "created_at) VALUES (%s, %s, %s, %s, %s)",
                          (g.user["user_id"], pet_id, directed_to, text, now()))
    log_event(g.user["user_id"], "ask_question", "Health_Question", question_id)
    who = match[0]["full_name"] if directed_to else "the veterinarians"
    return jsonify(message=f"Your question was sent to {who}.", question_id=question_id), 201
