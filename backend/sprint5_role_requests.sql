-- PetMed Sprint V: role requests.
-- After signing up, a user can ask to become a Veterinarian, Pet Health Expert,
-- Community Moderator or Administrator. An administrator approves or rejects
-- each request; only then does the user get the new role.
--
-- Run AFTER the other five scripts:
--   cat sprint5_role_requests.sql | mysql -u root -p

USE petmed;

CREATE TABLE IF NOT EXISTS `Role_Request` (
  `request_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` INT UNSIGNED NOT NULL,
  `role_id` INT UNSIGNED NOT NULL,
  `reason` TEXT NOT NULL,
  `status` VARCHAR(20) NOT NULL DEFAULT 'pending',
  `requested_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `reviewed_by_user_id` INT UNSIGNED NULL,
  `reviewed_at` DATETIME NULL,
  `review_notes` TEXT NULL,
  PRIMARY KEY (`request_id`),
  CONSTRAINT `fk_role_request_user_id` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`),
  CONSTRAINT `fk_role_request_role_id` FOREIGN KEY (`role_id`) REFERENCES `Role` (`role_id`),
  CONSTRAINT `fk_role_request_reviewed_by_user_id` FOREIGN KEY (`reviewed_by_user_id`) REFERENCES `User` (`user_id`),
  CONSTRAINT `chk_role_request_status` CHECK (`status` IN ('pending', 'approved', 'rejected'))
) ENGINE=InnoDB;

-- Sample: Marcus Williams (pet owner) asks to help moderate the community.
INSERT INTO Role_Request (user_id, role_id, reason, status, requested_at) VALUES
(87370001, (SELECT role_id FROM Role WHERE role_name = 'community_moderator'),
 'I am active in the community every day and want to help keep advice safe.', 'pending', '2026-11-16 09:00:00');
