"""Administrator: suspend, reactivate and add user accounts.

    python -m pytest tests -k Accounts -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from test_sprint5_use_cases import Sprint5Case  # noqa: E402
from test_sprint4 import ADMIN, MODERATOR, OWNER  # noqa: E402

MARCUS = "marcus.williams@petmed.com"   # active pet owner
SOFIA = "sofia.ramirez@petmed.com"      # suspended in the sample data
NEW_EMAIL = "jamie.chen@petmed.com"


class TestAdminAccounts(Sprint5Case):
    def setUp(self):
        super().setUp()
        # Only rows newer than this belong to the test (sample data keeps its own)
        self.max_note = self.sql_one("SELECT COALESCE(MAX(notification_id), 0) AS n FROM Notification")["n"]
        self.max_audit = self.sql_one("SELECT COALESCE(MAX(audit_id), 0) AS n FROM Audit_Event")["n"]

    def status(self, email):
        return self.sql_one("SELECT account_status FROM User WHERE email = %s", (email,))["account_status"]

    def restore(self, email, status):
        uid = self.user_id(email)
        self.run_sql("UPDATE User SET account_status = %s WHERE user_id = %s", (status, uid))
        self.run_sql("DELETE FROM Notification WHERE user_id = %s AND notification_id > %s", (uid, self.max_note))
        self.run_sql("DELETE FROM Audit_Event WHERE entity_id = %s AND audit_id > %s", (uid, self.max_audit))

    def test_suspend_then_reactivate(self):
        uid = self.user_id(MARCUS)
        self.addCleanup(self.restore, MARCUS, "active")
        token = self.token(MARCUS)  # Marcus is signed in before the suspension

        res = self.post(f"/api/admin/users/{uid}/status", {"status": "suspended", "reason": "Selling fake medicine."}, ADMIN)
        self.assertEqual(res.status_code, 200, res.get_json())
        self.assertEqual(self.status(MARCUS), "suspended")
        note = self.sql_one("SELECT message FROM Notification WHERE user_id = %s AND notification_id > %s",
                            (uid, self.max_note))
        self.assertIn("Selling fake medicine.", note["message"])

        # Locked out: can't sign in, and the session he already had stops working
        self.assertEqual(self.login(MARCUS).status_code, 403)   # "account suspended"
        self.assertEqual(self.client.get("/api/feed", headers={"Authorization": f"Bearer {token}"}).status_code, 401)

        res = self.post(f"/api/admin/users/{uid}/status", {"status": "active"}, ADMIN)
        self.assertEqual(res.status_code, 200, res.get_json())
        self.assertEqual(self.status(MARCUS), "active")
        self.assertEqual(self.login(MARCUS).status_code, 200)

    def test_reactivate_a_suspended_user(self):
        self.addCleanup(self.restore, SOFIA, "suspended")
        res = self.post(f"/api/admin/users/{self.user_id(SOFIA)}/status", {"status": "active"}, ADMIN)
        self.assertEqual(res.status_code, 200, res.get_json())
        self.assertEqual(self.status(SOFIA), "active")

    def test_invalid_status_changes_change_nothing(self):
        uid = self.user_id(MARCUS)
        cases = [({"status": "suspended"}, 400),                    # no reason
                 ({"status": "banned", "reason": "x"}, 400),         # not a status
                 ({"status": "active"}, 409)]                       # already active
        for body, code in cases:
            with self.subTest(body=body):
                self.assertEqual(self.post(f"/api/admin/users/{uid}/status", body, ADMIN).status_code, code)
        me = self.user_id(ADMIN)
        self.assertEqual(self.post(f"/api/admin/users/{me}/status", {"status": "suspended", "reason": "x"},
                                   ADMIN).status_code, 400)
        self.assertEqual(self.post("/api/admin/users/999999/status", {"status": "suspended", "reason": "x"},
                                   ADMIN).status_code, 404)
        self.assertEqual(self.status(MARCUS), "active")
        self.assertEqual(self.status(ADMIN), "active")

    def test_add_a_user_who_can_sign_in(self):
        before = self.sql_one("SELECT COUNT(*) AS n FROM User")["n"]
        res = self.post("/api/admin/users", {"full_name": "Jamie Chen", "email": NEW_EMAIL, "password": "Welcome2026",
                                             "role": "community_moderator"}, ADMIN)
        self.assertEqual(res.status_code, 201, res.get_json())
        uid = res.get_json()["user"]["user_id"]

        def remove():
            self.run_sql("DELETE FROM User_Role WHERE user_id = %s", (uid,))
            self.run_sql("DELETE FROM Audit_Event WHERE entity_name = 'User' AND entity_id = %s", (uid,))
            self.run_sql("DELETE FROM User WHERE user_id = %s", (uid,))
        self.addCleanup(remove)

        self.assertEqual(self.sql_one("SELECT COUNT(*) AS n FROM User")["n"], before + 1)
        login = self.login(NEW_EMAIL, "Welcome2026")
        self.assertEqual(login.status_code, 200)
        self.assertEqual(login.get_json()["roles"], ["community_moderator"])

    def test_invalid_new_users_are_refused(self):
        before = self.sql_one("SELECT COUNT(*) AS n FROM User")["n"]
        good = {"full_name": "Jamie Chen", "email": NEW_EMAIL, "password": "Welcome2026", "role": "pet_owner"}
        cases = [(dict(good, full_name=""), 400),
                 (dict(good, email="not-an-email"), 400),
                 (dict(good, password="short"), 400),
                 (dict(good, role="veterinarian"), 400),       # vets must apply and be verified
                 (dict(good, role="wizard"), 400),
                 (dict(good, email="maya.johnson@petmed.com"), 409)]
        for body, code in cases:
            with self.subTest(body=body):
                self.assertEqual(self.post("/api/admin/users", body, ADMIN).status_code, code)
        self.assertEqual(self.sql_one("SELECT COUNT(*) AS n FROM User")["n"], before)

    def test_only_administrators(self):
        uid = self.user_id(MARCUS)
        for email in (OWNER, MODERATOR):
            self.assertEqual(self.post(f"/api/admin/users/{uid}/status", {"status": "suspended", "reason": "x"},
                                       email).status_code, 403)
        self.assertEqual(self.status(MARCUS), "active")


if __name__ == "__main__":
    unittest.main()
