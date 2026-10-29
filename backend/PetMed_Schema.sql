-- PetMed database schema (MySQL 8.0.16 or later)
-- Built from PetMed_ERD_Business_Rules_Organized.svg (tables, columns, keys, optional fields)
-- and PetMed_Sprint_2_Data_Dictionary.md (data types).
-- Tables are created first, grouped by module; foreign keys are added at the bottom,
-- so the tables can be created in any order.

CREATE DATABASE IF NOT EXISTS petmed CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE petmed;

SET FOREIGN_KEY_CHECKS = 0;


# USER (Accounts & Access)

CREATE TABLE `User` (
  `user_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) NOT NULL UNIQUE,
  `password_hash` VARCHAR(255) NOT NULL,
  `full_name` VARCHAR(255) NOT NULL,
  `account_status` VARCHAR(30) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=87370000;

CREATE TABLE `Role` (
  `role_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `role_name` VARCHAR(40) NOT NULL UNIQUE,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB;

CREATE TABLE `Permission` (
  `permission_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `permission_code` VARCHAR(100) NOT NULL UNIQUE,
  PRIMARY KEY (`permission_id`)
) ENGINE=InnoDB;

CREATE TABLE `User_Role` (
  `user_id` INT UNSIGNED NOT NULL,
  `role_id` INT UNSIGNED NOT NULL,
  `assigned_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`, `role_id`)
) ENGINE=InnoDB;

CREATE TABLE `Role_Permission` (
  `role_id` INT UNSIGNED NOT NULL,
  `permission_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`role_id`, `permission_id`)
) ENGINE=InnoDB;

CREATE TABLE `Professional_Profile` (
  `profile_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` INT UNSIGNED NOT NULL UNIQUE,
  `professional_type` VARCHAR(30) NOT NULL,
  `credentials` TEXT NOT NULL,
  `specialty` VARCHAR(100) NOT NULL,
  `organization` VARCHAR(255) NOT NULL,
  `experience` TEXT NOT NULL,
  `verification_status` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`profile_id`)
) ENGINE=InnoDB;

CREATE TABLE `User_Restriction` (
  `restriction_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` INT UNSIGNED NOT NULL,
  `action_id` INT UNSIGNED NOT NULL,
  `starts_at` DATETIME NOT NULL,
  `ends_at` DATETIME NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`restriction_id`),
  CONSTRAINT chk_user_restriction_1 CHECK (ends_at > starts_at)
) ENGINE=InnoDB;

CREATE TABLE `Notification` (
  `notification_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` INT UNSIGNED NOT NULL,
  `type` VARCHAR(30) NOT NULL,
  `message` TEXT NOT NULL,
  `is_read` BOOLEAN NOT NULL DEFAULT FALSE,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`notification_id`)
) ENGINE=InnoDB;

CREATE TABLE `Message` (
  `message_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `sender_user_id` INT UNSIGNED NOT NULL,
  `recipient_user_id` INT UNSIGNED NOT NULL,
  `body` TEXT NOT NULL,
  `sent_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`message_id`)
) ENGINE=InnoDB;

CREATE TABLE `Verification_Review` (
  `review_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `profile_id` INT UNSIGNED NOT NULL,
  `admin_user_id` INT UNSIGNED NOT NULL,
  `decision` VARCHAR(20) NOT NULL,
  `reviewed_at` DATETIME NOT NULL,
  `notes` TEXT NOT NULL,
  PRIMARY KEY (`review_id`)
) ENGINE=InnoDB;


# Pet Health

CREATE TABLE `Pet` (
  `pet_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `owner_user_id` INT UNSIGNED NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `species` VARCHAR(50) NOT NULL,
  `breed` VARCHAR(100) NOT NULL,
  `birth_date` DATE NOT NULL,
  `weight` DECIMAL(7,2) NOT NULL,
  PRIMARY KEY (`pet_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7380000;

CREATE TABLE `Treatment` (
  `treatment_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `pet_id` INT UNSIGNED NOT NULL,
  `professional_user_id` INT UNSIGNED NULL,
  `description` TEXT NOT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  PRIMARY KEY (`treatment_id`),
  CONSTRAINT chk_treatment_1 CHECK (end_date >= start_date)
) ENGINE=InnoDB;

CREATE TABLE `Pet_Allergy` (
  `allergy_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `pet_id` INT UNSIGNED NOT NULL,
  `allergen` VARCHAR(150) NOT NULL,
  `reaction` TEXT NOT NULL,
  `noted_at` DATETIME NOT NULL,
  PRIMARY KEY (`allergy_id`)
) ENGINE=InnoDB;

CREATE TABLE `Reminder` (
  `reminder_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `pet_id` INT UNSIGNED NOT NULL,
  `user_id` INT UNSIGNED NOT NULL,
  `pet_medication_id` INT UNSIGNED NULL,
  `due_at` DATETIME NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`reminder_id`)
) ENGINE=InnoDB;

CREATE TABLE `Pet_Condition` (
  `condition_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `pet_id` INT UNSIGNED NOT NULL,
  `condition_name` VARCHAR(150) NOT NULL,
  `diagnosed_at` DATE NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`condition_id`)
) ENGINE=InnoDB;

CREATE TABLE `Data_Share_Authorization` (
  `authorization_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `pet_id` INT UNSIGNED NOT NULL,
  `owner_user_id` INT UNSIGNED NOT NULL,
  `professional_user_id` INT UNSIGNED NOT NULL,
  `scope` VARCHAR(100) NOT NULL,
  `granted_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `expires_at` DATETIME NULL,
  `revoked_at` DATETIME NULL,
  PRIMARY KEY (`authorization_id`),
  CONSTRAINT chk_data_share_authorization_1 CHECK (expires_at IS NULL OR expires_at > granted_at)
) ENGINE=InnoDB;

CREATE TABLE `Symptom_Log` (
  `symptom_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `pet_id` INT UNSIGNED NOT NULL,
  `symptom` VARCHAR(255) NOT NULL,
  `severity` VARCHAR(20) NOT NULL,
  `observed_at` DATETIME NOT NULL,
  `notes` TEXT NOT NULL,
  PRIMARY KEY (`symptom_id`)
) ENGINE=InnoDB;

CREATE TABLE `Vet_Referral` (
  `referral_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `pet_id` INT UNSIGNED NOT NULL,
  `vet_user_id` INT UNSIGNED NOT NULL,
  `reason` TEXT NOT NULL,
  `urgency` VARCHAR(20) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`referral_id`)
) ENGINE=InnoDB;

CREATE TABLE `Pet_Medication` (
  `pet_medication_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `pet_id` INT UNSIGNED NOT NULL,
  `medication_ref_id` INT UNSIGNED NULL,
  `name` VARCHAR(150) NOT NULL,
  `dosage` VARCHAR(100) NOT NULL,
  `frequency` VARCHAR(100) NOT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  PRIMARY KEY (`pet_medication_id`),
  CONSTRAINT chk_pet_medication_1 CHECK (end_date >= start_date)
) ENGINE=InnoDB;


# Catalog & Reference

CREATE TABLE `Product` (
  `product_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `product_code` VARCHAR(255) NOT NULL UNIQUE,
  `name` VARCHAR(200) NOT NULL,
  `description` TEXT NOT NULL,
  `usage_guidance` TEXT NOT NULL,
  `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB;

CREATE TABLE `Health_Resource` (
  `resource_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `author_user_id` INT UNSIGNED NULL,
  `title` VARCHAR(200) NOT NULL,
  `resource_type` VARCHAR(30) NOT NULL,
  `body` TEXT NOT NULL,
  `keywords` VARCHAR(500) NOT NULL,
  `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (`resource_id`)
) ENGINE=InnoDB;

CREATE TABLE `Medication_Reference` (
  `medication_ref_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `medication_code` VARCHAR(255) NOT NULL UNIQUE,
  `name` VARCHAR(255) NOT NULL,
  `uses` TEXT NOT NULL,
  `dosage_guidance` TEXT NOT NULL,
  `warnings` TEXT NOT NULL,
  `side_effects` TEXT NOT NULL,
  `source` VARCHAR(255) NOT NULL,
  `last_reviewed_at` DATETIME NOT NULL,
  PRIMARY KEY (`medication_ref_id`)
) ENGINE=InnoDB;

CREATE TABLE `Product_Review` (
  `review_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `product_id` INT UNSIGNED NOT NULL,
  `reviewer_user_id` INT UNSIGNED NOT NULL,
  `rating` TINYINT UNSIGNED NOT NULL,
  `review_text` TEXT NOT NULL,
  `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`review_id`),
  CONSTRAINT chk_product_review_1 CHECK (rating BETWEEN 1 AND 5)
) ENGINE=InnoDB;


# Moderation & Oversight

CREATE TABLE `Report` (
  `report_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `reporter_user_id` INT UNSIGNED NOT NULL,
  `post_id` INT UNSIGNED NULL,
  `comment_id` INT UNSIGNED NULL,
  `reported_user_id` INT UNSIGNED NULL,
  `response_id` INT UNSIGNED NULL,
  `product_id` INT UNSIGNED NULL,
  `reason` TEXT NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`report_id`),
  CONSTRAINT chk_report_1 CHECK (post_id IS NOT NULL OR comment_id IS NOT NULL OR reported_user_id IS NOT NULL OR response_id IS NOT NULL OR product_id IS NOT NULL)
) ENGINE=InnoDB;

CREATE TABLE `Moderation_Case` (
  `case_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `report_id` INT UNSIGNED NOT NULL,
  `assigned_moderator_id` INT UNSIGNED NULL,
  `case_status` VARCHAR(20) NOT NULL,
  `opened_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `closed_at` DATETIME NULL,
  PRIMARY KEY (`case_id`)
) ENGINE=InnoDB;

CREATE TABLE `System_Setting` (
  `setting_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `setting_key` VARCHAR(100) NOT NULL UNIQUE,
  `setting_value` TEXT NOT NULL,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by_user_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`setting_id`)
) ENGINE=InnoDB;

CREATE TABLE `Audit_Event` (
  `audit_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `actor_user_id` INT UNSIGNED NOT NULL,
  `event_type` VARCHAR(50) NOT NULL,
  `entity_name` VARCHAR(50) NOT NULL,
  `entity_id` INT UNSIGNED NOT NULL,
  `occurred_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`audit_id`)
) ENGINE=InnoDB;

CREATE TABLE `Moderation_Action` (
  `action_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `case_id` INT UNSIGNED NOT NULL,
  `actor_user_id` INT UNSIGNED NOT NULL,
  `target_user_id` INT UNSIGNED NULL,
  `action_type` VARCHAR(30) NOT NULL,
  `reason` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`action_id`)
) ENGINE=InnoDB;


# Community & Advice

CREATE TABLE `Post` (
  `post_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `author_user_id` INT UNSIGNED NOT NULL,
  `pet_id` INT UNSIGNED NULL,
  `body` TEXT NOT NULL,
  `post_type` VARCHAR(30) NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`post_id`)
) ENGINE=InnoDB;

CREATE TABLE `Tag` (
  `tag_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tag_name` VARCHAR(80) NOT NULL UNIQUE,
  `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (`tag_id`)
) ENGINE=InnoDB;

CREATE TABLE `Health_Article` (
  `article_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `author_user_id` INT UNSIGNED NOT NULL,
  `title` VARCHAR(200) NOT NULL,
  `content` TEXT NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  `published_at` DATETIME NOT NULL,
  PRIMARY KEY (`article_id`)
) ENGINE=InnoDB;

CREATE TABLE `Health_Question` (
  `question_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `asker_user_id` INT UNSIGNED NOT NULL,
  `pet_id` INT UNSIGNED NULL,
  `directed_to_user_id` INT UNSIGNED NULL,
  `question_text` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`question_id`)
) ENGINE=InnoDB;

CREATE TABLE `Comment` (
  `comment_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `post_id` INT UNSIGNED NOT NULL,
  `author_user_id` INT UNSIGNED NOT NULL,
  `parent_comment_id` INT UNSIGNED NULL,
  `body` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comment_id`)
) ENGINE=InnoDB;

CREATE TABLE `Post_Like` (
  `user_id` INT UNSIGNED NOT NULL,
  `post_id` INT UNSIGNED NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`, `post_id`)
) ENGINE=InnoDB;

CREATE TABLE `Post_Save` (
  `user_id` INT UNSIGNED NOT NULL,
  `post_id` INT UNSIGNED NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`, `post_id`)
) ENGINE=InnoDB;

CREATE TABLE `Post_Share` (
  `share_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `post_id` INT UNSIGNED NOT NULL,
  `user_id` INT UNSIGNED NOT NULL,
  `shared_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`share_id`)
) ENGINE=InnoDB;

CREATE TABLE `Post_Tag` (
  `post_id` INT UNSIGNED NOT NULL,
  `tag_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`post_id`, `tag_id`)
) ENGINE=InnoDB;

CREATE TABLE `User_Follow` (
  `follower_user_id` INT UNSIGNED NOT NULL,
  `followed_user_id` INT UNSIGNED NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`follower_user_id`, `followed_user_id`),
  CONSTRAINT chk_user_follow_1 CHECK (follower_user_id <> followed_user_id)
) ENGINE=InnoDB;

CREATE TABLE `Article_Tag` (
  `article_id` INT UNSIGNED NOT NULL,
  `tag_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`article_id`, `tag_id`)
) ENGINE=InnoDB;

CREATE TABLE `Advice_Response` (
  `response_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `question_id` INT UNSIGNED NOT NULL,
  `author_user_id` INT UNSIGNED NOT NULL,
  `source_type` VARCHAR(20) NOT NULL,
  `response_text` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`response_id`)
) ENGINE=InnoDB;

CREATE TABLE `Advice_Review` (
  `review_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `response_id` INT UNSIGNED NOT NULL,
  `reviewer_user_id` INT UNSIGNED NOT NULL,
  `rating` TINYINT UNSIGNED NOT NULL,
  `feedback` TEXT NOT NULL,
  PRIMARY KEY (`review_id`),
  UNIQUE KEY uq_advice_review_response_id_reviewer_user_id (`response_id`, `reviewer_user_id`),
  CONSTRAINT chk_advice_review_1 CHECK (rating BETWEEN 1 AND 5)
) ENGINE=InnoDB;


# Foreign keys (one per FK column in the ERD)

ALTER TABLE `User_Role` ADD CONSTRAINT fk_user_role_user_id FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `User_Role` ADD CONSTRAINT fk_user_role_role_id FOREIGN KEY (`role_id`) REFERENCES `Role` (`role_id`);
ALTER TABLE `Role_Permission` ADD CONSTRAINT fk_role_permission_role_id FOREIGN KEY (`role_id`) REFERENCES `Role` (`role_id`);
ALTER TABLE `Role_Permission` ADD CONSTRAINT fk_role_permission_permission_id FOREIGN KEY (`permission_id`) REFERENCES `Permission` (`permission_id`);
ALTER TABLE `Professional_Profile` ADD CONSTRAINT fk_professional_profile_user_id FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Verification_Review` ADD CONSTRAINT fk_verification_review_profile_id FOREIGN KEY (`profile_id`) REFERENCES `Professional_Profile` (`profile_id`);
ALTER TABLE `Verification_Review` ADD CONSTRAINT fk_verification_review_admin_user_id FOREIGN KEY (`admin_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Message` ADD CONSTRAINT fk_message_sender_user_id FOREIGN KEY (`sender_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Message` ADD CONSTRAINT fk_message_recipient_user_id FOREIGN KEY (`recipient_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Notification` ADD CONSTRAINT fk_notification_user_id FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `User_Restriction` ADD CONSTRAINT fk_user_restriction_user_id FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `User_Restriction` ADD CONSTRAINT fk_user_restriction_action_id FOREIGN KEY (`action_id`) REFERENCES `Moderation_Action` (`action_id`);
ALTER TABLE `Pet` ADD CONSTRAINT fk_pet_owner_user_id FOREIGN KEY (`owner_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Pet_Allergy` ADD CONSTRAINT fk_pet_allergy_pet_id FOREIGN KEY (`pet_id`) REFERENCES `Pet` (`pet_id`);
ALTER TABLE `Pet_Condition` ADD CONSTRAINT fk_pet_condition_pet_id FOREIGN KEY (`pet_id`) REFERENCES `Pet` (`pet_id`);
ALTER TABLE `Symptom_Log` ADD CONSTRAINT fk_symptom_log_pet_id FOREIGN KEY (`pet_id`) REFERENCES `Pet` (`pet_id`);
ALTER TABLE `Treatment` ADD CONSTRAINT fk_treatment_pet_id FOREIGN KEY (`pet_id`) REFERENCES `Pet` (`pet_id`);
ALTER TABLE `Treatment` ADD CONSTRAINT fk_treatment_professional_user_id FOREIGN KEY (`professional_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Pet_Medication` ADD CONSTRAINT fk_pet_medication_pet_id FOREIGN KEY (`pet_id`) REFERENCES `Pet` (`pet_id`);
ALTER TABLE `Pet_Medication` ADD CONSTRAINT fk_pet_medication_medication_ref_id FOREIGN KEY (`medication_ref_id`) REFERENCES `Medication_Reference` (`medication_ref_id`);
ALTER TABLE `Reminder` ADD CONSTRAINT fk_reminder_pet_id FOREIGN KEY (`pet_id`) REFERENCES `Pet` (`pet_id`);
ALTER TABLE `Reminder` ADD CONSTRAINT fk_reminder_user_id FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Reminder` ADD CONSTRAINT fk_reminder_pet_medication_id FOREIGN KEY (`pet_medication_id`) REFERENCES `Pet_Medication` (`pet_medication_id`);
ALTER TABLE `Data_Share_Authorization` ADD CONSTRAINT fk_data_share_authorization_pet_id FOREIGN KEY (`pet_id`) REFERENCES `Pet` (`pet_id`);
ALTER TABLE `Data_Share_Authorization` ADD CONSTRAINT fk_data_share_authorization_owner_user_id FOREIGN KEY (`owner_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Data_Share_Authorization` ADD CONSTRAINT fk_data_share_authorization_professional_user_id FOREIGN KEY (`professional_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Vet_Referral` ADD CONSTRAINT fk_vet_referral_pet_id FOREIGN KEY (`pet_id`) REFERENCES `Pet` (`pet_id`);
ALTER TABLE `Vet_Referral` ADD CONSTRAINT fk_vet_referral_vet_user_id FOREIGN KEY (`vet_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Post` ADD CONSTRAINT fk_post_author_user_id FOREIGN KEY (`author_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Post` ADD CONSTRAINT fk_post_pet_id FOREIGN KEY (`pet_id`) REFERENCES `Pet` (`pet_id`);
ALTER TABLE `Comment` ADD CONSTRAINT fk_comment_post_id FOREIGN KEY (`post_id`) REFERENCES `Post` (`post_id`);
ALTER TABLE `Comment` ADD CONSTRAINT fk_comment_author_user_id FOREIGN KEY (`author_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Comment` ADD CONSTRAINT fk_comment_parent_comment_id FOREIGN KEY (`parent_comment_id`) REFERENCES `Comment` (`comment_id`);
ALTER TABLE `Post_Like` ADD CONSTRAINT fk_post_like_user_id FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Post_Like` ADD CONSTRAINT fk_post_like_post_id FOREIGN KEY (`post_id`) REFERENCES `Post` (`post_id`);
ALTER TABLE `Post_Save` ADD CONSTRAINT fk_post_save_user_id FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Post_Save` ADD CONSTRAINT fk_post_save_post_id FOREIGN KEY (`post_id`) REFERENCES `Post` (`post_id`);
ALTER TABLE `User_Follow` ADD CONSTRAINT fk_user_follow_follower_user_id FOREIGN KEY (`follower_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `User_Follow` ADD CONSTRAINT fk_user_follow_followed_user_id FOREIGN KEY (`followed_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Post_Tag` ADD CONSTRAINT fk_post_tag_post_id FOREIGN KEY (`post_id`) REFERENCES `Post` (`post_id`);
ALTER TABLE `Post_Tag` ADD CONSTRAINT fk_post_tag_tag_id FOREIGN KEY (`tag_id`) REFERENCES `Tag` (`tag_id`);
ALTER TABLE `Health_Article` ADD CONSTRAINT fk_health_article_author_user_id FOREIGN KEY (`author_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Article_Tag` ADD CONSTRAINT fk_article_tag_article_id FOREIGN KEY (`article_id`) REFERENCES `Health_Article` (`article_id`);
ALTER TABLE `Article_Tag` ADD CONSTRAINT fk_article_tag_tag_id FOREIGN KEY (`tag_id`) REFERENCES `Tag` (`tag_id`);
ALTER TABLE `Health_Question` ADD CONSTRAINT fk_health_question_asker_user_id FOREIGN KEY (`asker_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Health_Question` ADD CONSTRAINT fk_health_question_pet_id FOREIGN KEY (`pet_id`) REFERENCES `Pet` (`pet_id`);
ALTER TABLE `Health_Question` ADD CONSTRAINT fk_health_question_directed_to_user_id FOREIGN KEY (`directed_to_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Advice_Response` ADD CONSTRAINT fk_advice_response_question_id FOREIGN KEY (`question_id`) REFERENCES `Health_Question` (`question_id`);
ALTER TABLE `Advice_Response` ADD CONSTRAINT fk_advice_response_author_user_id FOREIGN KEY (`author_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Advice_Review` ADD CONSTRAINT fk_advice_review_response_id FOREIGN KEY (`response_id`) REFERENCES `Advice_Response` (`response_id`);
ALTER TABLE `Advice_Review` ADD CONSTRAINT fk_advice_review_reviewer_user_id FOREIGN KEY (`reviewer_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Post_Share` ADD CONSTRAINT fk_post_share_post_id FOREIGN KEY (`post_id`) REFERENCES `Post` (`post_id`);
ALTER TABLE `Post_Share` ADD CONSTRAINT fk_post_share_user_id FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Report` ADD CONSTRAINT fk_report_reporter_user_id FOREIGN KEY (`reporter_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Report` ADD CONSTRAINT fk_report_post_id FOREIGN KEY (`post_id`) REFERENCES `Post` (`post_id`);
ALTER TABLE `Report` ADD CONSTRAINT fk_report_comment_id FOREIGN KEY (`comment_id`) REFERENCES `Comment` (`comment_id`);
ALTER TABLE `Report` ADD CONSTRAINT fk_report_reported_user_id FOREIGN KEY (`reported_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Report` ADD CONSTRAINT fk_report_response_id FOREIGN KEY (`response_id`) REFERENCES `Advice_Response` (`response_id`);
ALTER TABLE `Report` ADD CONSTRAINT fk_report_product_id FOREIGN KEY (`product_id`) REFERENCES `Product` (`product_id`);
ALTER TABLE `Moderation_Case` ADD CONSTRAINT fk_moderation_case_report_id FOREIGN KEY (`report_id`) REFERENCES `Report` (`report_id`);
ALTER TABLE `Moderation_Case` ADD CONSTRAINT fk_moderation_case_assigned_moderator_id FOREIGN KEY (`assigned_moderator_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Moderation_Action` ADD CONSTRAINT fk_moderation_action_case_id FOREIGN KEY (`case_id`) REFERENCES `Moderation_Case` (`case_id`);
ALTER TABLE `Moderation_Action` ADD CONSTRAINT fk_moderation_action_actor_user_id FOREIGN KEY (`actor_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Moderation_Action` ADD CONSTRAINT fk_moderation_action_target_user_id FOREIGN KEY (`target_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `System_Setting` ADD CONSTRAINT fk_system_setting_updated_by_user_id FOREIGN KEY (`updated_by_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Audit_Event` ADD CONSTRAINT fk_audit_event_actor_user_id FOREIGN KEY (`actor_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Product_Review` ADD CONSTRAINT fk_product_review_product_id FOREIGN KEY (`product_id`) REFERENCES `Product` (`product_id`);
ALTER TABLE `Product_Review` ADD CONSTRAINT fk_product_review_reviewer_user_id FOREIGN KEY (`reviewer_user_id`) REFERENCES `User` (`user_id`);
ALTER TABLE `Health_Resource` ADD CONSTRAINT fk_health_resource_author_user_id FOREIGN KEY (`author_user_id`) REFERENCES `User` (`user_id`);

SET FOREIGN_KEY_CHECKS = 1;
