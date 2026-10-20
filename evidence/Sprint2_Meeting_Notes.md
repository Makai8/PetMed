# PetMed – Sprint 2 Meeting Documentation

**Scrum Master:** Dorien Parris
**Team:** David, Makai, Makhel, Miles, Dorien Parris

---

## Meeting 1 – Sprint Planning (face-to-face)

**Date:** October 12, 2026 [Confirm]
**Format:** Face-to-face (photo: `evidence/team meeting 01.jpeg`)
**Attendees:** David, Makai, Makhel, Miles, Dorien Parris [confirm]

**Discussion**
- Reviewed the Sprint Cycle II requirements for the database design.
- Dorien created the Sprint 2 checklist (see the Sprint 2 section of the main `README.md`).

**Decisions**
- Dorien Parris confirmed as Scrum Master for Sprint 2.
- The database design must cover the complete system, not only the Sprint 1 screens.
- All Sprint 2 materials will be stored in GitHub (`docs/`, `backend/`, `evidence/`).

**Action items**

| Owner | Task |
|---|---|
| Dorien Parris | Create the ERD |
| Makhel | Verify the ERD supports the Functional Requirements; pick 3+ use cases for the presentation |
| Makai | Create the data dictionary |
| Miles | Write the database business rules |
| David | Review and revise the design; record UI-review changes and open questions |

---

## Meeting 2 – Business Rules, User Roles and ERD Approach (face-to-face)

**Date:** October 14, 2026 [Confirm]
**Format:** Face-to-face (photo: `evidence/team meeting 02.jpeg`)
**Attendees:** David, Makai, Makhel, Miles, Dorien Parris [confirm]

**Discussion**
- Reviewed the draft business rules.
- Discussed how to represent the five user roles (Pet Owner, Veterinarian, Pet Health Expert, Community Moderator, Administrator) in the database.
- Discussed the best approach for organizing the ERD.

**Decisions**
- Roles are stored through a USER_ROLE junction table instead of a single role field, so one user can hold more than one role.
- Professional roles (Veterinarian, Pet Health Expert) require verification before their privileges become active.
- The ERD is organized into five modules (Accounts & Access, Pet Health, Community & Advice, Moderation & Oversight, Catalog & Reference) connected through one central USER table.
- The final set of 46 business rules is stored in `backend/README.md`.

**Action items**

| Owner | Task |
|---|---|
| Dorien Parris | Update the ERD to use USER_ROLE and the five-module layout |
| Makai | Update the data dictionary to match the final ERD |
| Miles | Finalize the business rules in GitHub |
| David | Prepare the Sprint 2 presentation |
| Makhel | Confirm the use cases chosen for the presentation |
