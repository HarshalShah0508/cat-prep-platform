const STATUS_CLASS = {
  not_visited: 'palette-cell-not-visited',
  not_answered: 'palette-cell-not-answered',
  answered: 'palette-cell-answered',
  marked_for_review: 'palette-cell-marked',
  answered_marked_for_review: 'palette-cell-marked palette-cell-marked-answered',
}

export default function QuestionPalette({ questions, currentIndex, onJump }) {
  return (
    <div className="question-palette">
      <h3 className="palette-title">Questions</h3>
      <div className="palette-grid">
        {questions.map((q, idx) => (
          <button
            key={q.id}
            type="button"
            className={`palette-cell ${STATUS_CLASS[q.status] || STATUS_CLASS.not_visited} ${
              idx === currentIndex ? 'palette-cell-current' : ''
            }`}
            onClick={() => onJump(idx)}
          >
            {idx + 1}
          </button>
        ))}
      </div>
      <div className="palette-legend">
        <span>
          <span className="palette-swatch palette-cell-not-visited" /> Not visited
        </span>
        <span>
          <span className="palette-swatch palette-cell-not-answered" /> Not answered
        </span>
        <span>
          <span className="palette-swatch palette-cell-answered" /> Answered
        </span>
        <span>
          <span className="palette-swatch palette-cell-marked" /> Marked for review
        </span>
        <span>
          <span className="palette-swatch palette-cell-marked palette-cell-marked-answered" /> Answered
          &amp; marked for review
        </span>
      </div>
    </div>
  )
}
