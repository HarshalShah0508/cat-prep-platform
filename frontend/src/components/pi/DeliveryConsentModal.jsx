import { useState } from 'react'

export default function DeliveryConsentModal({ onContinue, onDecline }) {
  const [audioEnabled, setAudioEnabled] = useState(true)
  const [videoEnabled, setVideoEnabled] = useState(true)

  return (
    <div className="pi-modal-overlay">
      <div className="card pi-modal-card">
        <h2>Get delivery feedback too?</h2>

        <p>
          We can analyze your microphone and camera in the background to give you feedback on delivery —
          pauses, hesitation, eye contact, fidgeting.
        </p>

        <p>
          <strong>Nothing is recorded or stored.</strong> Only small summary numbers (like a pause count or
          eye-contact percentage) ever leave your device — your audio and video never do.
        </p>

        <label className="pi-modal-toggle">
          <input type="checkbox" checked={audioEnabled} onChange={(e) => setAudioEnabled(e.target.checked)} />
          Analyze voice delivery (pauses, pacing)
        </label>

        <label className="pi-modal-toggle">
          <input type="checkbox" checked={videoEnabled} onChange={(e) => setVideoEnabled(e.target.checked)} />
          Analyze body language via camera (eye contact, fidgeting)
        </label>

        <div className="pi-modal-actions">
          <button type="button" className="btn btn-secondary" onClick={onDecline}>
            Skip, take interview as-is
          </button>
          <button
            type="button"
            className="btn btn-primary"
            onClick={() => onContinue({ audioEnabled, videoEnabled })}
            disabled={!audioEnabled && !videoEnabled}
          >
            Continue
          </button>
        </div>
      </div>
    </div>
  )
}
