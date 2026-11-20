-- PetMed Sprint V sample data: two professionals waiting for verification.
-- Run AFTER the other six scripts (the last one is sprint5_role_requests.sql):
--   cat sprint5_sample_data.sql | mysql -u root -p
--
-- DEMO ONLY: both accounts use the password  PetMed123!  (stored as a hash).
-- They signed up as pet owners and asked to become professionals, so their
-- Professional_Profile is 'pending' until an administrator reviews it on the
-- Professional Verification page.

USE petmed;

INSERT INTO User (email, password_hash, full_name, account_status, created_at) VALUES
('dr.priya.shah@petmed.com',
 'pbkdf2:sha256:600000$086s4Sz2uvQpvmJM$f8d1d75ac051469930dc55079752869333e226181761ed39c071fb7fca3dab57',
 'Dr. Priya Shah', 'active', '2026-11-18 10:00:00'),
('jordan.lee@petmed.com',
 'pbkdf2:sha256:600000$aU8FKyaHhmyxTwVx$0b4a1ccc24a17ab5ef8ad60b5ed14cadab44fa2793e1f4969ddc4db05458646f',
 'Jordan Lee', 'active', '2026-11-18 14:30:00');

-- Both start as pet owners (every new account does)
INSERT INTO User_Role (user_id, role_id) VALUES
((SELECT user_id FROM User WHERE email = 'dr.priya.shah@petmed.com'), (SELECT role_id FROM Role WHERE role_name = 'pet_owner')),
((SELECT user_id FROM User WHERE email = 'jordan.lee@petmed.com'),    (SELECT role_id FROM Role WHERE role_name = 'pet_owner'));

-- Their professional details, waiting for review
INSERT INTO Professional_Profile (user_id, professional_type, credentials, specialty, organization, experience, verification_status) VALUES
((SELECT user_id FROM User WHERE email = 'dr.priya.shah@petmed.com'), 'veterinarian',
 'DVM, Florida veterinary license VM-48213', 'Emergency and critical care', 'Northside Animal ER',
 '5 years in emergency practice', 'pending'),
((SELECT user_id FROM User WHERE email = 'jordan.lee@petmed.com'), 'pet_health_expert',
 'Certified Applied Animal Behaviorist (CAAB)', 'Behavior', 'Calm Companions Training',
 '9 years helping owners with anxious and reactive pets', 'pending');

-- The matching role requests (shown on the Role Requests page too)
INSERT INTO Role_Request (user_id, role_id, reason, status, requested_at) VALUES
((SELECT user_id FROM User WHERE email = 'dr.priya.shah@petmed.com'), (SELECT role_id FROM Role WHERE role_name = 'veterinarian'),
 'I am a licensed emergency vet and would like to answer urgent questions.', 'pending', '2026-11-18 10:05:00'),
((SELECT user_id FROM User WHERE email = 'jordan.lee@petmed.com'), (SELECT role_id FROM Role WHERE role_name = 'pet_health_expert'),
 'I help owners with pet behavior problems and want to share that here.', 'pending', '2026-11-18 14:35:00');
