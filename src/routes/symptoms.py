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
    # ===================== DAVID: build this (Sprint V) =====================
    # Save a new Symptom_Log row for one of the signed-in owner's pets.
    # Worked example to copy from: update_status() in routes/verification.py
    # Done when: python -m pytest tests -k Symptoms   passes (no skips).
    #
    # 1. data = request.get_json(silent=True) or {}
    # 2. Required fields: pet_id, symptom, severity, observed_at.
    #    problem = missing(data, ...) or one_of(data, "severity", SEVERITIES)
    #    If there's a problem: return jsonify(message=problem), 400
    # 3. The pet must belong to this owner:
    #    pet = query_one("SELECT pet_id, name FROM Pet WHERE pet_id = %s AND owner_user_id = %s",
    #                    (clean(data, "pet_id"), g.user["user_id"]))
    #    No pet -> 400 "Choose one of your own pets."
    # 4. observed = parse_time(clean(data, "observed_at"))
    #    None -> 400.  Later than datetime.datetime.now() (allow 5 minutes) -> 400 "can't be in the future".
    # 5. symptom_id = execute("INSERT INTO Symptom_Log (pet_id, symptom, severity, observed_at, notes) "
    #                         "VALUES (%s, %s, %s, %s, %s)", (...))
    #    Use clean(data, "symptom", 255), clean(data, "notes") and observed.strftime("%Y-%m-%d %H:%M:%S").
    # 6. log_event(g.user["user_id"], "record_symptom", "Symptom_Log", symptom_id)
    # 7. Read the saved row back (join Pet for pet_name) and
    #    return jsonify(message=f"Saved for {pet['name']}.", symptom=saved), 201
    # Then delete the line below.
    return jsonify(message="Not built yet: David is building Record a Symptom (Sprint V)."), 501
