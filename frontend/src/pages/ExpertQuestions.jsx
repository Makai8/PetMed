import { useState } from 'react'
import { formatDate } from '../api/petmedApi.js'
import useApiData from '../api/useApiData.js'
import UseCaseLayout from '../components/UseCaseLayout.jsx'

// ------------------------------------------------------------
// Pet Health Expert use cases
// Sprint IV: browse questions and posts in the expert's approved
//   area of expertise.  GET /api/expert/topics?q=
// Sprint V: answer a question inside that area.
//   POST /api/expert/questions/<question_id>/answer {response_text}
// (src/routes/expert.py)
// ------------------------------------------------------------

function ExpertQuestions() {
  const [text, setText] = useState('')
  const [search, setSearch] = useState('')

  const result = useApiData(`/expert/topics?${new URLSearchParams({ q: search })}`)
  const d = result.status === 200 ? result.data : null

  return (
    <UseCaseLayout title="Questions in My Expertise" subtitle="Questions and posts in your approved area of expertise." result={result}>
      {d && (
        <p className="uc-specialty">
          Approved specialty: <span className="uc-pill uc-pill-mine">{d.specialty}</span>
          {d.organization && <span className="uc-muted"> · {d.organization}</span>}
        </p>
      )}
      <form className="uc-toolbar" onSubmit={(e) => { e.preventDefault(); setSearch(text.trim()) }}>
        <input type="search" placeholder="Search within your specialty" value={text}
               onChange={(e) => setText(e.target.value)} aria-label="Search your specialty" />
        <button className="primary-button uc-button" type="submit">Search</button>
      </form>

      {d && (
        <div className="uc-two-col">
          <section>
            <h2 className="uc-section-title">Questions sent to you ({d.questions.length})</h2>
            <div className="uc-list">
              {d.questions.map((item) => (
                <article key={item.question_id} className="uc-card">
                  <p className="uc-body uc-quote">“{item.question_text}”</p>
                  <p className="uc-muted uc-small">
                    {item.asked_by}{item.pet_name && <> · {item.pet_name} ({item.pet_species})</>} · {formatDate(item.created_at)}
                  </p>
                  {item.answers > 0
                    ? <span className="uc-pill uc-pill-answered">{item.answers} {item.answers === 1 ? 'answer' : 'answers'}</span>
                    : <span className="uc-unanswered">No answers yet</span>}

                  {/* MILES: add the answer form here (Sprint V). See docs/Sprint5_Team_Tasks.md */}
                </article>
              ))}
              {d.questions.length === 0 && <p className="uc-empty">No questions match.</p>}
            </div>
          </section>
          <section>
            <h2 className="uc-section-title">Posts tagged #{d.tag} ({d.posts.length})</h2>
            <div className="uc-list">
              {d.posts.map((p) => (
                <article key={p.post_id} className="uc-card">
                  <p className="uc-body">{p.body}</p>
                  <p className="uc-muted uc-small">
                    {p.author}{p.pet_name && <> · about {p.pet_name}</>} · {formatDate(p.created_at)}
                  </p>
                </article>
              ))}
              {d.posts.length === 0 && <p className="uc-empty">No posts match.</p>}
            </div>
          </section>
        </div>
      )}
    </UseCaseLayout>
  )
}

export default ExpertQuestions
