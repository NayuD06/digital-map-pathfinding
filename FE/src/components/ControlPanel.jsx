// Chọn thuật toán (Dijkstra / A*), nút Tìm đường và So sánh
import { ALGORITHMS } from '../constants.js'

export default function ControlPanel({
  algo,
  onAlgoChange,
  canRun,
  loading,
  showVisited,
  onShowVisitedChange,
  onFind,
  onCompare,
  onClear,
  hint,
  error,
}) {
  return (
    <section className="card">
      <p className="hint">{hint}</p>

      <fieldset className="algo-picker">
        <legend>Thuật toán</legend>
        {Object.entries(ALGORITHMS).map(([key, { label, color }]) => (
          <label key={key}>
            <input type="radio" name="algo" value={key} checked={algo === key} onChange={() => onAlgoChange(key)} />
            <span className="swatch" style={{ background: color }} />
            {label}
          </label>
        ))}
      </fieldset>

      <div className="buttons">
        <button className="primary" disabled={!canRun || loading} onClick={onFind}>
          Tìm đường
        </button>
        <button disabled={!canRun || loading} onClick={onCompare}>
          So sánh
        </button>
        <button disabled={loading} onClick={onClear}>
          Xóa
        </button>
      </div>

      <label className="toggle">
        <input type="checkbox" checked={showVisited} onChange={(e) => onShowVisitedChange(e.target.checked)} />
        Hiện node đã duyệt
      </label>

      {loading && <p className="muted">Đang tìm đường…</p>}
      {error && <p className="error">{error}</p>}
    </section>
  )
}
