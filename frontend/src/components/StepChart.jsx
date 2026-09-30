const WIDTH = 800
const HEIGHT = 360
const MARGIN = { top: 20, right: 24, bottom: 46, left: 56 }

function buildStepPath(points, xScale, yScale) {
  if (!points || points.length === 0) return ''
  let d = `M ${xScale(points[0][0])} ${yScale(points[0][1])}`
  for (let i = 1; i < points.length; i++) {
    const [x, y] = points[i]
    const [, prevY] = points[i - 1]
    // Horizontal hold at the previous value, then a vertical step up to the new one.
    d += ` L ${xScale(x)} ${yScale(prevY)} L ${xScale(x)} ${yScale(y)}`
  }
  return d
}

function SingleChart({ title, x_label, y_label, x_max, y_max, series }) {
  const innerWidth = WIDTH - MARGIN.left - MARGIN.right
  const innerHeight = HEIGHT - MARGIN.top - MARGIN.bottom
  const xMax = x_max ?? Math.max(1, ...series.flatMap((s) => s.points.map((p) => p[0])))
  const yMax = y_max ?? Math.max(1, ...series.flatMap((s) => s.points.map((p) => p[1])))

  const xScale = (x) => MARGIN.left + (x / xMax) * innerWidth
  const yScale = (y) => MARGIN.top + innerHeight - (y / yMax) * innerHeight

  const xTicks = []
  for (let x = 0; x <= xMax; x += Math.max(1, Math.round(xMax / 8))) xTicks.push(x)
  const yTicks = []
  for (let y = 0; y <= yMax; y += 1) yTicks.push(y)

  return (
    <div className="step-chart">
      {title && <div className="step-chart-title">{title}</div>}
      <svg
        viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
        className="step-chart-svg"
        role="img"
        aria-label={title || 'chart'}
      >
        {yTicks.map((y) => (
          <g key={`y-${y}`}>
            <line
              x1={MARGIN.left}
              x2={WIDTH - MARGIN.right}
              y1={yScale(y)}
              y2={yScale(y)}
              className="step-chart-gridline"
            />
            <text x={MARGIN.left - 8} y={yScale(y)} className="step-chart-tick" textAnchor="end" dy="0.32em">
              {y}
            </text>
          </g>
        ))}
        {xTicks.map((x) => (
          <text
            key={`x-${x}`}
            x={xScale(x)}
            y={HEIGHT - MARGIN.bottom + 18}
            className="step-chart-tick"
            textAnchor="middle"
          >
            {x}
          </text>
        ))}
        <line
          x1={MARGIN.left}
          x2={MARGIN.left}
          y1={MARGIN.top}
          y2={HEIGHT - MARGIN.bottom}
          className="step-chart-axis"
        />
        <line
          x1={MARGIN.left}
          x2={WIDTH - MARGIN.right}
          y1={HEIGHT - MARGIN.bottom}
          y2={HEIGHT - MARGIN.bottom}
          className="step-chart-axis"
        />
        {series.map((s) => (
          <path
            key={s.name}
            d={buildStepPath(s.points, xScale, yScale)}
            fill="none"
            stroke={s.color}
            strokeWidth="2.5"
          />
        ))}
        <text
          x={(MARGIN.left + WIDTH - MARGIN.right) / 2}
          y={HEIGHT - 4}
          className="step-chart-label"
          textAnchor="middle"
        >
          {x_label}
        </text>
        <text
          x={-(HEIGHT / 2)}
          y={12}
          className="step-chart-label"
          textAnchor="middle"
          transform="rotate(-90)"
        >
          {y_label}
        </text>
      </svg>
      <div className="step-chart-legend">
        {series.map((s) => (
          <span key={s.name} className="step-chart-legend-item">
            <span className="step-chart-swatch" style={{ background: s.color }} />
            {s.name}
          </span>
        ))}
      </div>
    </div>
  )
}

export default function StepChart({ charts }) {
  if (!Array.isArray(charts) || charts.length === 0) return null
  return (
    <div className="step-chart-group">
      {charts.map((chart, idx) => (
        <SingleChart key={chart.title || idx} {...chart} />
      ))}
    </div>
  )
}
