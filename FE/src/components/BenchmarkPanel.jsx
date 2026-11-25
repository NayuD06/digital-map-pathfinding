import { useState } from 'react'
import { getBenchmark } from '../api/client.js'
import { ALGORITHMS, formatDistance } from '../constants.js'

const formatAverage = new Intl.NumberFormat('vi-VN', { maximumFractionDigits: 2 })
const CSV_COLUMNS = ['pair', 'straight_m', 'algorithm', 'distance_m', 'runtime_ms', 'visited_count']
const SEED = 42

function downloadCsv(rows) {
  const lines = rows.map(row => CSV_COLUMNS.map(column => row[column]).join(','))
  const blob = new Blob([[CSV_COLUMNS.join(','), ...lines].join('\r\n') + '\r\n'], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'benchmark.csv'
  document.body.appendChild(link)
  link.click()
  link.remove()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}

export default function BenchmarkPanel() {
  const [input, setInput] = useState('50')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function run(event) {
    event.preventDefault()
    const n = Number(input)
    if (loading || !Number.isInteger(n) || n < 1 || n > 500) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      setResult({ requested: n, data: await getBenchmark(n, SEED) })
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const data = result?.data

  return (
    <details className="benchmark-panel">
      <summary>Đánh giá thực nghiệm (Benchmark)</summary>
      <form className="benchmark-form" onSubmit={run}>
        <label htmlFor="benchmark-pairs">Số cặp điểm (1–500)</label>
        <input
          id="benchmark-pairs"
          type="number"
          min="1"
          max="500"
          step="1"
          required
          value={input}
          disabled={loading}
          onChange={event => setInput(event.target.value)}
        />
        <button className="primary-action" type="submit" disabled={loading}>Chạy benchmark</button>
      </form>
      {loading && <p className="benchmark-status" role="status">Đang chạy benchmark…</p>}
      {error && <p className="error" role="alert">{error}</p>}
      {data && (
        <>
          <p className="benchmark-status" role="status">
            {data.pair_count === 0
              ? 'Không tìm được cặp điểm có đường đi để đo.'
              : `Đã đo ${data.pair_count}/${result.requested} cặp điểm (seed ${SEED}).`}
          </p>
          {data.pair_count > 0 && (
            <>
              <table className="stats-table" aria-label="Số liệu benchmark trung bình">
                <thead>
                  <tr>
                    <th scope="col">Chỉ số trung bình</th>
                    {data.summary.map(({ algorithm }) => (
                      <th scope="col" key={algorithm}>{ALGORITHMS[algorithm].label}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <th scope="row">Độ dài</th>
                    {data.summary.map(row => <td key={row.algorithm}>{formatDistance(row.avg_distance_m)}</td>)}
                  </tr>
                  <tr>
                    <th scope="row">Thời gian</th>
                    {data.summary.map(row => <td key={row.algorithm}>{formatAverage.format(row.avg_runtime_ms)} ms</td>)}
                  </tr>
                  <tr>
                    <th scope="row">Số nút đã duyệt</th>
                    {data.summary.map(row => <td key={row.algorithm}>{formatAverage.format(row.avg_visited_count)}</td>)}
                  </tr>
                </tbody>
              </table>
              <button className="benchmark-download" type="button" onClick={() => downloadCsv(data.rows)}>Tải CSV</button>
            </>
          )}
        </>
      )}
    </details>
  )
}
