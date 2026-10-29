-- MySQL dump 10.13  Distrib 26.10.0, for Win64 (x86_64)
--
-- Host: localhost    Database: petmed
-- ------------------------------------------------------
-- Server version	26.10.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'd5f3fb42-d2f5-11f1-bc96-24fbe3bf528a:1-115';

--
-- Current Database: `petmed`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `petmed` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `petmed`;

--
-- Table structure for table `advice_response`
--

DROP TABLE IF EXISTS `advice_response`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `advice_response` (
  `response_id` int unsigned NOT NULL AUTO_INCREMENT,
  `question_id` int unsigned NOT NULL,
  `author_user_id` int unsigned NOT NULL,
  `source_type` varchar(20) NOT NULL,
  `response_text` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`response_id`),
  KEY `fk_advice_response_question_id` (`question_id`),
  KEY `fk_advice_response_author_user_id` (`author_user_id`),
  CONSTRAINT `fk_advice_response_author_user_id` FOREIGN KEY (`author_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `fk_advice_response_question_id` FOREIGN KEY (`question_id`) REFERENCES `health_question` (`question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advice_response`
--

LOCK TABLES `advice_response` WRITE;
/*!40000 ALTER TABLE `advice_response` DISABLE KEYS */;
/*!40000 ALTER TABLE `advice_response` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `advice_review`
--

DROP TABLE IF EXISTS `advice_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `advice_review` (
  `review_id` int unsigned NOT NULL AUTO_INCREMENT,
  `response_id` int unsigned NOT NULL,
  `reviewer_user_id` int unsigned NOT NULL,
  `rating` tinyint unsigned NOT NULL,
  `feedback` text NOT NULL,
  PRIMARY KEY (`review_id`),
  UNIQUE KEY `uq_advice_review_response_id_reviewer_user_id` (`response_id`,`reviewer_user_id`),
  KEY `fk_advice_review_reviewer_user_id` (`reviewer_user_id`),
  CONSTRAINT `fk_advice_review_response_id` FOREIGN KEY (`response_id`) REFERENCES `advice_response` (`response_id`),
  CONSTRAINT `fk_advice_review_reviewer_user_id` FOREIGN KEY (`reviewer_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `chk_advice_review_1` CHECK ((`rating` between 1 and 5))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advice_review`
--

LOCK TABLES `advice_review` WRITE;
/*!40000 ALTER TABLE `advice_review` DISABLE KEYS */;
/*!40000 ALTER TABLE `advice_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `article_tag`
--

DROP TABLE IF EXISTS `article_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `article_tag` (
  `article_id` int unsigned NOT NULL,
  `tag_id` int unsigned NOT NULL,
  PRIMARY KEY (`article_id`,`tag_id`),
  KEY `fk_article_tag_tag_id` (`tag_id`),
  CONSTRAINT `fk_article_tag_article_id` FOREIGN KEY (`article_id`) REFERENCES `health_article` (`article_id`),
  CONSTRAINT `fk_article_tag_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `article_tag`
--

LOCK TABLES `article_tag` WRITE;
/*!40000 ALTER TABLE `article_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `article_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audit_event`
--

DROP TABLE IF EXISTS `audit_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_event` (
  `audit_id` int unsigned NOT NULL AUTO_INCREMENT,
  `actor_user_id` int unsigned NOT NULL,
  `event_type` varchar(50) NOT NULL,
  `entity_name` varchar(50) NOT NULL,
  `entity_id` int unsigned NOT NULL,
  `occurred_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`audit_id`),
  KEY `fk_audit_event_actor_user_id` (`actor_user_id`),
  CONSTRAINT `fk_audit_event_actor_user_id` FOREIGN KEY (`actor_user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_event`
--

LOCK TABLES `audit_event` WRITE;
/*!40000 ALTER TABLE `audit_event` DISABLE KEYS */;
/*!40000 ALTER TABLE `audit_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `comment_id` int unsigned NOT NULL AUTO_INCREMENT,
  `post_id` int unsigned NOT NULL,
  `author_user_id` int unsigned NOT NULL,
  `parent_comment_id` int unsigned DEFAULT NULL,
  `body` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comment_id`),
  KEY `fk_comment_post_id` (`post_id`),
  KEY `fk_comment_author_user_id` (`author_user_id`),
  KEY `fk_comment_parent_comment_id` (`parent_comment_id`),
  CONSTRAINT `fk_comment_author_user_id` FOREIGN KEY (`author_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `fk_comment_parent_comment_id` FOREIGN KEY (`parent_comment_id`) REFERENCES `comment` (`comment_id`),
  CONSTRAINT `fk_comment_post_id` FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_share_authorization`
--

DROP TABLE IF EXISTS `data_share_authorization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `data_share_authorization` (
  `authorization_id` int unsigned NOT NULL AUTO_INCREMENT,
  `pet_id` int unsigned NOT NULL,
  `owner_user_id` int unsigned NOT NULL,
  `professional_user_id` int unsigned NOT NULL,
  `scope` varchar(100) NOT NULL,
  `granted_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `expires_at` datetime DEFAULT NULL,
  `revoked_at` datetime DEFAULT NULL,
  PRIMARY KEY (`authorization_id`),
  KEY `fk_data_share_authorization_pet_id` (`pet_id`),
  KEY `fk_data_share_authorization_owner_user_id` (`owner_user_id`),
  KEY `fk_data_share_authorization_professional_user_id` (`professional_user_id`),
  CONSTRAINT `fk_data_share_authorization_owner_user_id` FOREIGN KEY (`owner_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `fk_data_share_authorization_pet_id` FOREIGN KEY (`pet_id`) REFERENCES `pet` (`pet_id`),
  CONSTRAINT `fk_data_share_authorization_professional_user_id` FOREIGN KEY (`professional_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `chk_data_share_authorization_1` CHECK (((`expires_at` is null) or (`expires_at` > `granted_at`)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_share_authorization`
--

LOCK TABLES `data_share_authorization` WRITE;
/*!40000 ALTER TABLE `data_share_authorization` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_share_authorization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `health_article`
--

DROP TABLE IF EXISTS `health_article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `health_article` (
  `article_id` int unsigned NOT NULL AUTO_INCREMENT,
  `author_user_id` int unsigned NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` text NOT NULL,
  `status` varchar(20) NOT NULL,
  `published_at` datetime NOT NULL,
  PRIMARY KEY (`article_id`),
  KEY `fk_health_article_author_user_id` (`author_user_id`),
  CONSTRAINT `fk_health_article_author_user_id` FOREIGN KEY (`author_user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `health_article`
--

LOCK TABLES `health_article` WRITE;
/*!40000 ALTER TABLE `health_article` DISABLE KEYS */;
/*!40000 ALTER TABLE `health_article` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `health_question`
--

DROP TABLE IF EXISTS `health_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `health_question` (
  `question_id` int unsigned NOT NULL AUTO_INCREMENT,
  `asker_user_id` int unsigned NOT NULL,
  `pet_id` int unsigned DEFAULT NULL,
  `directed_to_user_id` int unsigned DEFAULT NULL,
  `question_text` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`question_id`),
  KEY `fk_health_question_asker_user_id` (`asker_user_id`),
  KEY `fk_health_question_pet_id` (`pet_id`),
  KEY `fk_health_question_directed_to_user_id` (`directed_to_user_id`),
  CONSTRAINT `fk_health_question_asker_user_id` FOREIGN KEY (`asker_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `fk_health_question_directed_to_user_id` FOREIGN KEY (`directed_to_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `fk_health_question_pet_id` FOREIGN KEY (`pet_id`) REFERENCES `pet` (`pet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `health_question`
--

LOCK TABLES `health_question` WRITE;
/*!40000 ALTER TABLE `health_question` DISABLE KEYS */;
/*!40000 ALTER TABLE `health_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `health_resource`
--

DROP TABLE IF EXISTS `health_resource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `health_resource` (
  `resource_id` int unsigned NOT NULL AUTO_INCREMENT,
  `author_user_id` int unsigned DEFAULT NULL,
  `title` varchar(200) NOT NULL,
  `resource_type` varchar(30) NOT NULL,
  `body` text NOT NULL,
  `keywords` varchar(500) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`resource_id`),
  KEY `fk_health_resource_author_user_id` (`author_user_id`),
  CONSTRAINT `fk_health_resource_author_user_id` FOREIGN KEY (`author_user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `health_resource`
--

LOCK TABLES `health_resource` WRITE;
/*!40000 ALTER TABLE `health_resource` DISABLE KEYS */;
/*!40000 ALTER TABLE `health_resource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medication_reference`
--

DROP TABLE IF EXISTS `medication_reference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medication_reference` (
  `medication_ref_id` int unsigned NOT NULL AUTO_INCREMENT,
  `medication_code` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `uses` text NOT NULL,
  `dosage_guidance` text NOT NULL,
  `warnings` text NOT NULL,
  `side_effects` text NOT NULL,
  `source` varchar(255) NOT NULL,
  `last_reviewed_at` datetime NOT NULL,
  PRIMARY KEY (`medication_ref_id`),
  UNIQUE KEY `medication_code` (`medication_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medication_reference`
--

LOCK TABLES `medication_reference` WRITE;
/*!40000 ALTER TABLE `medication_reference` DISABLE KEYS */;
/*!40000 ALTER TABLE `medication_reference` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `message_id` int unsigned NOT NULL AUTO_INCREMENT,
  `sender_user_id` int unsigned NOT NULL,
  `recipient_user_id` int unsigned NOT NULL,
  `body` text NOT NULL,
  `sent_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`message_id`),
  KEY `fk_message_sender_user_id` (`sender_user_id`),
  KEY `fk_message_recipient_user_id` (`recipient_user_id`),
  CONSTRAINT `fk_message_recipient_user_id` FOREIGN KEY (`recipient_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `fk_message_sender_user_id` FOREIGN KEY (`sender_user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `moderation_action`
--

DROP TABLE IF EXISTS `moderation_action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `moderation_action` (
  `action_id` int unsigned NOT NULL AUTO_INCREMENT,
  `case_id` int unsigned NOT NULL,
  `actor_user_id` int unsigned NOT NULL,
  `target_user_id` int unsigned DEFAULT NULL,
  `action_type` varchar(30) NOT NULL,
  `reason` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`action_id`),
  KEY `fk_moderation_action_case_id` (`case_id`),
  KEY `fk_moderation_action_actor_user_id` (`actor_user_id`),
  KEY `fk_moderation_action_target_user_id` (`target_user_id`),
  CONSTRAINT `fk_moderation_action_actor_user_id` FOREIGN KEY (`actor_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `fk_moderation_action_case_id` FOREIGN KEY (`case_id`) REFERENCES `moderation_case` (`case_id`),
  CONSTRAINT `fk_moderation_action_target_user_id` FOREIGN KEY (`target_user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moderation_action`
--

LOCK TABLES `moderation_action` WRITE;
/*!40000 ALTER TABLE `moderation_action` DISABLE KEYS */;
/*!40000 ALTER TABLE `moderation_action` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `moderation_case`
--

DROP TABLE IF EXISTS `moderation_case`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `moderation_case` (
  `case_id` int unsigned NOT NULL AUTO_INCREMENT,
  `report_id` int unsigned NOT NULL,
  `assigned_moderator_id` int unsigned DEFAULT NULL,
  `case_status` varchar(20) NOT NULL,
  `opened_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `closed_at` datetime DEFAULT NULL,
  PRIMARY KEY (`case_id`),
  KEY `fk_moderation_case_report_id` (`report_id`),
  KEY `fk_moderation_case_assigned_moderator_id` (`assigned_moderator_id`),
  CONSTRAINT `fk_moderation_case_assigned_moderator_id` FOREIGN KEY (`assigned_moderator_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `fk_moderation_case_report_id` FOREIGN KEY (`report_id`) REFERENCES `report` (`report_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moderation_case`
--

LOCK TABLES `moderation_case` WRITE;
/*!40000 ALTER TABLE `moderation_case` DISABLE KEYS */;
/*!40000 ALTER TABLE `moderation_case` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notification` (
  `notification_id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int unsigned NOT NULL,
  `type` varchar(30) NOT NULL,
  `message` text NOT NULL,
  `is_read` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`notification_id`),
  KEY `fk_notification_user_id` (`user_id`),
  CONSTRAINT `fk_notification_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification`
--

LOCK TABLES `notification` WRITE;
/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permission` (
  `permission_id` int unsigned NOT NULL AUTO_INCREMENT,
  `permission_code` varchar(100) NOT NULL,
  PRIMARY KEY (`permission_id`),
  UNIQUE KEY `permission_code` (`permission_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pet`
--

DROP TABLE IF EXISTS `pet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pet` (
  `pet_id` int unsigned NOT NULL AUTO_INCREMENT,
  `owner_user_id` int unsigned NOT NULL,
  `name` varchar(100) NOT NULL,
  `species` varchar(50) NOT NULL,
  `breed` varchar(100) NOT NULL,
  `birth_date` date NOT NULL,
  `weight` decimal(7,2) NOT NULL,
  PRIMARY KEY (`pet_id`),
  KEY `fk_pet_owner_user_id` (`owner_user_id`),
  CONSTRAINT `fk_pet_owner_user_id` FOREIGN KEY (`owner_user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7380000 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pet`
--

LOCK TABLES `pet` WRITE;
/*!40000 ALTER TABLE `pet` DISABLE KEYS */;
/*!40000 ALTER TABLE `pet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pet_allergy`
--

DROP TABLE IF EXISTS `pet_allergy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pet_allergy` (
  `allergy_id` int unsigned NOT NULL AUTO_INCREMENT,
  `pet_id` int unsigned NOT NULL,
  `allergen` varchar(150) NOT NULL,
  `reaction` text NOT NULL,
  `noted_at` datetime NOT NULL,
  PRIMARY KEY (`allergy_id`),
  KEY `fk_pet_allergy_pet_id` (`pet_id`),
  CONSTRAINT `fk_pet_allergy_pet_id` FOREIGN KEY (`pet_id`) REFERENCES `pet` (`pet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pet_allergy`
--

LOCK TABLES `pet_allergy` WRITE;
/*!40000 ALTER TABLE `pet_allergy` DISABLE KEYS */;
/*!40000 ALTER TABLE `pet_allergy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pet_condition`
--

DROP TABLE IF EXISTS `pet_condition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pet_condition` (
  `condition_id` int unsigned NOT NULL AUTO_INCREMENT,
  `pet_id` int unsigned NOT NULL,
  `condition_name` varchar(150) NOT NULL,
  `diagnosed_at` date NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`condition_id`),
  KEY `fk_pet_condition_pet_id` (`pet_id`),
  CONSTRAINT `fk_pet_condition_pet_id` FOREIGN KEY (`pet_id`) REFERENCES `pet` (`pet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pet_condition`
--

LOCK TABLES `pet_condition` WRITE;
/*!40000 ALTER TABLE `pet_condition` DISABLE KEYS */;
/*!40000 ALTER TABLE `pet_condition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pet_medication`
--

DROP TABLE IF EXISTS `pet_medication`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pet_medication` (
  `pet_medication_id` int unsigned NOT NULL AUTO_INCREMENT,
  `pet_id` int unsigned NOT NULL,
  `medication_ref_id` int unsigned DEFAULT NULL,
  `name` varchar(150) NOT NULL,
  `dosage` varchar(100) NOT NULL,
  `frequency` varchar(100) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  PRIMARY KEY (`pet_medication_id`),
  KEY `fk_pet_medication_pet_id` (`pet_id`),
  KEY `fk_pet_medication_medication_ref_id` (`medication_ref_id`),
  CONSTRAINT `fk_pet_medication_medication_ref_id` FOREIGN KEY (`medication_ref_id`) REFERENCES `medication_reference` (`medication_ref_id`),
  CONSTRAINT `fk_pet_medication_pet_id` FOREIGN KEY (`pet_id`) REFERENCES `pet` (`pet_id`),
  CONSTRAINT `chk_pet_medication_1` CHECK ((`end_date` >= `start_date`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pet_medication`
--

LOCK TABLES `pet_medication` WRITE;
/*!40000 ALTER TABLE `pet_medication` DISABLE KEYS */;
/*!40000 ALTER TABLE `pet_medication` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post` (
  `post_id` int unsigned NOT NULL AUTO_INCREMENT,
  `author_user_id` int unsigned NOT NULL,
  `pet_id` int unsigned DEFAULT NULL,
  `body` text NOT NULL,
  `post_type` varchar(30) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`post_id`),
  KEY `fk_post_author_user_id` (`author_user_id`),
  KEY `fk_post_pet_id` (`pet_id`),
  CONSTRAINT `fk_post_author_user_id` FOREIGN KEY (`author_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `fk_post_pet_id` FOREIGN KEY (`pet_id`) REFERENCES `pet` (`pet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_like`
--

DROP TABLE IF EXISTS `post_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post_like` (
  `user_id` int unsigned NOT NULL,
  `post_id` int unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`,`post_id`),
  KEY `fk_post_like_post_id` (`post_id`),
  CONSTRAINT `fk_post_like_post_id` FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`),
  CONSTRAINT `fk_post_like_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_like`
--

LOCK TABLES `post_like` WRITE;
/*!40000 ALTER TABLE `post_like` DISABLE KEYS */;
/*!40000 ALTER TABLE `post_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_save`
--

DROP TABLE IF EXISTS `post_save`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post_save` (
  `user_id` int unsigned NOT NULL,
  `post_id` int unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`,`post_id`),
  KEY `fk_post_save_post_id` (`post_id`),
  CONSTRAINT `fk_post_save_post_id` FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`),
  CONSTRAINT `fk_post_save_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_save`
--

LOCK TABLES `post_save` WRITE;
/*!40000 ALTER TABLE `post_save` DISABLE KEYS */;
/*!40000 ALTER TABLE `post_save` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_share`
--

DROP TABLE IF EXISTS `post_share`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post_share` (
  `share_id` int unsigned NOT NULL AUTO_INCREMENT,
  `post_id` int unsigned NOT NULL,
  `user_id` int unsigned NOT NULL,
  `shared_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`share_id`),
  KEY `fk_post_share_post_id` (`post_id`),
  KEY `fk_post_share_user_id` (`user_id`),
  CONSTRAINT `fk_post_share_post_id` FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`),
  CONSTRAINT `fk_post_share_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_share`
--

LOCK TABLES `post_share` WRITE;
/*!40000 ALTER TABLE `post_share` DISABLE KEYS */;
/*!40000 ALTER TABLE `post_share` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_tag`
--

DROP TABLE IF EXISTS `post_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post_tag` (
  `post_id` int unsigned NOT NULL,
  `tag_id` int unsigned NOT NULL,
  PRIMARY KEY (`post_id`,`tag_id`),
  KEY `fk_post_tag_tag_id` (`tag_id`),
  CONSTRAINT `fk_post_tag_post_id` FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`),
  CONSTRAINT `fk_post_tag_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_tag`
--

LOCK TABLES `post_tag` WRITE;
/*!40000 ALTER TABLE `post_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `post_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `product_id` int unsigned NOT NULL AUTO_INCREMENT,
  `product_code` varchar(255) NOT NULL,
  `name` varchar(200) NOT NULL,
  `description` text NOT NULL,
  `usage_guidance` text NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`product_id`),
  UNIQUE KEY `product_code` (`product_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_review`
--

DROP TABLE IF EXISTS `product_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_review` (
  `review_id` int unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int unsigned NOT NULL,
  `reviewer_user_id` int unsigned NOT NULL,
  `rating` tinyint unsigned NOT NULL,
  `review_text` text NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`review_id`),
  KEY `fk_product_review_product_id` (`product_id`),
  KEY `fk_product_review_reviewer_user_id` (`reviewer_user_id`),
  CONSTRAINT `fk_product_review_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
  CONSTRAINT `fk_product_review_reviewer_user_id` FOREIGN KEY (`reviewer_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `chk_product_review_1` CHECK ((`rating` between 1 and 5))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_review`
--

LOCK TABLES `product_review` WRITE;
/*!40000 ALTER TABLE `product_review` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `professional_profile`
--

DROP TABLE IF EXISTS `professional_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `professional_profile` (
  `profile_id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int unsigned NOT NULL,
  `professional_type` varchar(30) NOT NULL,
  `credentials` text NOT NULL,
  `specialty` varchar(100) NOT NULL,
  `organization` varchar(255) NOT NULL,
  `experience` text NOT NULL,
  `verification_status` varchar(20) NOT NULL,
  PRIMARY KEY (`profile_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `fk_professional_profile_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `professional_profile`
--

LOCK TABLES `professional_profile` WRITE;
/*!40000 ALTER TABLE `professional_profile` DISABLE KEYS */;
/*!40000 ALTER TABLE `professional_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reminder`
--

DROP TABLE IF EXISTS `reminder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reminder` (
  `reminder_id` int unsigned NOT NULL AUTO_INCREMENT,
  `pet_id` int unsigned NOT NULL,
  `user_id` int unsigned NOT NULL,
  `pet_medication_id` int unsigned DEFAULT NULL,
  `due_at` datetime NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`reminder_id`),
  KEY `fk_reminder_pet_id` (`pet_id`),
  KEY `fk_reminder_user_id` (`user_id`),
  KEY `fk_reminder_pet_medication_id` (`pet_medication_id`),
  CONSTRAINT `fk_reminder_pet_id` FOREIGN KEY (`pet_id`) REFERENCES `pet` (`pet_id`),
  CONSTRAINT `fk_reminder_pet_medication_id` FOREIGN KEY (`pet_medication_id`) REFERENCES `pet_medication` (`pet_medication_id`),
  CONSTRAINT `fk_reminder_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reminder`
--

LOCK TABLES `reminder` WRITE;
/*!40000 ALTER TABLE `reminder` DISABLE KEYS */;
/*!40000 ALTER TABLE `reminder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report` (
  `report_id` int unsigned NOT NULL AUTO_INCREMENT,
  `reporter_user_id` int unsigned NOT NULL,
  `post_id` int unsigned DEFAULT NULL,
  `comment_id` int unsigned DEFAULT NULL,
  `reported_user_id` int unsigned DEFAULT NULL,
  `response_id` int unsigned DEFAULT NULL,
  `product_id` int unsigned DEFAULT NULL,
  `reason` text NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`report_id`),
  KEY `fk_report_reporter_user_id` (`reporter_user_id`),
  KEY `fk_report_post_id` (`post_id`),
  KEY `fk_report_comment_id` (`comment_id`),
  KEY `fk_report_reported_user_id` (`reported_user_id`),
  KEY `fk_report_response_id` (`response_id`),
  KEY `fk_report_product_id` (`product_id`),
  CONSTRAINT `fk_report_comment_id` FOREIGN KEY (`comment_id`) REFERENCES `comment` (`comment_id`),
  CONSTRAINT `fk_report_post_id` FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`),
  CONSTRAINT `fk_report_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
  CONSTRAINT `fk_report_reported_user_id` FOREIGN KEY (`reported_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `fk_report_reporter_user_id` FOREIGN KEY (`reporter_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `fk_report_response_id` FOREIGN KEY (`response_id`) REFERENCES `advice_response` (`response_id`),
  CONSTRAINT `chk_report_1` CHECK (((`post_id` is not null) or (`comment_id` is not null) or (`reported_user_id` is not null) or (`response_id` is not null) or (`product_id` is not null)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report`
--

LOCK TABLES `report` WRITE;
/*!40000 ALTER TABLE `report` DISABLE KEYS */;
/*!40000 ALTER TABLE `report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `role_id` int unsigned NOT NULL AUTO_INCREMENT,
  `role_name` varchar(40) NOT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_permission`
--

DROP TABLE IF EXISTS `role_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_permission` (
  `role_id` int unsigned NOT NULL,
  `permission_id` int unsigned NOT NULL,
  PRIMARY KEY (`role_id`,`permission_id`),
  KEY `fk_role_permission_permission_id` (`permission_id`),
  CONSTRAINT `fk_role_permission_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`permission_id`),
  CONSTRAINT `fk_role_permission_role_id` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_permission`
--

LOCK TABLES `role_permission` WRITE;
/*!40000 ALTER TABLE `role_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `role_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `symptom_log`
--

DROP TABLE IF EXISTS `symptom_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `symptom_log` (
  `symptom_id` int unsigned NOT NULL AUTO_INCREMENT,
  `pet_id` int unsigned NOT NULL,
  `symptom` varchar(255) NOT NULL,
  `severity` varchar(20) NOT NULL,
  `observed_at` datetime NOT NULL,
  `notes` text NOT NULL,
  PRIMARY KEY (`symptom_id`),
  KEY `fk_symptom_log_pet_id` (`pet_id`),
  CONSTRAINT `fk_symptom_log_pet_id` FOREIGN KEY (`pet_id`) REFERENCES `pet` (`pet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `symptom_log`
--

LOCK TABLES `symptom_log` WRITE;
/*!40000 ALTER TABLE `symptom_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `symptom_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_setting`
--

DROP TABLE IF EXISTS `system_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_setting` (
  `setting_id` int unsigned NOT NULL AUTO_INCREMENT,
  `setting_key` varchar(100) NOT NULL,
  `setting_value` text NOT NULL,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by_user_id` int unsigned NOT NULL,
  PRIMARY KEY (`setting_id`),
  UNIQUE KEY `setting_key` (`setting_key`),
  KEY `fk_system_setting_updated_by_user_id` (`updated_by_user_id`),
  CONSTRAINT `fk_system_setting_updated_by_user_id` FOREIGN KEY (`updated_by_user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_setting`
--

LOCK TABLES `system_setting` WRITE;
/*!40000 ALTER TABLE `system_setting` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_setting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tag` (
  `tag_id` int unsigned NOT NULL AUTO_INCREMENT,
  `tag_name` varchar(80) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`tag_id`),
  UNIQUE KEY `tag_name` (`tag_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag`
--

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `treatment`
--

DROP TABLE IF EXISTS `treatment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `treatment` (
  `treatment_id` int unsigned NOT NULL AUTO_INCREMENT,
  `pet_id` int unsigned NOT NULL,
  `professional_user_id` int unsigned DEFAULT NULL,
  `description` text NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  PRIMARY KEY (`treatment_id`),
  KEY `fk_treatment_pet_id` (`pet_id`),
  KEY `fk_treatment_professional_user_id` (`professional_user_id`),
  CONSTRAINT `fk_treatment_pet_id` FOREIGN KEY (`pet_id`) REFERENCES `pet` (`pet_id`),
  CONSTRAINT `fk_treatment_professional_user_id` FOREIGN KEY (`professional_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `chk_treatment_1` CHECK ((`end_date` >= `start_date`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `treatment`
--

LOCK TABLES `treatment` WRITE;
/*!40000 ALTER TABLE `treatment` DISABLE KEYS */;
/*!40000 ALTER TABLE `treatment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `account_status` varchar(30) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=87370000 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_follow`
--

DROP TABLE IF EXISTS `user_follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_follow` (
  `follower_user_id` int unsigned NOT NULL,
  `followed_user_id` int unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`follower_user_id`,`followed_user_id`),
  KEY `fk_user_follow_followed_user_id` (`followed_user_id`),
  CONSTRAINT `fk_user_follow_followed_user_id` FOREIGN KEY (`followed_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `fk_user_follow_follower_user_id` FOREIGN KEY (`follower_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `chk_user_follow_1` CHECK ((`follower_user_id` <> `followed_user_id`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_follow`
--

LOCK TABLES `user_follow` WRITE;
/*!40000 ALTER TABLE `user_follow` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_follow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_restriction`
--

DROP TABLE IF EXISTS `user_restriction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_restriction` (
  `restriction_id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int unsigned NOT NULL,
  `action_id` int unsigned NOT NULL,
  `starts_at` datetime NOT NULL,
  `ends_at` datetime NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`restriction_id`),
  KEY `fk_user_restriction_user_id` (`user_id`),
  KEY `fk_user_restriction_action_id` (`action_id`),
  CONSTRAINT `fk_user_restriction_action_id` FOREIGN KEY (`action_id`) REFERENCES `moderation_action` (`action_id`),
  CONSTRAINT `fk_user_restriction_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `chk_user_restriction_1` CHECK ((`ends_at` > `starts_at`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_restriction`
--

LOCK TABLES `user_restriction` WRITE;
/*!40000 ALTER TABLE `user_restriction` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_restriction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_role`
--

DROP TABLE IF EXISTS `user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_role` (
  `user_id` int unsigned NOT NULL,
  `role_id` int unsigned NOT NULL,
  `assigned_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`,`role_id`),
  KEY `fk_user_role_role_id` (`role_id`),
  CONSTRAINT `fk_user_role_role_id` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`),
  CONSTRAINT `fk_user_role_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_role`
--

LOCK TABLES `user_role` WRITE;
/*!40000 ALTER TABLE `user_role` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `verification_review`
--

DROP TABLE IF EXISTS `verification_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `verification_review` (
  `review_id` int unsigned NOT NULL AUTO_INCREMENT,
  `profile_id` int unsigned NOT NULL,
  `admin_user_id` int unsigned NOT NULL,
  `decision` varchar(20) NOT NULL,
  `reviewed_at` datetime NOT NULL,
  `notes` text NOT NULL,
  PRIMARY KEY (`review_id`),
  KEY `fk_verification_review_profile_id` (`profile_id`),
  KEY `fk_verification_review_admin_user_id` (`admin_user_id`),
  CONSTRAINT `fk_verification_review_admin_user_id` FOREIGN KEY (`admin_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `fk_verification_review_profile_id` FOREIGN KEY (`profile_id`) REFERENCES `professional_profile` (`profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `verification_review`
--

LOCK TABLES `verification_review` WRITE;
/*!40000 ALTER TABLE `verification_review` DISABLE KEYS */;
/*!40000 ALTER TABLE `verification_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vet_referral`
--

DROP TABLE IF EXISTS `vet_referral`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vet_referral` (
  `referral_id` int unsigned NOT NULL AUTO_INCREMENT,
  `pet_id` int unsigned NOT NULL,
  `vet_user_id` int unsigned NOT NULL,
  `reason` text NOT NULL,
  `urgency` varchar(20) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`referral_id`),
  KEY `fk_vet_referral_pet_id` (`pet_id`),
  KEY `fk_vet_referral_vet_user_id` (`vet_user_id`),
  CONSTRAINT `fk_vet_referral_pet_id` FOREIGN KEY (`pet_id`) REFERENCES `pet` (`pet_id`),
  CONSTRAINT `fk_vet_referral_vet_user_id` FOREIGN KEY (`vet_user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vet_referral`
--

LOCK TABLES `vet_referral` WRITE;
/*!40000 ALTER TABLE `vet_referral` DISABLE KEYS */;
/*!40000 ALTER TABLE `vet_referral` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-29  8:11:37
