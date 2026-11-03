// Biểu đồ Recharts so sánh hiệu năng các thuật toán
import { Bar, BarChart, Cell, LabelList, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { ALGORITHMS } from '../constants.js'

function MetricChart({ title, data, dataKey, format }) {
  return (
    <div className="chart">
      <h3>{title}</h3>
      <ResponsiveContainer width="100%" height={100}>
        <BarChart data={data} layout="vertical" margin={{ top: 0, right: 64, bottom: 0, left: 0 }}>
          <XAxis type="number" hide />
          <YAxis type="category" dataKey="label" width={72} tickLine={false} axisLine={false} />
          <Tooltip formatter={(value) => format(value)} cursor={{ fill: 'rgba(0,0,0,0.04)' }} />
          <Bar dataKey={dataKey} isAnimationActive={false} barSize={22}>
            {data.map((d) => (
              <Cell key={d.label} fill={d.color} />
            ))}
            <LabelList dataKey={dataKey} position="right" formatter={format} />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default function CompareChart({ results, title = 'So sánh' }) {
  const data = results.map((r) => ({ ...r, ...ALGORITHMS[r.algorithm] }))
  const dijkstra = results.find((r) => r.algorithm === 'dijkstra')
  const astar = results.find((r) => r.algorithm === 'astar')

  return (
    <section className="card">
      <h2>{title}</h2>
      {dijkstra && astar && (
        <p className="summary">
          A* duyệt ít hơn{' '}
          <strong>{Math.round((1 - astar.visited_count / dijkstra.visited_count) * 100)}%</strong> số node so với
          Dijkstra, độ dài đường đi chênh{' '}
          <strong>{Math.abs(astar.distance_m - dijkstra.distance_m).toFixed(1)} m</strong>.
        </p>
      )}
      <MetricChart
        title="Số node đã duyệt"
        data={data}
        dataKey="visited_count"
        format={(v) => Math.round(v).toLocaleString('vi-VN')}
      />
      <MetricChart title="Thời gian chạy (ms)" data={data} dataKey="runtime_ms" format={(v) => v.toFixed(2)} />
    </section>
  )
}
