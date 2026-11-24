"""Pet Owner: create a pet profile (My Pets page).

A pet owner needs a pet on file before they can record symptoms, track
medications or ask about a specific pet, so this comes before the Symptom
Tracker in the owner's workflow.

GET  /api/owner/pets/profiles   the owner's pets with age and health counts
POST /api/owner/pets            add a pet
     {"name": "Daisy", "species": "Dog", "breed": "Beagle",
      "birth_date": "2024-05-01", "weight": "22.5"}

(GET /api/owner/pets, the short list used by the Symptom Tracker's drop-down,
is in routes/symptoms.py.)
"""
import datetime

from flask import Blueprint, g, jsonify, request

from auth import PET_OWNER, require_roles
from db import execute, query, query_one
from helpers import clean, log_event, missing, one_of

bp = Blueprint("pets", __name__, url_prefix="/api/owner")

SPECIES = ("Dog", "Cat", "Bird", "Rabbit", "Reptile", "Fish", "Other")
MAX_WEIGHT = 300  # lb; anything heavier is a typo for a household pet


def pet_rows(where, params):
    return query(
        "SELECT p.pet_id, p.name, p.species, p.breed, p.birth_date, p.weight, "
        "(SELECT COUNT(*) FROM Symptom_Log s WHERE s.pet_id = p.pet_id) AS symptoms, "
        "(SELECT COUNT(*) FROM Pet_Allergy a WHERE a.pet_id = p.pet_id) AS allergies, "
        "(SELECT COUNT(*) FROM Pet_Condition c WHERE c.pet_id = p.pet_id) AS conditions "
        "FROM Pet p WHERE " + where + " ORDER BY p.name", params)


@bp.get("/pets/profiles")
@require_roles(PET_OWNER)
def pet_profiles():
    pets = pet_rows("p.owner_user_id = %s", (g.user["user_id"],))
    return jsonify(pets=pets, count=len(pets))


@bp.post("/pets")
@require_roles(PET_OWNER)
def add_pet():
    data = request.get_json(silent=True) or {}

    # 1. Required fields and allowed species
    problem = (missing(data, "name", "species", "breed", "birth_date", "weight")
               or one_of(data, "species", SPECIES))
    if problem:
        return jsonify(message=problem), 400
    name = clean(data, "name", 100)

    # 2. Birth date: a real date, not in the future, and a believable age
    try:
        born = datetime.date.fromisoformat(clean(data, "birth_date"))
    except ValueError:
        return jsonify(message="Enter the birth date as a date, for example 2024-05-01."), 400
    today = datetime.date.today()
    if born > today:
        return jsonify(message="The birth date can't be in the future."), 400
    if born.year < today.year - 50:
        return jsonify(message="Check the birth date: that would make the pet over 50 years old."), 400

    # 3. Weight: a positive number in pounds
    try:
        weight = round(float(clean(data, "weight")), 2)
    except ValueError:
        return jsonify(message="Enter the weight as a number of pounds, for example 22.5."), 400
    if not 0 < weight <= MAX_WEIGHT:
        return jsonify(message=f"The weight must be more than 0 and at most {MAX_WEIGHT} lb."), 400

    # 4. One pet per name per owner, so the pet drop-downs stay clear
    if query_one("SELECT pet_id FROM Pet WHERE owner_user_id = %s AND LOWER(name) = LOWER(%s)",
                 (g.user["user_id"], name)):
        return jsonify(message=f"You already have a pet named {name}."), 409

    # 5. Save it
    pet_id = execute("INSERT INTO Pet (owner_user_id, name, species, breed, birth_date, weight) "
                     "VALUES (%s, %s, %s, %s, %s, %s)",
                     (g.user["user_id"], name, clean(data, "species"), clean(data, "breed", 100),
                      born.isoformat(), weight))
    log_event(g.user["user_id"], "add_pet", "Pet", pet_id)

    return jsonify(message=f"{name} was added to your pets.", pet=pet_rows("p.pet_id = %s", (pet_id,))[0]), 201
