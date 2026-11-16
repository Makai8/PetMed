# PetMed – Sprint 4 Meeting Documentation

**Scrum Master:** Dorien Parris
**Team:** David Jean-Charles Bahidika, Makai Lyn-Ah-Ping, Makel Dickerson, Miles Sharpton, Dorien Parris
**Sprint goal:** Sign-in → Role Identification → Role-Based Navigation → Authorization → Database-Backed Retrieval
**Presentation:** Tuesday, November 17, 2026

---

## Meeting 1 – Sprint Planning

**Date:** Tuesday, November 10, 2026
**Attendees:** All members (David, Makai, Makel, Miles, Dorien)

**Discussion**
- Reviewed the Sprint Cycle IV requirements: sign-in for all five roles, role identification, role-based navigation, authorization, and one database-backed retrieval use case per role.
- Reviewed PetMed's assigned use cases:
  - Administrator: search, browse and list users
  - Pet Owner: browse the community feed
  - Veterinarian: view pet-health questions from owners
  - Pet Health Expert: browse questions and posts in their approved specialty
  - Community Moderator: view reported posts or reported health advice
- Chose the stack from the README: React website (`frontend/`), Python Flask API (`src/`), the MySQL database from Sprint III, and pytest for tests.
- Noted the GitHub requirement: every member pushes a meaningful contribution from their own account and must be able to run the app.

**Decisions**
- Dorien Parris continues as Scrum Master.
- Every role's page reads real data from MySQL through the API; nothing is hard-coded in the final version.
- Sample accounts share one demo password so the team can test every role.

**Assignments**

| Owner | Task |
|---|---|
| David Jean-Charles Bahidika | Website foundation: sign-in page, role dashboards, route guards, log out (`frontend/`) |
| Dorien Parris | Sprint IV sample data, Python API, the five role pages, tests, demo guide, meeting notes |
| Makai Lyn-Ah-Ping | Unanswered count on the Veterinarian page; help connect sign-in to the database |
| Miles Sharpton | Clear button on the Pet Owner community feed; database sign-in switch |
| Makel Dickerson | "Assigned to you" label on the Moderator's reported content |

---

## Meeting 2 – API and Database Walkthrough (Zoom)

**Date:** Thursday, November 12, 2026
**Format:** Zoom (the Scrum Master was sick)

**Discussion**
- A long how-to session on how the pieces connect:
  - The React website sends the email and password to the API (`POST /api/login`).
  - The API checks the password against the hashed password in the `User` table, finds the user's role in `User_Role`, and returns a signed token.
  - Each page sends that token with every request. The API checks the role again (`@require_roles`) before reading data from MySQL, and answers 403 if the role isn't allowed.
- Walked through setting up each computer: rebuilding the database with the five SQL scripts, installing the Python packages, putting each member's own MySQL password in `src/.env` (never committed), and starting the API and the website.
- Covered the common setup problems: PowerShell blocking `npm` (use `npm.cmd`) and "Access denied" from MySQL (wrong password in `src/.env`).

**Decisions**
- The API runs on port 4000 and the website on port 5173.
- All sample accounts use the password `PetMed123!`; real passwords are stored only as hashes.
- Each member makes their change on their own role's page and pushes it from their own GitHub account.

---

## Meeting 3 – Testing and Demo Check

**Date:** Monday, November 16, 2026
**Attendees:** All members

**Discussion**
- Confirmed every member can pull the latest code and run the app on their own computer.
- Checked that all five roles sign in and reach the correct dashboard, an invalid sign-in is rejected, and each role's page shows the expected data.
- Reviewed the demo order in `docs/Sprint4_Demo_Guide.md`.

**Decisions**
- Run the demo from the current GitHub version, after rebuilding the database so all lists show the expected starting data.
- Each member presents the part they built.

**Action items**

| Owner | Task |
|---|---|
| Makel Dickerson | Fix the "Assigned to you" label to compare with the signed-in user's full name |
| David, Makai, Makel, Dorien | Add a running-the-app screenshot to `evidence/Sprint4/` |
| All members | Rehearse the demo once before Tuesday's presentation |
