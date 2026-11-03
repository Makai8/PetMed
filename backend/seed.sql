USE petmed;

-- Roles: IDs 1 to 5 in this order
INSERT INTO Role (role_name) VALUES
('pet_owner'),
('veterinarian'),
('pet_health_expert'),
('community_moderator'),
('administrator');

-- Users: IDs start at 87370000
INSERT INTO User (email, password_hash, full_name, account_status) VALUES
('maya.johnson@petmed.com',    '$2b$10$examplehashMaya',    'Maya Johnson',      'active'),
('marcus.williams@petmed.com', '$2b$10$examplehashMarcus',  'Marcus Williams',   'active'),
('sofia.ramirez@petmed.com',   '$2b$10$examplehashSofia',   'Sofia Ramirez',     'suspended'),
('dr.james.carter@petmed.com', '$2b$10$examplehashJames',   'Dr. James Carter',  'active'),
('dr.aisha.bello@petmed.com',  '$2b$10$examplehashAisha',   'Dr. Aisha Bello',   'active'),
('kevin.nguyen@petmed.com',    '$2b$10$examplehashKevin',   'Kevin Nguyen',      'active'),
('tasha.brooks@petmed.com',    '$2b$10$examplehashTasha',   'Tasha Brooks',      'active'),
('daniel.owens@petmed.com',    '$2b$10$examplehashDaniel',  'Daniel Owens',      'active');

-- Link each user to a role
INSERT INTO User_Role (user_id, role_id) VALUES
(87370000, 1),  -- Maya, pet owner
(87370001, 1),  -- Marcus, pet owner
(87370002, 1),  -- Sofia, pet owner (suspended)
(87370003, 2),  -- Dr. Carter, veterinarian
(87370004, 2),  -- Dr. Bello, veterinarian
(87370005, 3),  -- Kevin, pet health expert
(87370006, 4),  -- Tasha, community moderator
(87370007, 5);  -- Daniel, administrator

-- Pets: IDs start at 7380000, weight in pounds
INSERT INTO Pet (owner_user_id, name, species, breed, birth_date, weight) VALUES
(87370000, 'Bella',  'Dog',  'Golden Retriever', '2018-04-12', 65.40),
(87370000, 'Milo',   'Cat',  'Siamese',          '2021-09-03', 9.80),
(87370001, 'Rocky',  'Dog',  'German Shepherd',  '2016-02-20', 78.20),
(87370001, 'Luna',   'Dog',  'French Bulldog',   '2022-06-15', 24.50),
(87370002, 'Simba',  'Cat',  'Maine Coon',       '2019-11-30', 16.30),
(87370002, 'Kiwi',   'Bird', 'Cockatiel',        '2023-03-08', 0.20);

-- Symptom logs: each one points to a pet
INSERT INTO Symptom_Log (pet_id, symptom, severity, observed_at, notes) VALUES
(7380000, 'Limping on back left leg',   'moderate', '2026-10-20 08:15:00', 'Worse after long walks, possible hip stiffness'),
(7380000, 'Drinking more water than usual', 'mild', '2026-10-24 19:30:00', 'Bowl emptied twice in one evening'),
(7380001, 'Vomiting after meals',       'moderate', '2026-10-22 12:45:00', 'Happened twice, switched food last week'),
(7380002, 'Loss of appetite',           'severe',   '2026-10-25 07:00:00', 'Skipped breakfast and dinner, low energy'),
(7380003, 'Heavy breathing',            'mild',     '2026-10-26 15:10:00', 'Mostly after playing outside in the heat'),
(7380004, 'Excessive scratching',       'mild',     '2026-10-27 21:00:00', 'Focused around the ears');

-- Posts: IDs start at 1
INSERT INTO Post (author_user_id, pet_id, body, post_type, status) VALUES
(87370000, 7380000, 'Bella turned 8 this year and is slowing down on walks. Any tips for senior Golden Retrievers?', 'question', 'published'),
(87370001, 7380003, 'Luna finally learned to sit and stay! French Bulldogs are stubborn but worth it.', 'update', 'published'),
(87370005, NULL,    'Reminder: chocolate, grapes and onions are toxic to dogs. Keep holiday treats out of reach.', 'tip', 'published'),
(87370002, 7380005, 'Kiwi has been extra loud in the mornings. Is that normal for cockatiels?', 'question', 'hidden');

-- Comments: each points to a post
INSERT INTO Comment (post_id, author_user_id, parent_comment_id, body) VALUES
(1, 87370003, NULL, 'Shorter, more frequent walks help a lot with senior dogs. A joint supplement is worth asking your vet about.'),
(1, 87370000, 1,    'Thank you Dr. Carter, I will try shorter walks this week.'),
(2, 87370000, NULL, 'Congrats! Consistency is everything with Frenchies.'),
(3, 87370001, NULL, 'Good reminder, Rocky almost got into a bag of grapes last month.');

-- Health questions sent to experts
INSERT INTO Health_Question (asker_user_id, pet_id, directed_to_user_id, question_text) VALUES
(87370001, 7380002, 87370004, 'Rocky has skipped two meals and seems tired. Should I bring him in today?'),
(87370000, 7380001, 87370005, 'What is the best way to switch Milo to a new food without upsetting his stomach?');
