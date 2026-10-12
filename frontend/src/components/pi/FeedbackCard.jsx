export default function FeedbackCard({ score, feedback, strengths = [], improvements = [], deliveryFeedback, modelAnswer }) {
  return (
    <div className="card evaluation-card">
      <h2>Feedback on your last answer</h2>
      <div className="stat-value">{score}</div>
      <div className="stat-label">Score out of 10</div>
      <p className="feedback-text">{feedback}</p>

      {strengths.length > 0 && (
        <div>
          <strong>Strengths</strong>
          <ul>
            {strengths.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {improvements.length > 0 && (
        <div>
          <strong>Areas to improve</strong>
          <ul>
            {improvements.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {modelAnswer && (
        <div className="pi-model-answer">
          <strong>Model answer</strong>
          <p className="feedback-text">{modelAnswer}</p>
        </div>
      )}

      {deliveryFeedback && (
        <div className="pi-delivery-feedback">
          <strong>Delivery</strong>
          <p className="feedback-text">{deliveryFeedback}</p>
        </div>
      )}
    </div>
  )
}
