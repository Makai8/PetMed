"""Sprint V tests: the five use cases that add or change data.

For each use case these check, as the assignment asks:
  - a normal case with valid data,
  - invalid or incomplete data is refused (and nothing is saved),
  - the data really was added to or changed in the database,
  - only the right role can do it.
The Sprint IV tests in this folder check that the earlier features still work.

Every test puts the database back the way it found it, so you can run them
as often as you like. Run from the repository root, after rebuilding the
database with all seven scripts (see src/README.md):

    python -m pytest tests -v

A use case that is still a starter (its route answers 501 "not built yet")
is reported as SKIPPED instead of failing, so the rest of the team's tests
still run. Once you finish your part, your tests must PASS.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from test_sprint4 import ADMIN, EXPERT, MODERATOR, OWNER, VET, PetMedTestCase  # noqa: E402

from db import execute, query, query_one  # noqa: E402

PRIYA = "dr.priya.shah@petmed.com"      # vet applicant, pending (sprint5_sample_data.sql)
JORDAN = "jordan.lee@petmed.com"        # expert applicant, pending
ANSWER = "Keep a log of how much water she drinks for two days and bring it to a vet visit soon."


class Sprint5Case(PetMedTestCase):
    def post(self, url, body, email):
        return self.client.post(url, json=body, headers={"Authorization": f"Bearer {self.token(email)}"})

    def sql(self, statement, params=()):
        with self.app.app_context():
            return query(statement, params)

    def sql_one(self, statement, params=()):
        with self.app.app_context():
            return query_one(statement, params)

    def run_sql(self, statement, params=()):
        with self.app.app_context():
            return execute(statement, params)

    def skip_if_not_built(self, res):
        if res.status_code == 501:
            self.skipTest(res.get_json().get("message", "Not built yet."))

    def user_id(self, email):
        return self.sql_one("SELECT user_id FROM User WHERE email = %s", (email,))["user_id"]


# ---------------------------------------------------------------- Administrator (Dorien)

class TestAdminVerification(Sprint5Case):
    def profile(self, email):
        return self.sql_one("SELECT pp.profile_id, pp.verification_status FROM Professional_Profile pp "
                            "JOIN User u ON u.user_id = pp.user_id WHERE u.email = %s", (email,))

    def restore(self, email, status, role_name=None):
        p = self.profile(email)
        uid = self.user_id(email)
        self.run_sql("UPDATE Professional_Profile SET verification_status = %s WHERE profile_id = %s",
                     (status, p["profile_id"]))
        self.run_sql("DELETE FROM Verification_Review WHERE profile_id = %s AND reviewed_at >= '2026-11-19'",
                     (p["profile_id"],))
        self.run_sql("DELETE FROM Audit_Event WHERE entity_name = 'Professional_Profile' AND entity_id = %s "
                     "AND event_type LIKE 'verification_%%'", (p["profile_id"],))
        if role_name:
            role_id = self.sql_one("SELECT role_id FROM Role WHERE role_name = %s", (role_name,))["role_id"]
            self.run_sql("DELETE FROM User_Role WHERE user_id = %s AND role_id = %s", (uid, role_id))
            self.run_sql("UPDATE Role_Request SET status = 'pending', reviewed_by_user_id = NULL, reviewed_at = NULL, "
                         "review_notes = NULL WHERE user_id = %s AND role_id = %s", (uid, role_id))

    def test_lists_pending_professionals(self):
        res = self.get("/api/admin/professionals?status=pending", ADMIN)
        self.assertEqual(res.status_code, 200)
        names = [p["full_name"] for p in res.get_json()["professionals"]]
        self.assertIn("Dr. Priya Shah", names)
        self.assertIn("Jordan Lee", names)

    def test_approve_updates_status_and_gives_role(self):
        before = self.profile(PRIYA)
        self.assertEqual(before["verification_status"], "pending")
        self.addCleanup(self.restore, PRIYA, "pending", "veterinarian")

        res = self.post(f"/api/admin/professionals/{before['profile_id']}/status",
                        {"status": "approved", "notes": "License checked with the state board."}, ADMIN)
        self.assertEqual(res.status_code, 200, res.get_json())
        self.assertEqual(res.get_json()["before"], "pending")

        # The database really changed
        self.assertEqual(self.profile(PRIYA)["verification_status"], "approved")
        review = self.sql_one("SELECT decision, notes FROM Verification_Review WHERE profile_id = %s "
                              "ORDER BY review_id DESC LIMIT 1", (before["profile_id"],))
        self.assertEqual(review["decision"], "approved")
        login = self.login(PRIYA).get_json()
        self.assertIn("veterinarian", login["roles"])

    def test_reject_needs_a_note_and_saves_nothing_without_one(self):
        p = self.profile(JORDAN)
        res = self.post(f"/api/admin/professionals/{p['profile_id']}/status", {"status": "rejected"}, ADMIN)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(self.profile(JORDAN)["verification_status"], "pending")

    def test_reject_with_note(self):
        p = self.profile(JORDAN)
        self.addCleanup(self.restore, JORDAN, "pending")
        res = self.post(f"/api/admin/professionals/{p['profile_id']}/status",
                        {"status": "rejected", "notes": "Certificate number could not be found."}, ADMIN)
        self.assertEqual(res.status_code, 200, res.get_json())
        self.assertEqual(self.profile(JORDAN)["verification_status"], "rejected")
        self.assertNotIn("pet_health_expert", self.login(JORDAN).get_json()["roles"])

    def test_bad_status_and_unknown_profile(self):
        p = self.profile(JORDAN)
        self.assertEqual(self.post(f"/api/admin/professionals/{p['profile_id']}/status",
                                   {"status": "maybe"}, ADMIN).status_code, 400)
        self.assertEqual(self.post("/api/admin/professionals/999999/status",
                                   {"status": "approved"}, ADMIN).status_code, 404)

    def test_only_administrators(self):
        p = self.profile(JORDAN)
        for email in (OWNER, VET, EXPERT, MODERATOR):
            res = self.post(f"/api/admin/professionals/{p['profile_id']}/status", {"status": "approved"}, email)
            self.assertEqual(res.status_code, 403, email)
        self.assertEqual(self.profile(JORDAN)["verification_status"], "pending")


# ---------------------------------------------------------------- Pet Owner (David)

class TestOwnerSymptoms(Sprint5Case):
    def new_symptom(self, **changes):
        body = {"pet_id": 7380000, "symptom": "Sneezing after walks", "severity": "mild",
                "observed_at": "2026-11-18T08:30", "notes": "Only in the morning"}
        body.update(changes)
        return body

    def count(self):
        return self.sql_one("SELECT COUNT(*) AS n FROM Symptom_Log")["n"]

    def test_lists_own_pets_and_history(self):
        pets = self.get("/api/owner/pets", OWNER).get_json()["pets"]
        self.assertEqual(sorted(p["name"] for p in pets), ["Bella", "Milo"])
        history = self.get("/api/owner/symptoms", OWNER).get_json()
        self.assertTrue(all(s["pet_name"] in ("Bella", "Milo") for s in history["symptoms"]))

    def test_records_a_symptom(self):
        before = self.count()
        res = self.post("/api/owner/symptoms", self.new_symptom(), OWNER)
        self.skip_if_not_built(res)
        self.assertEqual(res.status_code, 201, res.get_json())
        new_id = res.get_json()["symptom"]["symptom_id"]
        self.addCleanup(self.run_sql, "DELETE FROM Symptom_Log WHERE symptom_id = %s", (new_id,))
        self.addCleanup(self.run_sql, "DELETE FROM Audit_Event WHERE entity_name = 'Symptom_Log' AND entity_id = %s",
                        (new_id,))

        # The new row is in the database and in the owner's history
        self.assertEqual(self.count(), before + 1)
        row = self.sql_one("SELECT pet_id, symptom, severity FROM Symptom_Log WHERE symptom_id = %s", (new_id,))
        self.assertEqual((row["pet_id"], row["symptom"], row["severity"]), (7380000, "Sneezing after walks", "mild"))
        ids = [s["symptom_id"] for s in self.get("/api/owner/symptoms", OWNER).get_json()["symptoms"]]
        self.assertIn(new_id, ids)

    def test_invalid_data_is_refused_and_not_saved(self):
        before = self.count()
        self.skip_if_not_built(self.post("/api/owner/symptoms", {}, OWNER))
        cases = [
            self.new_symptom(symptom=""),                 # missing symptom
            self.new_symptom(severity="terrible"),        # not mild / moderate / severe
            self.new_symptom(observed_at="yesterday"),    # not a date
            self.new_symptom(observed_at="2099-01-01T10:00"),  # in the future
            self.new_symptom(pet_id=7380002),             # Rocky belongs to Marcus, not Maya
        ]
        for body in cases:
            with self.subTest(body=body):
                res = self.post("/api/owner/symptoms", body, OWNER)
                self.skip_if_not_built(res)
                self.assertEqual(res.status_code, 400, res.get_json())
        self.assertEqual(self.count(), before)

    def test_only_pet_owners(self):
        res = self.post("/api/owner/symptoms", self.new_symptom(), VET)
        self.assertEqual(res.status_code, 403)


# ---------------------------------------------------------------- Veterinarian (Makai)

class TestVetAnswers(Sprint5Case):
    def question(self, text_start):
        return self.sql_one("SELECT question_id FROM Health_Question WHERE question_text LIKE %s",
                            (text_start + "%",))["question_id"]

    def answers(self, question_id):
        return self.sql("SELECT author_user_id, source_type, response_text FROM Advice_Response "
                        "WHERE question_id = %s", (question_id,))

    def test_vet_answers_a_question(self):
        qid = self.question("Bella is drinking a lot more water")
        before = len(self.answers(qid))
        res = self.post(f"/api/vet/questions/{qid}/answer", {"response_text": ANSWER}, VET)
        self.skip_if_not_built(res)
        self.assertEqual(res.status_code, 201, res.get_json())
        rid = res.get_json()["response_id"]
        self.addCleanup(self.run_sql, "DELETE FROM Advice_Response WHERE response_id = %s", (rid,))
        self.addCleanup(self.run_sql, "DELETE FROM Audit_Event WHERE entity_name = 'Advice_Response' "
                                      "AND entity_id = %s", (rid,))

        rows = self.answers(qid)
        self.assertEqual(len(rows), before + 1)
        mine = [r for r in rows if r["author_user_id"] == self.user_id(VET)]
        self.assertEqual(mine[0]["source_type"], "veterinarian")

        # It shows on the questions page, and the same vet can't answer twice
        listed = self.get("/api/vet/questions?show=mine", VET).get_json()["questions"]
        self.assertTrue(any(a["response_text"] == ANSWER for q in listed for a in q["answer_list"]))
        self.assertEqual(self.post(f"/api/vet/questions/{qid}/answer", {"response_text": ANSWER}, VET).status_code,
                         409)

    def test_invalid_answers_are_refused(self):
        qid = self.question("Bella is drinking a lot more water")
        before = len(self.answers(qid))
        for body, code in (({"response_text": ""}, 400), ({"response_text": "Go to a vet."}, 400)):
            res = self.post(f"/api/vet/questions/{qid}/answer", body, VET)
            self.skip_if_not_built(res)
            self.assertEqual(res.status_code, code)
        res = self.post("/api/vet/questions/999999/answer", {"response_text": ANSWER}, VET)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(len(self.answers(qid)), before)

    def test_question_sent_to_someone_else(self):
        # The treats question was sent to Kevin (expert), not to a vet
        qid = self.question("How many treats a day")
        res = self.post(f"/api/vet/questions/{qid}/answer", {"response_text": ANSWER}, VET)
        self.skip_if_not_built(res)
        self.assertEqual(res.status_code, 403)

    def test_only_veterinarians(self):
        qid = self.question("Bella is drinking a lot more water")
        self.assertEqual(self.post(f"/api/vet/questions/{qid}/answer", {"response_text": ANSWER}, OWNER).status_code,
                         403)


# ---------------------------------------------------------------- Pet Health Expert (Miles)

class TestExpertAnswers(Sprint5Case):
    def question(self, text_start):
        return self.sql_one("SELECT question_id FROM Health_Question WHERE question_text LIKE %s",
                            (text_start + "%",))["question_id"]

    def test_expert_answers_inside_their_area(self):
        qid = self.question("How many treats a day")   # sent to Kevin, Nutrition
        text = "Treats should be under 10 percent of daily calories, so about 3 small biscuits for Bella."
        res = self.post(f"/api/expert/questions/{qid}/answer", {"response_text": text}, EXPERT)
        self.skip_if_not_built(res)
        self.assertEqual(res.status_code, 201, res.get_json())
        rid = res.get_json()["response_id"]
        self.addCleanup(self.run_sql, "DELETE FROM Advice_Response WHERE response_id = %s", (rid,))
        self.addCleanup(self.run_sql, "DELETE FROM Audit_Event WHERE entity_name = 'Advice_Response' "
                                      "AND entity_id = %s", (rid,))

        row = self.sql_one("SELECT question_id, author_user_id, source_type, response_text FROM Advice_Response "
                           "WHERE response_id = %s", (rid,))
        self.assertEqual(row["question_id"], qid)
        self.assertEqual(row["author_user_id"], self.user_id(EXPERT))
        self.assertEqual(row["source_type"], "pet_health_expert")
        topics = self.get("/api/expert/topics", EXPERT).get_json()
        answered = [q for q in topics["questions"] if q["question_id"] == qid][0]
        self.assertEqual(answered["answers"], 1)

    def test_outside_area_is_refused(self):
        qid = self.question("Luna breathes heavily")   # open question, not sent to Kevin
        res = self.post(f"/api/expert/questions/{qid}/answer", {"response_text": ANSWER}, EXPERT)
        self.skip_if_not_built(res)
        self.assertEqual(res.status_code, 403)

    def test_invalid_answers_are_refused(self):
        qid = self.question("How many treats a day")
        before = self.sql_one("SELECT COUNT(*) AS n FROM Advice_Response WHERE question_id = %s", (qid,))["n"]
        res = self.post(f"/api/expert/questions/{qid}/answer", {"response_text": "Fewer."}, EXPERT)
        self.skip_if_not_built(res)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(self.post("/api/expert/questions/999999/answer", {"response_text": ANSWER},
                                   EXPERT).status_code, 404)
        after = self.sql_one("SELECT COUNT(*) AS n FROM Advice_Response WHERE question_id = %s", (qid,))["n"]
        self.assertEqual(after, before)

    def test_unapproved_expert_is_locked_out(self):
        uid = self.user_id(EXPERT)
        self.run_sql("UPDATE Professional_Profile SET verification_status = 'suspended' WHERE user_id = %s", (uid,))
        self.addCleanup(self.run_sql, "UPDATE Professional_Profile SET verification_status = 'approved' "
                                      "WHERE user_id = %s", (uid,))
        qid = self.question("How many treats a day")
        res = self.post(f"/api/expert/questions/{qid}/answer", {"response_text": ANSWER}, EXPERT)
        self.skip_if_not_built(res)
        self.assertEqual(res.status_code, 403)

    def test_only_experts(self):
        qid = self.question("How many treats a day")
        self.assertEqual(self.post(f"/api/expert/questions/{qid}/answer", {"response_text": ANSWER},
                                   MODERATOR).status_code, 403)


# ---------------------------------------------------------------- Community Moderator (Makel)

class TestModeratorDecisions(Sprint5Case):
    def report(self, reason_start):
        return self.sql_one("SELECT r.report_id, r.status, r.post_id, r.response_id, mc.case_id, mc.case_status, "
                            "mc.assigned_moderator_id, mc.closed_at FROM Report r "
                            "LEFT JOIN Moderation_Case mc ON mc.report_id = r.report_id WHERE r.reason LIKE %s",
                            (reason_start + "%",))

    def restore(self, before):
        self.run_sql("UPDATE Report SET status = %s WHERE report_id = %s", (before["status"], before["report_id"]))
        self.run_sql("UPDATE Moderation_Case SET case_status = %s, assigned_moderator_id = %s, closed_at = %s "
                     "WHERE case_id = %s", (before["case_status"], before["assigned_moderator_id"],
                                            before["closed_at"], before["case_id"]))
        self.run_sql("DELETE FROM Moderation_Action WHERE case_id = %s AND created_at >= '2026-11-19'",
                     (before["case_id"],))
        self.run_sql("DELETE FROM Audit_Event WHERE entity_name = 'Moderation_Case' AND entity_id = %s "
                     "AND event_type LIKE 'moderation_%%'", (before["case_id"],))

    def test_remove_unsafe_post_closes_the_case(self):
        before = self.report("Garlic is toxic")
        self.assertEqual(before["status"], "open")
        self.addCleanup(self.restore, before)
        self.addCleanup(self.run_sql, "UPDATE Post SET status = 'published' WHERE post_id = %s", (before["post_id"],))

        res = self.post(f"/api/moderation/reports/{before['report_id']}/decision",
                        {"action": "remove_content", "reason": "Garlic is toxic to dogs."}, MODERATOR)
        self.skip_if_not_built(res)
        self.assertEqual(res.status_code, 200, res.get_json())

        after = self.report("Garlic is toxic")
        self.assertEqual(after["status"], "resolved")
        self.assertEqual(after["case_status"], "closed")
        self.assertIsNotNone(after["closed_at"])
        post = self.sql_one("SELECT status FROM Post WHERE post_id = %s", (before["post_id"],))
        self.assertEqual(post["status"], "removed")
        action = self.sql_one("SELECT action_type, actor_user_id FROM Moderation_Action WHERE case_id = %s "
                              "ORDER BY action_id DESC LIMIT 1", (before["case_id"],))
        self.assertEqual(action["action_type"], "remove_content")
        self.assertEqual(action["actor_user_id"], self.user_id(MODERATOR))
        # The removed post is gone from the Pet Owner's feed
        feed = self.get("/api/feed?q=garlic", OWNER).get_json()
        self.assertEqual(feed["count"], 0)

    def test_escalate_keeps_the_report_open(self):
        before = self.report("Cooked bones splinter")
        self.addCleanup(self.restore, before)
        res = self.post(f"/api/moderation/reports/{before['report_id']}/decision",
                        {"action": "escalate", "reason": "Needs an administrator to review the author."}, MODERATOR)
        self.skip_if_not_built(res)
        self.assertEqual(res.status_code, 200, res.get_json())
        after = self.report("Cooked bones splinter")
        self.assertEqual(after["status"], "open")
        self.assertEqual(after["case_status"], "escalated")
        self.assertEqual(after["assigned_moderator_id"], self.user_id(MODERATOR))

    def test_invalid_decisions_change_nothing(self):
        before = self.report("Garlic is toxic")
        self.skip_if_not_built(self.post(f"/api/moderation/reports/{before['report_id']}/decision", {}, MODERATOR))
        for body in ({"action": "delete_everything", "reason": "x"}, {"action": "dismiss", "reason": ""}, {}):
            with self.subTest(body=body):
                res = self.post(f"/api/moderation/reports/{before['report_id']}/decision", body, MODERATOR)
                self.skip_if_not_built(res)
                self.assertEqual(res.status_code, 400)
        self.assertEqual(self.report("Garlic is toxic"), before)
        resolved = self.report("Posted by a suspended account")
        res = self.post(f"/api/moderation/reports/{resolved['report_id']}/decision",
                        {"action": "dismiss", "reason": "Already handled."}, MODERATOR)
        self.assertEqual(res.status_code, 409)

    def test_only_moderators(self):
        before = self.report("Garlic is toxic")
        res = self.post(f"/api/moderation/reports/{before['report_id']}/decision",
                        {"action": "dismiss", "reason": "Not a problem."}, OWNER)
        self.assertEqual(res.status_code, 403)


if __name__ == "__main__":
    unittest.main()
