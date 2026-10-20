# PetMed Sprint 2: Requirements and Sprint 1 UI Review

Prepared by: David Jean-Charles Bahidika
Sprint 2, Section 1: Review Functional Requirements and Sprint 1 UI

## Purpose

The database has to serve the whole PetMed system, not only the screens built in Sprint 1. This review connects the two. It walks through every functional requirement, lists the data each Sprint 1 screen shows or collects, and combines both into one master list of data the system must store. That master list is the foundation for the ERD, the data dictionary, and the business rules.

## 1. Requirements Reviewed

The full Functional Requirements document was reviewed for all five roles, not only the use cases selected in Sprint 1.

* **All Roles:** account registration, sign in and sign out, profile management, notifications, messaging
* **Pet Owner:** manage pet profiles, create community posts, browse and interact with the feed, track symptoms and health events, manage medications and reminders, ask for health advice, search health information, review product and treatment information, rate and review advice or products
* **Veterinarian:** review pet health questions, provide general veterinary guidance, publish educational content, review symptom history, review medication information, refer owners to in person care, participate in professional discussion, report unsafe advice
* **Pet Health Expert:** manage expertise profile, answer specialty questions, publish educational content, recommend wellness resources, review product feedback, participate in community discussion, flag out of scope health concerns, report unsafe or misleading content
* **Community Moderator:** review reported posts, review reported advice, moderate comments and discussions, review reported users, manage moderation cases, warn or restrict users, escalate professional or safety concerns
* **Administrator:** manage user accounts, verify professional accounts, manage roles and permissions, manage health categories and tags, manage product and medication information, manage platform content, manage reported activity, generate analytics and reports, manage system configuration

### Additional System Requirements

Each of these shapes the database directly:

* **Multiple pets per owner:** one owner links to many pets.
* **Detailed pet profiles:** species, breed, age, weight, allergies, conditions, and medications are stored per pet, with allergies and conditions kept as separate records so a pet can have many of each.
* **Symptom tracking over time:** each symptom is its own dated entry, so history can be reviewed as a timeline.
* **Medication and treatment reminders:** reminders are scheduled records tied to a pet and, when relevant, to a medication.
* **Community feed:** posts, comments, likes, saves, shares, and follows are each stored, so every interaction is tracked.
* **Verified professional badges:** professional profiles carry a verification status set by an Administrator.
* **Advice source labels:** every advice response is stored with its source type: Community Advice, Pet Health Expert Guidance, or Veterinarian Guidance.
* **Searchable health content:** posts, articles, and health resources are linked to categories and tags.
* **Product listings:** products are informational listings with user reviews.
* **Notifications:** each notification belongs to one user and records whether it has been read.

## 2. Data Shown or Collected by Each Sprint 1 Screen

### Sign In and Account Screens

* **Sign In:** email and password. The user's role is identified after sign in, so the screen has no role picker.
* **Registration:** display name, email, password, and account type. Veterinarians and Pet Health Experts also submit license number, specialty, and credentials for verification.
* **Forgot Password:** the email address of the account to recover.

### Role Landing Screens

* **Pet Owner:** the owner's pets, upcoming reminders, recent symptom entries, community feed, and notifications.
* **Veterinarian:** open health questions, pets shared through owner authorization, referrals, and verified status.
* **Pet Health Expert:** questions in their specialty, their published content, and verified status.
* **Community Moderator:** open reports, assigned moderation cases, and case status.
* **Administrator:** pending professional verifications, escalated cases, user account status, and platform activity.

### Use Case Screens

* **Pet Owner, Manage Pet Profiles, My Pets Dashboard:** each pet's name, species, breed, age, and upcoming reminders.
* **Pet Owner, Manage Pet Profiles, Pet Health Profile:** species, breed, birth date, weight, sex, allergies, conditions, current medications, and symptom history.
* **Veterinarian, Review Pet Health Information, Pet Search Dashboard:** pets the veterinarian is authorized to view, owner name, species, and authorization details.
* **Veterinarian, Review Pet Health Information, Pet Health Record Dashboard:** symptom log, medications, treatments, allergies, conditions, and referrals for one pet.
* **Administrator, Verify Professional Accounts, Pending Professional Accounts Dashboard:** applicant name, specialty, date submitted, and verification status.
* **Administrator, Verify Professional Accounts, Professional Account Review:** license number, credentials, the decision (approve, reject, suspend, or revoke), notes, and review history.

## 3. Master List of Data the System Must Store

### Users and Access
USER, ROLE, PERMISSION, ROLE_PERMISSION, USER_ROLE

* Account email, password hash, display name, account status, created date
* Role assignments and the permissions each role grants

### Professionals
PROFESSIONAL_PROFILE, VERIFICATION_REVIEW

* License number, specialty, credentials
* Verification status, who verified the account, and when
* Full history of verification decisions

### Pets and Health Records
PET, PET_ALLERGY, PET_CONDITION, SYMPTOM_LOG, PET_MEDICATION, TREATMENT, REMINDER, VET_REFERRAL, DATA_SHARE_AUTHORIZATION

* Pet name, species, breed, birth date, weight, sex, notes
* Allergies with reactions, and conditions with status
* Symptoms with severity, date observed, and notes
* Medications with dosage, frequency, and start and end dates
* Treatments and the professional who recommended them
* Reminders with due date, type, and status
* Referrals to in person care with reason and urgency
* Owner permission for a professional to view a pet's records, with start, expiry, and revoke dates

### Community
POST, COMMENT, POST_LIKE, POST_SAVE, POST_SHARE, USER_FOLLOW, TAG, POST_TAG

* Posts with title, body, author, and status
* Comments and replies
* Likes, saves, shares, and follows
* Tags that make posts searchable

### Health Questions and Advice
HEALTH_QUESTION, ADVICE_RESPONSE, ADVICE_REVIEW, HEALTH_ARTICLE, ARTICLE_TAG, HEALTH_RESOURCE

* Health questions, optionally about a specific pet
* Advice responses labeled by source type
* Ratings and feedback on advice
* Educational articles from verified professionals
* Searchable guides, FAQs, and condition overviews

### Products and Medication Reference
PRODUCT, PRODUCT_REVIEW, MEDICATION_REFERENCE

* Product listings with description, category, and active status
* Product reviews with ratings from 1 to 5
* Medication reference information with warnings, source, and last reviewed date

### Moderation
REPORT, MODERATION_CASE, MODERATION_ACTION, USER_RESTRICTION

* Reports with reporter, reason, and status
* Moderation cases with assigned moderator and status
* Actions taken on each case, including warnings and removals
* Restrictions placed on users, with start and end dates

### System
NOTIFICATION, MESSAGE, SYSTEM_SETTING, AUDIT_EVENT

* Notifications with read status
* Messages between users
* System settings such as supported pet types and reminder rules
* A permanent log of important actions

## 4. Questions

1. Should a user be able to hold more than one role, for example a veterinarian who also owns pets?
2. Is online ordering, payment, and shipping in scope, or only informational product listings?
3. Will the system connect to a veterinary drug information service, or will Administrators maintain medication reference data?
4. Can a Pet Owner message a Veterinarian directly, or only through health questions?
5. Should Administrator analytics reports be saved, or generated on demand?
6. Which pet types must be supported at launch: dogs only, or dogs, cats, and others?
7. Can owners share part of a pet's record with a professional, such as symptoms only, or is sharing for the whole record?
8. Can a Community Moderator also take part in the community as a Pet Owner?
