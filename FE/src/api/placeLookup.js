// Tra cứu địa chỉ qua Nominatim. Giới hạn tối đa ~1 yêu cầu/giây trên cùng tab, có cache.
// Không lưu tọa độ thành nhãn người dùng. Khi mất mạng hiển thị nhãn trung tính.
const cache = new Map()
let queue = Promise.resolve()
let lastCall = 0
const keyFor = ({ lat, lng }) => `${Number(lat).toFixed(5)},${Number(lng).toFixed(5)}`
export function fromSearch(place) {
  const display = String(place.display_name || place.name || '').trim()
  const parts = display.split(',').map(s => s.trim()).filter(Boolean)
  return { lat: Number(place.lat), lng: Number(place.lng ?? place.lon), name: place.title || parts[0] || 'Địa điểm đã chọn', address: place.addressText || display || 'Chưa có địa chỉ chi tiết' }
}
export async function resolvePlace(point) {
  if (!point) return null
  const existing = fromSearch(point)
  if (point.address && point.name && point.name !== 'Vị trí đã chọn') return { ...existing, name: point.name, address: point.address }
  const key = keyFor(point)
  if (cache.has(key)) return cache.get(key)
  const job = queue.catch(() => {}).then(async () => {
    const elapsed = Date.now() - lastCall
    if (elapsed < 1150) await new Promise(r => setTimeout(r, 1150 - elapsed))
    lastCall = Date.now()
    const controller = new AbortController()
    const timer = setTimeout(() => controller.abort(), 7000)
    try {
      const url = new URL('https://nominatim.openstreetmap.org/reverse')
      url.search = new URLSearchParams({ format: 'jsonv2', lat: String(point.lat), lon: String(point.lng), zoom: '18', addressdetails: '1', 'accept-language': 'vi' })
      const response = await fetch(url, { signal: controller.signal, headers: { Accept: 'application/json' } })
      if (!response.ok) throw new Error('Tra cứu địa chỉ không khả dụng')
      const data = await response.json()
      const a = data.address || {}
      const name = data.name || a.amenity || a.building || a.tourism || a.shop || a.road || a.neighbourhood || 'Vị trí đã chọn'
      const result = { lat: point.lat, lng: point.lng, name, address: data.display_name || 'Chưa có địa chỉ chi tiết' }
      cache.set(key, result)
      return result
    } catch {
      return { lat: point.lat, lng: point.lng, name: point.name || 'Vị trí đã chọn', address: point.address || 'Chưa xác định được địa chỉ (kiểm tra kết nối mạng)' }
    } finally { clearTimeout(timer) }
  })
  queue = job
  return job
}
