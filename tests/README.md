# PetMed Tests

`test_sprint4.py` checks the Sprint IV requirements against the real database:

| Group | What it proves |
|---|---|
| Sign-in | Each of the five roles signs in and the right role comes back; wrong password, unknown email, empty form and a suspended account are rejected |
| Authorization | No token or a fake token gets 401; each feature answers 200 for its own role and 403 for the other four; only the website's address may call the API |
| Retrieval | Each feature returns the expected rows from MySQL (user search, feed search and topic filter, vet question filters, expert specialty, reported content filters) |

Run from the repository root, after rebuilding the database with all five scripts (see `src/README.md`):

```powershell
python -m pytest tests -v
```

The tests only read data, so you can run them as often as you like.
