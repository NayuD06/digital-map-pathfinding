export const ALGORITHMS = {
  dijkstra: { label: 'Dijkstra', color: '#de8b31' },
  astar: { label: 'A*', color: '#176acc' },
}
export const formatDistance = (metres) => metres >= 1000 ? `${(metres / 1000).toLocaleString('vi-VN', { maximumFractionDigits: 2 })} km` : `${Math.round(metres)} m`
