USE petmed;

-- 1. SEARCH: all dogs owned by Maya Johnson
SELECT p.name, p.breed, p.weight
FROM Pet p
JOIN User u ON p.owner_user_id = u.user_id
WHERE u.full_name = 'Maya Johnson' AND p.species = 'Dog';

-- 2. SEARCH: all suspended accounts
SELECT user_id, full_name, email
FROM User
WHERE account_status = 'suspended';

-- 3. RELATED DATA (JOIN): symptom logs with pet and owner, newest first
SELECT p.name AS pet, s.symptom, s.severity, s.observed_at, u.full_name AS owner
FROM Symptom_Log s
JOIN Pet p ON s.pet_id = p.pet_id
JOIN User u ON p.owner_user_id = u.user_id
ORDER BY s.observed_at DESC;

-- 4. ADD: Marcus adopts a new pet
INSERT INTO Pet (owner_user_id, name, species, breed, birth_date, weight)
VALUES (87370001, 'Coco', 'Dog', 'Beagle', '2025-05-01', 18.60);

SELECT pet_id, name, breed FROM Pet WHERE owner_user_id = 87370001;

-- 5. MODIFY: Bella gained weight at her checkup
SELECT name, weight FROM Pet WHERE pet_id = 7380000;
UPDATE Pet SET weight = 67.10 WHERE pet_id = 7380000;
SELECT name, weight FROM Pet WHERE pet_id = 7380000;

-- RULE 1 (UNIQUE): a second account with Maya's email is rejected
INSERT INTO User (email, password_hash, full_name, account_status)
VALUES ('maya.johnson@petmed.com', '$2b$10$fake', 'Fake Maya', 'active');

-- RULE 2 (FOREIGN KEY): a pet whose owner does not exist is rejected
INSERT INTO Pet (owner_user_id, name, species, breed, birth_date, weight)
VALUES (99999999, 'Ghost', 'Cat', 'Unknown', '2024-01-01', 8.00);

-- RULE 3 (CHECK): a user cannot follow themselves
INSERT INTO User_Follow (follower_user_id, followed_user_id)
VALUES (87370000, 87370000);
