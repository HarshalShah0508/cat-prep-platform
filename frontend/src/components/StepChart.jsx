const WIDTH = 800
const HEIGHT = 400
const MARGIN = { top: 20, right: 24, bottom: 46, left: 60 }
const INNER_WIDTH = WIDTH - MARGIN.left - MARGIN.right
const INNER_HEIGHT = HEIGHT - MARGIN.top - MARGIN.bottom

function niceStep(range) {
  const roughStep = range / 7
  const magnitude = 10 ** Math.floor(Math.log10(roughStep || 1))
  const normalized = roughStep / magnitude
  let niceNormalized
  if (normalized <= 1) niceNormalized = 1
  else if (normalized <= 2) niceNormalized = 2
  else if (normalized <= 5) niceNormalized = 5
  else niceNormalized = 10
  return Math.max(niceNormalized * magnitude, 1)
}

function tickRange(min, max) {
  const step = niceStep(max - min)
  const start = Math.ceil(min / step) * step
  const ticks = []
  for (let v = start; v <= max + 1e-9; v += step) ticks.push(Math.round(v * 100) / 100)
  return ticks
}

function buildStepPath(points, xScale, yScale) {
  if (!points || points.length === 0) return ''
  let d = `M ${xScale(points[0][0])} ${yScale(points[0][1])}`
  for (let i = 1; i < points.length; i++) {
    const [x, y] = points[i]
    const [, prevY] = points[i - 1]
    d += ` L ${xScale(x)} ${yScale(prevY)} L ${xScale(x)} ${yScale(y)}`
  }
  return d
}

function ChartFrame({ title, x_label, y_label, xTicks, yTicks, xScale, yScale, xAxisY, yAxisX, children, legend }) {
  return (
    <div className="step-chart">
      {title && <div className="step-chart-title">{title}</div>}
      <svg viewBox={`0 0 ${WIDTH} ${HEIGHT}`} className="step-chart-svg" role="img" aria-label={title || 'chart'}>
        {yTicks.map((y) => (
          <g key={`y-${y}`}>
            <line x1={MARGIN.left} x2={WIDTH - MARGIN.right} y1={yScale(y)} y2={yScale(y)} className="step-chart-gridline" />
            <text x={MARGIN.left - 8} y={yScale(y)} className="step-chart-tick" textAnchor="end" dy="0.32em">
              {y}
            </text>
          </g>
        ))}
        {xTicks.map((x) => (
          <g key={`x-${x}`}>
            <line x1={xScale(x)} x2={xScale(x)} y1={MARGIN.top} y2={HEIGHT - MARGIN.bottom} className="step-chart-gridline" />
            <text x={xScale(x)} y={HEIGHT - MARGIN.bottom + 18} className="step-chart-tick" textAnchor="middle">
              {x}
            </text>
          </g>
        ))}
        <line x1={yAxisX} x2={yAxisX} y1={MARGIN.top} y2={HEIGHT - MARGIN.bottom} className="step-chart-axis" />
        <line x1={MARGIN.left} x2={WIDTH - MARGIN.right} y1={xAxisY} y2={xAxisY} className="step-chart-axis" />
        {children}
        <text x={(MARGIN.left + WIDTH - MARGIN.right) / 2} y={HEIGHT - 4} className="step-chart-label" textAnchor="middle">
          {x_label}
        </text>
        <text x={-(HEIGHT / 2)} y={14} className="step-chart-label" textAnchor="middle" transform="rotate(-90)">
          {y_label}
        </text>
      </svg>
      {legend && <div className="step-chart-legend">{legend}</div>}
    </div>
  )
}

function StepLineChart({ title, x_label, y_label, x_max, y_max, series }) {
  const xMax = x_max ?? Math.max(1, ...series.flatMap((s) => s.points.map((p) => p[0])))
  const yMax = y_max ?? Math.max(1, ...series.flatMap((s) => s.points.map((p) => p[1])))
  const xScale = (x) => MARGIN.left + (x / xMax) * INNER_WIDTH
  const yScale = (y) => MARGIN.top + INNER_HEIGHT - (y / yMax) * INNER_HEIGHT

  const xTicks = tickRange(0, xMax)
  const yTicks = []
  for (let y = 0; y <= yMax; y += 1) yTicks.push(y)

  return (
    <ChartFrame
      title={title}
      x_label={x_label}
      y_label={y_label}
      xTicks={xTicks}
      yTicks={yTicks}
      xScale={xScale}
      yScale={yScale}
      xAxisY={yScale(0)}
      yAxisX={xScale(0)}
      legend={series.map((s) => (
        <span key={s.name} className="step-chart-legend-item">
          <span className="step-chart-swatch" style={{ background: s.color }} />
          {s.name}
        </span>
      ))}
    >
      {series.map((s) => (
        <path key={s.name} d={buildStepPath(s.points, xScale, yScale)} fill="none" stroke={s.color} strokeWidth="2.5" />
      ))}
    </ChartFrame>
  )
}

function BarChart({ title, x_label, y_label, categories, values, y_max, color = '#4338ca' }) {
  const yMax = y_max ?? Math.max(1, ...values)
  const yScale = (y) => MARGIN.top + INNER_HEIGHT - (y / yMax) * INNER_HEIGHT
  const bandWidth = INNER_WIDTH / categories.length
  const barWidth = bandWidth * 0.55

  const yTicks = tickRange(0, yMax)

  return (
    <ChartFrame
      title={title}
      x_label={x_label}
      y_label={y_label}
      xTicks={[]}
      yTicks={yTicks}
      xScale={() => 0}
      yScale={yScale}
      xAxisY={yScale(0)}
      yAxisX={MARGIN.left}
    >
      {categories.map((cat, idx) => {
        const bandCenter = MARGIN.left + bandWidth * (idx + 0.5)
        const barX = bandCenter - barWidth / 2
        const barTop = yScale(values[idx])
        const barHeight = yScale(0) - barTop
        return (
          <g key={cat}>
            <rect x={barX} y={barTop} width={barWidth} height={barHeight} fill={color} />
            <text x={bandCenter} y={HEIGHT - MARGIN.bottom + 18} className="step-chart-tick" textAnchor="middle">
              {cat}
            </text>
            <text x={bandCenter} y={barTop - 6} className="step-chart-tick" textAnchor="middle">
              {values[idx]}
            </text>
          </g>
        )
      })}
    </ChartFrame>
  )
}

function ScatterChart({ title, x_label, y_label, x_min, x_max, y_min, y_max, points, color = '#4338ca' }) {
  const xScale = (x) => MARGIN.left + ((x - x_min) / (x_max - x_min)) * INNER_WIDTH
  const yScale = (y) => MARGIN.top + INNER_HEIGHT - ((y - y_min) / (y_max - y_min)) * INNER_HEIGHT

  const xTicks = tickRange(x_min, x_max)
  const yTicks = tickRange(y_min, y_max)

  return (
    <ChartFrame
      title={title}
      x_label={x_label}
      y_label={y_label}
      xTicks={xTicks}
      yTicks={yTicks}
      xScale={xScale}
      yScale={yScale}
      xAxisY={yScale(0)}
      yAxisX={xScale(0)}
    >
      {points.map((p) => (
        <g key={p.label}>
          <circle cx={xScale(p.x)} cy={yScale(p.y)} r="5" fill={color} />
          <text x={xScale(p.x) + 9} y={yScale(p.y)} className="step-chart-tick" dy="0.32em">
            {p.label}
          </text>
        </g>
      ))}
    </ChartFrame>
  )
}

function SingleChart(chart) {
  if (chart.type === 'bar') return <BarChart {...chart} />
  if (chart.type === 'scatter') return <ScatterChart {...chart} />
  return <StepLineChart {...chart} />
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
