# PetMed – Sprint 5 Meeting Documentation

**Scrum Master:** Dorien Parris
**Team:** David Jean-Charles Bahidika, Makai Lyn-Ah-Ping, Makel Dickerson, Miles Sharpton, Dorien Parris
**Sprint goal:** Adding and modifying data. Each role's use case saves new data or changes existing data in MySQL.
**Deliverable:** Demonstration video (no in-class presentation), submitted on Canvas and stored or linked in GitHub

---

## Meeting 1 – Sprint Planning

**Date:** Thursday, November 19, 2026
**Attendees:** _(fill in)_

**Discussion**
- Reviewed the Sprint Cycle V requirements: five use cases that add or change data, testing (valid data, invalid
  data, the database really changes, earlier features still work), and a demo video instead of a presentation.
- Reviewed PetMed's assigned use cases:
  - Administrator: review a Veterinarian or Pet Health Expert account and update the professional verification status
  - Pet Owner: record a symptom or health event for one of their pets
  - Veterinarian: provide general veterinary guidance on a pet owner's health question
  - Pet Health Expert: respond to a question within the approved area of expertise
  - Community Moderator: review a reported post or advice and update the moderation case with the action taken
- Matched each use case to the tables already in the ERD: `Professional_Profile` + `Verification_Review`,
  `Symptom_Log`, `Advice_Response`, `Moderation_Case` + `Moderation_Action` + `Report`. No new tables were needed.
- Added two sample professionals waiting for verification (Dr. Priya Shah, Jordan Lee) so the Administrator
  use case has something to review.

**Decisions**
- Dorien Parris continues as Scrum Master.
- The Administrator use case is built first as the worked example; every other use case copies its pattern
  (check the data → save it → log it → show the result).
- Each use case refuses bad data with a clear message and saves nothing in that case.
- Every change is also recorded in `Audit_Event`.
- The work is split 40 / 15 / 15 / 15 / 15 (see the table). Each member pushes their part from their own account.

**Assignments**

| Owner | Share | Task |
|---|---|---|
| Dorien Parris | 40% | Sprint V sample data, shared helpers, Administrator verification (API + page), the lists the other pages need, menus, all Sprint V tests, video script, meeting notes |
| David Jean-Charles Bahidika | 15% | Pet Owner: record a symptom (API + form) |
| Makai Lyn-Ah-Ping | 15% | Veterinarian: answer a question (API + answer box) |
| Miles Sharpton | 15% | Pet Health Expert: answer in my expertise (API + answer box) |
| Makel Dickerson | 15% | Community Moderator: review a report (API + decision form), fix the "Assigned to you" label |

Details for each task: [`docs/Sprint5_Team_Tasks.md`](../docs/Sprint5_Team_Tasks.md)

---

## Meeting 2 – Progress Check

**Date:** _(fill in; suggested Sunday, November 22)_
**Attendees:** _(fill in)_

**Discussion**
- Each member shows their use case running and their tests passing (`python -m pytest tests -k <part> -v`).
- _(notes)_

**Decisions / blockers**
- _(notes)_

---

## Meeting 3 – Record the Demo Video

**Date:** _(fill in; suggested Monday, November 23)_
**Attendees:** _(fill in)_

**Discussion**
- Rebuilt the database, ran all tests, and recorded the video following
  [`docs/Sprint5_Demo_Video_Script.md`](../docs/Sprint5_Demo_Video_Script.md).
- _(notes)_

**Action items**

| Owner | Task |
|---|---|
| Dorien Parris | Upload the video to Canvas and add the link to the README |
