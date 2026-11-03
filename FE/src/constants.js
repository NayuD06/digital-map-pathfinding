// Tên hiển thị và màu của từng thuật toán, dùng chung cho bản đồ, bảng số liệu, biểu đồ
export const ALGORITHMS = {
  dijkstra: { label: 'Dijkstra', color: '#e8590c' },
  astar: { label: 'A*', color: '#1971c2' },
}

export function formatDistance(m) {
  return m >= 1000 ? `${(m / 1000).toFixed(2)} km` : `${Math.round(m)} m`
}
