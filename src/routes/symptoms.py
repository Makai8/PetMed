"""Pet Owner use case (Sprint V): record a symptom or health event for one of their pets.

GET  /api/owner/pets        the signed-in owner's pets (for the pet drop-down)
GET  /api/owner/symptoms    the owner's symptom history, newest first (?pet_id= to filter)
POST /api/owner/symptoms    save a new Symptom_Log row
     {"pet_id": 7380000, "symptom": "Limping", "severity": "mild",
      "observed_at": "2026-11-20T08:30", "notes": "After the park"}
"""
import datetime

from flask import Blueprint, g, jsonify, request

from auth import PET_OWNER, require_roles
from db import execute, query, query_one
from helpers import clean, log_event, missing, one_of

bp = Blueprint("symptoms", __name__, url_prefix="/api/owner")

SEVERITIES = ("mild", "moderate", "severe")


@bp.get("/pets")
@require_roles(PET_OWNER)
def my_pets():
    pets = query("SELECT pet_id, name, species, breed, weight FROM Pet WHERE owner_user_id = %s "
                 "ORDER BY name", (g.user["user_id"],))
    return jsonify(pets=pets)


@bp.get("/symptoms")
@require_roles(PET_OWNER)
def symptom_history():
    sql = ("SELECT s.symptom_id, s.pet_id, p.name AS pet_name, p.species AS pet_species, "
           "s.symptom, s.severity, s.observed_at, s.notes "
           "FROM Symptom_Log s JOIN Pet p ON p.pet_id = s.pet_id WHERE p.owner_user_id = %s")
    params = [g.user["user_id"]]
    pet_id = request.args.get("pet_id", "").strip()
    if pet_id.isdigit():
        sql += " AND s.pet_id = %s"
        params.append(int(pet_id))
    sql += " ORDER BY s.observed_at DESC, s.symptom_id DESC"
    rows = query(sql, params)
    return jsonify(symptoms=rows, count=len(rows))


def parse_time(value):
    """Turn "2026-11-20T08:30" (what a datetime-local input sends) into a datetime, or None."""
    for fmt in ("%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.datetime.strptime(value, fmt)
        except ValueError:
            pass
    return None


@bp.post("/symptoms")
@require_roles(PET_OWNER)
def record_symptom():
    data = request.get_json(silent=True) or {}
    problem = missing(data, "pet_id", "symptom", "severity", "observed_at") or one_of(data, "severity", SEVERITIES)
    if problem:
        return jsonify(message=problem), 400

    pet = query_one("SELECT pet_id, name FROM Pet WHERE pet_id = %s AND owner_user_id = %s",
                    (clean(data, "pet_id"), g.user["user_id"]))
    if pet is None:
        return jsonify(message="Choose one of your own pets."), 400

    observed = parse_time(clean(data, "observed_at"))
    if observed is None:
        return jsonify(message="Enter a valid date and time for when you noticed it."), 400
    if observed > datetime.datetime.now() + datetime.timedelta(minutes=5):
        return jsonify(message="The time you noticed it can't be in the future."), 400

    symptom_id = execute("INSERT INTO Symptom_Log (pet_id, symptom, severity, observed_at, notes) "
                         "VALUES (%s, %s, %s, %s, %s)",
                         (pet["pet_id"], clean(data, "symptom", 255), clean(data, "severity"),
                          observed.strftime("%Y-%m-%d %H:%M:%S"), clean(data, "notes")))
    log_event(g.user["user_id"], "record_symptom", "Symptom_Log", symptom_id)

    saved = query_one("SELECT s.symptom_id, s.pet_id, p.name AS pet_name, p.species AS pet_species, "
                      "s.symptom, s.severity, s.observed_at, s.notes "
                      "FROM Symptom_Log s JOIN Pet p ON p.pet_id = s.pet_id WHERE s.symptom_id = %s",
                      (symptom_id,))
    return jsonify(message=f"Saved for {pet['name']}.", symptom=saved), 201
