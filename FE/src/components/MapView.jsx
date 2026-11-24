import { useEffect, useMemo } from 'react'
import L from 'leaflet'
import { CircleMarker, MapContainer, Marker, Polyline, Rectangle, TileLayer, useMap, useMapEvents } from 'react-leaflet'
import { ALGORITHMS } from '../constants.js'

const makePin = (type) => L.divIcon({
  html: `<span class="pin-inner">${type === 'start' ? 'A' : 'B'}</span>`,
  className: `location-pin location-pin-${type}`,
  iconSize: [32, 38], iconAnchor: [16, 38],
})
const startIcon = makePin('start')
const endIcon = makePin('end')
function MapClick({ onMapClick }) {
  useMapEvents({ click: e => onMapClick({ lat: e.latlng.lat, lng: e.latlng.lng }) })
  return null
}
function ResizeMap() {
  const map = useMap()
  useEffect(() => {
    // Leaflet phải tính lại kích thước sau khi giao diện thay đổi.
    const element = map.getContainer()
    const observer = typeof ResizeObserver !== 'undefined'
      ? new ResizeObserver(() => map.invalidateSize({ pan: false }))
      : null
    observer?.observe(element)
    map.invalidateSize({ pan: false })
    return () => observer?.disconnect()
  }, [map])
  return null
}
function Recenter({ resetCount, bounds }) {
  const map = useMap()
  useEffect(() => { if (resetCount) map.fitBounds(bounds, { padding: [30, 30] }) }, [map, bounds, resetCount])
  return null
}
function FlyToAddress({ target }) {
  const map = useMap()
  useEffect(() => { if (target) map.flyTo([target.lat, target.lng], Math.max(map.getZoom(), 15), { duration: 0.6 }) }, [map, target])
  return null
}
function DraggableMarker({ point, icon, onMove }) {
  return <Marker position={[point.lat, point.lng]} icon={icon} draggable eventHandlers={{ dragend: e => {
    const latlng = e.target.getLatLng()
    onMove({ lat: latlng.lat, lng: latlng.lng })
  } }} />
}
export default function MapView({ graphInfo, start, end, results, showVisited, onMapClick, onStartMove, onEndMove, resetCount = 0, placeTarget = null }) {
  // useMemo giữ nguyên mảng giữa các lần render, để Recenter chỉ chạy khi bấm nút "Về khu vực bản đồ".
  const bounds = useMemo(() => {
    const [south, west, north, east] = graphInfo.bbox
    return [[south, west], [north, east]]
  }, [graphInfo.bbox])
  const ordered = [...results].sort((a, b) => (b.visited_count || 0) - (a.visited_count || 0))
  return <MapContainer className="map" bounds={bounds} preferCanvas zoomControl={false} scrollWheelZoom>
    <TileLayer attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' url="https://tile.openstreetmap.org/{z}/{x}/{y}.png" />
    {/* Khung bao vùng có dữ liệu bản đồ, để người dùng biết chọn điểm trong vùng nào */}
    <Rectangle bounds={bounds} interactive={false} pathOptions={{ color: '#555', weight: 1, dashArray: '6 6', fill: false }} />
    <ResizeMap />
    <FlyToAddress target={placeTarget} />
    <MapClick onMapClick={onMapClick} />
    <Recenter resetCount={resetCount} bounds={bounds} />
    {showVisited && ordered.map(r => (r.visited || []).map((position, index) =>
      <CircleMarker key={`${r.algorithm}-visited-${index}`} center={position} radius={2} interactive={false}
        pathOptions={{ color: ALGORITHMS[r.algorithm]?.color || '#2682d8', stroke: false, fillOpacity: 0.22 }} />))}
    {ordered.map((r, index) => <Polyline key={`${r.algorithm}-${index}`} positions={r.path || []} interactive={false}
      pathOptions={{ color: ALGORITHMS[r.algorithm]?.color || '#2682d8', weight: ordered.length > 1 && index === 0 ? 9 : 5, opacity: 0.95 }} />)}
    {start && <DraggableMarker point={start} icon={startIcon} onMove={onStartMove} />}
    {end && <DraggableMarker point={end} icon={endIcon} onMove={onEndMove} />}
  </MapContainer>
}
