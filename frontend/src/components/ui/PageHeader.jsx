export default function PageHeader({ eyebrow, title, subtitle, stats, actions, breadcrumb }) {
  return (
    <div className="ui-slab">
      <div className="ui-slab-copy">
        {breadcrumb && breadcrumb.length > 0 && (
          <div className="ui-breadcrumb">
            {breadcrumb.map((crumb, idx) => (
              <span key={crumb.label}>
                {idx > 0 && <span className="ui-breadcrumb-sep">›</span>}
                {crumb.onClick ? (
                  <button type="button" className="ui-breadcrumb-item" onClick={crumb.onClick}>
                    {crumb.label}
                  </button>
                ) : (
                  <span className="ui-breadcrumb-item ui-breadcrumb-item-current">{crumb.label}</span>
                )}
              </span>
            ))}
          </div>
        )}
        {eyebrow && <div className="ui-eyebrow">{eyebrow}</div>}
        <h1 className="ui-slab-title">{title}</h1>
        {subtitle && <p className="ui-slab-subtitle">{subtitle}</p>}
        {actions && <div className="ui-slab-actions">{actions}</div>}
      </div>
      {stats && stats.length > 0 && (
        <div className="ui-slab-stats">
          {stats.map((s) => (
            <div className="ui-slab-stat" key={s.label}>
              <div
                className="ui-slab-stat-value"
                style={s.accent ? { color: 'var(--ui-primary)' } : undefined}
              >
                {s.value}
              </div>
              <div className="ui-slab-stat-label">{s.label}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
