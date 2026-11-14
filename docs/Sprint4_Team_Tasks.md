# PetMed: Sprint Cycle IV Team Tasks

**Scrum Master:** Dorien Parris · **Presentation:** Tuesday, November 17, 2026

David already pushed the website foundation (sign-in page, role dashboards, route guards, log out). The steps below add the database API and turn each role's placeholder page into a working, database-backed page. Every member commits and pushes their own part **from their own GitHub account**. Dorien sends each member a zip with their files already in the right folders.

## Order

Steps 1–3 come first, in order. Steps 4–7 can happen in any order after step 3.

| Step | Who | Zip | What it adds | Commit message |
|---|---|---|---|---|
| 1 | Dorien | `1-Dorien-sample-data.zip` | Sprint IV sample data (real password hashes, posts, questions, reports) and this task list | `Add Sprint IV sample data and team tasks` |
| 2 | Makai | `2-Makai-api.zip` | Python API on port 4000: database sign-in (`POST /api/login`), tokens, role checks (`src/`) | `Add Flask API with database sign-in and role-based authorization` |
| 3 | Miles | `3-Miles-connect-pages.zip` | Connects the role pages to the API, shared page layout and styles, and the Pet Owner community feed | `Connect use case pages to the API and add Pet Owner community feed` |
| 4 | Makai | `4-Makai-veterinarian.zip` | Veterinarian: view pet-health questions | `Add Veterinarian pet-health questions` |
| 5 | Dorien | `5-Dorien-administrator.zip` | Administrator: search, browse and list users; demo guide; meeting notes | `Add Administrator user search, demo guide and meeting notes` |
| 6 | David | `6-David-expert-and-tests.zip` | Pet Health Expert: questions and posts in the approved specialty; all Sprint IV tests | `Add Pet Health Expert page and Sprint IV tests` |
| 7 | Makel | `7-Makel-moderator.zip` | Community Moderator: reported posts and advice; README run instructions | `Add Community Moderator reported content and run instructions` |

**David, after step 2:** in `frontend/src/auth/authApi.js` set `USE_TEST_USERS = false`, then commit and push (`Use database sign-in`). From then on, sign-in checks the database instead of the built-in test list. The password stays `PetMed123!`.

## How to add your part

In a terminal opened in your PetMed folder (the one with `backend`, `frontend` and `src`):

```powershell
git pull
Expand-Archive "$HOME\Downloads\<your zip name>.zip" -DestinationPath . -Force
git status
git add .
git commit -m "<your commit message from the table>"
git push
```

- `git status` should list only the files in your zip. If it shows anything else, ask before committing.
- If `git push` is rejected, run `git pull --no-edit` and then `git push` again.
- On macOS, unzip into the PetMed folder instead of using `Expand-Archive`.

## Then run the app on your own computer (everyone, this is checked)

Follow the five steps in [`src/README.md`](../src/README.md) once all steps above are pushed:

1. Rebuild the database with all five scripts, including the new `sample_data_sprint4.sql`.
2. `python -m pip install -r src/requirements.txt`
3. Copy `src/.env.example` to `src/.env` and put your own MySQL password in it. Never commit `src/.env`.
4. `python src/app.py` (the API, port 4000)
5. In a second terminal: `cd frontend`, `npm install`, `npm run dev`, then open <http://localhost:5173>.

Sign in with your role's sample account (password `PetMed123!`) and take a screenshot with your feature open. Save it as `evidence/Sprint4/<your-name>-running.png`, then commit and push it. That's your proof that you can pull and run the current system.

## Who explains what in the demo

| Member | Knows and presents |
|---|---|
| Dorien | GitHub and the team's commits; Administrator user search |
| David | Sign-in page, invalid sign-ins, dashboards and route guards; Pet Health Expert; running the tests |
| Miles | How the pages load data from the API; Pet Owner feed |
| Makai | How the server checks roles (`auth.py`, `@require_roles`); Veterinarian questions |
| Makel | Community Moderator reports; proving the data is live from MySQL |

Read your own files before Tuesday so you can explain them. The full demo order is in [`Sprint4_Demo_Guide.md`](Sprint4_Demo_Guide.md).
