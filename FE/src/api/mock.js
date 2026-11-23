// CHỈ DÀNH CHO DEMO FRONTEND (VITE_USE_MOCK=true).
// Hình dạng đường: thử lấy từ dịch vụ demo OSRM công khai (không phải thuật toán nhóm).
// OSRM nhận tọa độ A/B gửi tới máy chủ bên ngoài; cần Internet.
// Thời gian chạy / số node bên dưới đều là SỐ LIỆU MINH HỌA, KHÔNG dùng trong báo cáo.
const graphInfo = {
  place_name: 'District 1, Ho Chi Minh City, Vietnam',
  node_count: 0, edge_count: 0,
  bbox: [10.7632, 106.6825, 10.7966, 106.7135],
  center: [10.7769, 106.7009],
}
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))
export async function getGraphInfo() { await sleep(150); return graphInfo }

const geoDistance = (a, b) => {
  const rad = Math.PI / 180
  const dLat = (b.lat - a.lat) * rad
  const dLng = (b.lng - a.lng) * rad
  const h = Math.sin(dLat / 2) ** 2 + Math.cos(a.lat * rad) * Math.cos(b.lat * rad) * Math.sin(dLng / 2) ** 2
  return 12742000 * Math.asin(Math.sqrt(h))
}

// Trả về đường dạng [[lat, lng], ...] giống API BE.
// OSRM trả về GeoJSON [lng, lat]; bắt buộc đảo lại cho Leaflet.
async function roadGeometry(from, to) {
  const coords = `${from.lng},${from.lat};${to.lng},${to.lat}`
  const url = `https://router.project-osrm.org/route/v1/driving/${coords}?overview=full&geometries=geojson&steps=false`
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), 6500)
  try {
    const response = await fetch(url, { signal: controller.signal })
    if (!response.ok) throw new Error(`OSRM HTTP ${response.status}`)
    const body = await response.json()
    const route = body?.routes?.[0]
    const points = route?.geometry?.coordinates
    if (body.code !== 'Ok' || !Array.isArray(points) || points.length < 2) {
      throw new Error('OSRM không trả về tuyến hợp lệ')
    }
    return {
      path: points.map(([lng, lat]) => [lat, lng]),
      distance_m: route.distance,
      route_source: 'osrm-demo',
    }
  } finally {
    clearTimeout(timeout)
  }
}

async function routeShape(from, to) {
  try {
    return await roadGeometry(from, to)
  } catch (error) {
    console.warn('Không lấy được hình dạng tuyến từ OSRM:', error.message)
    return {
      // Trường hợp không có Internet: nối thẳng A-B, hiển thị NÉT ĐỨT.
      // Không cố mô phỏng đường phố bằng góc vuông sai thực tế.
      path: [[from.lat, from.lng], [to.lat, to.lng]],
      distance_m: geoDistance(from, to),
      route_source: 'straight-fallback',
    }
  }
}

function makeResult(algo, shape) {
  return {
    algorithm: algo,
    path: shape.path,
    route_source: shape.route_source,
    visited: [], // Chưa có node thuật toán thật. Không bịa tọa độ node đã duyệt.
    distance_m: shape.distance_m,
    runtime_ms: algo === 'astar' ? 3.1 : 8.4, // số liệu DEMO
    visited_count: algo === 'astar' ? 426 : 1284, // số liệu DEMO
  }
}
export async function findRoute(algo, from, to) {
  const shape = await routeShape(from, to)
  return makeResult(algo, shape)
}
export async function compareRoutes(from, to) {
  const shape = await routeShape(from, to) // gọi dịch vụ chỉ 1 lần
  return { results: ['dijkstra', 'astar'].map(algo => makeResult(algo, shape)) }
}
