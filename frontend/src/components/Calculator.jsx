import { useState } from 'react'

const OPS = {
  '+': (a, b) => a + b,
  '-': (a, b) => a - b,
  '*': (a, b) => a * b,
  '/': (a, b) => (b === 0 ? NaN : a / b),
  '^': (a, b) => Math.pow(a, b),
}

function format(n) {
  if (typeof n !== 'number' || !Number.isFinite(n)) return 'Error'
  const rounded = Math.round(n * 1e10) / 1e10
  return String(rounded)
}

const INITIAL = { display: '0', prevValue: null, operator: null, overwrite: true, memory: 0 }

export default function Calculator({ onClose }) {
  const [state, setState] = useState(INITIAL)
  const { display, prevValue, operator, overwrite, memory } = state

  function inputDigit(d) {
    setState((s) => {
      if (s.overwrite) {
        return { ...s, display: d === '.' ? '0.' : d, overwrite: false }
      }
      if (d === '.' && s.display.includes('.')) return s
      return { ...s, display: s.display === '0' && d !== '.' ? d : s.display + d }
    })
  }

  function applyOperator(op) {
    setState((s) => {
      const current = parseFloat(s.display)
      if (s.operator && !s.overwrite && s.prevValue !== null) {
        const result = OPS[s.operator](s.prevValue, current)
        return { ...s, display: format(result), prevValue: result, operator: op, overwrite: true }
      }
      return { ...s, prevValue: current, operator: op, overwrite: true }
    })
  }

  function equals() {
    setState((s) => {
      if (s.operator === null || s.prevValue === null) return s
      const current = parseFloat(s.display)
      const result = OPS[s.operator](s.prevValue, current)
      return { ...s, display: format(result), prevValue: null, operator: null, overwrite: true }
    })
  }

  function percent() {
    setState((s) => {
      const current = parseFloat(s.display)
      const value = s.operator && s.prevValue !== null ? (s.prevValue * current) / 100 : current / 100
      return { ...s, display: format(value), overwrite: true }
    })
  }

  function sqrt() {
    setState((s) => {
      const current = parseFloat(s.display)
      return { ...s, display: current < 0 ? 'Error' : format(Math.sqrt(current)), overwrite: true }
    })
  }

  function square() {
    setState((s) => {
      const current = parseFloat(s.display)
      return { ...s, display: format(current * current), overwrite: true }
    })
  }

  function toggleSign() {
    setState((s) =>
      s.display === '0'
        ? s
        : { ...s, display: s.display.startsWith('-') ? s.display.slice(1) : '-' + s.display },
    )
  }

  function backspace() {
    setState((s) => {
      if (s.overwrite) return s
      const next = s.display.length > 1 ? s.display.slice(0, -1) : '0'
      return { ...s, display: next === '-' ? '0' : next }
    })
  }

  function clearAll() {
    // C clears the current calculation only - memory persists across it, same as a
    // real calculator; only MC clears memory.
    setState((s) => ({ ...INITIAL, memory: s.memory }))
  }

  function memoryAdd() {
    setState((s) => ({ ...s, memory: s.memory + parseFloat(s.display), overwrite: true }))
  }

  function memorySubtract() {
    setState((s) => ({ ...s, memory: s.memory - parseFloat(s.display), overwrite: true }))
  }

  function memoryRecall() {
    setState((s) => ({ ...s, display: format(s.memory), overwrite: true }))
  }

  function memoryClear() {
    setState((s) => ({ ...s, memory: 0 }))
  }

  const BUTTONS = [
    { label: 'MC', onClick: memoryClear, cls: 'calculator-btn-mem' },
    { label: 'MR', onClick: memoryRecall, cls: 'calculator-btn-mem' },
    { label: 'M+', onClick: memoryAdd, cls: 'calculator-btn-mem' },
    { label: 'M-', onClick: memorySubtract, cls: 'calculator-btn-mem' },
    { label: 'C', onClick: clearAll, cls: '' },
    { label: '←', onClick: backspace, cls: '' },
    { label: '%', onClick: percent, cls: '' },
    { label: '÷', onClick: () => applyOperator('/'), cls: 'calculator-btn-op' },
    { label: '7', onClick: () => inputDigit('7'), cls: '' },
    { label: '8', onClick: () => inputDigit('8'), cls: '' },
    { label: '9', onClick: () => inputDigit('9'), cls: '' },
    { label: '×', onClick: () => applyOperator('*'), cls: 'calculator-btn-op' },
    { label: '4', onClick: () => inputDigit('4'), cls: '' },
    { label: '5', onClick: () => inputDigit('5'), cls: '' },
    { label: '6', onClick: () => inputDigit('6'), cls: '' },
    { label: '−', onClick: () => applyOperator('-'), cls: 'calculator-btn-op' },
    { label: '1', onClick: () => inputDigit('1'), cls: '' },
    { label: '2', onClick: () => inputDigit('2'), cls: '' },
    { label: '3', onClick: () => inputDigit('3'), cls: '' },
    { label: '+', onClick: () => applyOperator('+'), cls: 'calculator-btn-op' },
    { label: '√', onClick: sqrt, cls: '' },
    { label: 'x²', onClick: square, cls: '' },
    { label: 'xʸ', onClick: () => applyOperator('^'), cls: 'calculator-btn-op' },
    { label: '+/-', onClick: toggleSign, cls: '' },
    { label: '0', onClick: () => inputDigit('0'), cls: 'calculator-btn-zero' },
    { label: '.', onClick: () => inputDigit('.'), cls: '' },
  ]

  return (
    <div className="calculator-panel">
      <div className="calculator-header">
        <span>
          Calculator {memory !== 0 && <span className="calculator-memory-tag">M</span>}
        </span>
        <button type="button" className="calculator-close" onClick={onClose} aria-label="Close calculator">
          ×
        </button>
      </div>
      <div className="calculator-display">{display}</div>
      <div className="calculator-grid">
        {BUTTONS.map((btn, idx) =>
          btn.label === null ? (
            <span key={idx} />
          ) : (
            <button
              key={idx}
              type="button"
              className={`calculator-btn ${btn.cls}`}
              onClick={btn.onClick}
            >
              {btn.label}
            </button>
          ),
        )}
        <button type="button" className="calculator-btn calculator-btn-op calculator-btn-equals" onClick={equals}>
          =
        </button>
      </div>
    </div>
  )
}
