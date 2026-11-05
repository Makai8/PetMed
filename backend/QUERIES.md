# PetMed: Query List

The queries in [`backend/queries.sql`](queries.sql) show the database doing what PetMed needs: **searching**, **pulling related data**, **adding** and **modifying** records, and **enforcing business rules**. They use the sample data in [`backend/seed.sql`](seed.sql). Both files were written by David Jean-Charles Bahidika.

## How to run

From the `backend` folder, in this order:

| Step | PowerShell / macOS / Linux / Git Bash | Command Prompt (cmd) |
|---|---|---|
| 1. Create the database (once) | `cat PetMedDB.sql \| mysql -u root -p` | `mysql -u root -p < PetMedDB.sql` |
| 2. Load the sample data (once) | `cat seed.sql \| mysql -u root -p` | `mysql -u root -p < seed.sql` |
| 3. Run the queries | `cat queries.sql \| mysql -u root -p --force --table` | `mysql -u root -p --force --table < queries.sql` |

- `--force` keeps going after an error. Without it, MySQL stops at Rule 1, because the rule tests are **meant** to fail.
- `--table` prints the results as tables.
- To start over with clean data, run `mysql -u root -p -e "DROP DATABASE IF EXISTS petmed;"`, then steps 1 and 2 again.
- Saved your login with `mysql_config_editor` (see the README)? Then replace `-u root -p` with `--login-path=petmed`.

Each query can also be copied on its own into the `mysql>` prompt (`mysql -u root -p petmed`).

---

## Queries

### 1. Search: all dogs owned by Maya Johnson
Finds one owner's pets of one species by joining `Pet` to `User`.
```sql
SELECT p.name, p.breed, p.weight
FROM Pet p
JOIN User u ON p.owner_user_id = u.user_id
WHERE u.full_name = 'Maya Johnson' AND p.species = 'Dog';
```
**Expected:** 1 row, `Bella | Golden Retriever | 65.40`. Her other pet, Milo, is a cat.

### 2. Search: all suspended accounts
Filters users by account status, the way a moderator or administrator would look for them.
```sql
SELECT user_id, full_name, email
FROM User
WHERE account_status = 'suspended';
```
**Expected:** 1 row, `87370002 | Sofia Ramirez | sofia.ramirez@petmed.com`.

### 3. Related data: symptom logs with pet and owner, newest first
Joins three tables (`Symptom_Log`, `Pet` and `User`) to show each pet's health history together with its owner.
```sql
SELECT p.name AS pet, s.symptom, s.severity, s.observed_at, u.full_name AS owner
FROM Symptom_Log s
JOIN Pet p ON s.pet_id = p.pet_id
JOIN User u ON p.owner_user_id = u.user_id
ORDER BY s.observed_at DESC;
```
**Expected:** 6 rows, starting with `Simba | Excessive scratching | mild | 2026-10-27 21:00:00 | Sofia Ramirez`.

### 4. Add: Marcus adopts a new pet
Inserts a new `Pet` for an existing user, then lists his pets. MySQL assigns the new `pet_id` automatically.
```sql
INSERT INTO Pet (owner_user_id, name, species, breed, birth_date, weight)
VALUES (87370001, 'Coco', 'Dog', 'Beagle', '2025-05-01', 18.60);

SELECT pet_id, name, breed FROM Pet WHERE owner_user_id = 87370001;
```
**Expected:** 3 rows, Rocky, Luna and the new **Coco** (`7380006`).

### 5. Modify: Bella gained weight at her checkup
Shows the value before, updates it, and shows it after.
```sql
SELECT name, weight FROM Pet WHERE pet_id = 7380000;
UPDATE Pet SET weight = 67.10 WHERE pet_id = 7380000;
SELECT name, weight FROM Pet WHERE pet_id = 7380000;
```
**Expected:** `Bella | 65.40` before, `Bella | 67.10` after.

---

## Business rules: these are supposed to fail

Each statement breaks a rule, and the database **rejects** it. An error here means the rule is working.

### Rule 1 (UNIQUE): each email can only be used once
```sql
INSERT INTO User (email, password_hash, full_name, account_status)
VALUES ('maya.johnson@petmed.com', '$2b$10$fake', 'Fake Maya', 'active');
```
**Expected error:** `ERROR 1062 (23000): Duplicate entry 'maya.johnson@petmed.com' for key 'user.email'`

### Rule 2 (FOREIGN KEY): a pet must belong to a real user
```sql
INSERT INTO Pet (owner_user_id, name, species, breed, birth_date, weight)
VALUES (99999999, 'Ghost', 'Cat', 'Unknown', '2024-01-01', 8.00);
```
**Expected error:** `ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails …`

### Rule 3 (CHECK): a user can't follow themselves
```sql
INSERT INTO User_Follow (follower_user_id, followed_user_id)
VALUES (87370000, 87370000);
```
**Expected error:** `ERROR 3819 (HY000): Check constraint 'chk_user_follow_1' is violated.`

---

## Notes

- **Running `queries.sql` again changes the results:** a second **Coco** is added, and Bella's "before" weight shows 67.10. Rebuild the database (see *How to run*) to get the expected results above again.
- The sample data uses capitalized species (`'Dog'`, `'Cat'`), and query 1 filters on `'Dog'`. Keep the capitalization consistent when adding data.
- For more ways to write queries, see **Common SQL commands** in [`README.md`](README.md).
- The Sprint III presentation uses [`presentation_queries.sql`](presentation_queries.sql): queries A–D, the 3 use cases, 3 rule tests and practice queries. Load all three sample data files first (`seed.sql`, `sample_data_health_records.sql`, `sample_data_more.sql`; see `README.md`, step 7).
