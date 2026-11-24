-- PetMed Sprint V: before-and-after queries for the demo video.
-- Run each block in a MySQL prompt (mysql -u root -p petmed) BEFORE the use case,
-- do the use case in the website, then run the same block AFTER to show the change.

USE petmed;

-- 1. Administrator: professional verification (Dr. Priya Shah, Jordan Lee)
SELECT u.full_name, pp.professional_type, pp.verification_status
FROM Professional_Profile pp JOIN User u ON u.user_id = pp.user_id
ORDER BY pp.profile_id;

SELECT vr.review_id, u.full_name AS professional, vr.decision, vr.notes, vr.reviewed_at
FROM Verification_Review vr
JOIN Professional_Profile pp ON pp.profile_id = vr.profile_id
JOIN User u ON u.user_id = pp.user_id
ORDER BY vr.review_id DESC LIMIT 3;

SELECT u.full_name, r.role_name FROM User_Role ur
JOIN User u ON u.user_id = ur.user_id JOIN Role r ON r.role_id = ur.role_id
WHERE u.email = 'dr.priya.shah@petmed.com';

-- 1a. Administrator: account status (run before and after Suspend / Reactivate on Manage Users)
SELECT user_id, full_name, email, account_status FROM User ORDER BY full_name;

-- 2a. Pet Owner: Maya's pets (run before and after adding a pet on My Pets)
SELECT pet_id, name, species, breed, birth_date, weight FROM Pet
WHERE owner_user_id = (SELECT user_id FROM User WHERE email = 'maya.johnson@petmed.com')
ORDER BY pet_id;

-- 2. Pet Owner: symptom log (Maya's pets)
SELECT s.symptom_id, p.name AS pet, s.symptom, s.severity, s.observed_at, s.notes
FROM Symptom_Log s JOIN Pet p ON p.pet_id = s.pet_id
WHERE p.owner_user_id = (SELECT user_id FROM User WHERE email = 'maya.johnson@petmed.com')
ORDER BY s.symptom_id DESC;

-- 3 and 4. Veterinarian and Pet Health Expert: answers to questions
SELECT ar.response_id, LEFT(hq.question_text, 45) AS question, u.full_name AS author,
       ar.source_type, LEFT(ar.response_text, 60) AS answer, ar.created_at
FROM Advice_Response ar
JOIN Health_Question hq ON hq.question_id = ar.question_id
JOIN User u ON u.user_id = ar.author_user_id
ORDER BY ar.response_id DESC LIMIT 5;

-- 5. Community Moderator: reports, their cases and actions
SELECT r.report_id, LEFT(r.reason, 40) AS reason, r.status AS report_status,
       mc.case_id, mc.case_status, mc.closed_at
FROM Report r LEFT JOIN Moderation_Case mc ON mc.report_id = r.report_id
ORDER BY r.report_id;

SELECT ma.action_id, ma.case_id, u.full_name AS moderator, ma.action_type, ma.reason, ma.created_at
FROM Moderation_Action ma JOIN User u ON u.user_id = ma.actor_user_id
ORDER BY ma.action_id DESC LIMIT 3;

SELECT post_id, LEFT(body, 50) AS body, status FROM Post WHERE body LIKE 'A little garlic%';

-- Every Sprint V change is also written to the audit history
SELECT a.audit_id, u.full_name AS who, a.event_type, a.entity_name, a.entity_id, a.occurred_at
FROM Audit_Event a JOIN User u ON u.user_id = a.actor_user_id
ORDER BY a.audit_id DESC LIMIT 6;
