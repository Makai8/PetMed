"""Sprint V tests: requesting a role after sign-up, and administrator approval.

Needs the Role_Request table: run backend/sprint5_role_requests.sql after the
other five scripts. Every account these tests create is deleted afterward.

    python -m pytest tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from app import create_app  # noqa: E402
from db import execute, query, query_one  # noqa: E402

ADMIN = "daniel.owens@petmed.com"
OWNER = "maya.johnson@petmed.com"
DEMO_PASSWORD = "PetMed123!"
NEW_PASSWORD = "Pets2026"
NEW_USERS = ("role.test1@petmed.com", "role.test2@petmed.com")


class RoleRequestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            for email in NEW_USERS:
                row = query_one("SELECT user_id FROM User WHERE email = %s", (email,))
                if not row:
                    continue
                uid = row["user_id"]
                for profile in query("SELECT profile_id FROM Professional_Profile WHERE user_id = %s", (uid,)):
                    execute("DELETE FROM Verification_Review WHERE profile_id = %s", (profile["profile_id"],))
                for sql in ("DELETE FROM Professional_Profile WHERE user_id = %s",
                            "DELETE FROM Role_Request WHERE user_id = %s",
                            "DELETE FROM User_Role WHERE user_id = %s",
                            "DELETE FROM User WHERE user_id = %s"):
                    execute(sql, (uid,))

    # helpers
    def signup(self, email):
        res = self.client.post("/api/signup", json={"full_name": "Role Tester", "email": email, "password": NEW_PASSWORD})
        self.assertEqual(res.status_code, 201, res.get_json())
        return res.get_json()["token"]

    def token(self, email, password=DEMO_PASSWORD):
        res = self.client.post("/api/login", json={"email": email, "password": password})
        self.assertEqual(res.status_code, 200, res.get_json())
        return res.get_json()["token"]

    def post(self, url, token, body=None):
        return self.client.post(url, json=body or {}, headers={"Authorization": f"Bearer {token}"})

    def get(self, url, token):
        return self.client.get(url, headers={"Authorization": f"Bearer {token}"})

    # tests
    def test_new_user_requests_moderator_and_admin_approves(self):
        user = self.signup(NEW_USERS[0])
        res = self.post("/api/role-requests", user, {"role": "community_moderator", "reason": "I want to help."})
        self.assertEqual(res.status_code, 201)
        request_id = res.get_json()["request_id"]

        mine = self.get("/api/role-requests/mine", user).get_json()["requests"]
        self.assertEqual([(r["role"], r["status"]) for r in mine], [("community_moderator", "pending")])

        # Still only a pet owner until an administrator approves
        self.assertEqual(self.get("/api/moderation/reports", user).status_code, 403)

        admin = self.token(ADMIN)
        pending = self.get("/api/admin/role-requests", admin).get_json()["requests"]
        self.assertIn(request_id, [r["request_id"] for r in pending])
        self.assertEqual(self.post(f"/api/admin/role-requests/{request_id}/approve", admin).status_code, 200)

        # Signing in again lands on the new, higher role
        res = self.client.post("/api/login", json={"email": NEW_USERS[0], "password": NEW_PASSWORD}).get_json()
        self.assertEqual(res["role"], "community_moderator")
        self.assertIn("pet_owner", res["roles"])
        self.assertEqual(self.get("/api/moderation/reports", res["token"]).status_code, 200)

    def test_vet_request_saves_credentials_and_rejection_is_recorded(self):
        user = self.signup(NEW_USERS[1])
        self.assertEqual(self.post("/api/role-requests", user, {"role": "veterinarian", "reason": "Licensed vet."}).status_code, 400)
        res = self.post("/api/role-requests", user, {
            "role": "veterinarian", "reason": "Licensed vet.", "credentials": "DVM, FL license VM-12345",
            "organization": "Tallahassee Animal Clinic", "experience": "6 years"})
        self.assertEqual(res.status_code, 201)
        request_id = res.get_json()["request_id"]

        admin = self.token(ADMIN)
        row = [r for r in self.get("/api/admin/role-requests", admin).get_json()["requests"] if r["request_id"] == request_id][0]
        self.assertEqual(row["credentials"], "DVM, FL license VM-12345")

        self.assertEqual(self.post(f"/api/admin/role-requests/{request_id}/reject", admin, {"notes": "License not found."}).status_code, 200)
        self.assertEqual(self.post(f"/api/admin/role-requests/{request_id}/approve", admin).status_code, 409)
        mine = self.get("/api/role-requests/mine", user).get_json()["requests"]
        self.assertEqual((mine[0]["status"], mine[0]["review_notes"]), ("rejected", "License not found."))
        login = self.client.post("/api/login", json={"email": NEW_USERS[1], "password": NEW_PASSWORD}).get_json()
        self.assertEqual(login["roles"], ["pet_owner"])

    def test_bad_requests_are_refused(self):
        user = self.signup(NEW_USERS[0])
        self.assertEqual(self.post("/api/role-requests", user, {"role": "pet_owner", "reason": "x"}).status_code, 400)
        self.assertEqual(self.post("/api/role-requests", user, {"role": "administrator"}).status_code, 400)
        self.assertEqual(self.post("/api/role-requests", user, {"role": "administrator", "reason": "Help run it."}).status_code, 201)
        self.assertEqual(self.post("/api/role-requests", user, {"role": "administrator", "reason": "Again."}).status_code, 409)
        owner = self.token(OWNER)
        self.assertEqual(self.post("/api/role-requests", owner, {"role": "pet_owner", "reason": "x"}).status_code, 400)

    def test_only_administrators_review_requests(self):
        owner = self.token(OWNER)
        self.assertEqual(self.get("/api/admin/role-requests", owner).status_code, 403)
        self.assertEqual(self.post("/api/admin/role-requests/1/approve", owner).status_code, 403)
        self.assertEqual(self.client.post("/api/role-requests", json={"role": "administrator", "reason": "x"}).status_code, 401)

    def test_sample_pending_request_is_listed(self):
        admin = self.token(ADMIN)
        names = [(r["full_name"], r["role"]) for r in self.get("/api/admin/role-requests", admin).get_json()["requests"]]
        self.assertIn(("Marcus Williams", "community_moderator"), names)


if __name__ == "__main__":
    unittest.main()
