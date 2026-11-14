# PetMed: Sprint Cycle IV Demo Guide

**Presentation:** Tuesday, November 17, 2026. The demo is the working app, not slides.

## Before class

1. `git pull` so you run the current version from GitHub.
2. Rebuild the database with all five scripts (see [`src/README.md`](../src/README.md), step 1). This puts every list back to the expected starting data.
3. Check `USE_TEST_USERS = false` in `frontend/src/auth/authApi.js` (Makai's task), so sign-in uses the database.
4. Start the API: `python src/app.py`, then check <http://localhost:4000/api/health> shows `"users_in_database": 8`.
5. Start the website: `cd frontend`, then `npm run dev`. Open <http://localhost:5173>.
6. Keep a MySQL prompt open in a third terminal: `mysql -u root -p petmed`.
7. Run the tests once: `python -m pytest tests -v` should end with **23 passed**.

Every sample account uses the password **`PetMed123!`**.

## Demo order (about 10 minutes)

| # | Show | What to do | What the class should see |
|---|---|---|---|
| 1 | GitHub | Open the repo, then **Insights → Contributors** (or the commit list) | Sprint IV commits from all five members |
| 2 | Invalid sign-in | Click **Log In**, use `maya.johnson@petmed.com` with password `wrong` | "Invalid email or password." |
| 3 | Suspended account | Sign in as `sofia.ramirez@petmed.com` with the right password | "This account is suspended." |
| 3b | Sign up (optional) | Click **Create an account**, sign up as a new pet owner | Lands on the Pet Owner dashboard; the new user appears in Manage Users |
| 4 | Administrator | `daniel.owens@petmed.com`, then **Manage Users**. Search `carter`, then Role = Veterinarian, then Status = Suspended | 8 users; Dr. James Carter; 2 vets; Sofia Ramirez |
| 5 | Pet Owner | `maya.johnson@petmed.com`, then **Community Feed**. Search `garlic`, then clear it and click **#nutrition** | 8 posts; 1 post; 4 posts |
| 6 | Authorization (website) | Still as Maya, type `http://localhost:5173/admin/users` in the address bar | Access denied page |
| 7 | Authorization (server) | Run the two PowerShell lines below | The API refuses Maya with **403** |
| 8 | Veterinarian | `dr.james.carter@petmed.com`, then **Pet Health Questions**. Click each filter | All 6; Sent to me 1; Open to any vet 2; Unanswered 3 |
| 9 | Pet Health Expert | `kevin.nguyen@petmed.com`, then **Questions in My Expertise** | Specialty Nutrition: 2 questions sent to Kevin, 4 posts tagged #nutrition |
| 10 | Community Moderator | `tasha.brooks@petmed.com`, then **Reported Posts and Advice**. Switch the filters | 2 open reports (the garlic post and the cooked-bones advice); Resolved shows the older one |
| 11 | Real database | In the MySQL prompt run the INSERT below, then refresh Maya's feed | The new post appears at the top |
| 12 | Tests | Run `python -m pytest tests -v` | 23 passed |

Use **Log Out** between roles.

### Step 7: the server itself says no

Sign in to the API as Maya, then ask for the Administrator's user list:

```powershell
$t = (Invoke-RestMethod -Method Post -Uri http://localhost:4000/api/login -ContentType 'application/json' -Body '{"email":"maya.johnson@petmed.com","password":"PetMed123!"}').token
Invoke-RestMethod -Uri http://localhost:4000/api/admin/users -Headers @{ Authorization = "Bearer $t" }
```

The second line fails with **403** and "Your role is not allowed to use this feature." Hiding the menu isn't the only protection: the API checks the role on every request.

### Step 11: prove the data comes from MySQL

```sql
INSERT INTO Post (author_user_id, pet_id, body, post_type, status)
VALUES (87370000, 7380000, 'Live demo: Bella says hi to the class!', 'update', 'published');
```

Remove it afterward if you like:

```sql
DELETE FROM Post WHERE body = 'Live demo: Bella says hi to the class!';
```

## Who presents what

| Member | Part |
|---|---|
| Dorien Parris (Scrum Master) | Opening, GitHub (step 1), Administrator (step 4), closing |
| David Jean-Charles Bahidika | Sign-in page, invalid sign-ins, landing pages and the website guard (steps 2, 3, 6); Pet Health Expert and tests (steps 9, 12) |
| Miles Sharpton | Pet Owner feed (step 5) |
| Makai Lyn-Ah-Ping | How the server checks roles (step 7); Veterinarian (step 8) |
| Makel Dickerson | Community Moderator and the live database proof (steps 10, 11) |

## Testing checklist (do before Tuesday)

- [ ] All five roles sign in through the database and land on their own dashboard
- [ ] Wrong password is rejected; suspended account is rejected
- [ ] Each role's feature shows the expected data (table above)
- [ ] Another role's page shows Access denied, and the API answers 403 (step 7)
- [ ] `python -m pytest tests -v` shows 23 passed
- [ ] **Every member** has pulled and run the app on their own computer and saved a screenshot to `evidence/Sprint4/` (for example `evidence/Sprint4/miles-running.png`)
