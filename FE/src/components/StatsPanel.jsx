// Hiển thị số liệu: độ dài, thời gian chạy, số node đã duyệt
import { ALGORITHMS, formatDistance } from '../constants.js'

const ROWS = [
  { label: 'Độ dài đường đi', format: (r) => formatDistance(r.distance_m) },
  { label: 'Thời gian chạy', format: (r) => `${r.runtime_ms.toFixed(2)} ms` },
  { label: 'Số node đã duyệt', format: (r) => r.visited_count.toLocaleString('vi-VN') },
]

export default function StatsPanel({ results }) {
  if (results.length === 0) return null

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
    </section>
  )
}
