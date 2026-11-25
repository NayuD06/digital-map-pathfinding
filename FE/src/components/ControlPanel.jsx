import { ALGORITHMS } from '../constants.js'

export default function ControlPanel({
  algo,
  onAlgoChange,
  canRun,
  canClear,
  loading,
  comparing,
  error,
  showVisited,
  canShowVisited,
  onShowVisitedChange,
  onFind,
  onCompare,
  onClear,
}) {
  return (
    <section className="algorithm-section" aria-labelledby="algorithm-heading">
      <h2 id="algorithm-heading">Thuật toán</h2>
      <div className="algorithm-tabs">
        {Object.entries(ALGORITHMS).map(([key, { label }]) => (
          <button
            type="button"
            key={key}
            className={algo === key ? 'active' : ''}
            aria-pressed={algo === key}
            onClick={() => { if (key !== algo) onAlgoChange(key) }}
          >
            {label}
          </button>
        ))}
      </div>

      <div className="action-area">
        <button type="button" className="primary-action" disabled={!canRun || loading} onClick={onFind}>
          {loading && !comparing ? <span role="status">Đang tìm đường…</span> : '⌁ Tìm đường'}
        </button>
        <div className="action-secondary">
          <button type="button" disabled={!canRun || loading} onClick={onCompare}>
            {comparing ? <span role="status">Đang so sánh…</span> : '◇ So sánh cách tìm đường'}
          </button>
          <button type="button" disabled={!canClear} onClick={onClear}>
            Xóa tuyến
          </button>
        </div>
      </div>

      <label className="visited-control">
        <input
          type="checkbox"
          checked={canShowVisited && showVisited}
          disabled={!canShowVisited}
          onChange={(event) => onShowVisitedChange(event.target.checked)}
        />
        Hiện các nút đã duyệt trên bản đồ
      </label>

      {error && <div className="error" role="alert">{error}</div>}
    </section>
  )
}
