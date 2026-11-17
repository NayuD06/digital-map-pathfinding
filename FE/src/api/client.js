// Hàm gọi API backend, đọc địa chỉ từ import.meta.env.VITE_API_URL
// Định dạng dữ liệu theo BE/app/schemas.py.
// Đặt VITE_USE_MOCK=true trong FE/.env để dùng dữ liệu giả (mock.js) khi BE chưa chạy.
import * as mock from './mock.js'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'

async function get(path, params = {}) {
  const url = new URL(path, API_URL)
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') url.searchParams.set(key, value)
  })

  let res
  try {
    res = await fetch(url)
  } catch {
    throw new Error(`Không kết nối được backend tại ${API_URL}`)
  }

  if (!res.ok) {
    const body = await res.json().catch(() => null)
    const detail = body?.detail
    // 400, 404, 503: BE trả { detail: "thông báo" }; 422: detail là danh sách lỗi tham số
    throw new Error(typeof detail === 'string' ? detail : `Lỗi ${res.status} từ backend`)
  }
  return res.json()
}

const pointParams = (from, to) => ({
  from_lat: from.lat,
  from_lng: from.lng,
  to_lat: to.lat,
  to_lng: to.lng,
})

/** GET /api/graph/info → { place_name, node_count, edge_count, bbox: [s, w, n, e], center: [lat, lng] } */
export const getGraphInfo = () => (USE_MOCK ? mock.getGraphInfo() : get('/api/graph/info'))

/**
 * GET /api/route
 * @param {'dijkstra'|'astar'} algo
 * @param {{lat: number, lng: number}} from
 * @param {{lat: number, lng: number}} to
 * @returns {Promise<{algorithm, path: number[][], visited: number[][], distance_m, runtime_ms, visited_count}>}
 */
export const findRoute = (algo, from, to) =>
  USE_MOCK ? mock.findRoute(algo, from, to) : get('/api/route', { algo, ...pointParams(from, to) })

/** GET /api/compare → { results: [kết quả như findRoute, mỗi thuật toán một phần tử] } */
export const compareRoutes = (from, to) =>
  USE_MOCK ? mock.compareRoutes(from, to) : get('/api/compare', pointParams(from, to))
