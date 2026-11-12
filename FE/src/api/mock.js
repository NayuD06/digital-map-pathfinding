// Dữ liệu giả đúng định dạng API, để làm giao diện khi BE chưa xong.
// Bật bằng VITE_USE_MOCK=true trong FE/.env.

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

const GRAPH_INFO = {
  place_name: 'District 1, Ho Chi Minh City, Vietnam (dữ liệu giả)',
  node_count: 2481,
  edge_count: 5683,
  bbox: [10.7632, 106.6825, 10.7966, 106.7135],
  center: [10.7769, 106.7009],
}

// Đường gấp khúc qua 1 điểm trung gian, nút đã duyệt rải quanh điểm đi
function fakeRoute(algo, from, to) {
  const corner = [from.lat, to.lng]
  const path = [[from.lat, from.lng], corner, [to.lat, to.lng]]
  const spread = algo === 'astar' ? 0.3 : 1
  const count = algo === 'astar' ? 120 : 400
  const dLat = to.lat - from.lat
  const dLng = to.lng - from.lng
  const visited = Array.from({ length: count }, (_, i) => {
    const t = i / count
    const angle = i * 2.399
    return [
      from.lat + dLat * t + Math.sin(angle) * t * spread * Math.abs(dLng || 0.005),
      from.lng + dLng * t + Math.cos(angle) * t * spread * Math.abs(dLat || 0.005),
    ]
  })
  const meters = (Math.abs(dLat) + Math.abs(dLng)) * 111_000
  return {
    algorithm: algo,
    path,
    visited,
    distance_m: Math.round(meters * 10) / 10,
    runtime_ms: algo === 'astar' ? 1.8 : 5.2,
    visited_count: count,
  }
}

export async function getGraphInfo() {
  await delay(200)
  return GRAPH_INFO
}

export async function findRoute(algo, from, to) {
  await delay(300)
  return fakeRoute(algo, from, to)
}

export async function compareRoutes(from, to) {
  await delay(400)
  return { results: ['dijkstra', 'astar'].map((algo) => fakeRoute(algo, from, to)) }
}
