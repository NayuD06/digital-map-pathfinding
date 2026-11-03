// Lịch sử tìm đường lưu trong MySQL; click một dòng để chạy lại trên bản đồ
import { ALGORITHMS, formatDistance } from '../constants.js'

// Backend trả giờ máy chủ không kèm múi giờ, hiển thị dạng "10:05 03/11"
function formatTime(value) {
  const d = new Date(value)
  const pad = (n) => String(n).padStart(2, '0')
  return `${pad(d.getHours())}:${pad(d.getMinutes())} ${pad(d.getDate())}/${pad(d.getMonth() + 1)}`
}

export default function HistoryPanel({ items, error, onSelect }) {
  return (
    <section className="card">
      <h2>Lịch sử tìm đường</h2>
      {error && <p className="error">{error}</p>}
      {!error && items.length === 0 && <p className="muted">Chưa có lần tìm đường nào.</p>}
      {items.length > 0 && (
        <ul className="history">
          {items.map((item) => (
            <li key={item.id}>
              <button className="history-item" onClick={() => onSelect(item)}>
                <span className="swatch" style={{ background: ALGORITHMS[item.algorithm].color }} />
                <span className="history-main">
                  {ALGORITHMS[item.algorithm].label} · {formatDistance(item.distance_m)} ·{' '}
                  {item.visited_count.toLocaleString('vi-VN')} node
                </span>
                <span className="muted">{formatTime(item.created_at)}</span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
