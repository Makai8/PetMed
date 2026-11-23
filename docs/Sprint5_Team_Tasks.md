# Sprint V – Team Tasks (Adding and Modifying Data)

**Video due:** November 24 (check Canvas for the exact day and time). Submit it on Canvas and link it in the README.
**Scrum Master:** Dorien Parris

Each person builds one Sprint V use case and pushes it **from their own GitHub account**.
The Administrator use case (`routes/verification.py` + `pages/Verification.jsx`) is the
worked example: every other use case follows the same pattern.

| Person | Share | Use case | Files |
|---|---|---|---|
| Dorien Parris | 40% | Shared setup + **Administrator:** review a vet or expert and update the verification status | `backend/sprint5_sample_data.sql`, `src/helpers.py`, `src/routes/verification.py`, `pages/Verification.jsx`, the read-only lists the other pages need, menus and routes, all Sprint V tests, demo script, meeting notes |
| David Jean-Charles Bahidika | 15% | **Pet Owner:** record a symptom or health event for a pet | `src/routes/symptoms.py` → `record_symptom()`, `pages/SymptomTracker.jsx` → the form |
| Makai Lyn-Ah-Ping | 15% | **Veterinarian:** give general guidance on a pet owner's question | `src/routes/vet.py` → `answer_question()`, `pages/HealthQuestions.jsx` → the answer box |
| Miles Sharpton | 15% | **Pet Health Expert:** answer a question in the approved area of expertise | `src/routes/expert.py` → `answer_question()`, `pages/ExpertQuestions.jsx` → the answer box |
| Makel Dickerson | 15% | **Community Moderator:** review a report and update the moderation case | `src/routes/moderator.py` → `decide_report()`, `pages/ReportedContent.jsx` → the decision form + the "Assigned to you" fix |

## Before you start (everyone)

```powershell
git pull
```

Rebuild the database so you have the Sprint V sample data (from the `backend` folder):

```powershell
mysql -u root -p -e "DROP DATABASE IF EXISTS petmed;"
Get-Content PetMedDB.sql, seed.sql, sample_data_health_records.sql, sample_data_more.sql, sample_data_sprint4.sql, sprint5_role_requests.sql, sprint5_sample_data.sql | mysql -u root -p
```

Then start the API (`python src/app.py`) and the website (`npm.cmd run dev` in `frontend`).
All sample accounts use the password `PetMed123!`.

## How every Sprint V use case works

Open `src/routes/verification.py` and `frontend/src/pages/Verification.jsx` side by side. They show the whole pattern:

**API (Python)**
1. Read the JSON the page sent: `data = request.get_json(silent=True) or {}`
2. Check it with the helpers in `src/helpers.py` (`missing`, `one_of`, `clean`). Bad data → `return jsonify(message=...), 400` and **save nothing**.
3. Check the rules (does the pet belong to this owner? is this vet verified? is the report still open?) → 403, 404 or 409.
4. Save with `execute(...)`, then `log_event(...)`.
5. Answer `201` (new row) or `200` (changed row) with the saved data.

**Page (React)**
1. Keep what the user typed in `useState`.
2. On submit: `const res = await apiPost('/the/url', body, user.token)`.
3. `res.ok` → show `res.data.message` in a green `uc-success` box and call `result.reload()` so the list shows the change.
   Not ok → show `res.data.message` in a red `login-error` box.

Your route currently answers **501 "Not built yet"**. Replace the stub by following the numbered
comments in your function, then delete the `return ... 501` line.

## Definition of done

1. `python -m pytest tests -k <YourPart> -v` shows your tests **PASSED** (not SKIPPED):
   David `Symptoms`, Makai `Vet`, Miles `Expert`, Makel `Moderator`.
2. `python -m pytest tests` still passes everything else (the old features still work).
3. In the browser: one good save and one invalid attempt that shows the error message.
4. A screenshot of each in `evidence/Sprint5/<your-name>-*.png`.
5. Commit and push from **your own** account:
   ```powershell
   git add -A
   git commit -m "Sprint V: <your use case>"
   git pull --rebase
   git push
   ```

---

## David – Pet Owner: Symptom Tracker

**API:** `record_symptom()` in `src/routes/symptoms.py`. The two GET routes above it (your pets and the
history) are already done. Follow the 7 numbered steps in the function.

**Page:** `frontend/src/pages/SymptomTracker.jsx`. The history list on the right already works.
Build the form on the left (the comment in the file lists every field). You'll need:

```jsx
import { apiPost, formatDate } from '../api/petmedApi.js'
import { useAuth } from '../auth/AuthContext.jsx'
...
const { user } = useAuth()
const [form, setForm] = useState({ ...EMPTY, observed_at: nowForInput() })
const [message, setMessage] = useState(null)
const [saving, setSaving] = useState(false)
const [newId, setNewId] = useState(null)

function change(e) {
  setForm({ ...form, [e.target.name]: e.target.value })
}
```

**Check:** sign in as `maya.johnson@petmed.com`. Save "Sneezing after walks" for Bella → it appears at the
top of the history. Save with no pet chosen → red message "Please fill in which pet."

## Makai – Veterinarian: Answer a question

**API:** `answer_question()` at the bottom of `src/routes/vet.py`. Follow the 7 numbered steps.

**Page:** `frontend/src/pages/HealthQuestions.jsx`. Where the `MAKAI` comment is, inside each question card, add an
answer box:

- Show it only when the question is sent to you or open to any vet, and you haven't answered yet:
  `(item.sent_to_me || !item.sent_to) && !item.answer_list.some((a) => a.author === user.name)`
- A `<form className="uc-reply">` with a label "Your guidance", a `<textarea>` and a "Post guidance" button.
- Keep one draft per question: `const [drafts, setDrafts] = useState({})`, and
  `setDrafts({ ...drafts, [item.question_id]: e.target.value })`.
- On submit: `apiPost(`/vet/questions/${item.question_id}/answer`, { response_text: drafts[item.question_id] || '' }, user.token)`,
  show the message under that card, and `result.reload()` when it worked.

**Check:** sign in as `dr.james.carter@petmed.com` → "Sent to me" → answer Bella's water question → your answer
appears under it. Try "Go to a vet." → "Write at least 20 characters of guidance."

## Miles – Pet Health Expert: Answer in my expertise

**Implemented and verified locally on November 23, 2026.** The API saves the expert's
answer and audit event in MySQL, rejects short answers and duplicate submissions,
and restricts answers to approved experts and questions directed to them.
The page shows a specialty-labelled answer form, validation feedback, and the updated answer count after saving.

Verification: `python -m pytest tests -k Expert -v` reports **7 passed**, including all five
Sprint V expert tests. Full suite: **52 passed, 8 skipped, 43 subtests passed**; the skips
are unfinished Owner, Veterinarian, and Moderator starter routes. Production build and
ESLint on `ExpertQuestions.jsx` pass. Tests additionally check the audit event,
duplicate rejection, and empty/malformed answer payloads.

Browser evidence: [invalid answer](../evidence/Sprint5/miles-invalid.png) and
[successful save](../evidence/Sprint5/miles-saved.png). Both were captured against local
MySQL, and the saved `Advice_Response` and `Audit_Event` were verified directly.
Only the answer created during browser verification was removed afterward, so the
treats question is ready to demonstrate again. Existing local data was backed up before
applying the two missing Sprint V setup scripts.

**API:** `answer_question()` at the bottom of `src/routes/expert.py`. Follow the 7 numbered steps.

**Page:** `frontend/src/pages/ExpertQuestions.jsx`. Where the `MILES` comment is, add the same kind of answer box as
Makai's, shown when `item.answers === 0`, labelled `Your answer ({d.specialty})`, posting to
`/expert/questions/${item.question_id}/answer`.

**Check:** sign in as `kevin.nguyen@petmed.com` → answer the treats question → the card changes to "1 answer".
For the outside-your-area case, the test posts to Luna's question (not sent to Kevin) and expects 403.

## Makel – Community Moderator: Review a report

**API:** `decide_report()` at the bottom of `src/routes/moderator.py`. Follow the 8 numbered steps. `ACTIONS` and
`REMOVED_TEXT` are already defined above it.

**Page:** `frontend/src/pages/ReportedContent.jsx`.

1. **Fix the "Assigned to you" label:** it compares `r.assigned_to === 'Tasha'`, but `assigned_to` is the full name
   ("Tasha Brooks"). Use the signed-in user instead: `r.assigned_to === user.name`
   (`const { user } = useAuth()`).
2. Where the `MAKEL` comment is, for open reports (`r.status === 'open'`), add a `<form className="uc-reply">` with:
   - an "Action" `<select>` built from `ACTIONS` (already at the top of the file),
   - a "Reason" `<textarea>`,
   - a "Save decision" button that posts `{ action, reason }` to `/moderation/reports/${r.report_id}/decision`.
   Keep one `{ action, reason }` per report in state. After it works, show the message at the top of the list and
   `result.reload()` (the report moves to "Resolved").

**Check:** sign in as `tasha.brooks@petmed.com` → the garlic post → "Remove the content" with a reason → it moves to
Resolved, and the post disappears from Maya's Community Feed. Save with no reason → "Please fill in reason."

---

## If you're stuck

Run your tests with `-v` and read the first failure: it says which status code or value it expected.
Ask in the group chat before Sunday night so there's time to help before the video.
