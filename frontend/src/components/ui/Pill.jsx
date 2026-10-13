export default function Pill({ tone = 'neutral', children }) {
  return <span className={`ui-pill ui-pill-${tone}`}>{children}</span>
}
