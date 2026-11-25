import { ALGORITHMS, formatDistance } from '../constants.js'

const runtimeFormat = new Intl.NumberFormat('vi-VN', { maximumFractionDigits: 3 })

export default function StatsPanel({ results, mockMode }) {
  if (results.length === 0) return null

  const rows = [
    [mockMode ? 'Độ dài minh họa' : 'Độ dài đường đi', (result) => formatDistance(result.distance_m)],
    ['Thời gian chạy', (result) => mockMode ? '—' : `${runtimeFormat.format(result.runtime_ms)} ms`],
    ['Số nút đã duyệt', (result) => mockMode ? '—' : result.visited_count.toLocaleString('vi-VN')],
  ]

  return (
    <section className="results-section" aria-label="Số liệu tìm đường">
      <div className="result-title" role="status">
        {mockMode ? 'Tuyến đường minh họa' : '✓ Đã tìm thấy tuyến đường'}
      </div>
      <table className="stats-table">
        <thead>
          <tr>
            <th scope="col">Chỉ số</th>
            {results.map(({ algorithm }) => (
              <th key={algorithm} scope="col">{ALGORITHMS[algorithm]?.label ?? algorithm}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map(([label, format]) => (
            <tr key={label}>
              <th scope="row">{label}</th>
              {results.map((result) => (
                <td key={result.algorithm}>{format(result)}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {mockMode && (
        <p className="route-disclosure">
          Tuyến đường và các nút trên bản đồ là dữ liệu minh họa. Số liệu thuật toán có khi dùng backend của nhóm.
        </p>
      )}
    </section>
  )
}
