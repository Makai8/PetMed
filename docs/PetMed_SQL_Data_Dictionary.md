# PetMed: SQL Data Dictionary

This documents the database as it is built in MySQL by [`backend/PetMedDB.sql`](../backend/PetMedDB.sql): 41 tables, 69 foreign keys and 8 business-rule checks. Types, keys and defaults are taken directly from the SQL.

**Database:** `petmed` · **Engine:** InnoDB · **Character set:** utf8mb4 · **Requires:** MySQL 8.0.16+

**Key legend:** PK = primary key · FK = foreign key (→ table it references) · UQ = unique · PK, FK = part of a two-column primary key on a link table

> On Windows, MySQL shows table names in lowercase (`user`, `pet`). Names below use the casing from the schema file.

## Contents

- **USER (Accounts & Access):** [User](#user), [Role](#role), [Permission](#permission), [User_Role](#user_role), [Role_Permission](#role_permission), [Professional_Profile](#professional_profile), [User_Restriction](#user_restriction), [Notification](#notification), [Message](#message), [Verification_Review](#verification_review)
- **Pet Health:** [Pet](#pet), [Treatment](#treatment), [Pet_Allergy](#pet_allergy), [Reminder](#reminder), [Pet_Condition](#pet_condition), [Data_Share_Authorization](#data_share_authorization), [Symptom_Log](#symptom_log), [Vet_Referral](#vet_referral), [Pet_Medication](#pet_medication)
- **Catalog & Reference:** [Product](#product), [Health_Resource](#health_resource), [Medication_Reference](#medication_reference), [Product_Review](#product_review)
- **Moderation & Oversight:** [Report](#report), [Moderation_Case](#moderation_case), [System_Setting](#system_setting), [Audit_Event](#audit_event), [Moderation_Action](#moderation_action)
- **Community & Advice:** [Post](#post), [Tag](#tag), [Health_Article](#health_article), [Health_Question](#health_question), [Comment](#comment), [Post_Like](#post_like), [Post_Save](#post_save), [Post_Share](#post_share), [Post_Tag](#post_tag), [User_Follow](#user_follow), [Article_Tag](#article_tag), [Advice_Response](#advice_response), [Advice_Review](#advice_review)

## ID numbering

| Table | First ID | Why |
|---|---|---|
| `User` | 87370000 | U-S-E-R on a phone keypad = 8-7-3-7 |
| `Pet` | 7380000 | P-E-T on a phone keypad = 7-3-8 |
| All other tables | 1 | MySQL default |

---

## USER (Accounts & Access)

### User

Stores the account for each person using PetMed.

**IDs start at:** 87370000

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `user_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique identifier for a user. |
| `email` | VARCHAR(255) | No | UQ |  | User's email/login address. |
| `password_hash` | VARCHAR(255) | No |  |  | Secure password hash; never store a plaintext password. |
| `full_name` | VARCHAR(255) | No |  |  | User's full name. |
| `account_status` | VARCHAR(30) | No |  |  | Current account state, e.g. active, suspended, deactivated. |
| `created_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date and time the account was created. |

**Referenced by:** `Advice_Response`, `Advice_Review`, `Audit_Event`, `Comment`, `Data_Share_Authorization`, `Health_Article`, `Health_Question`, `Health_Resource`, `Message`, `Moderation_Action`, `Moderation_Case`, `Notification`, `Pet`, `Post`, `Post_Like`, `Post_Save`, `Post_Share`, `Product_Review`, `Professional_Profile`, `Reminder`, `Report`, `System_Setting`, `Treatment`, `User_Follow`, `User_Restriction`, `User_Role`, `Verification_Review`, `Vet_Referral`

### Role

Defines the role assigned to a user.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `role_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique identifier for a role. |
| `role_name` | VARCHAR(40) | No | UQ |  | Unique role name. |

**Referenced by:** `Role_Permission`, `User_Role`

### Permission

Defines an application permission.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `permission_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique identifier for a permission. |
| `permission_code` | VARCHAR(100) | No | UQ |  | Unique machine-readable permission name. |

**Referenced by:** `Role_Permission`

### User_Role

Associates users with roles; resolves the many-to-many relationship so a user can hold more than one role.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `user_id` | INT UNSIGNED | No | PK, FK → User.user_id |  | User receiving the role. |
| `role_id` | INT UNSIGNED | No | PK, FK → Role.role_id |  | Role assigned to the user. |
| `assigned_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date and time the role was assigned. |

**Rules enforced by the database:**
- Primary key is the pair (user_id, role_id), so the same link can't be stored twice.

### Role_Permission

Associates roles with permissions; resolves the many-to-many relationship.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `role_id` | INT UNSIGNED | No | PK, FK → Role.role_id |  | Role receiving the permission. |
| `permission_id` | INT UNSIGNED | No | PK, FK → Permission.permission_id |  | Permission assigned to the role. |

**Rules enforced by the database:**
- Primary key is the pair (role_id, permission_id), so the same link can't be stored twice.

### Professional_Profile

Stores professional credentials and verification details for a veterinarian or pet health expert.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `profile_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique professional profile identifier. |
| `user_id` | INT UNSIGNED | No | FK → User.user_id, UQ |  | User who owns this profile. |
| `professional_type` | VARCHAR(30) | No |  |  | Kind of professional: veterinarian or pet health expert. |
| `credentials` | TEXT | No |  |  | Description of qualifications or credentials. |
| `specialty` | VARCHAR(100) | No |  |  | Professional specialty or area of expertise. |
| `organization` | VARCHAR(255) | No |  |  | Clinic, practice or organization the professional works for. |
| `experience` | TEXT | No |  |  | Summary of professional experience. |
| `verification_status` | VARCHAR(20) | No |  |  | Administrative verification state. |

**Referenced by:** `Verification_Review`

### User_Restriction

Stores warnings, suspensions, and other limits placed on a user as the result of a moderation action.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `restriction_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique restriction identifier. |
| `user_id` | INT UNSIGNED | No | FK → User.user_id |  | User who is restricted. |
| `action_id` | INT UNSIGNED | No | FK → Moderation_Action.action_id |  | Moderation action that created the restriction. |
| `starts_at` | DATETIME | No |  |  | Date and time the restriction begins. |
| `ends_at` | DATETIME | No |  |  | Date and time the restriction ends. |
| `status` | VARCHAR(20) | No |  |  | Current restriction state. |

**Rules enforced by the database:**
- A restriction must end after it starts.

### Notification

Stores a notification delivered to a PetMed user.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `notification_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique identifier for a notification. |
| `user_id` | INT UNSIGNED | No | FK → User.user_id |  | User who receives the notification. |
| `type` | VARCHAR(30) | No |  |  | Kind of notification, e.g. comment, reminder, message. |
| `message` | TEXT | No |  |  | Text shown in the notification. |
| `is_read` | BOOLEAN | No |  | DEFAULT FALSE | Whether the recipient has read the notification. |
| `created_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date and time the notification was created. |

### Message

Stores a message sent from one user to another.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `message_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique identifier for a message. |
| `sender_user_id` | INT UNSIGNED | No | FK → User.user_id |  | User who sent the message. |
| `recipient_user_id` | INT UNSIGNED | No | FK → User.user_id |  | User who receives the message. |
| `body` | TEXT | No |  |  | Text content of the message. |
| `sent_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date and time the message was sent. |

### Verification_Review

Records each administrator decision on a professional profile, keeping a history of verification reviews.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `review_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique verification review identifier. |
| `profile_id` | INT UNSIGNED | No | FK → Professional_Profile.profile_id |  | Professional profile being reviewed. |
| `admin_user_id` | INT UNSIGNED | No | FK → User.user_id |  | Administrator who made the decision. |
| `decision` | VARCHAR(20) | No |  |  | Outcome of the review. |
| `reviewed_at` | DATETIME | No |  |  | Date and time the decision was made. |
| `notes` | TEXT | No |  |  | Reason or comments supporting the decision. |

---

## Pet Health

### Pet

Stores each pet profile; each pet is owned by one user.

**IDs start at:** 7380000

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `pet_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique identifier for a pet. |
| `owner_user_id` | INT UNSIGNED | No | FK → User.user_id |  | Pet Owner the pet belongs to. |
| `name` | VARCHAR(100) | No |  |  | Pet's name. |
| `species` | VARCHAR(50) | No |  |  | Animal species. |
| `breed` | VARCHAR(100) | No |  |  | Pet's breed, if known. |
| `birth_date` | DATE | No |  |  | Pet's date of birth, if known. |
| `weight` | DECIMAL(7,2) | No |  |  | Pet's weight. |

**Referenced by:** `Data_Share_Authorization`, `Health_Question`, `Pet_Allergy`, `Pet_Condition`, `Pet_Medication`, `Post`, `Reminder`, `Symptom_Log`, `Treatment`, `Vet_Referral`

### Treatment

Stores a treatment or care plan for a pet.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `treatment_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique treatment identifier. |
| `pet_id` | INT UNSIGNED | No | FK → Pet.pet_id |  | Pet receiving the treatment. |
| `professional_user_id` | INT UNSIGNED | Yes | FK → User.user_id |  | Professional who prescribed or recommended the treatment, if any. |
| `description` | TEXT | No |  |  | Treatment instructions/details. |
| `start_date` | DATE | No |  |  | Treatment start date. |
| `end_date` | DATE | No |  |  | Treatment end date. |

**Rules enforced by the database:**
- End date cannot be before the start date.

### Pet_Allergy

Stores a pet's allergy information.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `allergy_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique allergy record identifier. |
| `pet_id` | INT UNSIGNED | No | FK → Pet.pet_id |  | Pet with the allergy. |
| `allergen` | VARCHAR(150) | No |  |  | Substance causing the allergy. |
| `reaction` | TEXT | No |  |  | Observed reaction to the allergen. |
| `noted_at` | DATETIME | No |  |  | Date and time the allergy was recorded. |

### Reminder

Stores a scheduled reminder for an owner, optionally linked to a medication.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `reminder_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique reminder identifier. |
| `pet_id` | INT UNSIGNED | No | FK → Pet.pet_id |  | Pet the reminder concerns. |
| `user_id` | INT UNSIGNED | No | FK → User.user_id |  | User who receives the reminder (normally the pet owner). |
| `pet_medication_id` | INT UNSIGNED | Yes | FK → Pet_Medication.pet_medication_id |  | Related pet medication, if applicable. |
| `due_at` | DATETIME | No |  |  | Date and time the reminder is due. |
| `status` | VARCHAR(20) | No |  |  | Current reminder state. |

### Pet_Condition

Stores a pet's health condition.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `condition_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique condition record identifier. |
| `pet_id` | INT UNSIGNED | No | FK → Pet.pet_id |  | Pet associated with the condition. |
| `condition_name` | VARCHAR(150) | No |  |  | Name of the condition. |
| `diagnosed_at` | DATE | No |  |  | Date the condition was diagnosed. |
| `status` | VARCHAR(20) | No |  |  | Current condition state. |

### Data_Share_Authorization

Records an owner's permission for a professional to access a pet's data.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `authorization_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique authorization identifier. |
| `pet_id` | INT UNSIGNED | No | FK → Pet.pet_id |  | Pet whose information may be shared. |
| `owner_user_id` | INT UNSIGNED | No | FK → User.user_id |  | Pet Owner who granted access. |
| `professional_user_id` | INT UNSIGNED | No | FK → User.user_id |  | Professional who is allowed to view the records. |
| `scope` | VARCHAR(100) | No |  |  | Defines which data may be viewed. |
| `granted_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date/time permission was granted. |
| `expires_at` | DATETIME | Yes |  |  | Optional date/time permission expires. |
| `revoked_at` | DATETIME | Yes |  |  | Date/time permission was revoked. |

**Rules enforced by the database:**
- If set, the expiry must be after the grant time.

### Symptom_Log

Records symptoms observed for a pet.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `symptom_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique symptom-log entry identifier. |
| `pet_id` | INT UNSIGNED | No | FK → Pet.pet_id |  | Pet associated with the symptom. |
| `symptom` | VARCHAR(255) | No |  |  | Description/name of the symptom. |
| `severity` | VARCHAR(20) | No |  |  | Reported severity of the symptom. |
| `observed_at` | DATETIME | No |  |  | When the symptom was observed. |
| `notes` | TEXT | No |  |  | Additional symptom details. |

### Vet_Referral

Records a recommendation for a pet to receive in-person veterinary care.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `referral_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique referral identifier. |
| `pet_id` | INT UNSIGNED | No | FK → Pet.pet_id |  | Pet being referred. |
| `vet_user_id` | INT UNSIGNED | No | FK → User.user_id |  | Veterinarian who made the referral. |
| `reason` | TEXT | No |  |  | Reason for the referral. |
| `urgency` | VARCHAR(20) | No |  |  | Urgency level of the referral. |
| `created_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date/time referral was created. |

### Pet_Medication

Stores medications a pet is taking, with dosage and schedule; optionally linked to a medication reference entry.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `pet_medication_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique pet medication record identifier. |
| `pet_id` | INT UNSIGNED | No | FK → Pet.pet_id |  | Pet taking the medication. |
| `medication_ref_id` | INT UNSIGNED | Yes | FK → Medication_Reference.medication_ref_id |  | Related medication reference entry, when one exists. |
| `name` | VARCHAR(150) | No |  |  | Medication name as entered by the owner. |
| `dosage` | VARCHAR(100) | No |  |  | Dose amount and unit. |
| `frequency` | VARCHAR(100) | No |  |  | How often the medication is given. |
| `start_date` | DATE | No |  |  | Medication start date. |
| `end_date` | DATE | No |  |  | Medication end date. |

**Rules enforced by the database:**
- End date cannot be before the start date.

**Referenced by:** `Reminder`

---

## Catalog & Reference

### Product

Stores a product listing in the catalog.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `product_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique product identifier. |
| `product_code` | VARCHAR(255) | No | UQ |  | Unique product code. |
| `name` | VARCHAR(200) | No |  |  | Product name. |
| `description` | TEXT | No |  |  | Product details. |
| `usage_guidance` | TEXT | No |  |  | How the product should be used. |
| `is_active` | BOOLEAN | No |  | DEFAULT TRUE | Whether the listing is active/visible. |

**Referenced by:** `Product_Review`, `Report`

### Health_Resource

Stores searchable pet-health reference material such as guides, FAQs, and condition overviews.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `resource_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique health resource identifier. |
| `author_user_id` | INT UNSIGNED | Yes | FK → User.user_id |  | User who wrote the resource, if any. |
| `title` | VARCHAR(200) | No |  |  | Resource title. |
| `resource_type` | VARCHAR(30) | No |  |  | Category of resource. |
| `body` | TEXT | No |  |  | Main content of the resource. |
| `keywords` | VARCHAR(500) | No |  |  | Search terms for the resource. |
| `is_active` | BOOLEAN | No |  | DEFAULT TRUE | Whether the resource is visible. |

### Medication_Reference

Stores reference information about medications.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `medication_ref_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique medication reference identifier. |
| `medication_code` | VARCHAR(255) | No | UQ |  | Unique medication code. |
| `name` | VARCHAR(255) | No |  |  | Medication name. |
| `uses` | TEXT | No |  |  | What the medication is used for. |
| `dosage_guidance` | TEXT | No |  |  | General dosage guidance. |
| `warnings` | TEXT | No |  |  | Warnings and safety information. |
| `side_effects` | TEXT | No |  |  | Known side effects. |
| `source` | VARCHAR(255) | No |  |  | Source of the reference information. |
| `last_reviewed_at` | DATETIME | No |  |  | Date and time the reference was last reviewed. |

**Referenced by:** `Pet_Medication`

### Product_Review

Stores a user's review of a product.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `review_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique product-review identifier. |
| `product_id` | INT UNSIGNED | No | FK → Product.product_id |  | Product being reviewed. |
| `reviewer_user_id` | INT UNSIGNED | No | FK → User.user_id |  | User who wrote the review. |
| `rating` | TINYINT UNSIGNED | No |  |  | Numeric rating given to the product. |
| `review_text` | TEXT | No |  |  | Review details. |
| `is_active` | BOOLEAN | No |  | DEFAULT TRUE | Whether the review is visible. |
| `created_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date/time review was created. |

**Rules enforced by the database:**
- Rating must be a whole number from 1 to 5.

---

## Moderation & Oversight

### Report

Stores a report a user submits about a post, comment, user, advice response or product.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `report_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique report identifier. |
| `reporter_user_id` | INT UNSIGNED | No | FK → User.user_id |  | User who submitted the report. |
| `post_id` | INT UNSIGNED | Yes | FK → Post.post_id |  | Reported post, if the report targets a post. |
| `comment_id` | INT UNSIGNED | Yes | FK → Comment.comment_id |  | Reported comment, if the report targets a comment. |
| `reported_user_id` | INT UNSIGNED | Yes | FK → User.user_id |  | Reported user, if the report targets a user. |
| `response_id` | INT UNSIGNED | Yes | FK → Advice_Response.response_id |  | Reported advice response, if the report targets advice. |
| `product_id` | INT UNSIGNED | Yes | FK → Product.product_id |  | Reported product, if the report targets a product. |
| `reason` | TEXT | No |  |  | Reason the content was reported. |
| `status` | VARCHAR(20) | No |  |  | Current report state. |
| `created_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date/time report was created. |

**Rules enforced by the database:**
- A report must point at something: a post, comment, user, advice response or product.

**Referenced by:** `Moderation_Case`

### Moderation_Case

Tracks moderator/admin review of a report.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `case_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique moderation case identifier. |
| `report_id` | INT UNSIGNED | No | FK → Report.report_id |  | Report associated with this case. |
| `assigned_moderator_id` | INT UNSIGNED | Yes | FK → User.user_id |  | Moderator assigned to the case, if any. |
| `case_status` | VARCHAR(20) | No |  |  | Current case state. |
| `opened_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date/time case was opened. |
| `closed_at` | DATETIME | Yes |  |  | Date/time case was closed. |

**Referenced by:** `Moderation_Action`

### System_Setting

Stores configurable application settings.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `setting_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique system setting identifier. |
| `setting_key` | VARCHAR(100) | No | UQ |  | Unique setting name/key. |
| `setting_value` | TEXT | No |  |  | Configured value for the setting. |
| `updated_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date/time setting was last updated. |
| `updated_by_user_id` | INT UNSIGNED | No | FK → User.user_id |  | Administrator who last changed the setting. |

### Audit_Event

Keeps a permanent log of important system actions for accountability.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `audit_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique audit event identifier. |
| `actor_user_id` | INT UNSIGNED | No | FK → User.user_id |  | User who performed the action. |
| `event_type` | VARCHAR(50) | No |  |  | Type of action performed. |
| `entity_name` | VARCHAR(50) | No |  |  | Table affected by the action. |
| `entity_id` | INT UNSIGNED | No |  |  | Identifier of the affected record. |
| `occurred_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date and time the action occurred. |

### Moderation_Action

Records an action taken in response to a moderation case.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `action_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique moderation action identifier. |
| `case_id` | INT UNSIGNED | No | FK → Moderation_Case.case_id |  | Case the action belongs to. |
| `actor_user_id` | INT UNSIGNED | No | FK → User.user_id |  | Moderator or administrator who took the action. |
| `target_user_id` | INT UNSIGNED | Yes | FK → User.user_id |  | User the action applies to, if any. |
| `action_type` | VARCHAR(30) | No |  |  | Type of moderation action. |
| `reason` | TEXT | No |  |  | Reason for the action. |
| `created_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date/time action was taken. |

**Referenced by:** `User_Restriction`

---

## Community & Advice

### Post

Stores a community post created by a user.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `post_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique post identifier. |
| `author_user_id` | INT UNSIGNED | No | FK → User.user_id |  | User who wrote the post. |
| `pet_id` | INT UNSIGNED | Yes | FK → Pet.pet_id |  | Pet the post is about, if any. |
| `body` | TEXT | No |  |  | Post content. |
| `post_type` | VARCHAR(30) | No |  |  | Kind of post, e.g. question, experience, photo, product. |
| `status` | VARCHAR(20) | No |  |  | Publication/moderation state. |
| `created_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date/time post was created. |

**Referenced by:** `Comment`, `Post_Like`, `Post_Save`, `Post_Share`, `Post_Tag`, `Report`

### Tag

Stores a reusable tag that can be attached to posts or articles.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `tag_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique tag identifier. |
| `tag_name` | VARCHAR(80) | No | UQ |  | Unique tag label. |
| `is_active` | BOOLEAN | No |  | DEFAULT TRUE | Whether the tag can still be used. |

**Referenced by:** `Article_Tag`, `Post_Tag`

### Health_Article

Stores searchable health information articles.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `article_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique article identifier. |
| `author_user_id` | INT UNSIGNED | No | FK → User.user_id |  | Verified professional who wrote the article. |
| `title` | VARCHAR(200) | No |  |  | Article title. |
| `content` | TEXT | No |  |  | Body of the article. |
| `status` | VARCHAR(20) | No |  |  | Article publication state. |
| `published_at` | DATETIME | No |  |  | Date/time article was published. |

**Referenced by:** `Article_Tag`

### Health_Question

Stores a health question submitted by a user, optionally about a pet.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `question_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique question identifier. |
| `asker_user_id` | INT UNSIGNED | No | FK → User.user_id |  | User who asked the question. |
| `pet_id` | INT UNSIGNED | Yes | FK → Pet.pet_id |  | Pet related to the question, if applicable. |
| `directed_to_user_id` | INT UNSIGNED | Yes | FK → User.user_id |  | Professional the question is addressed to, if any. |
| `question_text` | TEXT | No |  |  | Text of the question. |
| `created_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date/time question was submitted. |

**Referenced by:** `Advice_Response`

### Comment

Stores a comment on a post; parent_comment_id supports nested replies.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `comment_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique comment identifier. |
| `post_id` | INT UNSIGNED | No | FK → Post.post_id |  | Post the comment belongs to. |
| `author_user_id` | INT UNSIGNED | No | FK → User.user_id |  | User who wrote the comment. |
| `parent_comment_id` | INT UNSIGNED | Yes | FK → Comment.comment_id |  | Parent comment for a reply, if any. |
| `body` | TEXT | No |  |  | Comment text. |
| `created_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date/time comment was created. |

**Referenced by:** `Comment`, `Report`

### Post_Like

Records a user's like on a post.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `user_id` | INT UNSIGNED | No | PK, FK → User.user_id |  | User who liked the post. |
| `post_id` | INT UNSIGNED | No | PK, FK → Post.post_id |  | Post that was liked. |
| `created_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date/time the like was recorded. |

**Rules enforced by the database:**
- Primary key is the pair (user_id, post_id), so the same link can't be stored twice.

### Post_Save

Records a user's saved/bookmarked post.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `user_id` | INT UNSIGNED | No | PK, FK → User.user_id |  | User who saved the post. |
| `post_id` | INT UNSIGNED | No | PK, FK → Post.post_id |  | Post that was saved. |
| `created_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date/time the post was saved. |

**Rules enforced by the database:**
- Primary key is the pair (user_id, post_id), so the same link can't be stored twice.

### Post_Share

Records each time a user shares a community post.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `share_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique share identifier. |
| `post_id` | INT UNSIGNED | No | FK → Post.post_id |  | Post that was shared. |
| `user_id` | INT UNSIGNED | No | FK → User.user_id |  | User who shared the post. |
| `shared_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date and time the post was shared. |

### Post_Tag

Associates posts with tags (many-to-many).

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `post_id` | INT UNSIGNED | No | PK, FK → Post.post_id |  | Post associated with the tag. |
| `tag_id` | INT UNSIGNED | No | PK, FK → Tag.tag_id |  | Tag assigned to the post. |

**Rules enforced by the database:**
- Primary key is the pair (post_id, tag_id), so the same link can't be stored twice.

### User_Follow

Records one user following another user.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `follower_user_id` | INT UNSIGNED | No | PK, FK → User.user_id |  | User who is following. |
| `followed_user_id` | INT UNSIGNED | No | PK, FK → User.user_id |  | User being followed. |
| `created_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date/time the follow was created. |

**Rules enforced by the database:**
- A user cannot follow themselves.
- Primary key is the pair (follower_user_id, followed_user_id), so the same link can't be stored twice.

### Article_Tag

Associates health articles with tags (many-to-many).

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `article_id` | INT UNSIGNED | No | PK, FK → Health_Article.article_id |  | Article associated with the tag. |
| `tag_id` | INT UNSIGNED | No | PK, FK → Tag.tag_id |  | Tag assigned to the article. |

**Rules enforced by the database:**
- Primary key is the pair (article_id, tag_id), so the same link can't be stored twice.

### Advice_Response

Stores an answer to a health question and labels its source.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `response_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique response identifier. |
| `question_id` | INT UNSIGNED | No | FK → Health_Question.question_id |  | Question being answered. |
| `author_user_id` | INT UNSIGNED | No | FK → User.user_id |  | User who wrote the response. |
| `source_type` | VARCHAR(20) | No |  |  | Labels the response source/role. |
| `response_text` | TEXT | No |  |  | Text of the advice. |
| `created_at` | DATETIME | No |  | DEFAULT CURRENT_TIMESTAMP | Date/time response was submitted. |

**Referenced by:** `Advice_Review`, `Report`

### Advice_Review

Stores a user's rating and feedback on an advice response.

| Column | Type | Null | Key | Default / Extra | Description |
|---|---|---|---|---|---|
| `review_id` | INT UNSIGNED | No | PK | AUTO_INCREMENT | Unique advice review identifier. |
| `response_id` | INT UNSIGNED | No | FK → Advice_Response.response_id |  | Advice response being reviewed. |
| `reviewer_user_id` | INT UNSIGNED | No | FK → User.user_id |  | User who wrote the review. |
| `rating` | TINYINT UNSIGNED | No |  |  | Rating given to the advice. |
| `feedback` | TEXT | No |  |  | Written feedback on the advice. |

**Rules enforced by the database:**
- Rating must be a whole number from 1 to 5.
- Each (response_id, reviewer_user_id) pair must be unique.

---

## Checking it against your database

Run these at the `mysql>` prompt (`mysql --login-path=petmed petmed`):

```sql
SHOW TABLES;                 -- 41 tables
DESCRIBE pet;                -- columns of one table
SHOW CREATE TABLE user;      -- full definition, including keys and AUTO_INCREMENT
SELECT COUNT(*) FROM information_schema.referential_constraints WHERE constraint_schema = 'petmed';  -- 69
```
