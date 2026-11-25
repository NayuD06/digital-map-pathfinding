// Hàm gọi API backend, đọc địa chỉ từ import.meta.env.VITE_API_URL
// Định dạng dữ liệu theo BE/app/schemas.py.
// Đặt VITE_USE_MOCK=true trong FE/.env để dùng dữ liệu giả (mock.js) khi BE chưa chạy.
import * as mock from './mock.js'
import { ALGORITHMS } from '../constants.js'

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
  try {
    return await res.json()
  } catch {
    throw new Error('Dữ liệu trả về từ backend không hợp lệ')
  }
}

const pointParams = (from, to) => ({
  from_lat: from.lat,
  from_lng: from.lng,
  to_lat: to.lat,
  to_lng: to.lng,
})

const algorithms = Object.keys(ALGORITHMS)
const nonNegative = (value) => Number.isFinite(value) && value >= 0
const count = (value) => Number.isSafeInteger(value) && value >= 0

function validPoint(point) {
  return Array.isArray(point) && point.length === 2
    && Number.isFinite(point[0]) && Math.abs(point[0]) <= 90
    && Number.isFinite(point[1]) && Math.abs(point[1]) <= 180
}

function validRoute(route) {
  return route && Array.isArray(route.path) && route.path.length > 0 && route.path.every(validPoint)
    && Array.isArray(route.visited) && route.visited.every(validPoint)
    && nonNegative(route.distance_m) && nonNegative(route.runtime_ms) && count(route.visited_count)
}

/** GET /api/graph/info → { place_name, node_count, edge_count, bbox: [s, w, n, e], center: [lat, lng] } */
export const getGraphInfo = () => (USE_MOCK ? mock.getGraphInfo() : get('/api/graph/info'))

/**
 * GET /api/route
 * @param {'dijkstra'|'astar'} algo
 * @param {{lat: number, lng: number}} from
 * @param {{lat: number, lng: number}} to
 * @returns {Promise<{algorithm, path: number[][], visited: number[][], distance_m, runtime_ms, visited_count}>}
 */
export async function findRoute(algo, from, to) {
  const route = await (USE_MOCK ? mock.findRoute(algo, from, to) : get('/api/route', { algo, ...pointParams(from, to) }))
  if (!validRoute(route) || route.algorithm !== algo) {
    throw new Error('Dữ liệu tuyến đường không hợp lệ')
  }
  return route
}

/** GET /api/compare → { results: [kết quả như findRoute, mỗi thuật toán một phần tử] } */
export async function compareRoutes(from, to) {
  const data = await (USE_MOCK ? mock.compareRoutes(from, to) : get('/api/compare', pointParams(from, to)))
  const results = data?.results
  if (!Array.isArray(results) || results.length !== algorithms.length || !results.every(validRoute)
      || !algorithms.every(name => results.some(route => route.algorithm === name))) {
    throw new Error('Dữ liệu so sánh không hợp lệ')
  }
  return data
}

function validBenchmark(data, requestedPairs) {
  if (!data || !count(data.pair_count) || data.pair_count > requestedPairs
      || !Array.isArray(data.summary) || !Array.isArray(data.rows)
      || data.rows.length !== data.pair_count * algorithms.length) return false

  const { pair_count: pairs, rows, summary } = data
  if (pairs === 0) return summary.length === 0
  return summary.length === algorithms.length
    && summary.every(item => item && nonNegative(item.avg_distance_m)
      && nonNegative(item.avg_runtime_ms) && nonNegative(item.avg_visited_count))
    && algorithms.every(name => summary.some(item => item.algorithm === name))
    && rows.every(row => row && count(row.pair) && row.pair < pairs && algorithms.includes(row.algorithm)
      && nonNegative(row.straight_m) && nonNegative(row.distance_m)
      && nonNegative(row.runtime_ms) && count(row.visited_count))
    && new Set(rows.map(row => `${row.pair}:${row.algorithm}`)).size === rows.length
}

/** Benchmark luôn lấy số liệu từ backend, kể cả khi bản đồ đang ở chế độ demo. */
export async function getBenchmark(n = 50, seed = 42) {
  const data = await get('/api/benchmark', { n, seed })
  if (!validBenchmark(data, n)) {
    throw new Error('Dữ liệu benchmark không hợp lệ')
  }
  return data
}
