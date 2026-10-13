export default function ListRow({ title, meta, actions }) {
  return (
    <div className="ui-list-row">
      <div className="ui-list-row-main">
        <div className="ui-list-row-title">{title}</div>
        {meta && <div className="ui-list-row-meta">{meta}</div>}
      </div>
      {actions && <div className="ui-list-row-actions">{actions}</div>}
    </div>
  )
}
