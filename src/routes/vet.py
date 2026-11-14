"""Veterinarian use case: view pet-health questions submitted by pet owners."""
from flask import Blueprint, g, jsonify, request

from auth import VETERINARIAN, require_roles
from db import query

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
