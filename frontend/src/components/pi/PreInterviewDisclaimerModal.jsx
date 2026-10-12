export default function PreInterviewDisclaimerModal({ onAcknowledge }) {
  return (
    <div className="pi-modal-overlay">
      <div className="card pi-modal-card">
        <h2>Before you begin</h2>

        <p>
          This is a mock IIM Personal Interview panel — it may probe your background, academics, current
          affairs knowledge, and why you want an MBA, the way a real panel would. Questions can get
          pointed; that's intentional.
        </p>

        <p>
          If a question is hard or the feedback is blunt, don't get discouraged. Every practice run is a
          chance to improve, and the only way to get better is to keep going.
        </p>

        <div className="pi-modal-actions">
          <button type="button" className="btn btn-primary" onClick={onAcknowledge}>
            OK, let's go
          </button>
        </div>
      </div>
    </div>
  )
}
