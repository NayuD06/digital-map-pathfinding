// Hàm gọi API backend, đọc địa chỉ từ import.meta.env.VITE_API_URL
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request(method, path, params = {}) {
  const url = new URL(path, API_URL)
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== '') url.searchParams.set(key, value)
  })

  let res
  try {
    res = await fetch(url, { method })
  } catch {
    throw new Error(`Không kết nối được backend tại ${API_URL}`)
  }

  if (!res.ok) {
    const body = await res.json().catch(() => null)
    const detail = body?.detail
    throw new Error(typeof detail === 'string' ? detail : `Lỗi ${res.status} từ backend`)
  }
  return res.json()
}

const get = (path, params) => request('GET', path, params)

const pointParams = (from, to) => ({
  from_lat: from.lat,
  from_lng: from.lng,
  to_lat: to.lat,
  to_lng: to.lng,
})

export const getGraphInfo = () => get('/api/graph/info')

export const findRoute = (algo, from, to) => get('/api/route', { algo, ...pointParams(from, to) })

export const compareRoutes = (from, to) => get('/api/compare', pointParams(from, to))

export const getHistory = (limit = 10) => get('/api/history', { limit })

export const runBenchmark = (n, seed) => request('POST', '/api/benchmark', { n, seed })
