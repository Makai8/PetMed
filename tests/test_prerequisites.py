"""Prerequisites for the Sprint V use cases.

- A pet owner asks a question (Ask for Health Advice) -> the vet or expert can answer it.
- A user reports a post or an answer -> the moderator can review it.
(Adding a pet, the prerequisite for the Symptom Tracker, is in test_owner_pets.py.
The prerequisite for the Administrator use case, applying with credentials, is in
test_sprint5_role_requests.py.)

    python -m pytest tests -k Prereq -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from test_sprint5_use_cases import ANSWER, PRIYA, Sprint5Case  # noqa: E402
from test_sprint4 import EXPERT, MODERATOR, OWNER, VET  # noqa: E402

QUESTION = "Milo has been scratching his ears a lot this week. What could cause that?"


class TestPrereqAskQuestion(Sprint5Case):
    def remove_question(self, qid):
        for rid in [r["response_id"] for r in self.sql("SELECT response_id FROM Advice_Response WHERE question_id = %s",
                                                       (qid,))]:
            self.run_sql("DELETE FROM Audit_Event WHERE entity_name = 'Advice_Response' AND entity_id = %s", (rid,))
        self.run_sql("DELETE FROM Advice_Response WHERE question_id = %s", (qid,))
        self.run_sql("DELETE FROM Health_Question WHERE question_id = %s", (qid,))
        self.run_sql("DELETE FROM Audit_Event WHERE entity_name = 'Health_Question' AND entity_id = %s", (qid,))

    def count(self):
        return self.sql_one("SELECT COUNT(*) AS n FROM Health_Question")["n"]

    def test_lists_only_verified_professionals(self):
        names = [p["full_name"] for p in self.get("/api/owner/professionals", OWNER).get_json()["professionals"]]
        self.assertIn("Dr. James Carter", names)
        self.assertIn("Kevin Nguyen", names)
        self.assertNotIn("Dr. Priya Shah", names)   # still pending verification

    def test_open_question_reaches_vets_and_their_answer_comes_back(self):
        res = self.post("/api/owner/questions", {"question_text": QUESTION, "pet_id": 7380001}, OWNER)
        self.assertEqual(res.status_code, 201, res.get_json())
        qid = res.get_json()["question_id"]
        self.addCleanup(self.remove_question, qid)

        row = self.sql_one("SELECT asker_user_id, pet_id, directed_to_user_id FROM Health_Question WHERE question_id = %s",
                           (qid,))
        self.assertEqual((row["asker_user_id"], row["pet_id"], row["directed_to_user_id"]),
                         (self.user_id(OWNER), 7380001, None))
        vet_list = self.get("/api/vet/questions?show=open", VET).get_json()["questions"]
        self.assertIn(qid, [q["question_id"] for q in vet_list])

        self.assertEqual(self.post(f"/api/vet/questions/{qid}/answer", {"response_text": ANSWER}, VET).status_code, 201)
        mine = [q for q in self.get("/api/owner/questions", OWNER).get_json()["questions"] if q["question_id"] == qid][0]
        self.assertEqual(mine["answer_list"][0]["source_type"], "veterinarian")

    def test_question_sent_to_expert_is_in_their_area(self):
        kevin = self.user_id(EXPERT)
        res = self.post("/api/owner/questions", {"question_text": QUESTION, "directed_to_user_id": kevin}, OWNER)
        self.assertEqual(res.status_code, 201, res.get_json())
        qid = res.get_json()["question_id"]
        self.addCleanup(self.remove_question, qid)
        topics = self.get("/api/expert/topics", EXPERT).get_json()["questions"]
        self.assertIn(qid, [q["question_id"] for q in topics])
        self.assertEqual(self.post(f"/api/expert/questions/{qid}/answer", {"response_text": ANSWER}, EXPERT).status_code,
                         201)

    def test_invalid_questions_are_refused_and_not_saved(self):
        before = self.count()
        for body in ({"question_text": ""},
                     {"question_text": "Help?"},                                   # too short
                     {"question_text": QUESTION, "pet_id": 7380002},               # Marcus's pet
                     {"question_text": QUESTION, "directed_to_user_id": self.user_id(PRIYA)},  # not verified
                     {"question_text": QUESTION, "directed_to_user_id": self.user_id(MODERATOR)}):  # not a professional
            with self.subTest(body=body):
                self.assertEqual(self.post("/api/owner/questions", body, OWNER).status_code, 400)
        self.assertEqual(self.count(), before)

    def test_only_pet_owners_ask(self):
        self.assertEqual(self.post("/api/owner/questions", {"question_text": QUESTION}, VET).status_code, 403)


class TestPrereqReport(Sprint5Case):
    def post_id(self, body_start):
        return self.sql_one("SELECT post_id FROM Post WHERE body LIKE %s", (body_start + "%",))["post_id"]

    def remove_report(self, rid):
        self.run_sql("DELETE FROM Report WHERE report_id = %s", (rid,))
        self.run_sql("DELETE FROM Audit_Event WHERE entity_name = 'Report' AND entity_id = %s", (rid,))

    def count(self):
        return self.sql_one("SELECT COUNT(*) AS n FROM Report")["n"]

    def some_post_not_by(self, email):
        return self.sql_one("SELECT post_id FROM Post WHERE status = 'published' AND author_user_id != %s "
                            "AND post_id NOT IN (SELECT post_id FROM Report WHERE post_id IS NOT NULL) "
                            "ORDER BY post_id LIMIT 1", (self.user_id(email),))["post_id"]

    def test_report_reaches_the_moderator_who_can_decide_it(self):
        pid = self.some_post_not_by(OWNER)
        res = self.post("/api/reports", {"post_id": pid, "reason": "Recommends a human painkiller for dogs."}, OWNER)
        self.assertEqual(res.status_code, 201, res.get_json())
        rid = res.get_json()["report_id"]
        self.addCleanup(self.remove_report, rid)

        row = self.sql_one("SELECT reporter_user_id, post_id, status FROM Report WHERE report_id = %s", (rid,))
        self.assertEqual((row["reporter_user_id"], row["post_id"], row["status"]), (self.user_id(OWNER), pid, "open"))
        reports = self.get("/api/moderation/reports?status=open", MODERATOR).get_json()["reports"]
        self.assertIn(rid, [r["report_id"] for r in reports])

        # The moderator can act on it (this opens a new case)
        res = self.post(f"/api/moderation/reports/{rid}/decision", {"action": "dismiss", "reason": "Checked: fine."},
                        MODERATOR)
        self.assertEqual(res.status_code, 200, res.get_json())
        case_id = res.get_json()["case"]["case_id"]
        self.addCleanup(self.run_sql, "DELETE FROM Moderation_Case WHERE case_id = %s", (case_id,))
        self.addCleanup(self.run_sql, "DELETE FROM Moderation_Action WHERE case_id = %s", (case_id,))
        self.addCleanup(self.run_sql, "DELETE FROM Audit_Event WHERE entity_name = 'Moderation_Case' AND entity_id = %s",
                        (case_id,))

    def test_report_an_answer(self):
        rid_answer = self.sql_one("SELECT response_id FROM Advice_Response ar JOIN User u ON u.user_id = ar.author_user_id "
                                  "WHERE u.email != %s ORDER BY response_id LIMIT 1", (EXPERT,))["response_id"]
        res = self.post("/api/reports", {"response_id": rid_answer, "reason": "This advice looks unsafe."}, EXPERT)
        self.assertEqual(res.status_code, 201, res.get_json())
        self.addCleanup(self.remove_report, res.get_json()["report_id"])

    def test_invalid_reports_are_refused_and_not_saved(self):
        before = self.count()
        pid = self.some_post_not_by(OWNER)
        own = self.sql_one("SELECT post_id FROM Post WHERE author_user_id = %s AND status = 'published' LIMIT 1",
                           (self.user_id(OWNER),))
        cases = [({"post_id": pid, "reason": ""}, 400),                          # no reason
                 ({"reason": "Spam"}, 400),                                      # nothing chosen
                 ({"post_id": pid, "response_id": 1, "reason": "Spam"}, 400),    # two things
                 ({"post_id": 999999, "reason": "Spam"}, 404)]                   # doesn't exist
        if own:
            cases.append(({"post_id": own["post_id"], "reason": "Spam"}, 400))   # own post
        for body, code in cases:
            with self.subTest(body=body):
                self.assertEqual(self.post("/api/reports", body, OWNER).status_code, code)
        self.assertEqual(self.count(), before)

        # The same person can't report the same thing twice while it's open
        res = self.post("/api/reports", {"post_id": pid, "reason": "Unsafe."}, OWNER)
        self.addCleanup(self.remove_report, res.get_json()["report_id"])
        self.assertEqual(self.post("/api/reports", {"post_id": pid, "reason": "Unsafe."}, OWNER).status_code, 409)


if __name__ == "__main__":
    unittest.main()
