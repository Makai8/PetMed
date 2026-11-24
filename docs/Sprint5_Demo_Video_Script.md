# PetMed: Sprint Cycle V Demo Video Script

The video shows the working app, not slides. Aim for 10 to 12 minutes. Record the screen with sound
(Zoom "Record", OBS, or the Windows Snipping Tool's video mode), with the website on one side and a
MySQL prompt on the other.

## Set up before recording

1. `git pull`, so you record the current GitHub version.
2. Rebuild the database with all seven scripts (see [`src/README.md`](../src/README.md), step 1), so every list starts
   from the expected sample data.
3. Start the API (`python src/app.py`) and the website (`npm.cmd run dev` in `frontend`).
4. Open a MySQL prompt: `mysql -u root -p petmed`. Keep [`backend/sprint5_check_queries.sql`](../backend/sprint5_check_queries.sql)
   open so you can paste each block.
5. Run `python -m pytest tests` once; it should end with **79 passed** and no skips.

Every sample account uses the password **`PetMed123!`**. Use **Log Out** between roles.

## Scenes

| # | Who talks | Show | Do | Point out |
|---|---|---|---|---|
| 1 | Dorien | GitHub | The repo's commit list for this week | Sprint V commits from all five members |
| 2 | Dorien | Sign-in | `maya.johnson@petmed.com` with password `wrong` | Still refused: earlier work still works |
| 3 | Dorien | **Administrator** | Run query block 1 (before). Sign in as `daniel.owens@petmed.com` → **Professional Verification** | Dr. Priya Shah and Jordan Lee are *pending* |
| 4 | Dorien | Invalid case | Click **Reject** on Jordan Lee with no note | "Add a note explaining why." Nothing changes |
| 5 | Dorien | Normal case | Type "License VM-48213 confirmed with the Florida board." on Priya, click **Approve** | Green message; she moves to the Approved tab with the review history |
| 6 | Dorien | Database | Run query block 1 again (after) | Status *approved*, a new Verification_Review row, and Priya now has the veterinarian role |
| 6a | Dorien | Optional: suspend a user | **Manage Users** → **Suspend** Marcus Williams with no reason (refused), then with a reason; then **Reactivate** him | Status flips to suspended and back; a suspended user can't sign in |
| 7 | David | **Pet Owner** | Run block 2 (before). Sign in as Maya → **Symptom Tracker** | Her pets' symptom history |
| 7a | David | Prerequisite: add a pet | **My Pets** → click **Add pet** with no name ("Please fill in name."), then add Daisy, Dog, Beagle, born 2024-05-01, 22.5 lb | Daisy appears in her pets, and in the Symptom Tracker's pet list |
| 8 | David | Invalid case | Click **Save symptom** with no pet chosen | "Please fill in which pet." |
| 9 | David | Normal case | Bella, "Sneezing after walks", Moderate, a note → **Save symptom** | It appears at the top of the history |
| 10 | David | Database | Run block 2 again | The new Symptom_Log row |
| 10a | David | Prerequisite: ask a question | **Ask for Health Advice** → Milo, send to Dr. James Carter, "Milo has been scratching his ears a lot this week. What could cause that?" | This is how questions reach vets and experts |
| 11 | Makai | **Veterinarian** | Run block 3 (before). Sign in as `dr.james.carter@petmed.com` → **Pet Health Questions** → **Sent to me** | Bella's water question has no answers |
| 12 | Makai | Invalid case | Type "Go to a vet." → **Post guidance** | "Write at least 20 characters of guidance." |
| 13 | Makai | Normal case | Write real guidance → **Post guidance** | The answer shows under the question, labelled Veterinarian |
| 14 | Makai | Database | Run block 3 again | New Advice_Response row with source_type *veterinarian* |
| 15 | Miles | **Pet Health Expert** | Sign in as `kevin.nguyen@petmed.com` → **Questions in My Expertise** | Specialty Nutrition; the treats question has no answers |
| 16 | Miles | Normal case | Answer the treats question | "1 answer" |
| 17 | Miles | Database | Run block 3 again | New row with source_type *pet_health_expert* |
| 17a | Makel | Prerequisite: report a post | As Maya, **Community Feed** → 🚩 **Report** on a post, with a reason | This is how reports reach the moderator |
| 18 | Makel | **Community Moderator** | Run block 5 (before). Sign in as `tasha.brooks@petmed.com` → **Reported Posts and Advice** | 2 open reports; the garlic post says "Assigned to you" |
| 19 | Makel | Invalid case | **Save decision** on the garlic post with no reason | "Please fill in reason." |
| 20 | Makel | Normal case | "Remove the content", reason "Garlic is toxic to dogs." → **Save decision** | Green message; the report moves to Resolved |
| 21 | Makel | Database | Run block 5 again | Report *resolved*, case *closed* with a closed_at time, a remove_content action, post status *removed* |
| 22 | Makel | Earlier feature | Sign in as Maya → **Community Feed**, search `garlic` | The removed post no longer shows |
| 23 | Dorien | Tests | `python -m pytest tests -v` | 79 passed: Sprint IV sign-in, authorization and retrieval plus all five Sprint V use cases |

## After recording

1. Upload the video to Canvas.
2. If the file is over 100 MB, upload it to YouTube (unlisted) or Google Drive (anyone with the link can view) and
   add the link to the top of the main `README.md` under **Sprint V demo video**. Otherwise commit it in `evidence/Sprint5/`.
