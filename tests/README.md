# PetMed Tests

`test_sprint4.py` checks the Sprint IV requirements against the real database:

| Group | What it proves |
|---|---|
| Sign-in | Each of the five roles signs in and the right role comes back; wrong password, unknown email, empty form and a suspended account are rejected |
| Sign up | A new Pet Owner can sign up and then sign in; a used email, a weak password, a missing name and a bad email are rejected (the test account is deleted afterward) |
| Role requests (`test_sprint5_role_requests.py`) | A new user requests a role and keeps only Pet Owner until an administrator approves; approval gives the role, rejection doesn't; vets must give credentials; bad or repeat requests are refused; only administrators can review |
| Authorization | No token or a fake token gets 401; each feature answers 200 for its own role and 403 for the other four; only the website's address may call the API |
| Retrieval | Each feature returns the expected rows from MySQL (user search, feed search and topic filter, vet question filters, expert specialty, reported content filters) |

Run from the repository root, after rebuilding the database with all five scripts (see `src/README.md`):

```powershell
python -m pytest tests -v
```

The tests leave the data as they found it, so you can run them as often as you like.
