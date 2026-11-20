"""Small helpers shared by the Sprint V use cases (adding and changing data).

Every use case that saves something follows the same three steps:
1. Read the JSON the website sent:      data = request.get_json(silent=True) or {}
2. Check it. Bad or missing data gets a 400 with a message the page can show:
       problem = missing(data, "symptom", "severity") or one_of(data, "severity", SEVERITIES)
       if problem:
           return jsonify(message=problem), 400
3. Save it with execute(...) from db.py, record it with log_event(...),
   and answer 201 (created) or 200 (changed) with the saved row.
"""
import datetime

from db import execute


def now():
    """The current time in the format MySQL DATETIME columns expect."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clean(data, key, limit=2000):
    """The text in data[key], with extra spaces removed and cut to `limit` characters."""
    return " ".join(str(data.get(key) or "").split())[:limit]


# How a field is named in error messages (anything not listed: "pet_name" -> "pet name")
LABELS = {
    "pet_id": "which pet",
    "observed_at": "when you noticed it",
    "response_text": "your answer",
}


def missing(data, *keys):
    """A message naming the first required field that is empty, or None if all are filled."""
    for key in keys:
        if not clean(data, key):
            return f"Please fill in {LABELS.get(key, key.replace('_', ' '))}."
    return None


def one_of(data, key, allowed):
    """A message if data[key] is not one of the allowed values, otherwise None."""
    if clean(data, key) not in allowed:
        return f"Choose a {key.replace('_', ' ')}: {', '.join(allowed)}."
    return None


def log_event(actor_user_id, event_type, entity_name, entity_id):
    """Add a row to Audit_Event, the history of important actions."""
    execute("INSERT INTO Audit_Event (actor_user_id, event_type, entity_name, entity_id, occurred_at) "
            "VALUES (%s, %s, %s, %s, %s)", (actor_user_id, event_type, entity_name, entity_id, now()))
