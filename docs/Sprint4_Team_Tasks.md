# PetMed: Sprint Cycle IV Team Tasks

**Scrum Master:** Dorien Parris · **Presentation:** Tuesday, November 17, 2026

## Already on GitHub

- **David:** website foundation: sign-in page, role dashboards, route guards, log out.
- **Dorien:** Sprint IV sample data, the Python API (`src/`, port 4000), the five database-backed role pages, tests, demo guide and meeting notes.

## Your task (Makai, Miles, Makel)

Each task is a small change to your role's page. Commit and push it **from your own GitHub account**. That's how the instructor checks that everyone contributed.

Before starting, get the latest code:

```powershell
git pull
```

### Makai: connect sign-in to the database + unanswered count (Veterinarian)

1. In `frontend/src/auth/authApi.js`, change line 8 from `const USE_TEST_USERS = true` to:

   ```js
   const USE_TEST_USERS = false
   ```

   Sign-in now checks the database through the API instead of the built-in test list.

2. In `frontend/src/pages/HealthQuestions.jsx`, find this line:

   ```jsx
   <p className="uc-count">{d.count} {d.count === 1 ? 'question' : 'questions'}</p>
   ```

   and replace it with:

   ```jsx
   <p className="uc-count">{d.count} {d.count === 1 ? 'question' : 'questions'} · {d.questions.filter((item) => item.answer_list.length === 0).length} unanswered</p>
   ```

   Check: signed in as Dr. Carter, Pet Health Questions shows **6 questions · 3 unanswered**.

```powershell
git add frontend/src/auth/authApi.js frontend/src/pages/HealthQuestions.jsx
git commit -m "Use database sign-in and show unanswered count for vets"
git push
```

### Miles: Clear button (Pet Owner community feed)

In `frontend/src/pages/CommunityFeed.jsx`, find this line:

```jsx
        <button className="primary-button uc-button" type="submit">Search</button>
```

and add this line right below it:

```jsx
        <button type="button" className="uc-chip" onClick={() => { setText(''); setSearch(''); setTag('') }}>Clear</button>
```

Check: signed in as Maya, click **#nutrition** (4 posts), then **Clear** (back to 8 posts).

```powershell
git add frontend/src/pages/CommunityFeed.jsx
git commit -m "Add Clear button to the community feed"
git push
```

### Makel: "Assigned to you" label (Community Moderator)

In `frontend/src/pages/ReportedContent.jsx`:

1. Below the line `import UseCaseLayout from '../components/UseCaseLayout.jsx'`, add:

   ```jsx
   import { useAuth } from '../auth/AuthContext.jsx'
   ```

2. Right below `function ReportedContent() {`, add:

   ```jsx
     const { user } = useAuth()
   ```

3. Find the line that starts with `<span className="uc-muted uc-small">Report #` and add this line right below it:

   ```jsx
                     {r.assigned_to === user.name && <span className="uc-pill uc-pill-mine">Assigned to you</span>}
   ```

Check: signed in as Tasha, the garlic report shows **Assigned to you**.

```powershell
git add frontend/src/pages/ReportedContent.jsx
git commit -m "Show which reports are assigned to the signed-in moderator"
git push
```

If `git push` is rejected, run `git pull --no-edit`, then `git push` again.

## Everyone: run the app on your own computer (this is checked)

Follow the five steps in [`src/README.md`](../src/README.md):

1. Rebuild the database with all five scripts, including `sample_data_sprint4.sql`.
2. `python -m pip install -r src/requirements.txt`
3. Copy `src/.env.example` to `src/.env` and put your own MySQL password in it. Never commit `src/.env`.
4. `python src/app.py` (the API, port 4000)
5. In a second terminal: `cd frontend`, `npm install`, `npm run dev`, then open <http://localhost:5173>.

Sign in with your role's account (password `PetMed123!`), open your feature, and take a screenshot. Save it as `evidence/Sprint4/<your-name>-running.png`, then commit and push it.

| Member | Sign in as | Feature to screenshot |
|---|---|---|
| Dorien | `daniel.owens@petmed.com` | Manage Users |
| David | `kevin.nguyen@petmed.com` | Questions in My Expertise |
| Makai | `dr.james.carter@petmed.com` | Pet Health Questions |
| Miles | `maya.johnson@petmed.com` | Community Feed |
| Makel | `tasha.brooks@petmed.com` | Reported Posts and Advice |

## Who explains what in the demo

| Member | Presents |
|---|---|
| Dorien | GitHub and the team's commits; Administrator user search |
| David | Sign-in page, invalid sign-ins, dashboards and route guards; Pet Health Expert; running the tests |
| Miles | Pet Owner feed |
| Makai | How the server checks roles (`src/auth.py`); Veterinarian questions |
| Makel | Community Moderator reports; proving the data is live from MySQL |

Read the files for your part before Tuesday so you can explain them. The full demo order is in [`Sprint4_Demo_Guide.md`](Sprint4_Demo_Guide.md).
