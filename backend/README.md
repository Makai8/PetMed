## Database Setup (MySQL)

PetMed uses a **MySQL** database named `petmed`. The full schema (41 tables, 69 foreign keys and the business-rule checks) is in [`backend/PetMedDB.sql`](PetMedDB.sql) and matches the Sprint 2 ERD.

### 1. Install the tools

| Tool | Notes |
|---|---|
| **MySQL Server 26.10** (Community) | Download the Windows MSI from [dev.mysql.com/downloads/mysql](https://dev.mysql.com/downloads/mysql/). Choose **Typical**, keep port **3306**, set a **root password**, and leave "Configure as a Windows Service" checked. |
| **VS Code extensions** | **SQLTools** (`mtxr.sqltools`) and **SQLTools MySQL/MariaDB/TiDB** (`mtxr.sqltools-driver-mysql`). VS Code offers to install both when you open this repo. |

### 2. Add MySQL to your PATH (one time)

Run this in PowerShell, then restart VS Code:

```powershell
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
[Environment]::SetEnvironmentVariable("Path", "$userPath;C:\Program Files\MySQL\MySQL Server 26.10\bin", "User")
```

To use it right away without restarting, also run: `$env:Path += ";C:\Program Files\MySQL\MySQL Server 26.10\bin"`

### 3. Save your login (one time)

This stores your password in an encrypted file on your own computer, so you aren't asked for it each time:

```powershell
mysql_config_editor set --login-path=petmed --user=root --password
```

### 4. Create the database

From the `backend` folder:

```powershell
Get-Content .\PetMedDB.sql -Raw | mysql --login-path=petmed
```

No output means it worked. Re-running the script after a design change? Drop the old copy first with `mysql --login-path=petmed -e "DROP DATABASE petmed;"`. This deletes any data in it.

### 5. Verify

```powershell
mysql --login-path=petmed -e "SELECT COUNT(*) AS tables FROM information_schema.tables WHERE table_schema='petmed';"
```

It should print **41**. To open a prompt inside the database, run `mysql --login-path=petmed petmed`, and type `exit` to leave.

### 6. Browse it in VS Code

In the **SQLTools** sidebar, add a new **MySQL** connection with host `localhost`, port `3306`, database `petmed` and user `root`. Leave the password empty and choose **Ask on connect**, so it is never saved to a file. Your editor settings in `.vscode/` stay on your own computer and are not committed.

### 7. Load the sample data

From the `backend` folder, run these **in this order** after step 4:

```powershell
Get-Content .\seed.sql -Raw | mysql --login-path=petmed
Get-Content .\sample_data_health_records.sql -Raw | mysql --login-path=petmed
Get-Content .\sample_data_more.sql -Raw | mysql --login-path=petmed
```

| File | What it adds |
|---|---|
| [`seed.sql`](seed.sql) | 8 users in 5 roles, 6 pets, symptoms, posts, comments, questions, products |
| [`sample_data_health_records.sql`](sample_data_health_records.sql) | Pet allergies, conditions and medications |
| [`sample_data_more.sql`](sample_data_more.sql) | Everything else, so **all 41 tables** have data: permissions, vet profiles, treatments, reminders, record sharing, tags, likes, articles, answers, reviews, reports and moderation |

To start over with clean data, drop the database (step 4), then run step 4 and these three files again.

### 8. Run the queries

- [`queries.sql`](queries.sql): search, related data, add, modify and business-rule tests. Explained with expected results in [`QUERIES.md`](QUERIES.md).
- [`presentation_queries.sql`](presentation_queries.sql): the Sprint III presentation queries (A–D, the 3 use cases, the 3 rules and practice queries). It needs all three sample data files loaded.

### Running the database

MySQL runs in the background as a **Windows service** and starts automatically when your computer boots, so normally there's nothing to start. Open a terminal and connect:

```powershell
mysql --login-path=petmed petmed
```

At the `mysql>` prompt you can run SQL, for example:

```sql
SHOW TABLES;
SELECT * FROM user;
DESCRIBE pet;
```

Type `exit` to leave. Leaving the prompt does **not** stop the server.

**Is the server running?**

```powershell
Get-Service MySQL*
```

`Status` should say **Running**. The command finds the service whatever its exact name is.

**Start, stop or restart the server.** These need PowerShell **as Administrator** (right-click PowerShell → Run as administrator):

```powershell
Get-Service MySQL* | Start-Service     # start
Get-Service MySQL* | Stop-Service      # stop (frees memory when you're not working on PetMed)
Get-Service MySQL* | Restart-Service   # restart
```

You can also use the **Services** app (press Win, type "Services") and find the entry starting with **MySQL**.

**Run a saved .sql file** (for example a script of test data):

```powershell
Get-Content .\your_file.sql -Raw | mysql --login-path=petmed petmed
```

**Common errors**

| Message | Fix |
|---|---|
| `Can't connect to MySQL server on 'localhost'` | The server is stopped. Start it with the commands above. |
| `Access denied for user 'root'@'localhost'` | Wrong password. Re-run the `mysql_config_editor set` command from step 3. |
| `'mysql' is not recognized` | MySQL isn't on your PATH yet. Do step 2, then restart VS Code. |
| `Unknown database 'petmed'` | The database hasn't been created yet. Do step 4. |

### Common SQL commands

Run these at the `mysql>` prompt (`mysql --login-path=petmed petmed`). Every SQL statement ends with a **semicolon** `;`, and text values go in **single quotes** `'like this'`.

**Look around**

```sql
SHOW TABLES;              -- list all 41 tables
DESCRIBE Pet;             -- show a table's columns and types
SELECT * FROM Pet;        -- show every row and column in a table
```

**Add rows (INSERT)**

```sql
-- A new user (user_id is assigned automatically, starting at 87370000)
INSERT INTO User (email, password_hash, full_name, account_status)
VALUES ('maya@petmed.com', 'hashed_pw', 'Maya Lopez', 'active');

-- A pet owned by that user (pet_id starts at 7380000)
INSERT INTO Pet (owner_user_id, name, species, breed, birth_date, weight)
VALUES ((SELECT user_id FROM User WHERE email = 'maya@petmed.com'),
        'Rex', 'dog', 'Labrador', '2021-04-12', 30.5);

-- A symptom for that pet
INSERT INTO Symptom_Log (pet_id, symptom, severity, observed_at, notes)
VALUES ((SELECT pet_id FROM Pet WHERE name = 'Rex'),
        'vomiting', 'mild', '2026-11-01 08:30:00', 'After breakfast');
```

**Find rows (SELECT)**

```sql
-- Pick columns, filter with WHERE, sort with ORDER BY
SELECT name, species, weight FROM Pet WHERE species = 'dog' ORDER BY name;

-- Pattern match: % means "anything"
SELECT full_name, email FROM User WHERE email LIKE '%@petmed.com';

-- Only the first few rows
SELECT * FROM Pet ORDER BY weight DESC LIMIT 5;

-- Count rows per group
SELECT species, COUNT(*) AS total FROM Pet GROUP BY species;
```

**Combine tables (JOIN)**

```sql
-- Each pet with its owner's name
SELECT u.full_name AS owner, p.name AS pet, p.species
FROM Pet p
JOIN User u ON u.user_id = p.owner_user_id;

-- A pet's symptom history, newest first
SELECT p.name, s.symptom, s.severity, s.observed_at
FROM Symptom_Log s
JOIN Pet p ON p.pet_id = s.pet_id
WHERE p.name = 'Rex'
ORDER BY s.observed_at DESC;
```

**Change rows (UPDATE)**

```sql
UPDATE Pet SET weight = 31.2 WHERE name = 'Rex';
UPDATE User SET account_status = 'suspended' WHERE email = 'maya@petmed.com';
```

**Remove rows (DELETE)**

```sql
-- Delete child rows before their parent: symptoms, then the pet, then the user.
-- The database blocks deleting a user who still owns a pet.
DELETE FROM Symptom_Log WHERE symptom = 'vomiting';
DELETE FROM Pet WHERE name = 'Rex';
DELETE FROM User WHERE email = 'maya@petmed.com';
```

> ⚠️ **Always include a `WHERE` on `UPDATE` and `DELETE`.** Without one, the command changes or deletes **every row** in the table.

### ID numbering

Primary keys auto-increment. Two tables start at numbers that spell the table name on a phone keypad:

| Table | First ID | Keypad |
|---|---|---|
| `User` | **87370000** | U-S-E-R = 8-7-3-7 |
| `Pet` | **7380000** | P-E-T = 7-3-8 |

All other tables start at 1.

### Sharing data with the team

Each member runs their own local copy from `PetMedDB.sql`. To share test data, export it and commit the file:

```powershell
mysqldump --login-path=petmed --databases petmed --result-file=petmed_dump.sql
```

Use `--result-file` rather than `>`: PowerShell's `>` saves the file in an encoding MySQL can't import.

### Notes

- On Windows, MySQL stores table names in lowercase (`user`, `pet`). Queries work with any casing, but use the same casing as the schema so the code also runs on macOS and Linux.
- **Never commit passwords.** Keep `askForPassword: true` in the shared SQLTools connection.
- The schema requires **MySQL 8.0.16 or later**, because the business-rule `CHECK` constraints need it.


# Business Rules 
1. Each user must have a unique email address.
2. Each user must be assigned at least one valid system role.
3. If PetMed supports multiple roles per user, role assignments must be stored through a user-role relationship rather than a single role field.
4. Roles may have multiple permissions, and permissions may belong to multiple roles.
5. Only users with the required permissions may perform restricted actions such as moderation, professional verification, or system administration.
6. Administrator accounts should not be created through normal public registration.
7. A professional profile must belong to one valid user account.
8. Veterinarian and Pet Health Expert privileges must remain inactive until the professional account is verified.
9. Only authorized Administrators may approve, reject, suspend, or revoke professional verification.
10. Each pet must belong to exactly one Pet Owner, while a Pet Owner may own multiple pets.
11. All pet-health records must reference a valid pet.
12. A pet may have multiple allergy, condition, symptom, treatment, and medication records.
13. A symptom log must record the pet, the symptom, and when it was observed.
14. A treatment may optionally reference the professional who prescribed or recommended it.
15. A medication record must belong to one pet and should include dosage, frequency, and treatment dates when applicable.
16. A reminder must belong to a valid pet and user, and may reference a medication record when appropriate.
17. A veterinary referral must belong to a valid pet and identify the professional who created it.
18. Pet-health data shared with a professional must be covered by a valid data-sharing authorization when authorization is required.
19. Revoked or expired data-sharing authorization must no longer grant access to protected pet-health information.
20. Every community post and health article must belong to one valid author.
21. Posts and articles may have multiple tags, and many-to-many relationships must be handled through associative entities such as POST_TAG and ARTICLE_TAG.
22. Each comment must belong to a valid post and a valid user.
23. A reply comment may reference another comment as its parent.
24. A user may like or save the same post only once.
25. A user may follow another user only once and may not follow themselves.
26. Each health question must belong to a valid user and may optionally reference a specific pet.
27. Each advice response must belong to one health question and identify the user who authored it.
28. Professional guidance may only be labeled as Veterinarian or Pet Health Expert guidance when the author has the appropriate verified professional status.
29. Every message must identify a valid sender and recipient.
30. Every notification must belong to a valid user and should record whether it has been read.
31. Each product must have a unique product identifier and may be marked inactive instead of permanently deleted.
32. Each product review must belong to one valid product and one valid user.
33. Product ratings must fall within the rating range approved by the application.
34. A user should have no more than one active review for the same product unless multiple reviews are intentionally supported.
35. Every report must identify the user who submitted it and the reported post, comment, or user when applicable.
36. Each moderation case must reference a valid report and may be assigned to one moderator.
37. Every moderation action must belong to a moderation case and identify the moderator or administrator who performed it.
38. Closed moderation cases should remain stored for audit and history purposes.
39. Medication reference records should preserve important safety information such as warnings, source information, and last-reviewed date when available.
40. Each system-setting key must be unique, and only authorized administrators may modify system settings.
41. Every primary key must uniquely identify one record.
42. Every required foreign key must reference an existing valid record.
43. The database must prevent orphaned records.
44. Important historical records should generally be archived, revoked, closed, or deactivated instead of permanently deleted when audit history is needed.
45. Date values must remain logically consistent, such as preventing an end date from occurring before a start date.
46. Status fields such as user status, verification status, report status, reminder status, and moderation-case status must use valid values defined by the system.


