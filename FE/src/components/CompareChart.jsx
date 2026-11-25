import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { ALGORITHMS } from '../constants.js'

const numberFormat = new Intl.NumberFormat('vi-VN', { maximumFractionDigits: 3 })

function MetricChart({ title, data, metric, unit, allowDecimals }) {
  return (
    <div className="comparison-chart-metric">
      <h3>{title}</h3>
      <ResponsiveContainer width="100%" height={145} minWidth={0}>
        <BarChart data={data} margin={{ top: 6, right: 8, left: 0, bottom: 0 }}>
          <CartesianGrid vertical={false} stroke="#e6edf4" strokeDasharray="3 3" />
          <XAxis dataKey="label" tick={{ fontSize: 11 }} tickLine={false} />
          <YAxis width={52} tick={{ fontSize: 10 }} tickLine={false} allowDecimals={allowDecimals} />
          <Tooltip formatter={(value) => [`${numberFormat.format(value)} ${unit}`, title]} />
          <Bar dataKey={metric} name={title} maxBarSize={52} radius={[4, 4, 0, 0]} isAnimationActive={false} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default function CompareChart({ results }) {
  const data = results.map(result => ({
    ...result,
    label: ALGORITHMS[result.algorithm].label,
    fill: ALGORITHMS[result.algorithm].color,
  }))

  return (
    <section className="comparison-chart" aria-labelledby="comparison-chart-heading">
      <h2 id="comparison-chart-heading">So sánh hiệu năng</h2>
      <MetricChart title="Thời gian chạy (ms)" data={data} metric="runtime_ms" unit="ms" allowDecimals />
      <MetricChart title="Số nút đã duyệt" data={data} metric="visited_count" unit="nút" allowDecimals={false} />
    </section>
  )
}
