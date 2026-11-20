"""Sprint IV tests: sign-in, authorization and data retrieval for all five roles.

These run against the real database named in src/.env, so first rebuild it with
all five scripts (see src/README.md). Then, from the repository root:

    python -m pytest tests -v

The tests only read data; they never change the database.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from app import create_app  # noqa: E402

PASSWORD = "PetMed123!"

# One sample account per role (from seed.sql)
ADMIN = "daniel.owens@petmed.com"
OWNER = "maya.johnson@petmed.com"
VET = "dr.james.carter@petmed.com"
EXPERT = "kevin.nguyen@petmed.com"
MODERATOR = "tasha.brooks@petmed.com"
SUSPENDED = "sofia.ramirez@petmed.com"

# Each role's Sprint IV feature and the only role allowed to use it
ENDPOINTS = {
    "/api/admin/users": ADMIN,
    "/api/feed": OWNER,
    "/api/vet/questions": VET,
    "/api/expert/topics": EXPERT,
    "/api/moderation/reports": MODERATOR,
}


class PetMedTestCase(unittest.TestCase):
    tokens = {}

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def login(self, email, password=PASSWORD):
        return self.client.post("/api/login", json={"email": email, "password": password})

    def token(self, email):
        if email not in self.tokens:
            res = self.login(email)
            self.assertEqual(res.status_code, 200, res.get_json())
            self.tokens[email] = res.get_json()["token"]
        return self.tokens[email]

    def get(self, url, email=None):
        headers = {"Authorization": f"Bearer {self.token(email)}"} if email else {}
        return self.client.get(url, headers=headers)


class TestSignIn(PetMedTestCase):
    def test_each_role_can_sign_in_and_role_is_identified(self):
        expected = {
            ADMIN: "administrator",
            OWNER: "pet_owner",
            VET: "veterinarian",
            EXPERT: "pet_health_expert",
            MODERATOR: "community_moderator",
        }
        for email, role in expected.items():
            with self.subTest(email=email):
                res = self.login(email)
                self.assertEqual(res.status_code, 200)
                body = res.get_json()
                self.assertTrue(body["token"])
                self.assertEqual(body["role"], role)

    def test_email_is_not_case_sensitive(self):
        self.assertEqual(self.login("Maya.Johnson@PetMed.com").status_code, 200)

    def test_wrong_password_is_rejected(self):
        res = self.login(OWNER, "wrong-password")
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()["message"], "Invalid email or password.")

    def test_unknown_email_gets_the_same_message(self):
        res = self.login("nobody@petmed.com")
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()["message"], "Invalid email or password.")

    def test_empty_form_is_rejected(self):
        self.assertEqual(self.login("", "").status_code, 400)

    def test_suspended_account_cannot_sign_in(self):
        res = self.login(SUSPENDED)
        self.assertEqual(res.status_code, 403)
        self.assertIn("suspended", res.get_json()["message"])

    def test_me_returns_the_signed_in_user(self):
        res = self.get("/api/me", VET)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["name"], "Dr. James Carter")


class TestAuthorization(PetMedTestCase):
    def test_no_token_is_refused(self):
        for url in ENDPOINTS:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 401)

    def test_fake_token_is_refused(self):
        res = self.client.get("/api/admin/users", headers={"Authorization": "Bearer not-a-real-token"})
        self.assertEqual(res.status_code, 401)

    def test_each_feature_is_open_only_to_its_role(self):
        for url, allowed in ENDPOINTS.items():
            for email in ENDPOINTS.values():
                with self.subTest(url=url, user=email):
                    expected = 200 if email == allowed else 403
                    self.assertEqual(self.get(url, email).status_code, expected)


class TestWebsiteAccess(PetMedTestCase):
    def test_website_origin_is_allowed_to_call_the_api(self):
        res = self.client.get("/api/health", headers={"Origin": "http://localhost:5173"})
        self.assertEqual(res.headers.get("Access-Control-Allow-Origin"), "http://localhost:5173")

    def test_other_sites_are_not_allowed(self):
        res = self.client.get("/api/health", headers={"Origin": "http://evil.example"})
        self.assertIsNone(res.headers.get("Access-Control-Allow-Origin"))


class TestSignUp(PetMedTestCase):
    NEW_EMAIL = "test.signup@petmed.com"

    def tearDown(self):
        # Remove the test account so the other tests still see 10 users
        from db import execute, query_one
        with self.app.app_context():
            row = query_one("SELECT user_id FROM User WHERE email = %s", (self.NEW_EMAIL,))
            if row:
                execute("DELETE FROM User_Role WHERE user_id = %s", (row["user_id"],))
                execute("DELETE FROM User WHERE user_id = %s", (row["user_id"],))

    def signup(self, **fields):
        body = {"full_name": "Test Owner", "email": self.NEW_EMAIL, "password": "Pets2026"}
        body.update(fields)
        return self.client.post("/api/signup", json=body)

    def test_new_pet_owner_can_sign_up_and_then_sign_in(self):
        res = self.signup()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()["role"], "pet_owner")
        self.assertEqual(self.login(self.NEW_EMAIL, "Pets2026").status_code, 200)

    def test_email_already_used_is_rejected(self):
        res = self.signup(email=OWNER)
        self.assertEqual(res.status_code, 409)

    def test_weak_password_is_rejected(self):
        self.assertEqual(self.signup(password="short1").status_code, 400)
        self.assertEqual(self.signup(password="nonumbers").status_code, 400)

    def test_missing_name_or_bad_email_is_rejected(self):
        self.assertEqual(self.signup(full_name="").status_code, 400)
        self.assertEqual(self.signup(email="not-an-email").status_code, 400)


class TestRetrieval(PetMedTestCase):
    def test_admin_lists_all_users(self):
        body = self.get("/api/admin/users", ADMIN).get_json()
        self.assertEqual(body["count"], 10)  # 8 + the 2 Sprint V applicants
        self.assertEqual(len(body["roles"]), 5)

    def test_admin_searches_users(self):
        body = self.get("/api/admin/users?q=carter", ADMIN).get_json()
        self.assertEqual([u["full_name"] for u in body["users"]], ["Dr. James Carter"])
        body = self.get("/api/admin/users?role=veterinarian", ADMIN).get_json()
        self.assertEqual(body["count"], 2)
        body = self.get("/api/admin/users?status=suspended", ADMIN).get_json()
        self.assertEqual([u["full_name"] for u in body["users"]], ["Sofia Ramirez"])

    def test_owner_browses_feed_of_published_posts_only(self):
        body = self.get("/api/feed", OWNER).get_json()
        self.assertEqual(body["count"], 8)  # the hidden post is left out
        self.assertNotIn("Kiwi", " ".join(p["body"] for p in body["posts"]))

    def test_owner_searches_and_filters_feed(self):
        body = self.get("/api/feed?q=garlic", OWNER).get_json()
        self.assertEqual(body["count"], 1)
        body = self.get("/api/feed?tag=nutrition", OWNER).get_json()
        self.assertEqual(body["count"], 4)

    def test_vet_views_questions(self):
        self.assertEqual(self.get("/api/vet/questions", VET).get_json()["count"], 6)
        mine = self.get("/api/vet/questions?show=mine", VET).get_json()
        self.assertEqual(mine["count"], 1)
        self.assertIn("drinking a lot more water", mine["questions"][0]["question_text"])
        self.assertEqual(self.get("/api/vet/questions?show=open", VET).get_json()["count"], 2)
        self.assertEqual(self.get("/api/vet/questions?show=unanswered", VET).get_json()["count"], 3)

    def test_expert_sees_only_their_specialty(self):
        body = self.get("/api/expert/topics", EXPERT).get_json()
        self.assertEqual(body["specialty"], "Nutrition")
        self.assertEqual(len(body["questions"]), 2)
        self.assertEqual(len(body["posts"]), 4)

    def test_moderator_views_reported_posts_and_advice(self):
        body = self.get("/api/moderation/reports", MODERATOR).get_json()
        self.assertEqual(body["count"], 2)  # open reports by default
        self.assertEqual(sorted(r["content_type"] for r in body["reports"]), ["advice", "post"])
        body = self.get("/api/moderation/reports?type=post&status=all", MODERATOR).get_json()
        self.assertEqual(body["count"], 2)
        body = self.get("/api/moderation/reports?type=advice", MODERATOR).get_json()
        self.assertEqual(body["count"], 1)


if __name__ == "__main__":
    unittest.main()
