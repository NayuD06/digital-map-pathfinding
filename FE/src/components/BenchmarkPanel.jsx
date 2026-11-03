// Chạy benchmark N cặp điểm ngẫu nhiên, xem số liệu trung bình, biểu đồ và tải CSV
import { useState } from 'react'
import { CartesianGrid, Legend, ResponsiveContainer, Scatter, ScatterChart, Tooltip, XAxis, YAxis } from 'recharts'
import { runBenchmark } from '../api/client.js'
import { ALGORITHMS } from '../constants.js'
import CompareChart from './CompareChart.jsx'

const CSV_COLUMNS = ['pair_index', 'algorithm', 'start_node', 'goal_node', 'straight_m', 'distance_m', 'runtime_ms', 'visited_count']

function downloadCsv(result) {
  const lines = [CSV_COLUMNS.join(','), ...result.rows.map((row) => CSV_COLUMNS.map((c) => row[c]).join(','))]
  // BOM để Excel đọc đúng UTF-8
  const blob = new Blob(['\ufeff' + lines.join('\n')], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `benchmark-${result.run_id ?? 'local'}-seed${result.seed}.csv`
  a.click()
  URL.revokeObjectURL(url)
}

// Số node duyệt theo khoảng cách đường chim bay: thấy A* càng lợi khi 2 điểm càng xa
function VisitedByDistance({ rows }) {
  return (
    <div className="chart">
      <h3>Số node đã duyệt theo khoảng cách đường chim bay</h3>
      <ResponsiveContainer width="100%" height={220}>
        <ScatterChart margin={{ top: 8, right: 8, bottom: 8, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            type="number"
            dataKey="straight_m"
            name="Khoảng cách (m)"
            tickFormatter={(v) => `${(v / 1000).toFixed(1)} km`}
          />
          <YAxis type="number" dataKey="visited_count" name="Node đã duyệt" width={40} />
          <Tooltip formatter={(value) => Math.round(value).toLocaleString('vi-VN')} />
          <Legend />
          {Object.entries(ALGORITHMS).map(([key, { label, color }]) => (
            <Scatter
              key={key}
              name={label}
              data={rows.filter((r) => r.algorithm === key)}
              fill={color}
              fillOpacity={0.7}
              isAnimationActive={false}
            />
          ))}
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  )
}

export default function BenchmarkPanel({ databaseEnabled }) {
  const [pairCount, setPairCount] = useState(50)
  const [seed, setSeed] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleRun() {
    setLoading(true)
    setError(null)
    try {
      setResult(await runBenchmark(pairCount, seed))
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  // Đưa số liệu trung bình về cùng dạng kết quả tìm đường để dùng lại CompareChart
  const averages = result?.summary.map((s) => ({
    algorithm: s.algorithm,
    distance_m: s.avg_distance_m,
    runtime_ms: s.avg_runtime_ms,
    visited_count: s.avg_visited_count,
  }))

  return (
    <>
      <section className="card">
        <p className="hint">Chạy cả 2 thuật toán trên N cặp điểm ngẫu nhiên trong quận.</p>
        <div className="form-row">
          <label>
            Số cặp điểm
            <input
              type="number"
              min={1}
              max={500}
              value={pairCount}
              onChange={(e) => setPairCount(Number(e.target.value))}
            />
          </label>
          <label>
            Seed (tùy chọn)
            <input type="number" value={seed} placeholder="ngẫu nhiên" onChange={(e) => setSeed(e.target.value)} />
          </label>
        </div>
        <div className="buttons">
          <button className="primary" disabled={loading || pairCount < 1} onClick={handleRun}>
            {loading ? 'Đang chạy…' : 'Chạy benchmark'}
          </button>
          <button disabled={!result} onClick={() => downloadCsv(result)}>
            Tải CSV
          </button>
        </div>
        {error && <p className="error">{error}</p>}
        {result && (
          <p className="muted">
            {result.pair_count} cặp, seed {result.seed} ·{' '}
            {result.run_id ? `đã lưu vào database (run #${result.run_id})` : 'không lưu (chưa cấu hình database)'}
          </p>
        )}
        {!databaseEnabled && !result && (
          <p className="muted">Chưa cấu hình MySQL: vẫn chạy được nhưng kết quả không được lưu lại.</p>
        )}
      </section>

      {result && (
        <>
          <CompareChart title="Trung bình" results={averages} />
          <section className="card">
            <p>
              A* chạy nhanh hơn Dijkstra ở{' '}
              <strong>
                {result.astar_faster_count}/{result.pair_count}
              </strong>{' '}
              cặp điểm.
            </p>
            <VisitedByDistance rows={result.rows} />
          </section>
        </>
      )}
    </>
  )
}
