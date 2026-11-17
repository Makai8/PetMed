"""Role home screens: GET /api/home?role= returns each role's own numbers."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from app import create_app  # noqa: E402

ACCOUNTS = {
    "administrator": "daniel.owens@petmed.com",
    "pet_owner": "maya.johnson@petmed.com",
    "veterinarian": "dr.james.carter@petmed.com",
    "pet_health_expert": "kevin.nguyen@petmed.com",
    "community_moderator": "tasha.brooks@petmed.com",
}


class RoleHomeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = create_app().test_client()
        cls.tokens = {}
        for role, email in ACCOUNTS.items():
            res = cls.client.post("/api/login", json={"email": email, "password": "PetMed123!"})
            cls.tokens[role] = res.get_json()["token"]

    def home(self, role, as_role=None):
        token = self.tokens[as_role or role]
        return self.client.get(f"/api/home?role={role}", headers={"Authorization": f"Bearer {token}"})

    def stats(self, role):
        body = self.home(role).get_json()
        return {s["label"]: s["value"] for s in body["stats"]}, body

    def test_each_role_gets_its_own_home(self):
        for role in ACCOUNTS:
            with self.subTest(role=role):
                res = self.home(role)
                self.assertEqual(res.status_code, 200)
                self.assertEqual(res.get_json()["role"], role)
                self.assertEqual(len(res.get_json()["stats"]), 4)

    def test_a_role_you_do_not_have_is_refused(self):
        self.assertEqual(self.home("administrator", as_role="pet_owner").status_code, 403)
        self.assertEqual(self.client.get("/api/home?role=pet_owner").status_code, 401)

    def test_pet_owner_sees_own_pets(self):
        stats, body = self.stats("pet_owner")
        self.assertEqual(stats["My pets"], 2)
        self.assertEqual(sorted(p["name"] for p in body["pets"]), ["Bella", "Milo"])

    def test_vet_counts(self):
        stats, _ = self.stats("veterinarian")
        self.assertEqual((stats["Sent to me"], stats["Open to any vet"], stats["Unanswered"]), (1, 2, 3))

    def test_expert_specialty(self):
        stats, body = self.stats("pet_health_expert")
        self.assertEqual(body["profile"]["specialty"], "Nutrition")
        self.assertEqual(stats["Posts tagged #nutrition"], 4)

    def test_moderator_and_admin_counts(self):
        stats, _ = self.stats("community_moderator")
        self.assertEqual(stats["Suspended users"], 1)
        stats, body = self.stats("administrator")
        self.assertEqual(stats["Total users"], 8)
        self.assertEqual(len(body["newest_users"]), 4)


if __name__ == "__main__":
    unittest.main()
