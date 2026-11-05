# PetMed – Sprint 3 Meeting Documentation

**Scrum Master:** Dorien Parris
**Team:** David, Makai, Makhel, Miles, Dorien Parris

Sprint 3 turned the Sprint 2 design into a working MySQL database. The team met three times: once to plan and assign the work, once to review the implementation and plan the app's pages, and once to check everyone's progress on GitHub before the presentation.

---

## Meeting 1 – Assignments, Tools, Goals and Use Cases

**Discussion**
- Reviewed the Sprint Cycle III requirements: build the database from the Sprint 2 ERD, fill it with meaningful sample data, run queries that search, combine, add and change data, show the business rules working, and present it all.
- **Tools.** Agreed on the tools every member would install so that everyone works the same way:
  - **MySQL Server** (Community edition) for the database itself.
  - **VS Code** with the **SQLTools** and **SQLTools MySQL** extensions, to browse tables and run queries inside the editor.
  - **GitHub** (`Makai8/PetMed`) to share every script, document and screenshot.
- **Goals.** Set the goals for the sprint:
  - Build all of the tables from the ERD, with the links between them and the rules the database can enforce on its own.
  - Load sample data that looks like real PetMed users, so the queries return meaningful results.
  - Write queries for searching, pulling related data, adding data and modifying data.
  - Keep every file on GitHub, so any member can rebuild the same database on their own computer.
- **Commits.** Agreed that every member makes at least 5 commits to GitHub during the sprint, so each person's work is visible in the history.
- **Use cases.** Chose the three situations to demonstrate, one from each main part of the app:
  1. A pet owner tracks a pet's symptoms over time to show the vet.
  2. A pet owner asks a health question and a verified vet answers it.
  3. A user reports another user, and a moderator reviews the report and takes action.

**Decisions**
- Dorien Parris continues as Scrum Master.
- The schema follows the Sprint 2 ERD exactly: 41 tables in five areas (Accounts & Access, Pet Health, Community & Advice, Catalog & Reference, Moderation & Oversight).
- All database scripts live in `backend/`; documents in `docs/`; screenshots and meeting notes in `evidence/`.
- Passwords are never committed. Each member keeps their own MySQL login on their own computer.

**Assignments**

| Owner | Task |
|---|---|
| Dorien Parris | Build the MySQL schema (`PetMedDB.sql`) from the ERD; keep the ERD up to date; write the database setup instructions in `backend/README.md` |
| David | Write the first set of sample data (`seed.sql`) and the demonstration queries (`queries.sql`) |
| Makai | Write the Sprint 3 functional requirements (Task 6) |
| Makhel | Add pet health sample data: allergies, conditions and medications (`sample_data_health_records.sql`) |
| Miles | Run the queries on a local database and record screenshot evidence; document how to check the MySQL login |

---

## Meeting 2 – Implementation, Page Layouts, Design and Buttons

**Discussion**
- **Implementation.** Reviewed the database as built:
  - 41 tables, 69 links (foreign keys) between them, and 8 built-in checks, such as ratings staying between 1 and 5 and a user not being able to follow themselves.
  - IDs number themselves. User IDs start at 87370000 and pet IDs at 7380000, because U-S-E-R and P-E-T spell those numbers on a phone keypad.
  - Walked through creating the database and loading the sample data, and fixed setup problems as they came up (adding MySQL to the PATH, saving the login, running scripts from PowerShell).
- **Page layouts.** Discussed how the app's main pages map to the database:
  - Home and splash screen.
  - Sign up and log in (User, Role).
  - My Pets and a pet's profile (Pet, Symptom_Log, Pet_Medication, Pet_Allergy, Pet_Condition, Reminder).
  - Community feed (Post, Comment, Tag) and Ask a Vet (Health_Question, Advice_Response).
  - Products and reviews (Product, Product_Review).
  - Moderator and administrator dashboards (Report, Moderation_Case, System_Setting).
- **Design.** Kept one consistent look across pages, matching the PetMed logo and the Sprint 1 screens.
- **Buttons.** Listed the main actions each page needs, since each button will save or read data in the database. Examples: *Add Pet*, *Log Symptom*, *Set Reminder*, *Ask a Question*, *Answer*, *Like*, *Save*, *Share*, *Follow*, *Write a Review*, *Report*, and the moderator's *Warn* and *Suspend*.

**Decisions**
- Every button that saves something must have a table and columns ready for it. The ERD and schema already cover the actions listed above.
- Some rules depend on who is logged in, such as only a pet's owner being able to edit its records. These will be enforced by the app in Sprint 4. The database enforces the rest itself.
- Sample data uses one consistent cast of characters (Maya, Marcus, Sofia, two vets, an expert, a moderator and an administrator), so queries and screenshots tell one connected story.

**Action items**

| Owner | Task |
|---|---|
| Dorien Parris | Finish the setup instructions and the SQL data dictionary |
| David | Finish the queries, including the business-rule tests |
| Makhel | Finish the health sample data |
| Miles | Capture query screenshots and sync the homepage and setup documentation |
| Makai | Finish the Task 6 functional requirements |

---

## Meeting 3 – Collaboration Check

**Discussion**
- Went through the GitHub history together to confirm each member's contributions and commit count.
- Each member confirmed they could build the database on their own computer from the scripts in `backend/` and see all 41 tables.
- Resolved merge conflicts that came up when several members pushed at the same time, and agreed to pull before starting work and before every push.
- Reviewed what the presentation needs: why we chose MySQL, the updated ERD, the tables, the sample data, the tools and commands, queries A–D, the 3 use cases, the 3 business rules, and the files on GitHub.
- Identified the remaining gaps: sample data for every table, the presentation queries, and these meeting notes.

**Decisions**
- All remaining work is committed to GitHub before the presentation.
- The team rebuilds the database from scratch before presenting, so the live queries match the expected results.
- Members should be ready to write a new query live if the instructor asks for one.

**Action items**

| Owner | Task |
|---|---|
| Dorien Parris | Commit the remaining sample data, presentation queries, query guide, data dictionary and meeting notes; prepare the presentation |
| All members | Pull the latest changes, rebuild the database, and practice the presentation queries |
