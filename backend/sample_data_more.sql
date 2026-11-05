-- PetMed Sprint Cycle III: more sample data
-- Fills the 30 tables that seed.sql and sample_data_health_records.sql leave empty,
-- using the same people and pets. Run AFTER both of those files, on a fresh database:
--   cat PetMedDB.sql | mysql -u root -p
--   cat seed.sql | mysql -u root -p
--   cat sample_data_health_records.sql | mysql -u root -p
--   cat sample_data_more.sql | mysql -u root -p
--
-- People from seed.sql:
--   87370000 Maya Johnson (pet owner)        87370004 Dr. Aisha Bello (veterinarian)
--   87370001 Marcus Williams (pet owner)     87370005 Kevin Nguyen (pet health expert)
--   87370002 Sofia Ramirez (owner, suspended) 87370006 Tasha Brooks (moderator)
--   87370003 Dr. James Carter (veterinarian) 87370007 Daniel Owens (administrator)
-- Pets: 7380000 Bella, 7380001 Milo (Maya) · 7380002 Rocky, 7380003 Luna (Marcus)
--       7380004 Simba, 7380005 Kiwi (Sofia)

USE petmed;

-- ============ ACCOUNTS & ACCESS ============

-- What each role is allowed to do
INSERT INTO Permission (permission_code) VALUES
('manage_own_pets'),        -- 1
('ask_health_questions'),   -- 2
('answer_health_questions'),-- 3
('view_shared_pet_records'),-- 4
('moderate_content'),       -- 5
('verify_professionals'),   -- 6
('manage_system_settings'); -- 7

INSERT INTO Role_Permission (role_id, permission_id) VALUES
(1, 1), (1, 2),                 -- pet owner
(2, 3), (2, 4),                 -- veterinarian
(3, 3),                         -- pet health expert
(4, 5),                         -- community moderator
(5, 5), (5, 6), (5, 7);         -- administrator

-- The two vets and the expert have professional profiles
INSERT INTO Professional_Profile (user_id, professional_type, credentials, specialty, organization, experience, verification_status) VALUES
(87370003, 'veterinarian',      'DVM, Florida licensed veterinarian',     'Senior dog care',   'Tallahassee Animal Clinic', '12 years in small-animal practice',          'approved'),
(87370004, 'veterinarian',      'DVM, Florida licensed veterinarian',     'Internal medicine', 'Capital City Pet Hospital', '8 years treating digestive and kidney issues', 'approved'),
(87370005, 'pet_health_expert', 'Certified pet nutrition specialist',     'Nutrition',         'Healthy Paws Nutrition',    '6 years advising on pet diets',                'approved');

-- Daniel (administrator) reviewed and approved each one
INSERT INTO Verification_Review (profile_id, admin_user_id, decision, reviewed_at, notes) VALUES
((SELECT profile_id FROM Professional_Profile WHERE user_id = 87370003), 87370007, 'approved', '2026-10-01 09:00:00', 'License number confirmed with the state board.'),
((SELECT profile_id FROM Professional_Profile WHERE user_id = 87370004), 87370007, 'approved', '2026-10-01 09:20:00', 'License number confirmed with the state board.'),
((SELECT profile_id FROM Professional_Profile WHERE user_id = 87370005), 87370007, 'approved', '2026-10-02 14:00:00', 'Nutrition certificate verified.');

-- Messages between users (Sofia's spam leads to the report below)
INSERT INTO Message (sender_user_id, recipient_user_id, body, sent_at) VALUES
(87370002, 87370000, 'Buy my miracle pills! They cure every pet illness in one day. Message me to order.', '2026-10-27 18:00:00'),
(87370003, 87370000, 'Hi Maya, how is Bella doing on the shorter walks?', '2026-10-29 10:15:00'),
(87370000, 87370003, 'Much better, thank you! She seems happier.', '2026-10-29 12:40:00');

-- Notifications
INSERT INTO Notification (user_id, type, message, is_read, created_at) VALUES
(87370000, 'comment',  'Dr. James Carter replied to your post about Bella.', TRUE,  '2026-10-21 09:05:00'),
(87370001, 'advice',   'Dr. Aisha Bello answered your question about Rocky.', FALSE, '2026-10-25 11:30:00'),
(87370000, 'reminder', 'Time for Bella''s allergy medicine.', FALSE, '2026-11-05 08:00:00'),
(87370002, 'account',  'Your account has been suspended for 30 days for sending spam.', FALSE, '2026-10-28 16:00:00');

-- ============ PET HEALTH ============

-- Treatments recommended by the vets
INSERT INTO Treatment (pet_id, professional_user_id, description, start_date, end_date) VALUES
(7380002, 87370004, 'Bland diet of boiled chicken and rice, plus extra water, while appetite returns.', '2026-10-25', '2026-11-08'),
(7380000, 87370003, 'Joint supplement and shorter, more frequent walks for hip stiffness.',            '2026-10-21', '2026-12-21');

-- Reminders, one linked to Bella's allergy medicine
INSERT INTO Reminder (pet_id, user_id, pet_medication_id, due_at, status) VALUES
(7380000, 87370000, (SELECT pet_medication_id FROM Pet_Medication WHERE pet_id = 7380000 AND name = 'Cetirizine'), '2026-11-05 08:00:00', 'scheduled'),
(7380002, 87370001, NULL, '2026-11-10 09:30:00', 'scheduled'),
(7380001, 87370000, NULL, '2026-10-30 17:00:00', 'completed');

-- Owners letting a vet see their pet's records (one active, one revoked)
INSERT INTO Data_Share_Authorization (pet_id, owner_user_id, professional_user_id, scope, granted_at, expires_at, revoked_at) VALUES
(7380002, 87370001, 87370004, 'symptoms and medications', '2026-10-25 10:00:00', '2026-12-25 10:00:00', NULL),
(7380001, 87370000, 87370003, 'symptoms only',            '2026-10-22 13:00:00', NULL, '2026-10-30 09:00:00');

-- Dr. Bello asks Marcus to bring Rocky in
INSERT INTO Vet_Referral (pet_id, vet_user_id, reason, urgency, created_at) VALUES
(7380002, 87370004, 'Rocky has stopped eating and has low energy. Please schedule an in-person exam.', 'urgent', '2026-10-25 11:35:00');

-- ============ COMMUNITY & ADVICE ============

INSERT INTO Tag (tag_name) VALUES
('senior-dogs'), ('training'), ('toxic-foods'), ('nutrition'), ('birds'), ('cats');

-- Tag the existing posts (post IDs 1 to 4 from seed.sql)
INSERT INTO Post_Tag (post_id, tag_id) VALUES
(1, (SELECT tag_id FROM Tag WHERE tag_name = 'senior-dogs')),
(2, (SELECT tag_id FROM Tag WHERE tag_name = 'training')),
(3, (SELECT tag_id FROM Tag WHERE tag_name = 'toxic-foods')),
(3, (SELECT tag_id FROM Tag WHERE tag_name = 'nutrition')),
(4, (SELECT tag_id FROM Tag WHERE tag_name = 'birds'));

INSERT INTO Post_Like (user_id, post_id) VALUES
(87370001, 1), (87370005, 1), (87370003, 1), (87370000, 2), (87370001, 3), (87370000, 3);

INSERT INTO Post_Save (user_id, post_id) VALUES
(87370000, 3), (87370001, 1);

INSERT INTO Post_Share (post_id, user_id) VALUES
(3, 87370000), (3, 87370001);

INSERT INTO User_Follow (follower_user_id, followed_user_id) VALUES
(87370000, 87370003),   -- Maya follows Dr. Carter
(87370001, 87370004),   -- Marcus follows Dr. Bello
(87370000, 87370005),   -- Maya follows Kevin
(87370001, 87370000);   -- Marcus follows Maya

-- Articles from the verified professionals
INSERT INTO Health_Article (author_user_id, title, content, status, published_at) VALUES
(87370003, 'Caring for Your Senior Dog', 'As dogs age they need shorter walks, softer beds, and regular checkups. Watch for stiffness, weight changes, and drinking more water than usual.', 'published', '2026-10-15 08:00:00'),
(87370005, 'How to Switch Your Pet''s Food Safely', 'Mix a little of the new food into the old food and increase it slowly over about a week to avoid an upset stomach.', 'published', '2026-10-18 08:00:00');

INSERT INTO Article_Tag (article_id, tag_id) VALUES
((SELECT article_id FROM Health_Article WHERE title = 'Caring for Your Senior Dog'),            (SELECT tag_id FROM Tag WHERE tag_name = 'senior-dogs')),
((SELECT article_id FROM Health_Article WHERE title = 'How to Switch Your Pet''s Food Safely'), (SELECT tag_id FROM Tag WHERE tag_name = 'nutrition')),
((SELECT article_id FROM Health_Article WHERE title = 'How to Switch Your Pet''s Food Safely'), (SELECT tag_id FROM Tag WHERE tag_name = 'cats'));

-- Answers to the two questions in seed.sql (question 1: Rocky, question 2: Milo)
INSERT INTO Advice_Response (question_id, author_user_id, source_type, response_text, created_at) VALUES
(1, 87370004, 'veterinarian',      'Two skipped meals plus low energy is worth a visit. I have sent you a referral. Keep water available until then.', '2026-10-25 11:30:00'),
(2, 87370005, 'pet_health_expert', 'Switch over about 7 days: start with one quarter new food and increase a little each day.', '2026-10-23 16:00:00'),
(2, 87370001, 'community',         'That slow switch worked for my dogs too.', '2026-10-24 09:10:00');

-- Owners rate the answers they got
INSERT INTO Advice_Review (response_id, reviewer_user_id, rating, feedback) VALUES
((SELECT response_id FROM Advice_Response WHERE question_id = 1 AND author_user_id = 87370004), 87370001, 5, 'Clear and fast. Rocky is eating again after the visit.'),
((SELECT response_id FROM Advice_Response WHERE question_id = 2 AND author_user_id = 87370005), 87370000, 4, 'Helpful, Milo did well with the slow switch.');

-- ============ CATALOG & REFERENCE ============

-- Reference information for the medicines in sample_data_health_records.sql
INSERT INTO Medication_Reference (medication_code, name, uses, dosage_guidance, warnings, side_effects, source, last_reviewed_at) VALUES
('MED-CET', 'Cetirizine', 'Relief of itching from allergies.',                       'Dose is set by a veterinarian based on weight.', 'Only give with veterinarian approval.',                  'Mild sleepiness.',            'Demonstration entry, not medical advice', '2026-10-01 00:00:00'),
('MED-CAR', 'Carprofen',  'Pain and swelling from joint problems.',                  'Dose is set by a veterinarian based on weight.', 'Not for cats. Do not combine with other pain relievers.', 'Upset stomach, low appetite.', 'Demonstration entry, not medical advice', '2026-10-01 00:00:00'),
('MED-APO', 'Apoquel',    'Itching from allergic skin conditions in dogs.',          'Dose is set by a veterinarian based on weight.', 'Only for dogs over 12 months old.',                      'Upset stomach.',              'Demonstration entry, not medical advice', '2026-10-01 00:00:00');

-- Link each pet medication to its reference entry
UPDATE Pet_Medication SET medication_ref_id = (SELECT medication_ref_id FROM Medication_Reference WHERE name = 'Cetirizine') WHERE name = 'Cetirizine';
UPDATE Pet_Medication SET medication_ref_id = (SELECT medication_ref_id FROM Medication_Reference WHERE name = 'Carprofen')  WHERE name = 'Carprofen';
UPDATE Pet_Medication SET medication_ref_id = (SELECT medication_ref_id FROM Medication_Reference WHERE name = 'Apoquel')    WHERE name = 'Apoquel';

INSERT INTO Product (product_code, name, description, usage_guidance) VALUES
('PRD-JOINT', 'Senior Joint Support Chews',     'Daily chews with glucosamine for older dogs.',          'Give with food. Ask your vet before starting.'),
('PRD-HYPO',  'Sensitive Skin Dog Food',        'Limited-ingredient food for dogs with food allergies.',  'Switch over 7 days.'),
('PRD-DENT',  'Dental Care Chews',              'Chews that help reduce plaque.',                        'One chew per day.'),
('PRD-CALM',  'Calm Paws Miracle Drops',        'Claims to cure anxiety instantly.',                     'Unverified claims; under review.');

INSERT INTO Product_Review (product_id, reviewer_user_id, rating, review_text) VALUES
((SELECT product_id FROM Product WHERE product_code = 'PRD-JOINT'), 87370000, 5, 'Bella moves more easily after a month.'),
((SELECT product_id FROM Product WHERE product_code = 'PRD-DENT'),  87370001, 3, 'Rocky likes them, but they break apart fast.'),
((SELECT product_id FROM Product WHERE product_code = 'PRD-HYPO'),  87370000, 4, 'Helped with Bella''s itchy skin.');

INSERT INTO Health_Resource (author_user_id, title, resource_type, body, keywords) VALUES
(NULL,     'Foods That Are Toxic to Dogs',  'faq',   'Chocolate, grapes, raisins, onions, garlic and xylitol can make dogs very sick.', 'toxic,chocolate,grapes,dogs'),
(87370003, 'Signs Your Pet Needs a Vet Now', 'guide', 'Trouble breathing, not eating for a day, or heavy bleeding all need a vet right away.', 'emergency,vet,warning signs');

-- ============ MODERATION & OVERSIGHT ============

-- Report 1: Maya reports Sofia for spam (handled and closed)
-- Report 2: Kevin reports a product with false claims (still open)
INSERT INTO Report (reporter_user_id, post_id, comment_id, reported_user_id, response_id, product_id, reason, status, created_at) VALUES
(87370000, NULL, NULL, 87370002, NULL, NULL, 'Sending spam messages selling fake miracle pills.', 'resolved', '2026-10-27 18:30:00'),
(87370005, NULL, NULL, NULL, NULL, (SELECT product_id FROM Product WHERE product_code = 'PRD-CALM'), 'Product claims to cure anxiety instantly, which is misleading.', 'open', '2026-11-01 10:00:00');

INSERT INTO Moderation_Case (report_id, assigned_moderator_id, case_status, opened_at, closed_at) VALUES
((SELECT report_id FROM Report WHERE reported_user_id = 87370002), 87370006, 'closed', '2026-10-28 09:00:00', '2026-10-28 16:00:00'),
((SELECT report_id FROM Report WHERE product_id IS NOT NULL),      NULL,     'open',   '2026-11-01 10:05:00', NULL);

-- Tasha's actions on case 1
INSERT INTO Moderation_Action (case_id, actor_user_id, target_user_id, action_type, reason, created_at) VALUES
((SELECT case_id FROM Moderation_Case WHERE case_status = 'closed'), 87370006, 87370002, 'warn',    'First warning for spam messages.',       '2026-10-28 10:00:00'),
((SELECT case_id FROM Moderation_Case WHERE case_status = 'closed'), 87370006, 87370002, 'suspend', 'Kept sending spam after the warning.', '2026-10-28 15:55:00');

-- The suspension (this is why Sofia's account_status is 'suspended' in seed.sql)
INSERT INTO User_Restriction (user_id, action_id, starts_at, ends_at, status) VALUES
(87370002, (SELECT action_id FROM Moderation_Action WHERE action_type = 'suspend' AND target_user_id = 87370002), '2026-10-28 16:00:00', '2026-11-27 16:00:00', 'active');

INSERT INTO System_Setting (setting_key, setting_value, updated_at, updated_by_user_id) VALUES
('supported_pet_types',     'Dog,Cat,Bird,Rabbit', '2026-10-01 08:00:00', 87370007),
('reminder_lead_minutes',   '60',                  '2026-10-01 08:00:00', 87370007),
('max_photo_upload_mb',     '10',                  '2026-10-01 08:00:00', 87370007);

-- History of important actions
INSERT INTO Audit_Event (actor_user_id, event_type, entity_name, entity_id, occurred_at) VALUES
(87370007, 'approve_professional', 'Professional_Profile', (SELECT profile_id FROM Professional_Profile WHERE user_id = 87370003), '2026-10-01 09:00:00'),
(87370007, 'approve_professional', 'Professional_Profile', (SELECT profile_id FROM Professional_Profile WHERE user_id = 87370004), '2026-10-01 09:20:00'),
(87370006, 'suspend_user',         'User',                 87370002,                                                                '2026-10-28 16:00:00'),
(87370007, 'update_setting',       'System_Setting',       (SELECT setting_id FROM System_Setting WHERE setting_key = 'supported_pet_types'), '2026-10-01 08:00:00');
