# PetMed API (Python + Flask)

The server behind the PetMed website. It runs on port 4000, checks sign-ins, works out each user's role, blocks features the role may not use, and reads data from the MySQL database built in Sprint III.

## Run the whole app (every team member)

You need **Python 3.10+**, **Node.js**, **MySQL** and the `petmed` database.

**1. Rebuild the database with the Sprint IV and V data.** From the `backend` folder:

```powershell
mysql -u root -p -e "DROP DATABASE IF EXISTS petmed;"
cat PetMedDB.sql | mysql -u root -p
cat seed.sql | mysql -u root -p
cat sample_data_health_records.sql | mysql -u root -p
cat sample_data_more.sql | mysql -u root -p
cat sample_data_sprint4.sql | mysql -u root -p
cat sprint5_role_requests.sql | mysql -u root -p
cat sprint5_sample_data.sql | mysql -u root -p
```

**2. Install the Python packages (once).** From the repository root:

```powershell
python -m pip install -r src/requirements.txt
```

If `python` isn't found on Windows, use `py` instead.

**3. Add your database password (once).** Copy `src/.env.example` to `src/.env` and put your MySQL root password on the `DB_PASSWORD=` line. `src/.env` is ignored by Git, so the password stays on your computer.

```powershell
Copy-Item src/.env.example src/.env
code src/.env
```

**4. Start the API.** In a terminal at the repository root:

```powershell
python src/app.py
```

Check it: <http://localhost:4000/api/health> should show `"users_in_database": 8`.

**5. Start the website.** Make sure `USE_TEST_USERS` is `false` in `frontend/src/auth/authApi.js`, so sign-in checks the database instead of the built-in test list. Then, in a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open <http://localhost:5173> and click **Log In**. Use `npm.cmd` instead of `npm` if PowerShell blocks `npm.ps1`.

## Sample accounts

Every sample account uses the demo password **`PetMed123!`** (the database stores only a hash of it).

| Role | Email | What works in Sprint IV |
|---|---|---|
| Administrator | `daniel.owens@petmed.com` | Manage Users: search, browse and list users |
| Pet Owner | `maya.johnson@petmed.com` | Community Feed: browse and search posts |
| Veterinarian | `dr.james.carter@petmed.com` | Pet Health Questions from owners |
| Pet Health Expert | `kevin.nguyen@petmed.com` | Questions in My Expertise (Nutrition) |
| Community Moderator | `tasha.brooks@petmed.com` | Reported Posts and Advice |
| Suspended pet owner | `sofia.ramirez@petmed.com` | Sign-in is refused |

## How sign-in and authorization work

1. **Sign-in:** `POST /api/login` finds the user by email and checks the password against the hash in `User.password_hash`. A wrong email and a wrong password get the same message. Suspended accounts are refused.
2. **Role identification:** the server reads the user's roles from `User_Role` → `Role` and returns them with a signed token (valid 8 hours).
3. **Authorization:** every feature route has `@require_roles(...)`. On each request the server reads the token, loads the user and roles from the database again, and answers **403** if the role is not allowed. The website's `RequireRole` guard also sends users away from other roles' pages, but the server check is what actually protects the data.

| Endpoint | Allowed role | File |
|---|---|---|
| `POST /api/login`, `GET /api/me` | anyone / any signed-in user | `auth.py` |
| `POST /api/signup` (creates a Pet Owner account) | anyone | `routes/signup.py` |
| `POST /api/role-requests`, `GET /api/role-requests/mine` (ask for an extra role) | any signed-in user | `routes/role_requests.py` |
| `GET /api/admin/role-requests?status=`, `POST /api/admin/role-requests/<id>/approve\|reject` | administrator | `routes/role_requests.py` |
| `GET /api/admin/users?q=&role=&status=` | administrator | `routes/admin.py` |
| `GET /api/feed?q=&tag=` | pet_owner | `routes/owner.py` |
| `GET /api/vet/questions?show=all\|mine\|open\|unanswered&q=` | veterinarian | `routes/vet.py` |
| `GET /api/expert/topics?q=` | pet_health_expert (approved profile only) | `routes/expert.py` |
| `GET /api/moderation/reports?type=all\|post\|advice&status=open\|resolved\|all` | community_moderator | `routes/moderator.py` |
| **Sprint V** `GET /api/admin/professionals?status=`, `POST /api/admin/professionals/<profile_id>/status` | administrator | `routes/verification.py` |
| **Sprint V** `GET /api/owner/pets`, `GET /api/owner/symptoms`, `POST /api/owner/symptoms` | pet_owner | `routes/symptoms.py` |
| **Sprint V** `POST /api/vet/questions/<question_id>/answer` | veterinarian (verified) | `routes/vet.py` |
| **Sprint V** `POST /api/expert/questions/<question_id>/answer` | pet_health_expert (approved, own questions) | `routes/expert.py` |
| **Sprint V** `POST /api/moderation/reports/<report_id>/decision` | community_moderator | `routes/moderator.py` |

## Files

| File | What it does |
|---|---|
| `app.py` | Starts the server on port 4000, registers every route, and lets the website (port 5173) call it |
| `config.py` | Reads settings from `src/.env` |
| `db.py` | Opens the MySQL connection and runs queries |
| `auth.py` | Sign-in, tokens, and the `@require_roles` check |
| `helpers.py` | Sprint V helpers for checking form data and logging actions (`missing`, `one_of`, `clean`, `log_event`) |
| `routes/*.py` | One file per role's use cases (Sprint IV reads data, Sprint V adds or changes it) |

## Run the tests

With the database rebuilt (step 1) and `src/.env` filled in:

```powershell
python -m pytest tests -v
```

31 tests cover sign-in for every role, rejected sign-ins, sign up, the role checks on every feature, and the data each feature returns.
