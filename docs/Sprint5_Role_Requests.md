# PetMed: Role Requests (Sprint V)

After signing up, every new user is a **Pet Owner**. They can then **optionally** ask to also become a **Veterinarian**, **Pet Health Expert**, **Community Moderator** or **Administrator**. Nobody gets a role just by asking: an administrator approves or rejects each request.

## How it works

1. **Sign up.** The sign-up form has an **I'm signing up as** list: Pet Owner (the default), Veterinarian, Pet Health Expert, Community Moderator or Administrator. Choosing anything but Pet Owner shows a short request form (why, plus credentials for vets and experts). The account is created as a **Pet Owner** either way, and the chosen role becomes a pending request. If the request details are incomplete, no account is created.
2. **Pending request.** Users who chose another role land on **Request a Professional Role**, which shows their pending request. Pet Owners go straight to their dashboard. The same page is on the Pet Owner dashboard for asking later.
   - Veterinarians and Pet Health Experts also enter their license or credentials, specialty, workplace and experience. These are saved in `Professional_Profile` with status `pending`.
3. **Administrator review.** On the Administrator dashboard, **Role Requests** lists pending requests with each person's details. The administrator adds an optional note and clicks **Approve** or **Reject**.
   - Approve: the user gets the role (`User_Role`). For vets and experts, their profile becomes `approved` and the decision is logged in `Verification_Review`.
   - Reject: the user keeps their current roles and sees the note.
4. **Next sign-in.** The user lands on the dashboard of their highest role (Administrator → Moderator → Expert → Veterinarian → Pet Owner).

## Database

A new table, `Role_Request`, is in `backend/sprint5_role_requests.sql`. Run it after the other five scripts:

```powershell
cat sprint5_role_requests.sql | mysql -u root -p
```

| Column | Meaning |
|---|---|
| `request_id` | Auto-numbered ID |
| `user_id` | Who is asking (FK → `User`) |
| `role_id` | The role they want (FK → `Role`) |
| `reason` | Why they're asking |
| `status` | `pending`, `approved` or `rejected` (CHECK) |
| `requested_at` | When they asked |
| `reviewed_by_user_id` | The administrator who decided (FK → `User`) |
| `reviewed_at`, `review_notes` | When, and the note to the user |

It also adds one sample request: Marcus Williams asking to be a Community Moderator.

Add `Role_Request` to the ERD and the data dictionary when this branch is merged.

## Files

| File | What it does |
|---|---|
| `src/routes/role_requests.py` | Request, list and approve/reject endpoints |
| `src/auth.py` | Roles now come back most powerful first, so the landing page is the highest role |
| `frontend/src/pages/RequestRole.jsx` | The optional step after sign-up, and "My requests" |
| `frontend/src/pages/RoleRequests.jsx` | The administrator's review page |
| `frontend/src/pages/Signup.jsx` | Sends new users to the optional step |
| `src/routes/signup.py` | Accepts the optional user type and saves it as a pending request |
| `tests/test_sprint5_role_requests.py` | 8 tests; all accounts they create are deleted afterward |
