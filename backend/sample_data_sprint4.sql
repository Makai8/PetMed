-- PetMed Sprint IV sample data: sign-in passwords and data for each role's use case.
-- Run AFTER: PetMedDB.sql, seed.sql, sample_data_health_records.sql, sample_data_more.sql
--   cat sample_data_sprint4.sql | mysql -u root -p
--
-- DEMO ONLY: every sample account uses the password  PetMed123!
-- The database stores only a salted hash of it (PBKDF2-SHA256), never the password itself.
-- Sofia Ramirez is suspended, so her sign-in is refused even with the right password.

USE petmed;

-- 1. Real password hashes (the seed file only had placeholders)
UPDATE User SET password_hash = 'pbkdf2:sha256:600000$oGN7u0MkR73wE7OU$a0956f5d60ba37bc917d82b79f749f15d1bf3a62de74f76fa5cec9173334609e' WHERE email = 'maya.johnson@petmed.com';
UPDATE User SET password_hash = 'pbkdf2:sha256:600000$N4A6J5wvkxnrH4MR$bac8d1de0056c57a612121b4a2da9c2e4d35f93519ab5c3c7bfa116eb5735403' WHERE email = 'marcus.williams@petmed.com';
UPDATE User SET password_hash = 'pbkdf2:sha256:600000$BsgzustJAQp5EN5C$0579ac0226873a4b9964aeeec584ee53beaa1d4bca41f1513f0d6ab2d139b212' WHERE email = 'sofia.ramirez@petmed.com';
UPDATE User SET password_hash = 'pbkdf2:sha256:600000$dFCptM6Aiz3WHyum$7d2630eadb4eb6a8f472eb9efd5aaea68b2a97d00eca890f638736957cf58d9a' WHERE email = 'dr.james.carter@petmed.com';
UPDATE User SET password_hash = 'pbkdf2:sha256:600000$b8socgZ68DMPSooE$3f74890cf7f6a60c7dab377cf82ec3d4ccdb866b461ba8cd9cd891b655c860a0' WHERE email = 'dr.aisha.bello@petmed.com';
UPDATE User SET password_hash = 'pbkdf2:sha256:600000$gj8hSwGBC7b6WOBY$856606a4983e6c9fc9c01ef0f6012fe0db5bfce26ac598eac74844a5e0a90ac9' WHERE email = 'kevin.nguyen@petmed.com';
UPDATE User SET password_hash = 'pbkdf2:sha256:600000$dtC4FONEA55WcxtK$16565669f71dc98eaee5c9edcf89534f39b8a87697e3f0c756ae657c91d3bb40' WHERE email = 'tasha.brooks@petmed.com';
UPDATE User SET password_hash = 'pbkdf2:sha256:600000$lX59kqeBIRnlOkPw$21e11a9221bd78daa1fdd1ff17c3018a3b24e1256cf45bc399351995b09b16f2' WHERE email = 'daniel.owens@petmed.com';

-- 2. Give the earlier sample rows realistic dates so lists sort sensibly
UPDATE Post SET created_at = '2026-10-20 08:30:00' WHERE post_id = 1;
UPDATE Post SET created_at = '2026-10-21 17:45:00' WHERE post_id = 2;
UPDATE Post SET created_at = '2026-10-22 12:00:00' WHERE post_id = 3;
UPDATE Post SET created_at = '2026-10-24 07:15:00' WHERE post_id = 4;
UPDATE Comment SET created_at = '2026-10-20 10:05:00' WHERE comment_id = 1;
UPDATE Comment SET created_at = '2026-10-20 11:30:00' WHERE comment_id = 2;
UPDATE Comment SET created_at = '2026-10-21 19:00:00' WHERE comment_id = 3;
UPDATE Comment SET created_at = '2026-10-22 13:20:00' WHERE comment_id = 4;
UPDATE Health_Question SET created_at = '2026-10-25 09:00:00' WHERE question_id = 1;
UPDATE Health_Question SET created_at = '2026-10-23 12:00:00' WHERE question_id = 2;

-- 3. More community posts for the Pet Owner feed
INSERT INTO Post (author_user_id, pet_id, body, post_type, status, created_at) VALUES
(87370001, 7380002, 'Thinking about switching Rocky to a grain-free food. Anything I should watch for?', 'question', 'published', '2026-11-02 18:10:00'),
(87370003, NULL,    'Senior dogs should get a blood panel once a year. It catches kidney and thyroid problems early.', 'tip', 'published', '2026-11-03 09:00:00'),
(87370000, 7380001, 'Update: Milo did great with the slow food switch. No more upset stomach!', 'update', 'published', '2026-11-04 20:30:00'),
(87370001, NULL,    'A little garlic in your dog''s food keeps fleas away. Works every time for me.', 'tip', 'published', '2026-11-05 14:00:00'),
(87370005, NULL,    'Measure your pet''s food with a cup instead of guessing. Most overweight pets are simply overfed.', 'tip', 'published', '2026-11-06 08:00:00');

INSERT INTO Post_Tag (post_id, tag_id) VALUES
((SELECT post_id FROM Post WHERE body LIKE 'Thinking about switching Rocky%'), (SELECT tag_id FROM Tag WHERE tag_name = 'nutrition')),
((SELECT post_id FROM Post WHERE body LIKE 'Senior dogs should get a blood panel%'), (SELECT tag_id FROM Tag WHERE tag_name = 'senior-dogs')),
((SELECT post_id FROM Post WHERE body LIKE 'Update: Milo did great%'), (SELECT tag_id FROM Tag WHERE tag_name = 'cats')),
((SELECT post_id FROM Post WHERE body LIKE 'Update: Milo did great%'), (SELECT tag_id FROM Tag WHERE tag_name = 'nutrition')),
((SELECT post_id FROM Post WHERE body LIKE 'A little garlic%'), (SELECT tag_id FROM Tag WHERE tag_name = 'toxic-foods')),
((SELECT post_id FROM Post WHERE body LIKE 'Measure your pet%'), (SELECT tag_id FROM Tag WHERE tag_name = 'nutrition'));

INSERT INTO Comment (post_id, author_user_id, parent_comment_id, body, created_at) VALUES
((SELECT post_id FROM Post WHERE body LIKE 'Thinking about switching Rocky%'), 87370005, NULL, 'Grain-free is not better for most dogs. Ask your vet first, and switch slowly over a week.', '2026-11-02 19:00:00'),
((SELECT post_id FROM Post WHERE body LIKE 'A little garlic%'), 87370003, NULL, 'Please don''t. Garlic is toxic to dogs, even in small amounts.', '2026-11-05 14:30:00');

INSERT INTO Post_Like (user_id, post_id) VALUES
(87370000, (SELECT post_id FROM Post WHERE body LIKE 'Senior dogs should get a blood panel%')),
(87370001, (SELECT post_id FROM Post WHERE body LIKE 'Update: Milo did great%')),
(87370000, (SELECT post_id FROM Post WHERE body LIKE 'Measure your pet%'));

-- 4. More health questions for the Veterinarian and Pet Health Expert screens
INSERT INTO Health_Question (asker_user_id, pet_id, directed_to_user_id, question_text, created_at) VALUES
(87370000, 7380000, 87370003, 'Bella is drinking a lot more water lately. Could it be her kidneys?', '2026-11-03 10:15:00'),
(87370001, 7380003, NULL,     'Luna breathes heavily and snores after short walks. Is that normal for a French Bulldog?', '2026-11-04 16:40:00'),
(87370000, 7380000, 87370005, 'How many treats a day is too many for a 65 lb Golden Retriever?', '2026-11-05 09:30:00'),
(87370001, 7380002, NULL,     'Is plain cooked chicken and rice OK for Rocky while his stomach settles?', '2026-11-06 12:00:00');

-- A community answer that a vet reports as unsafe
INSERT INTO Advice_Response (question_id, author_user_id, source_type, response_text, created_at) VALUES
((SELECT question_id FROM Health_Question WHERE question_text LIKE 'Is plain cooked chicken%'), 87370000, 'community',
 'Chicken and rice is fine, and the cooked bones are fine too since they are soft.', '2026-11-06 13:10:00');

-- 5. Reported posts and reported health advice for the Community Moderator
INSERT INTO Report (reporter_user_id, post_id, comment_id, reported_user_id, response_id, product_id, reason, status, created_at) VALUES
(87370003, (SELECT post_id FROM Post WHERE body LIKE 'A little garlic%'), NULL, NULL, NULL, NULL,
 'Garlic is toxic to dogs. This post could get a pet hurt.', 'open', '2026-11-05 14:35:00'),
(87370004, NULL, NULL, NULL,
 (SELECT response_id FROM Advice_Response WHERE response_text LIKE 'Chicken and rice is fine, and the cooked bones%'), NULL,
 'Cooked bones splinter and can tear a dog''s stomach. This advice is unsafe.', 'open', '2026-11-06 14:00:00'),
(87370000, 4, NULL, NULL, NULL, NULL,
 'Posted by a suspended account that was sending spam.', 'resolved', '2026-10-28 11:00:00');

INSERT INTO Moderation_Case (report_id, assigned_moderator_id, case_status, opened_at, closed_at) VALUES
((SELECT report_id FROM Report WHERE reason LIKE 'Garlic is toxic%'), 87370006, 'open', '2026-11-05 15:00:00', NULL),
((SELECT report_id FROM Report WHERE reason LIKE 'Cooked bones splinter%'), NULL, 'open', '2026-11-06 14:05:00', NULL),
((SELECT report_id FROM Report WHERE reason LIKE 'Posted by a suspended account%'), 87370006, 'closed', '2026-10-28 11:10:00', '2026-10-28 16:00:00');
