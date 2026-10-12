import { useEffect, useState } from 'react'

// Shown once, right after the delivery-consent modal, while calibrate() runs on whichever
// analyzer(s) were enabled. A one-time, interview-level step - never repeated per question.
export default function DeliveryCalibrationScreen({ durationMs }) {
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    const startedAt = performance.now()

    let rafId
    const tick = () => {
      const pct = Math.min(100, ((performance.now() - startedAt) / durationMs) * 100)
      setProgress(pct)
      if (pct < 100) rafId = requestAnimationFrame(tick)
    }

    rafId = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(rafId)
  }, [durationMs])

  return (
    <div className="pi-modal-overlay">
      <div className="card pi-modal-card">
        <h2>Calibrating…</h2>
        <p>
          Stay quiet and look at the camera for a moment — this helps us calibrate to your room and camera
          setup so delivery feedback is more accurate.
        </p>
        <div className="pi-calibration-bar">
          <div className="pi-calibration-bar__fill" style={{ width: `${progress}%` }} />
        </div>
      </div>
    </div>
  )
}
