"""Pet Owner: create a pet profile (My Pets).

Checks a valid pet is saved and shows up everywhere it should, invalid or
incomplete data is refused without saving anything, and only pet owners can
add pets. Every test removes what it added.

    python -m pytest tests -k Pets -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from test_sprint5_use_cases import Sprint5Case  # noqa: E402
from test_sprint4 import ADMIN, OWNER, VET  # noqa: E402


class TestOwnerAddsPet(Sprint5Case):
    def new_pet(self, **changes):
        body = {"name": "Daisy", "species": "Dog", "breed": "Beagle", "birth_date": "2024-05-01", "weight": "22.5"}
        body.update(changes)
        return body

    def count(self):
        return self.sql_one("SELECT COUNT(*) AS n FROM Pet")["n"]

    def remove(self, pet_id):
        self.run_sql("DELETE FROM Pet WHERE pet_id = %s", (pet_id,))
        self.run_sql("DELETE FROM Audit_Event WHERE entity_name = 'Pet' AND entity_id = %s", (pet_id,))

    def test_lists_the_owners_pets(self):
        res = self.get("/api/owner/pets/profiles", OWNER)
        self.assertEqual(res.status_code, 200)
        names = [p["name"] for p in res.get_json()["pets"]]
        self.assertEqual(names, ["Bella", "Milo"])

    def test_adds_a_pet(self):
        before = self.count()
        res = self.post("/api/owner/pets", self.new_pet(), OWNER)
        self.assertEqual(res.status_code, 201, res.get_json())
        pet = res.get_json()["pet"]
        self.addCleanup(self.remove, pet["pet_id"])

        # Really in the database, owned by Maya
        self.assertEqual(self.count(), before + 1)
        row = self.sql_one("SELECT owner_user_id, name, species, breed, weight FROM Pet WHERE pet_id = %s",
                           (pet["pet_id"],))
        self.assertEqual(row["owner_user_id"], self.user_id(OWNER))
        self.assertEqual((row["name"], row["species"], row["breed"], float(row["weight"])),
                         ("Daisy", "Dog", "Beagle", 22.5))

        # Shows on My Pets and in the Symptom Tracker's pet list, and can get a symptom
        self.assertIn("Daisy", [p["name"] for p in self.get("/api/owner/pets/profiles", OWNER).get_json()["pets"]])
        self.assertIn("Daisy", [p["name"] for p in self.get("/api/owner/pets", OWNER).get_json()["pets"]])
        res = self.post("/api/owner/symptoms", {"pet_id": pet["pet_id"], "symptom": "Itchy ears", "severity": "mild",
                                                 "observed_at": "2026-11-20T09:00"}, OWNER)
        self.assertEqual(res.status_code, 201, res.get_json())
        sid = res.get_json()["symptom"]["symptom_id"]
        self.addCleanup(self.run_sql, "DELETE FROM Audit_Event WHERE entity_name = 'Symptom_Log' AND entity_id = %s",
                        (sid,))
        self.addCleanup(self.run_sql, "DELETE FROM Symptom_Log WHERE symptom_id = %s", (sid,))

    def test_invalid_pets_are_refused_and_not_saved(self):
        before = self.count()
        cases = [
            self.new_pet(name=""),                    # missing name
            self.new_pet(species="Dragon"),           # not a listed species
            self.new_pet(breed=""),                   # missing breed
            self.new_pet(birth_date="last spring"),   # not a date
            self.new_pet(birth_date="2099-01-01"),    # in the future
            self.new_pet(birth_date="1950-01-01"),    # over 50 years old
            self.new_pet(weight="heavy"),             # not a number
            self.new_pet(weight="0"),                 # not positive
            self.new_pet(weight="900"),               # too heavy
        ]
        for body in cases:
            with self.subTest(body=body):
                self.assertEqual(self.post("/api/owner/pets", body, OWNER).status_code, 400)
        self.assertEqual(self.count(), before)

    def test_duplicate_name_is_refused(self):
        res = self.post("/api/owner/pets", self.new_pet(name="bella"), OWNER)
        self.assertEqual(res.status_code, 409)

    def test_only_pet_owners(self):
        for email in (VET, ADMIN):
            self.assertEqual(self.post("/api/owner/pets", self.new_pet(), email).status_code, 403, email)


if __name__ == "__main__":
    unittest.main()
