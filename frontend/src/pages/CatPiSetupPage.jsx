import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { startPiSession } from '../api/catPiApi'
import { getResumes, uploadResume } from '../api/catPiResumeApi'
import { useCatPi } from '../context/CatPiContext'
import PageHeader from '../components/ui/PageHeader'
import { AI_FEATURES_DISABLED, AI_DISABLED_MESSAGE } from '../config/featureFlags'

const UPLOAD_NEW_VALUE = '__upload_new__'

export default function CatPiSetupPage() {
  const navigate = useNavigate()
  const { trackSession } = useCatPi()

  const [resumes, setResumes] = useState([])
  const [resumeId, setResumeId] = useState('')
  const [loadingResumes, setLoadingResumes] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [starting, setStarting] = useState(false)
  const [error, setError] = useState('')

  async function fetchResumes() {
    const data = await getResumes()
    setResumes(data)
    return data
  }

  useEffect(() => {
    fetchResumes()
      .catch(() => setError('Could not load your saved resumes.'))
      .finally(() => setLoadingResumes(false))
  }, [])

  async function handleResumeFileChange(e) {
    const file = e.target.files?.[0]
    e.target.value = ''
    if (!file) return

    setUploading(true)
    setError('')
    try {
      const uploaded = await uploadResume(file)
      const data = await fetchResumes()
      setResumeId(String(uploaded.resume_id ?? data[data.length - 1]?.id ?? ''))
    } catch (err) {
      setError(err?.response?.data?.detail || 'Resume upload failed.')
    } finally {
      setUploading(false)
    }
  }

  function handleResumeSelectChange(e) {
    if (e.target.value === UPLOAD_NEW_VALUE) return
    setResumeId(e.target.value)
  }

  async function handleStart() {
    setStarting(true)
    setError('')
    try {
      const data = await startPiSession(resumeId ? Number(resumeId) : null)
      trackSession(data.session_id, data.status)
      navigate(`/pi/${data.session_id}`)
    } catch (err) {
      setError(err?.response?.data?.detail || 'Could not start a PI session.')
    } finally {
      setStarting(false)
    }
  }

  if (starting) {
    return (
      <div className="page-container">
        <div className="card generating-card">
          <h1>Generating your interview...</h1>
          <p className="text-muted">
            One Gemini call is writing all ~8 questions up front — this usually takes 10-30s, longer if the
            model is under heavy load. Hang tight.
          </p>
          <div className="spinner" />
        </div>
      </div>
    )
  }

  return (
    <div className="page-container">
      <PageHeader
        eyebrow="PI practice"
        title="AI Personal Interview Practice"
        subtitle="A mock IIM-style panel will ask you ~8 questions spanning background, academics, current affairs, why-MBA, and situational topics — with voice input, question read-aloud, and optional delivery coaching via your mic/camera."
      />

      {AI_FEATURES_DISABLED && <div className="alert alert-error">{AI_DISABLED_MESSAGE}</div>}
      {error && <div className="alert alert-error">{error}</div>}

      <div className="ui-card">
        {loadingResumes ? (
          <p className="text-muted">Loading resumes...</p>
        ) : (
          <div className="form-group">
            <label>Resume (optional)</label>
            <select value={resumeId} onChange={handleResumeSelectChange} disabled={uploading || AI_FEATURES_DISABLED}>
              <option value="">No resume</option>
              {resumes.map((resume) => (
                <option key={resume.id} value={resume.id}>
                  {resume.original_filename}
                </option>
              ))}
              <option value={UPLOAD_NEW_VALUE}>Upload new resume...</option>
            </select>
            <input
              type="file"
              accept="application/pdf"
              onChange={handleResumeFileChange}
              disabled={uploading || AI_FEATURES_DISABLED}
            />
            <p className="text-muted">
              {uploading ? 'Uploading resume...' : 'Questions will be tailored to this resume, if selected.'}
            </p>
          </div>
        )}

        <button
          type="button"
          className="btn btn-primary"
          onClick={handleStart}
          disabled={starting || uploading || AI_FEATURES_DISABLED}
        >
          {starting ? 'Starting...' : 'Start Interview'}
        </button>
      </div>
    </div>
  )
}
