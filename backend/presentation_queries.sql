-- PetMed Sprint III presentation: queries to run live
-- Setup (fresh database), from the backend folder:
--   cat PetMedDB.sql | mysql -u root -p
--   cat seed.sql | mysql -u root -p
--   cat sample_data_health_records.sql | mysql -u root -p
--   cat sample_data_more.sql | mysql -u root -p
-- Then open the prompt:  mysql -u root -p petmed   and paste one query at a time.

USE petmed;

-- ===== A. SEARCH: Maya's dogs =====
SELECT p.name, p.breed, p.weight
FROM Pet p JOIN User u ON p.owner_user_id = u.user_id
WHERE u.full_name = 'Maya Johnson' AND p.species = 'Dog';

-- ===== B. RELATED DATA: every symptom with its pet and owner =====
SELECT p.name AS pet, s.symptom, s.severity, u.full_name AS owner
FROM Symptom_Log s
JOIN Pet p  ON s.pet_id = p.pet_id
JOIN User u ON p.owner_user_id = u.user_id
ORDER BY s.observed_at DESC;

-- ===== C. ADD: Marcus adopts Coco =====
INSERT INTO Pet (owner_user_id, name, species, breed, birth_date, weight)
VALUES (87370001, 'Coco', 'Dog', 'Beagle', '2025-05-01', 18.60);
SELECT pet_id, name, breed FROM Pet WHERE owner_user_id = 87370001;

-- ===== D. MODIFY: Bella's new weight =====
UPDATE Pet SET weight = 67.10 WHERE name = 'Bella';
SELECT name, weight FROM Pet WHERE name = 'Bella';

-- ===== USE CASE 1: A pet owner tracks symptoms =====
SELECT symptom, severity, observed_at
FROM Symptom_Log
WHERE pet_id = 7380000          -- Bella
ORDER BY observed_at;

-- ===== USE CASE 2: A vet answers a health question =====
SELECT q.question_text, u.full_name AS answered_by,
       pp.verification_status, a.response_text
FROM Health_Question q
JOIN Advice_Response a       ON a.question_id = q.question_id
JOIN User u                  ON u.user_id = a.author_user_id
JOIN Professional_Profile pp ON pp.user_id = u.user_id
WHERE q.question_id = 1;        -- Marcus asking about Rocky

-- ===== USE CASE 3: A moderator handles a report =====
SELECT r.reason, mod_user.full_name AS moderator, a.action_type, a.created_at
FROM Report r
JOIN Moderation_Case c   ON c.report_id = r.report_id
JOIN Moderation_Action a ON a.case_id = c.case_id
JOIN User mod_user       ON mod_user.user_id = a.actor_user_id
ORDER BY a.created_at;

-- ===== RULES: each one should be REJECTED =====
-- 1. Email must be unique
INSERT INTO User (email, password_hash, full_name, account_status)
VALUES ('maya.johnson@petmed.com', 'x', 'Fake Maya', 'active');
-- 2. A pet must belong to a real user
INSERT INTO Pet (owner_user_id, name, species, breed, birth_date, weight)
VALUES (99999999, 'Ghost', 'Cat', 'Unknown', '2024-01-01', 8.00);
-- 3. A rating must be 1 to 5
INSERT INTO Product_Review (product_id, reviewer_user_id, rating, review_text)
VALUES (1, 87370001, 9, 'Too high');

-- ===== PRACTICE for the instructor's live question =====
-- How many pets does each owner have?
SELECT u.full_name, COUNT(p.pet_id) AS pets
FROM User u JOIN Pet p ON p.owner_user_id = u.user_id
GROUP BY u.full_name;

-- Which professionals can currently see a pet's records?
SELECT p.name AS pet, u.full_name AS professional, d.scope
FROM Data_Share_Authorization d
JOIN Pet p  ON p.pet_id = d.pet_id
JOIN User u ON u.user_id = d.professional_user_id
WHERE d.revoked_at IS NULL;

-- Average rating for each product
SELECT pr.name, AVG(r.rating) AS avg_rating, COUNT(*) AS reviews
FROM Product pr JOIN Product_Review r ON r.product_id = pr.product_id
GROUP BY pr.name;

-- Comments on a post
SELECT u.full_name, c.body
FROM Comment c JOIN User u ON u.user_id = c.author_user_id
WHERE c.post_id = 1;
