import { useState } from 'react'
import { formatDate } from '../api/petmedApi.js'
import useApiData from '../api/useApiData.js'
import ReportButton from '../components/ReportButton.jsx'
import UseCaseLayout from '../components/UseCaseLayout.jsx'

// ------------------------------------------------------------
// Pet Owner use case: browse and search the community feed.
// Data: GET /api/feed?q=&tag=  (src/routes/owner.py)
// ------------------------------------------------------------

const TYPE_LABELS = { question: 'Question', tip: 'Tip', update: 'Update' }

function CommunityFeed() {
  const [text, setText] = useState('')
  const [search, setSearch] = useState('')
  const [tag, setTag] = useState('')

  const result = useApiData(`/feed?${new URLSearchParams({ q: search, tag })}`)
  const d = result.status === 200 ? result.data : null

  return (
    <UseCaseLayout title="Community Feed" subtitle="Pet health posts and discussions from the PetMed community." result={result}>
      <form className="uc-toolbar" onSubmit={(e) => { e.preventDefault(); setSearch(text.trim()) }}>
        <input type="search" placeholder="Search posts, people or pets" value={text}
               onChange={(e) => setText(e.target.value)} aria-label="Search the feed" />
        <button className="primary-button uc-button" type="submit">Search</button>
        <button type="button" className="uc-chip" onClick={() => { setText(''); setSearch(''); setTag('') }}>Clear</button>
      </form>

      {d && (
        <>
          <div className="uc-chips" role="group" aria-label="Filter by topic">
            <button type="button" className={tag === '' ? 'uc-chip active' : 'uc-chip'} onClick={() => setTag('')}>All topics</button>
            {d.tags.map((t) => (
              <button type="button" key={t} className={tag === t ? 'uc-chip active' : 'uc-chip'} onClick={() => setTag(t)}>#{t}</button>
            ))}
          </div>
          <p className="uc-count">{d.count} {d.count === 1 ? 'post' : 'posts'}</p>

          <div className="uc-list">
            {d.posts.map((p) => (
              <article key={p.post_id} className="uc-card">
                <header className="uc-card-head">
                  <span className="uc-avatar" aria-hidden="true">{p.author[0]}</span>
                  <div>
                    <strong>{p.author}</strong>
                    <div className="uc-muted uc-small">
                      {formatDate(p.created_at)}{p.pet_name && <> · about {p.pet_name} ({p.pet_species})</>}
                    </div>
                  </div>
                  <span className={`uc-pill uc-pill-${p.post_type}`}>{TYPE_LABELS[p.post_type] || p.post_type}</span>
                </header>
                <p className="uc-body">{p.body}</p>
                {p.tags.length > 0 && <div className="uc-tags">{p.tags.map((t) => <span key={t}>#{t}</span>)}</div>}
                <footer className="uc-card-foot">
                  <span>❤️ {p.likes}</span>
                  <span>💬 {p.comments}</span>
                </footer>
                <ReportButton postId={p.post_id} />
                {p.comment_list.length > 0 && (
                  <ul className="uc-comments">
                    {p.comment_list.map((c, i) => <li key={i}><strong>{c.author}</strong> {c.body}</li>)}
                  </ul>
                )}
              </article>
            ))}
            {d.count === 0 && <p className="uc-empty">No posts match your search.</p>}
          </div>
        </>
      )}
    </UseCaseLayout>
  )
}

export default CommunityFeed
