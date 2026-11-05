// Hiển thị số liệu: độ dài, thời gian chạy, số node đã duyệt
import { ALGORITHMS, formatDistance } from '../constants.js'

const ROWS = [
  { label: 'Độ dài đường đi', format: (r) => formatDistance(r.distance_m) },
  { label: 'Thời gian chạy', format: (r) => `${r.runtime_ms.toFixed(2)} ms` },
  { label: 'Số node đã duyệt', format: (r) => r.visited_count.toLocaleString('vi-VN') },
]

export default function StatsPanel({ results }) {
  if (results.length === 0) return null
  // Backend chỉ trả về tối đa vài nghìn node đã duyệt (lấy mẫu đều) để bản đồ không bị đơ
  const sampled = results.find((r) => r.visited.length < r.visited_count)

  return (
    <section className="card">
      <h2>Kết quả</h2>
      <table className="stats">
        <thead>
          <tr>
            <th />
            {results.map((r) => (
              <th key={r.algorithm} style={{ color: ALGORITHMS[r.algorithm].color }}>
                {ALGORITHMS[r.algorithm].label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {ROWS.map((row) => (
            <tr key={row.label}>
              <th scope="row">{row.label}</th>
              {results.map((r) => (
                <td key={r.algorithm}>{row.format(r)}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {sampled && (
        <p className="muted">
          Bản đồ chỉ vẽ {sampled.visited.length.toLocaleString('vi-VN')} node đã duyệt cho mỗi thuật toán, lấy mẫu
          đều theo thứ tự duyệt.
        </p>
      )}
    </section>
  )
}
